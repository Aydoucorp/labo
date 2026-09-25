# Références de la maquette papier · Claire · Guide racine

Toutes validées le 2026-09-25. Fichiers retenus dans `retenues/references/`, variantes dans `sorties/references/`, prompts dans `references/prompts/`.

| Réf | Fichier retenu | Rôle | Moteur | Statut |
|---|---|---|---|---|
| R1 | `r1-couverture.png` | Couverture plate du guide (2:3, 2K) | Nano Banana 2 (KIE), v4 | Validée : textes exacts, aucun visage |
| R2 | `r2-packshot.png` | Packshot découpé du guide, bord déchiré + ombre (4:5, 2K) | Nano Banana 2 (KIE), réf. R1 | Validé : couverture fidèle |
| R3 | `r3-palette-matieres.png` | Planche palette émotionnelle + matières déchirées (9:16) | Nano Banana 2 (KIE), v2 | Validée : aucun texte |
| R4 | `r4-specimen-titres.png` | Spécimen des lettres découpées et taille des titres (9:16) | Nano Banana 2 (KIE) | Validé : « ÇA TOMBE », « RACINE », « FAUX », « pas aux ciseaux » exacts |
| R5 | `r5-maquette-mise-en-page.png` | Gabarit de mise en page au pixel (dessiné par `r5_maquette.py`) | Python / Pillow | Validé |

## Palette émotionnelle

| Rôle | Teinte | Plans |
|---|---|---|
| Base papier | Crème `#FAF6F3` | tous |
| Problème / mythe | Terracotta `#A8553A`, clair `#C9805F` | P01-P05, P10 |
| Verdict / contraste | Prune `#7A4351` | P06-P07 |
| Résolution | Sauge `#8C9B86` (décor seulement) | P08-P09, P11 |
| Encre | `#2E2A26` | titres |
| Neutres | Crème foncé `#EFE7E0`, argent `#B4ADA4` (décor seulement), kraft, papier journal flou | fonds de couches |

## Matières

Papier crème vieilli à grain et plis, papier déchiré à bord blanc fibreux, kraft, papier journal illisible, ruban adhésif de masquage, feutre noir (flèche, soulignement, marques d'impact, cercle, X), éclaboussures aquarelle terracotta et sauge, tampon prune, photos découpées à bord blanc.

## Taille des mots (gabarit 1080 × 1920)

- Zones vides : 220 px en haut, 380 px en bas (interface Reels / TikTok), 60 px sur les côtés.
- Titre 1 à 3 mots : lettres de 170 à 260 px (9-13 % de la hauteur), largeur ≤ 960 px, zone 260-620 px.
- Note au feutre : 60 à 90 px (environ 1/3 du titre), zone 630-720 px.
- Visuel découpé : 740-1500 px, un seul foyer, 3-4 couches.

## Place du packshot (P11)

Centré, 620 × 775 px (57 % de la largeur), entre 700 et 1480 px de hauteur, incliné de 3°, bord déchiré blanc et ombre de contact. Titre « MES RECETTES » au-dessus (260-560 px).

## Utilisation dans les prompts

R3 et R4 sont jointes comme références de style à chaque plan (R4 : jamais recopier ses mots). R2 est jointe comme produit au plan P11. Voir `prompts.md`.
