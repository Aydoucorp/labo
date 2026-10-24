# Motion design M2 (voix 53,12 à 57,40) : « si tu cibles correctement le cuir chevelu et que tu le traites comme une zone délicate ».
# Même visage que B6 (work/motion_b6.py) : une cible terracotta se pose sur la tempe, zoom, une goutte de soin tombe, halo doux « ZONE DÉLICATE ».
# Usage : python3 work/motion_m2.py [--image t ...]
import sys, math, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motion_b6 as mb
from motion_b6 import Image, ImageDraw, ImageFilter, F, rgb, p, S, calque, ease, texte, TERRA, TERRA_C, PRUNE, CREME, CX, W, H, FPS
DUREE = 4.28
TX, TY = mb.ligne_frontale(.86, .6)        # tempe droite (à droite de l'image)
TY += 30

def camera(t):
    a = p(t, 1.25, 1.85)                   # zoom sur la tempe sur « le cuir chevelu »
    k = 1.12 + .78 * a
    fx, fy = CX + (TX - CX) * a, mb.CY + (TY - mb.CY) * a
    sx, sy = CX + (600 - CX) * a, mb.CY + (760 - mb.CY) * a
    return k, fx, fy, sx, sy
mb.camera = camera

def cible(d, v, t):
    a = p(t, .30, .50) * (1 - p(t, 2.55, 2.80))
    if a <= 0: return
    e = 2.6 - 1.6 * p(t, .30, .75)         # arrive en grand puis se resserre sur « cibles »
    flash = math.exp(-((t - .90) / .10) ** 2) if t > .75 else 0  # verrouillage sur « correctement »
    for rr, w in [(46, 7), (24, 5)]:
        r = rr * e
        d.ellipse(v.boite(TX - r, TY - r, TX + r, TY + r), outline=rgb(TERRA, 255 * a), width=v.L(w + 4 * flash))
    for ang in range(4):
        c, s = math.cos(ang * math.pi / 2), math.sin(ang * math.pi / 2)
        r0, r1 = 52 * e, 74 * e
        d.line([v.P(TX + c * r0, TY + s * r0), v.P(TX + c * r1, TY + s * r1)], fill=rgb(TERRA, 255 * a), width=v.L(7))
    d.ellipse(v.boite(TX - 6, TY - 6, TX + 6, TY + 6), fill=rgb(TERRA, 255 * a))

def pipette(d, v, t):
    a = p(t, 2.60, 2.85) * (1 - p(t, 3.55, 3.80))
    if a <= 0: return
    y0 = TY - 120 + 40 * p(t, 2.60, 2.95)
    x = TX + 8
    d.rounded_rectangle(v.boite(x - 26, y0 - 150, x + 26, y0 - 78), radius=v.L(24), fill=rgb(PRUNE, 255 * a))
    d.rectangle(v.boite(x - 20, y0 - 84, x + 20, y0 - 66), fill=rgb("#5E3340", 255 * a))
    d.rounded_rectangle(v.boite(x - 13, y0 - 68, x + 13, y0 + 4), radius=v.L(10), fill=rgb("#FFFFFF", 150 * a), outline=rgb(PRUNE, 200 * a), width=v.L(3))
    d.rectangle(v.boite(x - 9, y0 - 30, x + 9, y0 - 2), fill=rgb("#E9B35A", 200 * a))
    # la goutte se forme puis tombe sur la tempe
    if 2.95 <= t < 3.35:
        g = (t - 2.95) / .40
        gy = y0 + 10 + (TY - y0 - 10) * ease(g) ** 1.6
        rg = 8 + 3 * min(1, g * 3)
        d.ellipse(v.boite(x - rg, gy - rg * 1.3, x + rg, gy + rg), fill=rgb("#E9B35A", 235 * a))

def halo(im, v, t):
    a = p(t, 3.25, 3.55)
    if a <= 0: return im
    puls = .78 + .22 * math.sin((t - 3.25) * 7)
    h = calque(); dh = ImageDraw.Draw(h)
    for r, al in [(150, 90), (105, 120), (65, 150)]:
        dh.ellipse(v.boite(TX - r, TY - r * .9, TX + r, TY + r * .9), fill=rgb(TERRA_C, al * a * puls))
    im = Image.alpha_composite(im, h.filter(ImageFilter.GaussianBlur(S(30))))
    # onde douce quand la goutte touche la peau
    o = calque(); do = ImageDraw.Draw(o)
    for k in range(2):
        g = (t - 3.35 - .25 * k) / .7
        if 0 < g < 1:
            r = 20 + 110 * g
            do.ellipse(v.boite(TX - r, TY - r * .7, TX + r, TY + r * .7), outline=rgb("#FFFFFF", 200 * (1 - g)), width=v.L(4))
    return Image.alpha_composite(im, o)

TITRES = [  # (début, fin, titre, sous-titre, apparition du sous-titre)
    (0.30, 2.70, "Cible", "LE CUIR CHEVELU", 1.38),
    (2.70, 9.00, "Traite-le comme une", "ZONE DÉLICATE", 3.54),
]

def image(t):
    v = mb.Vue(t)
    lay = calque(); d = ImageDraw.Draw(lay)
    mb.tete(d, v, t + 9, .6, .7)
    mb.duvet(d, v, t + 9, .6, .55)
    im = Image.alpha_composite(mb.FOND, lay)
    im = halo(im, v, t)
    lay = calque(); d = ImageDraw.Draw(lay)
    cible(d, v, t); pipette(d, v, t)
    im = Image.alpha_composite(im, lay)
    tl = calque(); dt_ = ImageDraw.Draw(tl)
    for (t0, t1, tit, sous, ts) in TITRES:
        a = p(t, t0, t0 + .25) * (1 - p(t, t1 - .12, t1 + .1))
        if a <= 0: continue
        bande = calque(); ImageDraw.Draw(bande).rounded_rectangle([S(110), S(140), S(970), S(385)], radius=S(46), fill=rgb(CREME, 215 * a))
        im = Image.alpha_composite(im, bande)
        texte(dt_, (540, 220), tit, F("Fraunces-SemiBold.ttf", 86 if len(tit) > 12 else 98), TERRA, a)
        texte(dt_, (540, 320), sous, F("SourceSans3-SemiBold.ttf", 64), PRUNE, a * p(t, ts, ts + .2))
    return Image.alpha_composite(im, tl)

if __name__ == "__main__":
    os.makedirs("sorties/motion", exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[1] == "--image":
        for tt in sys.argv[2:]:
            image(float(tt)).convert("RGB").resize((W, H), Image.LANCZOS).save(f"work/m2-motion-{tt}.jpg", quality=88)
        sys.exit()
    out = "sorties/motion/M2-motion-v1.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(round(DUREE * FPS))):
        pr.stdin.write(image(i / FPS).convert("RGB").resize((W, H), Image.LANCZOS).tobytes())
    pr.stdin.close(); pr.wait(); print("écrit :", out)
