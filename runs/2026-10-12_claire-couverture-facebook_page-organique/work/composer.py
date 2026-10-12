#!/usr/bin/env python3
"""Pose le nom et la signature de Claire (vraies polices de la charte) sur un fond de couverture Facebook.
   composer.py fond.png sortie.png [--apercu apercu.png]
   Sortie 1640x923 (16:9) : le mobile affiche toute l'image, l'ordinateur un bandeau central 2,63:1 (environ 1640x624),
   donc le texte reste au centre de ce bandeau. --apercu trace le cadre ordinateur pour contrôle."""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = pathlib.Path(__file__).parent / "fonts"
W, H = 1640, 923
NOM, SIGNATURE = "Les cheveux de Claire", "Tes cheveux ont changé. Toi aussi."
TERRACOTTA, ENCRE, CREME = (168, 85, 58), (46, 42, 38), (250, 246, 243)

fond, sortie = sys.argv[1], sys.argv[2]
im = Image.open(fond).convert("RGB")
# recadrage 16:9 exact puis mise à l'échelle
r = im.width / im.height
if r > W / H:
    w = round(im.height * W / H); im = im.crop(((im.width - w) // 2, 0, (im.width - w) // 2 + w, im.height))
else:
    h = round(im.width * H / W); im = im.crop((0, (im.height - h) // 2, im.width, (im.height - h) // 2 + h))
im = im.resize((W, H), Image.LANCZOS)

f_nom = ImageFont.truetype(str(D / "Fraunces-opsz72-600.ttf"), 112)
f_sig = ImageFont.truetype(str(D / "SourceSans3-400.ttf"), 46)
d = ImageDraw.Draw(im)
bn, bs = d.textbbox((0, 0), NOM, font=f_nom), d.textbbox((0, 0), SIGNATURE, font=f_sig)
hn, hs, gap = bn[3] - bn[1], bs[3] - bs[1], 34
y0 = H // 2 - (hn + gap + hs) // 2
xn, xs = (W - (bn[2] - bn[0])) // 2 - bn[0], (W - (bs[2] - bs[0])) // 2 - bs[0]

# halo crème très doux derrière le texte, pour la lisibilité sans cadre visible
halo = Image.new("L", (W, H), 0); hd = ImageDraw.Draw(halo)
hd.text((xn, y0 - bn[1]), NOM, font=f_nom, fill=255)
hd.text((xs, y0 + hn + gap - bs[1]), SIGNATURE, font=f_sig, fill=255)
halo = halo.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.55))
im = Image.composite(Image.new("RGB", (W, H), CREME), im, halo)

d = ImageDraw.Draw(im)
d.text((xn, y0 - bn[1]), NOM, font=f_nom, fill=TERRACOTTA)
d.text((xs, y0 + hn + gap - bs[1]), SIGNATURE, font=f_sig, fill=ENCRE)
im.save(sortie, optimize=True)

if "--apercu" in sys.argv:
    ap = im.copy(); a = ImageDraw.Draw(ap); bh = round(W / 2.63)
    a.rectangle((0, (H - bh) // 2, W - 1, (H + bh) // 2), outline=(220, 0, 0), width=4)
    ap.save(sys.argv[sys.argv.index("--apercu") + 1])
print(sortie, im.size)
