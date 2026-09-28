#!/usr/bin/env python3
"""Clip avatar parlant avec Seedance 2.5 sur KIE : image de départ (en référence) + extrait de voix off qui pilote les lèvres.

Usage :
  python3 scripts/kie_seedance.py --prompt-file p.txt --image depart.png --audio A01.wav --out clip.mp4 \
      [--duration 4] [--ratio 9:16] [--resolution 720p]

- Seedance 2.5 n'accepte pas à la fois une première image imposée et un audio de référence :
  l'image est envoyée dans reference_image_urls, le prompt la déclare « exact first frame ».
- Son du modèle désactivé (generate_audio=false) : le son du clip est coupé au montage.
- Lit KIE_API_KEY dans .env (via kie_image.py). La clé n'est jamais affichée.
- Affiche une ligne JSON : taskId, état, crédits consommés, fichier reçu.
"""
import argparse, json, pathlib, sys, time, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from kie_image import API, call, upload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=int, default=4)
    ap.add_argument("--ratio", default="9:16")
    ap.add_argument("--resolution", default="720p")
    a = ap.parse_args()

    img = a.image if a.image.startswith("http") else upload(a.image)
    aud = a.audio if a.audio.startswith("http") else upload(a.audio)
    task = call(f"{API}/createTask", {"model": "bytedance/seedance-2-5", "input": {
        "prompt": pathlib.Path(a.prompt_file).read_text(),
        "reference_image_urls": [img], "reference_audio_urls": [aud],
        "duration": a.duration, "aspect_ratio": a.ratio, "resolution": a.resolution,
        "generate_audio": False}})
    if task.get("code") != 200:
        sys.exit(f"création refusée : {task.get('code')} {task.get('msg')}")
    tid = task["data"]["taskId"]

    for _ in range(240):  # jusqu'à 20 min
        time.sleep(5)
        d = call(f"{API}/recordInfo?taskId={tid}")["data"]
        if d["state"] in ("success", "fail"):
            break
    res = {"taskId": tid, "state": d["state"], "credits": d.get("creditsConsumed")}
    if d["state"] == "success":
        url = json.loads(d["resultJson"])["resultUrls"][0]
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, a.out)
        res["file"] = a.out
    else:
        res["error"] = d.get("failMsg")
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
