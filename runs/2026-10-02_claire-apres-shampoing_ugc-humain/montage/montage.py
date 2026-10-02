# Montage UGC humain format A : 10 plans tirés des 3 clips Seedance (début figé coupé) (1080x1920, 30 i/s, son des clips coupé),
# le texte du script sur chaque plan (fichiers montage/textes/NN.txt), musique de la vidéo d'origine
# prolongée par un fondu sur elle-même jusqu'à la fin, puis fondu de sortie.
# Usage (depuis le dossier du run) : python3 montage/montage.py
import subprocess, os
FONT = "/home/user/labo/skills/creation-full-b-roll-artiste/assets/remotion/public/fonts/Montserrat-Bold.ttf"
CLIPS = ["sorties/clips/A-v1.mp4", "sorties/clips/B-v1.mp4", "sorties/clips/C-v1.mp4"]
# plans : (clip, début, fin) mesurés par scdet dans chaque clip Seedance
PLANS = [(0, 0, 2.625), (0, 2.625, 5.333), (0, 5.333, 9.167), (0, 9.167, 13.042),
         (1, 0, 2.958), (1, 2.958, 4.792), (1, 4.792, 7.042), (1, 7.042, 11.042),
         (2, 0, 3.667), (2, 3.667, 7.042)]
# démarrage figé de Seedance (image de départ tenue avant le geste), relevé à l'œil plan par plan : on le coupe
GEL = [0.33, 0.33, 1.83, 1.45, 0.80, 0.42, 0.42, 0.25, 0.25, 0.17]  # v4 : plans 3 et 4 raccourcis au maximum (temps de lecture gardé), plan 5 un peu plus
COUPES = [0.0]
for (c, a, b), g in zip(PLANS, GEL):
    COUPES.append(round(COUPES[-1] + (b - a - g), 3))
DUREE = COUPES[-1]
# les textes suivent les coupes réellement mesurées (scdet) dans le film rendu, pour éviter l'arrondi d'une image
COUPES_MESUREES = [2.300, 4.667, 6.667, 9.133, 11.267, 12.633, 14.500, 18.233, 21.667]
if len(COUPES_MESUREES) == 9:
    COUPES = [0.0] + COUPES_MESUREES + [DUREE]
MUSIQUE = "audio/musique-originale.m4a"
REPRISE, FONDU = 6.0, 1.5   # la musique (26,5 s) repart de 6 s avec un fondu enchaîné pour couvrir 31 s

v = "".join(f"[{c}:v]trim={a + g:.3f}:{b:.3f},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,setsar=1[p{k}];"
            for k, ((c, a, b), g) in enumerate(zip(PLANS, GEL)))
v += "".join(f"[p{k}]" for k in range(10)) + "concat=n=10:v=1:a=0[base]"
txt, cur = [], "base"
for k in range(10):
    a, b = COUPES[k], COUPES[k + 1]
    nxt = f"t{k}"
    txt.append(f"[{cur}]drawtext=fontfile={FONT}:textfile=montage/textes/{k + 1:02d}.txt:expansion=none:"
               f"fontsize=50:fontcolor=white:borderw=4:bordercolor=black@0.85:shadowx=2:shadowy=3:shadowcolor=black@0.5:"
               f"line_spacing=12:text_align=center:x=(w-text_w)/2:y=330:enable='between(t,{a:.3f},{b - 0.001:.3f})'[{nxt}]")
    cur = nxt
m1 = 26.4
aud = (f"[3:a]atrim=0:{m1},asetpts=PTS-STARTPTS[m1];[4:a]atrim={REPRISE},asetpts=PTS-STARTPTS[m2];"
       f"[m1][m2]acrossfade=d={FONDU}:c1=tri:c2=tri,atrim=0:{DUREE:.3f},afade=t=out:st={DUREE - 1.5:.3f}:d=1.5,"
       f"loudnorm=I=-14:TP=-1.5:LRA=11[aud]")
fc = v + ";" + ";".join(txt) + ";" + aud
cmd = ["ffmpeg", "-v", "error", "-y"]
for c in CLIPS: cmd += ["-i", c]
cmd += ["-i", MUSIQUE, "-i", MUSIQUE, "-filter_complex", fc, "-map", f"[{cur}]", "-map", "[aud]",
        "-t", f"{DUREE:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "retenues/claire-apres-shampoing-ugc-v4.mp4"]
os.makedirs("retenues", exist_ok=True)
subprocess.run(cmd, check=True)
print("retenues/claire-apres-shampoing-ugc-v4.mp4")
