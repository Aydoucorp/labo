#!/usr/bin/env python3
"""Avatar parlant synchronisé sur une voix (Kling AI Avatar sur KIE) : image de départ + extrait audio -> vidéo.

Les lèvres sont générées à partir de l'audio lui-même : la vidéo dure la durée de l'audio.

Usage :
  python3 scripts/kie_avatar.py --image depart.png --audio S01.wav --out clip.mp4 \
      [--prompt-file p.txt] [--model kling/ai-avatar-pro|kling/ai-avatar-standard]

- Lit KIE_API_KEY dans .env (via kie_image.py). La clé n'est jamais affichée.
- Affiche une ligne JSON : taskId, état, crédits consommés, fichier reçu.
"""
import argparse, json, pathlib, sys, time, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from kie_image import API, call, upload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompt-file", default=None)
    ap.add_argument("--model", default="kling/ai-avatar-pro")
    a = ap.parse_args()

    img = a.image if a.image.startswith("http") else upload(a.image)
    aud = a.audio if a.audio.startswith("http") else upload(a.audio)
    prompt = pathlib.Path(a.prompt_file).read_text() if a.prompt_file else ""
    task = call(f"{API}/createTask", {"model": a.model, "input": {
        "image_url": img, "audio_url": aud, "prompt": prompt}})
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
