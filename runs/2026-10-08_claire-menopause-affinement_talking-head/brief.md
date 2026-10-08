# Brief : talking head n°2 · Claire · affinement des cheveux à la ménopause

- Date : 2026-10-08
- Skill : `skills/talking-head` (mode A, découpage)
- Entrées : `script.txt` (script ElevenLabs avec balises d'émotion), `voix.mp3` (voix off Elise, 59,6 s)
- Configuration réutilisée : `Claire/talking-head/_config/` (images de départ 9:16 et 1:1, charte, recette Seedance 2.5)
- Alignement : forcé MMS (ctc-forced-aligner, demande de l'utilisateur) sur le texte du script sans balises (`script_texte.txt`) → `mots_mms.json`, converti en `mots.json`. Transcription Whisper gardée pour comparaison (`mots_whisper.json`).
- B-rolls : aucun repris de la bibliothèque, à la demande de l'utilisateur (« je vais t'en donner des nouveaux pour ce script »). 7 b-rolls à déposer dans `talking_head_broll_2/`.
- Voix au montage : voix off d'origine partout, son Seedance coupé, clips recalés phrase par phrase (charte).

Livrables du découpage : `decoupage.md`, `decoupage.json`, `audio_avatar/` (4 extraits), `prompts/`, `brolls-a-trouver.html`. Scripts : `build_decoupage.py`, `ecrire_decoupage_md.py`.
