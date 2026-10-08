#!/usr/bin/env python3
"""Bibliothèque des b-rolls du studio : retrouver un plan déjà filmé, trouvé ou généré avant d'en chercher ou d'en générer un nouveau.

Index : bibliotheque/brolls.json (vérité machine) et bibliotheque/brolls.md (tableau lisible, régénéré à chaque écriture).
B-rolls RÉELS (filmés ou trouvés par l'utilisateur, sans IA) : copiés dans bibliotheque/brolls-reels/ et décrits dans
bibliotheque/brolls-reels.md (fichier à part, régénéré à chaque ajout). Règle de l'utilisateur : toujours privilégier
un b-roll réel ; l'IA seulement en dernier recours. La recherche affiche les réels en premier.
Les b-rolls IA ne sont pas copiés : leur entrée pointe vers le fichier dans son run (sur GitHub).

Usage (depuis la racine du studio) :
  python3 scripts/biblio_brolls.py chercher "cheveux tombés lavabo"          # meilleurs plans pour une phrase ou des mots-clés
  python3 scripts/biblio_brolls.py ajouter-brief runs/<run>                  # enregistre les rushes d'un run full b-roll (brief.json + inventory.json)
  python3 scripts/biblio_brolls.py ajouter --json entrees.json               # ajoute des entrées décrites à la main
  python3 scripts/biblio_brolls.py usage <id> --run <run> --plan <plan> --phrase "..."   # note une réutilisation
  python3 scripts/biblio_brolls.py md                                        # régénère brolls.md

Champs d'une entrée : id (br-0001), fichier, original, type (video|image), origine (reel-utilisateur | ia-3d |
ia-realiste | ia-papercut | carte-texte), nature (reel | ia), copie_reel (copie dans brolls-reels/), style, marque, description, mots_cles, duree_s, format, modele,
cout_credits, usages [{run, plan, debut, fin, phrase}], notes.
"""
import argparse, json, os, re, shutil, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "bibliotheque", "brolls.json")
MD = os.path.join(ROOT, "bibliotheque", "brolls.md")
MD_REELS = os.path.join(ROOT, "bibliotheque", "brolls-reels.md")
DIR_REELS = os.path.join(ROOT, "bibliotheque", "brolls-reels")
REEL = ("reel-utilisateur", "filme-utilisateur", "trouve-utilisateur", "stock")
STOP = set("le la les un une des de du d l et a au aux en dans sur sous pour par avec sans ce cette ces tes ta ton mes ma mon "
           "son sa ses qui que qu ne pas plus tres the of a an and in on with to".split())


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def mots(t):
    return {m[:6] for m in re.findall(r"[a-z0-9]+", norm(t)) if m not in STOP and len(m) > 1}


def charger():
    return json.load(open(IDX)) if os.path.exists(IDX) else {"schema": "studio/brolls/1", "brolls": []}


def sauver(lib):
    os.makedirs(os.path.dirname(IDX), exist_ok=True)
    json.dump(lib, open(IDX, "w"), ensure_ascii=False, indent=1)
    ecrire_md(lib)


def sonde(path):
    p = os.path.join(ROOT, path)
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration:stream=width,height", "-of", "json", p],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
        st = d["streams"][0]
        dur = float(d["format"].get("duration", 0) or 0)
        return round(dur, 2), f"{st['width']}x{st['height']}"
    except Exception:  # noqa: BLE001
        return None, None


def nouvel_id(lib):
    n = max([int(b["id"][3:]) for b in lib["brolls"]] or [0]) + 1
    return f"br-{n:04d}"


def slug(txt):
    w = [x for x in re.findall(r"[a-z0-9]+", norm(txt)) if x not in STOP]
    return "-".join(w[:5]) or "broll"


def copier_reel(e):
    """Copie un b-roll réel dans bibliotheque/brolls-reels/ (nom : id_description-courte.ext)."""
    src = os.path.join(ROOT, e["fichier"])
    ext = os.path.splitext(e["fichier"])[1].lower() or ".mp4"
    dst = os.path.join(DIR_REELS, f"{e['id']}_{slug(e['description'])}{ext}")
    os.makedirs(DIR_REELS, exist_ok=True)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy(src, dst)
    e["copie_reel"] = os.path.relpath(dst, ROOT)


