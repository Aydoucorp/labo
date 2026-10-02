# effacer_textes.py
# Efface ses textes incrustés (« Day X », hook anglais, émojis) avec LaMa (inpainting IA, licence Apache 2.0,
# usage commercial autorisé), gratuitement sur CPU via onnxruntime. Les masques viennent de masques.py.
# Traite les images 0 à FIN (avant l'apparition du produit) et écrit work/efface.mkv (sans perte, FFV1).
# Modèle : Carve/LaMa-ONNX (lama_fp32.onnx, 208 Mo), téléchargé une fois dans ~/.cache/studio/.
# Usage : python3 effacer_textes.py

import subprocess, urllib.request
from pathlib import Path
import numpy as np, cv2, onnxruntime as ort

RUN = Path(__file__).resolve().parent
SRC = RUN / "source/original_pure-batana76.mp4"
MODELE = Path.home() / ".cache/studio/lama_fp32.onnx"
URL = "https://huggingface.co/Carve/LaMa-ONNX/resolve/main/lama_fp32.onnx"
FIN = 351            # dernière image gardée (le flacon entre dans le cadre à l'image 352, 11,73 s)
Y0, Y1 = 60, 420     # bande 720x360 qui contient tous les textes
DILATE = 9           # marge en plus des masques pour l'ombre et le contour flou

# texte : (première image, dernière image) où son masque est appliqué (fondus compris)
PLAGES = {"hook": (0, 92), "jour1": (12, 92), "jour14": (86, 172), "jour90": (164, 292), "jour180": (256, FIN)}

def modele():
    if not MODELE.exists():
        MODELE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, MODELE)
    return ort.InferenceSession(str(MODELE), providers=["CPUExecutionProvider"])

def lama(sess, img, mk):
    band, mb = img[Y0:Y1], mk[Y0:Y1]
    if not mb.any():
        return img
    pad = np.zeros((720, 720, 3), np.uint8); pad[:360] = band; pad[360:] = band[::-1]  # carré : bande + miroir
    pm = np.zeros((720, 720), np.uint8); pm[:360] = mb
    x = cv2.resize(cv2.cvtColor(pad, cv2.COLOR_BGR2RGB), (512, 512), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    mm = (cv2.resize(pm, (512, 512), interpolation=cv2.INTER_AREA) > 0).astype(np.float32)
    out = sess.run(None, {"image": x.transpose(2, 0, 1)[None], "mask": mm[None, None]})[0][0].transpose(1, 2, 0)
    if out.max() <= 1.5:
        out = out * 255
    out = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    up = cv2.resize(out, (720, 720), interpolation=cv2.INTER_CUBIC)[:360]
    a = cv2.GaussianBlur((mb > 0).astype(np.float32), (0, 0), 2)[..., None]  # bord du masque adouci
    res = img.copy()
    res[Y0:Y1] = (band * (1 - a) + up * a).astype(np.uint8)
    return res

def main():
    sess = modele()
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (DILATE, DILATE))
    M = {n: cv2.dilate(cv2.imread(str(RUN / f"work/masque_{n}.png"), 0), k) for n in PLAGES}
    cap = cv2.VideoCapture(str(SRC))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280",
                          "-r", "30", "-i", "-", "-c:v", "ffv1", str(RUN / "work/efface.mkv")], stdin=subprocess.PIPE)
    for i in range(FIN + 1):
        ok, f = cap.read()
        mk = np.zeros(f.shape[:2], np.uint8)
        for n, (a, b) in PLAGES.items():
            if a <= i <= b:
                mk = np.maximum(mk, M[n])
        p.stdin.write(lama(sess, f, mk).tobytes())
        if i % 25 == 0:
            print(f"image {i}/{FIN}", flush=True)
    p.stdin.close(); p.wait()
    print("fini", RUN / "work/efface.mkv")

if __name__ == "__main__":
    main()
