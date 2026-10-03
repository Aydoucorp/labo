# Brief · Claire · thyroïde, fer ou stress (texte FR sur vidéo)

Date : 2026-10-03
Concept : montage léger sur une vidéo existante (série des créas full-b-roll-artiste 002 et 003).

## Demande

- Vidéo source : « Video by thyroidalchemy », 4,9 s, 720×1280, gros plan d'un cuir chevelu clairsemé, mains qui écartent les cheveux. Texte d'origine déjà retiré par l'utilisateur.
- Texte d'origine (capture fournie) : « How to tell if your hair loss is a thyroid, iron or stress pattern... in 60 seconds ⤵️ ».
- Choix de l'utilisateur : traduction sans « en 60 secondes » (le clip dure 5 s), pas de bandeau, pas de motion CTA, son d'origine.

## Texte FR

« Comment savoir si ta chute de cheveux vient de la thyroïde, du fer ou du stress ⤵️ », sur toute la durée.

Style (comme la capture) : TikTok Sans Bold 80 px (1080×1920), blanc, contour noir 6 px, ombre noire (décalage 3/5 px, flou 5 px), aligné à gauche à 60 px, largeur max 900 px, interligne 98 px, bloc centré à y = 900, émoji ⤵️ Noto 78 px en fin de texte.

## Réglages

- Agrandissement Lanczos 720×1280 vers 1080×1920, H.264 CRF 18, son d'origine en AAC 192 kb/s.

## Reproduire

```
python3 montage_texte.py --frames 0.5,3   # images de contrôle
python3 montage_texte.py                  # rendu
```

## Sorties

- `sorties/claire-thyroide-fer-stress-fr_v1.mp4` (en attente de validation)
