#!/usr/bin/env python3
"""Recale les lèvres d'une vidéo existante sur une voix (Volcengine video-to-video lip sync sur KIE).

Garde l'image, les gestes et le décor de la vidéo source ; seule la bouche est redessinée pour suivre l'audio.
La vidéo rendue dure la durée de l'audio (25 i/s) : coupée si la source est plus longue, bouclée si elle est plus courte.

Usage :
  python3 scripts/kie_lipsync.py --video clip.mp4 --audio S01.wav --out clip_sync.mp4 [--mode lite|basic]

- Lit KIE_API_KEY dans .env (via kie_image.py). La clé n'est jamais affichée.
- Affiche une ligne JSON : taskId, état, crédits consommés, fichier reçu.
"""
import argparse, json, pathlib, sys, time, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from kie_image import API, call, upload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", default="lite")
    a = ap.parse_args()

    vid = a.video if a.video.startswith("http") else upload(a.video)
    aud = a.audio if a.audio.startswith("http") else upload(a.audio)
    task = call(f"{API}/createTask", {"model": "volcengine/video-to-video-lip-sync", "input": {
        "mode": a.mode, "video_url": vid, "audio_url": aud,
        "separate_vocal": False, "align_audio": True, "align_audio_reverse": False, "templ_start_seconds": 0}})
    if task.get("code") != 200:
        sys.exit(f"création refusée : {task.get('code')} {task.get('msg')}")
    tid = task["data"]["taskId"]

    for _ in range(360):  # jusqu'à 30 min
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
