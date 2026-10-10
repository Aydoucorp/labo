#!/usr/bin/env python3
"""Compare le minutage des mots : voix off de référence vs voix générée par Seedance (dont les lèvres suivent sa propre voix).
Usage : comparer_synchro.py <reference.wav> <clip.mp4> [<clip2.mp4> ...]   (Whisper small, français)"""
import sys, re, difflib, subprocess, tempfile
from faster_whisper import WhisperModel
m = WhisperModel("small", compute_type="int8")
norm = lambda w: re.sub(r"[^a-zàâäéèêëîïôöùûüç0-9]", "", w.lower())
def mots(path):
    wav = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    segs, _ = m.transcribe(wav, language="fr", word_timestamps=True)
    return [(w.word.strip(), round(w.start, 2)) for s in segs for w in (s.words or []) if norm(w.word)]
ref = mots(sys.argv[1])
for clip in sys.argv[2:]:
    out = mots(clip); A = [norm(w) for w, _ in ref]; B = [norm(w) for w, _ in out]
    ecarts = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): ecarts[i1 + k] = out[j1 + k][1] - ref[i1 + k][1]
    print(f"=== {clip}")
    for i, (w, t) in enumerate(ref):
        e = ecarts.get(i); print(f"{w:18s} {t:6.2f}  " + (f"{t+e:6.2f}  {e:+.2f}" if e is not None else "     ?"))
    v = [abs(e) for e in ecarts.values()]
    print(f"écart moyen {sum(v)/len(v):+.2f} s, max {max(v):.2f} s, mots appariés {len(v)}/{len(ref)}" if v else "aucun mot apparié")
