#!/usr/bin/env python3
"""Anime une image de départ avec Gemini Omni 1.1 Flash sur KIE (b-roll IA à partir d'une start frame).

Usage :
  python3 scripts/kie_omni.py --prompt-file p.txt --image depart.png --out clip.mp4 [--duration 6] [--resolution 720p] [--ratio 9:16]

- Modèle KIE : google/gemini-omni-flash-1-1 ; durée 4, 6, 8 ou 10 s ; résolution 360p, 720p, 1080p ou 4k ; ratio 9:16 ou 16:9.
- Prix relevé le 2026-10-08 en 720p : 4 s 63 cr, 6 s 84 cr, 8 s 105 cr, 10 s 126 cr.
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
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=int, default=6)
    ap.add_argument("--resolution", default="720p")
    ap.add_argument("--ratio", default="9:16")
    a = ap.parse_args()
    img = a.image if a.image.startswith("http") else upload(a.image)
    task = call(f"{API}/createTask", {"model": "google/gemini-omni-flash-1-1", "input": {
        "prompt": pathlib.Path(a.prompt_file).read_text(), "first_frame_url": img,
        "duration": a.duration, "resolution": a.resolution, "aspect_ratio": a.ratio}})
    if task.get("code") != 200:
        sys.exit(f"création refusée : {task.get('code')} {task.get('msg')}")
    tid = task["data"]["taskId"]
    for _ in range(240):
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
