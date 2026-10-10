# Brief · Claire · avant/après « 3 produits » (téléchargement 4), découpe pour VMake

Date : 2026-10-09

## Demande

- Vidéo source : 11,3 s, 720×1280, 30 i/s, 339 images. Avant/après capillaire : golfes et cheveux clairsemés, pointes abîmées, puis longueurs longues et ondulées. Textes incrustés : « there are THREE products that helped me transform my hair from THIS to... » (0 à ~5,5 s), « THIS 🤩🙌😉 » (~5,5 s à la fin), « details in caption » (~9,5 s à la fin).
- Découper en parties de 5 s maximum, numérotées, pour effacer les textes avec VMake ; Claude réassemblera ensuite.

## Découpe (à l'image près, filtre `select`, H.264 CRF 14, son AAC 192 kb/s)

| Fichier | Images | Temps |
|---|---|---|
| `sorties/a-nettoyer/partie-1_0-5s.mp4` | 0 à 149 | 0 à 5 s |
| `sorties/a-nettoyer/partie-2_5-10s.mp4` | 150 à 299 | 5 à 10 s |
| `sorties/a-nettoyer/partie-3_10-11.3s.mp4` | 300 à 338 | 10 à 11,3 s |

## Réassemblage (`assembler.py`)

- Parties nettoyées reçues : `source/nettoyees/partie-1.mp4` à `partie-3.mp4` (720×1280, 147 / 147 / 36 images).
- Comme pour la vidéo précédente, VMake a retiré les 3 premières images de chaque partie : chaque partie est précédée de 3 copies de sa première image, soit 339 images au total, calées sur le son d'origine continu.
- Agrandissement Lanczos en 1080×1920, H.264 CRF 18, AAC 192 kb/s, 11,3 s. Pas de texte, pas de bandeau, pas de CTA.

## Textes d'origine et traduction (pour mémoire)

- « there are THREE products that helped me transform my hair from THIS to... » : Il y a TROIS produits qui m'ont aidée à transformer mes cheveux, de ÇA à...
- « THIS 🤩🙌😉 » : ÇA 🤩🙌😉
- « details in caption » : détails en description
- Description d'origine : shampoing clarifiant/détox, masque hydratant profond, masque à l'huile cuir chevelu (aucune marque citée, CTA « TRANSFORM »).

## Sorties

- `sorties/claire-trois-produits-sans-texte_v1.mp4` (en attente de validation), `sorties/planche-contact_v1.jpg`
