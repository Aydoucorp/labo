#!/usr/bin/env python3
"""Construit la piste voix hybride et montage.json du talking head Claire (cheveux gris et carences).

Voix : passages avatar = voix générée par Seedance 2.5 dans chaque clip (lèvres synchrones) ;
autres plans = voix off d'origine (voix.mp3). Les morceaux sont mis bout à bout, chaque morceau
est ramené au même volume, avec de courts fondus pour éviter les clics.
Tous les temps de montage.json sont exprimés sur cette nouvelle piste (public/audio/voix_montage.wav).

Usage (depuis le dossier du run) :
  python3 montage/construire_montage.py              -> v1, voix hybride (montage.json)
  python3 montage/construire_montage.py --voix-off   -> v2, voix off d'origine partout, son Seedance coupé,
                                                        clips avatar recalés phrase par phrase sur la voix off (montage_voixoff.json)
"""
import json, pathlib, re, shutil, subprocess, sys

VOIX_OFF = "--voix-off" in sys.argv
SUF = "_cale" if VOIX_OFF else ""

RUN = pathlib.Path(__file__).resolve().parent.parent
M = RUN / "montage"
PUB = M / "public"
SR = 48000

# Morceaux de la piste voix, dans l'ordre. Avatar : bornes de parole mesurées (silencedetect -40 dB) sur le son
# du clip Seedance retenu. Voix off : bornes prises dans les silences de voix.mp3 (mots.json).
PIECES = [
    {"id": "S01", "src": "retenues/avatar_voix/S01.mp4", "speech": (0.32, 5.61)},
    {"id": "A01", "src": "retenues/avatar_voix/A01.mp4", "speech": (0.27, 8.81)},
    {"id": "M1", "src": "voix.mp3", "cut": (14.25, 22.75)},
    {"id": "A02", "src": "retenues/avatar_voix/A02.mp4", "speech": (0.44, 3.20)},
    {"id": "M2", "src": "voix.mp3", "cut": (25.64, 28.48)},
    {"id": "A03", "src": "retenues/avatar_voix/A03.mp4", "speech": (0.26, 6.57)},
    {"id": "M3", "src": "voix.mp3", "cut": (35.40, 42.95)},
    {"id": "A04", "src": "retenues/avatar_voix/A04.mp4", "speech": (1.60, 2.58)},
    {"id": "M4", "src": "voix.mp3", "cut": (44.64, 51.08)},
    {"id": "A05", "src": "retenues/avatar_voix/A05.mp4", "speech": (0.15, 5.84)},
]
PAD_IN, PAD_OUT = 0.12, 0.16  # marge avant le premier mot / après le dernier mot d'un clip avatar
TARGET_LUFS = -18.0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).stdout)


def lufs(path):
    err = subprocess.run(["ffmpeg", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def build_audio():
    tmp = M / "tmp_audio"
    tmp.mkdir(exist_ok=True)
    t = 0.0
    parts = []
    for p in PIECES:
        src = RUN / p["src"]
        if "speech" in p:
            a = max(0.0, p["speech"][0] - PAD_IN)
            b = min(duration(src), p["speech"][1] + PAD_OUT)
        else:
            a, b = p["cut"]
        p["in"], p["out"], p["start"] = a, b, round(t, 3)
        raw = tmp / f"{p['id']}_raw.wav"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(src), "-vn", "-ac", "1", "-ar", str(SR), str(raw)])
        gain = TARGET_LUFS - lufs(raw)
        d = b - a
        out = tmp / f"{p['id']}.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
             f"volume={gain:.2f}dB,afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.3f}:d=0.03", "-ac", "1", "-ar", str(SR), str(out)])
        p["gain_db"] = round(gain, 2)
        parts.append(out)
        t += d
        p["end"] = round(t, 3)
    lst = tmp / "liste.txt"
    lst.write_text("".join(f"file '{x}'\n" for x in parts))
    (PUB / "audio").mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ac", "2", "-ar", str(SR), str(PUB / "audio/voix_montage.wav")])
    return t


P = {}  # id -> morceau


def at(pid, x):
    """Temps sur la piste montée d'un instant x du fichier source du morceau pid."""
    p = P[pid]
    return round(p["start"] + (x - p["in"]), 3)


