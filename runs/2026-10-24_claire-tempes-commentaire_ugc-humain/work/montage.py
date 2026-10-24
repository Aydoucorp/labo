# Montage UGC tempes, réponse à un commentaire : voix ElevenLabs maître, clips Wan (son coupé, recalés) + b-rolls, bulle commentaire, sous-titres terracotta.
# Usage : python3 work/montage.py --b6 wan|motion|mixte [--b1 rush.mp4] [--b5 rush.mp4] [--out montage/final_9x16.mp4]
import argparse, json, subprocess, pathlib
ap = argparse.ArgumentParser()
ap.add_argument("--b6", choices=["wan", "motion", "mixte"], default="wan", help="B6 : clip Wan recalé, motion design, ou Wan sur « moins lifté » puis motion design")
ap.add_argument("--b1", default="", help="3D B1 de l'utilisateur (sinon provisoire bibliothèque)")
ap.add_argument("--b5", default="", help="3D B5 de l'utilisateur (sinon provisoire bibliothèque)")
ap.add_argument("--out", default="montage/final_9x16.mp4")
ap.add_argument("--couleur", default="&H005F80C9&", help="couleur ASS de la ligne lue (terracotta clair #C9805F)")
ap.add_argument("--y-sous-titres", type=int, default=1215)
a = ap.parse_args()

B = "/home/user/labo/runs/2026-10-01_claire-minoxidil-arret_full-broll/rushes/"
C, R, M = "sorties/clips/", "rushes/recus/", "sorties/motion/"
# (source, début dans la source, début timeline, fin timeline[, zoom image])
plans = [(C + "W1-v1.mp4", 0.5, 0.00, 7.75)]
if a.b1: plans.append((a.b1, 0.0, 7.75, 13.30))
else: plans += [(B + "14b_MECA_3DSCI_animation-3d-seul-follicule.mp4", 0.0, 7.75, 10.45),      # provisoire br-0019 : « restent ancrés moins longtemps »
                (B + "14a_MECA_3DSCI_animation-3d-large-dizaines.mp4", 0.6, 10.45, 12.00),      # provisoire br-0018 : « plus de chute »
                (B + "10_MECA_3DSCI_animation-3d-follicule-retrecit.mp4", 1.9, 12.00, 13.30)]  # provisoire br-0015 : « cheveux plus courts »
plans += [
    (R + "B2a-queue-de-cheval.jpg", 0, 13.30, 16.40, "in"),     # « tension constante, queues de cheval »
    (R + "B2b-chignon.jpg", 0, 16.40, 17.27, "out"),            # « chignons flous »
    (R + "B2c-bandeau.jpg", 0, 17.27, 17.86, "in"),             # « bandeaux »
    ("sorties/images/B2d-lunettes-v2.png", 0, 17.86, 19.40, "out"),  # « lunettes de soleil sur la tête »
    (C + "W3-v1.mp4", 0.0, 19.40, 23.95), (C + "W3-v1.mp4", 4.85, 23.95, 25.05),
    (C + "W4-v1.mp4", 0.24, 25.05, 26.88),
    (R + "b3-candidat-2.mp4", 0.0, 26.88, 30.88), (R + "b3-candidat-1.mp4", 0.0, 30.88, 31.75),
    (R + "b4-microscope.mp4", 0.0, 31.75, 36.60),
    (a.b5, 0.0, 36.60, 40.45) if a.b5 else (B + "15b_MECA_3DSCI_animation-3d-petite-poche.mp4", 0.3, 36.60, 40.45),  # provisoire br-0021
    (C + "W5-v1.mp4", 0.0, 40.45, 44.30),
]
if a.b6 == "wan":
    plans += [(C + "B6W-v1.mp4", 0.0, 44.30, 46.75), (C + "B6W-v1.mp4", 3.01, 46.75, 47.70), (C + "B6W-v1.mp4", 4.10, 47.70, 49.60)]
elif a.b6 == "motion":
    plans += [(M + "B6-motion-v1.mp4", 0.0, 44.30, 49.60)]
else:
    plans += [(C + "B6W-v1.mp4", 0.0, 44.30, 46.02), (M + "B6-motion-v1.mp4", 1.72, 46.02, 49.60)]
plans += [
    (C + "W6-v1.mp4", 0.0, 49.60, 52.48), (C + "W6-v1.mp4", 3.22, 52.48, 53.12),
    (M + "M2-motion-v1.mp4", 0.0, 53.12, 57.40),
    (C + "W7-v1.mp4", 0.0, 57.40, 63.25), (C + "W7-v1.mp4", 6.15, 63.25, 64.91),
]
FIN = 64.91
# fonds crème (motion design) : sous-titres encre avec contour crème ; les 3D (fond prune) gardent les sous-titres blancs
MOTION = [(53.12, 57.40)]
if a.b6 == "motion": MOTION.append((44.30, 49.60))
if a.b6 == "mixte": MOTION.append((46.02, 49.60))

