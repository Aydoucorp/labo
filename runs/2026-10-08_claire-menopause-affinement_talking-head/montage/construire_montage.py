#!/usr/bin/env python3
"""Construit montage.json du talking head n°2 (Claire, affinement des cheveux à la ménopause).

Voix : voix off ElevenLabs d'origine sur toute la vidéo (voix.mp3), son des clips coupé.
Clips avatar : recalés mot par mot sur la voix off par montage/recaler_mots.py (avatar/recale/*.mp4) ;
l'image 0 de chaque clip recalé = clipStart de couper_audio.py. Temps = alignement forcé MMS (mots_mms.json).
Usage (depuis le dossier du run) : python3 montage/construire_montage.py
"""
import json, pathlib

RUN = pathlib.Path(__file__).resolve().parent.parent
M = RUN / "montage"
W = json.load(open(RUN / "mots_mms.json"))["words"]
CL = {c["id"]: c["clipStart"] for c in json.load(open(RUN / "audio_avatar/clips_avatar.json"))}
DUR = 59.559

def t(word, after=0.0):
    for w in W:
        if w["start"] >= after - 1e-6 and w["w"].lower().strip("'’").startswith(word.lower()):
            return w["start"]
    raise SystemExit(f"mot introuvable : {word} après {after}")

# Coupes des plans (temps de decoupage.json, calés sur MMS)
C = [0.00, 4.30, 13.50, 16.70, 19.10, 21.20, 22.75, 26.10, 27.20, 31.30, 33.13, 36.68, 40.75, 45.80, 49.80, 52.33, 55.75, DUR]
AV = {"faceY": 0.22}
def av(i, cid, zoom):
    return {"type": "avatar", "start": C[i], "end": C[i + 1], "src": f"avatar/{cid}.mp4", "clipStart": CL[cid], "zoom": zoom, **AV}

segments = [
    {"type": "split", "start": C[0], "end": C[1], "src": "avatar/S01.mp4", "clipStart": CL["S01"],
     "banner": "2 femmes sur 3 voient leurs cheveux s'affiner à la ménopause",
     "broll": [{"src": "broll/broll_01.mp4", "start": C[0], "end": C[1], "from": 0.0, "pos": "50% 30%", "kb": "in"}]},
    {"type": "edu", "start": C[1], "end": C[2], "src": "edu/E1.mp4", "from": 0.0, "enter": "circle", "wipeX": "50%", "wipeY": "60%", "bg": "#FAF6F3"},
    av(2, "A01", "A"),
    {"type": "full", "start": C[3], "end": C[4], "src": "broll/broll_03.mp4", "from": 1.9, "kb": "in", "pos": "50% 35%", "subY": 0.72},
    av(4, "A01", "C"),
    {"type": "full", "start": C[5], "end": C[6], "src": "broll/broll_04.mp4", "from": 42.0, "kb": "in", "subY": 0.72},
    av(6, "A02", "B"),
    av(7, "A02", "C"),
    av(8, "A02", "A"),
    {"type": "full", "start": C[9], "end": C[10], "src": "broll/broll_05.mp4", "from": 2.0, "kb": "in", "pos": "50% 30%", "subY": 0.72},
    {"type": "full", "start": C[10], "end": C[11], "src": "broll/broll_06.mp4", "from": 44.0, "kb": "in", "pos": "55% 50%", "subY": 0.72},
    {"type": "full", "start": C[11], "end": C[12], "src": "broll/broll_07.mp4", "from": 0.3, "subY": 0.72},
    {"type": "infolist", "start": C[12], "end": C[13], "enter": "circle", "wipeX": "50%", "wipeY": "20%",
     "bg": "linear-gradient(180deg, #FAF6F3 0%, #EFE7E0 100%)",
     "rows": [
         {"t": round(t("l'huile", 41.5) - 0.1, 3), "title": "Huile de romarin", "img": "images/I1.png",
          "parts": [{"s": "Premières études "}, {"s": "encourageantes", "bold": True, "mark": round(t("encourageantes") - 0.05, 3)}]},
         {"t": round(t("massage", 42.5) - 0.1, 3), "title": "Massage quotidien", "img": "images/I2.png",
          "parts": [{"s": "Du cuir chevelu, "}, {"s": "chaque soir", "bold": True, "mark": round(t("encourageantes") - 0.05, 3)}]}]},
    av(13, "A03", "B"),
    av(14, "A03", "A"),
    av(15, "A03", "B"),
    av(16, "A03", "C"),
]

