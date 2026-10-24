# Motion design B6 aux couleurs de Claire (voix 44,30 à 49,60) : visage moins lifté, ligne frontale fragile, coiffage compliqué.
# Usage : python3 work/motion_b6.py [--image t] ; rendu 1080x1920, 30 i/s, suréchantillonné x2 ; bande des sous-titres (1150 à 1290 px) laissée calme.
import sys, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS, SS = 1080, 1920, 30, 2
DUREE = 5.30
FD = "/home/user/labo/runs/2026-10-08_claire-menopause-affinement_talking-head/montage/fonts_charte/"
TERRA, TERRA_C, PRUNE, CREME, CREME_F, ENCRE = "#A8553A", "#C9805F", "#7A4351", "#FAF6F3", "#EFE7E0", "#2E2A26"
PEAU, PEAU_F, CHEVEU, CHEVEU_C = "#F3CDB6", "#E4A98C", "#3B2A22", "#5A4234"
def F(nom, t): return ImageFont.truetype(FD + nom, int(t * SS))
def rgb(h, a=255): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (max(0, min(255, int(a))),)
def cl(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = cl(x); return x * x * (3 - 2 * x)
def p(t, a, b): return ease((t - a) / (b - a)) if b > a else float(t >= a)
def S(v): return int(round(v * SS))
def calque(): return Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))