def clip_start(pid):
    """Temps sur la piste montée de l'image 0 du clip avatar (champ clipStart du gabarit)."""
    if "clip0" in P[pid]:
        return P[pid]["clip0"]
    return round(P[pid]["start"] - P[pid]["in"], 3)


# v2 : coupes de la voix off d'origine (dans ses silences), une par passage du découpage.
CUTS_VOIX_OFF = [("S01", 0.0, 5.9), ("A01", 5.9, 14.25), ("M1", 14.25, 23.2), ("A02", 23.2, 25.64), ("M2", 25.64, 28.95),
                 ("A03", 28.95, 35.40), ("M3", 35.40, 43.40), ("A04", 43.40, 44.64), ("M4", 44.64, 51.40), ("A05", 51.40, None)]


def build_audio_voix_off():
    src = RUN / "voix.mp3"
    total = duration(src)
    (PUB / "audio").mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "2", "-ar", str(SR), str(PUB / "audio/voix_off.wav")])
    for p, (pid, a, b) in zip(PIECES, CUTS_VOIX_OFF):
        assert p["id"] == pid
        b = total if b is None else b
        p["in"], p["out"], p["start"], p["end"], p["gain_db"] = a, b, a, b, 0.0
    return total


def phrase_anchors(clip_ws, master_ws, onset, speech_end):
    """Points de calage (temps clip, temps voix off) : début de chaque phrase ou reprise après une pause, et fin de parole."""
    anchors = [(onset, master_ws[0]["s"])]
    for i in range(1, len(master_ws)):
        prev = master_ws[i - 1]
        if re.search(r"[.,:;!?]$", prev["w"]) or master_ws[i]["s"] - prev["e"] > 0.25:
            anchors.append((clip_ws[i]["s"], master_ws[i]["s"]))
    anchors.append((speech_end, master_ws[-1]["e"]))
    # temps croissants des deux côtés
    out = [anchors[0]]
    for c, m in anchors[1:]:
        if c > out[-1][0] + 0.1 and m > out[-1][1] + 0.1:
            out.append((c, m))
    return out


def warp_clip(pid, clip_ws, master_ws, speech, a, b):
    """Recale un clip avatar sur la voix off : chaque phrase du clip est légèrement ralentie ou accélérée
    pour que ses lèvres tombent sur la même phrase de la voix off. L'image 0 du fichier obtenu = temps a."""
    src = PUB / f"avatar/{pid}.mp4"
    tmp = M / "tmp_cale" / pid
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "src").mkdir(parents=True)
    run(["ffmpeg", "-v", "error", "-i", str(src), str(tmp / "src/%05d.png")])
    n = len(list((tmp / "src").glob("*.png")))
    anchors = phrase_anchors(clip_ws, master_ws, *speech)
    ms = [m for _, m in anchors]
    cs = [c for c, _ in anchors]

    def clip_time(t):
        if t <= ms[0]:
            return cs[0] - (ms[0] - t)
        if t >= ms[-1]:
            return cs[-1] + (t - ms[-1])
        for k in range(len(ms) - 1):
            if ms[k] <= t <= ms[k + 1]:
                return cs[k] + (t - ms[k]) * (cs[k + 1] - cs[k]) / (ms[k + 1] - ms[k])

    (tmp / "seq").mkdir()
    frames = int(round((b - a) * 30)) + 1
    for f in range(frames):
        idx = min(n, max(1, int(round(clip_time(a + f / 30) * 30)) + 1))
        (tmp / "seq" / f"{f:05d}.png").symlink_to(tmp / "src" / f"{idx:05d}.png")
    out = PUB / f"avatar/{pid}_cale.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", str(tmp / "seq/%05d.png"), "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "17", "-pix_fmt", "yuv420p", str(out)])
    shutil.rmtree(tmp)
    speeds = [round((cs[k + 1] - cs[k]) / (ms[k + 1] - ms[k]), 2) for k in range(len(ms) - 1)]
    return speeds


# Texte des sous-titres : le script fait foi (orthographe), les temps viennent de l'audio.
SCRIPT = {
    "S01": "Si vos cheveux deviennent gris dès la trentaine ou la quarantaine, ce n'est pas juste la génétique.",
    "A01": "Seulement 30 % du blanchiment précoce est héréditaire. Les 70 % restants, c'est votre corps qui vous envoie un signal.",
    "A02": "Avec l'âge, ou en cas de carences,",
    "A03": "Trois carences reviennent sans arrêt. La vitamine B12, le cuivre et le fer.",
    "A04": "Dans l'assiette :",
    "A05": "Et si vous voulez le protocole complet, écrivez « GUIDE » et je vous envoie mon guide gratuit.",
}
MASTER_FIX = {"carence,": "carences,", "légumineuse.": "légumineuses."}


