#!/bin/bash
# Génère les 12 pages de l'ebook « raie élargie » (GPT Image 2, 3:4) : ./work/generer.sh [1K|2K|4K]
RES=${1:-1K}
cd /home/user/labo
R=runs/2026-10-24_claire-raie-elargie_ebook
for n in 01 02 03 04 05 06 07 08 09 10 11 12; do
  python3 scripts/kie_image.py --model gpt-image-2-text-to-image --prompt-file $R/prompts/pages/$n.txt --out $R/sorties/pages/$n-v1.png --ratio 3:4 --resolution $RES > $R/work/logs/gen-$n-v1.log 2>&1 &
  sleep 2
done
wait
echo FINI
