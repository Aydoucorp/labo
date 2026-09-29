#!/usr/bin/env python3
"""make_captions.py : convertit words.json en captions.json au format Remotion Caption.

Convention Remotion : un espace devant chaque mot (le premier mot d'une page est
nettoye cote Remotion). La ponctuation qui suit le mot (punct_after) est collee
au mot. `timestampMs` est le milieu du mot, `hook_end_ms` la fin de la section HOOK.
`pageBreakAfter` est pose apres une ponctuation forte (. ? ! ...) et sur le dernier
mot du HOOK, pour que le style "red-box" ne deborde jamais sur la suite.
Un nombre suivi d'un symbole (% € $ £ °C, etc.) est fusionne en un seul token
("97" + "%" -> "97 %", "12" + "€" -> "12 €") avec le debut du premier et la fin
du second, pour que le karaoke n'affiche jamais un chiffre orphelin.

Sortie : work/captions.json (CONTRACTS.md section 7).
"""
from __future__ import annotations

import argparse
import re

from montage_common import STRONG_PUNCT, load_json, log, save_json, section_bounds


NUMBER_RE = re.compile(r"^[+-]?\d+(?:[.,]\d+)?$")
SYMBOL_RE = re.compile(r"^(%|‰|€|\$|£|¥|°C|°F|°|km|kg|g|cm|mm|ml|cl|l|h|min|s|x)$")


def merge_number_symbol(words: list[dict]) -> list[dict]:
    """Fusionne un nombre et le symbole qui le suit en un seul mot ("97" + "%" -> "97 %")."""
    out: list[dict] = []
    i = 0
    while i < len(words):
        w = words[i]
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt is not None and NUMBER_RE.match(str(w["w"])) and not w.get("punct_after")
                and SYMBOL_RE.match(str(nxt["w"]))):
            merged = dict(w)
            sym = str(nxt["w"])
            sep = "\u00a0" if sym in ("%", "‰", "€", "$", "£", "¥", "°C", "°F") or sym.isalpha() else ""
            merged["w"] = f"{w['w']}{sep}{sym}"
            merged["end"] = nxt["end"]
            merged["punct_after"] = nxt.get("punct_after") or ""
            scores = [x.get("score") for x in (w, nxt) if x.get("score") is not None]
            merged["score"] = round(min(scores), 3) if scores else None
            out.append(merged)
            i += 2
            continue
        out.append(w)
        i += 1
    return out


def build_captions(words: list[dict], hook_end_s: float | None) -> list[dict]:
    caps: list[dict] = []
    words = merge_number_symbol(words)
    for w in words:
        start = float(w["start"])
        end = float(w["end"])
        if end < start:
            end = start
        punct = w.get("punct_after") or ""
        # Typographie francaise : espace insecable avant ? ! : ;
        sep = "\u00a0" if punct in ("?", "!", ":", ";") else ""
        text = " " + str(w["w"]) + sep + punct
        cap = {
            "text": text,
            "startMs": int(round(start * 1000)),
            "endMs": int(round(end * 1000)),
            "timestampMs": int(round((start + end) / 2 * 1000)),
            "confidence": w.get("score"),
        }
        page_break = punct in STRONG_PUNCT
        if hook_end_s is not None and end <= hook_end_s + 1e-3:
            # dernier mot du hook : coupe de page
            nxt = None
            idx = words.index(w)
            if idx + 1 < len(words):
                nxt = float(words[idx + 1]["start"])
            if nxt is None or nxt >= hook_end_s - 1e-3:
                page_break = True
        if page_break:
            cap["pageBreakAfter"] = True
        caps.append(cap)
    return caps


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Genere work/captions.json (format Remotion Caption) depuis words.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("words", help="work/words.json (CONTRACTS.md section 1)")
    ap.add_argument("brief", help="brief.json (sections, fps)")
    ap.add_argument("--out", required=True, help="chemin de sortie, ex. work/captions.json")
    args = ap.parse_args()

    words_doc = load_json(args.words)
    brief = load_json(args.brief)
    fps = int(brief.get("project", {}).get("fps", 30))
    hook = section_bounds(brief, "HOOK")
    hook_end_s = hook[1] if hook else None
    words = sorted(words_doc.get("words", []), key=lambda w: float(w["start"]))
    caps = build_captions(words, hook_end_s)
    out = {
        "fps": fps,
        "hook_end_ms": int(round(hook_end_s * 1000)) if hook_end_s is not None else 0,
        "captions": caps,
    }
    save_json(args.out, out)
    log(f"captions : {len(caps)} mots, hook_end_ms={out['hook_end_ms']} -> {args.out}")


if __name__ == "__main__":
    main()
