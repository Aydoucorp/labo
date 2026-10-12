# montage_texte.py
# Rassemble les 6 parties nettoyées dans VMake (3 images perdues au début de chaque partie, compensées par 3 copies
# de la première image) et remet ses textes en français, au même endroit, aux mêmes images et dans le même style
# (blanc gras centré, fin contour sombre, émojis couleur). Positions et plages relevées par différence V1 / nettoyé,
# tailles calées sur la largeur des textes anglais. « Single-use vials » n'est pas remis (demande utilisateur).
# Son : celui de la V1 (son d'origine continu, fondu de sortie). Sortie 1080x1920.
# Usage : python3 montage_texte.py [--frames i1,i2,...]   (images de contrôle dans work/)
import subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RUN = Path(__file__).resolve().parent
W, H, FPS, K = 1080, 1920, 30, 1080 / 720
DECALAGE = 3
V1 = RUN / "sorties/claire-chhavi-sans-boite_v1.mp4"
OUT = RUN / "sorties/claire-romarin-fr_v1.mp4"
FONTFILE = str(RUN / "work/fonts/TikTokSans-700.ttf")
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
LARGEUR_MAX = 650  # px source : au-delà, la ligne est coupée en deux

# (première image, dernière image, lignes, haut de la 1re ligne en px source, taille px source, interligne px source, contour)
TEXTES = [
    (0, 119, ["Mes cheveux avant ces shots", "d'huile de romarin... 💔"], 212, 39.5, 48, True),
    (69, 124, ["J'avais tout essayé. Rien ne marchait ❤️‍🩹"], 927, 31, 34, True),
    (120, 411, ["Puis j'ai commencé à utiliser ces shots", "d'huile de romarin régulièrement..."], 177, 33, 40, True),
    (166, 205, ["Juste ce qu'il faut de romarin", "pour que ça marche"], 975, 23.5, 27, False),
    (239, 280, ["100 % d'origine végétale."], 980, 30.5, 34, False),
    (417, 485, ["Chute de cheveux réduite en seulement 14 jours ✨"], 180, 34.5, 40, True),
    (417, 452, ["Avant ❤️‍🩹"], 621, 47.5, 50, True),
    (453, 485, ["Après ✨"], 621, 47.5, 50, True),
    (486, 533, ["Avant ❤️"], 623, 47.5, 50, True),
    (534, 559, ["Mes cheveux repoussent enfin 😍"], 199, 34.5, 40, True),
    (560, 620, ["Résultats visibles en seulement 4 semaines ✨"], 888, 31, 36, True),
    (621, 687, ["Utilisation régulière = différence visible ❤️"], 231, 31, 36, True),
    (644, 687, ["La bonne dose. De vrais résultats. ✨"], 693, 28, 33, True),
    (688, 724, ["Commente « GUIDE » pour avoir le guide gratuitement"], 782, 31, 36, True),
]

def segs(t):
    """Découpe une ligne en morceaux texte / émoji (séquences ZWJ, variantes et tons de peau gardés ensemble)."""
    out, cur, i, cs = [], "", 0, list(t)
    while i < len(cs):
        c = cs[i]
        if ord(c) > 0x2500 and c not in "«»":
            if cur: out.append(("t", cur)); cur = ""
            e = c
            while i + 1 < len(cs) and (cs[i + 1] in "️‍" or 0x1F3FB <= ord(cs[i + 1]) <= 0x1F3FF or cs[i] == "‍"):
                i += 1; e += cs[i]
            out.append(("e", e))
        else:
            cur += c
        i += 1
    if cur: out.append(("t", cur))
    return out

def couper(lignes, font, esz):
    """Coupe en deux (lignes équilibrées) toute ligne plus large que LARGEUR_MAX."""
    res = []
    for l in lignes:
        if largeur(l, font, esz) <= LARGEUR_MAX * K:
            res.append(l); continue
        mots = l.split(" ")
        best = min(range(1, len(mots)), key=lambda k: max(largeur(" ".join(mots[:k]), font, esz), largeur(" ".join(mots[k:]), font, esz)))
        res += [" ".join(mots[:best]), " ".join(mots[best:])]
    return res

def largeur(l, font, esz):
    return sum(font.getlength(s) if k == "t" else esz * 1.1 for k, s in segs(l))

def emoji_img(s, esz):
    e = Image.new("RGBA", (200, 160), (0, 0, 0, 0)); ImageDraw.Draw(e).text((6, 6), s, font=EMOJI, embedded_color=True)
    bb = e.getbbox()
    return e.crop(bb).resize((esz, esz), Image.LANCZOS)

def calque(lignes, top, size, pitch, contour):
    size, pitch = size * K, pitch * K
    font = ImageFont.truetype(FONTFILE, round(size))
    esz = round(size * 1.05)
    lignes = couper(lignes, font, esz)
    cap = -font.getbbox("H", anchor="ls")[1]
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    om = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(om)
    emojis = []
    for n, l in enumerate(lignes):
        base = top * K + cap + n * pitch
        parts = segs(l)
        ws = [font.getlength(s) if k == "t" else esz * 1.1 for k, s in parts]
        x = W / 2 - sum(ws) / 2
        for (k, s), w in zip(parts, ws):
            if k == "t":
                od.text((x + 1, base + 2), s, font=font, fill=(0, 0, 0, 150), anchor="ls")
                if contour:
                    d.text((x, base), s, font=font, fill="white", anchor="ls", stroke_width=2, stroke_fill=(40, 40, 40, 255))
                else:
                    d.text((x, base), s, font=font, fill="white", anchor="ls")
            else:
                emojis.append((s, int(x + esz * 0.08), int(base - cap / 2 - esz / 2)))
            x += w
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(om.filter(ImageFilter.GaussianBlur(2.5)))
    img.alpha_composite(txt)
    for s, x, y in emojis:
        img.alpha_composite(emoji_img(s, esz), (x, y))
    return img

CALQUES = [(a, b, calque(l, t, s, p, c)) for a, b, l, t, s, p, c in TEXTES]

def frames():
    fr = []
    for i in range(1, 7):
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
    assert len(fr) == 725, len(fr)
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for s in sys.argv[2].split(","):
            compose(fr, int(s)).save(RUN / f"work/controle_{int(s):03d}.jpg", quality=88)
        return
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", str(V1), "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                          "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                          "-movflags", "+faststart", str(OUT)], stdin=subprocess.PIPE)
    for i in range(len(fr)):
        p.stdin.write(compose(fr, i).tobytes())
    p.stdin.close(); p.wait(); print(OUT, len(fr), "images")

if __name__ == "__main__":
    main()