def merge_tokens(ws):
    """Recolle les élisions (n + 'est), le signe % et les guillemets à leur mot."""
    out = []
    for w in ws:
        txt = w["w"]
        if out and (txt.startswith("'") or txt in ("%", "»")):
            out[-1] = {"w": out[-1]["w"] + ("\u00a0" + txt if txt in ("%", "»") else txt), "s": out[-1]["s"], "e": w["e"]}
        elif out and out[-1]["w"] == "«":
            out[-1] = {"w": "«\u00a0" + txt, "s": out[-1]["s"], "e": w["e"]}
        else:
            out.append(dict(w))
    return out


def script_words(txt):
    txt = txt.replace(" %", "\u00a0%").replace("« ", "«\u00a0").replace(" »", "\u00a0»").replace(" :", "\u00a0:")
    return txt.split(" ")


def subtitle_words():
    master = json.load(open(RUN / "mots.json"))
    avatar = json.load(open(M / "mots_avatar.json"))
    words = []
    for p in PIECES:
        pid = p["id"]
        if pid.startswith("M") or VOIX_OFF:
            ws = [w for w in master if p["in"] <= w["s"] < p["out"]]
            ws = merge_tokens(ws)
            # « peroxyde de l'hydrogène » (voix) -> « peroxyde d'hydrogène » (script)
            fixed = []
            for w in ws:
                if w["w"] == "l'hydrogène" and fixed and fixed[-1]["w"] == "de":
                    fixed[-1] = {"w": "d'hydrogène", "s": fixed[-1]["s"], "e": w["e"]}
                else:
                    fixed.append({**w, "w": MASTER_FIX.get(w["w"], w["w"])})
            for i, w in enumerate(fixed):
                words.append({"w": w["w"], "s": at(pid, w["s"]), "e": at(pid, w["e"]), **({"br": True} if i == 0 else {})})
        else:
            ws = merge_tokens(avatar[pid])
            target = script_words(SCRIPT[pid])
            if len(ws) != len(target):
                raise SystemExit(f"{pid} : {len(ws)} mots entendus pour {len(target)} dans le script")
            onset = p["speech"][0]
            for i, (w, txt) in enumerate(zip(ws, target)):
                s = max(w["s"], onset) if i == 0 else w["s"]
                words.append({"w": txt, "s": at(pid, s), "e": at(pid, max(w["e"], s + 0.08)), **({"br": True} if i == 0 else {})})
    return words


def word_time(words, text, after=0.0):
    for w in words:
        if w["s"] >= after and w["w"].strip(",.:«»\u00a0").lower().startswith(text.lower()):
            return w["s"]
    raise SystemExit(f"mot introuvable : {text}")


