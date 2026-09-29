#!/usr/bin/env python3
"""build_timeline.py : applique la grammaire de montage et ecrit work/timeline.json.

Regles (profil ADS ou EDU dans assets/profiles.json) :
  - un plan = un clip de round(start*fps) a round(end*fps), sans trou ; le dernier
    clip finit a la fin de l'audio ;
  - speed = playbackRate Remotion : 1.0, ou < 1 (ralenti borne par speed_ramp_max)
    si la fenetre choisie par best_window.py est plus courte que necessaire ;
  - Ken Burns si camera == static ou source image : zoom static_from -> static_to,
    sens alterne (push puis pull) d'un clip statique au suivant, origine (0.5, 0.42) ;
  - punch : au plus un par clip, sur le mot d'emphase (features.emphasis) le plus
    fort situe hors des 8 premieres et 8 dernieres frames ; jamais deux clips
    consecutifs avec punch ; garde-fou HOOK : si rien ne change dans la premiere
    seconde, un punch est pose a 0,6 s du premier clip ;
  - transitions (transition_in du clip N), par priorite :
      reel (UGC/STOCK/PRODUIT/SOCIAL) <-> 3DSCI : zoomthrough 8 frames, meme au sein
        d'une sequence (on rentre dans la matiere, puis on en ressort)
      meme sequence (03a -> 03b) : cut
      fin de HOOK : flash 3 frames si flash_allowed_in contient HOOK, sinon famille
      avant/apres (descriptions ou must_show) : wipe 8 frames
      changement de section : transitions.family_default (whip ADS, zoomthrough EDU), 8 frames
      EDU, meme section, energy <= 2 et camera static des deux cotes : dissolve 10 frames
      sinon : cut
    Direction alternee gauche/droite. Garde-fou : apres une transition visible,
    toute transition visible dans les visible_max_per_window_s suivantes redevient
    cut, SAUF le zoomthrough reel <-> 3DSCI qui reste visible et reinitialise la
    fenetre ; le tout premier clip est toujours cut ;
  - ambiance : true si le clip a une piste audio, a ambience_db du profil ;
  - sfx : whoosh a chaque transition visible (-14 dB), tick a chaque punch (-18 dB),
    impact bas au premier frame (-12 dB). Fichiers synthetiques dans assets/sfx/
    (generes par make_sfx.py si absents) ;
  - overlays : plan MOTION ou avec overlay_text -> overlay texte style stat.

Les chemins ecrits sont relatifs a la racine du projet (dossier de brief.json),
sauf les sfx qui sont relatifs au skill (assets/sfx/...), comme dans CONTRACTS.md.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from montage_common import (REAL_TYPES, SKILL_DIR, die, flatten_shots, get_profile, load_json, load_profiles,
                    log, project_root_from_brief, resolve_shot_source, save_json)
from make_sfx import ensure_sfx

PUNCH_FRAMES = 6
PUNCH_EDGE_FRAMES = 8
FLASH_FRAMES = 3
FAMILY_FRAMES = 8
DISSOLVE_FRAMES = 10
KB_ORIGIN = [0.5, 0.42]
SFX_DB = {"whoosh": -14.0, "tick": -18.0, "impact": -12.0}

AVANT_APRES = re.compile(r"\b(avant|apr[eè]s|before|after)\b", re.IGNORECASE)


def _aa_tags(shot: dict) -> set[str]:
    """Etiquettes avant/apres trouvees dans la description et must_show d'un plan."""
    text = (shot.get("description") or "") + " " + " ".join(shot.get("must_show") or [])
    found = {m.lower() for m in AVANT_APRES.findall(text)}
    out: set[str] = set()
    if found & {"avant", "before"}:
        out.add("avant")
    if any(f.startswith("apr") or f == "after" for f in found):
        out.add("apres")
    return out


def avant_apres_pair(a: dict, b: dict) -> bool:
    """Vrai si les deux plans forment un avant/apres (chacun etiquete, les deux etiquettes couvertes)."""
    ta, tb = _aa_tags(a), _aa_tags(b)
    return bool(ta) and bool(tb) and (ta | tb) == {"avant", "apres"}


