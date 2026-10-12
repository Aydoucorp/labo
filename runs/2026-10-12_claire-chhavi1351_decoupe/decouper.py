# decouper.py
# 1) Retire de la vidéo d'origine les 3 plans où l'on voit la boîte Brillare -> sorties/claire-chhavi-sans-boite_v1.mp4
#    (son d'origine en continu, coupé à la durée de la V1 avec un fondu de sortie, pour éviter les sauts de musique).
# 2) Découpe cette V1 en parties de 5 s maximum, coupées sur des changements de plan, à nettoyer dans VMake
#    -> sorties/a-nettoyer/partie-N_<début>-<fin>s.mp4
# Usage : python3 decouper.py

import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original.mp4"
V1 = RUN / "sorties/claire-chhavi-sans-boite_v1.mp4"
FPS = 30
TOTAL = 863  # images de la source

# plans avec la boîte (images incluses), repérés image par image
BOITE = [(125, 182), (225, 265), (338, 376)]

# bornes des parties dans la V1 (images), toutes sur un changement de plan, 150 images (5 s) max
PARTIES = [0, 125, 259, 386, 534, 621, 725]

def gardees():
    out, a = [], 0
    for b0, b1 in BOITE:
        out.append((a, b0 - 1)); a = b1 + 1
    out.append((a, TOTAL - 1))
    return out

def run(cmd):
    subprocess.run(cmd, check=True)

def main():
    plages = gardees()
    n = sum(b - a + 1 for a, b in plages)
    sel = "+".join(f"between(n\\,{a}\\,{b})" for a, b in plages)
    dur = n / FPS
    run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC),
         "-vf", f"select='{sel}',setpts=N/{FPS}/TB",
         "-af", f"atrim=0:{dur:.4f},afade=t=out:st={dur - 0.8:.4f}:d=0.8",
         "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", str(V1)])
    print(f"V1 : {n} images, {dur:.2f} s")

    assert PARTIES[-1] == n and all(b - a <= 150 for a, b in zip(PARTIES, PARTIES[1:]))
    dossier = RUN / "sorties/a-nettoyer"
    dossier.mkdir(parents=True, exist_ok=True)
    for i, (a, b) in enumerate(zip(PARTIES, PARTIES[1:]), 1):
        t0, t1 = a / FPS, b / FPS
        nom = dossier / f"partie-{i}_{t0:.1f}-{t1:.1f}s.mp4".replace(".0-", "-").replace(".0s", "s")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(V1),
             "-vf", f"select='between(n\\,{a}\\,{b - 1})',setpts=N/{FPS}/TB",
             "-af", f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB",
             "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", str(nom)])
        print(f"{nom.name} : images {a} à {b - 1} ({(b - a) / FPS:.2f} s)")

if __name__ == "__main__":
    main()