def main():
    total = build_audio_voix_off() if VOIX_OFF else build_audio()
    for p in PIECES:
        P[p["id"]] = p
    words = subtitle_words()
    if VOIX_OFF:
        master = json.load(open(RUN / "mots.json"))
        avatar = json.load(open(M / "mots_avatar.json"))
        for p in PIECES:
            if p["id"].startswith("M"):
                continue
            mw = merge_tokens([w for w in master if p["in"] <= w["s"] < p["out"]])
            cw = merge_tokens(avatar[p["id"]])
            if len(mw) != len(cw):
                raise SystemExit(f"{p['id']} : {len(cw)} mots dans le clip, {len(mw)} dans la voix off")
            speeds = warp_clip(p["id"], cw, mw, p["speech"], p["start"], p["end"])
            p["clip0"] = p["start"]
            print(f"{p['id']} recalé, vitesses par phrase : {speeds}")
    wt = lambda t, after=0.0: word_time(words, t, after)

    s01, a01, m1, a02, m2, a03, m3, a04, m4, a05 = (P[k] for k in ["S01", "A01", "M1", "A02", "M2", "A03", "M3", "A04", "M4", "A05"])
    t_ce = wt("ce")
    t_les70 = wt("Les", a01["start"])
    t_la_vit = wt("La", a03["start"])
    t_ecrivez = wt("écrivez")
    t_foods = [wt(x, m4["start"]) for x in ["foie", "fruits", "œufs", "viande", "légumineuses"]]
    t_et_soleil = wt("Et", m4["start"])

    AV = {"faceY": 0.22}
    segments = [
        {"type": "split", "start": 0.0, "end": s01["end"], "src": f"avatar/S01{SUF}.mp4", "clipStart": clip_start("S01"),
         "banner": "Cheveux blancs à 35 ans ? Ce n'est pas que la génétique",
         "broll": [{"src": "broll/broll_01.mp4", "start": 0.0, "end": round(t_ce - 0.05, 3), "from": 0.0, "pos": "50% 30%"},
                   {"src": "broll/broll_02.mp4", "start": round(t_ce - 0.05, 3), "end": s01["end"], "from": 0.0, "pos": "38% 50%", "kb": "in"}]},
        {"type": "avatar", "start": a01["start"], "end": round(t_les70 - 0.06, 3), "src": f"avatar/A01{SUF}.mp4", "clipStart": clip_start("A01"), "zoom": "C", **AV},
        {"type": "avatar", "start": round(t_les70 - 0.06, 3), "end": a01["end"], "src": f"avatar/A01{SUF}.mp4", "clipStart": clip_start("A01"), "zoom": "B", **AV},
        {"type": "edu", "start": m1["start"], "end": m1["end"], "src": "edu/E1.mp4", "from": 0.0, "enter": "circle", "wipeX": "50%", "wipeY": "60%", "bg": "#FAF6F3"},
        {"type": "avatar", "start": a02["start"], "end": a02["end"], "src": f"avatar/A02{SUF}.mp4", "clipStart": clip_start("A02"), "zoom": "A", **AV},
        {"type": "full", "start": m2["start"], "end": m2["end"], "src": "broll/broll_03.mp4", "from": 0.0, "kb": "in", "subY": 0.72},
        {"type": "avatar", "start": a03["start"], "end": round(t_la_vit - 0.06, 3), "src": f"avatar/A03{SUF}.mp4", "clipStart": clip_start("A03"), "zoom": "C", **AV},
        {"type": "avatar", "start": round(t_la_vit - 0.06, 3), "end": a03["end"], "src": f"avatar/A03{SUF}.mp4", "clipStart": clip_start("A03"), "zoom": "B", **AV},
        {"type": "infolist", "start": m3["start"], "end": m3["end"], "enter": "circle", "wipeX": "50%", "wipeY": "20%", "bg": "linear-gradient(180deg, #FAF6F3 0%, #EFE7E0 100%)",
         "rows": [
             {"t": round(wt("cuivre", m3["start"]) - 0.1, 3), "title": "Cuivre", "img": "images/I1.png",
              "parts": [{"s": "Fabrique la mélanine, "}, {"s": "votre pigment", "bold": True, "mark": wt("pigment", m3["start"])}]},
             {"t": round(wt("B12", m3["start"]) - 0.1, 3), "title": "B12", "img": "images/I2.png",
              "parts": [{"s": "Nourrit les cellules "}, {"s": "qui produisent le pigment", "bold": True, "mark": wt("cellules", m3["start"])}]},
             {"t": round(wt("fer", m3["start"]) - 0.1, 3), "title": "Fer", "img": "images/I3.png",
              "parts": [{"s": "Nourrit aussi "}, {"s": "ces cellules", "bold": True, "mark": wt("cellules", m3["start"])}]}]},
        {"type": "avatar", "start": a04["start"], "end": a04["end"], "src": f"avatar/A04{SUF}.mp4", "clipStart": clip_start("A04"), "zoom": "A", **AV},
        {"type": "card", "start": m4["start"], "end": round(t_et_soleil - 0.15, 3), "cardW": 0.78, "cardH": 0.44, "subY": 0.79,
         "clips": [{"src": f"images/I{4 + i}.png", "start": round((m4["start"] if i == 0 else t_foods[i] - 0.05), 3),
                    "end": round((t_foods[i + 1] - 0.05) if i < 4 else t_et_soleil - 0.15, 3), "kb": "in"} for i in range(5)]},
        {"type": "full", "start": round(t_et_soleil - 0.15, 3), "end": m4["end"], "src": "broll/broll_04.mp4", "from": 0.3, "kb": "in", "pos": "42% 50%", "subY": 0.72},
        {"type": "avatar", "start": a05["start"], "end": round(t_ecrivez - 0.06, 3), "src": f"avatar/A05{SUF}.mp4", "clipStart": clip_start("A05"), "zoom": "B", **AV},
        {"type": "avatar", "start": round(t_ecrivez - 0.06, 3), "end": round(total, 3), "src": f"avatar/A05{SUF}.mp4", "clipStart": clip_start("A05"), "zoom": "C", **AV},
    ]
    t_guide = wt("guide", a05["start"])
    t_envoie = wt("envoie", t_guide)
    t_30 = wt("30")
    overlays = [
        {"type": "flash", "t": a01["start"], "color": "#C9805F"},
        {"type": "bignumber", "start": round(t_30 - 0.06, 3), "end": round(wt("héréditaire") + 0.75, 3), "text": "30\u00a0%", "label": "héréditaire",
         "y": 0.56, "color": "#FAF6F3", "glow": "rgba(168,85,58,.65)"},
        {"type": "label", "start": round(wt("follicules") - 0.05, 3), "end": m1["end"], "text": "Follicule", "x": 0.33, "y": 0.62, "align": "right", "line": 70, "box": True, "color": "#7A4351"},
        {"type": "label", "start": round(wt("catalase") - 0.05, 3), "end": m1["end"], "text": "Catalase", "x": 0.67, "y": 0.72, "line": 70, "box": True, "color": "#A8553A"},
        {"type": "label", "start": round(wt("peroxyde") - 0.05, 3), "end": m1["end"], "text": "H\u2082O\u2082", "x": 0.33, "y": 0.78, "align": "right", "line": 70, "box": True, "color": "#7A4351"},
        {"type": "label", "start": round(wt("décolore") - 0.05, 3), "end": m1["end"], "text": "Pigment", "sub": "se décolore", "x": 0.70, "y": 0.30, "line": 70, "box": True, "color": "#A8553A"},
        {"type": "flash", "t": a05["start"], "color": "#C9805F"},
        {"type": "text", "start": round(t_guide - 0.05, 3), "end": round(total, 3), "text": "GUIDE", "x": 0.5, "y": 0.60, "size": 150, "color": "#FAF6F3", "bg": "#A8553A", "weight": 900},
        {"type": "follow", "start": round(t_guide + 0.5, 3), "end": round(total, 3), "handle": "@les_cheveux_de_claire", "avatar": "images/profil.jpg", "y": 0.745, "clickAfter": 1.2},
    ]
    montage = {
        "fps": 30, "width": 1080, "height": 1920, "durationSec": round(total, 3), "bg": "#FAF6F3",
        "audio": "audio/voix_off.wav" if VOIX_OFF else "audio/voix_montage.wav",
        "theme": {"accent": "#A8553A", "accent2": "#F2D2C0", "subBox": "#FAF6F3", "subText": "#2E2A26", "subDim": "#B4ADA4",
                  "bannerBg": "#A8553A", "bannerText": "#FAF6F3", "infoBg": "#EFE7E0", "infoText": "#2E2A26", "cardBg": "#FAF6F3", "followBlue": "#A8553A"},
        "subtitles": {"words": words, "maxWords": 4, "maxChars": 24, "size": 46,
                      "hide": [[round(t_guide - 0.05, 3), round(total, 3)]]},
        "segments": segments,
        "overlays": overlays,
    }
    json.dump(montage, open(M / ("montage_voixoff.json" if VOIX_OFF else "montage.json"), "w"), ensure_ascii=False, indent=1)
    json.dump([{k: p[k] for k in ("id", "src", "in", "out", "start", "end", "gain_db")} for p in PIECES],
              open(M / ("piste_voixoff.json" if VOIX_OFF else "piste_voix.json"), "w"), ensure_ascii=False, indent=1)
    for p in PIECES:
        print(f"{p['id']:4} {p['src']:32} {p['in']:6.2f}-{p['out']:6.2f}  ->  {p['start']:6.2f}-{p['end']:6.2f}  gain {p['gain_db']:+.1f} dB")
    print(f"durée totale {total:.2f} s")


if __name__ == "__main__":
    main()
