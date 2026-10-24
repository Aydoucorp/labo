# Aperçus séparés des clips Wan avec la voix d'origine et les recalages du montage.
# Chaque morceau : (début dans la source, début voix, fin voix). Décalage positif = Wan en retard, on saute dans la source.
import subprocess
A = "audio/voix.mp3"
CLIPS = {
 "1-W1_accroche": ("W1", [(0.5, 0.00, 7.70)]),
 "2-W3_micro-tensions": ("W3", [(0.0, 19.40, 23.95), (4.85, 23.95, 25.05)]),
 "3-W4_shampoing": ("W4", [(0.24, 25.05, 26.88)]),
 "4-W5_silhouette": ("W5", [(0.0, 40.45, 44.30)]),
 "5-W6_bonne-nouvelle": ("W6", [(0.0, 49.60, 52.48), (3.22, 52.48, 53.12)]),
 "6-W7_appel-a-l-action": ("W7", [(0.0, 57.40, 63.25), (6.15, 63.25, 64.91)]),
}
for nom, (c, morceaux) in CLIPS.items():
    fc, lab = [], ""
    for i, (s0, t0, t1) in enumerate(morceaux):
        fc.append(f"[0:v]trim=start={s0}:duration={t1 - t0},setpts=PTS-STARTPTS[v{i}]"); lab += f"[v{i}]"
    fc.append(f"{lab}concat=n={len(morceaux)}:v=1:a=0[v]")
    t0, t1 = morceaux[0][1], morceaux[-1][2]
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"sorties/clips/{c}-v1.mp4", "-ss", str(t0), "-t", str(t1 - t0), "-i", A,
                    "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", f"sorties/apercus/{nom}.mp4"], check=True)
    print(nom)
