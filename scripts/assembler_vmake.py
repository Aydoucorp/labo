#!/usr/bin/env python3
"""Réassemble des parties nettoyées dans VMake en une seule vidéo sans texte (sans son).

VMake perd les 3 premières images de chaque partie : chacune est complétée par 3 copies de sa première image,
pour rester calée sur la vidéo d'origine (même nombre d'images).
Usage : python3 scripts/assembler_vmake.py <sortie.mp4> <partie-1.mp4> <partie-2.mp4> ... [--decalage 3]
"""
import argparse, subprocess
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("sortie"); ap.add_argument("parties", nargs="+"); ap.add_argument("--decalage", type=int, default=3)
a = ap.parse_args()
fr = []
for p in a.parties:
    cap = cv2.VideoCapture(p); part = []
    while True:
        ok, f = cap.read()
        if not ok: break
        part.append(f)
    fr += [part[0]] * a.decalage + part
h, w = fr[0].shape[:2]
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "30", "-i", "-",
                       "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", a.sortie], stdin=subprocess.PIPE)
for f in fr:
    pr.stdin.write(f.tobytes())
pr.stdin.close(); pr.wait(); print(a.sortie, len(fr), "images")
