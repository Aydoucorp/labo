#!/usr/bin/env python3
"""prep_clips.py : prepare un clip pret a monter par plan (work/clips/{id}.mp4).

Pour chaque plan :
  - trim sur la fenetre de windows.json (+ 0,2 s de marge de chaque cote quand
    la source le permet) ;
  - scale + crop "cover" vers WxH (1080x1920 par defaut). Centrage sur le plus
    grand visage detecte (OpenCV Haar, 5 frames) si OpenCV est disponible, sinon
    centre pondere vers le tiers superieur ;
  - fps du projet, legere normalisation (eq contrast 1.03, saturation 1.05, et
    `normalize` doux si la plage de luminance est etroite) ;
  - H.264 CRF 16 preset fast, audio ambiant conserve en AAC (silence si absent) ;
  - une image fixe devient une video de la duree requise (Ken Burns dans Remotion) ;
  - un plan MOTION sans rush devient une carte a degrade anime ;
  - un rush trop court meme ralenti (windows.json `boomerang: true`) est monte en
    aller-retour du PROPRE rush (boomerang), boucle jusqu'a la duree requise, sans
    image figee ; c'est l'etape (b) du rattrapage decrit dans inventory.py.

La vitesse (playbackRate) n'est PAS appliquee ici : Remotion s'en charge.
Ecrit aussi work/clips/meta.json (lead_s, duration_s, has_audio par plan) que
build_timeline.py utilise pour trim_before_frames.
"""
from __future__ import annotations

import argparse
import math
import tempfile
from pathlib import Path

import numpy as np

from montage_common import (die, ffprobe, flatten_shots, load_json, log, project_root_from_brief,
                    resolve_shot_source, save_json)

MARGIN_S = 0.2
# Marge supplementaire en fin de clip pour couvrir les frames de transition sortante
TAIL_EXTRA_S = 0.2

try:  # OpenCV est optionnel
    import cv2  # type: ignore

    HAVE_CV2 = True
except Exception:  # pragma: no cover
    cv2 = None
    HAVE_CV2 = False


def sample_frames(path: Path, is_image: bool, t0: float, t1: float, n: int = 5) -> list[np.ndarray]:
    """n frames BGR de la source entre t0 et t1 (ou l'image elle-meme)."""
    if not HAVE_CV2:
        return []
    if is_image:
        img = cv2.imread(str(path))
        return [img] if img is not None else []
    cap = cv2.VideoCapture(str(path))
    frames = []
    if not cap.isOpened():
        return frames
    for i in range(n):
        t = t0 + (t1 - t0) * (i + 0.5) / n
        cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, t) * 1000.0)
        ok, frame = cap.read()
        if ok and frame is not None:
            frames.append(frame)
    cap.release()
    return frames


