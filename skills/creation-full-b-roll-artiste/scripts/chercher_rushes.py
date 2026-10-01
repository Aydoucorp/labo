# Cherche automatiquement les rushes STOCK / UGC / PRODUIT d'un brief sur Pixabay (vidéos libres de droits),
# propose 3 candidats par plan dans une page HTML (bandes de vignettes intégrées), puis télécharge les choix dans rushes/.
#
# Clé : PIXABAY_API_KEY dans .env à la racine du studio (jamais affichée ; masquée dans tous les messages d'erreur).
#
# Usage (depuis le dossier du projet) :
#   python3 $S/chercher_rushes.py brief.json                      # recherche + work/candidats/ + candidats.html
#   python3 $S/chercher_rushes.py brief.json --plans 03,04b       # seulement certains plans
#   python3 $S/chercher_rushes.py brief.json --choix "01a:2,03:1" # télécharge les choix (numéro 1 à 3) dans rushes/
#   python3 $S/chercher_rushes.py brief.json --choix auto         # prend le candidat 1 de chaque plan
#
# Mots-clés courts optionnels par plan : work/mots_cles.json ({"03": ["scalp serum drop", "hair serum"]}).
# Filtre : une vidéo n'est gardée que si au moins 60 % des mots de la requête sont dans ses tags.
# Stratégie de recherche : la requête du plan sans le suffixe du look book, puis le fallback, puis des versions de
# plus en plus courtes (mots-clés), jusqu'à avoir assez de résultats. Score : vertical, durée suffisante,
# résolution, popularité ; les vidéos générées par IA et de basse qualité passent en dernier.
import argparse, base64, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

API = "https://pixabay.com/api/videos/"
TYPES = {"STOCK", "UGC", "PRODUIT"}
UA = {"User-Agent": "Mozilla/5.0 (studio-claire chercher_rushes)"}  # Pixabay refuse le client Python par défaut (403)
STOP = set("a an the of on in at to with and or for from by into onto over under near next then its her his their "
           "very slowly slow close up view shot top down macro pov".split())


def charger_cle():
    cle = os.environ.get("PIXABAY_API_KEY")
    d = os.getcwd()
    while not cle and d != "/":
        f = os.path.join(d, ".env")
        if os.path.exists(f):
            for ligne in open(f):
                if ligne.startswith("PIXABAY_API_KEY="):
                    cle = ligne.split("=", 1)[1].strip().strip('"')
        d = os.path.dirname(d)
    if not cle:
        sys.exit("PIXABAY_API_KEY introuvable (.env ou variable d'environnement)")
    return cle


def masquer(texte, cle):
    return str(texte).replace(cle, "***")


def get_json(url, cle):
    for essai in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            if "403" in str(e):
                print("  accès refusé (403) :", masquer(e, cle)); break
            if "429" in str(e):
                time.sleep(20)
                continue
            if essai == 2:
                print("  requête échouée :", masquer(e, cle))
            time.sleep(2)
    return {"hits": []}


def requetes(shot, suffixe, manuels=()):
    """Requêtes de la plus précise à la plus large ; les mots-clés manuels (work/mots_cles.json) passent en premier."""
    vues, out = set(), [m for m in manuels]
    vues.update(out)
    base = (shot.get("query_en") or "").replace(suffixe, "").strip(" ,")
    fb = (shot.get("fallback") or {}).get("query_en") or ""
    for q in (base, fb):
        mots = [m for m in re.findall(r"[a-zA-Z']+", q.lower()) if m not in STOP]
        for k in (len(mots), 5, 4, 3, 2):
            if k <= len(mots):
                c = " ".join(mots[:k])[:100]
                if c and c not in vues:
                    vues.add(c); out.append(c)
    return out


def racine(m):
    return m.lower().strip("'s")[:5]


def pertinence(hit, q):
    """Part des mots de la requête retrouvés dans les tags de la vidéo (Pixabay renvoie des résultats très lâches)."""
    mots = [racine(m) for m in re.findall(r"[a-zA-Z]+", q) if m.lower() not in STOP]
    tags = {racine(t) for t in re.findall(r"[a-zA-Z]+", hit.get("tags", ""))}
    return sum(m in tags for m in mots) / max(len(mots), 1)


