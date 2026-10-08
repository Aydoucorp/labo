# Brief : talking head n°2 · Claire · affinement des cheveux à la ménopause

- Date : 2026-10-08
- Skill : `skills/talking-head` (mode A, découpage)
- Entrées : `script.txt` (script ElevenLabs avec balises d'émotion), `voix.mp3` (voix off Elise, 59,6 s)
- Configuration réutilisée : `Claire/talking-head/_config/` (images de départ 9:16 et 1:1, charte, recette Seedance 2.5)
- Alignement : forcé MMS (ctc-forced-aligner, demande de l'utilisateur) sur le texte du script sans balises (`script_texte.txt`) → `mots_mms.json`, converti en `mots.json`. Transcription Whisper gardée pour comparaison (`mots_whisper.json`).
- B-rolls : aucun repris de la bibliothèque, à la demande de l'utilisateur (« je vais t'en donner des nouveaux pour ce script »). 7 b-rolls à déposer dans `talking_head_broll_2/`.
- Voix au montage : voix off d'origine partout, son Seedance coupé, clips recalés phrase par phrase (charte).

Livrables du découpage : `decoupage.md`, `decoupage.json`, `audio_avatar/` (4 extraits), `prompts/`, `brolls-a-trouver.html`. Scripts : `build_decoupage.py`, `ecrire_decoupage_md.py`.

## Choix de l'utilisateur (2026-10-08)

- Bandeau d'accroche : 1b, « 2 femmes sur 3 voient leurs cheveux s'affiner à la ménopause ».
- Clips avatar : Seedance 2.5 en 720p (63 cr/s, 37 s, environ 2 331 cr).
- Images de départ de l'avatar : question posée, proposition de réutiliser celles du talking head n°1 (`Claire/talking-head/_config/`).
- Nouvelles images de départ (demande du 2026-10-08) : pull bleu melody, 3 images (9:16 principale, 9:16 deuxième caméra, 1:1), en 1K. Test comparatif GPT Image 2 contre Nano Banana 2.1 (`nano-banana-2-1` sur KIE, 4 cr en 1K, confirmé) sur l'image 9:16 principale : voir `journal_generations.md`.
