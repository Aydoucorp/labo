# decouper.py
# Découpe la vidéo d'origine en parties de 5 s maximum, coupées sur des changements de plan, à nettoyer dans VMake
# -> sorties/a-nettoyer/partie-N_<début>-<fin>s.mp4 (vidéo + son d'origine, H.264 CRF 14).
# Usage : python3 decouper.py

import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original.mp4"
FPS = 30
# bornes (images), toutes sur un changement de plan détecté (ffmpeg scene > 0.2), 150 images (5 s) max par partie
PARTIES = [0, 124, 247, 385, 484, 573]

def main():
    assert all(b - a <= 150 for a, b in zip(PARTIES, PARTIES[1:]))
    dossier = RUN / "sorties/a-nettoyer"
    dossier.mkdir(parents=True, exist_ok=True)
    for i, (a, b) in enumerate(zip(PARTIES, PARTIES[1:]), 1):
        t0, t1 = a / FPS, b / FPS
        nom = dossier / f"partie-{i}_{t0:.1f}-{t1:.1f}s.mp4".replace(".0-", "-").replace(".0s", "s")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC),
                        "-vf", f"select='between(n\\,{a}\\,{b - 1})',setpts=N/{FPS}/TB",
                        "-af", f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB",
                        "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", str(nom)], check=True)
        print(f"{nom.name} : images {a} à {b - 1} ({(b - a) / FPS:.2f} s)")

if __name__ == "__main__":
    main()