t_guide = t("GUIDE", 55.0)
overlays = [
    {"type": "label", "start": round(t("d'œstrogènes") - 0.05, 3), "end": C[2], "text": "Œstrogènes", "x": 0.38, "y": 0.80, "align": "right", "line": 60, "box": True, "color": "#A8553A"},
    {"type": "label", "start": round(t("phase") - 0.05, 3), "end": C[2], "text": "Phase de croissance", "x": 0.60, "y": 0.13, "align": "right", "line": 50, "box": True, "color": "#7A4351"},
    {"type": "label", "start": round(t("D-H-T") - 0.05, 3), "end": C[2], "text": "DHT", "x": 0.72, "y": 0.72, "line": 60, "box": True, "color": "#7A4351"},
    {"type": "label", "start": round(t("follicules", 12.0) - 0.05, 3), "end": C[2], "text": "Follicule", "x": 0.30, "y": 0.64, "align": "right", "line": 60, "box": True, "color": "#A8553A"},
    {"type": "flash", "t": C[4], "color": "#C9805F"},
    {"type": "cutout", "start": round(t("complément") - 0.12, 3), "end": C[9], "src": "images/O1.png", "x": 0.25, "y": 0.62, "w": 0.30, "rotate": -6},
    {"type": "inset", "start": round(t("Comment") - 0.1, 3), "end": C[16], "src": "images/guide_carte.png", "x": 0.5, "y": 0.62, "w": 0.48, "h": 0.36, "fit": "contain", "hideSubs": True},
    {"type": "text", "start": round(t_guide - 0.05, 3), "end": DUR, "text": "GUIDE", "x": 0.5, "y": 0.60, "size": 150, "color": "#FAF6F3", "bg": "#A8553A", "weight": 900},
    {"type": "follow", "start": round(t_guide + 0.6, 3), "end": DUR, "handle": "@les_cheveux_de_claire", "avatar": "images/profil.jpg", "y": 0.745, "clickAfter": 1.2},
]

# Sous-titres : mots exacts du script (MMS), ponctuation recollée, nouvelle ligne au début de chaque plan
words = []
firsts = {min((i for i, w in enumerate(W) if w["start"] >= c - 0.01)) for c in C[1:-1]}
for i, w in enumerate(W):
    txt = w["w"] + (w.get("punct_after") or "")
    txt = txt.replace("D-H-T", "DHT").replace("GUIDE", "« GUIDE »")
    e = {"w": txt, "s": w["start"], "e": w["end"]}
    if i in firsts or not words:
        e["br"] = True
    words.append(e)

montage = {
    "fps": 30, "width": 1080, "height": 1920, "durationSec": DUR, "bg": "#FAF6F3", "audio": "audio/voix.mp3",
    "theme": {"accent": "#A8553A", "accent2": "#F2D2C0", "subBox": "#FAF6F3", "subText": "#2E2A26", "subDim": "#B4ADA4",
              "bannerBg": "#A8553A", "bannerText": "#FAF6F3", "infoBg": "#EFE7E0", "infoText": "#2E2A26", "cardBg": "#FAF6F3", "followBlue": "#A8553A"},
    "subtitles": {"words": words, "maxWords": 4, "maxChars": 24, "size": 46, "hide": [[round(t_guide - 0.05, 3), DUR]]},
    "segments": segments, "overlays": overlays,
}
json.dump(montage, open(M / "montage.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(segments)} plans, {len(overlays)} surimpressions, {len(words)} mots, durée {DUR} s")
