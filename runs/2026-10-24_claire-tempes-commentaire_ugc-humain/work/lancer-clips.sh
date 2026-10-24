#!/bin/bash
# Lance les 6 clips Wan 3.0 (480P, 9:16), méthode écran noir : @Video1 = voix, @Image1 = retenues/cadrage.png (seule image).
cd /home/user/labo/runs/2026-10-24_claire-tempes-commentaire_ugc-humain
mkdir -p sorties/clips
for spec in W1:9:W1-pad W3:6:W3 W4:2:W4 W5:4:W5 W6:4:W6 W7:8:W7; do
  IFS=: read c d v <<< "$spec"
  python3 work/wan3_video.py prompts/video/$c.txt sorties/clips/$c-v1.mp4 --image retenues/cadrage.png \
    --video audio/clips/${v}_ecran-noir.mp4 --duration $d --resolution 480P > work/log-$c-v1.json 2>&1 &
  sleep 3
done
wait
cat work/log-W*-v1.json
