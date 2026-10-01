# Brief : Claire, arrêter le minoxidil (full b-roll artiste)

- Date : 2026-10-01
- Marque : Les cheveux de Claire (lire `Claire/BRAND-DNA-CLAIRE.md`)
- Concept : full b-roll artiste (skill `skills/creation-full-b-roll-artiste`)
- Entrées : `voix.mp3` (voix off ElevenLabs, 79,57 s), `script.txt`
- Profil : EDU (éducatif organique), plateforme TikTok, 9:16, 1080x1920, 30 i/s
- Sous-titres : karaoké mot à mot blanc avec contour, boîte rouge pendant le hook

## Étapes et réglages

1. Alignement : `align.py voix.mp3 script.txt` (MMS ctc-forced-aligner, 259 mots, 2 mots isolés à score bas, normal).
2. Features : 21 pauses, aucune au-dessus de 0,5 s (pas de resserrage), 13 mots appuyés, -19,2 LUFS, 3,27 mots/s.
3. Beats : `propose_beats.py --profile EDU` (24 beats mécaniques), puis découpe manuelle en 21 beats et 31 plans (`work/ecrire_brief.py`).
4. Validation : `validate_brief.py brief.json --fix-slugs` : 0 erreur, 0 avertissement.
5. Shot list : `build_brief.py` → `brief.html`.

## Structure

| Section | Temps | Plans |
|---|---|---|
| HOOK | 0,0 à 5,0 s | 4 |
| PROB | 5,0 à 19,6 s | 6 |
| OBJ | 19,6 à 23,75 s | 2 |
| MECA | 23,75 à 61,2 s | 13 |
| BENEF | 61,2 à 64,05 s | 1 |
| PREUVE | 64,05 à 68,85 s | 1 |
| PROD | 68,85 à 74,0 s | 2 |
| CTA | 74,0 à 79,57 s | 2 |

Types : UGC 17, 3DSCI 7, MOTION 3, STOCK 3, PRODUIT 1. Part UGC + PRODUIT : 55 %.

## Look book (à valider)

- Lumière : naturelle de fenêtre, matin, tons chauds
- Palette : crème, terracotta, bois clair, prune en accent
- Décor : salle de bain et pièce de vie d'une maison française, table en bois clair
- Personnes : femme de 40 à 50 ans, cheveux châtains ondulés avec quelques fils blancs, visage hors champ ou de profil, rendu smartphone
- Suffixe : natural window light, warm cream and terracotta tones, real woman in her 40s, smartphone footage, shallow depth of field

## Points de charte

- Le « 50 % » est une peur citée : affiché « « 50 % de mes cheveux ? » », jamais comme un fait.
- Sources à afficher et à vérifier sur « testées face au minoxidil » : Panahi et al., SKINmed 2015 (romarin contre minoxidil 2 %) ; Ibrahim et al., J Cosmet Dermatol 2021 (pépins de courge contre minoxidil 5 %).

## Générations IA

Choix de l'utilisateur (2026-10-01) : seuls les 8 plans IA sont générés (07, 08, 10, 14a, 14b, 15b, 17, 21b), le guide 21b en 3D, option A (Nano Banana 2 1K puis MiniMax H3 768P). Les 20 plans réels sont cherchés par l'utilisateur.

### Images (étape 1)

- Modèle : Nano Banana 2 (`nano-banana-2`), 1K, ratio 9:16, sans référence. Script : `python3 scripts/kie_image.py --prompt-file prompts/img/<plan>.txt --out sorties/plans/<plan>-img-v1.png --ratio 9:16 --resolution 1K`
- Prompts : `prompts/img/<plan>.txt` (description du plan + bloc de style commun : rendu 3D scientifique, palette terracotta, crème, rose chair et prune, fond prune sombre ; fond crème pour 21b ; aucun texte dans l'image).
- Sorties : `sorties/plans/<plan>-img-v1.png` (768x1376), planche `sorties/plans/planche-3d-v1.jpg`.
- Coût : 8 x 8 cr = 64 cr. Tâches KIE dans `logs/<plan>-img-v1.log`.

### Animations (étape 2)

- Images validées par l'utilisateur (« go »), aucun texte voulu dans les clips (texte uniquement au montage : sous-titres, mentions des plans 08 et 14b).
- Modèle : MiniMax H3 image vers vidéo (`minimax-h3/image-to-video`), 768P, 4 s demandées (4,46 s reçues, 768x1344). Script : `python3 scripts/kie_minimax.py --prompt-file prompts/ani/<plan>.txt --image sorties/plans/<plan>-img-v1.png --out sorties/clips/<plan>-clip-h3-v1.mp4 --duration 4 --resolution 768P`
- Prompts : `prompts/ani/<plan>.txt` (mouvement du plan + « aucun texte, pas de morphing, pas de changement de sujet »).
- Sorties : `sorties/clips/<plan>-clip-h3-v1.mp4`, planche `sorties/clips/planche-clips-v1.jpg`. Contrôle visuel : 8/8 sans texte ni déformation.
- Coût : 8 x 32 cr = 256 cr. Total IA du run : 320 cr.

### Plan 21a (étape 3)

- Demande de l'utilisateur : générer 21a avec MiniMax H3 768P, avec du texte dans la vidéo.
- Image : Nano Banana 2 1K, `prompts/img/21a.txt` (vue subjective, téléphone, « Guide » tapé dans le champ de commentaire, seul texte lisible). Vidéo : MiniMax H3 768P 4 s, `prompts/ani/21a.txt` (le pouce envoie le commentaire). On garde 0 à 3,6 s.
- Coût : 8 + 32 = 40 cr. Total génération du run : 360 cr.

## Montage

Voir `montage.md`. Rushes rapatriés du Drive (`rushes/drive/`), QC 100/100, créa finale `creas/full-b-roll-artiste/2026-10-01_full-b-roll-artiste_001.mp4`. Tous les plans sont enregistrés dans `bibliotheque/brolls.json`.
