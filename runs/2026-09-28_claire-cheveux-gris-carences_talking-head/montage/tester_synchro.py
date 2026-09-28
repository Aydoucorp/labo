#!/usr/bin/env python3
"""Vidéo test : son Seedance coupé, voix off (extrait @Audio1) posée dessus, clip recalé phrase par phrase
(début de chaque phrase du clip aligné sur le début de la même phrase dans la voix off).
Usage : python3 montage/tester_synchro.py avatar/A01_sync_v1.mp4 audio_avatar/A01.wav sortie.mp4"""
import sys, re, subprocess, shutil, pathlib
from faster_whisper import WhisperModel
clip, voix, out = sys.argv[1:4]
m = WhisperModel("medium", device="cpu", compute_type="int8")
def mots(f):
    segs, _ = m.transcribe(f, language="fr", word_timestamps=True)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
a, b = mots(clip), mots(voix)
norm = lambda w: re.sub(r"[^\w]", "", w.lower())
pairs, j = [], 0
for wb in b:
    for k in range(j, min(j + 4, len(a))):
        if norm(a[k][0])[:4] == norm(wb[0])[:4]:
            pairs.append((a[k], wb)); j = k + 1; break
anch = [(pairs[0][0][1], pairs[0][1][1])]
for (pa, pb), (qa, qb) in zip(pairs, pairs[1:]):
    if re.search(r"[.,:;!?]$", pb[0]) or qb[1] - pb[2] > 0.25:
        if qa[1] > anch[-1][0] + 0.1 and qb[1] > anch[-1][1] + 0.1:
            anch.append((qa[1], qb[1]))
anch.append((pairs[-1][0][2], pairs[-1][1][2]))
cs, ms = [x for x, _ in anch], [y for _, y in anch]
print("vitesses par phrase :", [round((cs[k+1]-cs[k])/(ms[k+1]-ms[k]), 2) for k in range(len(ms)-1)])
def ct(t):
    if t <= ms[0]: return cs[0] - (ms[0] - t)
    if t >= ms[-1]: return cs[-1] + (t - ms[-1])
    for k in range(len(ms)-1):
        if ms[k] <= t <= ms[k+1]:
            return cs[k] + (t - ms[k]) * (cs[k+1]-cs[k]) / (ms[k+1]-ms[k])
tmp = pathlib.Path("/tmp/claude-0/test_sync"); shutil.rmtree(tmp, ignore_errors=True); (tmp/"src").mkdir(parents=True); (tmp/"seq").mkdir()
subprocess.run(["ffmpeg","-v","error","-i",clip,"-vf","fps=30",str(tmp/"src/%05d.png")],check=True)
n = len(list((tmp/"src").glob("*.png")))
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",voix],capture_output=True,text=True).stdout)
for f in range(int(dur*30)):
    idx = min(n, max(1, int(round(ct(f/30)*30))+1))
    (tmp/"seq"/f"{f:05d}.png").symlink_to(tmp/"src"/f"{idx:05d}.png")
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",str(tmp/"seq/%05d.png"),"-i",voix,"-map","0:v","-map","1:a",
                "-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest",out],check=True)
shutil.rmtree(tmp)
print(out)