def score(hit, besoin):
    v = hit["videos"]
    m = v.get("large") if v.get("large", {}).get("width") else v["medium"]
    w, h = m["width"], m["height"]
    s = 0.0
    s += 3 if h > w else (1 if h == w else 0)
    s += 2 if hit["duration"] >= besoin else -5
    s += 1 if max(w, h) >= 1920 else 0
    s += min(hit.get("likes", 0), 500) / 500
    if hit.get("isAiGenerated") or hit.get("isLowQuality"):
        s -= 3
    return s


def telecharger_fichier(url, dest):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def bande(url_tiny, dest, duree):
    """Télécharge la version tiny et en tire une bande de 4 vignettes (jpg)."""
    tmp = dest + ".mp4"
    telecharger_fichier(url_tiny, tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-vf",
                    f"fps=4/{max(duree, 1)},scale=-2:180,tile=4x1:padding=4:color=white", "-frames:v", "1", dest],
                   check=False)
    os.remove(tmp)


def chercher(brief, cle, plans, n):
    suffixe = brief["project"].get("lookbook", {}).get("style_suffix_en", "")
    os.makedirs("work/candidats", exist_ok=True)
    res, deja = {}, set()
    mots_cles = json.load(open("work/mots_cles.json")) if os.path.exists("work/mots_cles.json") else {}
    for beat in brief["beats"]:
        for shot in beat["shots"]:
            sid = shot["id"]
            if shot["type"] not in TYPES or (plans and sid not in plans):
                continue
            besoin = round(shot["end"] - shot["start"] + 0.5, 1)
            hits, pert, utilisees = {}, {}, []
            for q in requetes(shot, suffixe, mots_cles.get(sid, [])):
                url = API + "?" + urllib.parse.urlencode({"key": cle, "q": q, "per_page": 30, "safesearch": "true"})
                d = get_json(url, cle)
                nb = 0
                for hit in d.get("hits", []):
                    p = pertinence(hit, q)
                    if p >= 0.6:
                        hits.setdefault(hit["id"], hit); nb += 1
                        pert[hit["id"]] = max(pert.get(hit["id"], 0), p)
                utilisees.append((q, nb))
                bons = [h for h in hits.values() if h["duration"] >= besoin]
                if len(bons) >= n * 2:
                    break
            classes = sorted(hits.values(), key=lambda h: (h["id"] in deja, -(score(h, besoin) + 3 * pert[h["id"]])))[:n]
            cands = []
            for k, hit in enumerate(classes, 1):
                v = hit["videos"]
                m = v["large"] if v.get("large", {}).get("width") else v["medium"]
                img = f"work/candidats/{sid}_c{k}.jpg"
                bande(v["tiny"]["url"], img, hit["duration"])
                deja.add(hit["id"])
                cands.append({"n": k, "pixabay_id": hit["id"], "page": hit["pageURL"], "url": m["url"],
                              "width": m["width"], "height": m["height"], "duration": hit["duration"],
                              "tags": hit["tags"], "auteur": hit["user"], "vignettes": img,
                              "ia": bool(hit.get("isAiGenerated"))})
            res[sid] = {"description": shot["description"], "start": shot["start"], "end": shot["end"],
                        "besoin_s": besoin, "requetes": utilisees, "candidats": cands}
            print(f"{sid:4} {len(cands)} candidat(s), requêtes : " + " | ".join(f"{q} ({c})" for q, c in utilisees))
    json.dump(res, open("work/candidats.json", "w"), ensure_ascii=False, indent=1)
    page_html(res)
    trouves = sum(1 for r in res.values() if r["candidats"])
    print(f"\n{trouves}/{len(res)} plans avec au moins un candidat. Page : candidats.html")


