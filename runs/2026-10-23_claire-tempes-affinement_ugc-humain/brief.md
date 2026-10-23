# Brief : UGC humain « tempes qui s'affinent » (Claire)

- Date : 2026-10-23
- **Partie 1 sur 2** : l'utilisateur a coupé la vidéo de référence en deux vidéos distinctes ; ce run fait la première (script et voix fournis). La partie 2 suivra dans un run séparé, avec son propre script et sa voix.
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Script : fourni par l'utilisateur (`script-elevenlabs.txt`), voix ElevenLabs **Victoria** (`audio/voix.mp3`, 64,99 s)
- Référence : TikTok anglophone (`references/video-reference.mp4`, 99,7 s) : créatrice brune aux cheveux longs ondulés, sweat bleu clair, boiseries vert sauge, grande fougère à droite ; accroche « Are your temples thinning? » main sur la tempe ; à 0:14 incrustation de deux photos avant / après de ses cheveux ; gestes vers les tempes vers 0:42 à 0:46 ; sous-titres mot à mot.
- Casting : même avatar brun que `runs/2026-10-22_claire-raie-elargie_ugc-humain` (visage, traits, âge, gabarit) ; **nouvelle coupe et nouvelle tenue** (règle de l'utilisateur).
- Méthode : comme la vidéo « raie élargie » : Wan 3.0 + structure d'Alexis, voix en `@Video1` écran noir, format hybride avec b-rolls (bibliothèque, puis b-rolls générés par l'utilisateur à partir de l'avatar), sous-titres 2 lignes terracotta, montage sur la voix d'origine.
- Pas de photo produit.

Découpage provisoire : `decoupage.md`.

## Choix validés (2026-10-23)
- Phrase avant / après (8,15 à 14,70 s) gardée telle quelle ; l'utilisateur fournit de vraies photos avant / après à incruster (comme la référence à 0:14). Rappel fait : la Brand DNA interdit l'avant-après qui laisse croire à une garantie ; décision de l'utilisateur.
- Look : cheveux attachés (queue basse), même longueur que l'avatar d'origine ; pull en maille avoine.
- Décor : celui de la référence (boiseries vert sauge, grande plante à droite, fauteuil blanc), recréé à partir de `work/decor-ref-30.png` (image de la référence, sous-titres floutés).
- Images GPT Image 2.5 Sunburst 1K ; vidéo Wan 3.0 480p. Avec la phrase avant / après, 8 clips Wan : environ 700 cr.

## Générations

| Fichier | Modèle | Réglages | Références | Prompt | Coût | Task id | Statut |
|---|---|---|---|---|---|---|---|
| `sorties/cadrage-v1.png` | GPT Image 2.5 Sunburst | 9:16, 1K | `casting/cadrage-video-raie.png`, `casting/de-face.png`, `work/decor-ref-30.png` | `prompts/image/cadrage-v1.txt` (queue basse ramenée sur l'épaule) | 6 cr | 21af857349097971fbd78e5ab190530d | non retenue |
| `sorties/cadrage-v2.png` | GPT Image 2.5 Sunburst | 9:16, 1K | idem | `prompts/image/cadrage-v2.txt` (queue dans le dos demandée, rendue sur l'épaule) | 6 cr | 2bd683770ae8356b07d73fe57b5cb61f | **retenue** (choix de l'utilisateur) |
| `sorties/avant-v1.png` | GPT Image 2.5 Sunburst | 3:4, 1K | `retenues/cadrage-v2.png`, `references/ref-avant.png` (style seulement) | `prompts/image/avant.txt` | 6 cr | 716c67634a8d16da69011372cd121314 | refusée : elle paraît plus âgée qu'après |
| `sorties/avant-v2.png` | GPT Image 2.5 Sunburst | 3:4, 1K | `retenues/cadrage-v2.png`, `casting/de-face.png`, `references/ref-avant.png` | `prompts/image/avant-v2.txt` (verrou d'âge : même âge ou plus jeune, pas de rides ajoutées) | 6 cr | 3294c7f472c65fc7b47787e604be79ca | à valider |
| `sorties/apres-v1.png` | GPT Image 2.5 Sunburst | 3:4, 1K | `retenues/cadrage-v2.png`, `references/ref-apres.png` (style seulement) | `prompts/image/apres.txt` | 6 cr | 8512f92cc24765d339aeef2c2a0c456a | à valider |

Avant / après générés par IA à la demande de l'utilisateur, qui l'indique dans la description de la publication (mention à l'écran conseillée).
