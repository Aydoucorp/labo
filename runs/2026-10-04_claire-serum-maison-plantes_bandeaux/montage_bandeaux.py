# montage_bandeaux.py
# Vidéo « sérum maison aux plantes » (42,7 s) :
#  - 0 à 4,9 s : le début nettoyé par l'utilisateur (source/debut-0-5s_sans-texte.mp4), sans aucun texte ajouté
#    (l'utilisateur pose son hook lui-même). Cet extrait commence à l'image 3 de l'original (décalage mesuré).
#  - ensuite : la vidéo d'origine à partir de l'image 150, ses textes anglais cachés par des bandeaux opaques
#    terracotta (texte crème), traduction FR (voir textes.md). Boîtes et timings : work/textes.json (reperer_textes.py).
#  - son d'origine (décalé de 3 images). Pas de motion CTA. Sortie 1080x1920.
# Usage : python3 montage_bandeaux.py [--frames t1,t2,...]

import json, subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

RUN = Path(__file__).resolve().parent
ORIG = RUN / "source/original_complet.mp4"
DEBUT = RUN / "source/debut-0-5s_sans-texte.mp4"
OUT = RUN / "sorties/claire-serum-maison-fr_v1.mp4"
W, H, FPS = 1080, 1920, 30
K = W / 720
DECALAGE = 3          # image 0 du début nettoyé = image 3 de l'original
RACCORD = 150         # première image de l'original utilisée après le début nettoyé
MARGE = 3             # images de bandeau en plus avant / après son texte (fondus)
TERRA, CREME = "#A8553A", "#FAF6F3"

FR = {
    "bay": "4 à 5 feuilles de laurier",
    "rosemary": "2 c. à soupe de romarin séché",
    "cloves": "1 c. à soupe de clous de girofle",
    "water": "35 cl d'eau",
    "simmer": "Laisse mijoter à feu doux environ 10 minutes",
    "strain": "Filtre bien...",
    "pour": "puis verse dans un flacon propre",
    "apply": "Je l'applique directement sur mon cuir chevelu, je masse doucement et je laisse agir sans rincer.",
    "result": "Le résultat ? 👀 Tu vois tous ces petits cheveux de repousse ?",
    "remember": "Mais attention : aucun sérum n'est magique. L'alimentation, les vitamines et une bonne hygiène de vie comptent aussi 😉",
    "save": "Tu testerais ? 🌿 Enregistre cette recette pour plus tard ⬇️",
}
CORRECTIONS = {"strain": [225, 452, 495, 492]}   # boîte relevée à la main (la détection avait pris la passoire)

FONT = ImageFont.truetype(str(RUN / "work/fonts/TikTokSans-600.ttf"), 60)
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
LH, ESZ = 72, 62

def segs(t):
    out, cur = [], ""
    for c in t:
        if ord(c) > 0x2500 and c not in "–":
            if cur: out.append(("t", cur)); cur = ""
            if c == "️": continue
            out.append(("e", c))
        else:
            cur += c
    if cur: out.append(("t", cur))
    return out

def lw(d, t):
    return sum(d.textlength(s, font=FONT) if k == "t" else ESZ + 6 for k, s in segs(t))

def wrap(d, text, maxw=860):
    words = text.split()
    def splits(ws, n):
        if n == 1: yield [ws]; return
        for i in range(1, len(ws) - n + 2):
            for r in splits(ws[i:], n - 1): yield [ws[:i]] + r
    for n in range(1, len(words) + 1):
        best = None
        for c in splits(words, n):
            m = max(lw(d, " ".join(l)) for l in c)
            if m <= maxw and (best is None or m < best[0]): best = (m, c)
        if best: return [" ".join(l) for l in best[1]]
    return [text]

def draw_line(img, d, text, cy):
    x = W / 2 - lw(d, text) / 2
    for k, s in segs(text):
        if k == "t":
            d.text((x, cy), s, font=FONT, fill=CREME, anchor="lm"); x += d.textlength(s, font=FONT)
        else:
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((6, 6), s, font=EMOJI, embedded_color=True)
            bb = e.getbbox()
            if bb: img.alpha_composite(e.crop(bb).resize((ESZ, ESZ), Image.LANCZOS), (int(x + 3), int(cy - ESZ / 2)))
            x += ESZ + 6

def bandeau(text, box):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    ls = wrap(d, text); tw = max(lw(d, l) for l in ls); th = LH * len(ls)
    x0, y0, x1, y1 = [v * K for v in box]
    cy = (y0 + y1) / 2
    bw = min(W - 24, max(tw + 64, (x1 - x0) + 48)); bh = max(th + 36, (y1 - y0) + 40)
    d.rounded_rectangle([W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2], radius=26, fill=TERRA)
    y = cy - th / 2 + LH / 2
    for l in ls:
        draw_line(img, d, l, y); y += LH
    return img

def plan():
    T = json.load(open(RUN / "work/textes.json")); out = []
    for n, txt in FR.items():
        box = CORRECTIONS.get(n, T[n]["box"])
        a = max(T[n]["debut"] - MARGE, RACCORD) - DECALAGE      # en images de sortie
        b = T[n]["fin"] + MARGE - DECALAGE
        out.append((a, b, bandeau(txt, box)))
    return out

def main():
    cd = cv2.VideoCapture(str(DEBUT)); co = cv2.VideoCapture(str(ORIG))
    frames = []
    while True:
        ok, f = cd.read()
        if not ok: break
        frames.append(f)
    for _ in range(RACCORD): co.read()
    while True:
        ok, f = co.read()
        if not ok: break
        frames.append(f)
    P = plan()
    def compose(i):
        img = Image.fromarray(cv2.resize(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_LANCZOS4)).convert("RGBA")
        for a, b, lay in P:
            if a <= i <= b: img.alpha_composite(lay)
        return img.convert("RGB")
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for t in sys.argv[2].split(","):
            compose(min(int(float(t) * FPS), len(frames) - 1)).save(RUN / f"sorties/controle_{float(t):05.2f}s.jpg", quality=88)
        return
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-ss", str(DECALAGE / FPS), "-i", str(ORIG), "-map", "0:v", "-map", "1:a",
                          "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                          "-shortest", "-movflags", "+faststart", str(OUT)], stdin=subprocess.PIPE)
    for i in range(len(frames)):
        p.stdin.write(compose(i).tobytes())
    p.stdin.close(); p.wait(); print(OUT, len(frames), "images")

if __name__ == "__main__":
    main()
