# Journal des générations · Claire · Affinement ménopause · Talking head n°2

Tarif KIE : 1 crédit ≈ 0,005 $.

| Étape | Variante | Modèle | ID de tâche | État | Fichier | Statut | Coût |
|---|---|---|---|---|---|---|---|
| Test image de départ 9:16 (pull bleu) | gpt v1 | gpt-image-2-image-to-image 1K | c12d918776e7f69412a4c9380229d58b | success | `sorties/config/depart_9x16_gpt_v1.png` | **retenue** (choix : GPT Image 2) | 6 cr |
| Test image de départ 9:16 (pull bleu) | gpt v2 | gpt-image-2-image-to-image 1K | 06b065ceda911a77bd3c970d1db4d4c5 | success | `sorties/config/depart_9x16_gpt_v2.png` | non retenue | 6 cr |
| Test image de départ 9:16 (pull bleu) | nb21 v1 | nano-banana-2-1 1K | abcc376186f63591c092924a38e93d2d | success | `sorties/config/depart_9x16_nb21_v1.png` | non retenue | 4 cr |
| Test image de départ 9:16 (pull bleu) | nb21 v2 | nano-banana-2-1 1K | 2bb024d54559886e448ede709ca76fb5 | success | `sorties/config/depart_9x16_nb21_v2.png` | non retenue | 4 cr |

