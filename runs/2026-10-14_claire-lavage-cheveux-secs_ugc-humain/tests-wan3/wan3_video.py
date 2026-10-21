#!/usr/bin/env python3
"""Test Wan 3.0 (KIE wan/3-0-video) : références images + voix en audio de référence (@Audio1).
   wan3_video.py prompt.txt sortie.mp4 --image a.png b.png --audio voix.wav --duration 9 --resolution 480P"""
import sys, json, time, urllib.request, pathlib, argparse
sys.path.insert(0, "/home/user/labo/scripts")
from kie_image import API, call, upload
ap = argparse.ArgumentParser(); ap.add_argument("prompt"); ap.add_argument("out")
ap.add_argument("--image", nargs="*", default=[]); ap.add_argument("--audio", nargs="*", default=[])
ap.add_argument("--duration", type=int, default=5); ap.add_argument("--resolution", default="480P"); ap.add_argument("--ratio", default="9:16")
a = ap.parse_args()
inp = {"prompt": pathlib.Path(a.prompt).read_text(), "duration": a.duration, "resolution": a.resolution,
       "aspect_ratio": a.ratio, "audio": True}
if a.image: inp["reference_image_urls"] = [upload(i) for i in a.image]
if a.audio: inp["reference_audio_urls"] = [upload(x) for x in a.audio]
t = call(f"{API}/createTask", {"model": "wan/3-0-video", "input": inp})
if t.get("code") != 200: sys.exit(f"refusé : {t.get('code')} {t.get('msg')}")
tid = t["data"]["taskId"]
for _ in range(360):
    time.sleep(5)
    d = call(f"{API}/recordInfo?taskId={tid}")["data"]
    if d["state"] in ("success", "fail"): break
r = {"taskId": tid, "state": d["state"], "credits": d.get("creditsConsumed")}
if d["state"] == "success":
    urllib.request.urlretrieve(json.loads(d["resultJson"])["resultUrls"][0], a.out); r["file"] = a.out
else: r["error"] = d.get("failMsg")
print(json.dumps(r, ensure_ascii=False))
