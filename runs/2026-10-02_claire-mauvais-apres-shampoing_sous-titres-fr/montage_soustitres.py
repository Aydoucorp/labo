# montage_soustitres.py
# Montage leger sur une video TikTok existante :
#  1. remplace ses sous-titres anglais incrustes par des bandeaux opaques avec le texte FR
#     (memes positions, memes timings, typo TikTok Sans) ;
#  2. coupe son CTA final : gel image sur la derniere image sans CTA (25,40 s), leger zoom ;
#  3. ajoute un motion CTA Claire « Commente GUIDE » sur le dernier plan floute ;
#  4. prolonge la musique d'origine par un raccord sur une mesure plus tot (21,55 s).
# Usage : python3 montage_soustitres.py [--frames t1,t2,...]  (sans option : rendu complet)

import math, subprocess, sys, json
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original_trendtrack_7689539918963510559.mp4"
FONTS = RUN / "work/fonts"
OUT = RUN / "sorties"
W, H, FPS = 1080, 1920, 30
K = W / 720  # facteur d'echelle depuis la source 720x1280

# ---- reglages ----
FREEZE_T = 25.40      # derniere image sans son CTA (frame 762)
MOTION_T = 26.60      # debut du flou + motion
CARD_T = 26.85        # apparition de la carte CTA
END_T = 30.00
AUDIO_LOOP_FROM = 21.55  # raccord musical trouve par similarite spectrale
SFX = Path("/home/user/labo/skills/creation-full-b-roll-artiste/assets/sfx")

# Sous-titres : (debut, fin, texte FR, boite de ses sous-titres en px source x0,y0,x1,y1)
CAPS = [
    (0.000, 9.200, "voici les signes que vous utilisez le mauvais après-shampoing...", (146, 249, 572, 324)),
    (9.200, 10.833, "vos cheveux ont l'air secs et abîmés...", (84, 290, 633, 327)),
    (10.833, 12.967, "vos doigts s'accrochent dans les nœuds pendant le séchage...", (116, 270, 602, 346)),
    (12.967, 14.900, "il devient difficile de séparer vos mèches sous la douche, même avec le produit...", (108, 249, 610, 368)),
    (14.900, 16.867, "vous trouvez de petits nœuds persistants après le brushing...", (108, 274, 608, 351)),
    (16.867, 18.800, "le brossage est laborieux...", (101, 260, 607, 338)),
    (18.800, 20.900, "vos longueurs semblent sèches, raides ou cassantes...", (54, 297, 664, 335)),
    (20.900, 22.467, "des nœuds se reforment aussitôt après le passage de la brosse...", (79, 278, 638, 355)),
    (22.467, 24.700, "vos cheveux peuvent aussi paraître lourds, plats et gras aux racines...", (101, 278, 622, 355)),
    (24.700, CARD_T, "le bon après-shampoing ou masque capillaire peut réparer tout cela...", (63, 297, 648, 375)),
]

CREME, CREME_F, TERRA, TERRA_C, PRUNE, ENCRE = "#FAF6F3", "#EFE7E0", "#A8553A", "#C9805F", "#7A4351", "#2E2A26"

def font(w, size):
    return ImageFont.truetype(str(FONTS / f"TikTokSans-{w}.ttf"), size)

def wrap(draw, text, f, maxw):
    """Coupe en un minimum de lignes, puis equilibre leurs largeurs."""
    words = text.split()
    tl = lambda ws: draw.textlength(" ".join(ws), font=f)
    def splits(ws, n):
        if n == 1:
            yield [ws]; return
        for i in range(1, len(ws) - n + 2):
            for rest in splits(ws[i:], n - 1):
                yield [ws[:i]] + rest
    for n in range(1, len(words) + 1):
        best = None
        for c in splits(words, n):
            m = max(tl(l) for l in c)
            if m <= maxw and (best is None or m < best[0]):
                best = (m, c)
        if best:
            return [" ".join(l) for l in best[1]]
    return [text]