| Image de départ 9:16 deuxième caméra | v1 | gpt-image-2-image-to-image 1K | ce7f7d4b7cbfe00cfc4c5f9e682d33ab | success | `sorties/config/depart_9x16_camera2_gpt_v1.png` | **retenue** (choix de l'utilisateur, angle léger) | 6 cr |
| Image de départ 1:1 | v1 | gpt-image-2-image-to-image 1K | 4b1b3c70aa5bebb43854232c4af5d57f | success | `sorties/config/depart_1x1_gpt_v1.png` | à valider | 6 cr |
| Image de départ animation E1 (9:16) | v1 | gpt-image-2-text-to-image 1K | e44d5977c39aeb68eeb44017398bb280 | success | `generations/image-E1_v1.png` | à valider | 6 cr |
| Image infographie I1 (1:1) | v1 | gpt-image-2-text-to-image 1K | 8d2ebc59ff6dbc2a58d521cab5b41617 | success | `generations/image-I1_v1.png` | à valider | 6 cr |
| Image infographie I2 (1:1) | v1 | gpt-image-2-text-to-image 1K | eb028314132be5b1205e21a7a8b15319 | success | `generations/image-I2_v1.png` | à valider | 6 cr |
| Objet O1 collagène (1:1, fond vert détouré) | v1 | gpt-image-2-text-to-image 1K | b2554d2bf1b7ff9ce314e408df9926ad | success | `generations/objet-O1_v1.png` | à valider | 6 cr |
| Image de départ 9:16 deuxième caméra | v2 | gpt-image-2-image-to-image 1K, refs : départ principale, photo de profil, photo de face, prompt `depart-9x16-camera2-v2.txt` | c873c96aa38bbac4081e3a7c61e17dcb | success | `sorties/config/depart_9x16_camera2_gpt_v2.png` | non retenue (choix de l'utilisateur) | 6 cr |
| Clip avatar S01 (1:1, 5 s) | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 = depart_1x1.png, @Audio1 = audio_avatar/S01.wav | 5a8809032d6a44808e8cfa659baae9bb | success | `avatar/S01_v1.mp4` | **retenu** (identité, cadre, lèvres OK ; Seedance prononce « constestent », « affiffinement », sans effet : voix off au montage) | 315 cr |
| Animation E1 (10 s) | v1 | minimax-h3/image-to-video 768P, image `generations/image-E1_v1.png` | 6d908532e3f0fdfba2c9a4129ca70bba | success | `generations/E1_v1.mp4` | **retenue** | 80 cr |
| Clip avatar A01 (9:16, 9 s) | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 = depart_9x16.png, @Audio1 = audio_avatar/A01.wav | 3003b50379025e0399ead5235d0ed915 | success | `avatar/A01_v1.mp4` | **retenu** (identité, cadre, lèvres OK ; « amensir » prononcé par Seedance, sans effet : voix off au montage) | 567 cr |
| Clip avatar A02 (9:16, 9 s) | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 = depart_9x16_camera2.png, @Audio1 = audio_avatar/A02.wav | 3f154b9292a4ea36d34b76f33262c986 | success | `avatar/A02_v1.mp4` | **retenu** (compte sur ses doigts fer et thyroïde, main ouverte sur collagène) | 567 cr |
| Clip avatar A03 (9:16, 14 s) | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 = depart_9x16.png, @Audio1 = audio_avatar/A03.wav | e71fa6cccd713dd5dcd269db28be18a1 | success | `avatar/A03_v1.mp4` | **retenu** (regard caméra pour le CTA ; « douce », « affirmation », « envoyerai » prononcés par Seedance, sans effet) | 882 cr |
| Clip avatar S01 | v2 | bytedance/seedance-2-5 720p, generate_audio, @Image1 = depart_1x1.png, @Audio1 = audio_avatar/S01.wav déclaré bande-son exacte + timeline mot à mot (`prompts/seedance-S01-v2.txt`) | 85cd2f847ff434b14e2a1d3878ec6ee3 | success | `avatar/S01_v2.mp4` | non retenu : retard jusqu'à 1,1 s malgré la voix off déclarée bande-son | 315 cr |
| Clip avatar A01 | v2 | bytedance/seedance-2-5 720p, generate_audio, @Image1 = depart_9x16.png, @Audio1 = audio_avatar/A01_v2.wav déclaré bande-son exacte + timeline mot à mot (`prompts/seedance-A01-v2.txt`) | 017731bdcb2ab07e4add978b50ad805e | success | `avatar/A01_v2.mp4` | non retenu : retard jusqu'à 0,7 s ; la v1 recalée mot par mot est plus fluide | 567 cr |
| Clip avatar S01 | S01_v3 | bytedance/seedance-2-5 720p, generate_audio, depart_1x1.png, @Audio1 = audio_avatar/S01_v3.wav (48 kHz, normalisé), prompt recherche web (liaison audio explicite, tête immobile) | f0d6d9245a0b02e41a0c96fd21e5ce0f | success | `avatar/S01_v3.mp4` | test : retard croissant jusqu'à 0,92 s | 315 cr |
| Clip avatar S01 | S01_v3_ecran-noir | bytedance/seedance-2-5 720p, generate_audio, depart_1x1.png, @Video1 = audio_avatar/S01_ecran-noir.mp4 (écran noir portant la voix off) | 0b092c62645b6ebf27b2dfa95201d670 | success | `avatar/S01_v3_ecran-noir.mp4` | test : 0 à 0,02 s sur les 5 premiers mots, puis jusqu'à 0,80 s | 342 cr |
| Clip avatar S01 | S01_profil_v1 | bytedance/seedance-2-5 720p, generate_audio, depart_1x1_profil.png (3/4 profil), @Audio1 = audio_avatar/S01_v3.wav, même prompt que v3 | 74230af3c8f802f6fdfebb5c949575d0 | success | `avatar/S01_profil_v1.mp4` | **retenu par l'utilisateur** (« le dernier clip que tu as envoyé est bien », version avec la voix Seedance) | 315 cr |
| Image de départ 1:1 profil (accroche) | v1 | gpt-image-2-image-to-image 1K | a88d27276cea42a77cf2fa6c0a972f61 | success | `sorties/config/depart_1x1_profil_gpt_v1.png` | test | 6 cr |
| B-roll B07 start frame | v1 | nano-banana-2-1 1K, 9:16, `prompts/broll-B07-depart.txt` | 2639274c351d47d3282177d7d4cba9c6 | success | `generations/broll-B07-depart_v1.png` | **retenue** | 4 cr |
| B-roll B07 animation | v1 | google/gemini-omni-flash-1-1 720p, 6 s, first_frame_url = start frame, `prompts/broll-B07-animation.txt` | 6a632c2519672c8685f6e32fc2963368 | success | `generations/broll-B07_v1.mp4` | **retenu** | 84 cr |
Références envoyées (dans cet ordre) : `Claire/avatar/avatar-face.jpg`, `Claire/avatar/avatar-profil.jpg`, `Claire/talking-head/_config/depart_9x16.png`. Prompt : `prompts/config/depart-9x16.txt`. Comparatif : `sorties/config/comparatif-depart-9x16.jpg`.

Deuxième caméra et 1:1 : générées à partir de `depart_9x16_gpt_v1.png` (+ photos de Claire). Prompts : `prompts/config/depart-9x16-camera2.txt`, `prompts/config/depart-1x1.txt`. Planche : `sorties/config/planche-images-depart.jpg`.

O1 : GPT Image 2 sur fond vert uni (#00B140), puis détourage par clé de couleur (`generations/objet-O1_v1_detoure.png`). Planche : `generations/planche-generations.jpg`.

**Total à ce stade : 4 421 cr (environ 22,11 $).** Contrôle des clips : `controle/planche_*.jpg` et transcriptions Whisper.

## Synchro lèvres et voix off (2026-10-08)

- Mesures (`controle/synchro_v1.txt`, `controle/synchro_v2.txt`, script `comparer_synchro.py`) : S01 v1 « Pourquoi » +0,5 s et 2 mots déformés ; A01 v1 dernière phrase +1,0 s ; A02 v1 max 0,4 s ; A03 v1 max 0,14 s.
- Demande de l'utilisateur : utiliser la voix off comme audio de Seedance pour que Claire parle avec cette voix. Sur KIE, Seedance 2.5 n'a pas d'option « garder l'audio fourni et caler les lèvres » (documentation vérifiée) : l'audio de référence sert de modèle et Seedance régénère la parole à son rythme. Test v2 (voix off déclarée bande-son exacte + timeline) : S01 +1,1 s, A01 +0,7 s. Pas d'amélioration fiable.
- Solution retenue pour le montage : `montage/recaler_mots.py`, recalage de l'image mot par mot sur la voix off (alignement de séquences tolérant aux mots déformés, vitesse d'image bornée entre 0,65 et 1,6), son Seedance remplacé par la voix off d'origine. Aperçus : `apercu/*_recale.mp4`. S01 v1 : 13 ancres, vitesse 1,00 à 1,40 ; A01 v1 : 26 ancres, vitesse 0,89 à 1,53.

- Recherche web (2026-10-08) et 3 essais S01 (`controle/synchro_v3.txt`). Technique retenue par l'utilisateur : lier explicitement l'audio à la parole (« @Audio1 is her dialogue voice […] sync her lip movement to @Audio1 »), ajoutée au gabarit 2 du skill ; le reste suit le skill.

Montage : rendu Remotion local (aucun crédit). Voir `montage.md`.
