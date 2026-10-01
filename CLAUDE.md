# Studio de production

Studio de création de contenus visuels e-commerce (photos produit, statiques publicitaires, vidéos courtes).

## Arborescence

| Dossier | Rôle | Règle |
|---|---|---|
| `refs/produits/<produit>/` | Photos produit d'origine | Lecture seule. Jamais modifiées ni écrasées. |
| `refs/style/` | Moodboards, créas inspirantes, exemples de ton | Lecture seule. |
| `refs/marque/` | Logo, palette, typos, charte | Lecture seule. |
| `scripts/` | Scripts réutilisables (redimensionnement, renommage, export…) | Un script = une tâche, commenté en tête. |
| `skills/` | Skills maison du studio (un sous-dossier par skill avec son `SKILL.md`) | `.claude/skills` pointe vers ce dossier : chaque skill ajouté ici est chargé automatiquement. |
| `runs/` | Toutes les sorties générées | Voir convention ci-dessous. |
| `Claire/` | Marque « Les cheveux de Claire » : `BRAND-DNA-CLAIRE.md` | Référence de marque, à lire avant toute création pour Claire. |
| `creas/<concept>/` | Créas finales validées, rangées par concept | Nommage obligatoire, voir « Créas finales ». |
| `bibliotheque/` | Index de tous les b-rolls déjà filmés, trouvés ou générés (`brolls.json`, `brolls.md`) | À consulter avant toute recherche ou génération ; mis à jour après chaque montage. |

## Convention des runs

Chaque session de production crée son propre dossier :

```
runs/AAAA-MM-JJ_<produit>_<objet>/
├── brief.md      (demande, références utilisées, modèle/outil, prompts)
├── sorties/      (toutes les générations)
└── retenues/     (uniquement les versions validées)
```

Exemple : `runs/2026-09-24_serviette-microfibre_statiques-meta/`

## Règles de travail