def page_html(res):
    cartes = []
    for sid, r in res.items():
        lignes = []
        for c in r["candidats"]:
            b64 = base64.b64encode(open(c["vignettes"], "rb").read()).decode() if os.path.exists(c["vignettes"]) else ""
            fmt = "vertical" if c["height"] > c["width"] else "horizontal"
            lignes.append(
                f'<label class="cand"><input type="radio" name="{sid}" value="{c["n"]}">'
                f'<img src="data:image/jpeg;base64,{b64}"><span><b>{c["n"]}</b> · {c["duration"]} s · {c["width"]}x{c["height"]} ({fmt})'
                f'{" · IA" if c["ia"] else ""} · <a href="{c["page"]}" target="_blank">voir sur Pixabay</a></span></label>')
        lignes.append(f'<label class="cand aucun"><input type="radio" name="{sid}" value="0"> Aucun ne va (je cherche moi-même ou génération IA)</label>')
        cartes.append(f'<section><h2>{sid} <small>{r["start"]:.1f} à {r["end"]:.1f} s · il faut {r["besoin_s"]} s mini</small></h2>'
                      f'<p>{r["description"]}</p>{"".join(lignes)}</section>')
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Choix des rushes</title><style>
:root{{--bg:#FAF6F3;--card:#fff;--ink:#2E2A26;--acc:#A8553A;--line:#EFE7E0}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,sans-serif;padding:16px;max-width:980px;margin:auto}}
h1{{color:var(--acc)}} section{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0}}
h2{{margin:0 0 4px}} small{{color:#7a716a;font-weight:400}} .cand{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:8px;border-radius:8px;cursor:pointer}}
.cand:hover{{background:var(--line)}} .cand img{{max-width:100%;height:auto;border-radius:6px}} a{{color:var(--acc)}}
#barre{{position:sticky;bottom:0;background:var(--acc);color:#fff;padding:12px;border-radius:12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
#barre code{{background:#fff;color:var(--ink);padding:4px 8px;border-radius:6px;word-break:break-all;flex:1}} button{{padding:8px 14px;border:0;border-radius:8px;cursor:pointer}}
</style></head><body><h1>Choix des rushes</h1><p>Pour chaque plan, coche la vidéo qui colle le mieux à la phrase. Les 4 vignettes montrent le début, le milieu et la fin de la vidéo. Quand c'est fini, copie la ligne en bas et envoie-la.</p>
{"".join(cartes)}
<div id="barre"><b>Ta sélection :</b><code id="sel">(rien de coché)</code><button onclick="navigator.clipboard.writeText(document.getElementById('sel').textContent)">Copier</button></div>
<script>
function maj(){{const v=[...document.querySelectorAll('input:checked')].map(i=>i.name+':'+i.value);document.getElementById('sel').textContent=v.length?v.join(','):'(rien de coché)'}}
document.querySelectorAll('input').forEach(i=>i.addEventListener('change',maj));
</script></body></html>"""
    open("candidats.html", "w").write(html)


def telecharger(brief, choix_txt):
    res = json.load(open("work/candidats.json"))
    if choix_txt == "auto":
        choix = {sid: 1 for sid, r in res.items() if r["candidats"]}
    else:
        choix = {a.strip(): int(b) for a, b in (c.split(":") for c in choix_txt.split(",") if ":" in c)}
    noms = {s["id"]: s["filename"] for b in brief["beats"] for s in b["shots"]}
    os.makedirs("rushes", exist_ok=True)
    credits = []
    for sid, k in choix.items():
        if k == 0 or sid not in res:
            continue
        c = next((c for c in res[sid]["candidats"] if c["n"] == k), None)
        if not c:
            print(f"{sid} : candidat {k} inexistant"); continue
        dest = os.path.join("rushes", noms[sid])
        telecharger_fichier(c["url"], dest)
        credits.append(f"| {sid} | {c['page']} | {c['auteur']} |")
        print(f"{sid} -> {dest} ({c['width']}x{c['height']}, {c['duration']} s)")
    with open("rushes/SOURCES.md", "a") as f:
        f.write("\n| Plan | Source Pixabay | Auteur |\n|---|---|---|\n" + "\n".join(credits) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--plans", default="", help="IDs séparés par des virgules (par défaut : tous les STOCK, UGC, PRODUIT)")
    ap.add_argument("--n", type=int, default=3, help="candidats par plan")
    ap.add_argument("--choix", default=None, help='"01a:2,03:1" ou "auto"')
    a = ap.parse_args()
    brief = json.load(open(a.brief))
    if a.choix:
        telecharger(brief, a.choix)
    else:
        chercher(brief, charger_cle(), set(filter(None, a.plans.split(","))), a.n)


if __name__ == "__main__":
    main()
