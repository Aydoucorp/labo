#!/usr/bin/env python3
"""Contrôle automatique d'un montage exporté, avant livraison. Écrit rapport_controle.md (OK / À CORRIGER par point)
et les planches d'images (via controler.py). À lancer à chaque passe de contrôle (3 passes minimum).

Vérifie :
- fichier exporté : 1080×1920, 30 i/s, H.264 + AAC, durée = durationSec de montage.json ;
- volume : environ -14 LUFS intégrés, pic sous -1 dBFS ;
- plans : se suivent sans trou ni chevauchement de 0 à la fin ; médias présents dans public/ ;
- clips avatar : assez longs pour leur plan (sinon image figée ou noire) ;
- sous-titres : aucune ligne qui enjambe deux plans ; texte identique au script ;
- voix (Whisper sur l'export) : tout le script, dans l'ordre, sans mot manquant ni doublon ; pauses de plus de 0,8 s.

Usage : python3 controler_montage.py out/final.mp4 montage.json script.txt [--sortie controle] [--modele medium]
"""
import argparse, difflib, json, pathlib, re, subprocess, unicodedata

ICI = pathlib.Path(__file__).resolve().parent


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def norm_mots(txt):
    txt = re.sub(r"\[[^\]]*\]", " ", txt)  # balises ElevenLabs ([thoughtful]…)
    txt = txt.lower().replace("’", "'").replace("%", " pour cent ").replace("«", " ").replace("»", " ")
    txt = re.sub(r"\b30\b", "trente", re.sub(r"\b70\b", "soixante-dix", txt))
    txt = re.sub(r"[^\w' -]", " ", txt)
    return [w for w in re.split(r"[\s']+", txt) if w]


def sans_accents(w):
    return "".join(c for c in unicodedata.normalize("NFD", w) if unicodedata.category(c) != "Mn")


