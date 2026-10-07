# assembler.py
# Réassemble les 4 parties nettoyées par l'utilisateur sur VMake (source/nettoyees/partie-N.mp4).
# Chaque partie nettoyée commence 3 images après la partie envoyée (mesuré par comparaison d'images) :
# on comble ces 3 images en répétant la première image de la partie, pour garder les 482 images
# et le son d'origine continu, calé à l'image. Pas de texte, pas de CTA (l'utilisateur pose son hook).
# Sortie : sorties/claire-chute-brossage-sans-texte_v1.mp4 en 1080x1920.
import subprocess
from pathlib import Path
import cv2
RUN = Path(__file__).resolve().parent
W, H, FPS = 1080, 1920, 30
DECALAGE = 3
OUT = RUN / "sorties/claire-chute-brossage-sans-texte_v1.mp4"
frames = []
for i in range(1, 5):
    cap = cv2.VideoCapture(str(RUN / f"source/nettoyees/partie-{i}.mp4")); part = []
    while True:
        ok, f = cap.read()
        if not ok: break
        part.append(f)
    frames += [part[0]] * DECALAGE + part
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "576x1024", "-r", str(FPS),
                      "-i", "-", "-i", str(RUN / "source/original.mp4"), "-map", "0:v", "-map", "1:a",
                      "-vf", f"scale={W}:{H}:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(OUT)],
                     stdin=subprocess.PIPE)
for f in frames:
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
print(OUT, len(frames), "images")
