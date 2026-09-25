# Assemble le film final : clips rognés/figés à la durée mesurée de chaque plan, voix off entière, bruitages papier sous la voix.
import subprocess, os
exec(open("build_storyboard.py").read().split("def texts")[0])
FF = os.path.expanduser("~/.local/bin/ffmpeg")

# segments par plan : (début dans le clip, fin dans le clip, gel en fin de segment)
SEG = {p[0]: [(0.0, round(p[2]-p[1], 3), 0.0)] for p in PLANS}
SEG["P11"] = [(0.90, 0.90+2.42, 0.0)]                 # saute le doublon du livret (0,2-0,6 s)
SEG["P07"] = [(0.42, 1.45, 2.73-1.03),                # QUANTITÉ seul jusqu'au 2e « ni » (18,32)
              (1.50, 2.58, 1.22-1.08),                # + ÉPAISSEUR jusqu'au 3e « ni » (19,54)
              (2.62, 2.62+0.99, 0.0)]                 # + VITESSE jusqu'à 20,53

inputs, vf, af, vl, al = [], [], [], [], []
k = 0
for p in PLANS:
    pid = p[0]
    for (a, b, hold) in SEG[pid]:
        inputs += ["-i", f"sorties/clips/{pid}-clip-v1.mp4"]
        vf.append(f"[{k}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration={hold:.3f}[v{k}]")
        af.append(f"[{k}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,apad=pad_dur={hold:.3f}[a{k}]")
        vl.append(f"[v{k}]"); al.append(f"[a{k}]"); k += 1
inputs += ["-i", "audio/voix-off-finale.m4a"]
fc = ";".join(vf + af) + ";" + \
     "".join(vl) + f"concat=n={k}:v=1:a=0,format=yuv420p[vid];" + \
     "".join(al) + f"concat=n={k}:v=0:a=1,volume=-12dB,alimiter=limit=0.2[sfx];" + \
     f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo[vo];" + \
     "[vo][sfx]amix=inputs=2:duration=first:normalize=0[aud]"
os.makedirs("retenues/film", exist_ok=True)
cmd = [FF, "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[vid]", "-map", "[aud]",
       "-t", "31.72", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-r", "30",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "retenues/film/claire-guide-racine-papercut-v1.mp4"]
subprocess.run(cmd, check=True)
print("ok")
