#!/usr/bin/env python3
"""Anime une image de départ avec Gemini Omni Flash 1.1 sur KIE, attend le clip et le télécharge.

Usage :
  python3 scripts/kie_video.py --prompt-file p.txt --first-frame image.png --out sorties/x.mp4 \
      [--duration 4|6|8|10] [--ratio 9:16] [--resolution 720p|1080p]

- Lit KIE_API_KEY dans .env (via kie_image.py). La clé n'est jamais affichée.
- Affiche une ligne JSON : taskId, état, crédits consommés, fichier reçu.
"""
import argparse, json, pathlib, sys, time, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from kie_image import API, call, upload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--first-frame", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", default="4")
    ap.add_argument("--ratio", default="9:16")
    ap.add_argument("--resolution", default="1080p")
    a = ap.parse_args()

    frame = a.first_frame if a.first_frame.startswith("http") else upload(a.first_frame)
    task = call(f"{API}/createTask", {"model": "google/gemini-omni-flash-1-1", "input": {
        "prompt": pathlib.Path(a.prompt_file).read_text(), "first_frame_url": frame,
        "duration": a.duration, "aspect_ratio": a.ratio, "resolution": a.resolution}})
    if task.get("code") != 200:
        sys.exit(f"création refusée : {task.get('code')} {task.get('msg')}")
    tid = task["data"]["taskId"]

    for _ in range(180):  # jusqu'à 15 min
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