def detect_face_center(frames: list[np.ndarray]) -> tuple[float, float] | None:
    """Centre (x, y) en pixels source du plus grand visage trouve, sinon None."""
    if not HAVE_CV2 or not frames:
        return None
    try:
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    except Exception:
        return None
    if cascade.empty():
        return None
    best = None
    for fr in frames:
        gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape[:2]
        scale = 480.0 / max(w, h) if max(w, h) > 480 else 1.0
        small = cv2.resize(gray, (int(w * scale), int(h * scale))) if scale != 1.0 else gray
        faces = cascade.detectMultiScale(small, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
        for (x, y, fw, fh) in faces:
            area = fw * fh
            if best is None or area > best[0]:
                best = (area, (x + fw / 2) / scale, (y + fh / 2) / scale)
    if best is None:
        return None
    return best[1], best[2]


def luma_range(frames: list[np.ndarray]) -> tuple[float, float] | None:
    if not HAVE_CV2 or not frames:
        return None
    vals = []
    for fr in frames:
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        vals.append(g.reshape(-1))
    allv = np.concatenate(vals)
    return float(np.percentile(allv, 1)), float(np.percentile(allv, 99))


def cover_filter(sw: int, sh: int, tw: int, th: int, center: tuple[float, float] | None) -> str:
    """Filtre scale+crop 'cover' vers tw x th, centre sur `center` (pixels source)."""
    s = max(tw / sw, th / sh)
    scaled_w = int(math.ceil(sw * s))
    scaled_h = int(math.ceil(sh * s))
    scaled_w += scaled_w % 2
    scaled_h += scaled_h % 2
    scaled_w = max(scaled_w, tw)
    scaled_h = max(scaled_h, th)
    if center is None:
        cx, cy = sw / 2, sh * 0.42  # centre pondere vers le tiers superieur
    else:
        cx, cy = center
    x0 = int(round(cx * s - tw / 2))
    y0 = int(round(cy * s - th / 2))
    x0 = max(0, min(scaled_w - tw, x0))
    y0 = max(0, min(scaled_h - th, y0))
    return f"scale={scaled_w}:{scaled_h}:flags=lanczos,crop={tw}:{th}:{x0}:{y0}"


def color_filter(lr: tuple[float, float] | None) -> str:
    f = "eq=contrast=1.03:saturation=1.05"
    if lr is not None and (lr[1] - lr[0]) < 150:
        f = "normalize=smoothing=20:strength=0.35," + f
    return f


def run_ffmpeg(args: list[str]) -> None:
    import subprocess

    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-y"] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("ffmpeg : " + res.stderr[-1500:])


def encode_args(fps: int) -> list[str]:
    return ["-r", str(fps), "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart"]


def make_motion_card(out: Path, w: int, h: int, fps: int, duration: float, seed: int,
                     palette: list[str] | None = None) -> None:
    """Carte MOTION : dégradé animé. `palette` (3 couleurs hex, project.motion_palette du brief) impose la charte."""
    palettes = [
        ("0x161a3a", "0x4b2a8a", "0x0e7a6e"),
        ("0x1f1d2b", "0x8a2a4b", "0xd97b2f"),
        ("0x0b2545", "0x13315c", "0x8da9c4"),
        ("0x1a1a1a", "0x3d3d3d", "0xb8860b"),
    ]
    c0, c1, c2 = ([c.replace("#", "0x") for c in palette[:3]] if palette and len(palette) >= 3
                  else palettes[seed % len(palettes)])
    # dégradé linéaire vertical quand la charte impose la palette (le spiral laisse un point visible au centre)
    gtype = f"type=linear:x0={w // 2}:y0=0:x1={w // 2}:y1={h}" if palette else \
        f"type=spiral:x0={w // 3}:y0={h // 3}:x1={w * 2 // 3}:y1={h * 2 // 3}"
    src = (f"gradients=size={w}x{h}:speed=0.02:duration={duration:.3f}:rate={fps}:nb_colors=3"
           f":c0={c0}:c1={c1}:c2={c2}:{gtype}")
    run_ffmpeg(["-f", "lavfi", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-t", f"{duration:.3f}", "-map", "0:v:0", "-map", "1:a:0", "-shortest",
                *encode_args(fps), str(out)])


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Prepare les clips 1080x1920 prets a monter dans work/clips/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("brief", help="brief.json")
    ap.add_argument("inventory", help="work/inventory.json")
    ap.add_argument("windows", help="work/windows.json")
    ap.add_argument("--out", required=True, help="dossier de sortie, ex. work/clips/")
    ap.add_argument("--width", type=int, default=None, help="largeur (defaut : brief.project.width ou 1080)")
    ap.add_argument("--height", type=int, default=None, help="hauteur (defaut : brief.project.height ou 1920)")
    ap.add_argument("--fps", type=int, default=None, help="fps (defaut : brief.project.fps ou 30)")
    ap.add_argument("--no-face", action="store_true", help="desactive la detection de visage")
    ap.add_argument("--force", action="store_true", help="regenere meme si le clip existe deja")
    args = ap.parse_args()

    brief = load_json(args.brief)
    inventory = load_json(args.inventory)
    windows = load_json(args.windows)
    root = project_root_from_brief(args.brief)
    proj = brief.get("project", {})
    W = args.width or int(proj.get("width", 1080))
    H = args.height or int(proj.get("height", 1920))
    FPS = args.fps or int(proj.get("fps", 30))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    win_by_id = {w["id"]: w for w in windows["shots"]}
    inv_by_file = {e["file"]: e for e in inventory["shots"] if e.get("file")}
    use_face = HAVE_CV2 and not args.no_face
    log(f"prep_clips : {W}x{H} @ {FPS} fps, visage {'OpenCV' if use_face else 'desactive (centre pondere)'}")

    prev_meta: dict[str, dict] = {}
    if (out_dir / "meta.json").exists():
        try:
            prev_meta = load_json(out_dir / "meta.json").get("clips", {})
        except Exception:
            prev_meta = {}

    meta: dict[str, dict] = {}
    for idx, shot in enumerate(flatten_shots(brief)):
        sid = shot["id"]
        plan_dur = float(shot["end"]) - float(shot["start"])
        win = win_by_id.get(sid)
        if win is None:
            die(f"plan {sid} absent de windows.json")
        speed = float(win.get("speed", 1.0))
        out = out_dir / f"{sid}.mp4"
        src_rel, method = resolve_shot_source(sid, inventory)
        # Duree de source utile : plan x vitesse + 0,2 s de securite (fenetre) + marge de sortie
        needed_core = plan_dur * speed + MARGIN_S

        if out.exists() and not args.force and sid in prev_meta:
            meta[sid] = prev_meta[sid]
            log(f"  {sid} : existe deja, conserve")
            continue

        if src_rel is None:
            dur = needed_core + TAIL_EXTRA_S
            make_motion_card(out, W, H, FPS, dur, idx, brief.get("project", {}).get("motion_palette"))
            meta[sid] = {"lead_s": 0.0, "duration_s": round(dur, 3), "has_audio": False,
                         "speed": speed, "source": None, "method": "motion"}
            log(f"  {sid} : carte MOTION générée ({dur:.2f} s)")
        else:
            src_path = root / src_rel
            inv = inv_by_file.get(src_rel)
            if inv is None or not src_path.exists():
                die(f"source introuvable pour {sid} : {src_rel}")
            sw, sh = int(inv["width"]), int(inv["height"])
            is_image = bool(inv.get("is_image"))
            in_s = float(win["in_s"])
            out_s = float(win["out_s"])
            frames = sample_frames(src_path, is_image, in_s, out_s) if use_face else []
            center = detect_face_center(frames) if use_face else None
            vf = cover_filter(sw, sh, W, H, center) + "," + color_filter(luma_range(frames)) + f",fps={FPS}"
            face_note = f", visage en ({center[0]:.0f},{center[1]:.0f})" if center else ""

            if is_image:
                dur = needed_core + TAIL_EXTRA_S
                run_ffmpeg(["-loop", "1", "-framerate", str(FPS), "-i", str(src_path),
                            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                            "-t", f"{dur:.3f}", "-vf", vf, "-map", "0:v:0", "-map", "1:a:0", "-shortest",
                            *encode_args(FPS), str(out)])
                meta[sid] = {"lead_s": 0.0, "duration_s": round(dur, 3), "has_audio": False,
                             "speed": speed, "source": src_rel, "method": "image"}
                log(f"  {sid} : image -> video {dur:.2f} s{face_note}")
                continue

            src_dur = float(inv.get("duration_s") or 0.0)
            has_audio = bool(inv.get("has_audio"))
            lead = min(MARGIN_S, max(0.0, in_s))
            tail = min(MARGIN_S + TAIL_EXTRA_S, max(0.0, src_dur - out_s))
            t_start = in_s - lead
            t_len = (out_s - in_s) + lead + tail
            padded = bool(win.get("padded")) or (out_s - in_s) + 1e-3 < needed_core

            if not padded:
                inputs = ["-ss", f"{t_start:.3f}", "-t", f"{t_len:.3f}", "-i", str(src_path)]
                if has_audio:
                    maps = ["-map", "0:v:0", "-map", "0:a:0"]
                else:
                    inputs += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
                    maps = ["-map", "0:v:0", "-map", "1:a:0", "-shortest"]
                run_ffmpeg([*inputs, "-vf", vf, *maps, "-t", f"{t_len:.3f}", *encode_args(FPS), str(out)])
                meta[sid] = {"lead_s": round(lead, 3), "duration_s": round(t_len, 3), "has_audio": has_audio,
                             "speed": speed, "source": src_rel, "method": method}
                log(f"  {sid} : {src_rel} [{t_start:.2f} +{t_len:.2f} s]{face_note}")
            else:
                # Boomerang : unite aller + retour, bouclee jusqu'a la duree requise
                target = needed_core + TAIL_EXTRA_S
                with tempfile.TemporaryDirectory() as td:
                    unit = Path(td) / "unit.mp4"
                    run_ffmpeg(["-i", str(src_path), "-filter_complex",
                                f"[0:v]{vf},split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[v]",
                                "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast",
                                "-pix_fmt", "yuv420p", str(unit)])
                    unit_dur = ffprobe(unit)["duration_s"] or (2 * src_dur)
                    loops = max(0, int(math.ceil(target / max(unit_dur, 0.1))) - 1)
                    run_ffmpeg(["-stream_loop", str(loops), "-i", str(unit),
                                "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                                "-t", f"{target:.3f}", "-map", "0:v:0", "-map", "1:a:0", "-shortest",
                                *encode_args(FPS), str(out)])
                meta[sid] = {"lead_s": 0.0, "duration_s": round(target, 3), "has_audio": False,
                             "speed": speed, "source": src_rel, "method": method + "+boomerang"}
                log(f"  {sid} : {src_rel} trop court, boomerang jusqu'à {target:.2f} s{face_note}")

    for sid, m in meta.items():
        m["clip"] = f"{sid}.mp4"
    save_json(out_dir / "meta.json", {"width": W, "height": H, "fps": FPS, "clips": meta})
    log(f"prep_clips : {len(meta)} clips -> {out_dir}")


if __name__ == "__main__":
    main()
