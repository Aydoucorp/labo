#!/usr/bin/env python3
"""Découpe la voix maître en extraits pour les clips avatar (un extrait = un clip vidéo généré depuis l'image de départ).
Usage : python3 couper_audio.py voix.mp3 decoupage.json [--mots mots.json] [--marge 0.3] [--min 4] [--max 30] [--sortie audio_avatar]
decoupage.json doit contenir "clips_avatar": [{"id": "A01", "debut": 4.43, "fin": 9.0, "format": "9:16"}, ...]
(debut/fin = premier et dernier mot du passage ; les marges sont ajoutées ici).
- Passage plus court que --min : allongé avec de l'audio autour (le montage n'en affiche que la partie utile).
- Passage plus long que --max : coupé à la plus longue pause proche du milieu (nécessite --mots), en A01a, A01b...
Écrit un wav par clip + clips_avatar.json avec clipStart (temps absolu de l'image 0 du clip, à reporter dans montage.json).
"""
import argparse, json, os, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("decoupage")
ap.add_argument("--mots", default=None, help="mots.json (transcription) pour couper les passages trop longs à une pause")
ap.add_argument("--marge", type=float, default=0.3)
ap.add_argument("--min", type=float, default=4.0, help="durée minimale d'un clip du modèle vidéo (s)")
ap.add_argument("--max", type=float, default=30.0, help="durée maximale d'un clip du modèle vidéo (s)")
ap.add_argument("--sortie", default="audio_avatar")
a = ap.parse_args()
d = json.load(open(a.decoupage))
mots = json.load(open(a.mots)) if a.mots else None
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.audio]).decode().strip())

def scinder(c):
    """Coupe récursivement un passage trop long à la plus longue pause située dans son tiers central."""
    if c["fin"] - c["debut"] + 2 * a.marge <= a.max:
        return [c]
    if not mots:
        raise SystemExit(f"{c['id']} dure {c['fin'] - c['debut']:.1f} s (> {a.max} s) : fournis --mots pour le couper à une pause, ou coupe-le dans decoupage.json.")
    ws = [w for w in mots if c["debut"] - 0.01 <= w["s"] and w["e"] <= c["fin"] + 0.01]
    L = c["fin"] - c["debut"]
    cands = [(ws[i + 1]["s"] - ws[i]["e"], i) for i in range(len(ws) - 1)
             if c["debut"] + L / 3 <= ws[i]["e"] <= c["debut"] + 2 * L / 3]
    if not cands:
        cands = [(ws[i + 1]["s"] - ws[i]["e"], i) for i in range(len(ws) - 1)]
    _, i = max(cands)
    g = {**c, "id": c["id"] + "a", "fin": ws[i]["e"]}
    h = {**c, "id": c["id"] + "b", "debut": ws[i + 1]["s"]}
    return scinder(g) + scinder(h)

os.makedirs(a.sortie, exist_ok=True)
out = []
for c0 in d["clips_avatar"]:
    for c in scinder(c0):
        s = max(0.0, c["debut"] - a.marge)
        e = min(dur, c["fin"] + a.marge)
        if e - s < a.min:  # allonge jusqu'à la durée minimale du modèle
            manque = a.min - (e - s)
            s = max(0.0, s - manque / 2); e = min(dur, s + a.min); s = max(0.0, e - a.min)
        f = os.path.join(a.sortie, f"{c['id']}.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", a.audio, "-ac", "1", "-ar", "48000", f], check=True)
        out.append({**c, "clipStart": round(s, 3), "clipEnd": round(e, 3), "duree": round(e - s, 3),
                    "duree_a_demander": int(-(-(e - s) // 1)), "fichier": f})
        print(f"{c['id']:6s} {s:7.2f} -> {e:7.2f}  ({e - s:5.2f} s, demander {int(-(-(e - s) // 1))} s)  {c.get('format', '9:16')}  {f}")
json.dump(out, open(os.path.join(a.sortie, "clips_avatar.json"), "w"), ensure_ascii=False, indent=1)
print(f"Total à générer : {sum(x['duree_a_demander'] for x in out)} s sur {len(out)} clips")
