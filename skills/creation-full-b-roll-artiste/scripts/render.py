#!/usr/bin/env python3
"""render.py : rend la video finale avec Remotion puis normalise le son.

Etapes :
  1. rassemble clips, voix off, musique, captions et sfx dans assets/remotion/public/render/
     (liens durs si possible, sinon copies) et reecrit un timeline.json avec des chemins
     relatifs a public/ ;
  2. `npm install` au premier usage (node_modules absent) ;
  3. `npx remotion render src/index.ts Main|Preview ... --codec=h264 --crf=18 --concurrency=2`
     avec le navigateur detecte (--browser, BROLL_BROWSER, chromium Playwright si present,
     sinon Remotion telecharge le sien) ;
  4. loudnorm ffmpeg en deux passes sur la piste audio (I = vo_lufs du profil, TP -1.5, LRA 11)
     puis mux avec la video (copie) ;
  5. ecrit out/final.srt (depuis captions.json, pages de 4 mots max) et out/timeline.json.

--preview rend la composition "Preview" (540x960) pour un aller-retour rapide.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from montage_common import (REMOTION_DIR, STRONG_PUNCT, die, ffprobe_duration, get_profile, load_json,
                    load_profiles, log, project_root_from_timeline, resolve_asset, save_json, which)

PUBLIC_RENDER = "render"
SRT_COMBINE_MS = 900
SRT_MAX_TOKENS = 4


def find_browser(explicit: str | None) -> tuple[str | None, str | None]:
    """Chemin du navigateur et chrome-mode Remotion correspondant."""
    candidates: list[str] = []
    if explicit:
        candidates.append(explicit)
    for var in ("BROLL_BROWSER", "REMOTION_BROWSER_EXECUTABLE", "PUPPETEER_EXECUTABLE_PATH"):
        if os.environ.get(var):
            candidates.append(os.environ[var])
    # Emplacements Playwright usuels (le chromium complet marche en mode chrome-for-testing)
    pw_roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "/opt/pw-browsers", str(Path.home() / ".cache" / "ms-playwright")]
    for root in pw_roots:
        if not root:
            continue
        candidates.append(os.path.join(root, "chromium"))
        candidates += sorted(glob.glob(os.path.join(root, "chromium-*", "chrome-linux", "chrome")), reverse=True)
        candidates += sorted(glob.glob(os.path.join(root, "chromium_headless_shell-*", "chrome-linux", "headless_shell")), reverse=True)
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome-headless-shell"):
        w = which(name)
        if w:
            candidates.append(w)
    for c in candidates:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            mode = "headless-shell" if "headless" in os.path.basename(c) else "chrome-for-testing"
            return c, mode
    return None, None


def ensure_node_modules(remotion_dir: Path) -> None:
    if (remotion_dir / "node_modules" / "remotion").exists():
        return
    npm = which("npm")
    if not npm:
        die("npm introuvable dans le PATH (Node 22 requis pour Remotion)")
    log("npm install (premier usage)...")
    t0 = time.time()
    res = subprocess.run([npm, "install", "--no-audit", "--no-fund"], cwd=str(remotion_dir))
    if res.returncode != 0:
        die("npm install a echoue")
    log(f"npm install termine en {time.time() - t0:.0f} s")


def link_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def stage_assets(timeline: dict, root: Path, public: Path) -> dict:
    """Copie les ressources dans public/render/ et retourne un timeline aux chemins publics."""
    render_dir = public / PUBLIC_RENDER
    if render_dir.exists():
        shutil.rmtree(render_dir)
    render_dir.mkdir(parents=True)
    used: set[str] = set()

    def stage(path: str | None, sub: str) -> str | None:
        if not path:
            return None
        src = resolve_asset(path, root)
        if src is None:
            die(f"ressource introuvable : {path} (ni dans le projet {root}, ni dans le skill)")
        name = src.name
        key = f"{sub}/{name}"
        if key in used and not (render_dir / sub / name).samefile(src):
            name = f"{src.parent.name}_{name}"
            key = f"{sub}/{name}"
        used.add(key)
        link_or_copy(src, render_dir / sub / name)
        return f"{PUBLIC_RENDER}/{sub}/{name}"

    tl = json.loads(json.dumps(timeline))
    for clip in tl["clips"]:
        clip["src"] = stage(clip["src"], "clips")
    tl["audio"]["vo"] = stage(tl["audio"].get("vo"), "audio")
    tl["audio"]["music"] = stage(tl["audio"].get("music"), "audio")
    tl["captions"]["file"] = stage(tl["captions"]["file"], "captions")
    for s in tl.get("sfx", []):
        s["src"] = stage(s["src"], "sfx")
    save_json(render_dir / "timeline.json", tl)
    return tl


def loudnorm_two_pass(video_in: Path, out: Path, target_i: float, tp: float = -1.5, lra: float = 11.0) -> dict:
    """Normalise la piste audio (deux passes) et remuxe avec la video copiee."""
    base = f"loudnorm=I={target_i}:TP={tp}:LRA={lra}"
    p1 = subprocess.run(["ffmpeg", "-v", "info", "-nostdin", "-i", str(video_in), "-af", base + ":print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr, re.S)
    if not m:
        raise RuntimeError("loudnorm passe 1 : mesure introuvable\n" + p1.stderr[-1500:])
    meas = json.loads(m.group(0))
    bad = any(meas[k] in ("-inf", "inf") for k in ("input_i", "input_tp", "input_lra", "input_thresh"))
    if bad:
        log("loudnorm : piste quasi silencieuse, normalisation en une passe")
        af = base
    else:
        af = (f"{base}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:measured_LRA={meas['input_lra']}"
              f":measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true")
    out.parent.mkdir(parents=True, exist_ok=True)
    p2 = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(video_in), "-map", "0:v:0", "-map", "0:a:0",
                         "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                         "-movflags", "+faststart", str(out)], capture_output=True, text=True)
    if p2.returncode != 0:
        raise RuntimeError("loudnorm passe 2 : " + p2.stderr[-1500:])
    return meas


def ms_to_srt(ms: int) -> str:
    ms = max(0, int(ms))
    h, rem = divmod(ms, 3600000)
    mnt, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{mnt:02d}:{s:02d},{ms:03d}"


def captions_to_srt(captions: list[dict]) -> str:
    """Pages de 4 mots max, regroupees dans une fenetre de 900 ms, coupees sur ponctuation forte."""
    pages: list[list[dict]] = []
    cur: list[dict] = []
    for c in captions:
        if cur and (len(cur) >= SRT_MAX_TOKENS or c["startMs"] - cur[0]["startMs"] > SRT_COMBINE_MS):
            pages.append(cur)
            cur = []
        cur.append(c)
        text = c["text"].strip()
        if c.get("pageBreakAfter") or any(text.endswith(p) for p in STRONG_PUNCT):
            pages.append(cur)
            cur = []
    if cur:
        pages.append(cur)
    lines = []
    for i, page in enumerate(pages):
        start = page[0]["startMs"]
        end = page[-1]["endMs"]
        if i + 1 < len(pages):
            end = min(pages[i + 1][0]["startMs"], end + 700)
        else:
            end += 500
        text = "".join(c["text"] for c in page).strip()
        lines.append(f"{i + 1}\n{ms_to_srt(start)} --> {ms_to_srt(end)}\n{text}\n")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Rend la video finale (Remotion + loudnorm) a partir de work/timeline.json.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("timeline", help="work/timeline.json")
    ap.add_argument("--out", required=True, help="fichier de sortie, ex. out/final_9x16.mp4")
    ap.add_argument("--preview", action="store_true", help="rend la composition Preview (540x960), rapide")
    ap.add_argument("--profiles", default=None, help="assets/profiles.json (defaut : celui du skill)")
    ap.add_argument("--project", default=None, help="racine du projet (defaut : parent de work/)")
    ap.add_argument("--browser", default=None, help="executable Chromium/Chrome (defaut : detection automatique)")
    ap.add_argument("--concurrency", type=int, default=2, help="onglets Chrome en parallele (defaut 2)")
    ap.add_argument("--crf", type=int, default=18, help="qualite H.264 (defaut 18)")
    ap.add_argument("--cache-mb", type=int, default=512,
                    help="cache de frames OffthreadVideo en Mo (defaut 512 ; reduire si le compositeur est tue par manque de memoire)")
    ap.add_argument("--no-retry", action="store_true", help="ne pas retenter en concurrence 1 si le rendu echoue")
    ap.add_argument("--progress-bar", action="store_true", help="active la barre de progression fine")
    ap.add_argument("--logo", default=None, help="PNG de logo (copie dans public/render/)")
    ap.add_argument("--no-loudnorm", action="store_true", help="ne pas normaliser le son")
    ap.add_argument("--keep-raw", action="store_true", help="conserver le rendu brut avant loudnorm")
    ap.add_argument("--frames", default=None,
                    help="liste de frames (ex. 14,46,330) : rend ces images PNG dans le dossier --out au lieu d'une video")
    args = ap.parse_args()

    t_all = time.time()
    tl_path = Path(args.timeline).resolve()
    timeline = load_json(tl_path)
    root = Path(args.project).resolve() if args.project else project_root_from_timeline(tl_path)
    profile = get_profile(load_profiles(args.profiles), timeline["profile"])
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if not which("npx"):
        die("npx introuvable dans le PATH (ajoutez le dossier bin de Node 22 au PATH)")
    ensure_node_modules(REMOTION_DIR)

    public = REMOTION_DIR / "public"
    staged = stage_assets(timeline, root, public)
    props: dict = {"timelinePath": f"{PUBLIC_RENDER}/timeline.json", "progressBar": bool(args.progress_bar), "logo": None}
    if args.logo:
        lp = Path(args.logo)
        if not lp.exists():
            die(f"logo introuvable : {args.logo}")
        link_or_copy(lp, public / PUBLIC_RENDER / "logo" / lp.name)
        props["logo"] = f"{PUBLIC_RENDER}/logo/{lp.name}"
    props_path = public / PUBLIC_RENDER / "props.json"
    save_json(props_path, props)

    browser, mode = find_browser(args.browser)
    comp = "Preview" if args.preview else "Main"
    browser_args = [f"--browser-executable={browser}", f"--chrome-mode={mode}"] if browser else []
    if browser:
        log(f"navigateur : {browser} ({mode})")
    else:
        log("navigateur : aucun trouve, Remotion telechargera Chrome Headless Shell")

    if args.frames:
        # Images fixes de controle : --out est alors un dossier
        out.mkdir(parents=True, exist_ok=True)
        cmd = ["npx", "remotion", "render", "src/index.ts", comp, str(out), f"--props={props_path}",
               f"--frames={args.frames}", "--image-format=png", f"--concurrency={args.concurrency}", "--log=warn",
               "--timeout=120000", *browser_args]
        t0 = time.time()
        res = subprocess.run(cmd, cwd=str(REMOTION_DIR))
        if res.returncode != 0:
            die(f"le rendu des images a echoue (code {res.returncode})")
        log(f"images rendues dans {out} en {time.time() - t0:.1f} s")
        return

    raw = out.with_name(out.stem + ".raw.mp4")

    def render_cmd(concurrency: int, cache_mb: int) -> list[str]:
        return ["npx", "remotion", "render", "src/index.ts", comp, str(raw), f"--props={props_path}",
                "--codec=h264", f"--crf={args.crf}", f"--concurrency={concurrency}", "--log=warn",
                "--timeout=120000", f"--offthreadvideo-cache-size-in-bytes={cache_mb * 1024 * 1024}", *browser_args]

    attempts = [(args.concurrency, args.cache_mb)]
    if not args.no_retry:
        attempts.append((1, max(128, args.cache_mb // 2)))
    t0 = time.time()
    res = None
    for i, (conc, cache_mb) in enumerate(attempts):
        cmd = render_cmd(conc, cache_mb)
        log(f"rendu Remotion ({comp}, tentative {i + 1}/{len(attempts)}) : {' '.join(cmd)}")
        res = subprocess.run(cmd, cwd=str(REMOTION_DIR))
        if res.returncode == 0 and raw.exists():
            break
        log(f"echec du rendu (code {res.returncode}), nouvelle tentative plus frugale" if i + 1 < len(attempts) else "")
    t_render = time.time() - t0
    if res is None or res.returncode != 0 or not raw.exists():
        die(f"le rendu Remotion a echoue (code {res.returncode if res else '?'})")
    log(f"rendu termine en {t_render:.1f} s ({staged['duration_frames']} frames)")

    t0 = time.time()
    if args.no_loudnorm:
        shutil.move(str(raw), str(out))
        meas = None
    else:
        meas = loudnorm_two_pass(raw, out, float(profile["vo_lufs"]))
        if not args.keep_raw:
            raw.unlink(missing_ok=True)
    t_audio = time.time() - t0

    # Sous-titres SRT et copie du timeline
    cap_path = resolve_asset(timeline["captions"]["file"], root)
    if cap_path:
        caps = load_json(cap_path).get("captions", [])
        (out.parent / "final.srt").write_text(captions_to_srt(caps), encoding="utf-8")
    if (out.parent / "timeline.json").resolve() != tl_path:
        save_json(out.parent / "timeline.json", timeline)

    dur = ffprobe_duration(out)
    report = {
        "output": str(out), "composition": comp, "render_s": round(t_render, 1), "audio_s": round(t_audio, 1),
        "total_s": round(time.time() - t_all, 1), "duration_s": dur,
        "loudnorm_measured": meas, "browser": browser,
    }
    save_json(out.parent / ("render_report_preview.json" if args.preview else "render_report.json"), report)
    log(f"OK : {out} ({dur} s) ; rendu {t_render:.1f} s, audio {t_audio:.1f} s, total {report['total_s']} s")


if __name__ == "__main__":
    main()
