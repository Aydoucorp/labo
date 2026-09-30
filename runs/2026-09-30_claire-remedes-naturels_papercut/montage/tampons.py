# Compose les tampons de notes (1/10, 0/10, 5/10) façon tampon encreur, en PNG transparent, puis une courte séquence
# d'impact (le tampon tombe : grand et transparent -> taille finale, petit rebond) pour la superposer au montage.
import numpy as np, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/home/user/labo/skills/creation-full-b-roll-artiste/assets/remotion/public/fonts/Montserrat-ExtraBold.ttf"
NOTES = {"1-10": ("1/10", (168, 85, 58)), "0-10": ("0/10", (168, 85, 58)), "5-10": ("5/10", (122, 67, 81))}
rng = np.random.default_rng(7)

def tampon(txt, col, w=520):
    h = int(w * 0.62)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w - 10, h - 10), radius=26, outline=col + (255,), width=16)
    d.rounded_rectangle((34, 34, w - 34, h - 34), radius=16, outline=col + (255,), width=5)
    f = ImageFont.truetype(F, int(h * 0.56)); bb = d.textbbox((0, 0), txt, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f, fill=col + (255,))
    a = np.array(im); alpha = a[..., 3].astype(float)
    grain = rng.random(alpha.shape)                       # encre irrégulière : trous et zones plus claires
    alpha *= np.where(grain < 0.10, 0.15, np.where(grain < 0.25, 0.75, 1.0))
    a[..., 3] = alpha.clip(0, 255).astype(np.uint8)
    im = Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.6))
    return im.rotate(-10, expand=True, resample=Image.BICUBIC)

for k, (txt, col) in NOTES.items():
    t = tampon(txt, col); out = pathlib.Path(f"montage/tampons/{k}"); out.mkdir(parents=True, exist_ok=True)
    t.save(out / "final.png")
    # séquence d'impact : 5 images de chute (échelle 1,6 -> 1,0, opacité 0,3 -> 1) + 3 images de rebond
    scales = [1.6, 1.4, 1.22, 1.08, 1.0, 0.96, 1.02, 1.0]; ops = [0.3, 0.5, 0.7, 0.9, 1, 1, 1, 1]
    W, H = int(t.width * 1.6) + 4, int(t.height * 1.6) + 4
    for i, (s, o) in enumerate(zip(scales, ops)):
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ti = t.resize((int(t.width * s), int(t.height * s)), Image.LANCZOS)
        a = np.array(ti); a[..., 3] = (a[..., 3] * o).astype(np.uint8); ti = Image.fromarray(a)
        fr.alpha_composite(ti, ((W - ti.width) // 2, (H - ti.height) // 2)); fr.save(out / f"f{i:03d}.png")
    print(k, W, H)
