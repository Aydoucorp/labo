# Assemble le film final : clips rognés à la durée mesurée de chaque plan (1080x1920, 30 i/s), voix off entière,
# bruitages papier des clips sous la voix, tampons de notes (1/10, 0/10, 5/10) qui tombent pile sur le mot, avec un choc sourd.
# Usage (depuis le dossier du run) : python3 montage/montage.py
import json, os, subprocess

# (plan, début, fin) mesurés sur la voix off (work/words.json, alignement MMS)
PLANS = [("P01", 0.00, 2.66), ("P02", 2.66, 5.76), ("P03", 5.76, 7.63), ("P04", 7.63, 11.03), ("P05", 11.03, 13.36),
         ("P06", 13.36, 15.84), ("P07", 15.84, 17.27), ("P08", 17.27, 19.69), ("P09", 19.69, 21.69), ("P10", 21.69, 25.58),
         ("P11", 25.58, 28.78), ("P12", 28.78, 31.74), ("P13", 31.74, 34.69), ("P14", 34.69, 39.06), ("P15", 39.06, 40.62),
         ("P16", 40.62, 42.19)]
DUREE = 42.19
H3 = {"P03", "P05", "P06", "P08", "P09", "P11", "P13", "P15"}  # plans refusés par Omni, animés avec MiniMax H3
OFFSET = {"P14": 0.60, "P08": 1.20}  # P14 : la croix sur « 5 % » arrive vers 3,9 s dans le clip ; on démarre plus tard pour la caler sur « même pas » (37,88 s)
# tampons : (dossier, instant du mot, plan, centre x, centre y, largeur) en fractions de l'image
TAMPONS = [("1-10", 6.95, "P03", 0.73, 0.50, 0.56), ("0-10", 14.84, "P06", 0.70, 0.66, 0.56), ("5-10", 20.96, "P09", 0.70, 0.55, 0.56)]
SFX_IMPACT = "/home/user/labo/skills/creation-full-b-roll-artiste/assets/sfx/impact_low.wav"

fin_plan = {p: b for p, a, b in PLANS}
src = lambda p: f"sorties/clips/{p}-clip-{'h3-' if p in H3 else ''}v1.mp4"

inputs, vf, af, vl, al = [], [], [], [], []
for k, (p, a, b) in enumerate(PLANS):
    d, o = round(b - a, 3), OFFSET.get(p, 0.0)
    inputs += ["-i", src(p)]
    vf.append(f"[{k}:v]trim={o}:{o + d},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1,"
              f"tpad=stop_mode=clone:stop_duration=1,trim=0:{d},setpts=PTS-STARTPTS[v{k}]")
    af.append(f"[{k}:a]atrim={o}:{o + d},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{d}[a{k}]")
    vl.append(f"[v{k}]"); al.append(f"[a{k}]")
n = len(PLANS)
inputs += ["-i", "audio/voix.mp3"]; i_voix = n
fc = vf + af + ["".join(vl) + f"concat=n={n}:v=1:a=0[base]",
                "".join(al) + f"concat=n={n}:v=0:a=1,volume=-12dB[sfx]"]

# tampons : séquence d'impact (8 images) puis image finale tenue jusqu'à la fin du plan
cur, idx = "base", n + 1
impacts = []
for j, (dos, t, p, cx, cy, wf) in enumerate(TAMPONS):
    final_w = 570  # largeur du tampon final dans sa séquence d'impact (916 px = 1,6 x)
    s = wf * 1080 / final_w
    seq_w, seq_h = int(916 * s) // 2 * 2, int(656 * s) // 2 * 2
    x, y = int(cx * 1080 - seq_w / 2), int(cy * 1920 - seq_h / 2)
    inputs += ["-framerate", "30", "-itsoffset", f"{t:.3f}", "-i", f"montage/tampons/{dos}/f%03d.png"]
    inputs += ["-loop", "1", "-framerate", "30", "-i", f"montage/tampons/{dos}/f007.png"]
    t_fin = t + 8 / 30
    fc.append(f"[{idx}:v]scale={seq_w}:{seq_h},format=rgba[ts{j}]")
    fc.append(f"[{idx + 1}:v]scale={seq_w}:{seq_h},format=rgba,trim=0:{DUREE},setpts=PTS-STARTPTS[tf{j}]")
    fc.append(f"[{cur}][ts{j}]overlay={x}:{y}:eof_action=pass[o{j}a]")
    fc.append(f"[o{j}a][tf{j}]overlay={x}:{y}:enable='between(t,{t_fin:.3f},{fin_plan[p]:.3f})'[o{j}]")
    cur = f"o{j}"; idx += 2
    impacts.append(t)
for j, t in enumerate(impacts):
    inputs += ["-i", SFX_IMPACT]
    fc.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-4dB,adelay={int(t * 1000)}|{int(t * 1000)},apad[imp{j}]")
    idx += 1
fc.append(f"[{i_voix}:a]aresample=48000,aformat=channel_layouts=stereo[vo]")
fc.append("[vo][sfx]" + "".join(f"[imp{j}]" for j in range(len(impacts))) +
          f"amix=inputs={2 + len(impacts)}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aud]")
fc.append(f"[{cur}]format=yuv420p[vid]")

os.makedirs("retenues/film", exist_ok=True)
out = "retenues/film/claire-remedes-naturels-papercut-v1.mp4"
cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[vid]", "-map", "[aud]",
       "-t", f"{DUREE}", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-r", "30",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print(out)
