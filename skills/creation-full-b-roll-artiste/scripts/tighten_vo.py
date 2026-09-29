#!/usr/bin/env python3
"""
tighten_vo.py : resserre une voix off en raccourcissant les silences trop longs.

Optionnel, à lancer AVANT align.py quand l'utilisateur l'active. Tout silence plus long
que --max-pause est ramené à --keep secondes (on garde le début et la fin du silence, on
retire le milieu) ; chaque coupe est adoucie par un micro fondu de 10 ms de chaque côté.
La détection se fait sur l'enveloppe RMS (pas 10 ms) avec un seuil adaptatif.

Sortie : wav PCM 16 bits mono, même fréquence d'échantillonnage que l'entrée.

Exemple :
  python3 scripts/tighten_vo.py voix.mp3 --out work/vo_tight.wav --max-pause 0.5 --keep 0.25
  python3 scripts/align.py work/vo_tight.wav script.txt --out work/words.json
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from broll_common import decode_audio, die, info  # noqa: E402

STEP = 0.01
FADE_S = 0.010


def native_sample_rate(path):
    cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0",
           "-show_entries", "stream=sample_rate", "-of", "csv=p=0", path]
    try:
        out = subprocess.run(cmd, capture_output=True, check=True, text=True).stdout.strip()
        return int(out.splitlines()[0])
    except Exception:  # noqa: BLE001
        return 48000


def silence_runs(x, sr, threshold_db=None):
    hop, win = int(STEP * sr), int(0.02 * sr)
    n = max(1, (len(x) - win) // hop)
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    db = 20 * np.log10(np.sqrt(np.mean(x[idx] ** 2, axis=1)) + 1e-9)
    if threshold_db is None:
        floor, speech = np.percentile(db, 10), np.percentile(db, 80)
        threshold_db = floor + 0.35 * (speech - floor)
    silent = db <= threshold_db
    runs, start = [], None
    for f in range(n):
        if silent[f] and start is None:
            start = f
        elif not silent[f] and start is not None:
            runs.append((start * hop, f * hop))
            start = None
    if start is not None:
        runs.append((start * hop, len(x)))
    return runs, float(threshold_db)


def write_wav(path, x, sr):
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1",
           "-i", "-", "-c:a", "pcm_s16le", path]
    try:
        subprocess.run(cmd, input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        die(f"écriture wav impossible : {e.stderr.decode(errors='replace').strip()}")


def main():
    ap = argparse.ArgumentParser(
        description="Compresse les silences trop longs d'une voix off (à lancer avant align.py).")
    ap.add_argument("audio", help="voix off d'entrée (mp3, wav, m4a...)")
    ap.add_argument("--out", required=True, help="wav de sortie, ex. work/vo_tight.wav")
    ap.add_argument("--max-pause", type=float, default=0.5,
                    help="durée de silence tolérée en secondes (défaut : 0.5)")
    ap.add_argument("--keep", type=float, default=0.25,
                    help="durée conservée pour chaque silence raccourci (défaut : 0.25)")
    ap.add_argument("--threshold-db", type=float, default=None,
                    help="seuil de silence en dBFS (défaut : adaptatif)")
    ap.add_argument("--edges", action="store_true",
                    help="raccourcir aussi le silence de début et de fin (par défaut on les garde)")
    ap.add_argument("--map", default=None,
                    help="fichier JSON optionnel listant les coupes (temps source et temps cible)")
    args = ap.parse_args()

    if not os.path.isfile(args.audio):
        die(f"audio introuvable : {args.audio}")
    if args.keep < 0 or args.max_pause <= 0 or args.keep > args.max_pause:
        die("il faut 0 <= --keep <= --max-pause et --max-pause > 0")

    sr = native_sample_rate(args.audio)
    x, sr = decode_audio(args.audio, sr)
    x = np.array(x, dtype=np.float32, copy=True)  # buffer modifiable pour les fondus
    runs, thr = silence_runs(x, sr, args.threshold_db)
    fade = int(FADE_S * sr)
    ramp_out = np.linspace(1.0, 0.0, fade, dtype=np.float32)
    ramp_in = ramp_out[::-1]

    pieces, cuts = [], []
    pos = 0
    removed = 0
    for (a, b) in runs:
        dur = (b - a) / sr
        if dur <= args.max_pause:
            continue
        if not args.edges and (a == 0 or b >= len(x)):
            continue
        keep = int(args.keep * sr)
        cut_a = a + keep // 2
        cut_b = b - (keep - keep // 2)
        if cut_b - cut_a < fade * 2:
            continue
        seg = x[pos:cut_a].copy()
        if seg.size >= fade:
            seg[-fade:] *= ramp_out
        pieces.append(seg)
        pos = cut_b
        # fondu d'entrée appliqué sur le début du morceau suivant
        x[cut_b:cut_b + fade] *= ramp_in
        cuts.append({"src_start": round(cut_a / sr, 3), "src_end": round(cut_b / sr, 3),
                     "removed_s": round((cut_b - cut_a) / sr, 3),
                     "dst_t": round((sum(p.size for p in pieces)) / sr, 3)})
        removed += cut_b - cut_a
    pieces.append(x[pos:])
    y = np.concatenate(pieces)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    write_wav(args.out, y, sr)
    if args.map:
        with open(args.map, "w", encoding="utf-8") as f:
            json.dump({"src": args.audio, "dst": args.out, "sr": sr, "threshold_db": round(thr, 1),
                       "max_pause_s": args.max_pause, "keep_s": args.keep, "cuts": cuts},
                      f, ensure_ascii=False, indent=1)
    info(f"écrit : {args.out} ({len(x) / sr:.2f} s -> {len(y) / sr:.2f} s, "
         f"{len(cuts)} silences raccourcis, {removed / sr:.2f} s retirées, seuil {thr:.1f} dB)")


if __name__ == "__main__":
    main()
