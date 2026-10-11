# Brief · Confihair · 20 pistes de logo (Z-Image)

Date : 2026-10-11

## Demande

- Générer les 20 prompts de logo fournis par l'utilisateur (`prompts/prompts-logo-confihair.txt`, « Confihair : 20 prompts de logo (11/10/2026) »), sans les modifier.
- Modèle choisi par l'utilisateur : **Z-Image sur KIE**, résolution 1K (le moins cher de la grille KIE).

## Références et charte (rappel du fichier de prompts)

- Exprimer le premium, une chevelure dense, épaisse, forte, une femme adulte chaleureuse (45 à 60 ans) ; fuir le médical, le girly, le miracle.
- Couleurs : encre `#0D0B04`, tabac `#5C4329`, jaune `#FFDA49` en touche, papier `#FAF3E1`. Le pétrole `#00353E` est réservé au bouton d'achat, absent des logos.
- Pas de photo produit nécessaire pour un logo. Confihair n'a pas encore de dossier `refs/produits/` ni de brand DNA dans le studio.

## Modèle et réglages

| Réglage | Valeur |
|---|---|
| Modèle | `z-image` (KIE, endpoint `/api/v1/jobs/createTask`) |
| Ratio | 1:1 |
| Résolution | ~1K (Z-Image n'a pas de réglage de résolution) |
| Références | aucune (texte vers image seulement) |
| Prompts | les 20 du fichier, mot pour mot, un fichier par piste dans `prompts/logo-NN.txt` (tous sous la limite de 1000 caractères) |
| Coût | 0,8 crédit par image, soit 16 crédits (0,08 $) pour les 20 (grille KIE relevée le 11/10/2026) |

Comparatif présenté à l'utilisateur avant le choix (crédits par image) : Z-Image 0,8 ; Seedream 5 Flash 1K 3,24 ; Ideogram v3 Turbo 3,5 ; Nano Banana 2.1 1K 4, 2K 6, 4K 9. Higgsfield (Nano Banana 2.1 : 1,5 / 2 / 3 crédits en 1K / 2K / 4K) écarté : compte à 0 crédit, et l'utilisateur veut KIE.

## Reproduire

```
python3 generer_logos.py            # les 20 pistes
python3 generer_logos.py 4 13       # seulement certaines pistes
```

Chaque génération est notée dans `journal.md` (taskId, état, fichier, crédits).

## Sorties

- `sorties/logo-NN_<piste>_v1.png` : en attente de génération (clé `KIE_API_KEY` absente de la session au 11/10/2026).