inputs, fc, labels = [], [], []
for i, pl in enumerate(plans):
    src, s0, t0, t1 = pl[:4]; d = t1 - t0
    if src.endswith((".jpg", ".png")):
        # image fixe : Ken Burns doux (zoom avant ou arrière de 8 %), suréchantillonné pour éviter le tremblement
        n = int(round(d * 30)) + 2
        z = f"1+0.08*on/{n}" if pl[4] == "in" else f"1.08-0.08*on/{n}"
        inputs += ["-loop", "1", "-framerate", "30", "-t", f"{d + 0.2}", "-i", src]
        fc.append(f"[{i}:v]scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,"
                  f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
                  f"trim=duration={d},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    else:
        dur_src = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
        vit = min(1.0, (dur_src - s0) / d)  # ralenti léger si le rush est trop court
        inputs += ["-i", src]
        fc.append(f"[{i}:v]trim=start={s0}:duration={d * vit + 0.05},setpts=(PTS-STARTPTS)/{vit},"
                  f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,"
                  f"trim=duration={d},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    labels.append(f"[v{i}]")
n = len(plans)
fc.append("".join(labels) + f"concat=n={n}:v=1:a=0[base]")
# bulle « Réponse au commentaire de Sylvie » : apparaît d'un coup, s'efface pendant la pause après « tempes »
inputs += ["-loop", "1", "-framerate", "30", "-t", f"{FIN}", "-i", "montage/bulle.png"]
fc.append(f"[{n}:v]format=rgba,fade=t=out:st=4.10:d=0.25:alpha=1[bul]")
fc.append("[base][bul]overlay=0:0:shortest=1[o0]")

def ts(t):
    t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
mots = [w for w in json.load(open("work/mots.json"))["words"] if w["start"] >= 4.3]  # le commentaire lu est déjà dans la bulle
def propre(w): return w["w"].strip("«»,.…!?").upper().replace("'", "’")
phrases, ph = [], []
for k, w in enumerate(mots):
    ph.append(w)
    if w["w"].rstrip().endswith((",", ".", "…", "»", "!", "?", ":")) or (w.get("punct_after") or "").strip() or k + 1 == len(mots) or mots[k + 1]["start"] - w["end"] > 0.25:
        phrases.append(ph); ph = []
def lignes_de(ph, maxc=16):
    import math
    n_ = max(1, math.ceil(len(" ".join(propre(x) for x in ph)) / maxc))
    while True:
        cible = len(" ".join(propre(x) for x in ph)) / n_
        out, l = [], []
        for w in ph:
            if l and len(" ".join(propre(x) for x in l + [w])) > max(cible + 3, 8) and len(out) < n_ - 1:
                out.append(l); l = []
            l.append(w)
        out.append(l)
        if all(len(" ".join(propre(x) for x in o)) <= maxc + 2 for o in out) or n_ > 8:
            return out
        n_ += 1
blocs = []
for ph in phrases:
    ls = lignes_de(ph)
    for i in range(0, len(ls), 2):
        blocs.append(ls[i:i + 2])
ev = []
for b, bl in enumerate(blocs):
    t_fin_bloc = blocs[b + 1][0][0]["start"] if b + 1 < len(blocs) else min(FIN, bl[-1][-1]["end"] + 0.4)
    for li, l in enumerate(bl):
        t0 = l[0]["start"]; t1 = bl[li + 1][0]["start"] if li + 1 < len(bl) else t_fin_bloc
        clair = any(m0 <= t0 < m1 for m0, m1 in MOTION)
        base, fort = ("&H00262A2E&", "&H003A55A8&") if clair else ("&H00FFFFFF&", a.couleur)
        lignes = [f"{{\\c{fort}}}{' '.join(propre(x) for x in l2)}{{\\c{base}}}" if lj == li else " ".join(propre(x) for x in l2) for lj, l2 in enumerate(bl)]
        style = "{\\c&H00262A2E&\\3c&H00F3F6FA&\\bord4\\shad0}" if clair else ""
        ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Mot,,0,0,0,,{{\\an5\\pos(540,{a.y_sous_titres})}}" + style + "\\N".join(lignes))
ASS = a.out.rsplit(".", 1)[0] + ".ass"
pathlib.Path(ASS).write_text("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Mot,Montserrat ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00201A16,&H8C000000,-1,0,0,0,100,100,0,0,1,2.5,3,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
fc.append(f"[o0]ass={ASS}:fontsdir=montage/polices[vout]")
inputs += ["-i", "audio/voix.mp3"]
fc.append(f"[{n + 1}:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
       "-t", f"{FIN}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", a.out]
subprocess.run(cmd, check=True)
print("écrit :", a.out)
