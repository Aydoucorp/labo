#!/usr/bin/env bash
# Lance le rendu Remotion en arrière-plan (un rendu d'une minute peut dépasser 10 min sur une petite machine).
# Usage : bash rendre.sh dossier_projet_montage [--scale=0.5 pour un brouillon]
# Suivi : tail -f dossier/out/rendu.log   |   Fin : présence de dossier/out/FINI
set -e
cd "$1"; shift || true
BROWSER=""
for b in /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell /opt/pw-browsers/chromium; do
  [ -x "$b" ] && BROWSER="--browser-executable=$b" && break
done
mkdir -p out; rm -f out/FINI
nohup bash -c "npx remotion render src/index.js Main out/video.mp4 --props=montage.json --codec=h264 --crf=18 $BROWSER $* > out/rendu.log 2>&1; echo \$? > out/FINI" >/dev/null 2>&1 &
echo "Rendu lancé (PID $!). Suivre : tail -f $(pwd)/out/rendu.log"