def caption_layer(text, box):
    """Bandeau opaque noir arrondi + texte blanc, couvrant ses sous-titres."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(600, 60)
    lines = wrap(d, text, f, 860)
    lh = 72
    tw = max(d.textlength(l, font=f) for l in lines)
    th = lh * len(lines)
    x0, y0, x1, y1 = [v * K for v in box]
    cy = (y0 + y1) / 2
    bw = max(tw + 64, (x1 - x0) + 40)
    bh = max(th + 36, (y1 - y0) + 34)
    bx0, by0 = W / 2 - bw / 2, cy - bh / 2
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=26, fill=(0, 0, 0, 255))
    ty = cy - th / 2
    for l in lines:
        lw = d.textlength(l, font=f)
        d.text((W / 2 - lw / 2, ty + lh / 2), l, font=f, fill="white", anchor="lm")
        ty += lh
    return img

# ---- motion CTA ----
def ease_out_back(t, s=1.7):
    t = min(max(t, 0), 1) - 1
    return t * t * ((s + 1) * t + s) + 1

def ease(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t) ** 3

def paste_scaled(base, layer, scale, center, alpha=1.0):
    if scale <= 0.01 or alpha <= 0:
        return
    w, h = layer.size
    l = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    if alpha < 1:
        a = l.getchannel("A").point(lambda v: int(v * alpha)); l.putalpha(a)
    base.alpha_composite(l, (int(center[0] - l.width / 2), int(center[1] - l.height / 2)))

def make_card():
    cw, ch = 860, 560
    card = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, cw + 20, ch + 30], radius=48, fill=(0, 0, 0, 110))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([20, 20, cw + 20, ch + 20], radius=48, fill=CREME)
    f1 = font(700, 66)
    d.text((cw / 2 + 20, 120), "Commente", font=f1, fill=ENCRE, anchor="mm")
    f3 = font(600, 50)
    for i, l in enumerate(["pour savoir quel", "après-shampoing choisir"]):
        d.text((cw / 2 + 20, 430 + i * 64), l, font=f3, fill=ENCRE, anchor="mm")
    return card

def make_pill():
    f = font(700, 128)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    tw = tmp.textlength("GUIDE", font=f) + 4 * 14
    pw, ph = int(tw + 110), 190
    pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    d.rounded_rectangle([0, 0, pw, ph], radius=ph // 2, fill=TERRA)
    x = 55
    for c in "GUIDE":
        d.text((x, ph / 2 + 4), c, font=f, fill=CREME, anchor="lm")
        x += d.textlength(c, font=f) + 14
    return pill

def make_bar(typed, cursor_on):
    bw, bh = 760, 120
    bar = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar)
    d.rounded_rectangle([0, 0, bw, bh], radius=60, fill=CREME_F, outline=TERRA_C, width=4)
    f = font(600, 54)
    if typed:
        d.text((48, bh / 2), typed, font=f, fill=ENCRE, anchor="lm")
        cx = 48 + d.textlength(typed, font=f) + 6
    else:
        d.text((48, bh / 2), "Ajouter un commentaire...", font=font(500, 46), fill="#9A918A", anchor="lm")
        cx = 46
    if cursor_on:
        d.rectangle([cx, bh / 2 - 30, cx + 5, bh / 2 + 30], fill=TERRA)
    # bouton envoyer
    d.ellipse([bw - 104, 14, bw - 14, bh - 14], fill=TERRA if typed == "GUIDE" else TERRA_C)
    ax, ay = bw - 59, bh / 2
    d.polygon([(ax - 18, ay - 22), (ax + 24, ay), (ax - 18, ay + 22), (ax - 8, ay)], fill=CREME)
    return bar

CARD, PILL = make_card(), make_pill()
CARD_C = (510, 860)

def motion_layer(t):
    """t = secondes depuis CARD_T."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t < 0:
        return img
    s = ease_out_back(t / 0.45) if t < 0.45 else 1.0
    paste_scaled(img, CARD, 0.6 + 0.4 * s, CARD_C, alpha=ease(t / 0.2))
    # pastille GUIDE : pop puis pulsation
    tp = t - 0.30
    if tp > 0:
        ps = ease_out_back(tp / 0.4, 2.4) if tp < 0.4 else 1.0
        pulse = 1 + 0.06 * math.sin(max(0, t - 2.2) * math.pi / 0.35) if 2.2 < t < 2.55 else 1
        paste_scaled(img, PILL, ps * pulse, (CARD_C[0], CARD_C[1] - 10))
    # barre de commentaire qui tape GUIDE
    tb = t - 0.9
    if tb > 0:
        n = int(max(0, tb - 0.35) / 0.11)
        typed = "GUIDE"[:min(5, n)]
        cur = int(t * 3.2) % 2 == 0
        y = CARD_C[1] + 420 + 40 * (1 - ease(tb / 0.35))
        paste_scaled(img, make_bar(typed, cur), 1.0, (CARD_C[0], y), alpha=ease(tb / 0.3))
    # fleche vers l'icone commentaires (rail de droite)
    ta = t - 1.6
    if ta > 0:
        d = ImageDraw.Draw(img)
        bob = 14 * abs(math.sin(ta * math.pi / 0.5)) if ta < 2.0 else 0
        a = ease(ta / 0.25)
        col = (168, 85, 58, int(255 * a))
        pts =[(810 + 120 * u, 1180 + 70 * u - 60 * math.sin(u * math.pi) - bob) for u in np.linspace(0, 1, 20)]
        d.line(pts, fill=col, width=14, joint="curve")
        ex, ey = pts[-1]
        d.polygon([(ex + 2, ey + 34), (ex - 26, ey - 8), (ex + 28, ey - 10)], fill=col)
    return img

