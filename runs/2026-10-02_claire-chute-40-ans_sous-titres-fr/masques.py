# masques.py
# Construit les masques de ses textes incrustés (un masque fixe par texte) pour les effacer par inpainting gratuit (OpenCV).
# Méthode : un pixel est « texte » s'il est blanc et fin (top-hat) sur au moins 80 % des images où le texte est
# pleinement visible ; on dilate ensuite pour couvrir le contour noir et l'ombre. Les émojis sont pris en rectangle.
# Sortie : work/masque_<nom>.png (720x1280) + work/masques_apercu.jpg
# Usage : python3 masques.py

import cv2, numpy as np
from pathlib import Path

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original_pure-batana76.mp4"

# nom : (images pleinement visibles, zone de recherche x0,y0,x1,y1, rectangles émoji)
TEXTES = {
    "hook":    ((2, 76),    (40, 205, 712, 335), [(560, 262, 700, 330)]),
    "jour1":   ((18, 76),   (150, 130, 570, 205), []),
    "jour14":  ((100, 158), (150, 130, 570, 205), []),
    "jour90":  ((178, 256), (150, 130, 570, 205), []),
    "jour180": ((294, 350), (150, 130, 570, 205), [(436, 136, 500, 202)]),
}

def frames():
    cap = cv2.VideoCapture(str(SRC)); out = []
    while True:
        ok, f = cap.read()
        if not ok:
            return out
        out.append(f)

def build(fr):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    masks = {}
    for nom, ((a, b), (x0, y0, x1, y1), emojis) in TEXTES.items():
        acc = np.zeros(fr[0].shape[:2], np.float32)
        for f in fr[a:b + 1]:
            g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, k)
            acc += ((th > 40) & (g > 200)).astype(np.float32)
        acc /= (b - a + 1)
        m = np.zeros_like(acc, np.uint8)
        m[y0:y1, x0:x1] = (acc[y0:y1, x0:x1] >= 0.8).astype(np.uint8) * 255
        # supprime les petits points isolés (reflets fixes)
        n, lab, st, _ = cv2.connectedComponentsWithStats(m)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] < 6:
                m[lab == i] = 0
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
        # l'ombre portée part vers le bas : on prolonge le masque de 3 px vers le bas
        m = np.maximum(np.maximum(m, np.roll(m, 4, axis=0)), np.roll(np.roll(m, 3, axis=0), 3, axis=1))
        for (ex0, ey0, ex1, ey1) in emojis:
            m[ey0:ey1, ex0:ex1] = 255
        masks[nom] = m
        cv2.imwrite(str(RUN / f"work/masque_{nom}.png"), m)
    return masks

if __name__ == "__main__":
    fr = frames()
    masks = build(fr)
    tiles = []
    for nom, idx in [("hook", 40), ("jour14", 130), ("jour90", 220), ("jour180", 320)]:
        f = fr[idx].copy()
        full = masks[nom] if nom != "hook" else np.maximum(masks["hook"], masks["jour1"])
        f[full > 0] = (0, 0, 255)
        tiles.append(f[100:360])
    cv2.imwrite(str(RUN / "work/masques_apercu.jpg"), np.vstack(tiles))
