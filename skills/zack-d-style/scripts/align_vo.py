#!/usr/bin/env python3
"""Whisper mots -> aligne chaque ligne du script (1 ligne = 1 plan) -> <run>/shots_timing.json + words_en.json
Usage : align_vo.py <run_dir> <vo.mp3> <script.txt> [lang=en]"""
import sys, json, re, difflib, os
from faster_whisper import WhisperModel
run, vo, script = sys.argv[1], sys.argv[2], sys.argv[3]; lang = sys.argv[4] if len(sys.argv) > 4 else "en"
mdl = WhisperModel("small.en" if lang == "en" else "small", compute_type="int8")
segs, _ = mdl.transcribe(vo, language=lang, word_timestamps=True)
words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in (s.words or []) if w.word.strip()]
json.dump(words, open(os.path.join(run, "words_en.json"), "w"), indent=0)
norm = lambda t: re.sub(r"[^a-z0-9' ]", " ", t.lower()).split()
lines = [l.strip() for l in open(script) if l.strip()]
wn = [norm(w["w"])[0] if norm(w["w"]) else "" for w in words]
shots, i = [], 0
for k, line in enumerate(lines):
    lw = norm(line); n = len(lw); best = (0, n)
    for d in range(-2, 3):
        m = n + d
        if m <= 0 or i + m > len(wn): continue
        r = difflib.SequenceMatcher(None, lw, wn[i:i+m]).ratio()
        if r > best[0]: best = (r, m)
    m = best[1]; seg = words[i:i+m]
    shots.append({"id": k+1, "start": seg[0]["s"], "end": seg[-1]["e"], "dur": round(seg[-1]["e"]-seg[0]["s"], 2), "text": line, "match": round(best[0], 2)})
    i += m
json.dump(shots, open(os.path.join(run, "shots_timing.json"), "w"), indent=1, ensure_ascii=False)
for s in shots: print(f'{s["id"]:2d} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["dur"]:4.1f}s) m={s["match"]:.2f} | {s["text"][:70]}')
print("mots non alignés:", len(words)-i, "| fin VO:", words[-1]["e"], "s")
