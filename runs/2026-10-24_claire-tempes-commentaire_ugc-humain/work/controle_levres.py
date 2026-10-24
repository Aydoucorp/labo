# Contrôle des lèvres d'un clip Wan : sur chaque mot qui commence par p, b ou m (bouche fermée),
# ouverture minimale de la bouche à ±0,1 s du début du mot (temps de la voix ElevenLabs), comparée à l'ouverture médiane du clip.
# Usage : python3 work/controle_levres.py clip.mp4 debut_voix_s fin_voix_s
import sys, json, numpy as np
sys.path.insert(0, "/home/user/labo/scripts")
from mesure_levres import bouche
clip, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
mots = [w for w in json.load(open("work/mots.json"))["words"] if t0 <= w["start"] < t1]
v, fps = bouche(clip)
med = float(np.median(v))
ok = 0; cibles = [w for w in mots if w["w"].lower().lstrip("«'").startswith(("p", "b", "m"))]
for w in cibles:
    t = w["start"] - t0
    i0, i1 = max(0, int((t - 0.1) * fps)), min(len(v), int((t + 0.1) * fps) + 1)
    mn = float(v[i0:i1].min()) if i1 > i0 else float("nan")
    r = mn / med if med else float("nan")
    etat = "fermée" if r < 0.35 else ("presque" if r < 0.6 else "OUVERTE")
    ok += etat == "fermée"
    print(f"{w['w']:16} {t:5.2f} s  ouverture {r:4.2f} x médiane  {etat}")
print(f"bilabiales fermées : {ok}/{len(cibles)}")
