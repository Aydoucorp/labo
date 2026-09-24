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
