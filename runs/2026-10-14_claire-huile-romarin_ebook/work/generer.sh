#!/bin/bash
# Génère les 11 pages de l'ebook 002 dans l'ordre (GPT Image 2, 3:4, 1K).
cd /home/user/labo
for n in 01 02 03 04 05 06 07 08 09 10 11; do
  python3 scripts/kie_image.py --model gpt-image-2-text-to-image --prompt-file runs/2026-10-14_claire-huile-romarin_ebook/prompts/pages/$n.txt --out runs/2026-10-14_claire-huile-romarin_ebook/sorties/pages/$n-v1.png --ratio 3:4 --resolution 1K > runs/2026-10-14_claire-huile-romarin_ebook/work/logs/gen-$n-v1.log 2>&1 &
  sleep 2
done
wait
echo FINI