# ---- rendu ----
def read_frames():
    cap = cv2.VideoCapture(str(SRC))
    fr = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        fr.append(f)
    return fr

CAP_LAYERS = {}

def compose(frames, t):
    if t < FREEZE_T:
        idx = min(int(round(t * FPS)), len(frames) - 1)
        zoom = 1.0
    else:
        idx = int(round(FREEZE_T * FPS)) - 1
        zoom = 1.0 + 0.012 * (t - FREEZE_T)  # leger zoom continu sur le gel
    f = cv2.cvtColor(frames[idx], cv2.COLOR_BGR2RGB)
    f = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)
    if zoom > 1:
        cw, ch = int(W / zoom), int(H / zoom)
        x0, y0 = (W - cw) // 2, int((H - ch) * 0.45)
        f = cv2.resize(f[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_CUBIC)
    if t >= MOTION_T:
        a = ease((t - MOTION_T) / 0.4)
        sig = 1 + 26 * a
        f = cv2.GaussianBlur(f, (0, 0), sig)
        f = (f.astype(np.float32) * (1 - 0.32 * a)).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(f).convert("RGBA")
    for i, (a0, a1, txt, box) in enumerate(CAPS):
        if a0 <= t < a1:
            if i not in CAP_LAYERS:
                CAP_LAYERS[i] = caption_layer(txt, box)
            img.alpha_composite(CAP_LAYERS[i])
    if t >= CARD_T:
        img.alpha_composite(motion_layer(t - CARD_T))
    return img.convert("RGB")

def build_audio(out_wav):
    xf = 0.15
    cut = 26.40
    tail = END_T - cut + xf
    fc = (f"[0:a]atrim=0:{cut},asetpts=PTS-STARTPTS[a];"
          f"[1:a]atrim=0:{tail},asetpts=PTS-STARTPTS[b];"
          f"[a][b]acrossfade=d={xf}[m];"
          f"[m]afade=t=out:st={END_T - 0.8}:d=0.8,atrim=0:{END_T}[mus];"
          f"[2:a]adelay={int(CARD_T*1000)}|{int(CARD_T*1000)},volume=0.55[s1];"
          f"[3:a]adelay={int((CARD_T+0.3)*1000)}|{int((CARD_T+0.3)*1000)},volume=0.6[s2];"
          f"[mus][s1][s2]amix=inputs=3:normalize=0:duration=first[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC),
                    "-ss", str(AUDIO_LOOP_FROM - xf), "-i", str(SRC),
                    "-i", str(SFX / "whoosh_soft.wav"), "-i", str(SFX / "tick_soft.wav"),
                    "-filter_complex", fc, "-map", "[out]",
                    "-ar", "44100", "-ac", "2", str(out_wav)], check=True)

def main():
    frames = read_frames()
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for ts in sys.argv[2].split(","):
            compose(frames, float(ts)).save(OUT / f"controle_{float(ts):05.2f}s.jpg", quality=88)
        return
    wav = RUN / "work/audio_final.wav"
    build_audio(wav)
    out = OUT / "claire-mauvais-apres-shampoing-fr_v1.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
                          "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
                         stdin=subprocess.PIPE)
    for n in range(int(END_T * FPS)):
        p.stdin.write(compose(frames, n / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out)

if __name__ == "__main__":
    main()
