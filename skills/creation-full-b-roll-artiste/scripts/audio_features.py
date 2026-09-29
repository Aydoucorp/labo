#!/usr/bin/env python3
"""
audio_features.py : mesures acoustiques de la voix off, produit work/features.json.

Entrées : l'audio (mp3, wav, m4a...) et work/words.json (sortie de align.py).
Sorties (contrat section 2) :
  - pauses        : silences >= 0.18 s entre deux mots, avec after_word_i (mot qui précède)
  - emphasis      : mots appuyés, énergie RMS du mot > moyenne locale glissante + 1,5 écart-type
                    (champ z ; t = instant du pic d'énergie dans le mot)
  - energy        : enveloppe RMS en dB, pas 0,05 s (forme d'onde du brief HTML)
  - loudness_lufs : loudness intégrée (ffmpeg loudnorm, sinon pyloudnorm)
  - speech_rate_wps : débit en mots par seconde (du premier au dernier mot)

Exemple :
  python3 scripts/audio_features.py voix.mp3 work/words.json --out work/features.json
"""

import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from broll_common import decode_audio, die, info  # noqa: E402

SR = 16000
STEP = 0.01  # pas d'analyse fin (10 ms) pour les silences et les pics


def rms_db_envelope(x, sr, hop_s, win_s):
    hop, win = int(hop_s * sr), int(win_s * sr)
    if len(x) < win:
        x = np.pad(x, (0, win - len(x)))
    n = 1 + (len(x) - win) // hop
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    rms = np.sqrt(np.mean(x[idx] ** 2, axis=1))
    return 20 * np.log10(rms + 1e-9)


def silence_mask(db):
    """Seuil adaptatif : plancher (p10) + 35 % de l'écart au niveau de parole (p80)."""
    floor, speech = np.percentile(db, 10), np.percentile(db, 80)
    thr = floor + 0.35 * (speech - floor)
    return db <= thr, float(thr)


def longest_silent_run(silent, f0, f1):
    """Plus longue suite de trames silencieuses dans [f0, f1). Retourne (debut, longueur)."""
    best, cur, start = (None, 0), 0, None
    for f in range(max(0, f0), min(f1, len(silent))):
        if silent[f]:
            if cur == 0:
                start = f
            cur += 1
            if cur > best[1]:
                best = (start, cur)
        else:
            cur = 0
    return best


def detect_pauses(words, silent, pause_min):
    """Pour chaque paire de mots voisins, cherche le plus long silence entre le début
    du premier et la fin du second (robuste aux frontières ASR approximatives)."""
    pauses, seen = [], set()
    for i in range(len(words) - 1):
        f0 = int(round(words[i]["start"] / STEP))
        f1 = int(round(words[i + 1]["end"] / STEP))
        start, length = longest_silent_run(silent, f0, f1)
        if start is None or length * STEP < pause_min:
            continue
        key = (start, length)
        if key in seen:
            continue
        seen.add(key)
        ps, pe = start * STEP, (start + length) * STEP
        # le mot qui précède la pause : dernier mot commençant avant le milieu du silence
        mid = (ps + pe) / 2
        after = max((k for k, w in enumerate(words) if w["start"] < mid), default=i)
        pauses.append({"start": round(ps, 3), "end": round(pe, 3),
                       "dur": round(pe - ps, 3), "after_word_i": after})
    pauses.sort(key=lambda p: p["start"])
    return pauses


