# Montage UGC tempes : voix ElevenLabs maître, clips Wan (son coupé) + b-rolls, inserts, dates, accroche, sous-titres mot à mot.
# Usage : python3 work/montage.py [--b1 rush.mp4] [--b4 rush.mp4] [--avant photo.jpg --apres photo.jpg] [--out ...]
import argparse, json, subprocess, pathlib
ap = argparse.ArgumentParser()
ap.add_argument("--b1", default="", help="b-roll tempe clairsemée de l'utilisateur (sinon provisoire)")
ap.add_argument("--b3", default="", help="3D Drew follicule qui se fragilise (sinon provisoire)")
ap.add_argument("--b4", default="", help="b-roll macro des cheveux fins de l'utilisateur (sinon provisoire)")
ap.add_argument("--avant", default="", help="photo avant de l'utilisateur"); ap.add_argument("--apres", default="", help="photo après de l'utilisateur")
ap.add_argument("--out", default="montage/final_9x16.mp4")
ap.add_argument("--couleur", default="&H005F80C9&", help="couleur ASS de la ligne lue (défaut terracotta clair #C9805F)")
ap.add_argument("--y-sous-titres", type=int, default=1215)
a = ap.parse_args()

B = "/home/user/labo/runs/2026-10-01_claire-minoxidil-arret_full-broll/rushes/"
B4P = B + "16_MECA_UGC_petits-cheveux-repousse-ligne.mp4"  # provisoire : br-0022
B75 = "/home/user/labo/runs/2026-10-08_claire-menopause-affinement_talking-head/generations/E1_v1.mp4"  # br-0075
F = "/home/user/labo/skills/creation-full-b-roll-artiste/assets/remotion/public/fonts/"
BR = "/home/user/labo/bibliotheque/brolls-reels/"
# (source, début dans la source, début timeline, fin timeline)
plans = [
    ("sorties/clips/W1-v1.mp4", 0.5, 0.00, 8.20),
    ("sorties/clips/W8-v1.mp4", 0.0, 8.20, 11.40),
    ("sorties/clips/W8-v1.mp4", 3.43, 11.40, 14.75),   # Wan en retard de 0,23 s après « à ça » : saut dans la pause
    ("sorties/clips/W2-v1.mp4", 0.0, 14.75, 18.05),
    (a.b1 or B4P, 0.3 if a.b1 else 0.0, 18.05, 21.70),   # provisoire : br-0022 (br-0031 contient en fait une hélice d'ADN, voir montage.md)
    ("sorties/motion/B2-motion.mp4", 0.0, 21.70, 25.50),                                     # motion design : cycle de pousse
    (a.b3 or B + "10_MECA_3DSCI_animation-3d-follicule-retrecit.mp4", 1.9, 25.50, 27.85),   # provisoire : br-0015
    ("sorties/clips/W3-v1.mp4", 0.0, 27.85, 29.40),
    (a.b4 or B + "07_MECA_3DSCI_animation-3d-coupe-cuir.mp4", 0.0, 29.40, 34.45),   # provisoire : br-0012
    ("sorties/clips/W4-v1.mp4", 0.0, 34.45, 42.55),
    ("sorties/clips/W5-v1.mp4", 0.47, 42.55, 44.25),   # Wan en retard constant de 0,47 s
    ("sorties/motion/B5a-motion.mp4", 0.0, 44.25, 49.05),                                    # motion design : hormones, tempes
    ("sorties/motion/B5b-motion.mp4", 0.0, 49.05, 52.00),                                    # motion design : œstrogène, cortisol
    ("sorties/clips/W6-v1.mp4", 0.05, 52.00, 53.10),
    ("sorties/clips/W6-v1.mp4", 1.30, 53.10, 54.85),   # retard qui monte à 0,2 s : recalage à « devient »
    ("sorties/clips/W7-v1.mp4", 0.0, 54.85, 64.99),
]
MOTION = [(21.70, 25.50), (44.25, 52.00)]  # plans de motion design sur fond crème
inputs, fc, labels = [], [], []
for i, (src, s0, t0, t1) in enumerate(plans):
    d = t1 - t0
    dur_src = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
    vit = min(1.0, (dur_src - s0) / d)  # ralenti léger si le rush est trop court
    inputs += ["-i", src]
    fc.append(f"[{i}:v]trim=start={s0}:duration={d * vit + 0.05},setpts=(PTS-STARTPTS)/{vit},"
              f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,"
              f"trim=duration={d},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    labels.append(f"[v{i}]")
n = len(plans)
fc.append("".join(labels) + f"concat=n={n}:v=1:a=0[base]")
# inserts
ins = []
if a.avant: ins.append((a.avant, 9.85, 13.30, 320, 170, 28))
if a.apres: ins.append((a.apres, 10.80, 13.30, 320, 170, 716))
cur = "base"
for k, (img, t0, t1, w, y, x) in enumerate(ins):
    j = n + k; inputs += ["-loop", "1", "-t", "66", "-i", img]
    fc.append(f"[{j}:v]scale={w}:-1,pad=iw+16:ih+16:8:8:white[i{k}]")
    fc.append(f"[{cur}][i{k}]overlay={x}:{y}:enable='between(t,{t0},{t1})'[o{k}]"); cur = f"o{k}"
fc.append(f"[{cur}]ass=montage/textes.ass[vout]")

# sous-titres mot à mot + accroche + dates (ASS)
def ts(t):
    t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
mots = json.load(open("work/mots.json"))["words"]
ev = []
# Sous-titres façon pub Facebook de référence : 2 lignes centrées, majuscules, la ligne en cours de lecture en couleur (terracotta), l'autre en blanc.
COUL = a.couleur
def propre(w): return w["w"].strip("«»,.…").upper().replace("'", "’")
# 1) phrases (ponctuation ou pause > 0,25 s) ; 2) lignes équilibrées de 16 caractères max ; 3) blocs de 2 lignes
phrases, ph = [], []
for k, w in enumerate(mots):
    ph.append(w)
    if w["w"].rstrip().endswith((",", ".", "…", "»")) or (w.get("punct_after") or "").strip() or k + 1 == len(mots) or mots[k + 1]["start"] - w["end"] > 0.25:
        phrases.append(ph); ph = []
def lignes_de(ph, maxc=16):
    import math
    n = max(1, math.ceil(len(" ".join(propre(x) for x in ph)) / maxc))
    while True:
        cible = len(" ".join(propre(x) for x in ph)) / n
        out, l = [], []
        for w in ph:
            if l and len(" ".join(propre(x) for x in l + [w])) > max(cible + 3, 8) and len(out) < n - 1:
                out.append(l); l = []
            l.append(w)
        out.append(l)
        if all(len(" ".join(propre(x) for x in o)) <= maxc + 2 for o in out) or n > 8:
            return out
        n += 1
blocs = []
for ph in phrases:
    ls = lignes_de(ph)
    for i in range(0, len(ls), 2):
        blocs.append(ls[i:i + 2])
for b, bl in enumerate(blocs):
    t_fin_bloc = blocs[b + 1][0][0]["start"] if b + 1 < len(blocs) else bl[-1][-1]["end"] + 0.4
    for li, l in enumerate(bl):
        t0 = l[0]["start"]; t1 = bl[li + 1][0]["start"] if li + 1 < len(bl) else t_fin_bloc
        lignes = []
        for lj, l2 in enumerate(bl):
            txt = " ".join(propre(x) for x in l2)
            clair = any(m0 <= t0 < m1 for m0, m1 in MOTION)  # fond crème : encre + terracotta, sans contour
            base, fort = ("&H00262A2E&", "&H003A55A8&") if clair else ("&H00FFFFFF&", COUL)
            lignes.append(f"{{\\c{fort}}}{txt}{{\\c{base}}}" if lj == li else txt)
        clair = any(m0 <= t0 < m1 for m0, m1 in MOTION)
        style = "{\\c&H00262A2E&\\bord0\\shad0}" if clair else ""
        ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Mot,,0,0,0,,{{\\an5\\pos(540,{a.y_sous_titres})}}" + style + "\\N".join(lignes))
ev.append(f"Dialogue: 1,{ts(0)},{ts(2.85)},Hook,,0,0,0,,{{\\an8\\pos(540,250)}}Tes tempes\\Ns’affinent ?")
pathlib.Path("montage").mkdir(exist_ok=True)
pathlib.Path("montage/textes.ass").write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Mot,Montserrat ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00201A16,&H8C000000,-1,0,0,0,100,100,0,0,1,2.5,3,5,0,0,0,1
Style: Hook,Montserrat ExtraBold,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,0,8,0,0,0,1
Style: Date,Montserrat ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,2,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
fc[-1] = f"[{cur}]ass=montage/textes.ass:fontsdir={F}[vout]"
vi = n + len(ins); inputs += ["-i", "audio/voix.mp3"]
fc.append(f"[{vi}:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
       "-t", "64.99", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", a.out]
subprocess.run(cmd, check=True)
print("écrit :", a.out)
