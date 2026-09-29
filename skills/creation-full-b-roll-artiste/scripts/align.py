#!/usr/bin/env python3
"""
align.py : aligne mot à mot une voix off et son script, produit work/words.json.

Le script est TOUJOURS la vérité du texte : la sortie contient exactement les mots
du script, dans l'ordre, sans trou, avec des timestamps monotones.

Cascade de méthodes (option --method auto) :
  1. ctc  : ctc-forced-aligner (modèle MMS forced aligner, ONNX, CPU). Alignement
            forcé lettre par lettre, très précis, insensible aux mots inconnus
            (noms de marque) puisqu'il n'a pas à reconnaître le texte.
  2. whisper : faster-whisper (modèle Systran, word_timestamps=True) puis
            réconciliation des mots reconnus avec ceux du script par alignement de
            séquences (Needleman-Wunsch sur formes normalisées). Les mots du script
            non appariés reçoivent des timestamps interpolés (score = null).

Exemples :
  python3 scripts/align.py voix.mp3 script.txt --out work/words.json
  python3 scripts/align.py voix.wav script.txt --out work/words.json --method whisper --model medium
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from broll_common import (atoms, audio_duration, convert_to_wav16k, die, info,  # noqa: E402
                          load_script, pronounced_letters, script_hash,
                          set_number_variant, tokenize_script)

MIN_WORD_S = 0.02  # durée minimale attribuée à un mot


# ---------------------------------------------------------------------------
# Méthode 1 : ctc-forced-aligner (ONNX, CPU)
# ---------------------------------------------------------------------------

def align_ctc(wav16k, words, model_path=None):
    """Retourne une liste de (start, end, score|None) alignée sur `words`."""
    import numpy as np
    try:
        import ctc_forced_aligner as cfa
    except ImportError as e:
        raise RuntimeError(f"ctc-forced-aligner non installé ({e})")

    t0 = time.time()
    kwargs = {"model_path": model_path} if model_path else {}
    aligner = cfa.AlignmentSingleton(**kwargs)
    info(f"[ctc] modèle chargé en {time.time() - t0:.1f} s ({aligner.model_path})")

    import soundfile as sf
    audio, sr = sf.read(wav16k, dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if sr != cfa.SAMPLING_FREQ:
        raise RuntimeError(f"le wav doit être à {cfa.SAMPLING_FREQ} Hz (reçu {sr})")

    t1 = time.time()
    emissions, stride_ms = cfa.generate_emissions(aligner.model, audio, batch_size=2)
    info(f"[ctc] émissions calculées en {time.time() - t1:.1f} s "
         f"({emissions.shape[0]} trames, pas {stride_ms} ms)")

    # Tokens prononçables (lettres a-z et apostrophe), un <star> avant chaque mot
    # pour absorber les silences et bruits entre les mots.
    idx_map = []      # index dans words pour chaque token aligné
    tokens = []
    for i, w in enumerate(words):
        pron = pronounced_letters(w["w"])
        if not pron:
            continue
        idx_map.append(i)
        tokens.append("<star>")
        tokens.append(" ".join(pron))
    if not idx_map:
        raise RuntimeError("aucun mot prononçable dans le script")

    segments, scores, blank = cfa.get_alignments(emissions, tokens, aligner.tokenizer)
    spans = cfa.get_spans(tokens, segments, blank)

    result = [None] * len(words)
    for k, tok in enumerate(tokens):
        if tok == "<star>":
            continue
        span = spans[k]
        letters = [s for s in span if s.label != blank and s.label != "<star>"]
        if not letters:
            continue
        f0, f1 = letters[0].start, letters[-1].end + 1
        start = f0 * stride_ms / 1000.0
        end = f1 * stride_ms / 1000.0
        # confiance : probabilité moyenne des trames de lettres (log-prob -> 0..1)
        frame_scores = []
        for s in letters:
            frame_scores.extend(scores[s.start:s.end + 1].tolist())
        conf = float(np.exp(np.mean(frame_scores))) if frame_scores else None
        # tokens = [<star>, mot, <star>, mot, ...] : le mot k correspond à idx_map[k // 2]
        result[idx_map[k // 2]] = (start, end, conf)
    return result, "ctc-forced-aligner"


# ---------------------------------------------------------------------------
# Méthode 2 : faster-whisper + réconciliation avec le script
# ---------------------------------------------------------------------------

def transcribe_whisper(wav16k, model_name, language):
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError(f"faster-whisper non installé ({e})")
    t0 = time.time()
    threads = max(1, os.cpu_count() or 1)
    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=threads)
    info(f"[whisper] modèle {model_name} chargé en {time.time() - t0:.1f} s")
    t1 = time.time()
    segments, _ = model.transcribe(wav16k, language=language, beam_size=5,
                                   word_timestamps=True, vad_filter=False,
                                   condition_on_previous_text=False)
    hyp = []
    for seg in segments:
        for w in seg.words or []:
            hyp.append({"w": w.word.strip(), "start": float(w.start),
                        "end": float(w.end), "p": float(w.probability)})
    info(f"[whisper] transcription en {time.time() - t1:.1f} s, {len(hyp)} mots reconnus")
    # Whisper sépare parfois "c" et "'est" : on recolle les morceaux qui commencent
    # par une apostrophe au mot précédent.
    merged = []
    for h in hyp:
        if merged and h["w"][:1] in ("'", "’") and merged[-1]["w"]:
            merged[-1]["w"] += h["w"]
            merged[-1]["end"] = h["end"]
            merged[-1]["p"] = min(merged[-1]["p"], h["p"])
        else:
            merged.append(h)
    return merged


def _sim(a, b):
    if a == b:
        return 1.0
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio()


def needleman_wunsch(ref, hyp, gap=-0.5, accept=0.6):
    """Alignement global de deux listes d'atomes (chaînes normalisées).

    Score d'appariement = 2*sim - 1 (exact = +1, sim 0,5 = 0). Retourne la liste
    des paires (i_ref, j_hyp) acceptées (sim >= accept).
    """
    import numpy as np
    n, m = len(ref), len(hyp)
    S = np.zeros((n + 1, m + 1), dtype=np.float32)
    S[:, 0] = np.arange(n + 1) * gap
    S[0, :] = np.arange(m + 1) * gap
    sims = np.zeros((n, m), dtype=np.float32)
    for i in range(n):
        for j in range(m):
            sims[i, j] = _sim(ref[i], hyp[j])
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            S[i, j] = max(S[i - 1, j - 1] + 2 * sims[i - 1, j - 1] - 1,
                          S[i - 1, j] + gap, S[i, j - 1] + gap)
    pairs = []
    i, j = n, m
    while i > 0 and j > 0:
        if abs(S[i, j] - (S[i - 1, j - 1] + 2 * sims[i - 1, j - 1] - 1)) < 1e-6:
            if sims[i - 1, j - 1] >= accept:
                pairs.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif abs(S[i, j] - (S[i - 1, j] + gap)) < 1e-6:
            i -= 1
        else:
            j -= 1
    pairs.reverse()
    return pairs


def align_whisper(wav16k, words, model_name, language):
    hyp = transcribe_whisper(wav16k, model_name, language)
    if not hyp:
        raise RuntimeError("whisper n'a reconnu aucun mot")

    # atomes du script
    ref_atoms, ref_owner = [], []
    for i, w in enumerate(words):
        for a in atoms(w["w"]):
            ref_atoms.append(a)
            ref_owner.append(i)
    # atomes de l'hypothèse
    hyp_atoms, hyp_owner = [], []
    for j, h in enumerate(hyp):
        for a in atoms(h["w"]):
            hyp_atoms.append(a)
            hyp_owner.append(j)

    pairs = needleman_wunsch(ref_atoms, hyp_atoms)
    matched = {}
    for ia, ja in pairs:
        i, j = ref_owner[ia], hyp_owner[ja]
        h = hyp[j]
        if i in matched:
            s, e, p = matched[i]
            matched[i] = (min(s, h["start"]), max(e, h["end"]), min(p, h["p"]))
        else:
            matched[i] = (h["start"], h["end"], h["p"])
    n_ok = len(matched)
    info(f"[whisper] {n_ok}/{len(words)} mots du script appariés, "
         f"{len(words) - n_ok} interpolés")
    result = [matched.get(i) for i in range(len(words))]
    return result, "faster-whisper+script"


# ---------------------------------------------------------------------------
# Post-traitement commun : interpolation, monotonie, bornes
# ---------------------------------------------------------------------------

def interpolate_missing(result, words, duration):
    """Complète les mots sans timestamps par interpolation entre voisins appariés.

    L'intervalle disponible est réparti au prorata du nombre de lettres prononcées.
    """
    n = len(words)
    weights = [max(1, len(pronounced_letters(w["w"])) or 1) for w in words]
    out = [list(r) if r else None for r in result]

    # 1. interpolation des trous entre voisins appariés
    i = 0
    while i < n:
        if out[i] is not None:
            i += 1
            continue
        j = i
        while j < n and out[j] is None:
            j += 1
        # intervalle disponible
        left = out[i - 1][1] if i > 0 else 0.0
        right = out[j][0] if j < n else duration
        if right <= left:
            right = left + MIN_WORD_S * (j - i)
        total_w = sum(weights[i:j])
        t = left
        for k in range(i, j):
            d = (right - left) * weights[k] / total_w
            out[k] = [t, t + d, None]
            t += d
        i = j
    return out


def enforce_monotonic(out, duration):
    """Monotonie stricte, durée minimale par mot, bornes de l'audio."""
    n = len(out)
    prev_end = 0.0
    for k in range(n):
        s, e, sc = out[k]
        s = max(s, prev_end)
        e = max(e, s + MIN_WORD_S)
        if k + 1 < n and out[k + 1][2] is not None and out[k + 1][0] < e:
            # on ne mord pas sur un mot suivant bien aligné, sauf si trop court
            e = max(out[k + 1][0], s + MIN_WORD_S)
        out[k] = [s, e, sc]
        prev_end = e
    # dernier ajustement : rien au delà de la durée
    for k in range(n):
        s, e, sc = out[k]
        out[k] = [min(s, duration), min(e, duration), sc]
    return out


