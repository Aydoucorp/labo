#!/usr/bin/env python3
"""Génère UNE image par job (modèle image KIE : run.json image.model, défaut gpt-image-2), text-to-image ou image-to-image avec refs.
   jobs.json : [{"name","prompt","negative","refs":[chemins...],"aspect":"9:16"}]. Skip si OUT/<name>.png existe."""
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
IMG_RES=(_run_cfg(sys.argv[1]).get("image") or {}).get("resolution") or "2K"   # studio : résolution choisie par l'utilisateur, écrite dans run.json image.resolution
IMG_MODEL=(_run_cfg(sys.argv[1]).get("image") or {}).get("model") or "gpt-image-2"   # défaut du process ; ou tout modèle KIE image-to-image collé par l'utilisateur (ex. gpt-image-2-5-sunburst)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
args = sys.argv[1:]; only = [a for a in args[1:] if not a.startswith("--")]
OUT = os.path.join(os.path.dirname(os.path.abspath(args[0])), "OUT"); os.makedirs(OUT, exist_ok=True)
jobs = json.load(open(args[0])); jobs = jobs if isinstance(jobs, list) else [jobs]
def api(path, body=None):
    for t in range(6):
        try:
            r = urllib.request.Request("https://api.kie.ai/api/v1/jobs/" + path, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                       headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY, "User-Agent": UA})
            return json.load(urllib.request.urlopen(r, timeout=60))
        except Exception as e:
            if t == 5: raise
            print(f"  réseau KO ({str(e)[:60]}) → nouvel essai", flush=True); time.sleep(10 * (t + 1))
def create(model, inp):
    j = api("createTask", {"model": model, "input": inp}); tid = (j.get("data") or {}).get("taskId")
    if not tid: raise RuntimeError("createTask KO: " + json.dumps(j)[:300])
    return tid
def wait(tid, tmax=1500):
    t0 = time.time()
    while time.time() - t0 < tmax:
        d = api("recordInfo?taskId=" + tid).get("data") or {}
        if d.get("state") == "success": return json.loads(d.get("resultJson") or "{}")["resultUrls"][0]
        if d.get("state") == "fail": raise RuntimeError("KIE fail: " + str(d.get("failMsg") or d.get("failCode")))
        time.sleep(6)
    raise RuntimeError("timeout KIE")
def gen(model, inp, tries=3):
    last = None
    for t in range(tries):
        try: return wait(create(model, inp))
        except RuntimeError as e:
            last = e; print(f"  tentative {t+1} KO : {str(e)[:80]}", flush=True); time.sleep(8)
            if t == 1 and inp.get("resolution") == "2K": inp = dict(inp, resolution="1K"); print("  → repli 1K", flush=True)
    raise last
def download(url, path):
    for t in range(4):
        try: open(path, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=300).read()); return
        except Exception as e:
            if t == 3: raise
            time.sleep(10)
_upcache = {}
def upload(path):
    if path in _upcache: return _upcache[path]
    for i in range(5):
        r = subprocess.run(["curl", "-s", "--max-time", "300", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload", "-H", f"Authorization: Bearer {KEY}",
                            "-F", f"file=@{path}", "-F", "uploadPath=zack-frames", "-F", f"fileName={int(time.time()*1000)}-{i}{os.path.splitext(path)[1]}"], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            if d.get("data", {}).get("downloadUrl"): _upcache[path] = d["data"]["downloadUrl"]; return _upcache[path]
        except Exception: pass
        time.sleep(6)
    raise RuntimeError("upload KO " + path)
for job in jobs:
    name = job["name"]
    if only and name not in only: continue
    out = f"{OUT}/{name}.png"
    if os.path.exists(out): print(f"[{name}] existe, skip", flush=True); continue
    prompt = job["prompt"] + "\n\nNEGATIVE: " + job.get("negative", "")
    RUN = os.path.dirname(os.path.dirname(os.path.abspath(args[0])))
    refs = [os.path.join(RUN, r) if not os.path.isabs(r) else r for r in job.get("refs", [])]
    print(f"[{name}] gen ({'i2i ' + str(len(refs)) + ' refs' if refs else 't2i'})…", flush=True)
    if refs:
        url = gen(IMG_MODEL+"-image-to-image", {"prompt": prompt, "input_urls": [upload(r) for r in refs], "aspect_ratio": job.get("aspect", "9:16"), "resolution": IMG_RES})
    else:
        url = gen(IMG_MODEL+"-text-to-image", {"prompt": prompt, "aspect_ratio": job.get("aspect", "9:16"), "resolution": IMG_RES})
    download(url, out); print(f"[{name}] → {out}", flush=True)
print("terminé")
