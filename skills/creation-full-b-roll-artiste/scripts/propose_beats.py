#!/usr/bin/env python3
"""
propose_beats.py : découpe mécanique de la voix off en beats, produit work/beats_draft.json.

Entrées : work/words.json (align.py), work/features.json (audio_features.py), un profil
(ADS ou EDU) lu dans assets/profiles.json.

Règles :
  - une frontière de beat est toujours une frontière de mot ;
  - candidats de coupe : ponctuation forte (. ! ? : ...), pause >= pause_min_s, virgule
    avec pause, connecteur en début de proposition (mais, parce que, et là, donc, alors,
    résultat, sauf que, en fait) ; une virgule seule est un candidat faible ;
  - les beats sont assemblés par programmation dynamique : la durée vise
    shot.default.target du profil et reste entre min et max quand c'est possible ;
    une coupe hors candidat n'est prise que pour éviter un beat beaucoup trop long
    (cut_reason "duree_max") ;
  - les beats qui commencent dans les 2 premières secondes (hook) utilisent les bornes
    shot.HOOK du profil ;
  - un beat plus long que max reçoit suggested_split : liste des instants (secondes) des
    sous-frontières proposées, pour en faire une séquence de 2 ou 3 plans ;
  - energy (1 à 5) combine le z-score du RMS moyen du beat et celui du débit local ;
  - la coupe est posée juste avant le mot suivant : max(fin du mot, début du suivant - 0,08 s).

Exemple :
  python3 scripts/propose_beats.py work/words.json work/features.json --profile ADS --out work/beats_draft.json
"""

import argparse
import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from broll_common import die, info, load_profiles, normalize_word  # noqa: E402

HOOK_WINDOW_S = 2.0
CUT_LEAD_S = 0.08
STRONG_PUNCT = {".", "!", "?", ":", "..."}
CONNECTORS_1 = {"mais", "donc", "alors", "resultat", "bref", "pourtant", "sinon"}
CONNECTORS_2 = {("parce", "que"), ("et", "la"), ("sauf", "que"), ("en", "fait"),
                ("du", "coup"), ("en", "plus"), ("c'est", "pourquoi")}

# Coûts de la programmation dynamique
CUT_COST_NONE = 6.0       # coupe hors candidat (uniquement pour éviter un beat trop long)
STRONG_SCORE = 5.0        # à partir de ce score, une frontière est "forte" (fin de phrase + pause)
CROSS_STRONG_COST = 3.0   # pénalité par frontière forte enjambée à l'intérieur d'un beat
OVER_MAX_PER_S = 3.0      # pénalité par seconde au delà de max
UNDER_MIN_PER_S = 5.0     # pénalité par seconde en dessous de min
OUT_OF_RANGE = 1.0        # coût fixe dès qu'on sort de [min, max]
TARGET_WEIGHT = 2.0       # poids de l'écart à la cible dans [min, max]

# Une coupe forcée (hors candidat) n'est jamais posée après ces mots outils, ni devant
# un symbole ("97 | %"), ni entre un nombre et son unité.
NO_CUT_AFTER = {"le", "la", "les", "l'", "un", "une", "des", "de", "du", "d'", "a", "au", "aux",
                "en", "dans", "sur", "sous", "pour", "par", "avec", "sans", "et", "ou", "ni",
                "qui", "que", "qu'", "ce", "cet", "cette", "ces", "c'est", "ta", "ton", "tes",
                "ma", "mon", "mes", "sa", "son", "ses", "notre", "votre", "leur", "nos", "vos",
                "leurs", "ne", "n'", "pas", "plus", "tres", "tout", "toute", "tous", "toutes",
                "si", "comme", "chez", "vers", "entre", "je", "tu", "il", "elle", "on", "nous",
                "vous", "ils", "elles", "se", "s'", "me", "te", "y"}
SYMBOLS = {"%", "€", "$", "£"}


def default_profiles_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "assets", "profiles.json")


def load_json(path, label):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        die(f"{label} illisible : {e}")


def candidate_scores(words, pauses):
    """Score et raison de coupe pour chaque frontière après le mot i (i de 0 à n-2)."""
    n = len(words)
    pause_after = {p["after_word_i"]: p["dur"] for p in pauses}
    norm = [normalize_word(w["w"]) for w in words]
    scores, reasons = [0.0] * (n - 1), [""] * (n - 1)
    for i in range(n - 1):
        punct = words[i]["punct_after"]
        pause = pause_after.get(i, 0.0)
        s, parts = 0.0, []
        if punct in STRONG_PUNCT:
            s += 3.0
            parts.append("ponctuation")
        elif punct == ",":
            s += 1.0 if pause == 0 else 1.5
            parts.append("ponctuation")
        if pause > 0:
            s += 2.0 + min(1.5, pause / 0.3)
            parts.insert(0, "pause")
        nxt = norm[i + 1]
        nxt2 = norm[i + 2] if i + 2 < n else ""
        if nxt in CONNECTORS_1 or (nxt, nxt2) in CONNECTORS_2:
            s += 1.5
            parts.append("connecteur")
        scores[i] = s
        if not parts:
            reasons[i] = ""
        elif "pause" in parts and "ponctuation" in parts:
            reasons[i] = "pause+ponctuation"
        elif "pause" in parts:
            reasons[i] = "pause"
        elif "ponctuation" in parts:
            reasons[i] = "ponctuation"
        else:
            reasons[i] = "connecteur"
    return scores, reasons


