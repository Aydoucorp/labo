#!/bin/bash
# F1 v2 : deux clips Seedance 2.5 720p, son généré désactivé, prompt sobre ; F1b part de la dernière image utile de F1a.
cd /home/user/labo
python3 scripts/kie_seedance.py --prompt-file runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/prompts/video/F-sobre.txt --image runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/retenues/depart.png --voix-ecran-noir runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/audio/extraits/F1a.wav --resolution 720p --out runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F1a-v2.mp4
ffmpeg -v error -y -ss 5.45 -i runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F1a-v2.mp4 -frames:v 1 runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F1a-v2_fin.png
python3 scripts/kie_seedance.py --prompt-file runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/prompts/video/F-sobre.txt --image runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F1a-v2_fin.png --voix-ecran-noir runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/audio/extraits/F1b.wav --resolution 720p --out runs/2026-10-14_claire-lavage-cheveux-secs_ugc-humain/sorties/clips/F1b-v2.mp4
echo FINI
