#!/usr/bin/env python3
"""best_window.py : choisit, pour chaque rush video, la fenetre la plus vivante.

Methode : decodage en 160 px de large a 10 fps (ffmpeg, rawvideo gris) puis
difference absolue moyenne entre frames consecutives (score de mouvement).
On retient la fenetre de duree requise (duree du plan x vitesse + 0,2 s de marge)
qui maximise le mouvement moyen, en evitant les 0,3 premieres secondes et en
preferant demarrer sur une montee de mouvement (cut on action).

Vitesse : `speed` est le playbackRate Remotion (1.0 par defaut). Rattrapage d'un
rush trop court, dans l'ordre : (a) ralenti jusqu'a playbackRate 1/speed_ramp_max ;
(b) boomerang du propre rush (aller-retour, eventuellement ralenti) : la fenetre
couvre alors tout le rush, `boomerang` (alias `padded`) vaut true et `method`
devient "frame-diff+boomerang" ; prep_clips.py construit l'aller-retour sans
image figee. Les substitutions (c) (d) (e) ont deja ete decidees par inventory.py.

Image fixe : in_s = 0, method = "image". Plan MOTION genere : method = "motion".

Sortie : work/windows.json (CONTRACTS.md section 6, champs additionnels : speed,
duration_needed_s, padded, source_method).
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path

import numpy as np

from montage_common import (die, flatten_shots, get_profile, load_json, load_profiles, log,
                    project_root_from_brief, resolve_shot_source, save_json)

ANALYSIS_W = 160
ANALYSIS_FPS = 10
AVOID_START_S = 0.3
SAFETY_S = 0.2
RISE_BONUS = 0.15


def decode_gray(path: Path, width: int, height: int) -> np.ndarray:
    """Frames en niveaux de gris (n, h, w) a ANALYSIS_FPS, largeur ANALYSIS_W."""
    h = max(2, int(round(ANALYSIS_W * height / max(1, width))))
    h += h % 2
    cmd = [
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(path),
        "-vf", f"scale={ANALYSIS_W}:{h},fps={ANALYSIS_FPS}",
        "-f", "rawvideo", "-pix_fmt", "gray", "-",
    ]
    res = subprocess.run(cmd, capture_output=True, check=False, timeout=600)
    if res.returncode != 0 or not res.stdout:
        raise RuntimeError(f"decodage impossible : {res.stderr.decode(errors='ignore')[-500:]}")
    n = len(res.stdout) // (ANALYSIS_W * h)
    arr = np.frombuffer(res.stdout[: n * ANALYSIS_W * h], dtype=np.uint8)
    return arr.reshape(n, h, ANALYSIS_W)


def motion_curve(frames: np.ndarray) -> np.ndarray:
    """Score de mouvement entre frames consecutives (0..1), longueur n-1."""
    if frames.shape[0] < 2:
        return np.zeros(0, dtype=np.float32)
    f = frames.astype(np.int16)
    diff = np.abs(f[1:] - f[:-1]).mean(axis=(1, 2)) / 255.0
    return diff.astype(np.float32)


def pick_window(motion: np.ndarray, dur_s: float, needed_s: float, avoid_start_s: float) -> tuple[float, float, float] | None:
    """Fenetre [in, out] maximisant mouvement moyen + bonus de montee. None si impossible."""
    n = motion.shape[0]
    hop = 1.0 / ANALYSIS_FPS
    wn = max(1, int(math.ceil(needed_s / hop)))
    start_min = int(math.ceil(avoid_start_s / hop))
    last_start = int(math.floor((dur_s - needed_s) / hop))
    last_start = min(last_start, n - wn)
    if last_start < start_min:
        return None
    if n == 0:
        return avoid_start_s, avoid_start_s + needed_s, 0.0
    # Normalisation par le 95e percentile pour un score comparable entre rushes
    p95 = float(np.percentile(motion, 95)) if n > 0 else 0.0
    norm = max(p95, 1e-4)
    csum = np.concatenate([[0.0], np.cumsum(motion, dtype=np.float64)])
    best = None
    for s in range(start_min, last_start + 1):
        e = min(n, s + wn)
        mean = (csum[e] - csum[s]) / max(1, e - s)
        before = motion[max(0, s - 3):s]
        after = motion[s:min(n, s + 3)]
        rise = 0.0
        if before.size and after.size:
            rise = float(np.clip((after.mean() - before.mean()) / norm, -1.0, 1.0))
        score = mean / norm + RISE_BONUS * rise
        if best is None or score > best[0]:
            best = (score, s, mean / norm)
    if best is None:
        return None
    _, s, ms = best
    in_s = s * hop
    return round(in_s, 3), round(in_s + needed_s, 3), round(float(min(1.0, ms)), 3)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Choisit la fenetre la plus dynamique de chaque rush et ecrit work/windows.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("inventory", help="work/inventory.json")
    ap.add_argument("brief", help="brief.json")
    ap.add_argument("--out", required=True, help="chemin de sortie, ex. work/windows.json")
    ap.add_argument("--profiles", default=None, help="assets/profiles.json (defaut : celui du skill)")
    args = ap.parse_args()

    inventory = load_json(args.inventory)
    brief = load_json(args.brief)
    root = project_root_from_brief(args.brief)
    profile = get_profile(load_profiles(args.profiles), brief["project"]["profile"])
    ramp = float(profile.get("speed_ramp_max", 1.0))
    min_rate = 1.0 / ramp if ramp > 0 else 1.0
    by_id = {s["id"]: s for s in inventory["shots"]}

    out_shots: list[dict] = []
    cache: dict[str, np.ndarray] = {}

    for shot in flatten_shots(brief):
        sid = shot["id"]
        plan_dur = float(shot["end"]) - float(shot["start"])
        src_rel, method = resolve_shot_source(sid, inventory)
        entry = {
            "id": sid, "src": src_rel, "in_s": 0.0, "out_s": round(plan_dur + SAFETY_S, 3),
            "motion_score": None, "method": "motion", "speed": 1.0,
            "duration_needed_s": round(plan_dur + SAFETY_S, 3), "padded": False, "boomerang": False,
            "source_method": method,
        }
        if src_rel is None:
            out_shots.append(entry)
            log(f"  {sid} : carte MOTION (aucune source)")
            continue

        src_entry = None
        for e in inventory["shots"]:
            if e.get("file") == src_rel:
                src_entry = e
                break
        src_path = root / src_rel
        if src_entry is None or not src_path.exists():
            die(f"source introuvable pour {sid} : {src_rel}")

        if src_entry.get("is_image"):
            entry["method"] = "image"
            out_shots.append(entry)
            log(f"  {sid} : image fixe, Ken Burns")
            continue

        dur = float(src_entry.get("duration_s") or 0.0)
        try:
            if src_rel not in cache:
                frames = decode_gray(src_path, src_entry["width"], src_entry["height"])
                cache[src_rel] = motion_curve(frames)
            motion = cache[src_rel]
        except RuntimeError as exc:
            log(f"  {sid} : {exc} ; fenetre par defaut")
            motion = np.zeros(max(0, int(dur * ANALYSIS_FPS) - 1), dtype=np.float32)

        # 1) vitesse normale en evitant le debut
        speed = 1.0
        needed = plan_dur * speed + SAFETY_S
        win = pick_window(motion, dur, needed, AVOID_START_S)
        # 2) ralenti jusqu'a 1/speed_ramp_max
        if win is None and dur > 0:
            speed = max(min_rate, min(1.0, (dur - AVOID_START_S - SAFETY_S) / max(plan_dur, 1e-3)))
            needed = plan_dur * speed + SAFETY_S
            win = pick_window(motion, dur, needed, AVOID_START_S)
        # 3) ralenti max sans eviter le debut
        if win is None and dur > 0:
            speed = min_rate
            needed = plan_dur * speed + SAFETY_S
            win = pick_window(motion, dur, needed, 0.0)
        # 4) boomerang du propre rush (aller-retour), vitesse 1 si 2 x duree suffit, sinon ralenti
        if win is None:
            speed = max(min_rate, min(1.0, (2.0 * dur - SAFETY_S) / max(plan_dur, 1e-3)))
            needed = plan_dur * speed + SAFETY_S
            ms = float(np.clip(motion.mean() / max(float(np.percentile(motion, 95)), 1e-4), 0, 1)) if motion.size else 0.0
            entry.update({"in_s": 0.0, "out_s": round(dur, 3), "motion_score": round(ms, 3),
                          "padded": True, "boomerang": True})
        else:
            entry.update({"in_s": win[0], "out_s": win[1], "motion_score": win[2]})
        entry.update({"method": "frame-diff+boomerang" if entry["boomerang"] else "frame-diff",
                      "speed": round(speed, 3), "duration_needed_s": round(needed, 3)})
        out_shots.append(entry)
        extra = f", vitesse {speed:.2f}" if speed != 1.0 else ""
        extra += ", complété en boomerang" if entry["padded"] else ""
        log(f"  {sid} : fenêtre {entry['in_s']:.2f} -> {entry['out_s']:.2f} s (mouvement {entry['motion_score']}){extra}")

    save_json(args.out, {"shots": out_shots})
    log(f"windows : {len(out_shots)} plans -> {args.out}")


if __name__ == "__main__":
    main()
