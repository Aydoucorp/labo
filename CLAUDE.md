# Studio de production

Studio de création de contenus visuels e-commerce (photos produit, statiques publicitaires, vidéos courtes).

## Arborescence

| Dossier | Rôle | Règle |
|---|---|---|
| `refs/produits/<produit>/` | Photos produit d'origine | Lecture seule. Jamais modifiées ni écrasées. |
| `refs/style/` | Moodboards, créas inspirantes, exemples de ton | Lecture seule. |
| `refs/marque/` | Logo, palette, typos, charte | Lecture seule. |
| `scripts/` | Scripts réutilisables (redimensionnement, renommage, export…) | Un script = une tâche, commenté en tête. |
| `skills/` | Skills maison du studio (un sous-dossier par skill avec son `SKILL.md`) | |
| `runs/` | Toutes les sorties générées | Voir convention ci-dessous. |

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

## Miroir Google Drive (obligatoire)

Le dossier Drive « Studio marketing » est la copie de sauvegarde du studio.
**Toute création ou modification de fichier ici doit être reproduite immédiatement dans Drive, au même emplacement.**

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

- Envoyer les fichiers sans conversion en format Google (`.md`, images et scripts restent tels quels).
- Quand un nouveau sous-dossier est créé dans Drive, ajouter son ID à ce tableau.
- Pour modifier un fichier déjà présent dans Drive : téléverser la nouvelle version dans le même dossier, puis mettre l'ancienne à la corbeille (l'outil Drive ne remplace pas le contenu).
- Les photos produit déposées par l'utilisateur dans Drive (`refs/produits/<produit>/`) sont la source : les rapatrier ici avant de travailler.

## Clés API et secrets

- Les clés sont dans `.env` à la racine (ex. `KIE_API_KEY`). Ce fichier est ignoré par git.
- **Ne jamais afficher une clé en clair** : ni dans une réponse, ni dans un log, ni dans un `brief.md`. Masquer toute sortie de commande qui pourrait la contenir.
- **Ne jamais copier `.env` dans Drive**, ni la clé dans un autre fichier du studio.
- Charger les clés avec `set -a; . ./.env; set +a` puis utiliser `$KIE_API_KEY`.
- Vérifier le solde KIE : `GET https://api.kie.ai/api/v1/chat/credit` avec l'en-tête `Authorization: Bearer $KIE_API_KEY`.
