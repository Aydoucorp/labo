# montage_texte.py
# Remet ses textes, traduits en français, sur la vidéo nettoyée (parties VMake réassemblées comme dans assembler.py),
# au même endroit, dans le même style (blanc gras, ombre légère, centré) et aux mêmes images que l'original :
#   - hook 4 lignes : images 0 à 160 ; - « ÇA 🥹🙌🏼🤭 » : 161 à la fin ; - « détails en description » (italique) : 293 à la fin.
# Positions relevées par différence original / nettoyé (px source 720x1280). Son d'origine. Sortie 1080x1920.
# Usage : python3 montage_texte.py [--frames i1,i2]
import subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
RUN = Path(__file__).resolve().parent
W, H, FPS, K = 1080, 1920, 30, 1080 / 720
DECALAGE = 3
OUT = RUN / "sorties/claire-trois-produits-fr_v2.mp4"
FONTFILE = str(RUN / "work/fonts/TikTokSans-700.ttf")
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
ESZ = 60

# (première image, dernière image, lignes, centre vertical de la 1re ligne en px source, italique, taille, interligne)
TEXTES = [
    (0, 160, ["il y a TROIS", "produits qui m'ont aidée", "à transformer mes", "cheveux, de ÇA à..."], 650, False, 62, 66),
    (161, 338, ["ÇA 🥹🙌🏼🤭"], 697, False, 62, 66),
    (293, 338, ["détails en description"], 861, True, 52, 60),
]

def segs(t):
    out, cur, i = [], "", 0
    cs = list(t)
    while i < len(cs):
        c = cs[i]
        if ord(c) > 0x2500:
            if cur: out.append(("t", cur)); cur = ""
            e = c
            while i + 1 < len(cs) and (0x1F3FB <= ord(cs[i + 1]) <= 0x1F3FF or cs[i + 1] == "️"):
                i += 1; e += cs[i]
            out.append(("e", e))
        else:
            cur += c
        i += 1
    if cur: out.append(("t", cur))
    return out

def draw_text_layer(lignes, y0, italic, size, LH):
    FONT = ImageFont.truetype(FONTFILE, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    emojis = []
    for n, l in enumerate(lignes):
        cy = y0 * K + n * LH
        parts = segs(l)
        widths = [d.textlength(s, font=FONT) if k == "t" else ESZ + 4 for k, s in parts]
        x = W / 2 - sum(widths) / 2
        for (k, s), w in zip(parts, widths):
            if k == "t":
                sd.text((x + 2, cy + 3), s, font=FONT, fill=(0, 0, 0, 170), anchor="lm")
                d.text((x, cy), s, font=FONT, fill="white", anchor="lm")
            else:
                emojis.append((s, x + 2, cy))
            x += w
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    if italic:
        # faux italique : cisaillement horizontal autour de la ligne
        a = np.array(lay); cy = int(y0 * K); M = np.float32([[1, -0.2, 0.2 * cy], [0, 1, 0]])
        lay = Image.fromarray(cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR))
        b = np.array(img); img = Image.fromarray(cv2.warpAffine(b, M, (W, H), flags=cv2.INTER_LINEAR))
    img.alpha_composite(lay)
    for s, x, cy in emojis:
        e = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); ImageDraw.Draw(e).text((6, 6), s, font=EMOJI, embedded_color=True)
        bb = e.getbbox()
        if bb: img.alpha_composite(e.crop(bb).resize((ESZ, ESZ), Image.LANCZOS), (int(x), int(cy - ESZ / 2)))
    return img

LAYERS = [(a, b, draw_text_layer(l, y, it, sz, lh)) for a, b, l, y, it, sz, lh in TEXTES]

def frames():
    fr = []
    for i in range(1, 4):
        cap = cv2.VideoCapture(str(RUN / f"source/nettoyees/partie-{i}.mp4")); part = []
        while True:
            ok, f = cap.read()
            if not ok: break
            part.append(f)
        fr += [part[0]] * DECALAGE + part
    return fr

def compose(fr, i):
    img = Image.fromarray(cv2.resize(cv2.cvtColor(fr[i], cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_LANCZOS4)).convert("RGBA")
    for a, b, lay in LAYERS:
        if a <= i <= b: img.alpha_composite(lay)
    return img.convert("RGB")

def main():
    fr = frames()
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for s in sys.argv[2].split(","):
            compose(fr, int(s)).save(RUN / f"sorties/controle_{int(s):03d}.jpg", quality=88)
        return
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", str(RUN / "source/original.mp4"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                          "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                          "-movflags", "+faststart", str(OUT)], stdin=subprocess.PIPE)
    for i in range(len(fr)):
        p.stdin.write(compose(fr, i).tobytes())
    p.stdin.close(); p.wait(); print(OUT, len(fr), "images")

if __name__ == "__main__":
    main()