def loud_mask(wav16k, step=0.01):
    """Masque parole/silence au pas de 10 ms (enveloppe RMS, seuil adaptatif)."""
    import numpy as np
    from broll_common import decode_audio
    x, sr = decode_audio(wav16k, 16000)
    hop, win = int(step * sr), int(0.02 * sr)
    n = max(1, (len(x) - win) // hop)
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    rms = np.sqrt(np.mean(x[idx] ** 2, axis=1))
    db = 20 * np.log10(rms + 1e-9)
    floor, speech = np.percentile(db, 10), np.percentile(db, 80)
    thr = floor + 0.35 * (speech - floor)
    return db > thr, len(x) / sr


def global_offset(timed, loud, duration, search=0.35, step=0.01, core=0.6):
    """Décalage global (secondes) des timestamps whisper.

    On garde le coeur de chaque mot (60 % central) et on cherche le décalage qui
    maximise la proportion de parole (masque d'énergie) à l'intérieur de ces coeurs.
    Les mots en pleine phrase ne discriminent pas, ceux qui bordent une pause tirent
    le décalage vers la vraie position. Corrige le biais systématique de whisper
    (large-v3 place les mots 150 à 300 ms trop tôt, surtout après une pause).
    Retourne (décalage, gain de score par rapport à zéro).
    """
    import numpy as np
    n = len(loud)
    lf = loud.astype(np.float32)
    cum = np.concatenate([[0.0], np.cumsum(lf)])
    best, best_score, score_zero = 0.0, -1e9, 0.0
    for k in range(-int(search / step), int(search / step) + 1):
        tot, cnt = 0.0, 0
        for s_, e_, _ in timed:
            c, d = (s_ + e_) / 2 + k * step, (e_ - s_) * core
            f0 = int((c - d / 2) / step)
            f1 = max(int((c + d / 2) / step), f0 + 1)
            if f0 < 0 or f1 > n:
                continue
            tot += (cum[f1] - cum[f0]) / (f1 - f0)
            cnt += 1
        if k == 0 and cnt:
            score_zero = tot / cnt
        if cnt and tot / cnt > best_score + 1e-9:
            best, best_score = k * step, tot / cnt
    # gain par rapport à l'absence de décalage : sous 0,05 le biais n'est pas systématique
    # (erreurs mot à mot que le recalage local corrige mieux qu'un décalage global)
    return float(round(best, 3)), float(best_score - score_zero)


def snap_to_energy(timed, wav16k, max_shift=0.15, max_extend=0.06, shared_window=0.08):
    """Recale les frontières de mots sur l'enveloppe d'énergie (pas 10 ms).

    Deux cas par frontière entre mots voisins :
      - frontière partagée (les mots se touchent) : si un silence d'au moins 40 ms
        existe à moins de shared_window, la fin du mot précédent est posée au début du
        silence et le début du mot suivant à sa fin. Sinon rien ne bouge.
      - frontière avec trou : chaque bord est étendu tant que le signal est fort
        (au plus max_extend, pour ne pas avaler la consonne douce du mot suivant),
        ou rétréci tant qu'il est silencieux (au plus max_shift), sans toucher le voisin.
    Surtout utile pour whisper, qui colle les mots entre eux sans respecter les
    pauses ; presque neutre pour ctc, déjà précis à 20 ms.
    """
    step = 0.01
    loud, last_hi = loud_mask(wav16k, step)
    n = len(loud)

    def is_loud(t):
        f = int(round(t / step))
        return bool(loud[min(max(f, 0), n - 1)])

    def extend_fwd(t, hi):
        while t + step <= hi and is_loud(t):
            t += step
        return t

    def shrink_back(t, lo):
        while t - step >= lo and not is_loud(t - step):
            t -= step
        return t

    def shrink_fwd(t, hi):
        while t + step <= hi and not is_loud(t):
            t += step
        return t

    def extend_back(t, lo):
        while t - step >= lo and is_loud(t - step):
            t -= step
        return t

    out = [list(t) for t in timed]
    m = len(out)
    # premier début et dernière fin
    out[0][0] = extend_back(out[0][0], max(0.0, out[0][0] - max_extend)) if is_loud(out[0][0]) \
        else shrink_fwd(out[0][0], min(out[0][1] - MIN_WORD_S, out[0][0] + max_shift))
    out[-1][1] = extend_fwd(out[-1][1], min(last_hi, out[-1][1] + max_extend)) if is_loud(out[-1][1] - step) \
        else shrink_back(out[-1][1], max(out[-1][0] + MIN_WORD_S, out[-1][1] - max_shift))

    for k in range(m - 1):
        e, s2 = out[k][1], out[k + 1][0]
        lo = max(out[k][0] + MIN_WORD_S, min(e, s2) - max_shift)
        hi = min(out[k + 1][1] - MIN_WORD_S, max(e, s2) + max_shift)
        if hi <= lo:
            continue
        if s2 - e < 0.03:
            # frontière partagée : on cherche le plus long silence tout proche
            # (fenêtre serrée, sinon on risque d'attraper la pause d'un autre mot)
            b = (e + s2) / 2
            lo2, hi2 = max(lo, b - shared_window), min(hi, b + shared_window)
            f0, f1 = int(round(lo2 / step)), int(round(hi2 / step))
            best, run_start, cur = None, None, 0
            for f in range(f0, min(f1, n) + 1):
                if f < n and not loud[f]:
                    if cur == 0:
                        run_start = f
                    cur += 1
                    if best is None or cur > best[1]:
                        best = (run_start, cur)
                else:
                    cur = 0
            if best and best[1] >= 4:
                out[k][1] = best[0] * step
                out[k + 1][0] = (best[0] + best[1]) * step
        else:
            # trou : chaque bord se cale sur le signal
            if is_loud(e - step):
                e = extend_fwd(e, min(s2, e + max_extend))
            else:
                e = shrink_back(e, lo)
            if is_loud(s2):
                s2 = extend_back(s2, max(e, s2 - max_extend))
            else:
                s2 = shrink_fwd(s2, hi)
            out[k][1], out[k + 1][0] = e, s2
    return [[round(s, 3), round(e, 3), sc] for s, e, sc in out]


def build_output(audio_arg, duration, language, method, words, timed):
    return {
        "audio": audio_arg,
        "duration_s": round(duration, 3),
        "language": language,
        "method": method,
        "script_hash": script_hash(words),
        "words": [
            {"i": i, "w": w["w"], "start": round(t[0], 3), "end": round(t[1], 3),
             "score": (round(t[2], 3) if t[2] is not None else None),
             "punct_after": w["punct_after"]}
            for i, (w, t) in enumerate(zip(words, timed))
        ],
    }


def check_output(data, words):
    """Vérifications finales : mots identiques, ordre, monotonie, bornes."""
    ws = data["words"]
    if [w["w"] for w in ws] != [w["w"] for w in words]:
        die("incohérence interne : les mots de sortie diffèrent du script")
    prev = 0.0
    for w in ws:
        if w["start"] < prev - 1e-6 or w["end"] < w["start"]:
            die(f"timestamps non monotones au mot {w['i']} ({w['w']})")
        prev = w["end"]
    if ws and ws[-1]["end"] > data["duration_s"] + 1e-6:
        die("un mot dépasse la durée de l'audio")


def main():
    ap = argparse.ArgumentParser(
        description="Aligne une voix off française et son script mot à mot (words.json).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Méthodes : auto (ctc puis whisper en secours), ctc (ctc-forced-aligner), "
                "whisper (faster-whisper + réconciliation avec le script).\n"
                "Le wav 16 kHz intermédiaire est écrit dans le dossier de --out."))
    ap.add_argument("audio", help="voix off (mp3, wav, m4a...)")
    ap.add_argument("script", help="script texte UTF-8 (vérité du texte)")
    ap.add_argument("--out", required=True, help="fichier de sortie, ex. work/words.json")
    ap.add_argument("--method", choices=["auto", "ctc", "whisper"], default="auto")
    ap.add_argument("--model", choices=["small", "medium", "large-v3"], default="small",
                    help="taille du modèle faster-whisper (défaut : small)")
    ap.add_argument("--language", default="fr", help="code langue ISO 639-1 (défaut : fr)")
    ap.add_argument("--numbers", choices=["fr", "be"], default="fr",
                    help="prononciation des nombres pour ctc : fr (soixante-dix) ou be (septante, nonante)")
    ap.add_argument("--no-snap", action="store_true",
                    help="ne pas recaler les frontières de mots sur l'énergie du signal")
    ap.add_argument("--ctc-model", default=None,
                    help="chemin du modèle ONNX ctc-forced-aligner (défaut : ~/ctc_forced_aligner/model.onnx)")
    args = ap.parse_args()

    if not os.path.isfile(args.audio):
        die(f"audio introuvable : {args.audio}")
    if not os.path.isfile(args.script):
        die(f"script introuvable : {args.script}")

    set_number_variant(args.numbers)
    words = tokenize_script(load_script(args.script))
    if not words:
        die("le script ne contient aucun mot")
    info(f"script : {len(words)} mots")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.audio))[0]
    wav16k = os.path.join(out_dir, f"{stem}_16k.wav")
    t0 = time.time()
    convert_to_wav16k(args.audio, wav16k)
    duration = audio_duration(wav16k)
    info(f"audio : {duration:.3f} s, wav 16 kHz écrit en {time.time() - t0:.1f} s ({wav16k})")

    result, method = None, None
    errors = []
    order = {"auto": ["ctc", "whisper"], "ctc": ["ctc"], "whisper": ["whisper"]}[args.method]
    for m in order:
        t1 = time.time()
        try:
            if m == "ctc":
                result, method = align_ctc(wav16k, words, args.ctc_model)
            else:
                result, method = align_whisper(wav16k, words, args.model, args.language)
            info(f"[{m}] alignement terminé en {time.time() - t1:.1f} s")
            break
        except Exception as e:  # noqa: BLE001
            errors.append(f"{m} : {e}")
            info(f"[{m}] échec : {e}")
    if result is None:
        die("aucune méthode d'alignement n'a abouti :\n  " + "\n  ".join(errors))

    n_missing = sum(1 for r in result if r is None)
    if n_missing:
        info(f"{n_missing} mot(s) sans timestamps direct, interpolés")
    timed = interpolate_missing(result, words, duration)
    if not args.no_snap:
        if method.startswith("faster-whisper"):
            loud, _ = loud_mask(wav16k)
            off, gain = global_offset(timed, loud, duration)
            if abs(off) >= 0.02 and gain >= 0.05:
                info(f"[whisper] décalage global des timestamps corrigé de {off * 1000:+.0f} ms "
                     f"(gain {gain:.3f})")
                timed = [[max(0.0, s_ + off), min(duration, e_ + off), sc] for s_, e_, sc in timed]
        timed = snap_to_energy(timed, wav16k)
    timed = enforce_monotonic(timed, duration)
    data = build_output(args.audio, duration, args.language, method, words, timed)
    check_output(data, words)
    # mots très mal alignés : souvent des mots du script absents de l'audio (ou l'inverse)
    weak = [w for w in data["words"] if w["score"] is not None and w["score"] < 0.05]
    if len(weak) >= 3:
        preview = ", ".join(f'{w["w"]} ({w["start"]:.2f}s)' for w in weak[:12])
        info(f"attention : {len(weak)} mot(s) avec un score < 0.05, vérifier que le script "
             f"correspond bien à la voix : {preview}{' ...' if len(weak) > 12 else ''}")
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    info(f"écrit : {args.out} ({len(words)} mots, méthode {method}, total {time.time() - t0:.1f} s)")


if __name__ == "__main__":
    main()
