#!/usr/bin/env python3
"""Découpe une vidéo (tierce ou tournée) en rushes réutilisables comme b-roll : un fichier par plan.

Usage :
  python3 scripts/rushes_video.py <video> --dossier runs/<run>/rushes --prefixe <nom-court> \
      [--seuil 0.25] [--min 0.6] [--debut 0] [--fin <s>] [--coupes 1.2,3.4]

- Détecte les changements de plan (ffmpeg scene > seuil) ; --coupes ajoute des coupes à la main (en s).
- Ignore les plans plus courts que --min secondes (transitions, flashs).
- Exporte chaque plan sans son, à la résolution d'origine (H.264 CRF 16) :
  <dossier>/<prefixe>_<NN>_<debut>-<fin>s.mp4
- Écrit <dossier>/<prefixe>_planche.jpg (image du milieu de chaque rush, numérotée) pour décrire les rushes,
  et affiche la liste des rushes (numéro, début, fin, durée, fichier).
"""
import argparse, re, subprocess
from pathlib import Path
import cv2, numpy as np


def duree(video):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                                capture_output=True, text=True).stdout)


def coupes_auto(video, seuil):
    out = subprocess.run(["ffmpeg", "-i", video, "-vf", f"select='gt(scene,{seuil})',metadata=print:file=-", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stdout
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", out)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--dossier", required=True); ap.add_argument("--prefixe", required=True)
    ap.add_argument("--seuil", type=float, default=0.25); ap.add_argument("--min", type=float, default=0.6)
    ap.add_argument("--debut", type=float, default=0.0); ap.add_argument("--fin", type=float, default=None)
    ap.add_argument("--coupes", default="")
    a = ap.parse_args()
    fin = a.fin or duree(a.video)
    cs = sorted(set(round(c, 3) for c in coupes_auto(a.video, a.seuil) + [float(x) for x in a.coupes.split(",") if x]))
    bornes = [a.debut] + [c for c in cs if a.debut < c < fin] + [fin]
    plans = [(t0, t1) for t0, t1 in zip(bornes, bornes[1:]) if t1 - t0 >= a.min]
    d = Path(a.dossier); d.mkdir(parents=True, exist_ok=True)
    tuiles = []
    for n, (t0, t1) in enumerate(plans, 1):
        f = d / f"{a.prefixe}_{n:02d}_{t0:.1f}-{t1:.1f}s.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", a.video, "-t", f"{t1 - t0 - 0.034:.3f}", "-an",
                        "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", str(f)], check=True)
        cap = cv2.VideoCapture(str(f)); cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / 2))
        ok, img = cap.read()
        if ok:
            img = cv2.resize(img, (180, int(180 * img.shape[0] / img.shape[1])))
            cv2.putText(img, f"{n:02d}", (4, 22), 0, 0.7, (0, 255, 255), 2); tuiles.append(img)
        print(f"{n:02d}  {t0:6.2f}  {t1:6.2f}  {t1 - t0:5.2f} s  {f}")
    if tuiles:
        h = max(t.shape[0] for t in tuiles); tuiles = [cv2.copyMakeBorder(t, 0, h - t.shape[0], 0, 0, cv2.BORDER_CONSTANT) for t in tuiles]
        while len(tuiles) % 8: tuiles.append(np.zeros_like(tuiles[0]))
        cv2.imwrite(str(d / f"{a.prefixe}_planche.jpg"), np.vstack([np.hstack(tuiles[i:i + 8]) for i in range(0, len(tuiles), 8)]))


if __name__ == "__main__":
    main()
