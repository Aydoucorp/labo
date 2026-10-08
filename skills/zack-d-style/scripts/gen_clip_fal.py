#!/usr/bin/env python3
"""Clips via FAL · MiniMax H3 Max Turbo image-to-video (start + end frame), en parallèle. Même interface que gen_clip.py :
   legs.json [{"name","start","end"|null,"prompt","duration"}] → OUT/<name>.mp4. Skip si le mp4 existe.
   Clé FAL : env FAL_KEY ou ~/.claude/.keys/fal.env. Upload des frames via KIE (URL publique acceptée par FAL).
   Usage: gen_clip_fal.py legs.json [names...] [--par N] [--res 1080P|768P|480P]
   Testé 14/09/26 : 13 s le clip, 1076×1928 24 fps, promo 0,02 $/s en 1080P."""
import json, os, sys, time, subprocess, urllib.request, threading
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
def _kie_key(p):
    if os.environ.get("KIE_API_KEY"): return os.environ["KIE_API_KEY"]
    d = os.path.dirname(os.path.abspath(p))
    for _ in range(5):
        f = os.path.join(d, ".kie_key")
        if os.path.exists(f): return json.load(open(f))["key"]
        f2 = os.path.join(d, ".keys.json")
        if os.path.exists(f2) and json.load(open(f2)).get("kie"): return json.load(open(f2))["kie"]
        d = os.path.dirname(d)
    raise SystemExit("clé KIE introuvable (upload des frames)")
def _fal_key():
    if os.environ.get("FAL_KEY"): return os.environ["FAL_KEY"]
    d = os.path.dirname(os.path.abspath(JOBS))
    for _ in range(5):
        f = os.path.join(d, ".keys.json")
        if os.path.exists(f):
            k = json.load(open(f)).get("fal")
            if k: return k
        d = os.path.dirname(d)
    f = os.path.expanduser("~/.claude/.keys/fal.env")
    if os.path.exists(f): return open(f).read().strip().split("=", 1)[1]
    raise SystemExit("clé FAL introuvable (~/.claude/.keys/fal.env)")
args = sys.argv[1:]; JOBS = args[0]; KIE = _kie_key(JOBS); FAL = _fal_key()
RUN = os.path.dirname(os.path.dirname(os.path.abspath(JOBS)))  # legs.json est dans <run>/jobs/
OUT = os.path.join(os.path.dirname(os.path.abspath(JOBS)), "OUT"); os.makedirs(OUT, exist_ok=True)
PAR = int(args[args.index("--par") + 1]) if "--par" in args else 6
RES = args[args.index("--res") + 1] if "--res" in args else "1080P"
only = [a for a in args[1:] if not a.startswith("--") and a != str(PAR) and a != RES]
def _run_cfg(p):
    d=os.path.dirname(os.path.dirname(os.path.abspath(p))); f=os.path.join(d,"run.json")
    try: return json.load(open(f))
    except Exception: return {}
_CFG=_run_cfg(JOBS).get("video",{})
MODEL = (args[args.index("--model")+1] if "--model" in args else None) or _CFG.get("model") or "minimax/h3-max-turbo/image-to-video"   # tout endpoint FAL image-to-video start/end
MIN_D = int(_CFG.get("min_duration",5)); MAX_D = int(_CFG.get("max_duration",10))
H = {"Authorization": "Key " + FAL, "Content-Type": "application/json"}
_up_cache = {}; _lock = threading.Lock()
def upload(p):
    p = p if os.path.isabs(p) else os.path.join(RUN, p)
    with _lock:
        if p in _up_cache: return _up_cache[p]
    for i in range(4):
        r = subprocess.run(["curl", "-s", "--max-time", "300", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload", "-H", f"Authorization: Bearer {KIE}",
                            "-F", f"file=@{p}", "-F", "uploadPath=fal-legs", "-F", f"fileName={int(time.time()*1000)}-{i}-{os.path.basename(p)}"], capture_output=True, text=True)
        try:
            u = json.loads(r.stdout)["data"]["downloadUrl"]
            with _lock: _up_cache[p] = u
            return u
        except Exception: time.sleep(5)
    raise RuntimeError("upload KO " + p)
def fal(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=H, method="POST" if body else "GET")
    try: return json.load(urllib.request.urlopen(r, timeout=120))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur {url.split('/')[-1]} : {e.read().decode()[:300]}")
def gen(job):
    n = job["name"]; out = f"{OUT}/{n}.mp4"
    if os.path.exists(out): print(f"[{n}] déjà là", flush=True); return
    body = {"prompt": job["prompt"], "image_url": upload(job["start"]), "duration": max(MIN_D, min(MAX_D, int(job.get("duration", 5)))), "resolution": RES, "prompt_expansion_mode": "balanced"}  # H3 : 5 s minimum (validé au run, pas au submit) — l'utilisateur recale au montage
    if job.get("end"): body["end_image_url"] = upload(job["end"])
    print(f"[{n}] H3 Max Turbo {body['duration']}s ({'2' if job.get('end') else '1'} frame{'s' if job.get('end') else ''})…", flush=True)
    t0 = time.time()
    for attempt in range(3):
        try:
            j = fal(f"https://queue.fal.run/{MODEL}", body); break
        except RuntimeError as e:
            msg = str(e)
            if "HTTP 422" in msg and "duration" in msg and body["duration"] != 5:   # durée refusée → 5 s (l'utilisateur recale au montage)
                print(f"[{n}] durée {body['duration']} refusée → 5 s", flush=True); body["duration"] = 5; continue
            if attempt == 2: raise RuntimeError("submit KO " + msg)
            time.sleep(5)
    rid = j["request_id"]; su = j.get("status_url") or f"https://queue.fal.run/{MODEL}/requests/{rid}/status"; ru = j.get("response_url") or f"https://queue.fal.run/{MODEL}/requests/{rid}"
    while True:
        st = fal(su)
        if st.get("status") == "COMPLETED": break
        if st.get("status") not in ("IN_QUEUE", "IN_PROGRESS"): raise RuntimeError(f"statut {st}")
        time.sleep(3)
    res = fal(ru)
    for i in range(4):
        try: open(out, "wb").write(urllib.request.urlopen(urllib.request.Request(res["video"]["url"], headers={"User-Agent": UA}), timeout=300).read()); break
        except Exception: time.sleep(5)
    try: json.dump({"request_id": rid, "duration": body["duration"], "timings": res.get("timings"), "model": MODEL}, open(out + ".json", "w"))
    except Exception: pass
    print(f"[{n}] → {out} ({int(time.time()-t0)} s)", flush=True)
jobs = [j for j in json.load(open(JOBS)) if not only or j["name"] in only]
errs = []; sem = threading.Semaphore(PAR)
def work(j):
    with sem:
        try: gen(j)
        except Exception as e: errs.append(j["name"]); print(f"[{j['name']}] KO : {str(e)[:200]}", flush=True)
th = [threading.Thread(target=work, args=(j,)) for j in jobs]
for t in th: t.start()
for t in th: t.join()
print("terminé" + (f" — KO : {', '.join(errs)}" if errs else ""), flush=True)