def cut_time(words, i, duration):
    """Instant de coupe après le mot i : juste avant le mot suivant."""
    if i >= len(words) - 1:
        return duration
    return max(words[i]["end"], words[i + 1]["start"] - CUT_LEAD_S)


def bounds_for(profile, start_t):
    key = "HOOK" if start_t < HOOK_WINDOW_S else "default"
    b = profile["shot"][key]
    return b["min"], b["target"], b["max"]


def duration_cost(dur, lo, target, hi):
    if dur < lo:
        return UNDER_MIN_PER_S * (lo - dur) + OUT_OF_RANGE
    if dur > hi:
        return OVER_MAX_PER_S * (dur - hi) + OUT_OF_RANGE
    span = max(hi - lo, 0.1)
    return TARGET_WEIGHT * ((dur - target) / span) ** 2


def forced_cut_allowed(words, i):
    """Une coupe hors candidat après le mot i est-elle acceptable ?"""
    prev, nxt = normalize_word(words[i]["w"]), normalize_word(words[i + 1]["w"])
    if prev in NO_CUT_AFTER or nxt in SYMBOLS:
        return False
    if prev.replace(",", "").isdigit():
        return False  # "200 | foyers", "3 | secondes"
    return True


def segment(words, scores, profile, duration):
    """Programmation dynamique : dp[j] = meilleur coût pour couvrir les mots 0..j-1."""
    n = len(words)
    forced_ok = [forced_cut_allowed(words, i) for i in range(n - 1)]
    starts = [0.0] + [cut_time(words, i, duration) for i in range(n - 1)]
    ends = [cut_time(words, i, duration) for i in range(n)]
    INF = float("inf")
    # nombre cumulé de frontières fortes avant la frontière i (pour pénaliser les enjambements)
    strong_prefix = [0] * n
    for i in range(1, n):
        strong_prefix[i] = strong_prefix[i - 1] + (1 if scores[i - 1] >= STRONG_SCORE else 0)
    dp, prev = [INF] * (n + 1), [-1] * (n + 1)
    dp[0] = 0.0
    for j in range(1, n + 1):
        end_t = ends[j - 1]
        for i in range(0, j):
            if dp[i] == INF:
                continue
            start_t = starts[i]
            dur = end_t - start_t
            lo, target, hi = bounds_for(profile, start_t)
            if dur > 3 * hi and j - i > 1:
                # inutile d'explorer des beats gigantesques
                continue
            if j < n:
                sc = scores[j - 1]
                if sc <= 0:
                    if not forced_ok[j - 1]:
                        continue
                    cut_c = CUT_COST_NONE
                else:
                    cut_c = max(0.0, 6.0 - sc) * 0.6
            else:
                cut_c = 0.0
            crossed = strong_prefix[j - 1] - strong_prefix[i]
            c = dp[i] + duration_cost(dur, lo, target, hi) + cut_c + CROSS_STRONG_COST * crossed
            if c < dp[j]:
                dp[j], prev[j] = c, i
    # reconstruction
    cuts, j = [], n
    while j > 0:
        cuts.append((prev[j], j - 1))
        j = prev[j]
    cuts.reverse()
    return cuts, starts, ends


def suggested_split(words, wf, wt, scores, start_t, end_t, hi):
    """Sous-frontières pour un beat trop long : 2 plans si <= 2*max, sinon 3.

    On choisit les frontières internes qui maximisent le score de candidat tout en
    restant proches d'un découpage régulier et au dessus de la durée min possible.
    """
    dur = end_t - start_t
    k = 2 if dur <= 2 * hi else 3
    # frontière après le mot i, i dans [wf, wt-1] ; on écarte les coupes contre nature
    internal = [i for i in range(wf, wt) if scores[i] > 0 or forced_cut_allowed(words, i)]
    if len(internal) < k - 1:
        return None
    best, best_score = None, -1e9
    ideal = [start_t + dur * m / k for m in range(1, k)]
    for combo in itertools.combinations(internal, k - 1):
        ts = [cut_time(words, i, end_t) for i in combo]
        pieces = [a - b for a, b in zip(ts + [end_t], [start_t] + ts)]
        if min(pieces) < 0.6:
            continue
        s = sum(scores[i] for i in combo) - sum(abs(t - g) for t, g in zip(ts, ideal)) * 1.5
        if max(pieces) > hi:
            s -= (max(pieces) - hi) * 2
        if s > best_score:
            best, best_score = ts, s
    return [round(t, 3) for t in best] if best else None


