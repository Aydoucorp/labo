# Brief · Claire · sérum pousse sans minoxidil (vidéo jenronfit) · découpe pour VMake

Date : 2026-10-14

## Demande

1. Couper la vidéo en parties de 5 s maximum.
2. L'utilisateur efface les textes de chaque partie dans VMake et renvoie les parties.
3. Rassembler les parties nettoyées et remettre les textes en français dans le style d'origine (comme `2026-10-12_claire-chhavi1351_decoupe`).

## Source

- `source/original.mp4` : « Video by jenronfit », 13,17 s, 720×1280, 30 i/s, 395 images, son d'origine.
- Contenu : 0-3,7 s, cheveux tombés dans une main puis plusieurs plans d'elle (« You should use minoxidil ») ; 3,7-6,6 s, montre un flacon de sérum bleu et son compte-gouttes ; 6,6-13,2 s, face caméra, cheveux longs et volumineux, encarts photo avant/après.
- Textes anglais incrustés (lus sur la planche, à vérifier au montage) : « "You should use minoxidil" » ; « No thank you... because THIS growth serum exists » ; liste « - reduces shedding by 92% / - reduces breakage immediately / - visible growth within 30-60 days / - non-greasy formula / - zero minoxidil or finasteride » ; « reduced my shedding in 4 weeks! » ; « completely transformed my hair ».

## Parties à nettoyer dans VMake

Coupées sur un changement de plan (détection ffmpeg, seuil 0,2), 5 s maximum (`sorties/a-nettoyer/`) :

| Partie | Images source | Durée |
|---|---|---|
| `partie-1_0-3.7s.mp4` | 0 à 111 | 3,73 s |
| `partie-2_3.7-6.6s.mp4` | 112 à 198 | 2,90 s |
| `partie-3_6.6-10.7s.mp4` | 199 à 321 | 4,10 s |
| `partie-4_10.7-13.2s.mp4` | 322 à 394 | 2,43 s |

Rappel : VMake perd les 3 premières images de chaque partie ; au réassemblage, compléter avec 3 copies de la première image.

## Reproduire

```
python3 decouper.py
```

## Textes FR (12/10 → 14/10, décisions utilisateur)

| Texte d'origine | Texte FR à remettre |
|---|---|
| "You should use minoxidil" | *(non remis : l'utilisateur l'ajoute lui-même à la main)* |
| No thank you... because THIS growth serum exists | Non merci… parce que CETTE huile existe (texte de l'utilisateur) |
| - reduces shedding by 92% | - réduit la chute de 92 % |
| - reduces breakage immediately | - réduit la casse dès la première utilisation |
| - visible growth within 30-60 days | - pousse visible en 30 à 60 jours |
| - non-greasy formula | - formule non grasse |
| - zero minoxidil or finasteride | - zéro minoxidil, zéro finastéride |
| reduced my shedding in 4 weeks! | ma chute a diminué en 4 semaines ! |
| completely transformed my hair | a complètement transformé mes cheveux |

Le plan du flacon (3,7 à 6,6 s) est gardé. Sérum non identifié (étiquette « TA… » / « …CAL », flacon bleu à compte-gouttes) : `work/flacon*.jpg`.

## Montage FR (`montage_texte.py`)

- Parties nettoyées reçues dans `source/nettoyees/partie-1` à `partie-4` : 3 premières images perdues par partie (décalage mesuré), compensées par 3 copies de la première image. 395 images.
- Style relevé sur l'original : blanc, demi-gras, centré, sans contour, ombre douce. TikTok Sans 600, tailles calées sur la largeur des textes anglais (« Non merci… » 38,7 px source, le reste 28,3 à 29,5 px), lignes de plus de 640 px source coupées en deux.
- Plages (images) et centres verticaux (px source) : « Non merci… » 112–147 (735) ; « parce que CETTE huile / existe » 112–147 (786, interligne 31) ; liste ligne par ligne comme l'original, jusqu'à 271 (centres 685, 729, 772, 816, 861 ; apparitions 148, 166, 187, 214, 238) ; « ma chute a diminué en 4 semaines ! » 272–321 (790) ; « a complètement transformé mes cheveux » 322–379 (697). 0–111 sans texte (hook ajouté par l'utilisateur).
- Son d'origine. Sortie 1080×1920, H.264 CRF 18, AAC 192 kb/s.

```
python3 montage_texte.py --frames 130,250   # images de contrôle (work/)
python3 montage_texte.py                    # montage complet
```

## Sorties

- `sorties/a-nettoyer/partie-1` à `partie-4` (à passer dans VMake)
- `sorties/claire-huile-sans-minoxidil-fr_v1.mp4` (montage FR, en attente de validation)
