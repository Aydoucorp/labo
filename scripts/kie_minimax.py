#!/usr/bin/env python3
"""Anime une image de départ avec MiniMax H3 image vers vidéo sur KIE (animations éducatives, b-roll de secours).

Usage :
  python3 scripts/kie_minimax.py --prompt-file p.txt --image depart.png --out anim.mp4 [--duration 9] [--resolution 768P|2K]

- Durée 4 à 15 s ; le ratio suit celui de l'image de départ.
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
    ap.add_argument("--duration", type=int, default=9)
    ap.add_argument("--resolution", default="768P")
    a = ap.parse_args()

    img = a.image if a.image.startswith("http") else upload(a.image)
    task = call(f"{API}/createTask", {"model": "minimax-h3/image-to-video", "input": {
        "prompt": pathlib.Path(a.prompt_file).read_text(), "first_frame_url": img,
        "duration": a.duration, "resolution": a.resolution}})
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
