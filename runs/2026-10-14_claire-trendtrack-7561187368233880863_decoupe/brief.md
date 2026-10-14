# Brief · Claire · quantité d'après-shampoing (TikTok Trendtrack 7561187368233880863) · découpe pour VMake

Date : 2026-10-14

## Demande

Couper la vidéo en parties de 5 s maximum, à nettoyer dans VMake (« remove text ») par l'utilisateur. La suite (réassemblage, textes) sera précisée à réception des parties nettoyées.

## Source

- `source/original.mp4` : TikTok trouvé via Trendtrack (id 7561187368233880863), 19,1 s, 720×1280, 30 i/s, 573 images, son d'origine.
- Contenu : femme sous la douche qui verse de l'après-shampoing dans sa main, l'applique sur un côté puis l'autre, en rajoute, le répartit au peigne, puis résultat cheveux secs longs et ondulés (dernières 1,5 s).
- Textes anglais incrustés (lus sur la planche, à vérifier) : « POV: You thought this was WAY too much conditioner... until you tried it » ; « I start with this much for the first side... » ; « I add a little more for the areas that didn't get coated on that side... » ; « Then this much for the other side... » ; « Aaaand a little bit more... » ; « That's how much I need to evenly coat my hair strands... » ; « Make that your goal... but adjust the amount for your length & density ».

## Parties à nettoyer dans VMake

Toutes coupées sur un changement de plan (détection ffmpeg, seuil 0,2), 5 s maximum, durées équilibrées (`sorties/a-nettoyer/`) :

| Partie | Images source | Durée |
|---|---|---|
| `partie-1_0-4.1s.mp4` | 0 à 123 | 4,13 s |
| `partie-2_4.1-8.2s.mp4` | 124 à 246 | 4,10 s |
| `partie-3_8.2-12.8s.mp4` | 247 à 384 | 4,60 s |
| `partie-4_12.8-16.1s.mp4` | 385 à 483 | 3,30 s |
| `partie-5_16.1-19.1s.mp4` | 484 à 572 | 2,97 s |

Rappel : VMake perd les 3 premières images de chaque partie ; au réassemblage, compléter avec 3 copies de la première image (comme `2026-10-12_claire-chhavi1351_decoupe/montage_texte.py`).

## Reproduire

```
python3 decouper.py
```