def ajouter_entree(lib, e):
    deja = next((b for b in lib["brolls"] if b["fichier"] == e["fichier"]), None)
    if deja:
        for u in e.get("usages", []):
            if u not in deja["usages"]:
                deja["usages"].append(u)
        return deja["id"]
    dur, fmt = sonde(e["fichier"])
    e.setdefault("duree_s", dur)
    e.setdefault("format", fmt)
    e["id"] = nouvel_id(lib)
    for k in ("original", "modele", "cout_credits", "notes", "style", "marque"):
        e.setdefault(k, None)
    e.setdefault("usages", [])
    e.setdefault("mots_cles", [])
    if e.get("origine") in REEL:
        e["origine"] = "reel-utilisateur"
    e["nature"] = "reel" if e.get("origine") == "reel-utilisateur" else "ia"
    if e["nature"] == "reel":
        copier_reel(e)
    lib["brolls"].append(e)
    return e["id"]


ORIGINE = {"UGC": "reel-utilisateur", "STOCK": "reel-utilisateur", "PRODUIT": "reel-utilisateur", "3DSCI": "ia-3d",
           "IAGEN": "ia-3d", "SCREEN": "capture", "SOCIAL": "contenu-utilisateur"}


def ajouter_brief(lib, run, originaux):
    run = run.rstrip("/")
    b = json.load(open(os.path.join(ROOT, run, "brief.json")))
    inv = json.load(open(os.path.join(ROOT, run, "work", "inventory.json")))
    words = json.load(open(os.path.join(ROOT, run, "work", "words.json")))["words"]
    fichier = {s["id"]: s.get("file") for s in inv["shots"]}
    marque = b["project"].get("brand")
    ids = []
    for beat in b["beats"]:
        for s in beat["shots"]:
            f = fichier.get(s["id"])
            if not f or s["type"] == "MOTION":
                continue
            phrase = " ".join(w["w"] for w in words if w["start"] < s["end"] and w["end"] > s["start"])
            e = {"fichier": f"{run}/{f}", "original": originaux.get(s["id"]), "type": "video",
                 "origine": originaux.get(s["id"] + ":origine") or ORIGINE.get(s["type"], s["type"].lower()),
                 "style": "3d-scientifique" if s["type"] in ("3DSCI", "IAGEN") else "realiste-smartphone",
                 "marque": marque, "description": s["description"],
                 "mots_cles": sorted(set((s.get("must_show") or []) + re.findall(r"[a-zA-Zéèêàùç'-]+", s.get("query_fr") or ""))),
                 "requete_en": s.get("query_en"),
                 "usages": [{"run": run, "plan": s["id"], "debut": s["start"], "fin": s["end"], "phrase": phrase}]}
            ids.append((s["id"], ajouter_entree(lib, e)))
    return ids


def chercher(lib, q, n=8):
    qm = mots(q)
    res = []
    for b in lib["brolls"]:
        texte = " ".join([b["description"], " ".join(b.get("mots_cles", [])), b.get("requete_en") or ""] +
                         [u.get("phrase", "") for u in b["usages"]])
        sc = len(qm & mots(texte))
        if sc:
            res.append((sc, b))
    # Règle de l'utilisateur : les b-rolls réels passent avant les b-rolls IA, puis par pertinence
    res.sort(key=lambda x: (x[1].get("nature") != "reel", -x[0]))
    return res[:n]


