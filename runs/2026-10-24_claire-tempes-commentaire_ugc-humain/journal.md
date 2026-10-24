# Journal : UGC tempes, réponse à un commentaire

Clips : `wan/3-0-video` 480P 9:16, audio activé, @Image1 `retenues/cadrage.png` seule, @Video1 voix en écran noir (`audio/clips/`), prompts `prompts/video/<clip>.txt`.

| Date | Clip | Durée | Task id | Coût | Mots (son Wan / voix) | Lèvres p/b/m | Correction au montage |
|---|---|---|---|---|---|---|---|
| 2026-10-24 | W1 (0,5 s de silence en tête) | 9 s | 704b3a403ae1919b69f20a1395064eed | 136 cr | 31/31, écart nul (2 premiers mots après pause mal datés par Whisper) | 5/6 | début source 0,5 s |
| 2026-10-24 | W3 | 6 s | 5d54e41de9a0b97cfb41b2a692ded3a0 | 96 cr | 15/15, retard de 0,3 s sur « ils réagissent vite » | 1/1 | recalage à 23,95 s (+0,3 s) |
| 2026-10-24 | W4 | 2 s | 6f50addd1c184fa12d1f283f1f3a5c1d | 32 cr | retard constant d'environ 0,24 s | 1/1 | début source 0,24 s |
| 2026-10-24 | W5 | 4 s | 33f92b28bd42fa0f2b0dc2389adcfbee | 64 cr | 16/16, écart max 0,02 s | aucune p/b/m | aucune |
| 2026-10-24 | W6 | 4 s | ea85620fdd14a41378560ed7064e114f | 64 cr | 13/13, retard de 0,35 s sur « à cet endroit » | 2/2 | recalage à 52,48 s (+0,34 s) |
| 2026-10-24 | W7 | 8 s | 36f42b43767d1ff1121e32f95f75b5e6 | 128 cr | 33/33, retard de 0,25 à 0,38 s sur la fin | aucune p/b/m | recalage à 63,25 s (+0,3 s) |

Total clips : 520 cr. Images : 7,6 cr. Total du run à ce stade : 527,6 cr (environ 2,64 $). Tenue et coiffure stables sur les 6 clips. Aperçus recalés : `sorties/apercus/`.

## 2026-10-24 : B3, B4 reçus, B2d confié au studio
- Reçus de l'utilisateur : 4 extraits d'une même vidéo TikTok pour B3 (texte retiré) et 1 vidéo microscope pour B4, copiés dans `rushes/recus/`.
- B3 retenu : `b3-candidat-2.mp4` 0 à 4,0 s + `b3-candidat-1.mp4` 0 à 0,87 s (les autres moments montrent des flacons de marque : écartés). B4 : `b4-microscope.mp4` 0 à 4,85 s.
- Aperçu avec la voix (26,88 à 36,60 s) : `montage/apercus/apercu-b3-b4.mp4`.
- Origine (réel ou IA) des rushes reçus : à confirmer par l'utilisateur avant l'enregistrement en bibliothèque.
- B2d (lunettes) : l'utilisateur demande que le studio le génère avec Nano Banana 2.1 (1K, 4 cr), entrée `retenues/cadrage.png`, prompt `prompts/image/B2d-lunettes-v1.txt`. En attente de la clé KIE (absente du conteneur).

## 2026-10-24 : B6, motion design contre 3D
- Demande : voir B6 en motion design et recevoir en même temps un prompt 3D, pour comparer.
- Motion design : `work/motion_b6.py` (Pillow, gratuit) → `sorties/motion/B6-motion-v1.mp4` (5,30 s), aperçu avec la voix `montage/apercus/apercu-b6-motion.mp4`. Trois temps calés sur les mots : « lifté » 1,12 s (flèches de lift qui s'inversent, tempes qui reculent, coin de bouche qui retombe), « ligne frontale » 1,74 s (zoom, pointillés terracotta sur la ligne frontale, qui s'effritent sur « fragile » 2,69 s), « coiffer » 3,74 s (un peigne passe, les mèches se relèvent puis retombent, retour sur « compliqué » 4,68 s).
- Pillow système cassé après le redémarrage du conteneur : rendu fait avec un environnement Python temporaire (Pillow 13).
- Option 3D : prompt texte seul `prompts/video/B6-3d-v1.txt` (buste 3D façon rendu médical sur fond prune, 6 s), ajouté en carte « B6-3D » dans `1-brolls-tempes-commentaire.html`.
- Clé KIE : toujours absente (aucun `.env` dans le conteneur, rien dans les fichiers ignorés).
