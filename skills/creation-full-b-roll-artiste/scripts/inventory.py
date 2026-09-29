#!/usr/bin/env python3
"""inventory.py : apparie chaque plan du brief a un fichier du dossier rushes/.

Regles d'appariement (insensibles a la casse) :
  1. nom exact du champ `filename` du plan ;
  2. prefixe `{id}_`, `{id}.` ou `{id}-` avec une extension acceptee
     (mp4, mov, webm, mkv, jpg, jpeg, png). Une image fixe est acceptee et sera
     animee en Ken Burns par le montage.

Statuts : ok | too_short | missing | bad_format.
  too_short : duree du rush < duree du plan + 0,4 s (jamais pour une image).
Ordre de rattrapage d'un rush too_short (champ `recovery`), pour garder le
PROPRE rush du plan aussi longtemps que possible (l'image confirme la voix) :
  (a) "slowmo"    : ralenti jusqu'a 1/speed_ramp_max si duree x speed_ramp_max
                    couvre le plan + 0,2 s ;
  (b) "boomerang" : aller-retour du propre rush, combine au ralenti si besoin,
                    si duree x 2 x speed_ramp_max couvre le plan + 0,2 s ;
  (c) substitution par un plan voisin de la MEME sequence (03a -> 03b) ;
  (d) substitution par le plan du meme type le plus proche dans le temps ;
  (e) carte MOTION generee par prep_clips.py.
Les plans missing ou bad_format suivent (c) (d) (e). Le detail est repris dans
`substitutions[].reason` et dans windows.json (`boomerang`, `method`).

Sortie : work/inventory.json (CONTRACTS.md section 5).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from montage_common import (ALL_EXT, IMAGE_EXT, die, ffprobe, flatten_shots, get_profile, load_json,
                    load_profiles, log, project_root_from_brief, save_json)

TOO_SHORT_MARGIN_S = 0.4


def find_candidates(rushes_dir: Path, shot: dict) -> tuple[Path | None, str | None]:
    """Cherche le fichier d'un plan. Retourne (chemin, methode) ou (None, None)."""
    files = [p for p in rushes_dir.iterdir() if p.is_file() and p.suffix.lower() in ALL_EXT]
    lower_map: dict[str, list[Path]] = {}
    for p in files:
        lower_map.setdefault(p.name.lower(), []).append(p)

    expected = (shot.get("filename") or "").lower()
    if expected and expected in lower_map:
        return sorted(lower_map[expected])[0], "exact"
    # Nom exact sans tenir compte de l'extension
    if expected:
        stem = Path(expected).stem
        for p in files:
            if p.stem.lower() == stem:
                return p, "exact"

    sid = shot["id"].lower()
    pattern = re.compile(r"^" + re.escape(sid) + r"[._-]")
    matches = [p for p in files if pattern.match(p.name.lower())]
    if matches:
        # Priorite aux videos, puis ordre alphabetique pour etre deterministe
        matches.sort(key=lambda p: (p.suffix.lower() in IMAGE_EXT, p.name.lower()))
        return matches[0], "prefix"
    return None, None


