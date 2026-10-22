# Montage UGC raie élargie : voix ElevenLabs maître, clips Wan (son coupé) + b-rolls, inserts, dates, accroche, sous-titres mot à mot.
# Usage : python3 work/montage.py [--c1 sorties/clips/C1-v2.mp4 --c1-debut 0.5] [--c7 ... --c7-decal 0.12] [--frames]
import argparse, json, subprocess, pathlib
ap = argparse.ArgumentParser()
ap.add_argument("--c1", default="sorties/clips/C1-v2.mp4"); ap.add_argument("--c1-debut", type=float, default=0.5)
ap.add_argument("--c7", default="sorties/clips/C7-v2.mp4"); ap.add_argument("--c7-decal", type=float, default=0.0,
                help="avance des lèvres sur la voix (s) : le clip C7 est posé d'autant plus tard")
ap.add_argument("--p2", default="", help="3D inflammation fournie par l'utilisateur (sinon br-0013 en remplacement)")
ap.add_argument("--out", default="montage/final_9x16.mp4")
ap.add_argument("--couleur", default="&H005F80C9&", help="couleur ASS de la ligne lue (défaut terracotta clair #C9805F)")
ap.add_argument("--y-sous-titres", type=int, default=1215)
a = ap.parse_args()

B = "/home/user/labo/runs/2026-10-01_claire-minoxidil-arret_full-broll/rushes/"
F = "/home/user/labo/skills/creation-full-b-roll-artiste/assets/remotion/public/fonts/"
c7 = 37.80 + a.c7_decal
# (source, début dans la source, début timeline, fin timeline, vitesse)
plans = [
    (a.c1, a.c1_debut, 0.00, 3.00),
    ("sorties/clips/C2-v1.mp4", 0.0, 3.00, 8.95),
    ("sorties/clips/C3-v1.mp4", 0.0, 8.95, 15.60),
    (B + "10_MECA_3DSCI_animation-3d-follicule-retrecit.mp4", 0.0, 15.60, 20.30),   # br-0015
    ("rushes/v-queue-utilisateur-v2-pyjama.mp4", 0.2, 20.30, 23.70),
    ("sorties/clips/C5-v1.mp4", 0.0, 23.70, 30.25),
    (B + "07_MECA_3DSCI_animation-3d-coupe-cuir.mp4", 1.0, 30.25, 32.25),          # br-0012
    (a.p2 or B + "08_MECA_3DSCI_animation-3d-cheveu-continue.mp4", 0.8 if not a.p2 else 0.3, 32.25, 35.25),  # P2 ou br-0013
    ("rushes/v-raie-utilisateur-v1.mp4", 0.9, 35.25, c7),
    (a.c7, 0.0, c7, 43.73),
]
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
ins = [("sorties/insert-raies-nb-v1.png", 0.0, 2.85, 960, 1330), ("sorties/insert-follicule-nb-v1.png", 14.30, 15.60, 760, 1330)]
cur = "base"
for k, (img, t0, t1, w, y) in enumerate(ins):
    j = n + k; inputs += ["-loop", "1", "-t", "44", "-i", img]
    fc.append(f"[{j}:v]scale={w}:-1,pad=iw+16:ih+16:8:8:white[i{k}]")
    fc.append(f"[{cur}][i{k}]overlay=(W-w)/2:{y}:enable='between(t,{t0},{t1})'[o{k}]"); cur = f"o{k}"
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
            lignes.append(f"{{\\c{COUL}}}{txt}{{\\c&H00FFFFFF&}}" if lj == li else txt)
        ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Mot,,0,0,0,,{{\\an5\\pos(540,{a.y_sous_titres})}}" + "\\N".join(lignes))
ev.append(f"Dialogue: 1,{ts(0)},{ts(2.85)},Hook,,0,0,0,,{{\\an8\\pos(540,250)}}Si ta raie s’élargit\\Nécoute bien")
for t0, t1, txt in [(20.30, 23.70, "mars 2024"), (35.25, c7, "juin 2024")]:
    ev.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},Date,,0,0,0,,{{\\an7\\pos(60,140)}}{txt}")
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
       "-t", "43.73", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", a.out]
subprocess.run(cmd, check=True)
print("écrit :", a.out)
