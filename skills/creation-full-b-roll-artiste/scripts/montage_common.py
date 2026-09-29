#!/usr/bin/env python3
"""Fonctions communes aux scripts de la brique MONTAGE de CRÉATION FULL B-ROLL ARTISTE.

Chargement du brief et des profils, ffprobe, resolution des chemins.
Aucun chemin absolu n'est code en dur : le dossier du skill est deduit de
l'emplacement de ce fichier, le dossier projet de l'emplacement de brief.json.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PROFILES = SKILL_DIR / "assets" / "profiles.json"
SFX_DIR = SKILL_DIR / "assets" / "sfx"
REMOTION_DIR = SKILL_DIR / "assets" / "remotion"

VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
IMAGE_EXT = {".jpg", ".jpeg", ".png"}
ALL_EXT = VIDEO_EXT | IMAGE_EXT

REAL_TYPES = {"UGC", "STOCK", "PRODUIT", "SOCIAL"}
STRONG_PUNCT = {".", "?", "!", "..."}


def log(msg: str) -> None:
    """Message d'etat sur stderr (les sorties JSON restent propres)."""
    print(msg, file=sys.stderr, flush=True)


def die(msg: str, code: int = 2) -> None:
    log(f"ERREUR : {msg}")
    sys.exit(code)


def load_json(path: str | Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str | Path, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_profiles(path: str | Path | None = None) -> dict:
    return load_json(path or DEFAULT_PROFILES)


def get_profile(profiles: dict, name: str) -> dict:
    if name not in profiles:
        die(f"profil inconnu '{name}' (attendu : ADS ou EDU)")
    return profiles[name]


def shot_limits(profile: dict, section: str) -> dict:
    """Bornes min/target/max d'un plan pour une section donnee."""
    shots = profile["shot"]
    return shots.get(section, shots["default"])


def project_root_from_brief(brief_path: str | Path) -> Path:
    return Path(brief_path).resolve().parent


def project_root_from_timeline(timeline_path: str | Path) -> Path:
    """Le timeline vit dans projet/work/ : la racine est le parent de work/."""
    p = Path(timeline_path).resolve().parent
    if p.name == "work":
        return p.parent
    return p


def flatten_shots(brief: dict) -> list[dict]:
    """Liste des plans dans l'ordre chronologique, enrichis de leur beat."""
    shots: list[dict] = []
    for beat in brief.get("beats", []):
        for shot in beat.get("shots", []):
            s = dict(shot)
            s["_beat_id"] = beat["id"]
            s["_section"] = beat["section"]
            s["_function"] = beat.get("function")
            s["_energy"] = beat.get("energy", 3)
            s["_beat_text"] = beat.get("text", "")
            shots.append(s)
    shots.sort(key=lambda s: s["start"])
    return shots


def section_of(brief: dict, t: float) -> str | None:
    for sec in brief.get("sections", []):
        if sec["start"] - 1e-6 <= t < sec["end"] - 1e-6:
            return sec["id"]
    return None


def section_bounds(brief: dict, sec_id: str) -> tuple[float, float] | None:
    for sec in brief.get("sections", []):
        if sec["id"] == sec_id:
            return sec["start"], sec["end"]
    return None


def run(cmd: list[str], check: bool = True, capture: bool = True, timeout: int | None = None) -> subprocess.CompletedProcess:
    """Execute une commande, en levant une erreur lisible en cas d'echec."""
    try:
        return subprocess.run(cmd, check=check, capture_output=capture, text=True, timeout=timeout)
    except subprocess.CalledProcessError as e:
        err = (e.stderr or "")[-2000:]
        raise RuntimeError(f"commande echouee ({cmd[0]}) : {err}") from e


def ffprobe(path: str | Path) -> dict | None:
    """Metadonnees d'un media : duree, dimensions, fps, piste audio, image fixe.

    Retourne None si ffprobe echoue ou si aucun flux video n'est trouve.
    """
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_streams", "-show_format", str(path),
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None
    try:
        info = json.loads(res.stdout)
    except json.JSONDecodeError:
        return None
    video = None
    has_audio = False
    for st in info.get("streams", []):
        if st.get("codec_type") == "video" and video is None:
            video = st
        elif st.get("codec_type") == "audio":
            has_audio = True
    if video is None:
        return None
    ext = Path(path).suffix.lower()
    is_image = ext in IMAGE_EXT or video.get("codec_name") in {"png", "mjpeg"} and video.get("nb_frames") in (None, "1")
    fps = None
    for key in ("avg_frame_rate", "r_frame_rate"):
        val = video.get(key)
        if val and val != "0/0":
            num, _, den = val.partition("/")
            try:
                d = float(den) if den else 1.0
                if d > 0:
                    fps = round(float(num) / d, 3)
                    break
            except ValueError:
                pass
    duration = None
    for src in (video.get("duration"), info.get("format", {}).get("duration")):
        if src not in (None, "N/A"):
            try:
                duration = float(src)
                break
            except ValueError:
                pass
    if is_image:
        duration = None
        fps = None
    return {
        "duration_s": round(duration, 3) if duration is not None else None,
        "width": int(video.get("width", 0)),
        "height": int(video.get("height", 0)),
        "fps": fps,
        "has_audio": has_audio,
        "is_image": bool(is_image),
        "codec": video.get("codec_name"),
    }


def ffprobe_duration(path: str | Path) -> float | None:
    """Duree (secondes) d'un fichier audio ou video via ffprobe."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
        return float(res.stdout.strip())
    except (subprocess.CalledProcessError, ValueError, subprocess.TimeoutExpired):
        return None


def resolve_asset(path: str, project_root: Path) -> Path | None:
    """Resout un chemin de ressource : absolu, relatif au projet, sinon relatif au skill."""
    p = Path(path)
    if p.is_absolute() and p.exists():
        return p
    for base in (project_root, SKILL_DIR):
        cand = base / path
        if cand.exists():
            return cand
    return None


def resolve_shot_source(shot_id: str, inventory: dict) -> tuple[str | None, str]:
    """Fichier source a utiliser pour un plan : un substitut s'il en existe un,
    sinon son propre rush (ok ou too_short recuperable par la vitesse), sinon MOTION.

    Retourne (chemin relatif au projet ou None, methode) avec methode dans
    {"own", "substitute", "motion"}.
    """
    by_id = {s["id"]: s for s in inventory["shots"]}
    for sub in inventory.get("substitutions", []):
        if sub["shot"] == shot_id:
            if sub["use"] == "MOTION":
                return None, "motion"
            target = by_id.get(sub["use"])
            if target and target.get("file"):
                return target["file"], "substitute"
    entry = by_id.get(shot_id)
    if entry and entry.get("file") and entry.get("status") in ("ok", "too_short"):
        return entry["file"], "own"
    return None, "motion"


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").lower() in ("1", "true", "yes", "oui")
