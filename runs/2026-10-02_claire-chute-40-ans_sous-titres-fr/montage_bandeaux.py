# montage_bandeaux.py
# Version avec bandeaux (v2, demande utilisateur) de la vidéo avant/après chute de cheveux à 40 ans :
#  1. part de la vidéo d'origine (ses textes anglais sont cachés par des bandeaux opaques, plus d'effacement IA) ;
#  2. bandeaux comme la créa full-b-roll-artiste 002 : hook en rouge (texte blanc), « Jour X » en terracotta
#     (texte crème), chaque bandeau couvre la boîte de son texte anglais + marge, ombre et contour compris ;
#  3. coupe avant l'apparition du produit : gel sur l'image 351 (11,70 s), léger zoom ;
#  4. motion CTA Claire « Commente GUIDE » sur le dernier plan flouté ;
#  5. son d'origine supprimé, remplacé par la musique fournie (source/musique_gabrielaabm.mp3) dès 0 s.
# Usage : python3 montage_bandeaux.py [--frames t1,t2,...]  (sans option : rendu complet)

import math, subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original_pure-batana76.mp4"
MUSIQUE = RUN / "source/musique_gabrielaabm.mp3"
FONTS = RUN / "work/fonts"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
OUT = RUN / "sorties"
W, H, FPS = 1080, 1920, 30
VERSION = "v2"

# ---- réglages ----
FREEZE_T = 11.70      # dernière image sans le flacon (image 351)
MOTION_T = 12.40      # début du flou + motion
CARD_T = 12.65        # apparition de la carte CTA
END_T = 15.80
SFX = Path("/home/user/labo/skills/creation-full-b-roll-artiste/assets/sfx")

# Bandeaux : (début, fin, lignes, couleur, encre, boîte de son texte en px source 720x1280 x0,y0,x1,y1).
# Les plages couvrent aussi les fondus (son texte s'estompe avec l'image) : changement au creux du noir (3,00 s et 5,60 s)
# et au milieu du fondu enchaîné 90 -> 180 (9,17 s). Toutes les boîtes « Jour » ont la même taille (celle de « Day 180 😍 »).
BOITE_JOUR = (221, 136, 499, 209)
TEXTES = [
    (0.000, 3.000, ["La chute de cheveux", "à 40 ans, c'est terrifiant 😢💔"], "#E0202A", "white", (65, 206, 699, 333)),
    (0.400, 3.000, ["Jour 1"], "#A8553A", "#FAF6F3", BOITE_JOUR),
    (3.000, 5.600, ["Jour 14"], "#A8553A", "#FAF6F3", BOITE_JOUR),
    (5.600, 9.170, ["Jour 90"], "#A8553A", "#FAF6F3", BOITE_JOUR),
    (9.170, None, ["Jour 180 😍"], "#A8553A", "#FAF6F3", BOITE_JOUR),
]
K = W / 720

CREME, CREME_F, TERRA, TERRA_C, ENCRE = "#FAF6F3", "#EFE7E0", "#A8553A", "#C9805F", "#2E2A26"
CTA_LIGNES = ["pour recevoir", "la solution"]

def font(w, size):
    return ImageFont.truetype(str(FONTS / f"TikTokSans-{w}.ttf"), size)

EMOJI = ImageFont.truetype(EMOJI_FONT, 109)
TXT = font(600, 60)
LH = 72
ESZ = 62

def is_emoji(c):
    return ord(c) > 0x2500

def segments(text):
    parts, cur = [], ""
    for c in text:
        if is_emoji(c):
            if cur:
                parts.append(("t", cur)); cur = ""
            parts.append(("e", c))
        else:
            cur += c
    if cur:
        parts.append(("t", cur))
    return parts

def line_width(d, text):
    return sum(d.textlength(s, font=TXT) if k == "t" else ESZ + 6 for k, s in segments(text))

