# montage_texte.py
# Vidéo « thyroidalchemy » (5 s, cuir chevelu en gros plan) : pose le hook FR sur toute la durée, dans le style
# de la capture fournie par l'utilisateur (blanc gras, contour noir, aligné à gauche, au centre de l'image).
# Pas de bandeau, pas de motion, son d'origine conservé. Sortie 1080x1920.
# Usage : python3 montage_texte.py [--frames t1,t2]

import subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original_thyroidalchemy.mp4"
OUT = RUN / "sorties/claire-thyroide-fer-stress-fr_v1.mp4"
W, H, FPS = 1080, 1920, 30
TEXTE = "Comment savoir si ta chute de cheveux vient de la thyroïde, du fer ou du stress ⤵️"
FONT = ImageFont.truetype(str(RUN / "fonts/TikTokSans-700.ttf"), 80)
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
X0, MAXW, LH, CY = 60, 900, 98, 900   # marge gauche, largeur max, interligne, centre vertical du bloc

def lignes(d):
    mots, out, cur = TEXTE.replace(" ⤵️", "").split(), [], ""
    for m in mots:
        t = (cur + " " + m).strip()
        if d.textlength(t, font=FONT) <= MAXW or not cur:
            cur = t
        else:
            out.append(cur); cur = m
    out.append(cur)
    return out

def calque():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    ls = lignes(d)
    y = CY - LH * len(ls) / 2 + LH / 2
    ombre = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ombre)
    for i, l in enumerate(ls):
        od.text((X0 + 3, y + i * LH + 5), l, font=FONT, fill=(0, 0, 0, 150), anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0, 150))
    img.alpha_composite(ombre.filter(ImageFilter.GaussianBlur(5)))
    for i, l in enumerate(ls):
        d.text((X0, y + i * LH), l, font=FONT, fill="white", anchor="lm", stroke_width=6, stroke_fill="black")
    # émoji flèche en fin de dernière ligne
    e = Image.new("RGBA", (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(e).text((6, 6), "⤵️", font=EMOJI, embedded_color=True)
    e = e.crop(e.getbbox()).resize((78, 78), Image.LANCZOS)
    xl = X0 + d.textlength(ls[-1], font=FONT) + 14
    img.alpha_composite(e, (int(xl), int(y + (len(ls) - 1) * LH - 39)))
    return img

def main():
    lay = calque()
    cap = cv2.VideoCapture(str(SRC)); frames = []
    while True:
        ok, f = cap.read()
        if not ok: break
        frames.append(f)
    def compose(i):
        f = cv2.resize(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_LANCZOS4)
        img = Image.fromarray(f).convert("RGBA"); img.alpha_composite(lay); return img.convert("RGB")
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for t in sys.argv[2].split(","):
            compose(min(int(float(t) * FPS), len(frames) - 1)).save(RUN / f"sorties/controle_{float(t):04.1f}s.jpg", quality=88)
        return
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", str(SRC), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(OUT)],
                         stdin=subprocess.PIPE)
    for i in range(len(frames)):
        p.stdin.write(compose(i).tobytes())
    p.stdin.close(); p.wait(); print(OUT)

if __name__ == "__main__":
    main()
