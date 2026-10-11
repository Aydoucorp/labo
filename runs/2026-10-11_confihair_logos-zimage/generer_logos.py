# generer_logos.py
# Génère les 20 pistes de logo Confihair avec Z-Image sur KIE (1:1, ~1K, 0,8 crédit par image).
# Découpe prompts/prompts-logo-confihair.txt en un fichier par prompt (prompts/logo-NN.txt), puis appelle
# scripts/kie_image.py --model z-image pour chacun, 5 en parallèle. Les images vont dans sorties/logo-NN_<piste>_v1.png
# et chaque résultat (taskId, crédits, fichier) est ajouté à journal.md.
# Usage : python3 generer_logos.py            (les 20)
#         python3 generer_logos.py 3 12 17    (seulement ces numéros)

import json, re, subprocess, sys, unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parent.parent
SOURCE = RUN / "prompts/prompts-logo-confihair.txt"
JOURNAL = RUN / "journal.md"
VERSION = "v1"

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40].strip("-")

def pistes():
    t = SOURCE.read_text()
    out = []
    for num, titre, prompt in re.findall(r"## (\d+)\. (.+?)\n+```\n(.*?)\n```", t, re.S):
        n = int(num)
        f = RUN / f"prompts/logo-{n:02d}.txt"
        f.write_text(prompt.strip() + "\n")
        out.append((n, titre.strip(), f))
    return out

def generer(piste):
    n, titre, f = piste
    sortie = RUN / f"sorties/logo-{n:02d}_{slug(titre)}_{VERSION}.png"
    r = subprocess.run([sys.executable, str(ROOT / "scripts/kie_image.py"), "--model", "z-image",
                        "--prompt-file", str(f), "--out", str(sortie), "--ratio", "1:1"],
                       capture_output=True, text=True)
    try:
        res = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        res = {"state": "erreur", "error": (r.stderr or r.stdout).strip()[-200:]}
    return n, titre, sortie, res

def main():
    voulus = {int(x) for x in sys.argv[1:]}
    todo = [p for p in pistes() if not voulus or p[0] in voulus]
    if not JOURNAL.exists():
        JOURNAL.write_text("# Journal des générations\n\n| Logo | Version | Modèle | Prompt | taskId | État | Fichier | Crédits |\n|---|---|---|---|---|---|---|---|\n")
    with ThreadPoolExecutor(5) as ex:
        for n, titre, sortie, res in ex.map(generer, todo):
            fichier = f"`sorties/{sortie.name}`" if res.get("state") == "success" else res.get("error", "")
            ligne = (f"| {n:02d} {titre} | {VERSION} | z-image 1:1 | `prompts/logo-{n:02d}.txt` | {res.get('taskId', '')} "
                     f"| {res.get('state')} | {fichier} | {res.get('credits', '')} |\n")
            with JOURNAL.open("a") as j:
                j.write(ligne)
            print(f"logo {n:02d} : {res.get('state')} {res.get('file', res.get('error', ''))}", flush=True)

if __name__ == "__main__":
    main()
