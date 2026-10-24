# Brief : UGC humain « tempes, réponse à un commentaire » (Claire)

- Date : 2026-10-24
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Script et voix fournis : `script-elevenlabs.txt`, `audio/voix.mp3` (ElevenLabs **Sidonie**, vitesse 1,0, stabilité 50 ; 64,91 s), alignés mot à mot (`work/mots.json`).
- Format : vidéo « réponse à un commentaire ». Le hook (« J'ai perdu beaucoup de cheveux partout sur ma tête et surtout sur mes tempes ») s'affiche dans une bulle façon TikTok, reproduite au pixel près sur `references/ref-bulle-frame.png` et `references/ref-bulle.png` : « Réponse au commentaire de <prénom> », photo de profil authentique (pas mannequin), police TikTok Sans. Fautes volontaires demandées par l'utilisateur : « Jai » (sans apostrophe) et « têtes ».
- Casting : même avatar brun (mêmes traits, âge, gabarit), même coiffure que la vidéo tempes partie 1 (queue basse), **nouveau haut**. Même décor sauge.
- Méthode : Wan 3.0 480p, voix en `@Video1` écran noir, structure d'Alexis ; b-rolls 3D dans le style des premières vidéos (fond prune, coupes de peau semi-réalistes, comme br-0013 / br-0015), plus explicites ; 2 motion design ; sous-titres 2 lignes terracotta.
- **Budget : 2,50 € maximum** (environ 580 cr). Objectif : environ 480 cr.
- Règles de l'utilisateur pour les b-rolls (2026-10-24) : chaque b-roll correspond à 100 % à la phrase dite, se comprend immédiatement sans le son, et reste agréable à regarder. La vidéo 1 (raie élargie) a bien marché (beaucoup de mails et d'interactions) : on garde sa recette.

Découpage : `decoupage.md`.

## Choix validés (2026-10-24)
- Haut : pull en maille terracotta. Voix : Sidonie (voulu). Prénom : Sylvie. Images 1K, vidéo 480p.
- Budget relevé par l'utilisateur à son solde (environ 3 €) : « micro-tensions » passe en face caméra (W3 de 6 s).

## Générations
| Fichier | Modèle | Réglages | Références | Prompt | Coût | Task id | Statut |
|---|---|---|---|---|---|---|---|
| `sorties/cadrage-v1.png` | GPT Image 2.5 Sunburst | 9:16, 1K | `casting/cadrage-tempes.png` | `prompts/image/cadrage-v1.txt` (seul le haut change : pull terracotta) | 6 cr | ba4c61ef2af0f6e8c5f5acf55790fdb4 | à valider |
| `sorties/profil-sylvie-a.png` | Z-Image | 1:1 | aucune | `prompts/image/profil-sylvie-a.txt` (déjeuner au jardin) | 0,8 cr | cc248eef97f617e17d9c3e4ee568c21a | à choisir |
| `sorties/profil-sylvie-b.png` | Z-Image | 1:1 | aucune | `prompts/image/profil-sylvie-b.txt` (selfie en voiture) | 0,8 cr | e5be13dc2a6bd46a9383e3fb81346610 | à choisir |

Bulle : `work/bulle.py` (TikTok Sans, mesures de `references/ref-bulle-frame.png` x2,011, placée plus haut à la demande de l'utilisateur : y=100 au lieu de 273, au-dessus de la tête), texte « Jai perdu beaucoup de / cheveux partout sur ma têtes / et surtout sur mes tempes ».