def ecrire_md(lib):
    L = ["# Bibliothèque des b-rolls\n",
         "Avant de chercher ou de générer un plan, chercher ici : `python3 scripts/biblio_brolls.py chercher \"mots\"`.",
         "Index complet : `brolls.json`. Les fichiers restent dans leur run (GitHub).\n",
         "| ID | Nature | Origine | Style | Durée | Ce qu'on voit | Utilisé pour | Fichier |", "|---|---|---|---|---|---|---|---|"]
    for b in lib["brolls"]:
        us = "<br>".join(f"{u['run'].split('/')[-1][:10]} {u['plan']} : « {u['phrase'][:70]} »" for u in b["usages"])
        L.append(f"| {b['id']} | {'**réel**' if b.get('nature') == 'reel' else 'IA'} | {b['origine']} | {b.get('style') or ''} | {str(b['duree_s']) + ' s' if b.get('duree_s') else 'image'} | {b['description']} | {us} | `{b['fichier']}` |")
    open(MD, "w").write("\n".join(L) + "\n")
    ecrire_md_reels(lib)


def ecrire_md_reels(lib):
    """Fichier à part : description de chaque b-roll réel (sans IA), alimenté à chaque nouvel ajout."""
    R = [b for b in lib["brolls"] if b.get("nature") == "reel"]
    L = ["# B-rolls réels (sans IA)\n",
         "Plans filmés ou trouvés par l'utilisateur. **À privilégier toujours** : un b-roll IA ne se génère qu'en dernier recours,",
         "quand aucun b-roll réel ne colle et que l'utilisateur n'en a pas trouvé.",
         "Fichiers stockés dans `bibliotheque/brolls-reels/` (copie) ; ce fichier est régénéré à chaque nouveau b-roll.\n",
         f"**{len(R)} b-rolls réels.**\n",
         "| ID | Durée | Format | Ce qu'on voit | Mots-clés | Utilisé pour | Fichier stocké |", "|---|---|---|---|---|---|---|"]
    for b in R:
        us = "<br>".join(f"{u['run'].split('/')[-1][:10]} {u['plan']} : « {u.get('phrase', '')[:60]} »" for u in b["usages"])
        L.append(f"| {b['id']} | {str(b['duree_s']) + ' s' if b.get('duree_s') else 'image'} | {b.get('format') or ''} | {b['description']} | "
                 f"{', '.join([m for m in b.get('mots_cles', []) if norm(m) not in STOP][:8])} | {us} | `{b.get('copie_reel') or b['fichier']}` |")
    open(MD_REELS, "w").write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("chercher"); c.add_argument("q"); c.add_argument("--n", type=int, default=8)
    a = sp.add_parser("ajouter-brief"); a.add_argument("run"); a.add_argument("--originaux", default=None,
                                                                             help="JSON {plan: chemin original, 'plan:origine': origine}")
    j = sp.add_parser("ajouter"); j.add_argument("--json", required=True)
    u = sp.add_parser("usage"); u.add_argument("id"); u.add_argument("--run", required=True); u.add_argument("--plan", required=True)
    u.add_argument("--phrase", default=""); u.add_argument("--debut", type=float); u.add_argument("--fin", type=float)
    sp.add_parser("md")
    a2 = ap.parse_args()
    lib = charger()
    if a2.cmd == "chercher":
        for sc, b in chercher(lib, a2.q, a2.n):
            print(f"{b['id']}  score {sc}  {'RÉEL' if b.get('nature') == 'reel' else 'IA  '}  {b['origine']:18} {b.get('duree_s')} s  {b['description']}\n        {b['fichier']}")
        return
    if a2.cmd == "ajouter-brief":
        orig = json.load(open(a2.originaux)) if a2.originaux else {}
        for sid, bid in ajouter_brief(lib, a2.run, orig):
            print(sid, "->", bid)
    elif a2.cmd == "ajouter":
        for e in json.load(open(a2.json)):
            print(ajouter_entree(lib, e), e["fichier"])
    elif a2.cmd == "usage":
        b = next(x for x in lib["brolls"] if x["id"] == a2.id)
        b["usages"].append({"run": a2.run, "plan": a2.plan, "debut": a2.debut, "fin": a2.fin, "phrase": a2.phrase})
    sauver(lib)
    print(f"bibliothèque : {len(lib['brolls'])} b-rolls -> {os.path.relpath(IDX, ROOT)}")


if __name__ == "__main__":
    main()
