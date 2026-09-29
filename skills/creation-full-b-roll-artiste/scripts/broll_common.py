#!/usr/bin/env python3
"""
Fonctions partagées par les scripts de la brique ALIGNEMENT de CRÉATION FULL B-ROLL ARTISTE.

Contenu :
  - décodage audio via ffmpeg (n'importe quel format vers PCM float mono)
  - tokenisation du script en mots (règles documentées ci-dessous)
  - normalisation des mots (sans accents, sans casse, sans ponctuation)
  - conversion des nombres en mots français (pour l'alignement phonétique)

Règles de tokenisation (stables, utilisées par align.py) :
  1. Le script est découpé sur les espaces et retours à la ligne.
  2. Les élisions et contractions avec apostrophe forment UN SEUL mot :
     "l'eau", "c'est", "qu'une", "aujourd'hui". Raison : c'est l'unité visuelle
     naturelle d'un sous-titre et les moteurs ASR sortent aussi un seul mot.
     L'apostrophe typographique (’) est conservée dans `w` mais normalisée en (')
     pour la comparaison.
  3. Les mots composés avec trait d'union restent un seul mot ("peut-être",
     "dis-moi", "quatre-vingt-dix").
  4. Un nombre est un mot ("20", "1,5", "97%", "12€", "30g"). Un symbole seul
     ("%", "€") est un mot à part entière (il est prononcé : "pour cent", "euros").
  5. La ponctuation qui suit un mot est retirée du mot et rangée dans
     `punct_after` avec les valeurs fermées du contrat : "", ",", ".", "?", "!",
     ":", "...". Correspondances : ";" devient ",", "…" devient "...".
     Si plusieurs signes se suivent ("?!"), on garde le plus fort dans l'ordre
     "..." > "?" > "!" > "." > ":" > ",".
  6. Les guillemets, parenthèses, crochets et tirets isolés ne sont pas des mots.
     Un tiret isolé (–, —, -) vaut une virgule pour le mot précédent.
"""

import re
import subprocess
import sys
import unicodedata

import numpy as np

# Ponctuation retenue dans punct_after, par force décroissante
PUNCT_PRIORITY = ["...", "?", "!", ".", ":", ","]

# Caractères de ponctuation ou de citation pouvant entourer un mot
_LEAD_STRIP = "«\"'‘“(\\[{—–-…"
_TRAIL_CHARS = ".,;:!?…»\"'’”)\\]}—–"


def die(msg, code=1):
    """Affiche un message d'erreur et quitte avec un code non nul."""
    print(f"ERREUR : {msg}", file=sys.stderr)
    sys.exit(code)


def info(msg):
    """Message d'information sur stderr (stdout reste propre)."""
    print(msg, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------

def decode_audio(path, sr=16000):
    """Décode un fichier audio (mp3, wav, m4a...) en float32 mono via ffmpeg.

    Retourne (samples, sr). Quitte avec un message clair si ffmpeg échoue.
    """
    cmd = [
        "ffmpeg", "-v", "error", "-nostdin", "-i", path,
        "-f", "f32le", "-ac", "1", "-ar", str(sr), "-",
    ]
    try:
        raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    except FileNotFoundError:
        die("ffmpeg introuvable dans le PATH")
    except subprocess.CalledProcessError as e:
        die(f"ffmpeg n'a pas pu décoder {path} : {e.stderr.decode(errors='replace').strip()}")
    samples = np.frombuffer(raw, dtype=np.float32)
    if samples.size == 0:
        die(f"audio vide ou illisible : {path}")
    return samples, sr


def convert_to_wav16k(src, dst):
    """Convertit src en wav 16 kHz mono PCM 16 bits (fichier dst)."""
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", src,
           "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", dst]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        die("ffmpeg introuvable dans le PATH")
    except subprocess.CalledProcessError as e:
        die(f"conversion ffmpeg impossible : {e.stderr.decode(errors='replace').strip()}")
    return dst


