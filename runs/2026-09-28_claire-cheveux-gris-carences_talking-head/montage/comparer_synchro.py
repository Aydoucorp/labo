#!/usr/bin/env python3
"""Test de synchro : compare le temps de chaque mot dit par Seedance (son du clip) au même mot de la voix off (extrait envoyé en @Audio1).
Si les écarts sont faibles (< 0,1 s), on peut couper le son Seedance et poser la voix off : les lèvres tombent juste.
Usage : python3 montage/comparer_synchro.py avatar/A01_sync_v1.mp4 audio_avatar/A01.wav"""
import sys, re
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
def mots(f):
    segs, _ = m.transcribe(f, language="fr", word_timestamps=True)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
a, b = mots(sys.argv[1]), mots(sys.argv[2])
norm = lambda w: re.sub(r"[^\w]", "", w.lower())
print(f"{'mot voix off':18} {'voix off':>9} {'seedance':>9} {'écart':>7}")
ecarts, j = [], 0
for wb, sb, eb in b:
    for k in range(j, min(j + 4, len(a))):
        if norm(a[k][0])[:4] == norm(wb)[:4]:
            d = a[k][1] - sb; ecarts.append(d); j = k + 1
            print(f"{wb:18} {sb:9.2f} {a[k][1]:9.2f} {d:+7.2f}")
            break
    else:
        print(f"{wb:18} {sb:9.2f} {'?':>9}")
if ecarts:
    ecarts_int = ecarts[1:] if len(ecarts) > 1 else ecarts  # le premier mot Whisper est souvent mal daté
    print(f"écart moyen {sum(ecarts_int)/len(ecarts_int):+.2f} s, max {max(abs(x) for x in ecarts_int):.2f} s, mots appariés {len(ecarts)}/{len(b)}")
