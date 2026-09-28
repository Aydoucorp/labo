# Mesure le décalage lèvres / voix d'un clip avatar : corrélation entre l'ouverture de la bouche (image) et l'énergie de la voix (extrait audio).
# Décalage positif = la bouche bouge APRÈS la voix (vidéo en retard) ; négatif = la bouche est EN AVANCE sur la voix.
import cv2, numpy as np, subprocess, sys, json
def audio_env(wav, fps):
    raw = subprocess.run(["ffmpeg","-v","error","-i",wav,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(float)
    hop = int(16000/fps); n = len(a)//hop
    return np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)) for i in range(n)])
def mouth_signal(video):
    cap = cv2.VideoCapture(video); fps = cap.get(cv2.CAP_PROP_FPS)
    frames=[]
    while True:
        ok, fr = cap.read()
        if not ok: break
        frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32))
    H, W = frames[0].shape
    # zone de la bouche repérée à la main sur les images de départ (fractions de l'image)
    fx0, fy0, fx1, fy1 = (0.46, 0.29, 0.60, 0.38) if H == W else (0.48, 0.28, 0.63, 0.33)
    x, y, w, h = int(W*fx0), int(H*fy0), int(W*(fx1-fx0)), int(H*(fy1-fy0))
    print("  zone bouche", x, y, w, h, "sur", W, H)
    # ouverture de bouche ~ proportion de pixels sombres (intérieur de la bouche) dans la zone
    sig = np.array([np.mean(f[y:y+h, x:x+w] < np.percentile(np.stack(frames)[:, y:y+h, x:x+w], 15)) for f in frames])
    return sig, fps
res={}
for c in sys.argv[1:]:
    m, fps = mouth_signal(f"avatar/{c}_v1.mp4"); e = audio_env(f"audio_avatar/{c}.wav", fps)
    n = min(len(m), len(e)); m = (m[:n]-m[:n].mean())/(m[:n].std()+1e-9); e = (e[:n]-e[:n].mean())/(e[:n].std()+1e-9)
    best=None
    for lag in range(-int(fps), int(fps)+1):   # ±1 s
        if lag>=0: r = np.corrcoef(m[lag:], e[:n-lag])[0,1]
        else: r = np.corrcoef(m[:n+lag], e[-lag:])[0,1]
        if best is None or r>best[1]: best=(lag,r)
    r0 = np.corrcoef(m, e)[0,1]
    res[c]={"decalage_s": round(best[0]/fps,3), "correlation": round(best[1],2), "correlation_sans_decalage": round(r0,2)}
    print(c, res[c])
json.dump(res, open("sorties/mesure_synchro.json","w"), indent=1)
