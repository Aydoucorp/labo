#!/usr/bin/env python3
"""Legs {VID_MODEL} via KIE : jobs/legs.json [{"name","start","end"|null,"prompt","duration":"5"|"10"}]. Skip si OUT/<name>.mp4 existe."""
import json, os, sys, time, subprocess, urllib.request
import json as _j
def _resolve_key(jobs_path):
    if os.environ.get("KIE_API_KEY"): return os.environ["KIE_API_KEY"]
    d=os.path.dirname(os.path.abspath(jobs_path))
    for _ in range(4):
        p=os.path.join(d,".kie_key")
        if os.path.exists(p): return _j.load(open(p))["key"]
        p2=os.path.join(d,".keys.json")
        if os.path.exists(p2) and _j.load(open(p2)).get("kie"): return _j.load(open(p2))["kie"]
        d=os.path.dirname(d)
    raise SystemExit("Aucune clé KIE : déclarer <run>/.kie_key ({\"key\":...}) ou exporter KIE_API_KEY")
KEY=_resolve_key(sys.argv[1])
def _run_cfg(p):
    d=os.path.dirname(os.path.dirname(os.path.abspath(p)))
    try: return json.load(open(os.path.join(d,"run.json")))
    except Exception: return {}
_V=_run_cfg(sys.argv[1]).get("video") or {}
VID_MODEL=_V.get("model") or "kling-3.0/video"; VID_MODE=_V.get("mode","pro")   # défaut du process ; ou tout modèle KIE image-to-video collé par l'utilisateur
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
args = sys.argv[1:]; only = [a for a in args[1:] if not a.startswith("--")]
OUT = os.path.join(os.path.dirname(os.path.abspath(args[0])), "OUT"); os.makedirs(OUT, exist_ok=True)
RUN = os.path.dirname(os.path.dirname(os.path.abspath(args[0])))  # chemins start/end de legs.json relatifs au dossier du run
jobs = json.load(open(args[0]))
def api(path, body=None):
    for t in range(6):
        try:
            r = urllib.request.Request("https://api.kie.ai/api/v1/jobs/" + path, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                       headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY, "User-Agent": UA})
            return json.load(urllib.request.urlopen(r, timeout=60))
        except Exception as e:
            if t == 5: raise
            time.sleep(10 * (t + 1))
def gen(model, inp, tries=3):
    last = None
    for t in range(tries):
        try:
            j = api("createTask", {"model": model, "input": inp}); tid = (j.get("data") or {}).get("taskId")
            if not tid: raise RuntimeError("createTask KO: " + json.dumps(j)[:300])
            t0 = time.time()
            while time.time() - t0 < 2400:
                d = api("recordInfo?taskId=" + tid).get("data") or {}
                if d.get("state") == "success": return json.loads(d.get("resultJson") or "{}")["resultUrls"][0]
                if d.get("state") == "fail": raise RuntimeError("KIE fail: " + str(d.get("failMsg") or d.get("failCode")))
                time.sleep(8)
            raise RuntimeError("timeout KIE")
        except RuntimeError as e:
            last = e; print(f"  tentative {t+1} KO : {str(e)[:100]}", flush=True); time.sleep(10)
    raise last
def download(url, path):
    for t in range(4):
        try: open(path, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=600).read()); return
        except Exception:
            if t == 3: raise
            time.sleep(10)
def upload(path):
    for i in range(5):
        r = subprocess.run(["curl", "-s", "--max-time", "300", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload", "-H", f"Authorization: Bearer {KEY}",
                            "-F", f"file=@{path}", "-F", "uploadPath=zack-legs", "-F", f"fileName={int(time.time()*1000)}-{i}.png"], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            if d.get("data", {}).get("downloadUrl"): return d["data"]["downloadUrl"]
        except Exception: pass
        time.sleep(6)
    raise RuntimeError("upload KO " + path)
for job in jobs:
    n = job["name"]
    if only and n not in only: continue
    out = f"{OUT}/{n}.mp4"
    if os.path.exists(out): print(f"[{n}] existe, skip", flush=True); continue
    urls = [upload(os.path.join(RUN, job["start"]))]
    if job.get("end"): urls.append(upload(os.path.join(RUN, job["end"])))
    print(f"[{n}] {VID_MODEL} {job.get('duration','5')}s ({len(urls)} frames)…", flush=True)
    url = gen(VID_MODEL, {"prompt": job["prompt"], "image_urls": urls, "duration": job.get("duration", "5"), "aspect_ratio": "9:16", "mode": VID_MODE, "multi_shots": False, "sound": False})
    download(url, out); print(f"[{n}] → {out}", flush=True)
print("terminé")