def fond():
    im = Image.new("RGBA", (W * SS, H * SS), rgb(CREME))
    v = Image.new("L", (W // 8, H // 8), 0); dv = ImageDraw.Draw(v)
    for r in range(40):
        dv.ellipse([-r * 6 + 10, -r * 9 + 20, W // 8 + r * 6 - 10, H // 8 + r * 9 - 20], outline=int(r * 3.2))
    v = v.filter(ImageFilter.GaussianBlur(6)).resize(im.size)
    im.paste(Image.new("RGBA", im.size, rgb(CREME_F)), (0, 0), v)
    return im
FOND = fond()

# ---------- caméra : zoom sur la ligne frontale pendant la 2e phrase ----------
CX, CY = 540, 790                       # centre du visage (coordonnées dessin)
def camera(t):
    z_in, z_out = p(t, 1.70, 2.25), p(t, 3.45, 3.95)
    a = z_in * (1 - z_out) + .45 * z_out  # 1re phrase : plan large ; 2e : gros plan ; 3e : plan moyen
    k = 1.12 + .75 * a
    fx, fy = CX, CY + (585 - CY) * a      # point visé : la ligne frontale
    sx, sy = CX, CY + (735 - CY) * a
    return k, fx, fy, sx, sy

class Vue:
    def __init__(s, t): s.k, s.fx, s.fy, s.sx, s.sy = camera(t)
    def P(s, x, y): return (S(s.sx + (x - s.fx) * s.k), S(s.sy + (y - s.fy) * s.k))
    def L(s, v): return max(1, S(v * s.k))
    def boite(s, x0, y0, x1, y1): a, b = s.P(x0, y0); c, d = s.P(x1, y1); return [a, b, c, d]

# ---------- ligne frontale, avec recul des tempes r (0 à 1) ----------
def ligne_frontale(u, r):
    y = CY - 225 + 140 * u * u
    y -= r * 62 * math.exp(-((abs(u) - .80) / .17) ** 2)
    x = CX + 190 * u - r * 10 * math.copysign(1, u) * math.exp(-((abs(u) - .85) / .2) ** 2)
    return x, y

def tete(d, v, t, r, sourire):
    # cheveux longs derrière (attachés bas, comme l'avatar)
    d.rounded_rectangle(v.boite(CX - 238, 610, CX + 238, 1105), radius=v.L(150), fill=rgb(CHEVEU))
    # cou et épaules (pull terracotta de l'avatar)
    d.rectangle(v.boite(CX - 70, 960, CX + 70, 1080), fill=rgb(PEAU_F))
    d.ellipse(v.boite(CX - 330, 1050, CX + 330, 1330), fill=rgb(TERRA_C))
    d.chord(v.boite(CX - 95, 1010, CX + 95, 1100), 0, 180, fill=rgb(PEAU_F))
    # visage
    d.ellipse(v.boite(CX - 182, 560, CX + 182, 1035), fill=rgb(PEAU))
    d.ellipse(v.boite(CX - 196, 520, CX + 196, 900), fill=rgb(PEAU))  # front : la peau apparaît quand les tempes reculent
    # joues : remontées au départ, elles descendent quand le visage perd son « lift »
    dj = 26 * p(t, 1.05, 1.55)
    for sx in (-1, 1):
        jx, jy = CX + sx * 105, 870 + dj
        d.ellipse(v.boite(jx - 48, jy - 26, jx + 48, jy + 26), fill=rgb(PEAU_F, 110))
    # sourcils, nez, bouche (le coin de la bouche retombe avec le visage)
    for sx in (-1, 1):
        pts = [(CX + sx * (45 + 75 * i / 8), 760 - 16 * math.sin(math.pi * i / 8) + 6 * dj / 26 * (i / 8)) for i in range(9)]
        d.line([v.P(*q) for q in pts], fill=rgb(CHEVEU_C, 230), width=v.L(9), joint="curve")
        ex, ey = CX + sx * 85, 815
        d.arc(v.boite(ex - 30, ey - 14, ex + 30, ey + 14), 200, 340, fill=rgb(ENCRE, 200), width=v.L(6))
    d.line([v.P(CX - 4, 820), v.P(CX - 14, 890), v.P(CX + 8, 900)], fill=rgb(PEAU_F), width=v.L(6), joint="curve")
    pts = [(CX - 52 + 104 * i / 10, 955 + sourire * 16 * math.sin(math.pi * i / 10) - (1 - sourire) * 5 * math.sin(math.pi * i / 10)) for i in range(11)]
    d.line([v.P(*q) for q in pts], fill=rgb("#B5604A"), width=v.L(8), joint="curve")
    # masse de cheveux du dessus, découpée par la ligne frontale
    haut = [ligne_frontale(-1 + 2 * i / 60, r) for i in range(61)]
    crane = [(CX + 222 * math.cos(a), 760 - 270 * math.sin(a)) for a in [math.pi * i / 60 for i in range(61)]]
    d.polygon([v.P(*q) for q in haut + crane], fill=rgb(CHEVEU))

def duvet(d, v, t, r, densite):
    # petits cheveux fins le long de la ligne frontale aux tempes
    for i in range(46):
        u = -1 + 2 * (i + .5) / 46
        if abs(u) < .45: continue
        tempe = math.exp(-((abs(u) - .82) / .2) ** 2)
        if (i * 37 % 100) / 100 > densite + (1 - tempe) * (1 - densite): continue
        x, y = ligne_frontale(u, r)
        long = 22 + 10 * ((i * 53) % 7) / 7
        ox = math.copysign(1, u) * (4 + 6 * tempe)
        d.line([v.P(x, y - 6), v.P(x + ox, y + long * (1 - .35 * tempe))], fill=rgb(CHEVEU, 255 - 90 * tempe * (1 - densite)), width=v.L(2.6 - 1.2 * tempe * (1 - densite)))

def fleche(d, v, x0, y0, x1, y1, coul, a, w=10):
    if a <= 0: return
    c = rgb(coul, 255 * a)
    d.line([v.P(x0, y0), v.P(x1, y1)], fill=c, width=v.L(w))
    ang = math.atan2(y1 - y0, x1 - x0); s = 26
    pts = [(x1 + s * math.cos(ang), y1 + s * math.sin(ang)),
           (x1 + s * .8 * math.cos(ang + 2.3), y1 + s * .8 * math.sin(ang + 2.3)),
           (x1 + s * .8 * math.cos(ang - 2.3), y1 + s * .8 * math.sin(ang - 2.3))]
    d.polygon([v.P(*q) for q in pts], fill=c)

def meche(d, v, x, y, ang, long, a=1., w=4.5):
    # mèche fine : ang = 0 pend vers le bas, positif = relevée vers l'extérieur droit
    pts = []
    for j in range(9):
        s = j / 8; aa = ang * (1 - .25 * s)
        pts.append((x + math.sin(aa) * long * s + 6 * s * s, y + math.cos(aa) * long * s))
    d.line([v.P(*q) for q in pts], fill=rgb(CHEVEU, 255 * a), width=v.L(w), joint="curve")

def peigne_x(t):
    # aller sur « coiffer », retour sur « compliqué »
    if t < 3.70: return None
    if t < 4.45: return 880 - 680 * ease((t - 3.70) / .75)
    if t < 4.62: return 200
    if t < 5.25: return 200 + 680 * ease((t - 4.62) / .63)
    return None

def peigne(d, v, x, y):
    d.rounded_rectangle(v.boite(x - 110, y - 46, x + 110, y - 8), radius=v.L(14), fill=rgb(PRUNE))
    for i in range(16):
        tx = x - 100 + 200 * i / 15
        d.line([v.P(tx, y - 10), v.P(tx, y + 34)], fill=rgb(PRUNE), width=v.L(6))

def angle_meche(t, mx, sens):
    # la mèche se relève quand le peigne passe, puis retombe en oscillant
    ang = 0.
    for (t0, t1, x0, x1) in [(3.70, 4.45, 880, 200), (4.62, 5.25, 200, 880)]:
        if t < t0: continue
        tp = t0 + (t1 - t0) * cl((mx - x0) / (x1 - x0))  # instant où le peigne passe la mèche
        dt = t - tp
        if dt < 0: continue
        if dt < .12: ang = max(ang, 1.9 * dt / .12)
        else: ang = max(ang, 1.9 * math.exp(-(dt - .12) * 5.5) * math.cos((dt - .12) * 13))
    return ang * sens

def texte(d, xy, txt, font, coul, a):
    if a > 0: d.text((S(xy[0]), S(xy[1])), txt, font=font, fill=rgb(coul, 255 * a), anchor="mm")

TITRES = [  # (début, fin, titre, sous-titre, apparition du sous-titre)
    (0.00, 1.72, "Ton visage", "MOINS LIFTÉ", 1.12),
    (1.72, 3.50, "Ligne frontale", "FRAGILE", 2.69),
    (3.50, 9.00, "Te coiffer", "PLUS COMPLIQUÉ", 4.68),
]

def image(t):
    v = Vue(t)
    r = .25 + .75 * p(t, .55, 1.50) + .35 * p(t, 2.69, 3.10)  # les tempes reculent sur « moins lifté », puis encore sur « fragile »
    sourire = 1 - p(t, 1.05, 1.50)
    densite = 1 - .78 * p(t, 2.69, 3.10)    # le duvet des tempes se clairsème sur « fragile »
    lay = calque(); d = ImageDraw.Draw(lay)
    tete(d, v, t, r, sourire)
    duvet(d, v, t, r, densite)
    # 1re phrase : flèches « lift » qui s'inversent
    a_up, a_dn = p(t, .05, .35) * (1 - p(t, 1.0, 1.2)), p(t, 1.12, 1.35) * (1 - p(t, 1.65, 1.9))
    for sx in (-1, 1):
        fleche(d, v, CX + sx * 235, 900, CX + sx * 270, 780, TERRA, a_up)
        fleche(d, v, CX + sx * 270, 790, CX + sx * 245, 905, PRUNE, a_dn)
    # 2e phrase : la ligne frontale est tracée en pointillés terracotta, puis s'effrite aux tempes
    a_l = p(t, 1.95, 2.15) * (1 - p(t, 3.40, 3.65))
    if a_l > 0:
        n = int(60 * p(t, 1.95, 2.60))
        for i in range(0, n, 2):
            u0, u1 = -1 + 2 * i / 60, -1 + 2 * (i + 1) / 60
            tempe = math.exp(-((abs(u0) - .82) / .2) ** 2)
            casse = p(t, 2.69, 3.0) * tempe
            if casse > .5 and i % 4 == 0: continue
            q0, q1 = ligne_frontale(u0, r), ligne_frontale(u1, r)
            coul = TERRA if casse < .3 else PRUNE
            d.line([v.P(q0[0], q0[1] - 14), v.P(q1[0], q1[1] - 14)], fill=rgb(coul, 255 * a_l), width=v.L(7 - 3 * casse))
        # petits cheveux qui se détachent et tombent
        for j, (u, td) in enumerate([(-.86, 2.72), (.80, 2.80), (-.74, 2.95), (.90, 3.02)]):
            if t < td: continue
            x, y = ligne_frontale(u, r); dt = t - td
            a = 1 - p(dt, .35, .55)
            meche(d, v, x + math.copysign(18, u) * dt, y + 260 * dt * dt + 20 * dt, .6 * math.sin(dt * 9 + j), 26, a, 2.6)
    # 3e phrase : le peigne passe, les mèches des tempes se relèvent puis retombent
    a3 = p(t, 3.55, 3.80)
    if a3 > 0:
        for u in (-.95, -.88, -.80, .80, .88, .95):
            x, y = ligne_frontale(u, r)
            ang = angle_meche(t, x, -1 if u < 0 else 1)
            meche(d, v, x, y + 4, -ang if u < 0 else ang, 120, a3, 4)
        px = peigne_x(t)
        if px is not None: peigne(d, v, px, ligne_frontale(cl((px - CX) / 190, -1, 1), r)[1] + 18)
        a_q = p(t, 4.70, 4.90)
        if a_q > 0:  # traits d'agacement façon BD
            for sx in (-1, 1):
                bx, by = CX + sx * 300, 600
                for k in range(3):
                    ang = math.radians(-90 + sx * (25 + 30 * k))
                    d.line([v.P(bx + 18 * math.cos(ang), by + 18 * math.sin(ang)), v.P(bx + 58 * math.cos(ang), by + 58 * math.sin(ang))], fill=rgb(TERRA, 255 * a_q), width=v.L(8))
    im = Image.alpha_composite(FOND, lay)
    # titres (fixes à l'écran, hors zoom)
    tl = calque(); dt_ = ImageDraw.Draw(tl)
    for (t0, t1, tit, sous, ts) in TITRES:
        a = p(t, t0, t0 + .25) * (1 - p(t, t1 - .12, t1 + .1))
        if a <= 0: continue
        bande = calque(); db = ImageDraw.Draw(bande)
        db.rounded_rectangle([S(150), S(140), S(930), S(385)], radius=S(46), fill=rgb(CREME, 215 * a))
        im = Image.alpha_composite(im, bande)
        texte(dt_, (540, 220), tit, F("Fraunces-SemiBold.ttf", 98), TERRA, a)
        texte(dt_, (540, 320), sous, F("SourceSans3-SemiBold.ttf", 64), PRUNE, a * p(t, ts, ts + .2))
    return Image.alpha_composite(im, tl)

if __name__ == "__main__":
    os.makedirs("sorties/motion", exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[1] == "--image":
        for tt in sys.argv[2:]:
            image(float(tt)).convert("RGB").resize((W, H), Image.LANCZOS).save(f"work/b6-motion-{tt}.jpg", quality=88)
        sys.exit()
    out = "sorties/motion/B6-motion-v1.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(round(DUREE * FPS))):
        pr.stdin.write(image(i / FPS).convert("RGB").resize((W, H), Image.LANCZOS).tobytes())
    pr.stdin.close(); pr.wait(); print("écrit :", out)
