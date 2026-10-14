#!/usr/bin/env python3
"""Mesure la synchro lèvres / voix directement sur l'image (sans passer par le son généré par Seedance).

Usage : python3 scripts/mesure_levres.py clip.mp4 voix.wav [--fenetre 2.0] [--pas 1.0] [--csv sortie.csv]

- Ouverture de la bouche image par image (MediaPipe Face Landmarker : distance lèvre haute / lèvre basse,
  rapportée à la hauteur du visage).
- Enveloppe de la voix (énergie) ramenée à la cadence de la vidéo.
- Par fenêtre glissante : décalage qui aligne le mieux bouche et voix (positif = la bouche est en retard)
  et corrélation (au-dessus de 0,5 : la bouche suit la voix ; en dessous de 0,3 : elle ne la suit plus).
- Si le clip a un son (voix Seedance), la même mesure est faite contre ce son : on voit si la bouche suit
  la voix d'origine ou la parole inventée par Seedance.
Le modèle face_landmarker.task est téléchargé une fois dans ~/.cache/mediapipe/.
"""
import argparse, pathlib, subprocess, urllib.request
import numpy as np, cv2
import mediapipe as mp

MODELE = pathlib.Path.home() / ".cache/mediapipe/face_landmarker.task"
URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"


def bouche(clip):
    if not MODELE.exists():
        MODELE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, MODELE)
    opts = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELE)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO, num_faces=1)
    det = mp.tasks.vision.FaceLandmarker.create_from_options(opts)
    cap = cv2.VideoCapture(str(clip)); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    vals, i = [], 0
    while True:
        ok, img = cap.read()
        if not ok:
            break
        res = det.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),
                                   int(i * 1000 / fps))
        if res.face_landmarks:
            p = res.face_landmarks[0]
            vals.append(abs(p[14].y - p[13].y) / max(1e-6, abs(p[152].y - p[10].y)))
        else:
            vals.append(np.nan)
        i += 1
    v = np.array(vals)
    if np.isnan(v).any():  # images sans visage détecté : interpolation
        idx = np.arange(len(v)); ok = ~np.isnan(v)
        v = np.interp(idx, idx[ok], v[ok])
    return v, fps


def enveloppe(src, fps, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float)
    if x.size == 0:
        return None
    h = int(16000 / fps)
    e = np.array([np.sqrt(np.mean(x[k * h:(k + 1) * h] ** 2)) if k * h < len(x) else 0 for k in range(n)])
    return np.log1p(e)


def norm(a):
    s = a.std()
    return (a - a.mean()) / s if s > 0 else a * 0


def fenetres(m, e, fps, win, pas, lagmax=0.5):
    out = []
    W, P, L = int(win * fps), int(pas * fps), int(lagmax * fps)
    for t0 in range(L, len(m) - W - L + 1, P):
        best, bc = 0, -2
        for d in range(-L, L + 1):  # d > 0 : la bouche bouge après la voix
            c = np.corrcoef(norm(e[t0:t0 + W]), norm(m[t0 + d:t0 + d + W]))[0, 1]
            if c > bc:
                best, bc = d, c
        out.append((t0 / fps, (t0 + W) / fps, best / fps, bc))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("voix")
    ap.add_argument("--fenetre", type=float, default=2.0); ap.add_argument("--pas", type=float, default=1.0)
    ap.add_argument("--csv", default=None)
    a = ap.parse_args()
    m, fps = bouche(a.clip)
    ev = enveloppe(a.voix, fps, len(m)); es = enveloppe(a.clip, fps, len(m))
    rv = fenetres(m, ev, fps, a.fenetre, a.pas)
    rs = fenetres(m, es, fps, a.fenetre, a.pas) if es is not None else [(None, None, None, None)] * len(rv)
    print(f"{'fenêtre':>13} | {'voix d origine':^22} | {'son Seedance':^22}")
    print(f"{'':>13} | {'décalage':>9} {'corrél.':>9}    | {'décalage':>9} {'corrél.':>9}")
    lignes = []
    for (t0, t1, dv, cv), (_, _, ds, cs) in zip(rv, rs):
        s2 = f"{ds:+8.2f}s {cs:9.2f}" if ds is not None else f"{'-':>9} {'-':>9}"
        etat = "OK" if cv >= 0.5 and abs(dv) <= 0.1 else ("à vérifier" if cv >= 0.3 else "DÉCROCHE")
        print(f"{t0:5.1f}-{t1:5.1f} s | {dv:+8.2f}s {cv:9.2f}    | {s2}   {etat}")
        lignes.append(f"{t0:.2f},{t1:.2f},{dv:.3f},{cv:.3f},{'' if ds is None else f'{ds:.3f}'},{'' if cs is None else f'{cs:.3f}'},{etat}")
    if a.csv:
        pathlib.Path(a.csv).write_text("debut,fin,decalage_voix,correl_voix,decalage_seedance,correl_seedance,etat\n" + "\n".join(lignes) + "\n")


if __name__ == "__main__":
    main()