def audio_duration(path):
    """Durée en secondes via ffprobe."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "csv=p=0", path]
    try:
        out = subprocess.run(cmd, capture_output=True, check=True, text=True).stdout.strip()
        return float(out)
    except Exception:
        samples, sr = decode_audio(path)
        return len(samples) / sr


# ---------------------------------------------------------------------------
# Nombres en français
# ---------------------------------------------------------------------------

_UNITS = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit",
          "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize",
          "dix-sept", "dix-huit", "dix-neuf"]
_TENS = {20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 60: "soixante"}
NUMBER_VARIANT = "fr"  # "fr" (soixante-dix, quatre-vingt-dix) ou "be" (septante, nonante)


def set_number_variant(variant):
    """Choisit la prononciation des dizaines 70 et 90 : "fr" ou "be" (Belgique, Suisse)."""
    global NUMBER_VARIANT
    if variant not in ("fr", "be"):
        raise ValueError(f"variante inconnue : {variant}")
    NUMBER_VARIANT = variant


def _below_100(n):
    if n < 20:
        return _UNITS[n]
    if NUMBER_VARIANT == "be" and (70 <= n < 80 or 90 <= n < 100):
        t, u = (n // 10) * 10, n % 10
        name = "septante" if t == 70 else "nonante"
        if u == 0:
            return name
        if u == 1:
            return f"{name} et un"
        return f"{name}-{_UNITS[u]}"
    if n < 70:
        t, u = (n // 10) * 10, n % 10
        if u == 0:
            return _TENS[t]
        if u == 1:
            return f"{_TENS[t]} et un"
        return f"{_TENS[t]}-{_UNITS[u]}"
    if n < 80:
        u = n - 60
        return "soixante et onze" if u == 11 else f"soixante-{_UNITS[u]}"
    u = n - 80
    if u == 0:
        return "quatre-vingts"
    return f"quatre-vingt-{_UNITS[u]}"


def _below_1000(n):
    if n < 100:
        return _below_100(n)
    h, r = divmod(n, 100)
    head = "cent" if h == 1 else f"{_UNITS[h]} cent"
    if r == 0:
        return head + ("s" if h > 1 else "")
    return f"{head} {_below_100(r)}"


def fr_number_words(n):
    """Entier positif vers mots français (jusqu'aux milliards)."""
    n = int(n)
    if n < 1000:
        return _below_1000(n)
    parts = []
    for div, name in ((10**9, "milliard"), (10**6, "million"), (1000, "mille")):
        q, n = divmod(n, div)
        if q:
            if name == "mille":
                # "cinq cent mille", "quatre-vingt mille" : le s tombe devant mille
                q_words = re.sub(r"(cent|vingt)s$", r"\1", _below_1000(q))
                parts.append("mille" if q == 1 else f"{q_words} mille")
            else:
                parts.append(f"{_below_1000(q)} {name}{'s' if q > 1 else ''}")
    if n:
        parts.append(_below_1000(n))
    return " ".join(parts)


_ORDINALS = {1: "premier", 2: "deuxième", 3: "troisième", 4: "quatrième",
             5: "cinquième", 6: "sixième", 7: "septième", 8: "huitième",
             9: "neuvième", 10: "dixième"}

_SYMBOLS = {"%": " pour cent ", "€": " euros ", "$": " dollars ", "£": " livres ",
            "&": " et ", "+": " plus ", "°": " degrés ", "‰": " pour mille "}

_NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")


def _num_to_words(m, text_after):
    s = m.group(0)
    if "," in s or "." in s:
        a, b = re.split(r"[.,]", s, maxsplit=1)
        return f" {fr_number_words(a)} virgule {fr_number_words(b)} "
    return f" {fr_number_words(s)} "


def spell_numbers_fr(text):
    """Remplace les nombres et symboles d'un mot par leur forme prononcée.

    "97%" -> "quatre-vingt-dix-sept pour cent", "1er" -> "premier", "12€" -> "douze euros".
    """
    m = re.fullmatch(r"(\d+)(er|ère|re|ème|e|èmes|es)", text)
    if m:
        n = int(m.group(1))
        suf = m.group(2)
        if n == 1:
            return "première" if suf in ("ère", "re") else "premier"
        base = _ORDINALS.get(n)
        if base is None:
            w = fr_number_words(n)
            w = w[:-1] if w.endswith("e") else w
            base = f"{w}ième"
        return base
    out = _NUM_RE.sub(lambda mm: _num_to_words(mm, ""), text)
    for k, v in _SYMBOLS.items():
        out = out.replace(k, v)
    return re.sub(r"\s+", " ", out).strip()


# ---------------------------------------------------------------------------
# Normalisation et tokenisation
# ---------------------------------------------------------------------------

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def normalize_word(w):
    """Forme de comparaison : minuscules, sans accents, apostrophe simple, sans ponctuation."""
    s = w.replace("’", "'").replace("‘", "'").lower()
    s = strip_accents(s)
    s = s.replace("œ", "oe").replace("æ", "ae")
    # on garde le séparateur décimal entre deux chiffres ("1,5"), rien d'autre
    s = re.sub(r"(?<=\d)[.,](?=\d)", "\x00", s)
    s = re.sub(r"[^a-z0-9'%€$£&+\x00]", "", s)
    return s.replace("\x00", ",")


def pronounced_letters(w):
    """Forme phonétique latine (lettres a-z et apostrophe) pour l'aligneur CTC.

    Les nombres et symboles sont épelés en français. Retourne "" si rien n'est prononçable.
    """
    s = w.replace("’", "'").replace("‘", "'").lower()
    s = spell_numbers_fr(s)
    s = strip_accents(s).replace("œ", "oe").replace("æ", "ae")
    s = re.sub(r"[^a-z']", "", s)
    return s


def atoms(w):
    """Découpe un mot normalisé en atomes comparables entre script et ASR.

    "97%" -> ["97", "%"], "12€" -> ["12", "euros"], "l'eau" -> ["l'eau"].
    """
    n = normalize_word(w)
    if not n:
        return []
    n = n.replace("€", "euros").replace("$", "dollars").replace("£", "livres")
    parts = re.findall(r"\d+(?:[.,]\d+)?|%|[a-z']+(?:\d+[a-z']*)*|[a-z0-9']+", n)
    parts = [p.replace(".", ",") for p in parts if p and p != "'"]
    return parts or [n]


def _map_punct(chars):
    """Réduit une suite de signes de ponctuation à une valeur fermée du contrat."""
    found = set()
    if "..." in chars or "…" in chars:
        found.add("...")
    for c in chars:
        if c in "?!.:,":
            found.add(c)
        elif c == ";":
            found.add(",")
        elif c in "—–-":
            found.add(",")
    for p in PUNCT_PRIORITY:
        if p in found:
            return p
    return ""


def tokenize_script(text):
    """Découpe le texte du script en mots selon les règles du module.

    Retourne une liste de dicts {"w": str, "punct_after": str}.
    """
    words = []
    for chunk in text.split():
        raw = chunk
        # ponctuation de tête
        while raw and raw[0] in _LEAD_STRIP and not (raw[0] == "-" and len(raw) > 1 and raw[1].isdigit()):
            raw = raw[1:]
        # ponctuation de queue (on ne touche pas au séparateur décimal "1,5")
        trail = ""
        while raw and (raw[-1] in _TRAIL_CHARS):
            if raw[-1] in ".," and len(raw) >= 3 and raw[-2].isdigit() and raw[-3] == raw[-1]:
                break
            trail = raw[-1] + trail
            raw = raw[:-1]
        # apostrophe finale de type "l'" (mot tronqué) : on la garde
        if raw == "" and chunk.endswith(("'", "’")) and len(chunk) > 1:
            raw = chunk[:-1]
        if raw == "":
            # chunk purement ponctuation : on l'attache au mot précédent
            if words:
                p = _map_punct(chunk)
                cur = words[-1]["punct_after"]
                order = {p: i for i, p in enumerate(PUNCT_PRIORITY)}
                if p and (not cur or order[p] < order.get(cur, 99)):
                    words[-1]["punct_after"] = p
            continue
        # "1." en fin de phrase : le point est de la ponctuation, pas un décimal
        punct = _map_punct(trail)
        words.append({"w": raw, "punct_after": punct})
    return words


def script_hash(words):
    """sha1 du script normalisé (mots normalisés séparés par un espace)."""
    import hashlib
    norm = " ".join(normalize_word(w["w"]) for w in words)
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()


def load_script(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except OSError as e:
        die(f"script illisible : {e}")


def load_profiles(profiles_path):
    import json
    try:
        with open(profiles_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        die(f"profiles.json illisible : {e}")
    except ValueError as e:
        die(f"profiles.json invalide : {e}")


if __name__ == "__main__":
    # petit auto-test des règles
    demo = "Tu frottes ton sol, et l'eau colle encore ?! « Résultat » : 97 % ont vu, 1,5 fois... 12€ le 1er."
    for t in tokenize_script(demo):
        print(t, atoms(t["w"]), pronounced_letters(t["w"]))
    for n in (0, 1, 21, 71, 80, 81, 91, 97, 200, 1001, 2024, 1500000):
        print(n, fr_number_words(n))
