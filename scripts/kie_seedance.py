#!/usr/bin/env python3
"""Clip avatar parlant avec Seedance 2.5 sur KIE : image de départ (en référence) + extrait de voix off qui pilote les lèvres.

MÉTHODE PAR DÉFAUT DU STUDIO (validée le 2026-10-10, écart lèvres / voix ≤ 0,02 s) :
  python3 scripts/kie_seedance.py --prompt-file p.txt --image depart.png --voix-ecran-noir A01.wav --out clip.mp4 \
      --generate-audio [--ratio 9:16] [--resolution 720p]
  La voix ElevenLabs est transformée en vidéo écran noir (A01_ecran-noir.mp4, à côté de l'audio) et envoyée en @Video1.
  Le prompt ne contient PAS le texte à dire ni de consigne de rythme (gabarit 2 du skill talking-head).
  Sans --duration, la durée du clip = durée de la voix arrondie à la seconde supérieure (4 s minimum).
  Au montage : son Seedance coupé, voix ElevenLabs d'origine posée telle quelle.

Ancien usage (voix en référence audio, lèvres décalées de 0,3 à 1 s) :
  python3 scripts/kie_seedance.py --prompt-file p.txt --image depart.png --audio A01.wav --out clip.mp4 \
      [--duration 4] [--ratio 9:16] [--resolution 720p]
  python3 scripts/kie_seedance.py --prompt-file p.txt --image a.png b.png c.png --out clip.mp4 --duration 12
      (plusieurs images = @Image1, @Image2... dans l'ordre ; sans --audio : clip muet multi-plans, ex. UGC humain)
  --video ref.mp4 : vidéo de référence (@Video1), par exemple un écran noir qui porte la voix off (astuce de synchro labiale).

- Seedance 2.5 n'accepte pas à la fois une première image imposée et un audio de référence :
  l'image est envoyée dans reference_image_urls, le prompt la déclare « exact first frame ».
- Par défaut, son du modèle désactivé. Avec --generate-audio, Seedance fait parler le personnage lui-même
  (voix et lèvres générées ensemble) ; l'audio de référence sert alors de modèle de voix (@Audio1 dans le prompt).
- Lit KIE_API_KEY dans .env (via kie_image.py). La clé n'est jamais affichée.
- Affiche une ligne JSON : taskId, état, crédits consommés, fichier reçu.
"""
import argparse, json, math, pathlib, subprocess, sys, time, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from kie_image import API, call, upload


TAILLES = {"9:16": "720x1280", "1:1": "720x720", "16:9": "1280x720", "4:3": "960x720", "3:4": "720x960"}


def ecran_noir(audio, ratio):
    """Vidéo écran noir qui porte la voix (référence @Video1). Renvoie (chemin mp4, durée de la voix en s)."""
    src = pathlib.Path(audio)
    out = src.with_name(src.stem + "_ecran-noir.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={TAILLES.get(ratio, '720x1280')}:r=24",
                    "-i", str(src), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]).decode())
    return str(out), dur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--image", required=True, nargs="+")
    ap.add_argument("--audio", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=int, default=None, help="durée du clip (s) ; par défaut 4, ou la durée de la voix avec --voix-ecran-noir")
    ap.add_argument("--ratio", default="9:16")
    ap.add_argument("--resolution", default="720p")
    ap.add_argument("--generate-audio", action="store_true")
    ap.add_argument("--video", default=None, help="vidéo de référence (@Video1), ex. écran noir portant la voix off")
    ap.add_argument("--voix-ecran-noir", default=None, help="voix (wav/mp3) à envoyer en vidéo écran noir (@Video1) : méthode par défaut")
    a = ap.parse_args()
    prompt = pathlib.Path(a.prompt_file).read_text()
    if a.voix_ecran_noir:
        a.video, dur_voix = ecran_noir(a.voix_ecran_noir, a.ratio)
        if a.duration is None:
            a.duration = max(4, math.ceil(dur_voix - 0.05))
        if "@Audio1" in prompt:
            print("attention : le prompt cite @Audio1 alors que la voix part en @Video1", file=sys.stderr)
    if a.duration is None:
        a.duration = 4

    imgs = [i if i.startswith("http") else upload(i) for i in a.image]
    inp = {"prompt": prompt, "reference_image_urls": imgs,
           "duration": a.duration, "aspect_ratio": a.ratio, "resolution": a.resolution,
           "generate_audio": a.generate_audio}
    if a.audio:
        inp["reference_audio_urls"] = [a.audio if a.audio.startswith("http") else upload(a.audio)]
    if a.video:
        inp["reference_video_urls"] = [a.video if a.video.startswith("http") else upload(a.video)]
    task = call(f"{API}/createTask", {"model": "bytedance/seedance-2-5", "input": inp})
    if task.get("code") != 200:
        sys.exit(f"création refusée : {task.get('code')} {task.get('msg')}")
    tid = task["data"]["taskId"]

    for _ in range(240):  # jusqu'à 20 min
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
