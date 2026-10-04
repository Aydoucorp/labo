# Brief · Claire · sérum maison aux plantes (bandeaux FR)

Date : 2026-10-04
Concept : montage léger sur une vidéo existante (série full-b-roll-artiste 002 à 004).

## Demande

- Vidéo source : recette d'un sérum maison pour le cuir chevelu (laurier, romarin, clous de girofle), 42,7 s, 720×1280, textes anglais incrustés (relevé complet et traduction : `textes.md`).
- L'utilisateur a nettoyé lui-même les 5 premières secondes (`source/debut-0-5s_sans-texte.mp4`) : rien n'y est ajouté, il pose son hook avec son application.
- Le reste : bandeaux comme d'habitude (terracotta, texte crème), pas de motion CTA, son d'origine.
- Mot modifié à la demande : « frémir » remplacé par « mijoter à feu doux ».

## Réglages

- Le début nettoyé commence à l'image 3 de l'original (décalage mesuré par comparaison d'images) : 147 images nettoyées, puis l'original à partir de l'image 150 ; son d'origine décalé de 0,1 s. Durée finale 42,53 s.
- Boîtes et timings de ses textes : `reperer_textes.py` (top-hat sur les pixels blancs, masque fixe par texte, présence image par image), `work/textes.json` ; boîte de « strain well... » corrigée à la main (225, 452, 495, 492).
- Bandeaux : terracotta `#A8553A`, texte crème `#FAF6F3`, TikTok Sans SemiBold 60 px, interligne 72 px, coins 26 px, lignes équilibrées (860 px max), émojis Noto 62 px ; chaque bandeau couvre la boîte de son texte + marge, de 3 images avant à 3 images après son texte (jamais avant l'image 150).
- Sortie 1080×1920, H.264 CRF 18, AAC 192 kb/s.

## Reproduire

```
python3 reperer_textes.py
python3 montage_bandeaux.py --frames 8,13,23   # images de contrôle
python3 montage_bandeaux.py
```

## Sorties

- `sorties/claire-serum-maison-fr_v1.mp4` (validée : copiée dans `retenues/` et dans `creas/full-b-roll-artiste/2026-10-04_full-b-roll-artiste_004.mp4`), `sorties/planche-contact_v1.jpg`
- `sorties/a-nettoyer/` : la fin découpée en morceaux de 5 s (proposée puis abandonnée au profit des bandeaux)
