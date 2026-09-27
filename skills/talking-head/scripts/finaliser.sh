#!/usr/bin/env bash
# Finalise l'export : volume normalisé pour les réseaux (environ -14 LUFS, pic -1,5 dBFS), image copiée sans réencodage,
# lecture rapide sur mobile (faststart). Ne change ni le calage ni la durée.
# Usage : bash finaliser.sh out/video.mp4 out/video_finale.mp4
set -e
ffmpeg -v error -y -i "$1" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$2"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$2"
