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

Aucune lancée. Résolution et modèle à choisir par l'utilisateur avant toute génération (règle du studio).