def draw_line(img, text, cy, ink):
    d = ImageDraw.Draw(img)
    x = W / 2 - line_width(d, text) / 2
    for k, s in segments(text):
        if k == "t":
            d.text((x, cy), s, font=TXT, fill=ink, anchor="lm")
            x += d.textlength(s, font=TXT)
        else:
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            ImageDraw.Draw(e).text((6, 6), s, font=EMOJI, embedded_color=True)
            bb = e.getbbox()
            if bb:
                img.alpha_composite(e.crop(bb).resize((ESZ, ESZ), Image.LANCZOS), (int(x + 3), int(cy - ESZ / 2)))
            x += ESZ + 6

LAYERS = {}

def text_layer(i):
    """Bandeau opaque arrondi couvrant son texte (contour et ombre compris), texte FR centré dedans."""
    if i not in LAYERS:
        _, _, lignes, fill, ink, box = TEXTES[i]
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        tw = max(line_width(d, l) for l in lignes)
        th = LH * len(lignes)
        x0, y0, x1, y1 = [v * K for v in box]
        cy = (y0 + y1) / 2
        bw = min(W - 24, max(tw + 64, (x1 - x0) + 40))
        bh = max(th + 36, (y1 - y0) + 34)
        d.rounded_rectangle([W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2], radius=26, fill=fill)
        ty = cy - th / 2 + LH / 2
        for l in lignes:
            draw_line(img, l, ty, ink)
            ty += LH
        LAYERS[i] = img
    return LAYERS[i]

