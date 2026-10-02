# Montage UGC humain format A : 3 clips Seedance bout à bout (1080x1920, 30 i/s, son des clips coupé),
# le texte du script sur chaque plan (fichiers montage/textes/NN.txt), musique de la vidéo d'origine
# prolongée par un fondu sur elle-même jusqu'à la fin, puis fondu de sortie.
# Usage (depuis le dossier du run) : python3 montage/montage.py
import subprocess, os
FONT = "/home/user/labo/skills/creation-full-b-roll-artiste/assets/remotion/public/fonts/Montserrat-Bold.ttf"
CLIPS = ["sorties/clips/A-v1.mp4", "sorties/clips/B-v1.mp4", "sorties/clips/C-v1.mp4"]
# coupes mesurées (scdet) dans chaque clip, en secondes depuis le début du film
COUPES = [0, 2.625, 5.333, 9.167, 13.042, 13.042 + 2.958, 13.042 + 4.792, 13.042 + 7.042, 24.083, 24.083 + 3.667, 31.125]
DUREE = COUPES[-1]
MUSIQUE = "audio/musique-originale.m4a"
REPRISE, FONDU = 6.0, 1.5   # la musique (26,5 s) repart de 6 s avec un fondu enchaîné pour couvrir 31 s

v = "".join(f"[{i}:v]scale=1080:1920:flags=lanczos,fps=30,setsar=1[v{i}];" for i in range(3))
v += "[v0][v1][v2]concat=n=3:v=1:a=0[base]"
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
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "retenues/claire-apres-shampoing-ugc-v1.mp4"]
os.makedirs("retenues", exist_ok=True)
subprocess.run(cmd, check=True)
print("retenues/claire-apres-shampoing-ugc-v1.mp4")
