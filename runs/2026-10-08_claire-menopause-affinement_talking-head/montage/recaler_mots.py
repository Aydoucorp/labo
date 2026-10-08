#!/usr/bin/env python3
"""Recale l'image d'un clip Seedance sur la voix off, mot par mot (déformation temporelle).
Chaque mot reconnu dans le son du clip est apparié au même mot de la voix off ; entre deux mots appariés,
l'image est accélérée ou ralentie linéairement. Le son du clip est remplacé par la voix off d'origine.
Usage : python3 recaler_mots.py clip.mp4 extrait_voix_off.wav sortie.mp4 [--vmin 0.6 --vmax 1.6]
"""
import argparse, re, subprocess, cv2, numpy as np
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("clip"); ap.add_argument("voix"); ap.add_argument("sortie")
a = ap.parse_args()
m = WhisperModel("medium", device="cpu", compute_type="int8")
def mots(f):
    segs, _ = m.transcribe(f, language="fr", word_timestamps=True)
    return [(re.sub(r"[^\w]", "", w.word.lower()), w.start, w.end) for s in segs for w in s.words]
A, B = mots(a.clip), mots(a.voix)
# appariement par alignement de séquences (tolère les mots mal prononcés par Seedance), ancres sur le début des mots
import difflib
sim = lambda x, y: difflib.SequenceMatcher(None, x, y).ratio()
n, k = len(B), len(A)
D = np.zeros((n + 1, k + 1)); P = {}
for i in range(1, n + 1): D[i][0] = D[i-1][0] - 0.5
for jj in range(1, k + 1): D[0][jj] = D[0][jj-1] - 0.5
for i in range(1, n + 1):
    for jj in range(1, k + 1):
        s = sim(B[i-1][0], A[jj-1][0])
        opts = [(D[i-1][jj-1] + (s if s >= 0.5 else -1), "d"), (D[i-1][jj] - 0.5, "u"), (D[i][jj-1] - 0.5, "l")]
        D[i][jj], P[i, jj] = max(opts)
i, jj, ancres = n, k, []
while i > 0 and jj > 0:
    mv = P[i, jj]
    if mv == "d":
        if sim(B[i-1][0], A[jj-1][0]) >= 0.5: ancres.append((B[i-1][1], A[jj-1][1]))
        i, jj = i - 1, jj - 1
    elif mv == "u": i -= 1
    else: jj -= 1
ancres.sort()
dur_v = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.voix]).decode())
cap = cv2.VideoCapture(a.clip); fps = cap.get(5); N = int(cap.get(7))
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
dur_c = len(frames) / fps
# bornes : début et fin alignés, ancres strictement croissantes des deux côtés
pts = [(0.0, 0.0)] + sorted(ancres) + [(dur_v, min(dur_c - 1 / fps, dur_v + (dur_c - dur_v) if dur_c > dur_v else dur_c - 1 / fps))]
clean = [pts[0]]
for t_, s_ in pts[1:]:
    if t_ > clean[-1][0] + 0.02 and s_ > clean[-1][1] + 0.02: clean.append((t_, s_))
# lissage : on retire les ancres qui imposent une vitesse hors de [VMIN, VMAX] (image saccadée)
VMIN, VMAX = 0.65, 1.6
changed = True
while changed and len(clean) > 2:
    changed = False
    for q in range(1, len(clean) - 1):
        v1 = (clean[q][1] - clean[q-1][1]) / (clean[q][0] - clean[q-1][0])
        v2 = (clean[q+1][1] - clean[q][1]) / (clean[q+1][0] - clean[q][0])
        if not (VMIN <= v1 <= VMAX and VMIN <= v2 <= VMAX):
            del clean[q]; changed = True; break
T, S = np.array([p[0] for p in clean]), np.array([p[1] for p in clean])
h, w = frames[0].shape[:2]
tmp = a.sortie + ".video.mp4"
vw = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
n_out = int(round(dur_v * fps))
for i in range(n_out):
    s = float(np.interp(i / fps, T, S))
    vw.write(frames[min(len(frames) - 1, int(round(s * fps)))])
vw.release()
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", a.voix, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", a.sortie], check=True)
import os; os.remove(tmp)
vit = np.diff(S) / np.diff(T)
print(f"{a.sortie} : {len(clean)-2} ancres, vitesse image {vit.min():.2f} à {vit.max():.2f}, durée {dur_v:.2f} s")
