#!/usr/bin/env python3
"""Calage MMS (préféré par le studio) : découpe les mots alignés par ctc-forced-aligner ligne par ligne -> shots_timing.json.
   1) python3 skills/creation-full-b-roll-artiste/scripts/align.py VO.mp3 SCRIPT-FR-tts.txt --out mots_mms.json --method ctc --language fr
   2) align_vo_mms.py <run_dir> mots_mms.json SCRIPT-FR.txt
   Même format de sortie que align_vo.py (Whisper) : [{"id","start","end","dur","text","match"}]."""
import json, os, re, sys
run, words_p, script = sys.argv[1], sys.argv[2], sys.argv[3]
words = json.load(open(os.path.join(run, words_p) if not os.path.isabs(words_p) else words_p))["words"]
lines = [l.strip() for l in open(os.path.join(run, script) if not os.path.isabs(script) else script) if l.strip()]
tok = lambda t: [x for x in t.split() if re.search(r"\w", x)]
n_script = sum(len(tok(l)) for l in lines)
if n_script != len(words): raise SystemExit(f"le script ({n_script} mots) ne correspond pas à l'alignement ({len(words)} mots)")
shots, i = [], 0
for k, line in enumerate(lines):
    n = len(tok(line)); seg = words[i:i + n]; i += n
    low = [w["w"] for w in seg if w.get("score", 1) < 0.05]
    shots.append({"id": k + 1, "start": seg[0]["start"], "end": seg[-1]["end"], "dur": round(seg[-1]["end"] - seg[0]["start"], 2),
                  "text": line, "match": 1.0, "mots_faibles": low})
json.dump(shots, open(os.path.join(run, "shots_timing.json"), "w"), indent=1, ensure_ascii=False)
for s in shots: print(f'{s["id"]:2d} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["dur"]:4.1f}s) | {s["text"][:70]}' + (f'  [faible: {", ".join(s["mots_faibles"])}]' if s["mots_faibles"] else ""))
print("mots non alignés: 0 | fin VO:", words[-1]["end"], "s")
