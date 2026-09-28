#!/usr/bin/env python3
"""Fiche HTML des b-rolls à trouver, livrée dès le découpage (mode A) : une carte par b-roll avec la phrase,
le moment dans l'audio, la durée minimale de la vidéo à chercher, les mots-clés à copier en un clic et une case « Trouvé ».

Lit la clé `brolls` de decoupage.json :
  [{"id": "B01", "debut": 0.0, "fin": 3.2, "phrase": "...", "importance": "Important · accroche",
    "voir": "...", "profil": "...", "mots_fr": [...], "mots_en": [...], "hashtags": [...],
    "eviter": "...", "format": "vertical de préférence"}]

Usage : python3 fiche_brolls.py decoupage.json brolls-a-trouver.html --titre "Marque · Sujet" --depot "dossier GitHub talking_head_broll_2"
"""
import argparse, json, pathlib

MARGE = 1.0  # secondes de vidéo en plus de l'audio, pour la coupe


def fr_num(x):
    return f"{x:.1f}".replace(".", ",")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decoupage")
    ap.add_argument("sortie")
    ap.add_argument("--titre", default="Talking head")
    ap.add_argument("--depot", default="le dossier de b-rolls indiqué, avec le nom de fichier de chaque carte")
    a = ap.parse_args()

    d = json.load(open(a.decoupage))
    brolls = d.get("brolls") or []
    if not brolls:
        raise SystemExit("decoupage.json ne contient pas de clé « brolls »")
    data = []
    for i, b in enumerate(brolls, 1):
        dur = b["fin"] - b["debut"]
        data.append({
            "id": b["id"], "prio": b.get("importance", ""), "moyen": "moyen" in b.get("importance", "").lower(),
            "phrase": b["phrase"], "start": f"{fr_num(b['debut'])} s", "end": f"{fr_num(b['fin'])} s",
            "dur": f"{fr_num(dur)} s", "min": f"{fr_num(dur + MARGE)} s",
            "voir": b.get("voir", ""), "profil": b.get("profil", ""),
            "fr": b.get("mots_fr", []), "en": b.get("mots_en", []), "tags": b.get("hashtags", []),
            "eviter": b.get("eviter", "") + (f" Format : {b['format']}." if b.get("format") else ""),
            "file": f"broll_{i:02d}.mp4",
        })
    tpl = (pathlib.Path(__file__).parent / "fiche_brolls_modele.html").read_text()
    html = (tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False))
               .replace("__SOUS_TITRE__", f"{a.titre} · {len(data)} vidéos à chercher sur les réseaux")
               .replace("__DEPOT__", a.depot)
               .replace("__CLE__", "brolls-" + pathlib.Path(a.sortie).resolve().parent.name)
               .replace("__N__", str(len(data))))
    pathlib.Path(a.sortie).write_text(html)
    print(f"{a.sortie} : {len(data)} b-rolls")


if __name__ == "__main__":
    main()
