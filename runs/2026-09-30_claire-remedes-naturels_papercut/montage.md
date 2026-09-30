# Montage · Claire · Remèdes naturels notés sur 10 · Paper Cut

**Créa finale** : `creas/papercut/2026-09-30_papercut_002.mp4` (copie : `retenues/film/claire-remedes-naturels-papercut-v1.mp4`) · 42,2 s · 1080×1920 · 30 i/s · H.264 + AAC · -14,2 LUFS, pic -1,4 dBFS.

- **Voix** : voix off ElevenLabs entière, non retouchée. Coupes calées sur l'alignement MMS mot à mot (`work/words.json`).
- **Plans** : 16 clips coupés à la durée mesurée de chaque collage (voir `storyboard.md`). P08 démarre à 1,2 s et P14 à 0,6 s dans leur clip pour que la croix tombe sur le bon mot.
- **Notes** : tampons 1/10 (6,95 s), 0/10 (14,84 s), 5/10 (20,96 s) composés à part (`montage/tampons.py`), imprimés sur une étiquette crème, qui tombent pile sur le mot avec un choc sourd.
- **Son** : voix + bruitages papier des clips à -12 dB + chocs des tampons, normalisation -14 LUFS. Ni musique ni sous-titres (les titres des collages portent la lecture).

## Contrôles (3 passes)

1. Image : planche toutes les 0,5 s et moments des tampons. Corrigé : tampon 0/10 illisible sur le flacon foncé, tampons trop discrets (agrandis, étiquette crème).
2. Son : Whisper sur le film, tout le script dans l'ordre (écarts = chiffres transcrits en chiffres) ; -14,2 LUFS, pic -1,4 dBFS.
3. Fichier : aucun écran noir, aucune image figée involontaire, format 1080×1920, 30 i/s, 48 kHz.

Reproduire : `python3 montage/tampons.py` puis `python3 montage/montage.py` (depuis le dossier du run).