def propose_substitution(shot: dict, shots: list[dict], status_by_id: dict[str, str]) -> dict:
    """Voisin de la meme sequence, sinon meme type le plus proche, sinon MOTION."""
    sid = shot["id"]
    beat = shot["_beat_id"]
    usable = [s for s in shots if s["id"] != sid and status_by_id.get(s["id"]) in ("ok", "too_short_ok")]

    same_seq = [s for s in usable if s["_beat_id"] == beat]
    if same_seq:
        best = min(same_seq, key=lambda s: abs(s["start"] - shot["start"]))
        return {"shot": sid, "use": best["id"], "reason": "voisin même séquence"}

    same_type = [s for s in usable if s["type"] == shot["type"]]
    if same_type:
        best = min(same_type, key=lambda s: abs(s["start"] - shot["start"]))
        return {"shot": sid, "use": best["id"], "reason": f"même type ({shot['type']}) le plus proche"}

    return {"shot": sid, "use": "MOTION", "reason": "aucun rush compatible, carte MOTION générée"}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Apparie les plans du brief aux fichiers de rushes/ et ecrit work/inventory.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("brief", help="brief.json (CONTRACTS.md section 4)")
    ap.add_argument("rushes", help="dossier des rushes deposes par l'utilisateur")
    ap.add_argument("--out", required=True, help="chemin de sortie, ex. work/inventory.json")
    ap.add_argument("--profiles", default=None, help="assets/profiles.json (defaut : celui du skill)")
    args = ap.parse_args()

    brief = load_json(args.brief)
    root = project_root_from_brief(args.brief)
    rushes_dir = Path(args.rushes)
    if not rushes_dir.is_absolute():
        rushes_dir = (Path.cwd() / rushes_dir).resolve()
    if not rushes_dir.is_dir():
        die(f"dossier de rushes introuvable : {rushes_dir}")
    profiles = load_profiles(args.profiles)
    profile = get_profile(profiles, brief["project"]["profile"])
    speed_max = float(profile.get("speed_ramp_max", 1.0))

    try:
        rushes_rel = str(rushes_dir.relative_to(root))
    except ValueError:
        rushes_rel = str(rushes_dir)

    shots = flatten_shots(brief)
    entries: list[dict] = []
    status_by_id: dict[str, str] = {}

    for shot in shots:
        plan_dur = float(shot["end"]) - float(shot["start"])
        entry = {
            "id": shot["id"],
            "expected": shot.get("filename"),
            "file": None,
            "match": None,
            "duration_s": None,
            "width": None,
            "height": None,
            "fps": None,
            "has_audio": False,
            "is_image": False,
            "plan_duration_s": round(plan_dur, 3),
            "type": shot["type"],
            "status": "missing",
        }
        path, method = find_candidates(rushes_dir, shot)
        if path is None:
            entries.append(entry)
            status_by_id[shot["id"]] = "missing"
            continue
        try:
            rel = str(path.relative_to(root))
        except ValueError:
            rel = str(path)
        entry["file"] = rel
        entry["match"] = method
        info = ffprobe(path)
        if info is None or info["width"] <= 0:
            entry["status"] = "bad_format"
            status_by_id[shot["id"]] = "bad_format"
            entries.append(entry)
            continue
        entry.update({
            "duration_s": info["duration_s"],
            "width": info["width"],
            "height": info["height"],
            "fps": info["fps"],
            "has_audio": info["has_audio"],
            "is_image": info["is_image"],
        })
        if info["is_image"]:
            entry["status"] = "ok"
            status_by_id[shot["id"]] = "ok"
        elif info["duration_s"] is None or info["duration_s"] <= 0:
            entry["status"] = "bad_format"
            status_by_id[shot["id"]] = "bad_format"
        elif info["duration_s"] < plan_dur + TOO_SHORT_MARGIN_S:
            entry["status"] = "too_short"
            needed = plan_dur + 0.2
            dur = info["duration_s"]
            # (a) ralenti seul : etire d'un facteur speed_ramp_max (playbackRate 1/speed_ramp_max)
            if dur * speed_max >= needed:
                entry["recovery"] = "slowmo"
                entry["speed_needed"] = round(max(1.0 / speed_max, min(1.0, dur / needed)), 3)
            # (b) boomerang du propre rush (aller-retour), combine au ralenti si besoin
            elif dur * 2 * speed_max >= needed:
                entry["recovery"] = "boomerang"
                entry["speed_needed"] = round(max(1.0 / speed_max, min(1.0, (2 * dur) / needed)), 3)
            else:
                entry["recovery"] = "substitute"
            entry["recoverable_by_speed"] = entry["recovery"] == "slowmo"
            entry["recoverable_by_boomerang"] = entry["recovery"] in ("slowmo", "boomerang")
            status_by_id[shot["id"]] = "too_short_ok" if entry["recovery"] != "substitute" else "too_short"
        else:
            entry["status"] = "ok"
            status_by_id[shot["id"]] = "ok"
        entries.append(entry)

    missing: list[str] = []
    substitutions: list[dict] = []
    for shot in shots:
        st = status_by_id[shot["id"]]
        if st in ("missing", "bad_format", "too_short"):
            missing.append(shot["id"])
            if shot["type"] == "MOTION" and st == "missing":
                substitutions.append({"shot": shot["id"], "use": "MOTION", "reason": "plan MOTION sans rush, carte générée"})
            else:
                sub = propose_substitution(shot, shots, status_by_id)
                if st == "too_short":
                    sub["reason"] += " (rush propre trop court même en boomerang ralenti)"
                elif st == "bad_format":
                    sub["reason"] += " (rush propre illisible)"
                else:
                    sub["reason"] += " (aucun rush trouvé)"
                substitutions.append(sub)

    out = {
        "rushes_dir": rushes_rel,
        "shots": entries,
        "missing": missing,
        "substitutions": substitutions,
    }
    save_json(args.out, out)

    n_ok = sum(1 for e in entries if e["status"] == "ok")
    log(f"inventory : {n_ok}/{len(entries)} plans ok, {len(missing)} à substituer -> {args.out}")
    for e in entries:
        if e["status"] != "ok":
            rec = f", rattrapage : {e['recovery']}" if e.get("recovery") else ""
            log(f"  - {e['id']} : {e['status']} ({e.get('file') or 'aucun fichier'}{rec})")
    for s in substitutions:
        log(f"  substitution {s['shot']} -> {s['use']} ({s['reason']})")


if __name__ == "__main__":
    main()
