# Z-Image (KIE, texte vers image uniquement) : python3 work/zimage.py prompt.txt ratio sortie.png
import sys, json, time, urllib.request, pathlib
sys.path.insert(0, "/home/user/labo/scripts")
from kie_image import call, API
p, ratio, out = sys.argv[1:4]
t = call(f"{API}/createTask", {"model": "z-image", "input": {"prompt": pathlib.Path(p).read_text().strip(), "aspect_ratio": ratio}})
if t.get("code") != 200: sys.exit(f"refus {t.get('code')} {t.get('msg')}")
tid = t["data"]["taskId"]
for _ in range(120):
    time.sleep(4); d = call(f"{API}/recordInfo?taskId={tid}")["data"]
    if d["state"] in ("success", "fail"): break
r = {"taskId": tid, "state": d["state"], "credits": d.get("creditsConsumed")}
if d["state"] == "success":
    urllib.request.urlretrieve(json.loads(d["resultJson"])["resultUrls"][0], out); r["file"] = out
else: r["error"] = d.get("failMsg")
print(json.dumps(r))
