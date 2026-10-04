# reperer_textes.py
# Repère la boîte (x0,y0,x1,y1 en px 720x1280) et les images de début/fin de chacun de ses textes incrustés.
# Masque fixe par texte : pixels blancs fins (top-hat) présents sur >= 80 % des images du cœur de la plage,
# puis présence image par image (part du masque allumée) pour trouver le début et la fin exacts.
# Sortie : work/textes.json
import json, cv2, numpy as np
from pathlib import Path
RUN = Path(__file__).resolve().parent
cap = cv2.VideoCapture(str(RUN / "source/original_complet.mp4")); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
k = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
def tm(f):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    return (cv2.morphologyEx(g, cv2.MORPH_TOPHAT, k) > 35) & (g > 190)
# nom : (cœur de plage en s, fenêtre de recherche en s, zone y)
T = {"want": ((0.8, 2.0), (0.0, 3.0), (330, 450)), "try": ((3.2, 4.1), (2.5, 4.9), (420, 540)),
     "bay": ((4.6, 5.5), (4.0, 6.0), (470, 560)), "rosemary": ((6.1, 6.6), (5.7, 7.0), (470, 560)),
     "cloves": ((7.2, 9.1), (6.8, 9.5), (470, 560)), "water": ((9.7, 11.5), (9.3, 12.0), (470, 560)),
     "simmer": ((12.2, 14.0), (11.8, 15.0), (660, 800)), "strain": ((16.6, 18.0), (16.0, 18.6), (430, 530)),
     "pour": ((19.0, 19.8), (18.5, 20.3), (700, 800)), "apply": ((20.8, 26.4), (20.0, 27.2), (290, 480)),
     "result": ((27.6, 32.0), (27.0, 32.6), (240, 420)), "remember": ((33.2, 37.8), (32.4, 38.3), (290, 460)),
     "save": ((38.7, 42.2), (38.0, 42.7), (280, 400))}
out = {}
for n, ((a, b), (wa, wb), (y0, y1)) in T.items():
    acc = np.mean([tm(fr[i])[y0:y1] for i in range(int(a * 30), int(b * 30))], axis=0)
    m = (acc >= 0.7).astype(np.uint8)
    nl, lab, st, _ = cv2.connectedComponentsWithStats(m)
    for i in range(1, nl):
        if st[i, cv2.CC_STAT_AREA] < 5: m[lab == i] = 0
    ys, xs = np.nonzero(m)
    box = [int(xs.min()), int(ys.min() + y0), int(xs.max()), int(ys.max() + y0)]
    pres = [float(tm(fr[i])[y0:y1][m > 0].mean()) for i in range(int(wa * 30), min(int(wb * 30), len(fr)))]
    on = [int(wa * 30) + j for j, p in enumerate(pres) if p > 0.35]
    out[n] = {"box": box, "debut": on[0], "fin": on[-1], "pixels": int(m.sum())}
    print(n, out[n])
json.dump(out, open(RUN / "work/textes.json", "w"), indent=1)
