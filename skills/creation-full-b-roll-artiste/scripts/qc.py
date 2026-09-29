#!/usr/bin/env python3
"""qc.py : controle qualite du montage rendu, score /100 et planche contact.

Controles (poids) :
  couverture audio 100 % (15) ; aucun clip < 0,8 s sauf HOOK >= 0,6 (10) ;
  aucun clip > max du profil (5) ; pas deux `value` identiques consecutives (5) ;
  pas le meme rush reutilise a moins de reuse_min_gap_s (5) ;
  relance (changement de clip, punch, overlay ou transition) dans chaque fenetre
  de relance_max_s (10) ; image qui change dans la premiere seconde du hook (5) ;
  transitions visibles espacees de visible_max_per_window_s (5), le zoomthrough
  reel <-> 3DSCI etant exempte (il reste visible et reinitialise la fenetre) ;
  freezedetect ffmpeg n=0.003 d=0.8 : 0 occurrence (15) ;
  loudness integree dans +/- 1 LU de vo_lufs (10) ;
  duree du fichier = duree de l'audio +/- 0,1 s (10) ;
  planche contact generee (5) : 1 frame au milieu de chaque clip, 4 colonnes.

Chaque echec liste une correction proposee. Sortie : out/qc_report.md et
out/contact_sheet.jpg (a cote du rapport).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from montage_common import (REAL_TYPES, die, ffprobe, ffprobe_duration, get_profile, load_json, load_profiles,
                            log, project_root_from_timeline, resolve_asset, shot_limits)

WEIGHTS = {
    "couverture": 15, "clips_min": 10, "clips_max": 5, "values": 5, "reuse": 5, "relance": 10,
    "hook_change": 5, "transitions": 5, "freeze": 15, "loudness": 10, "duree": 10, "planche": 5,
}


class Check:
    def __init__(self, key: str, name: str, ok: bool, measured: str, threshold: str, fix: str = "") -> None:
        self.key, self.name, self.ok, self.measured, self.threshold, self.fix = key, name, ok, measured, threshold, fix


def freeze_count(video: Path) -> int:
    res = subprocess.run(["ffmpeg", "-v", "info", "-nostdin", "-i", str(video), "-vf", "freezedetect=n=0.003:d=0.8",
                          "-an", "-f", "null", "-"], capture_output=True, text=True)
    return len(re.findall(r"freeze_start", res.stderr))


def measure_loudness(video: Path) -> float | None:
    res = subprocess.run(["ffmpeg", "-v", "info", "-nostdin", "-i", str(video), "-af",
                          "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", res.stderr, re.S)
    if not m:
        return None
    try:
        return float(json.loads(m.group(0))["input_i"])
    except (ValueError, KeyError):
        return None


def has_drawtext() -> bool:
    res = subprocess.run(["ffmpeg", "-v", "quiet", "-filters"], capture_output=True, text=True)
    return " drawtext " in res.stdout


def contact_sheet(video: Path, clips: list[dict], fps: int, out: Path) -> bool:
    cols = 4
    rows = max(1, -(-len(clips) // cols))
    label = has_drawtext()
    with tempfile.TemporaryDirectory() as td:
        for i, c in enumerate(clips):
            t = (c["from_frame"] + c["duration_frames"] / 2) / fps
            vf = "scale=270:480"
            if label:
                txt = str(c["shot_id"]).replace("'", "").replace(":", "")
                vf += f",drawtext=text='{txt}':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=6"
            r = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-ss", f"{t:.3f}", "-i", str(video),
                                "-frames:v", "1", "-vf", vf, f"{td}/{i + 1:03d}.png"], capture_output=True, text=True)
            if r.returncode != 0:
                log(f"planche : frame {c['shot_id']} impossible : {r.stderr[-300:]}")
                return False
        out.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-framerate", "1", "-i", f"{td}/%03d.png",
                            "-vf", f"tile={cols}x{rows}:padding=4:margin=4:color=black", "-frames:v", "1", "-q:v", "3",
                            str(out)], capture_output=True, text=True)
        if r.returncode != 0:
            log(f"planche : mosaique impossible : {r.stderr[-300:]}")
            return False
    return out.exists()


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Controle qualite du rendu final : score /100, rapport Markdown et planche contact.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("timeline", help="work/timeline.json (ou out/timeline.json)")
    ap.add_argument("video", help="out/final_9x16.mp4")
    ap.add_argument("brief", help="brief.json")
    ap.add_argument("--out", required=True, help="rapport, ex. out/qc_report.md")
    ap.add_argument("--profiles", default=None, help="assets/profiles.json (defaut : celui du skill)")
    ap.add_argument("--project", default=None, help="racine du projet (defaut : parent de work/)")
    args = ap.parse_args()

    tl = load_json(args.timeline)
    brief = load_json(args.brief)
    profiles = load_profiles(args.profiles)
    profile = get_profile(profiles, tl["profile"])
    video = Path(args.video)
    if not video.exists():
        die(f"video introuvable : {video}")
    out_md = Path(args.out)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    root = Path(args.project).resolve() if args.project else project_root_from_timeline(Path(args.timeline).resolve())

    fps = int(tl["fps"])
    clips = tl["clips"]
    total = int(tl["duration_frames"])
    audio_dur = float(brief["audio"]["duration_s"])
    checks: list[Check] = []

    # 1. couverture
    gaps = []
    cursor = 0
    for c in clips:
        if c["from_frame"] != cursor:
            gaps.append((cursor, c["from_frame"]))
        cursor = c["from_frame"] + c["duration_frames"]
    end_ok = cursor == total
    dur_ok = abs(total - round(audio_dur * fps)) <= 1
    ok = not gaps and end_ok and dur_ok
    checks.append(Check("couverture", "Couverture audio 100 %", ok,
                        f"{len(gaps)} trou(s), fin des clips = {cursor} / {total} frames, audio = {round(audio_dur * fps)} frames",
                        "0 trou, fin = duration_frames = round(audio*fps)",
                        "relancer build_timeline.py ; verifier que les plans du brief couvrent l'audio sans trou"))

    # 2. duree min
    short = []
    for c in clips:
        d = c["duration_frames"] / fps
        lim = 0.6 if c.get("section") == "HOOK" else 0.8
        if d < lim - 1e-6:
            short.append(f"{c['shot_id']} ({d:.2f} s)")
    checks.append(Check("clips_min", "Aucun clip trop court", not short, ", ".join(short) or "aucun",
                        ">= 0,8 s (HOOK >= 0,6 s)", "fusionner le plan trop court avec son voisin dans le brief"))

    # 3. duree max
    long_ = []
    for c in clips:
        d = c["duration_frames"] / fps
        mx = float(shot_limits(profile, c.get("section", "default"))["max"])
        if d > mx + 0.05:
            long_.append(f"{c['shot_id']} ({d:.2f} s > {mx} s)")
    checks.append(Check("clips_max", "Aucun clip trop long", not long_, ", ".join(long_) or "aucun",
                        "<= max du profil par section", "couper le plan en deux (sequence a/b) dans le brief"))

    # 4. values consecutives
    dup = []
    for a, b in zip(clips, clips[1:]):
        if a.get("value") and a.get("value") == b.get("value"):
            dup.append(f"{a['shot_id']}->{b['shot_id']} ({a['value']})")
    checks.append(Check("values", "Pas deux valeurs de plan identiques consecutives", not dup, ", ".join(dup) or "aucune",
                        "value differente d'un plan au suivant", "changer la valeur de plan (large/moyen/detail...) d'un des deux plans"))

    # 5. reutilisation de rush
    gap_min = float(profile.get("reuse_min_gap_s", 10.0))
    reuse = []
    last_end: dict[str, tuple[float, str]] = {}
    for c in clips:
        src = c.get("source_rush")
        if not src:
            continue
        start = c["from_frame"] / fps
        end = (c["from_frame"] + c["duration_frames"]) / fps
        if src in last_end:
            prev_end, prev_id = last_end[src]
            if start - prev_end < gap_min:
                reuse.append(f"{prev_id}->{c['shot_id']} ({src}, {start - prev_end:.1f} s)")
        last_end[src] = (end, c["shot_id"])
    checks.append(Check("reuse", "Pas de rush reutilise trop tot", not reuse, ", ".join(reuse) or "aucune",
                        f">= {gap_min} s entre deux usages", "fournir un rush distinct pour le plan substitue"))

    # 6. relance
    events = {0.0, total / fps}
    for c in clips:
        events.add(c["from_frame"] / fps)
        if c.get("punch"):
            events.add(c["punch"]["at_frame"] / fps)
        if c["transition_in"]["type"] != "cut":
            events.add(c["from_frame"] / fps)
    for o in tl.get("overlays", []):
        events.add(o["from_frame"] / fps)
    ev = sorted(events)
    max_gap = max((b - a for a, b in zip(ev, ev[1:])), default=0.0)
    relance = float(profile.get("relance_max_s", 5.0))
    checks.append(Check("relance", "Relance visuelle reguliere", max_gap <= relance + 1e-6,
                        f"plus long intervalle sans evenement : {max_gap:.2f} s", f"<= {relance} s",
                        "ajouter un plan, un punch (mot appuye) ou un overlay dans l'intervalle"))

    # 7. hook
    hook_events = [t for t in ev if 0 < t <= 1.0 + 1e-6]
    checks.append(Check("hook_change", "Image qui change dans la premiere seconde", bool(hook_events),
                        f"{len(hook_events)} evenement(s) dans ]0 ; 1 s]", ">= 1",
                        "raccourcir le plan HOOK (< 1 s) ou poser un punch sur un mot du hook"))

    # 8. transitions visibles
    win = float(profile["transitions"].get("visible_max_per_window_s", 8.0))
    vis = []
    close = []
    last_t = None
    for prev, c in zip([None] + clips[:-1], clips):
        t = c["transition_in"]
        if t["type"] == "cut":
            continue
        t_s = c["from_frame"] / fps
        vis.append(t_s)
        pt, ct = (prev or {}).get("type"), c.get("type")
        exempt = t["type"] == "zoomthrough" and ((pt in REAL_TYPES and ct == "3DSCI") or (pt == "3DSCI" and ct in REAL_TYPES))
        if last_t is not None and not exempt and t_s - last_t < win - 1e-6:
            close.append(f"{last_t:.1f}->{t_s:.1f} s ({t['type']})")
        last_t = t_s
    checks.append(Check("transitions", "Transitions visibles espacees", not close, ", ".join(close) or f"{len(vis)} visible(s), aucune trop proche",
                        f">= {win} s entre deux transitions visibles", "build_timeline.py ramene la transition en cut ; verifier le garde-fou"))

    # 9. freeze
    nfreeze = freeze_count(video)
    checks.append(Check("freeze", "Aucune image figee (freezedetect)", nfreeze == 0, f"{nfreeze} occurrence(s)", "0",
                        "verifier le rush concerne (trop court, fin de fichier) ; best_window.py choisit une autre fenetre ou prep_clips.py boucle en boomerang"))

    # 10. loudness
    target = float(profile["vo_lufs"])
    lufs = measure_loudness(video)
    ok = lufs is not None and abs(lufs - target) <= 1.0
    checks.append(Check("loudness", "Loudness integree", ok, f"{lufs if lufs is not None else 'non mesuree'} LUFS",
                        f"{target} +/- 1 LU", "relancer render.py sans --no-loudnorm"))

    # 11. duree
    vdur = ffprobe_duration(video)
    ok = vdur is not None and abs(vdur - audio_dur) <= 0.1
    checks.append(Check("duree", "Duree du fichier = duree de l'audio", ok, f"{vdur} s vs audio {audio_dur} s", "+/- 0,1 s",
                        "verifier duration_frames du timeline et l'audio de reference"))

    # 12. planche contact
    sheet = out_md.parent / "contact_sheet.jpg"
    ok = contact_sheet(video, clips, fps, sheet)
    checks.append(Check("planche", "Planche contact", ok, str(sheet) if ok else "non generee", "generee",
                        "verifier que ffmpeg lit la video finale"))

    score = sum(WEIGHTS[c.key] for c in checks if c.ok)
    info = ffprobe(video) or {}

    lines = [f"# Rapport QC : {video.name}", "",
             f"**Score : {score} / 100**", "",
             f"- Video : {info.get('width')}x{info.get('height')} @ {info.get('fps')} fps, {vdur} s, audio {'oui' if info.get('has_audio') else 'non'}",
             f"- Profil : {tl['profile']} ; {len(clips)} clips ; {len(vis)} transition(s) visible(s) ; "
             f"{sum(1 for c in clips if c.get('punch'))} punch(s) ; {len(tl.get('overlays', []))} overlay(s)",
             f"- Planche contact : {sheet if sheet.exists() else 'non generee'}", "",
             "| Controle | Resultat | Mesure | Seuil | Poids |", "|---|---|---|---|---|"]
    for c in checks:
        lines.append(f"| {c.name} | {'OK' if c.ok else 'ECHEC'} | {c.measured} | {c.threshold} | {WEIGHTS[c.key]} |")
    fails = [c for c in checks if not c.ok]
    lines += ["", "## Corrections proposees", ""]
    if fails:
        for c in fails:
            lines.append(f"- **{c.name}** : {c.fix}")
    else:
        lines.append("Aucune : tous les controles passent.")
    lines += ["", "## Clips", "", "| Plan | Section | De (s) | Duree (s) | Vitesse | Transition | Punch | Ken Burns | Source |", "|---|---|---|---|---|---|---|---|---|"]
    for c in clips:
        t = c["transition_in"]
        lines.append(f"| {c['shot_id']} | {c.get('section', '')} | {c['from_frame'] / fps:.2f} | {c['duration_frames'] / fps:.2f} | {c['speed']} | "
                     f"{t['type']}{'/' + t['dir'] if t.get('dir') else ''} | {'oui' if c.get('punch') else 'non'} | "
                     f"{'oui' if c.get('kenburns') else 'non'} | {c.get('source_rush') or 'MOTION'} |")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"QC : score {score}/100, {len(fails)} echec(s) -> {out_md}")
    for c in fails:
        log(f"  ECHEC {c.name} : {c.measured} (attendu {c.threshold})")


if __name__ == "__main__":
    main()
