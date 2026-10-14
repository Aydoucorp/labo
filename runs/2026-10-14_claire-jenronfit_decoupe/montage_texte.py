# montage_texte.py
# Rassemble les 4 parties nettoyées dans VMake (3 images perdues au début de chaque partie, compensées par 3 copies
# de la première image) et remet ses textes en français, au même endroit, aux mêmes images et dans le même style
# (blanc demi-gras centré, sans contour, ombre douce). Positions relevées sur l'original, plages par différence
# original / nettoyé, tailles calées sur la largeur des textes anglais (TikTok Sans 600).
# « You should use minoxidil » (0 à 3,7 s) n'est pas remis : l'utilisateur l'ajoute lui-même.
# Son d'origine. Sortie 1080x1920.
# Usage : python3 montage_texte.py [--frames i1,i2,...]   (images de contrôle dans work/)
import subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RUN = Path(__file__).resolve().parent
W, H, FPS, K = 1080, 1920, 30, 1080 / 720
DECALAGE = 3
SRC = RUN / "source/original.mp4"
OUT = RUN / "sorties/claire-huile-sans-minoxidil-fr_v1.mp4"
FONTFILE = str(RUN / "work/fonts/TikTokSans-600.ttf")
LARGEUR_MAX = 640  # px source : au-delà, la ligne est coupée en deux

# (première image, dernière image, lignes, centre vertical de la 1re ligne en px source, taille px source, interligne px source)
TEXTES = [
    (112, 147, ["Non merci…"], 735, 38.7, 40),
    (112, 147, ["parce que CETTE huile", "existe"], 786, 28.3, 31),
    (148, 271, ["- réduit la chute de 92 %"], 685, 28.5, 44),
    (166, 271, ["- réduit la casse dès la première utilisation"], 729, 28.5, 44),
    (187, 271, ["- pousse visible en 30 à 60 jours"], 772, 28.5, 44),
    (214, 271, ["- formule non grasse"], 816, 28.5, 44),
    (238, 271, ["- zéro minoxidil, zéro finastéride"], 861, 28.5, 44),
    (272, 321, ["ma chute a diminué en 4 semaines !"], 790, 28.7, 34),
    (322, 379, ["a complètement transformé mes cheveux"], 697, 29.5, 34),
]

def couper(l, font):
    if font.getlength(l) <= LARGEUR_MAX * K:
        return [l]
    m = l.split(" ")
    k = min(range(1, len(m)), key=lambda k: max(font.getlength(" ".join(m[:k])), font.getlength(" ".join(m[k:]))))
    return [" ".join(m[:k]), " ".join(m[k:])]

def calque(lignes, cy, size, pitch):
    font = ImageFont.truetype(FONTFILE, round(size * K))
    lignes = [x for l in lignes for x in couper(l, font)]
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    om = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(om)
    for n, l in enumerate(lignes):
        y = (cy + n * pitch) * K
        od.text((W / 2 + 1, y + 2), l, font=font, fill=(0, 0, 0, 190), anchor="mm")
        d.text((W / 2, y), l, font=font, fill="white", anchor="mm")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(om.filter(ImageFilter.GaussianBlur(3)))
    img.alpha_composite(txt)
    return img

CALQUES = [(a, b, calque(l, y, s, p)) for a, b, l, y, s, p in TEXTES]

def frames():
    fr = []
    for i in range(1, 5):
        cap = cv2.VideoCapture(str(RUN / f"source/nettoyees/partie-{i}.mp4")); part = []
        while True:
            ok, f = cap.read()
            if not ok: break
            part.append(f)
        fr += [part[0]] * DECALAGE + part
    return fr

def compose(fr, i):
    img = Image.fromarray(cv2.resize(cv2.cvtColor(fr[i], cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_LANCZOS4)).convert("RGBA")
    for a, b, c in CALQUES:
        if a <= i <= b: img.alpha_composite(c)
    return img.convert("RGB")

def main():
    fr = frames()
    assert len(fr) == 395, len(fr)
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for s in sys.argv[2].split(","):
            compose(fr, int(s)).save(RUN / f"work/controle_{int(s):03d}.jpg", quality=88)
        return
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", str(SRC), "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                          "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                          "-movflags", "+faststart", str(OUT)], stdin=subprocess.PIPE)
    for i in range(len(fr)):
        p.stdin.write(compose(fr, i).tobytes())
    p.stdin.close(); p.wait(); print(OUT, len(fr), "images")

if __name__ == "__main__":
    main()
