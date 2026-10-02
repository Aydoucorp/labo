# Brief · Claire · chute de cheveux à 40 ans, avant/après (sous-titres FR sans bandeau + CTA)

Date : 2026-10-02
Concept : montage léger sur une vidéo existante (même principe que `2026-10-02_full-b-roll-artiste_002`).

## Demande

- Vidéo source : TikTok « Video by pure.batana76 », 14,8 s, 720×1280, musique seule, textes anglais incrustés (« Day 1 / Hair loss at 40 is terrifying 😢💔 », « Day 14 », « Day 90 », « Day 180 😍 »), puis le flacon Batana et « Link in bio » à la fin.
- Mêmes traitements que la vidéo précédente : textes en français, CTA Claire en motion.
- Couper le moment où elle montre le produit : la spectatrice ne doit pas savoir quel produit est utilisé, elle commente GUIDE pour recevoir la solution.
- Effacer ses textes sans bandeau, gratuitement.

## Effacement des textes : choix de l'outil

| Option | Verdict |
|---|---|
| IA payantes KIE (Wan 2.7 Video Edit ~190 cr, HappyHorse ~340 cr pour 12 s en 720p) | Chiffrées, écartées par l'utilisateur (« fais-le gratuitement »). |
| hjunior29/video-text-remover (proposé par l'utilisateur) | Détection YOLO, mais effacement par filtres OpenCV (Telea / Navier-Stokes) : taches floues visibles, testé ici, écarté. |
| ProPainter (référence en inpainting vidéo, utilisé par video-subtitle-remover, VideoSubtitleRemover, videowipe…) | Licence S-Lab non commerciale : interdit pour de la pub. Écarté. |
| **LaMa** (Carve/LaMa-ONNX, licence Apache 2.0) | **Retenu** : usage commercial autorisé, tourne sur CPU (~4,5 s par image), rendu propre sur cuir chevelu et meubles. |

Méthode (`masques.py` puis `effacer_textes.py`) :
- un masque fixe par texte : pixels blancs fins (top-hat > 40, niveau > 200) présents sur au moins 80 % des images où le texte est pleinement visible, dilatés (ellipse 15 px + ombre décalée de 3 à 4 px vers le bas et la droite), émojis pris en rectangle ;
- dilatation supplémentaire de 9 px au moment de l'effacement ;
- LaMa sur la bande y = 60 à 420 (720×360 complétée en miroir, ramenée à 512×512), recollée uniquement dans le masque avec un bord adouci (flou gaussien 2 px) ;
- plages d'application, fondus compris : hook 0 à 92, jour 1 : 12 à 92, jour 14 : 86 à 172, jour 90 : 164 à 292, jour 180 : 256 à 351 (images).

## Textes FR (timings calés sur les siens)

| Début | Fin | Texte |
|---|---|---|
| 0,00 | 2,63 | La chute de cheveux / à 40 ans, c'est terrifiant 😢💔 |
| 0,50 | 2,63 | Jour 1 |
| 3,23 | 5,37 | Jour 14 |
| 5,83 | 8,63 | Jour 90 |
| 9,70 | 12,65 | Jour 180 😍 |

Style : comme les siens, sans bandeau. TikTok Sans SemiBold 68 px (1080×1920), blanc, contour noir 5 px, ombre portée noire (décalage 3,5 px, flou 4 px), émojis Noto Color Emoji 74 px, fondu 0,12 s.

## Fin

- Le flacon entre dans le cadre à 11,73 s (image 352) : gel sur l'image 351 à partir de 11,70 s, zoom lent 1,2 %/s.
- Flou + assombrissement de 12,40 à 12,80 s, carte CTA à 12,65 s : « Commente GUIDE pour recevoir la solution » (même carte crème, pastille GUIDE terracotta, barre de commentaire, flèche que la créa 002).
- Musique : son d'origine jusqu'à 14,70 s, raccord à 9,20 s (fondu enchaîné 0,15 s), fondu de sortie 0,8 s. SFX `whoosh_soft` + `tick_soft` sur la carte. Durée totale 15,8 s.

## Reproduire

```
python3 masques.py            # masques de ses textes
python3 effacer_textes.py     # effacement LaMa -> work/efface.mkv (~25 min sur 4 CPU)
python3 montage_soustitres.py --frames 1.5,4,7,10.5,13.5   # images de contrôle
python3 montage_soustitres.py # rendu complet
```

## Sorties

- `sorties/claire-chute-40-ans-fr_v1.mp4` (en attente de validation)
