#!/usr/bin/env python3
"""Génère une image sur KIE (Nano Banana 2 par défaut, ou GPT Image 2 avec --model), attend le résultat et le télécharge.

Usage :
  python3 scripts/kie_image.py --prompt-file p.txt --out sorties/x.png \
      [--ref image.png ...] [--ratio 9:16] [--resolution 1K|2K|4K] [--model nano-banana-2|gpt-image-2-image-to-image]

- Lit KIE_API_KEY dans .env (racine du studio). La clé n'est jamais affichée.
- Les images de référence locales sont d'abord envoyées sur le stockage temporaire KIE.
- Affiche une ligne JSON : taskId, état, crédits consommés, fichier reçu.
"""
import argparse, json, os, sys, time, urllib.request, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"


def load_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("KIE_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("KIE_API_KEY absente de .env")


KEY = load_key()


def call(url, payload=None):
    req = urllib.request.Request(url, method="POST" if payload is not None else "GET",
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                                 data=json.dumps(payload).encode() if payload is not None else None)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def upload(path):
    # multipart via curl : plus simple et fiable qu'urllib pour les fichiers
    out = subprocess.run(["curl", "-sS", "-m", "120", "-X", "POST", UPLOAD,
                          "-H", f"Authorization: Bearer {KEY}",
                          "-F", f"file=@{path}", "-F", "uploadPath=studio/refs",
                          "-F", f"fileName={pathlib.Path(path).name}"],
                         capture_output=True, text=True)
    data = json.loads(out.stdout)
    if data.get("code") != 200:
        sys.exit(f"upload échoué : {data.get('msg')}")
    return data["data"]["downloadUrl"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref", nargs="*", default=[])
    ap.add_argument("--ratio", default="9:16")
    ap.add_argument("--resolution", default="1K")
    ap.add_argument("--model", default="nano-banana-2")
    a = ap.parse_args()

    refs = [r if r.startswith("http") else upload(r) for r in a.ref]
    prompt = pathlib.Path(a.prompt_file).read_text()
    if a.model.startswith("gpt-image-2"):
        inp = {"prompt": prompt, "input_urls": refs, "aspect_ratio": a.ratio, "resolution": a.resolution}
    else:
        inp = {"prompt": prompt, "image_input": refs, "aspect_ratio": a.ratio,
               "resolution": a.resolution, "output_format": "png"}
    task = call(f"{API}/createTask", {"model": a.model, "input": inp})
    if task.get("code") != 200:
        sys.exit(f"création refusée : {task.get('code')} {task.get('msg')}")
    tid = task["data"]["taskId"]

    for _ in range(120):
        time.sleep(5)
        d = call(f"{API}/recordInfo?taskId={tid}")["data"]
        if d["state"] in ("success", "fail"):
            break
    res = {"taskId": tid, "state": d["state"], "credits": d.get("creditsConsumed"), "refs": refs}
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
