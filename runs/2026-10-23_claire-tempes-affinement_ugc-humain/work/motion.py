# Motion design aux couleurs de Claire, calé au mot près sur la voix : python3 work/motion.py [B2|B5a|B5b ...]
# Rendu 1080x1920, 30 i/s, suréchantillonné x2 ; le tiers bas (sous-titres vers 1150 à 1290 px) reste libre.
import sys, math, subprocess, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS, SS = 1080, 1920, 30, 2
FD = "/home/user/labo/runs/2026-10-08_claire-menopause-affinement_talking-head/montage/fonts_charte/"
TERRA, TERRA_C, PRUNE, CREME, CREME_F, ENCRE = "#A8553A", "#C9805F", "#7A4351", "#FAF6F3", "#EFE7E0", "#2E2A26"
PEAU, PEAU_F, CHEVEU = "#F3CDB6", "#E4A98C", "#3B2A22"
def F(nom, t): return ImageFont.truetype(FD + nom, int(t * SS))
def rgb(h, a=255): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)
def cl(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = cl(x); return x * x * (3 - 2 * x)
def p(t, a, b): return ease((t - a) / (b - a)) if b > a else float(t >= a)
def S(v): return int(v * SS)

def fond():
    im = Image.new("RGBA", (W * SS, H * SS), rgb(CREME))
    v = Image.new("L", (W // 8, H // 8), 0); dv = ImageDraw.Draw(v)
    for r in range(40):
        dv.ellipse([-r * 6 + 10, -r * 9 + 20, W // 8 + r * 6 - 10, H // 8 + r * 9 - 20], outline=int(r * 3.2))
    v = v.filter(ImageFilter.GaussianBlur(6)).resize(im.size)
    im.paste(Image.new("RGBA", im.size, rgb(CREME_F)), (0, 0), v)
    return im

def texte(d, xy, txt, font, coul, a=1.0, ancre="mm"):
    if a <= 0: return
    d.text((S(xy[0]), S(xy[1])), txt, font=font, fill=rgb(coul, int(255 * a)), anchor=ancre)

def fleche(d, x, y, haut, coul, a, taille=46):
    s = taille; c = rgb(coul, int(255 * a))
    if haut: pts = [(x, y - s), (x - s * .8, y + s * .4), (x + s * .8, y + s * .4)]
    else: pts = [(x, y + s), (x - s * .8, y - s * .4), (x + s * .8, y - s * .4)]
    d.polygon([(S(a_), S(b_)) for a_, b_ in pts], fill=c)

def calque(): return Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))

# ---------- B2 : le cycle de pousse se raccourcit (voix 21,70 à 25,50) ----------
def ombre(im, boite, r):
    o = calque(); ImageDraw.Draw(o).rounded_rectangle([S(v) for v in boite], radius=S(r), fill=(60, 30, 20, 70))
    return Image.alpha_composite(im, o.filter(ImageFilter.GaussianBlur(S(18))))

def B2(t):
    im = ombre(fond(), (60, 985, 1020, 1095), 40); lay = calque(); d = ImageDraw.Draw(lay)
    texte(d, (540, 205), "Cycle de pousse", F("Fraunces-SemiBold.ttf", 104), TERRA, p(t, 0, .4))
    a_sous = p(t, 3.08, 3.4)
    texte(d, (540, 325), "DE PLUS EN PLUS COURT", F("SourceSans3-SemiBold.ttf", 64), PRUNE, a_sous)
    d.rounded_rectangle([S(60), S(975), S(1020), S(1085)], radius=S(40), fill=rgb(PEAU))
    d.rounded_rectangle([S(60), S(975), S(1020), S(1000)], radius=S(12), fill=rgb(PEAU_F))
    xs, Ls, bulbes, ep, durees = [230, 540, 850], [600, 390, 180], [46, 34, 22], [20, 14, 9], [250, 165, 80]
    fen = [(0.15, 1.15), (1.2, 2.2), (2.25, 3.05)]
    texte(d, (540, 1365), "TEMPS DE POUSSE", F("SourceSans3-SemiBold.ttf", 46), TERRA, p(t, .3, .6))
    for i in range(3):
        if t < fen[i][0]: continue
        g = p(t, *fen[i]); x = xs[i]; L = Ls[i] * g; b = bulbes[i]
        d.ellipse([S(x - b * .75), S(1035 - b * .65), S(x + b * .75), S(1035 + b * .95)], fill=rgb(CHEVEU))
        pts = [(x + 22 * math.sin(k / 12 * math.pi / 2) * (k / 12), 1035 - (L + 60) * k / 12) for k in range(13)]
        d.line([(S(a_), S(b_)) for a_, b_ in pts], fill=rgb(CHEVEU), width=S(ep[i]), joint="curve")
        w = durees[i] * g
        d.rounded_rectangle([S(x - w / 2), S(1420), S(x + w / 2), S(1452)], radius=S(16), fill=rgb(TERRA))
    if a_sous > 0:
        tips = [(xs[i] + 22, 1035 - Ls[i] - 60) for i in range(3)]
        d.line([(S(tips[0][0] + 30), S(tips[0][1])), (S(tips[2][0] + 10), S(tips[2][1] - 40))], fill=rgb(PRUNE, int(220 * a_sous)), width=S(8))
        fleche(d, tips[2][0] + 14, tips[2][1] - 22, False, PRUNE, a_sous, 34)
    return Image.alpha_composite(im, lay)

# ---------- B5a : les fluctuations hormonales touchent d'abord les tempes (voix 44,25 à 49,05) ----------
def courbe(x):
    amp = .25 + .75 * x
    return amp * (math.sin(x * 19) * .6 + math.sin(x * 41 + 1.3) * .3 + math.sin(x * 7.3) * .25)

def B5a(t):
    im = fond(); lay = calque(); d = ImageDraw.Draw(lay)
    texte(d, (540, 205), "Hormones", F("Fraunces-SemiBold.ttf", 104), TERRA, p(t, 0, .35))
    x0, x1, yc, A = 80, 1000, 560, 190
    a_g = 1 - p(t, 3.3, 3.6)
    if a_g > 0:
        d.line([(S(x0), S(yc + A + 50)), (S(x1), S(yc + A + 50))], fill=rgb(ENCRE, int(110 * a_g)), width=S(4))
        n = int(180 * p(t, .1, 3.2))
        if n > 1:
            pts = [(x0 + (x1 - x0) * k / 180, yc - A * courbe(k / 180)) for k in range(n + 1)]
            d.line([(S(a_), S(b_)) for a_, b_ in pts], fill=rgb(TERRA, int(255 * a_g)), width=S(13), joint="curve")
            hx, hy = pts[-1]; d.ellipse([S(hx - 16), S(hy - 16), S(hx + 16), S(hy + 16)], fill=rgb(TERRA_C, int(255 * a_g)))
        f = F("SourceSans3-SemiBold.ttf", 50)
        for (xa, xb, lab, tw) in [(x0, 590, "PÉRIMÉNOPAUSE", .49), (610, x1, "MÉNOPAUSE", 1.53)]:
            a = p(t, tw, tw + .3) * a_g
            if a > 0:
                y = yc + A + 95
                d.rounded_rectangle([S(xa), S(y - 6), S(xb), S(y + 6)], radius=S(6), fill=rgb(PRUNE, int(255 * a)))
                texte(d, ((xa + xb) / 2, y + 55), lab, f, PRUNE, a)
    im = Image.alpha_composite(im, lay)
    ah = p(t, 3.4, 3.8)
    if ah > 0:
        c = calque(); dc = ImageDraw.Draw(c); cx, cy = 540, 640; k = .9 + .1 * ah
        def E(x0_, y0_, x1_, y1_): return [S(cx + (x0_ - cx) * k), S(cy + (y0_ - cy) * k), S(cx + (x1_ - cx) * k), S(cy + (y1_ - cy) * k)]
        dc.rectangle(E(cx - 80, cy + 230, cx + 80, cy + 360), fill=rgb(PEAU, int(255 * ah)))
        dc.ellipse(E(cx - 320, cy + 330, cx + 320, cy + 560), fill=rgb(CREME_F, int(255 * ah)))
        dc.ellipse(E(cx - 200, cy - 250, cx + 200, cy + 250), fill=rgb(PEAU, int(255 * ah)), outline=rgb(PEAU_F, int(255 * ah)), width=S(6))
        dc.chord(E(cx - 215, cy - 270, cx + 215, cy + 110), 180, 360, fill=rgb(CHEVEU, int(240 * ah)))
        at = p(t, 4.3, 4.5)
        if at > 0:
            puls = .7 + .3 * math.sin((t - 4.3) * 14)
            halo = calque(); dh = ImageDraw.Draw(halo)
            for sx in (-1, 1):
                tx, ty = cx + sx * 185, cy - 50
                dh.ellipse([S(tx - 95), S(ty - 95), S(tx + 95), S(ty + 95)], fill=rgb(TERRA_C, int(220 * at * puls)))
            c = Image.alpha_composite(c, halo.filter(ImageFilter.GaussianBlur(S(24)))); dc = ImageDraw.Draw(c)
            for sx in (-1, 1):
                tx, ty = cx + sx * 185, cy - 50
                dc.ellipse([S(tx - 40), S(ty - 40), S(tx + 40), S(ty + 40)], fill=rgb(TERRA, int(255 * at)))
            texte(dc, (cx, 1000), "LES TEMPES D'ABORD", F("SourceSans3-SemiBold.ttf", 62), TERRA, at)
        im = Image.alpha_composite(im, c)
    return im

# ---------- B5b : œstrogène baisse, cortisol augmente (voix 49,05 à 52,00) ----------
def jauge(d, cx, haut, bas, niveau, coul, a, temps):
    w = 270
    d.rounded_rectangle([S(cx - w / 2), S(haut), S(cx + w / 2), S(bas)], radius=S(52), outline=rgb(ENCRE, int(90 + 110 * a)), width=S(6), fill=rgb("#FFFFFF", 170))
    y = bas - (bas - haut - 24) * niveau
    d.rounded_rectangle([S(cx - w / 2 + 16), S(y), S(cx + w / 2 - 16), S(bas - 16)], radius=S(38), fill=rgb(coul, int(140 + 115 * a)))
    for k in range(7):
        by = bas - 36 - ((temps * 110 + k * 61) % max(1, bas - 36 - y))
        bx = cx - 80 + (k * 41) % 160
        if by > y + 16: d.ellipse([S(bx - 9), S(by - 9), S(bx + 9), S(by + 9)], fill=rgb("#FFFFFF", 120))

def B5b(t):
    im = fond()
    for cx in (300, 780): im = ombre(im, (cx - 140, 390, cx + 140, 1085), 52)
    lay = calque(); d = ImageDraw.Draw(lay)
    haut, bas = 380, 1075
    ne = .84 - .66 * p(t, .89, 1.35); nc = .16 + .70 * p(t, 2.18, 2.6)
    ae, ac = p(t, .3, .6), p(t, 1.6, 1.9)
    f = F("Fraunces-SemiBold.ttf", 82)
    texte(d, (300, 270), "Œstrogène", f, TERRA, .3 + .7 * ae)
    texte(d, (780, 270), "Cortisol", f, PRUNE, .3 + .7 * ac)
    jauge(d, 300, haut, bas, ne, TERRA_C, ae, t)
    jauge(d, 780, haut, bas, nc, PRUNE, ac, t)
    fleche(d, 540, 640, False, TERRA, p(t, .89, 1.1), 62)
    fleche(d, 540, 860, True, PRUNE, p(t, 2.18, 2.4), 62)
    return Image.alpha_composite(im, lay)

SCENES = {"B2": (B2, 3.80), "B5a": (B5a, 4.80), "B5b": (B5b, 2.95)}
for nom in (sys.argv[1:] or SCENES):
    fn, dur = SCENES[nom]
    out = f"sorties/motion/{nom}-motion.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(round(dur * FPS))):
        fr = fn(i / FPS).convert("RGB").resize((W, H), Image.LANCZOS)
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait(); print("écrit :", out)
