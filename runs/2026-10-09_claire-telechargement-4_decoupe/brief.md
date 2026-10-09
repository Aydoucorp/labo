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

## Suite

En attente des parties nettoyées. Rappel : sur la vidéo précédente, VMake a retiré les 3 premières images de chaque partie (comblées au réassemblage par répétition de la première image).