def word_energy(x, sr, words):
    """Énergie RMS (dB) de chaque mot et instant du pic (fenêtre 30 ms)."""
    e_db, t_peak = [], []
    win = int(0.03 * sr)
    for w in words:
        a, b = int(w["start"] * sr), max(int(w["end"] * sr), int(w["start"] * sr) + win)
        seg = x[a:b]
        if seg.size == 0:
            e_db.append(-90.0)
            t_peak.append(w["start"])
            continue
        e_db.append(float(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)))
        if seg.size > win:
            frames = np.lib.stride_tricks.sliding_window_view(seg, win)[::win // 3]
            k = int(np.argmax(np.mean(frames ** 2, axis=1)))
            t_peak.append(w["start"] + (k * (win // 3) + win / 2) / sr)
        else:
            t_peak.append((w["start"] + w["end"]) / 2)
    return np.array(e_db), t_peak


def detect_emphasis(words, e_db, t_peak, half_window=7, z_min=1.5, min_dur=0.12):
    """z-score de l'énergie du mot par rapport à ses voisins (fenêtre glissante centrée).

    Les mots très courts (articles, liaisons) sont ignorés : leur énergie est peu fiable.
    """
    n = len(words)
    valid = np.array([(w["end"] - w["start"]) >= min_dur for w in words])
    out = []
    for i in range(n):
        if not valid[i]:
            continue
        lo, hi = max(0, i - half_window), min(n, i + half_window + 1)
        neigh = e_db[lo:hi][valid[lo:hi]]
        if neigh.size < 4:
            continue
        mu, sd = float(np.mean(neigh)), float(np.std(neigh))
        if sd < 0.5:
            sd = 0.5  # évite les z explosifs sur une voix très plate
        z = (e_db[i] - mu) / sd
        if z > z_min:
            out.append({"word_i": i, "t": round(t_peak[i], 3), "z": round(float(z), 2)})
    return out


def loudness_lufs(audio_path, x, sr):
    """Loudness intégrée via ffmpeg loudnorm (JSON), sinon pyloudnorm, sinon null."""
    cmd = ["ffmpeg", "-v", "info", "-nostdin", "-i", audio_path,
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]
    try:
        err = subprocess.run(cmd, capture_output=True, text=True).stderr
        m = re.search(r"\{.*?\}", err, re.S)
        if m:
            val = json.loads(m.group(0)).get("input_i")
            if val is not None and val not in ("-inf", "inf"):
                return round(float(val), 1)
    except Exception as e:  # noqa: BLE001
        info(f"loudnorm ffmpeg indisponible : {e}")
    try:
        import pyloudnorm as pyln
        meter = pyln.Meter(sr)
        return round(float(meter.integrated_loudness(x.astype(np.float64))), 1)
    except Exception as e:  # noqa: BLE001
        info(f"pyloudnorm indisponible : {e}")
    return None


def main():
    ap = argparse.ArgumentParser(
        description="Extrait pauses, mots appuyés, enveloppe RMS, loudness et débit (features.json).")
    ap.add_argument("audio", help="voix off (même fichier que pour align.py)")
    ap.add_argument("words", help="work/words.json produit par align.py")
    ap.add_argument("--out", required=True, help="fichier de sortie, ex. work/features.json")
    ap.add_argument("--pause-min", type=float, default=0.18,
                    help="durée minimale d'une pause en secondes (défaut : 0.18)")
    ap.add_argument("--hop", type=float, default=0.05,
                    help="pas de l'enveloppe RMS en secondes (défaut : 0.05)")
    args = ap.parse_args()

    if not os.path.isfile(args.audio):
        die(f"audio introuvable : {args.audio}")
    try:
        with open(args.words, "r", encoding="utf-8") as f:
            wdata = json.load(f)
    except (OSError, ValueError) as e:
        die(f"words.json illisible : {e}")
    words = wdata.get("words") or []
    if not words:
        die("words.json ne contient aucun mot")

    x, sr = decode_audio(args.audio, SR)
    duration = len(x) / sr
    if abs(duration - float(wdata.get("duration_s", duration))) > 0.5:
        info(f"attention : durée audio {duration:.2f} s différente de words.json "
             f"({wdata.get('duration_s')}) ; l'audio n'est peut-être pas le bon")

    # enveloppe fine pour les silences, enveloppe 50 ms pour le HTML
    fine_db = rms_db_envelope(x, sr, STEP, 0.02)
    silent, thr = silence_mask(fine_db)
    env_db = rms_db_envelope(x, sr, args.hop, args.hop)

    pauses = detect_pauses(words, silent, args.pause_min)
    e_db, t_peak = word_energy(x, sr, words)
    emphasis = detect_emphasis(words, e_db, t_peak)

    span = words[-1]["end"] - words[0]["start"]
    rate = round(len(words) / span, 2) if span > 0 else None

    features = {
        "duration_s": round(duration, 3),
        "loudness_lufs": loudness_lufs(args.audio, x, sr),
        "pauses": pauses,
        "emphasis": emphasis,
        "energy": {"hop_s": args.hop, "rms_db": [round(float(v), 1) for v in env_db]},
        "speech_rate_wps": rate,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(features, f, ensure_ascii=False, indent=1)
    info(f"écrit : {args.out} ({len(pauses)} pauses, {len(emphasis)} mots appuyés, "
         f"loudness {features['loudness_lufs']} LUFS, débit {rate} mots/s, seuil silence {thr:.1f} dB)")


if __name__ == "__main__":
    main()