def is_3dsci_crossing(prev: dict, cur: dict) -> bool:
    """Passage reel -> 3DSCI ou 3DSCI -> reel : zoomthrough porteur de sens, exempte du garde-fou."""
    pt, ct = prev["type"], cur["type"]
    return (pt in REAL_TYPES and ct == "3DSCI") or (pt == "3DSCI" and ct in REAL_TYPES)


def pick_transition(prev: dict, cur: dict, profile: dict) -> tuple[str, int]:
    """Type et duree (frames) de la transition entrante de `cur`, hors garde-fou."""
    trans = profile["transitions"]
    family = trans.get("family_default", "whip")
    if is_3dsci_crossing(prev, cur):
        return "zoomthrough", FAMILY_FRAMES
    if prev["_beat_id"] == cur["_beat_id"]:
        return "cut", 0
    if prev["_section"] == "HOOK" and cur["_section"] != "HOOK":
        if "HOOK" in trans.get("flash_allowed_in", []):
            return "flash", FLASH_FRAMES
        return family, FAMILY_FRAMES
    if avant_apres_pair(prev, cur):
        return "wipe", FAMILY_FRAMES
    if prev["_section"] != cur["_section"]:
        return family, FAMILY_FRAMES
    if (trans.get("dissolve_allowed") and prev["_energy"] <= 2 and cur["_energy"] <= 2
            and prev.get("camera") == "static" and cur.get("camera") == "static"):
        return "dissolve", DISSOLVE_FRAMES
    return "cut", 0


