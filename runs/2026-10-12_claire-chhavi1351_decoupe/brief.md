# Brief · Claire · huile de romarin (vidéo chhavi1351) · découpe pour VMake

Date : 2026-10-12

## Demande

1. Couper tous les moments où l'on voit la boîte du produit → V1.
2. Découper la V1 en parties de 5 s maximum.
3. L'utilisateur efface les textes de chaque partie dans VMake (« remove text ») et renvoie les parties.
4. Rassembler les parties nettoyées et remettre les textes en français.

## Source

- `source/original.mp4` : « Video by chhavi1351 », 28,77 s, 720×1280, 30 i/s, 863 images, son d'origine (musique).
- Produit montré : boîte « Brillare Rosemary Oil Shots ». Les fioles et le compte-gouttes restent (seule la boîte est coupée).

## 1. V1 sans la boîte

Plans retirés (repérés par détection de changements de plan puis vérifiés image par image) :

| Plan | Images source | Temps source |
|---|---|---|
| Boîte de face | 125 à 182 | 4,17 à 6,10 s |
| Boîte, face avant de près | 225 à 265 | 7,50 à 8,87 s |
| Boîte, liste des ingrédients | 338 à 376 | 11,27 à 12,57 s |

Résultat : `sorties/claire-chhavi-sans-boite_v1.mp4`, 725 images, 24,17 s. Son d'origine laissé en continu (pas de saut de musique aux coupes), coupé à 24,17 s avec un fondu de sortie de 0,8 s.

## 2. Parties à nettoyer dans VMake

Toutes coupées sur un changement de plan, 5 s maximum (`sorties/a-nettoyer/`) :

| Partie | Images V1 | Durée |
|---|---|---|
| `partie-1_0-4.2s.mp4` | 0 à 124 | 4,17 s |
| `partie-2_4.2-8.6s.mp4` | 125 à 258 | 4,47 s |
| `partie-3_8.6-12.9s.mp4` | 259 à 385 | 4,23 s |
| `partie-4_12.9-17.8s.mp4` | 386 à 533 | 4,93 s |
| `partie-5_17.8-20.7s.mp4` | 534 à 620 | 2,90 s |
| `partie-6_20.7-24.2s.mp4` | 621 à 724 | 3,47 s |

Rappel : VMake perd les 3 premières images de chaque partie ; au réassemblage, compléter avec 3 copies de la première image (comme `2026-10-07_claire-trendtrack-7688758403652439328_decoupe/assembler.py`).

## Textes de la vidéo (anglais → proposition FR)

| Texte d'origine | Proposition FR |
|---|---|
| My hair before these Rosemary Oil Shots... ❤️‍🩹 | Mes cheveux avant ces shots d'huile de romarin... ❤️‍🩹 |
| I tried everything. Nothing worked 💔 | J'avais tout essayé. Rien ne marchait 💔 |
| Then I started using Brillare Rosemary Oil Shots consistently... | Puis j'ai commencé à utiliser ces shots d'huile de romarin régulièrement... (nom de marque retiré, comme la boîte) |
| 20% Rosemary Concentration — the clinically effective dose | 20 % de romarin concentré, la dose efficace selon les études cliniques |
| 100% Plant-Based. | 100 % d'origine végétale. |
| Single-use vials | Fioles à usage unique |
| Hair fall reduced in just 14 days ✨ | Chute de cheveux réduite en seulement 14 jours ✨ |
| Before ❤️‍🩹 / After ✨ | Avant ❤️‍🩹 / Après ✨ |
| Baby hairs showing up 😍 | Les baby hairs qui repoussent 😍 |
| Visible results in just 4 weeks ✨ | Résultats visibles en seulement 4 semaines ✨ |
| Consistent use = visible difference ❤️ | Utilisation régulière = différence visible ❤️ |
| Right dose. Real results. ✨ | La bonne dose. De vrais résultats. ✨ |
| Comment 'ROSEMARY' for link | Commente « ROMARIN » pour avoir le lien |

À valider avec l'utilisateur avant le montage final (formulations, mot du CTA).

## Reproduire

```
python3 decouper.py   # V1 sans la boîte + parties à nettoyer
```

## Sorties

- `sorties/claire-chhavi-sans-boite_v1.mp4` (V1 sans la boîte, avec ses textes anglais)
- `sorties/a-nettoyer/partie-1` à `partie-6` (à passer dans VMake)
