#!/usr/bin/env python3
"""Transcription mot par mot avec horodatage (faster-whisper).
Usage : python3 transcrire.py voix.mp3 [--langue fr] [--modele small|medium] [--sortie dossier]
Sorties : mots.json  [{"w": mot, "s": début, "e": fin}]  +  transcription.txt (phrases minutées)
Installation si absent : pip install faster-whisper --break-system-packages
"""
import argparse, json, os, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("audio")
ap.add_argument("--langue", default=None, help="fr, en... (auto si absent)")
ap.add_argument("--modele", default="small")
ap.add_argument("--sortie", default=".")
a = ap.parse_args()

from faster_whisper import WhisperModel

dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.audio]).decode().strip())
m = WhisperModel(a.modele, device="cpu", compute_type="int8")
segs, info = m.transcribe(a.audio, language=a.langue, word_timestamps=True, vad_filter=False)
mots, lignes = [], []
for s in segs:
    lignes.append(f"{s.start:7.2f} -> {s.end:7.2f}  {s.text.strip()}")
    for w in s.words:
        mots.append({"w": w.word.strip(), "s": round(float(w.start), 3), "e": round(float(w.end), 3)})
os.makedirs(a.sortie, exist_ok=True)
json.dump(mots, open(os.path.join(a.sortie, "mots.json"), "w"), ensure_ascii=False, indent=0)
open(os.path.join(a.sortie, "transcription.txt"), "w").write("\n".join(lignes) + "\n")
pauses = [(round(float(x["e"]), 2), round(float(y["s"]), 2)) for x, y in zip(mots, mots[1:]) if y["s"] - x["e"] >= 0.3]
print(f"Langue : {info.language}  |  Durée audio : {dur:.2f} s  |  Mots : {len(mots)}  |  Débit : {len(mots) / dur * 60:.0f} mots/min")
print(f"Pauses >= 0,3 s : {len(pauses)}  {pauses[:20]}")
