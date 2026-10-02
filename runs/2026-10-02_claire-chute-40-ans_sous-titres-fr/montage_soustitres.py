# montage_soustitres.py
# Montage léger sur une vidéo TikTok existante (avant/après chute de cheveux, 40 ans) :
#  1. part de work/efface.mkv (ses textes anglais effacés par LaMa, voir effacer_textes.py) ;
#  2. pose les textes FR dans son style (blanc, contour et ombre noirs, émojis), mêmes places, mêmes timings ;
#  3. coupe avant l'apparition du produit : gel sur l'image 351 (11,70 s), léger zoom ;
#  4. motion CTA Claire « Commente GUIDE » sur le dernier plan flouté ;
#  5. prolonge la musique d'origine par un raccord sur une mesure plus tôt (9,20 s).
# Usage : python3 montage_soustitres.py [--frames t1,t2,...]  (sans option : rendu complet)

import math, subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original_pure-batana76.mp4"
EFFACE = RUN / "work/efface.mkv"
FONTS = RUN / "work/fonts"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
OUT = RUN / "sorties"
W, H, FPS = 1080, 1920, 30
VERSION = "v1"

# ---- réglages ----
FREEZE_T = 11.70      # dernière image sans le flacon (image 351)
MOTION_T = 12.40      # début du flou + motion
CARD_T = 12.65        # apparition de la carte CTA
END_T = 15.80
AUDIO_LOOP_FROM = 9.20   # raccord musical trouvé par similarité spectrale
AUDIO_CUT = 14.70
SFX = Path("/home/user/labo/skills/creation-full-b-roll-artiste/assets/sfx")

# Textes : (début, fin, lignes, centre vertical de chaque ligne en px 1080x1920). Timings = ceux de ses textes.
TEXTES = [
    (0.000, 2.633, ["La chute de cheveux", "à 40 ans, c'est terrifiant 😢💔"], [356, 446]),
    (0.500, 2.633, ["Jour 1"], [255]),
    (3.233, 5.367, ["Jour 14"], [255]),
    (5.833, 8.633, ["Jour 90"], [255]),
    (9.700, CARD_T, ["Jour 180 😍"], [255]),
]
FONDU = 0.12  # apparition / disparition des textes

CREME, CREME_F, TERRA, TERRA_C, ENCRE = "#FAF6F3", "#EFE7E0", "#A8553A", "#C9805F", "#2E2A26"
CTA_LIGNES = ["pour recevoir", "la solution"]

def font(w, size):
    return ImageFont.truetype(str(FONTS / f"TikTokSans-{w}.ttf"), size)

EMOJI = ImageFont.truetype(EMOJI_FONT, 109)
TXT = font(600, 68)

def is_emoji(c):
    return ord(c) > 0x2500

def draw_line(img, text, cy):
    """Texte blanc, contour noir et ombre portée, émojis en couleur, centré horizontalement."""
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
    d = ImageDraw.Draw(img)
    esz = 74
    widths = [d.textlength(s, font=TXT) if k == "t" else esz + 6 for k, s in parts]
    x = W / 2 - sum(widths) / 2
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    xs = x
    for (k, s), w in zip(parts, widths):
        if k == "t":
            sd.text((xs + 3, cy + 5), s, font=TXT, fill=(0, 0, 0, 170), anchor="lm", stroke_width=6, stroke_fill=(0, 0, 0, 170))
        xs += w
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)))
    for (k, s), w in zip(parts, widths):
        if k == "t":
            d.text((x, cy), s, font=TXT, fill="white", anchor="lm", stroke_width=5, stroke_fill="black")
        else:
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            ImageDraw.Draw(e).text((6, 6), s, font=EMOJI, embedded_color=True)
            bb = e.getbbox()
            if bb:
                e = e.crop(bb).resize((esz, esz), Image.LANCZOS)
                img.alpha_composite(e, (int(x + 3), int(cy - esz / 2)))
        x += w

LAYERS = {}

def text_layer(i):
    if i not in LAYERS:
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        _, _, lignes, ys = TEXTES[i]
        for l, y in zip(lignes, ys):
            draw_line(img, l, y)
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
    cap = cv2.VideoCapture(str(EFFACE)); fr = []
    while True:
        ok, f = cap.read()
        if not ok:
            return fr
        fr.append(f)

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
    for i, (a0, a1, _, _) in enumerate(TEXTES):
        if a0 <= t < a1:
            al = min(1, (t - a0) / FONDU if a0 > 0 else 1, (a1 - t) / FONDU)
            lay = text_layer(i)
            if al < 1:
                lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * al)))
            img.alpha_composite(lay)
    if t >= CARD_T:
        img.alpha_composite(motion_layer(t - CARD_T))
    return img.convert("RGB")

def build_audio(out_wav):
    xf = 0.15
    tail = END_T - AUDIO_CUT + xf
    fc = (f"[0:a]atrim=0:{AUDIO_CUT},asetpts=PTS-STARTPTS[a];"
          f"[1:a]atrim=0:{tail},asetpts=PTS-STARTPTS[b];"
          f"[a][b]acrossfade=d={xf}[m];"
          f"[m]afade=t=out:st={END_T - 0.8}:d=0.8,atrim=0:{END_T}[mus];"
          f"[2:a]adelay={int(CARD_T*1000)}|{int(CARD_T*1000)},volume=0.55[s1];"
          f"[3:a]adelay={int((CARD_T+0.3)*1000)}|{int((CARD_T+0.3)*1000)},volume=0.6[s2];"
          f"[mus][s1][s2]amix=inputs=3:normalize=0:duration=first[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-ss", str(AUDIO_LOOP_FROM - xf), "-i", str(SRC),
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
