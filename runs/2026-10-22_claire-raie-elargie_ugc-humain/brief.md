# Brief : UGC humain « raie élargie » (Claire)

- Date : 2026-10-22
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Script : fourni par l'utilisateur (`script-elevenlabs.txt`), voix ElevenLabs « sidonie » (`audio/voix.mp3`, 43,73 s)
- Référence : TikTok anglophone (`references/video-reference.mp4`, 36,5 s) et son analyse (`references/analyse-reference.md`)
- Décor : `references/decor.jpg` (soubassement bleu-gris, rideau de lin beige, plante)
- Casting : nouvel avatar brun (`casting/`, issu du test « avatar sans blond » du 2026-10-21 ; `de-face.png` = référence visage)
- Pas de photo produit : aucun plan produit.
- Méthode : Wan 3.0 (`wan/3-0-video`) + structure de prompt d'Alexis, voix en `@Video1` écran noir, 480p, 9:16.
- Images : GPT Image 2.5 Sunburst 1K pour l'image de cadrage. Incrustations recréées avec le modèle le moins cher, insérées au montage.

Découpage : voir `decoupage.md`.

## Choix validés (2026-10-22)
- Tenue : marinière rouge et blanc, montre connectée blanche au poignet gauche, élastique noir au poignet droit (comme la référence).
- 7 clips Wan 3.0 de 3 à 8 s (voir `decoupage.md`), environ 710 cr en 480p.
- Son au montage : voix ElevenLabs d'origine, son Wan coupé.
- Inserts : Z-Image d'abord ; si l'image est ratée, Nano Banana 2.1 avec l'insert découpé de la référence en entrée (`work/inserts/`).
- Relances : aucune relance payante sans l'accord de l'utilisateur (consulter d'abord).

## Générations

| Fichier | Modèle | Réglages | Références | Prompt | Coût | Task id | Statut |
|---|---|---|---|---|---|---|---|
| `sorties/cadrage-v1.png` | GPT Image 2.5 Sunburst (`gpt-image-2-5-sunburst-image-to-image`) | 9:16, 1K | `casting/de-face.png`, `references/decor.jpg` | `prompts/image/cadrage-v1.txt` | 6 cr | a2472c3b7cf6bfd099037e3b8e91cebe | à valider |
| `sorties/cadrage-v2.png` | GPT Image 2.5 Sunburst | 9:16, 1K | idem + `work/cadrage-ref.png` (cadrage de la référence à 4,5 s, composition seule) | `prompts/image/cadrage-v2.txt` | 6 cr | 7b93fa33fbb3446f216e3bbc4eb10224 | à valider |
| `sorties/insert-raies-zimage-v1.png` | Z-Image (`z-image`, texte seul) | 16:9 | aucune (Z-Image n'accepte pas d'image) | `prompts/image/insert-raies-zimage.txt` | 0,8 cr | 0616d2b74bc51f60b84b3f3b7cc63cfd | raté : les deux raies se ressemblent |
| `sorties/insert-follicule-zimage-v1.png` | Z-Image | 4:3 | aucune | `prompts/image/insert-follicule-zimage.txt` | 0,8 cr | d1e653c0054a976b05455ca5311ebd29 | raté : pas de rétrécissement visible |
| `sorties/insert-raies-nb-v1.png` | Nano Banana 2.1 (`nano-banana-2-1`) | 16:9, 1K | `work/inserts/insert-raies-ref-x2.png` | `prompts/image/insert-raies-nb.txt` | 4 cr | d29004f2c2c5dc6e88e7c5b75b3ef34c | à valider |
| `sorties/insert-follicule-nb-v1.png` | Nano Banana 2.1 | 4:3, 1K | `work/inserts/insert-follicule-ref-x3.png` | `prompts/image/insert-follicule-nb.txt` | 4 cr | 20a37bba51eb07ad023efc20fa2c34bc | à valider |

Total images : 21,6 cr.
