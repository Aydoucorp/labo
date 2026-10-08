# Brief · Claire · parasites du cuir chevelu · Zack D

- **Date** : 2026-10-08
- **Concept** : Zack D (skill `skills/zack-d-style`), recette SPEEDY (lignes de 1 à 4 s).
- **Marque** : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`).
- **Entrées utilisateur** : `script-source.txt` (script avec balises d'émotion ElevenLabs), `VO.mp3` (ElevenLabs, voix Elise, 49,24 s).
- **Demande** : vidéo Zack D, voix off calée sur les plans.

## Script
`SCRIPT-FR.txt` : le script de l'utilisateur sans les balises, coupé en 20 lignes (une ligne = un plan), aucun mot changé. `SCRIPT-FR-tts.txt` : le même en un bloc.

## Calage
MMS (ctc-forced-aligner) : `align.py VO.mp3 SCRIPT-FR-tts.txt --method ctc` → `mots_mms.json` (159 mots), puis `align_vo_mms.py` → `shots_timing.json`. 0 mot non aligné. Scores faibles mais position cohérente : « le » (3,82 s), « gouttes » (12,40 s), « œufs » (14,80 s).

## Storyboard
`STORYBOARD.md` / `storyboard.json` : 21 clips, 22 stills de chaîne, durée Kling cumulée 65 s.

## Bibliothèque
Recherche « cuir chevelu parasites poux huile coco » : rien dans le style Zack D (monde bleu quadrillé, Pixar), tout est à générer. Format 100 % animé : pas de b-roll réel à placer.

## Modèles (ceux du skill)
- Images : gpt-image-2 (KIE), résolution à choisir par l'utilisateur.
- Clips : Kling 3.0 (KIE) `kling-3.0/video`, start + end, sans son, mode à choisir.

## Décisions
- Personnage-ancre : Claire en version Pixar, à partir de `Claire/talking-head/_config/depart_9x16.png` (copiée dans `refs/claire-ref.png`), pull bleu.
- Résolutions : images 1K (gpt-image-2, 6 cr), clips 720p (Kling 3.0 std, 14 cr/s), choisies par l'utilisateur le 2026-10-08. Budget estimé 1 054 cr (5,27 $) hors reprises.

## Points de vigilance (Brand DNA)
Le Brand DNA interdit les allégations santé et demande de renvoyer vers un professionnel. Le script affirme que l'arbre à thé « tue les œufs » et que l'huile de coco « étouffe » les parasites : script de l'utilisateur, livré tel quel, signalé.

## Prompts et réglages
- Setup (gpt-image-2 image-to-image, 1K, 9:16) : prompts exacts dans `jobs/setup.json` (`CHAR-sheet` : refs claire-ref + plate ; `M-cuir-chevelu` : ref plate).
- Stills (gpt-image-2 image-to-image, 1K, 9:16) : prompts dans `jobs/stills.json`, écrits par `work/ecrire_stills.py`. Refs : plate en 1re, fiche perso en 2e quand Claire apparaît, coupe `M-cuir-chevelu` pour S15-S16, S02 comme référence des parasites pour S03, S09, S10, S13.
- Reprises demandées par l'utilisateur : S08 (posture tordue), S18 et S19 (Claire en pied). Anciennes versions dans `jobs/_rejets/`. S06 gardé tel quel (validé).
- Clips (Kling 3.0 `kling-3.0/video`, mode std 720p, sans son, start + end, 9:16) : prompts dans `jobs/legs.json`, écrits par `work/ecrire_legs.py`. 21 clips, 65 s.
