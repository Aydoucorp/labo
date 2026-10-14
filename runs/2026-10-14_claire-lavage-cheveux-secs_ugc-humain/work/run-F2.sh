#!/bin/bash
# F2 : deux clips Seedance 2.5 720p, son généré désactivé, prompt sobre ; F2b part de la dernière image utile de F2a.
cd /home/user/labo
python3 scripts/kie_seedance.py --prompt-file runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/prompts/video/F-sobre.txt --image runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/retenues/depart.png --voix-ecran-noir runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/audio/extraits/F2a.wav --resolution 720p --out runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F2a-v1.mp4
ffmpeg -v error -y -ss 4.20 -i runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F2a-v1.mp4 -frames:v 1 runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F2a-v1_fin.png
python3 scripts/kie_seedance.py --prompt-file runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/prompts/video/F-sobre.txt --image runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F2a-v1_fin.png --voix-ecran-noir runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/audio/extraits/F2b.wav --resolution 720p --out runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F2b-v1.mp4
echo FINI