- Toujours partir des photos de `refs/produits/<produit>/` : le produit doit rester fidèle (forme, couleur, logo, texte).
- Ne rien écrire en dehors de `runs/` pendant une production, sauf demande explicite.
- Noter dans `brief.md` chaque prompt et chaque réglage utilisé, pour pouvoir reproduire une image validée.
- Nommage : minuscules, tirets, sans accents ni espaces (`statique-angle-douleur-v2.png`).
- Si un produit n'a pas encore de dossier dans `refs/produits/`, le signaler avant de générer quoi que ce soit.
- **Résolution demandée avant toute génération (règle de l'utilisateur)** : avant de lancer des images ou des vidéos, demander à l'utilisateur la résolution voulue pour chaque type de média (ex. images 1K / 2K / 4K ; vidéos 720p / 1080p / 2K), en indiquant pour chaque option le modèle et le coût en crédits. Ne jamais choisir la résolution à sa place.
- **Bibliothèque des b-rolls (règle de l'utilisateur)** : avant de chercher, filmer ou générer un plan, consulter `bibliotheque/` (`python3 scripts/biblio_brolls.py chercher "mots-clés"`) et réutiliser ce qui existe déjà (même un plan d'un autre concept, s'il colle au propos). Après chaque montage, enregistrer tous les rushes et plans générés retenus (`ajouter-brief` pour un full b-roll, `ajouter --json` sinon) avec ce qu'ils montrent et la phrase sur laquelle ils ont servi. But : ne jamais payer deux fois le même plan.
- **Validation à chaque étape (règle de l'utilisateur)** : toujours montrer à l'utilisateur les images et les vidéos des plans (SendUserFile), et attendre sa validation explicite avant l'animation, le montage ou toute étape suivante. Ne jamais enchaîner deux étapes payantes sans ce feu vert.

## Créas finales

- Chaque créa finale validée est copiée dans `creas/<concept>/` (dossiers : papercut, claymotion, disney, jouet, talking-object, tableau-blanc, low-poly-cinema, humain-penseur, clip-musical, zack-d-style, le-montage, talking-head, full-b-roll-artiste). Un nouveau concept = un nouveau dossier, ici et dans Drive.
- Nom : `AAAA-MM-JJ_<concept>_<NNN>.<ext>` : date de création, concept, numéro de la vidéo sur ce concept sur 3 chiffres (001, 002…), jamais remis à zéro.
- Avant de nommer, lire `creas/registre.md`, prendre le dernier numéro du concept + 1, puis mettre à jour le registre (compteur + ligne d'historique).
- Le fichier original reste dans `runs/.../retenues/`.

## Sauvegardes : GitHub + Google Drive

**GitHub = copie complète du studio.** Après chaque étape (fichier créé ou modifié), commit puis `git push origin claude/trusting-carson-sott4i` sur le dépôt `Aydoucorp/labo`, et vérifier que la branche distante est à jour. Tout y va, sauf `.env`.

**Drive « Studio marketing » = ce que l'utilisateur consulte**, au même emplacement que dans le studio. À recopier dans Drive à chaque création ou modification :
- `CLAUDE.md`, le brand DNA des marques (`Claire/`), le `SKILL.md` de chaque skill ;
- dans chaque run : `brief.md`, `storyboard.md` (ou `decoupage.md`), `montage.md`, `journal.md`, les README de références et le script ;
- `creas/registre.md` et les créas finales (envoyées à l'utilisateur, qui les dépose) ;
- `bibliotheque/brolls.md` (tableau des b-rolls réutilisables).

Ne vont pas dans Drive (ils sont sur GitHub) : code et scripts, références techniques des skills, polices, fichiers de prompts, JSON, images et clips intermédiaires.

| Dossier | ID Drive |
|---|---|
| Studio marketing (racine) | `1oA5bUUlm8jX3Yuj1haPIEaGymAJSODzC` |
| refs | `1aAjKqKjxfOsK2E_91cMjCrWVo2EZNGjK` |
| refs/produits | `1Gh98KDVBdNxFjjX7OLDXcLQVYE15FQZ3` |
| refs/style | `19uBQR1nemTx0qWW7qCNCYTTreosVjlqN` |
| refs/marque | `1VgfIea-8y0MTv0xBMApP8QP_6-42Y65_` |
| scripts | `1g33xgzU2HsDBzlU47Iw9YZDm9ylUi1YP` |
| skills | `1B0i2m_FUVSzmMd_jj42V5YXs8lV8DvUA` |
| runs | `1C65QZGUKzNdwrqqUnPiX7Fg_d9Cp06oX` |
| Claire | `1dgKN8HMiOInBg1c6G_8EEOWkE8SC3s_t` |
| skills/papercut-publicite | `1aZeuW6cB0qx5x0ZQh5qO7FX80csTlcwv` |
| skills/papercut-publicite/references | `1rl6kcwfGlurVifkRQebccGxoaR-E5oIe` |
| runs/2026-09-25_claire-guide-racine_papercut | `1BcImeaga5IbPWTA3dOh3zlcXo1xQL2zM` |
| runs/2026-09-25_claire-guide-racine_papercut/audio | `1C4oheQkcPRid15q2HMB2ZQHSxG3OPmqw` |
| runs/2026-09-25_claire-guide-racine_papercut/sorties | `1LbCHUp_VfnQEwjwyPjw5mYEjG1yB7BfX` |
| runs/2026-09-25_claire-guide-racine_papercut/retenues | `1OZqhHXZ1HOT_gBDw4bC8fBCzWy_al8dx` |
| runs/2026-09-25_claire-guide-racine_papercut/references | `1FAb_B7namPsKKEnV-bnA37CmaiPLOHqI` |
| creas | `1FDZFVjSxYWmDJMos5vFhK_lw85pCLDQ2` |
| creas/papercut | `1FX_RJJ56CpfhzfMHh793ggFzjq12coZj` |
| creas/claymotion | `1GmE1ApFKMVsoPD2wkdeWALJeZ8AfjcxM` |
| creas/disney | `11zuVh06YPqPP7xR2sK98ZNDGybNuX-BK` |
| creas/jouet | `1t9yg8KhxRhCdpTYe0tE_ATEyGy2cl6DQ` |
| creas/talking-object | `1d_9ZyhOp7O9QMGSa5HGU8M1hg3LGabQz` |
| creas/tableau-blanc | `1DknXPFE3ZG9sZR4qhc3VnBqqEZyoFu0Y` |
| creas/low-poly-cinema | `1Lp8v7xeoxhpPrh_WeAI_Te85b7x4KbTQ` |
| creas/humain-penseur | `1kNZTjsOlNG3ysuVcbPLpMrg1sDe7YQvn` |
| creas/clip-musical | `1LHfMg73-9MhkaUKDJdzkCuLZ566jqOio` |
| creas/zack-d-style | `1TnJFpWcv_IdeGIcCWj2Jz0y7l51-MJOn` |
| creas/le-montage | `17CXCyn0gLuCL6xgstBEB2Tp41AboHRKq` |
| creas/talking-head | `1Pnvncr5Bn2-VoHNCD0Rx1XweyrNmeliV` |
| skills/talking-head | `1tHAfP_iUIfeNt9zCMIeVxjM8AzaqrI-y` |
| runs/2026-09-28_claire-cheveux-gris-carences_talking-head | `1Yly3bxgWu1-MnSl3U91BSr4huvDPViH5` |
| skills/creation-full-b-roll-artiste | `1JDzZC2iEsrpcUFxdz-P_o1y4FiP5ljJn` |
| creas/full-b-roll-artiste | `1Jjvqlp6Wz4io83GjIogc5vkguzqa4GWR` |
| runs/2026-09-30_claire-remedes-naturels_papercut | `1BYa4jh4-BnoQ5QiaDuDNR3Wk4J55aDm5` |
| runs/2026-10-01_claire-minoxidil-arret_full-broll | `1U2Gcs3ki17bgGs9h4bUAS9HpKhXKCmJI` |
| runs/2026-10-01_claire-minoxidil-arret_full-broll/rushes | `1NSXnTa6orE1cKmaiKNLzlbkMXwdS-LUI` |
| bibliotheque | `1yxN95-FEXf-TRK352fpooRQy2H17Ppdc` |

- Envoyer les fichiers sans conversion en format Google (`.md`, images et scripts restent tels quels).
- Quand un nouveau sous-dossier est créé dans Drive, ajouter son ID à ce tableau.
- Pour modifier un fichier déjà présent dans Drive : téléverser la nouvelle version dans le même dossier, puis mettre l'ancienne à la corbeille (l'outil Drive ne remplace pas le contenu).
- Les photos produit déposées par l'utilisateur dans Drive (`refs/produits/<produit>/`) sont la source : les rapatrier ici avant de travailler.
- Les images, l'audio et la vidéo ne passent pas par l'outil Drive (trop lourds) : les envoyer à l'utilisateur avec SendUserFile et le lui signaler, pour qu'il les dépose lui-même dans Drive.

## Clés API et secrets

- Les clés sont dans `.env` à la racine (ex. `KIE_API_KEY`). Ce fichier est ignoré par git.
- **Ne jamais afficher une clé en clair** : ni dans une réponse, ni dans un log, ni dans un `brief.md`. Masquer toute sortie de commande qui pourrait la contenir.
- **Ne jamais copier `.env` dans Drive**, ni la clé dans un autre fichier du studio.
- Charger les clés avec `set -a; . ./.env; set +a` puis utiliser `$KIE_API_KEY`.
- Vérifier le solde KIE : `GET https://api.kie.ai/api/v1/chat/credit` avec l'en-tête `Authorization: Bearer $KIE_API_KEY`.