def energy_levels(beats, words, features):
    """Niveau 1 à 5 à partir du RMS moyen du beat et du débit local (z-scores combinés)."""
    env = np.array(features["energy"]["rms_db"], dtype=float)
    hop = float(features["energy"]["hop_s"])
    rms_vals, rate_vals = [], []
    for b in beats:
        f0, f1 = int(b["start"] / hop), max(int(b["end"] / hop), int(b["start"] / hop) + 1)
        seg = env[f0:f1]
        seg = seg[seg > -60] if np.any(seg > -60) else seg
        rms_vals.append(float(np.mean(seg)) if seg.size else -60.0)
        n_words = b["word_to"] - b["word_from"] + 1
        spoken = words[b["word_to"]]["end"] - words[b["word_from"]]["start"]
        rate_vals.append(n_words / max(spoken, 0.2))
    rms_vals, rate_vals = np.array(rms_vals), np.array(rate_vals)

    def z(v):
        sd = float(np.std(v))
        return (v - np.mean(v)) / sd if sd > 1e-6 else np.zeros_like(v)

    combined = 0.6 * z(rms_vals) + 0.4 * z(rate_vals)
    levels = []
    for c in combined:
        if c < -1.0:
            levels.append(1)
        elif c < -0.33:
            levels.append(2)
        elif c < 0.33:
            levels.append(3)
        elif c < 1.0:
            levels.append(4)
        else:
            levels.append(5)
    return levels


def beat_text(words, wf, wt):
    return " ".join(w["w"] + w["punct_after"] for w in words[wf:wt + 1])


def main():
    ap = argparse.ArgumentParser(
        description="Propose une segmentation mécanique en beats à partir de words.json et features.json.")
    ap.add_argument("words", help="work/words.json")
    ap.add_argument("features", help="work/features.json")
    ap.add_argument("--profile", required=True, choices=["ADS", "EDU"])
    ap.add_argument("--out", required=True, help="fichier de sortie, ex. work/beats_draft.json")
    ap.add_argument("--profiles", default=default_profiles_path(),
                    help="chemin de profiles.json (défaut : assets/profiles.json à côté des scripts)")
    args = ap.parse_args()

    wdata = load_json(args.words, "words.json")
    features = load_json(args.features, "features.json")
    profiles = load_profiles(args.profiles)
    if args.profile not in profiles:
        die(f"profil {args.profile} absent de {args.profiles}")
    profile = profiles[args.profile]
    words = wdata.get("words") or []
    if not words:
        die("words.json ne contient aucun mot")
    duration = float(wdata.get("duration_s") or features.get("duration_s") or words[-1]["end"])
    pauses = [p for p in features.get("pauses", []) if p["dur"] >= profile.get("pause_min_s", 0.18)]

    scores, reasons = candidate_scores(words, pauses)
    cuts, starts, ends = segment(words, scores, profile, duration)

    beats = []
    for k, (wf, wt) in enumerate(cuts):
        start_t = 0.0 if k == 0 else beats[-1]["end"]
        end_t = duration if k == len(cuts) - 1 else ends[wt]
        lo, target, hi = bounds_for(profile, start_t)
        if k == len(cuts) - 1:
            reason = reasons[wt] if wt < len(reasons) and reasons[wt] else "ponctuation"
            if words[wt]["punct_after"] in STRONG_PUNCT or words[wt]["punct_after"] == ",":
                reason = "ponctuation"
        else:
            reason = reasons[wt] or "duree_max"
        split = suggested_split(words, wf, wt, scores, start_t, end_t, hi) if end_t - start_t > hi else None
        beats.append({
            "id": f"{k + 1:02d}",
            "start": round(start_t, 3), "end": round(end_t, 3),
            "word_from": wf, "word_to": wt,
            "text": beat_text(words, wf, wt),
            "cut_reason": reason,
            "energy": 3,
            "suggested_split": split,
        })
    for b, lvl in zip(beats, energy_levels(beats, words, features)):
        b["energy"] = lvl

    # contrôles
    for a, b in zip(beats, beats[1:]):
        if abs(a["end"] - b["start"]) > 1e-6 or a["word_to"] + 1 != b["word_from"]:
            die("incohérence interne : beats non contigus")
    if beats[0]["start"] != 0.0 or abs(beats[-1]["end"] - duration) > 1e-6:
        die("incohérence interne : les beats ne couvrent pas tout l'audio")

    out = {"profile": args.profile, "beats": beats}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    durs = [b["end"] - b["start"] for b in beats]
    n_split = sum(1 for b in beats if b["suggested_split"])
    info(f"écrit : {args.out} ({len(beats)} beats, durée moyenne {np.mean(durs):.2f} s, "
         f"min {min(durs):.2f}, max {max(durs):.2f}, {n_split} avec suggested_split)")


if __name__ == "__main__":
    main()
