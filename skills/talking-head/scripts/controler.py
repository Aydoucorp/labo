#!/usr/bin/env python3
"""Contrôle visuel d'un export : planches d'images (4 i/s) autour de chaque coupe + mesures techniques.
Usage : python3 controler.py video.mp4 montage.json [--sortie controle]
"""
import argparse, json, os, subprocess
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("montage"); ap.add_argument("--sortie", default="controle")
a = ap.parse_args(); os.makedirs(a.sortie, exist_ok=True)
m = json.load(open(a.montage))
probe = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height,r_frame_rate", "-of", "compact", a.video]).decode()
print(probe)
coupes = sorted({round(s["start"], 2) for s in m.get("segments", [])} | {round(s["end"], 2) for s in m.get("segments", [])})
for i, t in enumerate(coupes):
    t0 = max(0, t - 0.5)
    out = os.path.join(a.sortie, f"coupe_{i:02d}_{t:06.2f}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", "1", "-i", a.video, "-vf",
                    f"fps=8,scale=180:-1,drawtext=text='%{{pts\\:hms\\:{t0:.2f}}}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black,tile=8x1",
                    "-frames:v", "1", out], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", "fps=2,scale=160:-1,tile=10x6", os.path.join(a.sortie, "planche_%02d.jpg")], check=True)
loud = subprocess.run(["ffmpeg", "-i", a.video, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr.splitlines()[-12:]
print("\n".join(loud))
print(f"{len(coupes)} planches de coupe + planches générales dans {a.sortie}/")