def overlay_text_for(shot: dict) -> str:
    if shot.get("overlay_text"):
        return str(shot["overlay_text"]).strip()
    desc = shot.get("description") or shot.get("_beat_text") or ""
    m = re.search(r"\d+(?:[.,]\d+)?\s?(?:%|€|euros?|secondes?|s\b|min\b|x\b)?", desc)
    if m:
        return m.group(0).strip()
    words = re.findall(r"[\wÀ-ÿ'-]+", desc)
    return " ".join(words[:3])


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Construit work/timeline.json a partir du brief, de l'inventaire, des fenetres et des features audio.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("brief", help="brief.json")
    ap.add_argument("inventory", help="work/inventory.json")
    ap.add_argument("windows", help="work/windows.json")
    ap.add_argument("features", help="work/features.json (emphasis, pauses)")
    ap.add_argument("--out", required=True, help="chemin de sortie, ex. work/timeline.json")
    ap.add_argument("--music", default=None, help="fichier musique optionnel (relatif au projet ou absolu)")
    ap.add_argument("--clips", default=None, help="dossier des clips prepares (defaut : <dossier de --out>/clips)")
    ap.add_argument("--captions", default=None, help="captions.json (defaut : <dossier de --out>/captions.json)")
    ap.add_argument("--profiles", default=None, help="assets/profiles.json (defaut : celui du skill)")
    args = ap.parse_args()

    brief = load_json(args.brief)
    inventory = load_json(args.inventory)
    windows = load_json(args.windows)
    features = load_json(args.features)
    profiles = load_profiles(args.profiles)
    proj = brief["project"]
    profile = get_profile(profiles, proj["profile"])
    root = project_root_from_brief(args.brief)
    out_path = Path(args.out).resolve()
    clips_dir = Path(args.clips).resolve() if args.clips else out_path.parent / "clips"
    captions_path = Path(args.captions).resolve() if args.captions else out_path.parent / "captions.json"

    fps = int(proj.get("fps", 30))
    W = int(proj.get("width", 1080))
    H = int(proj.get("height", 1920))
    audio_dur = float(brief["audio"]["duration_s"])
    duration_frames = int(round(audio_dur * fps))

    meta_path = clips_dir / "meta.json"
    if not meta_path.exists():
        die(f"meta.json introuvable dans {clips_dir} : lancez prep_clips.py d'abord")
    meta = load_json(meta_path)["clips"]
    win_by_id = {w["id"]: w for w in windows["shots"]}

    def rel(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(root))
        except ValueError:
            return str(p.resolve())

    shots = flatten_shots(brief)
    if not shots:
        die("aucun plan dans le brief")

    # 1) clips de base
    clips: list[dict] = []
    for i, shot in enumerate(shots):
        sid = shot["id"]
        m = meta.get(sid)
        if m is None:
            die(f"clip manquant pour le plan {sid} (prep_clips.py)")
        from_f = int(round(float(shot["start"]) * fps))
        end_f = duration_frames if i == len(shots) - 1 else int(round(float(shot["end"]) * fps))
        if i > 0:
            from_f = clips[-1]["from_frame"] + clips[-1]["duration_frames"]  # couverture sans trou
        dur_f = max(1, end_f - from_f)
        win = win_by_id.get(sid, {})
        speed = float(m.get("speed", win.get("speed", 1.0)))
        src_rel, _method = resolve_shot_source(sid, inventory)
        clips.append({
            "shot_id": sid,
            "src": rel(clips_dir / m.get("clip", f"{sid}.mp4")),
            "from_frame": from_f,
            "duration_frames": dur_f,
            "trim_before_frames": int(round(float(m.get("lead_s", 0.0)) * fps)),
            "speed": round(speed, 3),
            "kenburns": None,
            "punch": None,
            "transition_in": {"type": "cut", "frames": 0, "dir": None},
            "ambience": bool(m.get("has_audio")),
            "ambience_db": float(profile["ambience_db"]),
            "section": shot["_section"],
            "type": shot["type"],
            "camera": shot.get("camera"),
            "value": shot.get("value"),
            "source_rush": src_rel,
            "source_method": m.get("method"),
        })

    # 2) Ken Burns alterne sur les plans statiques ou images
    kb = profile["kenburns"]
    push = True
    for shot, clip in zip(shots, clips):
        is_static = shot.get("camera") == "static" or str(clip["source_method"]).startswith("image")
        if is_static:
            a, b = float(kb["static_from"]), float(kb["static_to"])
            clip["kenburns"] = {"from": a if push else b, "to": b if push else a, "origin": list(KB_ORIGIN)}
            push = not push

    # 3) punch sur les mots d'emphase
    emphasis = sorted(features.get("emphasis", []), key=lambda e: -float(e.get("z", 0)))
    prev_punch = False
    for clip in clips:
        lo = clip["from_frame"] + PUNCH_EDGE_FRAMES
        hi = clip["from_frame"] + clip["duration_frames"] - PUNCH_EDGE_FRAMES
        chosen = None
        if not prev_punch and hi > lo:
            for e in emphasis:
                f = int(round(float(e["t"]) * fps))
                if lo <= f <= hi:
                    chosen = f
                    break
        if chosen is not None:
            clip["punch"] = {"at_frame": chosen, "scale": float(profile["punch_scale"]), "frames": PUNCH_FRAMES}
        prev_punch = chosen is not None

    # Garde-fou hook : quelque chose doit changer dans la premiere seconde
    first = clips[0]
    if first["duration_frames"] > fps and first["punch"] is None:
        kick = int(round(0.6 * fps))
        if PUNCH_EDGE_FRAMES <= kick <= first["duration_frames"] - PUNCH_EDGE_FRAMES:
            first["punch"] = {"at_frame": first["from_frame"] + kick, "scale": float(profile["punch_scale"]), "frames": PUNCH_FRAMES}
            if len(clips) > 1 and clips[1]["punch"] is not None:
                clips[1]["punch"] = None  # jamais deux punchs consecutifs
            log("  garde-fou hook : punch ajoute a 0,6 s")

    # 4) transitions
    window_s = float(profile["transitions"].get("visible_max_per_window_s", 8.0))
    last_visible_t = None
    dir_toggle = "left"
    for i in range(1, len(clips)):
        ttype, frames = pick_transition(shots[i - 1], shots[i], profile)
        t_s = clips[i]["from_frame"] / fps
        exempt = ttype == "zoomthrough" and is_3dsci_crossing(shots[i - 1], shots[i])
        if ttype != "cut" and not exempt and last_visible_t is not None and (t_s - last_visible_t) < window_s:
            ttype, frames = "cut", 0
        direction = None
        if ttype in ("whip", "wipe"):
            direction = dir_toggle
            dir_toggle = "right" if dir_toggle == "left" else "left"
        # Une transition ne peut pas depasser la duree du clip sortant ni entrant
        frames = min(frames, clips[i - 1]["duration_frames"], clips[i]["duration_frames"])
        if frames <= 0:
            ttype = "cut"
        clips[i]["transition_in"] = {"type": ttype, "frames": int(frames), "dir": direction}
        if ttype != "cut":
            last_visible_t = t_s

    # 5) sfx
    sfx_files = ensure_sfx()

    def sfx_rel(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(SKILL_DIR))
        except ValueError:
            return str(p.resolve())

    sfx: list[dict] = [{"src": sfx_rel(sfx_files["impact"]), "at_frame": 0, "db": SFX_DB["impact"]}]
    for clip in clips:
        t = clip["transition_in"]
        if t["type"] != "cut":
            sfx.append({"src": sfx_rel(sfx_files["whoosh"]), "at_frame": max(0, clip["from_frame"] - 2), "db": SFX_DB["whoosh"]})
        if clip["punch"]:
            sfx.append({"src": sfx_rel(sfx_files["tick"]), "at_frame": clip["punch"]["at_frame"], "db": SFX_DB["tick"]})
    sfx.sort(key=lambda s: s["at_frame"])

    # 6) overlays
    overlays: list[dict] = []
    for shot, clip in zip(shots, clips):
        if shot["type"] == "MOTION" or shot.get("overlay_text"):
            text = overlay_text_for(shot)
            if text:
                overlays.append({"type": "text", "text": text, "from_frame": clip["from_frame"],
                                 "duration_frames": clip["duration_frames"], "style": "stat", "anchor": "center"})

    # 7) captions et safe zone
    subs = proj.get("subtitles", {})
    hook_end = 0.0
    for sec in brief.get("sections", []):
        if sec["id"] == "HOOK":
            hook_end = float(sec["end"])
    safe = profiles.get("platform_safe_zone", {}).get(proj.get("platform", "tiktok"))

    music = None
    if args.music:
        mp = Path(args.music)
        music = rel(mp) if mp.exists() else args.music

    timeline = {
        "schema": "broll-director/timeline/1",
        "fps": fps, "width": W, "height": H, "duration_frames": duration_frames,
        "profile": proj["profile"],
        "audio": {
            "vo": brief["audio"]["file"],
            "music": music,
            "music_db": float(profile["music_db"]),
            "ambience_db": float(profile["ambience_db"]),
        },
        "clips": clips,
        "captions": {
            "file": rel(captions_path),
            "style": subs.get("style", "default"),
            "hook_style": subs.get("hook_style", "red-box"),
            "hook_end_frame": int(round(hook_end * fps)),
        },
        "overlays": overlays,
        "sfx": sfx,
        "endcard": None,
        "safe_zone": {k: int(v) for k, v in safe.items()} if safe else None,
    }
    save_json(out_path, timeline)

    n_vis = sum(1 for c in clips if c["transition_in"]["type"] != "cut")
    n_punch = sum(1 for c in clips if c["punch"])
    log(f"timeline : {len(clips)} clips, {duration_frames} frames, {n_vis} transitions visibles, "
        f"{n_punch} punchs, {len(overlays)} overlays, {len(sfx)} sfx -> {out_path}")
    for c in clips:
        t = c["transition_in"]
        log(f"  {c['shot_id']:>4} [{c['from_frame']:>4}+{c['duration_frames']:>3}] {c['section']:<6} "
            f"in={t['type']}{'/' + t['dir'] if t['dir'] else ''} speed={c['speed']} "
            f"kb={'oui' if c['kenburns'] else 'non'} punch={'oui' if c['punch'] else 'non'} amb={'oui' if c['ambience'] else 'non'}")


if __name__ == "__main__":
    main()