def chunks(words, max_words=4, max_chars=26, gap=0.45):
    """Même découpage en lignes que Subtitles.jsx."""
    out, cur = [], []
    for w in words:
        prev = cur[-1] if cur else None
        ln = sum(len(x["w"]) + 1 for x in cur) + len(w["w"])
        if prev and (w.get("br") or re.search(r"[.!?:]$", prev["w"]) or w["s"] - prev["e"] > gap or len(cur) >= max_words or ln > max_chars):
            out.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.!?;:,]$", w["w"]) and len(cur) >= 2:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("montage")
    ap.add_argument("script")
    ap.add_argument("--sortie", default="controle")
    ap.add_argument("--modele", default="medium")
    a = ap.parse_args()
    m = json.load(open(a.montage))
    pub = pathlib.Path(a.montage).resolve().parent / "public"
    sortie = pathlib.Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    res = []

    def check(nom, ok, detail=""):
        res.append((nom, ok, detail))

    # 1. fichier exporté
    p = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate",
                       "-of", "json", a.video]).stdout)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    au = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
    dur = float(p["format"]["duration"])
    check("Format 1080×1920, 30 i/s, H.264 + AAC",
          v["width"] == 1080 and v["height"] == 1920 and v["r_frame_rate"] == "30/1" and v["codec_name"] == "h264" and au and au["codec_name"] == "aac",
          f"{v['width']}×{v['height']}, {v['r_frame_rate']}, {v['codec_name']} + {au['codec_name'] if au else 'aucun son'}")
    check("Durée = montage", abs(dur - m["durationSec"]) < 0.25, f"export {dur:.2f} s, montage {m['durationSec']:.2f} s")

    # 2. volume
    err = sh(["ffmpeg", "-i", a.video, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    i_lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
    peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)[-1])
    check("Volume ≈ -14 LUFS, pic < -1 dBFS", -15.5 <= i_lufs <= -12.5 and peak <= -1.0, f"{i_lufs} LUFS, pic {peak} dBFS")

    # 3. plans
    segs = sorted(m["segments"], key=lambda s: s["start"])
    trous = [f"{x['end']:.2f}→{y['start']:.2f}" for x, y in zip(segs, segs[1:]) if abs(y["start"] - x["end"]) > 1 / 30]
    bornes = abs(segs[0]["start"]) < 1 / 30 and abs(segs[-1]["end"] - m["durationSec"]) < 1 / 30
    check("Plans continus de 0 à la fin", not trous and bornes, ", ".join(trous) or "aucun trou")
    manquants = set()
    for s in segs:
        for f in [s.get("src")] + [b.get("src") for b in s.get("broll", []) + s.get("clips", [])] + [r.get("img") for r in s.get("rows", [])]:
            if f and not (pub / f).exists():
                manquants.add(f)
    for o in m.get("overlays", []):
        for f in (o.get("src"), o.get("avatar"), o.get("media")):
            if f and not (pub / f).exists():
                manquants.add(f)
    if m.get("audio") and not (pub / m["audio"]).exists():
        manquants.add(m["audio"])
    check("Médias présents dans public/", not manquants, ", ".join(sorted(manquants)) or "tous présents")

    # 4. clips avatar assez longs
    courts = []
    for s in segs:
        if s["type"] in ("avatar", "split") and s.get("src"):
            f = pub / s["src"]
            if f.exists():
                d = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).stdout)
                besoin = s["end"] - s.get("clipStart", s["start"])
                if besoin > d + 0.05:
                    courts.append(f"{s['src']} ({besoin:.2f} s demandés, {d:.2f} s dispo, plan {s['start']:.2f}–{s['end']:.2f})")
    check("Clips avatar assez longs", not courts, " ; ".join(courts) or "ok")

    # 5. sous-titres
    words = m.get("subtitles", {}).get("words", [])
    if words:
        seg_de = lambda t: next((i for i, s in enumerate(segs) if s["start"] <= t < s["end"]), -1)
        enjambe = [" ".join(w["w"] for w in c) for c in chunks(words) if seg_de(c[0]["s"]) != seg_de(c[-1]["s"])]
        check("Aucune ligne de sous-titres sur deux plans", not enjambe, " | ".join(enjambe[:6]) or "ok")
        script = norm_mots(pathlib.Path(a.script).read_text())
        subs = norm_mots(" ".join(w["w"] for w in words))
        diff = [f"{' '.join(script[i1:i2]) or '∅'} → {' '.join(subs[j1:j2]) or '∅'}"
                for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, script, subs).get_opcodes() if op != "equal"]
        check("Sous-titres identiques au script", not diff, " ; ".join(diff[:8]) or "ok")

    # 6. voix réelle (Whisper)
    from faster_whisper import WhisperModel
    wm = WhisperModel(a.modele, device="cpu", compute_type="int8")
    segs_w, _ = wm.transcribe(a.video, language="fr", word_timestamps=True)
    ws = [w for s in segs_w for w in s.words]
    entendu = norm_mots(" ".join(w.word for w in ws))
    script = norm_mots(pathlib.Path(a.script).read_text())
    ops = [(op, script[i1:i2], entendu[j1:j2]) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, script, entendu).get_opcodes() if op != "equal"]
    # écarts d'orthographe ou de prononciation proches (Whisper) séparés des vrais trous
    def grave(o):
        op, s, e = o
        if op != "replace":
            return True  # mot manquant ou en trop
        if abs(len(s) - len(e)) >= 2 or len(s) >= 3:
            return difflib.SequenceMatcher(None, sans_accents(" ".join(s)), sans_accents(" ".join(e))).ratio() < 0.6
        return False  # un ou deux mots proches : prononciation ou erreur de transcription, à réécouter
    graves = [o for o in ops if grave(o)]
    legers = [o for o in ops if o not in graves]
    check("Voix : tout le script, dans l'ordre, sans doublon", not graves,
          " ; ".join(f"{op} « {' '.join(s) or '∅'} » → « {' '.join(e) or '∅'} »" for op, s, e in graves[:8]) or "ok")
    if legers:
        check("Voix : mots à réécouter (prononciation ou transcription)", True,
              " ; ".join(f"« {' '.join(s)} » entendu « {' '.join(e)} »" for _, s, e in legers[:10]))
    pauses = [f"{x.end:.2f} s ({y.start - x.end:.2f} s)" for x, y in zip(ws, ws[1:]) if y.start - x.end > 0.8]
    check("Aucune pause de plus de 0,8 s", not pauses, ", ".join(pauses) or "ok")

    # 7. planches d'images
    sh(["python3", str(ICI / "controler.py"), a.video, a.montage, "--sortie", str(sortie)])

    lignes = ["# Rapport de contrôle", "", f"Fichier : `{a.video}`", "", "| Point | Statut | Détail |", "|---|---|---|"]
    lignes += [f"| {n} | {'OK' if ok else '**À CORRIGER**'} | {d} |" for n, ok, d in res]
    lignes += ["", f"Planches d'images : `{sortie}/` (regarder les coupes, les lèvres, les textes)."]
    (sortie / "rapport_controle.md").write_text("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
