#!/bin/bash
# Lance les 8 clips Wan 3.0 (480P, 9:16), méthode écran noir : @Video1 = voix, @Image1 = cadrage-v2 (seule image, verrou tenue).
cd /home/user/labo/runs/2026-10-23_claire-tempes-affinement_ugc-humain
mkdir -p sorties/clips
for spec in W1:9:W1-pad W8:7:W8 W2:4:W2 W3:2:W3 W4:8:W4 W5:2:W5 W6:3:W6 W7:11:W7; do
  IFS=: read c d v <<< "$spec"
  python3 work/wan3_video.py prompts/video/$c.txt sorties/clips/$c-v1.mp4 \
    --image retenues/cadrage-v2.png --video audio/clips/${v}_ecran-noir.mp4 \
    --duration $d --resolution 480P > work/log-$c-v1.json 2>&1 &
done
wait
cat work/log-W*-v1.json
