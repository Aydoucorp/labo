#!/usr/bin/env python3
"""Récupère et prépare les b-rolls déposés par l'utilisateur, prêts pour le montage.

Pour chaque b-roll attendu (clé `brolls` de decoupage.json, fichier broll_01.mp4, broll_02.mp4…) :
1. Retrouve le fichier dans le dossier de dépôt même s'il est mal nommé (« broll_01.mp4.mp4 », « Broll 1.MOV »).
   S'il reste des fichiers non reconnus, les liste pour que l'utilisateur dise lequel est lequel.
2. Fichier vide ou quasi vide (renommage raté sur GitHub) : le restaure depuis l'historique git
   (dernière version non vide, y compris sous son ancien nom avant renommage).
3. Coupe le son, passe en 30 i/s H.264, recadre au centre en 9:16 si la vidéo est horizontale ou carrée
   (option --garder-horizontal pour un plan en bandeau), et garde les premières secondes : durée de l'audio + marge.
4. Écrit un rapport (tableau) : source, résolution, orientation, durée disponible / nécessaire, son, actions.

Usage : python3 recuperer_brolls.py dossier_depot decoupage.json sortie_public_broll [--marge 1.0] [--garder-horizontal B04]
"""
import argparse, json, pathlib, re, subprocess

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
MIN_OCTETS = 10_000


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
              "-of", "json", str(path)]).stdout
    d = json.loads(out or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    return (v["width"], v["height"], float(d["format"]["duration"]), audio) if v else None


def numero(nom):
    """Numéro de b-roll lu dans un nom de fichier : broll_01, B-roll 1, b1…"""
    m = re.search(r"(?:b[-_ ]?roll|^b)[-_ ]?0*(\d+)", nom.lower())
    return int(m.group(1)) if m else None


def restaurer_depuis_git(path):
    """Dernière version non vide du fichier dans l'historique git (suit les renommages)."""
    repo = sh(["git", "rev-parse", "--show-toplevel"], cwd=path.parent).stdout.strip()
    if not repo:
        return False
    rel = str(path.resolve().relative_to(repo))
    log = sh(["git", "log", "--follow", "--name-only", "--format=%H", "--", rel], cwd=repo).stdout.split("\n")
    commit = None
    for line in log:
        line = line.strip()
        if re.fullmatch(r"[0-9a-f]{40}", line):
            commit = line
        elif line and commit:
            blob = f"{commit}:{line}"
            size = sh(["git", "cat-file", "-s", blob], cwd=repo).stdout.strip()
            if size.isdigit() and int(size) > MIN_OCTETS:
                data = subprocess.run(["git", "show", blob], cwd=repo, capture_output=True).stdout
                path.write_bytes(data)
                return f"restauré depuis {commit[:7]} ({line})"
    # le fichier vidé a pu remplacer un fichier supprimé du même dossier (renommage fait par suppression + ajout)
    log = sh(["git", "log", "--diff-filter=D", "--name-only", "--format=%H", "--", str(pathlib.Path(rel).parent)], cwd=repo).stdout.split("\n")
    commit = None
    for line in log:
        line = line.strip()
        if re.fullmatch(r"[0-9a-f]{40}", line):
            commit = line
        elif line and commit and pathlib.Path(line).suffix.lower() in VIDEO_EXT:
            blob = f"{commit}^:{line}"
            size = sh(["git", "cat-file", "-s", blob], cwd=repo).stdout.strip()
            if size.isdigit() and int(size) > MIN_OCTETS:
                path.write_bytes(subprocess.run(["git", "show", blob], cwd=repo, capture_output=True).stdout)
                return f"restauré depuis {line} supprimé en {commit[:7]}"
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("depot")
    ap.add_argument("decoupage")
    ap.add_argument("sortie")
    ap.add_argument("--marge", type=float, default=1.0)
    ap.add_argument("--garder-horizontal", nargs="*", default=[], help="ids de b-rolls à garder en 16:9 (plan en bandeau)")
    a = ap.parse_args()

    depot, sortie = pathlib.Path(a.depot), pathlib.Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    brolls = json.load(open(a.decoupage)).get("brolls") or []
    fichiers = [f for f in depot.iterdir() if f.is_file() and any(s.lower() in VIDEO_EXT for s in f.suffixes)]
    par_numero = {}
    for f in fichiers:
        n = numero(f.name)
        if n is not None:
            par_numero.setdefault(n, []).append(f)

    lignes, utilises = [], set()
    for i, b in enumerate(brolls, 1):
        besoin = b["fin"] - b["debut"] + a.marge
        cand = par_numero.get(i, [])
        actions = []
        if not cand:
            lignes.append((b["id"], "MANQUANT", "", "", f"{besoin:.1f} s", "", "à fournir"))
            continue
        src = max(cand, key=lambda f: f.stat().st_size)
        utilises.update(cand)
        if src.name != f"broll_{i:02d}.mp4":
            actions.append(f"nom lu : {src.name}")
        if src.stat().st_size < MIN_OCTETS:
            r = restaurer_depuis_git(src)
            if not r:
                lignes.append((b["id"], src.name, "", "", f"{besoin:.1f} s", "", "fichier vide, à redéposer"))
                continue
            actions.append(r)
        info = probe(src)
        if not info:
            lignes.append((b["id"], src.name, "illisible", "", f"{besoin:.1f} s", "", "à redéposer"))
            continue
        w, h, dur, son = info
        orient = "vertical" if h > w else ("carré" if h == w else "horizontal")
        vf = ["fps=30"]
        if h <= w and b["id"] not in a.garder_horizontal:
            vf[:0] = ["crop=ih*9/16:ih:(iw-ih*9/16)/2:0", "scale=1080:1920"]
            actions.append("recadré en 9:16 (centre)")
        else:
            vf.append("scale='if(gt(iw,ih),min(1920,iw),-2)':'if(gt(iw,ih),-2,min(1920,ih))'")
        garde = min(dur, besoin)
        if dur > besoin:
            actions.append(f"gardé 0 → {garde:.1f} s")
        if son:
            actions.append("son coupé")
        out = sortie / f"broll_{i:02d}.mp4"
        sh(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", f"{garde:.3f}", "-an", "-vf", ",".join(vf),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", str(out)], check=True)
        alerte = " (TROP COURT)" if dur < b["fin"] - b["debut"] else ""
        lignes.append((b["id"], src.name, f"{w}×{h}", orient, f"{dur:.1f} s / {besoin:.1f} s{alerte}", "oui" if son else "non", " ; ".join(actions)))

    print("| B-roll | Fichier reçu | Résolution | Orientation | Durée dispo / nécessaire | Son | Actions |")
    print("|---|---|---|---|---|---|---|")
    for l in lignes:
        print("| " + " | ".join(l) + " |")
    autres = [f.name for f in fichiers if f not in utilises]
    if autres:
        print(f"\nFichiers non reconnus (dire à quel b-roll ils correspondent) : {', '.join(autres)}")


if __name__ == "__main__":
    main()