# ---- motion CTA (même carte que la créa full-b-roll-artiste 002) ----
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
        l.putalpha(l.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(l, (int(center[0] - l.width / 2), int(center[1] - l.height / 2)))

def make_card():
    cw, ch = 860, 560
    card = Image.new("RGBA", (cw + 40, ch + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, cw + 20, ch + 30], radius=48, fill=(0, 0, 0, 110))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([20, 20, cw + 20, ch + 20], radius=48, fill=CREME)
    d.text((cw / 2 + 20, 120), "Commente", font=font(700, 66), fill=ENCRE, anchor="mm")
    for i, l in enumerate(CTA_LIGNES):
        d.text((cw / 2 + 20, 430 + i * 64), l, font=font(600, 50), fill=ENCRE, anchor="mm")
    return card

def make_pill():
    f = font(700, 128)
    tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength("GUIDE", font=f) + 4 * 14
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
    if typed:
        d.text((48, bh / 2), typed, font=font(600, 54), fill=ENCRE, anchor="lm")
        cx = 48 + d.textlength(typed, font=font(600, 54)) + 6
    else:
        d.text((48, bh / 2), "Ajouter un commentaire...", font=font(500, 46), fill="#9A918A", anchor="lm")
        cx = 46
    if cursor_on:
        d.rectangle([cx, bh / 2 - 30, cx + 5, bh / 2 + 30], fill=TERRA)
    d.ellipse([bw - 104, 14, bw - 14, bh - 14], fill=TERRA if typed == "GUIDE" else TERRA_C)
    ax, ay = bw - 59, bh / 2
    d.polygon([(ax - 18, ay - 22), (ax + 24, ay), (ax - 18, ay + 22), (ax - 8, ay)], fill=CREME)
    return bar

CARD, PILL = make_card(), make_pill()
CARD_C = (510, 860)

def motion_layer(t):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t < 0:
        return img
    s = ease_out_back(t / 0.45) if t < 0.45 else 1.0
    paste_scaled(img, CARD, 0.6 + 0.4 * s, CARD_C, alpha=ease(t / 0.2))
    tp = t - 0.30
    if tp > 0:
        ps = ease_out_back(tp / 0.4, 2.4) if tp < 0.4 else 1.0
        pulse = 1 + 0.06 * math.sin((t - 2.2) * math.pi / 0.35) if 2.2 < t < 2.55 else 1
        paste_scaled(img, PILL, ps * pulse, (CARD_C[0], CARD_C[1] - 10))
    tb = t - 0.9
    if tb > 0:
        n = int(max(0, tb - 0.35) / 0.11)
        y = CARD_C[1] + 420 + 40 * (1 - ease(tb / 0.35))
        paste_scaled(img, make_bar("GUIDE"[:min(5, n)], int(t * 3.2) % 2 == 0), 1.0, (CARD_C[0], y), alpha=ease(tb / 0.3))
    ta = t - 1.6
    if ta > 0:
        d = ImageDraw.Draw(img)
        bob = 14 * abs(math.sin(ta * math.pi / 0.5)) if ta < 2.0 else 0
        col = (168, 85, 58, int(255 * ease(ta / 0.25)))
        pts = [(905 + 75 * u + 40 * math.sin(u * math.pi), 1105 + 120 * u - bob) for u in np.linspace(0, 1, 24)]
        d.line(pts, fill=col, width=14, joint="curve")
        ex, ey = pts[-1]
        d.polygon([(ex + 2, ey + 34), (ex - 26, ey - 8), (ex + 28, ey - 10)], fill=col)
    return img

# ---- rendu ----
def read_frames():
    cap = cv2.VideoCapture(str(SRC)); fr = []
    while len(fr) < round(FREEZE_T * FPS) + 1:  # images 0 a 351, avant le flacon
        ok, f = cap.read()
        if not ok:
            break
        fr.append(f)
    return fr

def compose(frames, t):
    if t < FREEZE_T:
        idx, zoom = min(int(round(t * FPS)), len(frames) - 1), 1.0
    else:
        idx, zoom = len(frames) - 1, 1.0 + 0.012 * (t - FREEZE_T)
    f = cv2.resize(cv2.cvtColor(frames[idx], cv2.COLOR_BGR2RGB), (W, H), interpolation=cv2.INTER_LANCZOS4)
    if zoom > 1:
        cw, ch = int(W / zoom), int(H / zoom)
        x0, y0 = (W - cw) // 2, int((H - ch) * 0.45)
        f = cv2.resize(f[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_CUBIC)
    if t >= MOTION_T:
        a = ease((t - MOTION_T) / 0.4)
        f = cv2.GaussianBlur(f, (0, 0), 1 + 26 * a)
        f = (f.astype(np.float32) * (1 - 0.32 * a)).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(f).convert("RGBA")
    for i, (a0, a1, *_rest) in enumerate(TEXTES):
        a1 = CARD_T if a1 is None else a1
        if a0 <= t < a1:
            img.alpha_composite(text_layer(i))
    if t >= CARD_T:
        img.alpha_composite(motion_layer(t - CARD_T))
    return img.convert("RGB")

def build_audio(out_wav):
    """Musique fournie dès 0 s (son d'origine supprimé), fondu de sortie, SFX sur la carte CTA."""
    fc = (f"[0:a]atrim=0:{END_T},asetpts=PTS-STARTPTS,afade=t=out:st={END_T - 0.8}:d=0.8[mus];"
          f"[1:a]adelay={int(CARD_T*1000)}|{int(CARD_T*1000)},volume=0.55[s1];"
          f"[2:a]adelay={int((CARD_T+0.3)*1000)}|{int((CARD_T+0.3)*1000)},volume=0.6[s2];"
          f"[mus][s1][s2]amix=inputs=3:normalize=0:duration=first[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(MUSIQUE),
                    "-i", str(SFX / "whoosh_soft.wav"), "-i", str(SFX / "tick_soft.wav"),
                    "-filter_complex", fc, "-map", "[out]", "-ar", "44100", "-ac", "2", str(out_wav)], check=True)

def main():
    frames = read_frames()
    if len(sys.argv) > 2 and sys.argv[1] == "--frames":
        for ts in sys.argv[2].split(","):
            compose(frames, float(ts)).save(OUT / f"controle_{float(ts):05.2f}s.jpg", quality=88)
        return
    wav = RUN / "work/audio_final.wav"
    build_audio(wav)
    out = OUT / f"claire-chute-40-ans-fr_{VERSION}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                          str(out)], stdin=subprocess.PIPE)
    for n in range(int(END_T * FPS)):
        p.stdin.write(compose(frames, n / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out)

if __name__ == "__main__":
    main()
