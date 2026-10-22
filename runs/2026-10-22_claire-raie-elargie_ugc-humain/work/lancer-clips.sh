#!/bin/bash
# Lance les 5 clips Wan 3.0 (480P, 9:16), méthode écran noir : @Video1 = voix, @Image1 = cadrage-v2, @Image2 = visage.
cd /home/user/labo/runs/2026-10-22_claire-raie-elargie_ugc-humain
mkdir -p sorties/clips
for spec in C1:3 C2:6 C3:7 C5:7 C7:6; do
  c=${spec%%:*}; d=${spec##*:}
  python3 work/wan3_video.py prompts/video/$c.txt sorties/clips/$c-v1.mp4 \
    --image sorties/cadrage-v2.png casting/de-face.png --video audio/clips/${c}_ecran-noir.mp4 \
    --duration $d --resolution 480P > work/log-$c-v1.json 2>&1 &
done
wait
cat work/log-C*-v1.json
