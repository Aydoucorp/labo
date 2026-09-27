#!/usr/bin/env bash
# Normalise les vidéos d'un dossier (b-roll, clips avatar, animations) pour un rendu rapide et sans surprise :
# 30 i/s constants, H.264, sans son, plus grand côté limité à 1920 px. Les originaux ne sont pas modifiés.
# Usage : bash preparer_medias.sh dossier_source dossier_sortie
set -e
SRC="$1"; OUT="$2"; mkdir -p "$OUT"
for f in "$SRC"/*.{mp4,mov,webm,m4v,MP4,MOV}; do
  [ -e "$f" ] || continue
  b=$(basename "${f%.*}")
  ffmpeg -v error -y -i "$f" -an -r 30 -vf "scale='if(gt(iw,ih),min(1920,iw),-2)':'if(gt(iw,ih),-2,min(1920,ih))'" \
    -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p "$OUT/$b.mp4"
  echo "$OUT/$b.mp4  $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 "$OUT/$b.mp4")"
done
