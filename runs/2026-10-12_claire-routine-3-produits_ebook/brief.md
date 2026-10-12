# Brief : ebook « Les 3 produits qui transforment tes cheveux » (ebook full value)

- Date : 2026-10-12
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Skill : `skills/ebook-full-value` (GPT Image 2, 3:4, 1K, choisi par l'utilisatrice)
- Vidéo associée : « Les 3 produits indispensables pour transformer tes cheveux » (shampoing clarifiant, masque nourrissant, masque à l'huile), CTA « Commente CHEVEUX ».

## Cadrage validé (questions)
- Types de produits, sans aucune marque : comment choisir chaque produit (ingrédients à chercher et à fuir, texture) et comment l'utiliser. Les liens produits sont envoyés à part en message privé.
- Angle : la routine en 3 produits (rôle, choix, quantité, temps de pose, ordre, planning de la semaine selon le type de cheveux).
- Même DA que les 2 premiers ebooks (bloc DA repris), tutoiement, ton optimiste, 12 pages.

## Problème et émotion (étape 1)
Femme de 40 à 55 ans aux cheveux ternes, secs sur les longueurs, plats à la racine, salle de bain pleine de produits sans résultat. Émotion : lassitude, envie d'une routine simple qui marche.

## Deep research (étape 2)

| Point | Ce qu'on retient | Source |
|---|---|---|
| Clarifiant vs chélatant | Le clarifiant retire résidus de produits, sébum, film en surface (tensioactifs) ; le chélatant (EDTA, acide citrique) fixe les minéraux du calcaire. | [GK Hair](https://www.gkhair.com/blogs/all-blog-posts/chelating-vs-clarifying-shampoo), [Macujo](https://www.macujo.com/chelating-vs-clarifying-shampoo/) |
| Fréquence du clarifiant | En général 1 fois par semaine au maximum ; trop souvent : irritation, cheveux cassants et ternes. Cheveux colorés : toutes les 3 à 4 semaines, attendre 2 semaines après une coloration. | [Ulta](https://ulta.com/discover/beauty-education/how-often-to-use-clarifying-shampoo), [GK Hair](https://www.gkhair.com/blogs/all-blog-posts/how-to-use-clarifying-shampoo-correctly), [Oceanside](https://oceansidehairsalon.com/blog/shampoos-that-work-hard-water-hair/) |
| Cheveux blancs | Jaunissement par calcaire, pollution, résidus et chaleur ; clarifiant ou chélatant occasionnel, suivi d'un soin. | [Wella](https://www.wella.com/professional/en-DK/blog/hair-care/how-to-get-yellow-tones-out-of-grey-hair), [Quicksilver Hair](https://quicksilverhair.com/how-to-clarify-your-curly-or-straight-gray-hair/) |
| Shampoing sur le cuir chevelu | Shampoing concentré sur le cuir chevelu, la mousse rince les longueurs ; après-shampoing sur les longueurs (recommandations attribuées à l'AAD). | [Foothill Dermatology](https://foothillderm.com/blog/tips-for-healthy-hair), [HealthDay](https://www.healthday.com/health-news/skin-health/health-tip-teach-your-kids-healthy-hair-habits-732032.html) |
| Masque | Mi-longueurs et pointes, jamais les racines ; 5 à 20 minutes ; 1 à 2 fois par semaine. Ingrédients : céramides, alcools gras (base adoucissante), panthénol, glycérine. | [Wella](https://www.wella.com/professional/en-US/blog/hair-care/hair-mask-vs-conditioner), [Gisou](https://gisou.com/blogs/blog/how-to-use-a-hair-mask-the-right-way), [DermApproved](https://dermapproved.com/ingredients/fatty-alcohols/) |
| Huile de coco avant lavage | Seule huile testée (vs tournesol, minérale) qui réduit nettement la perte de protéines du cheveu en pré-lavage. Pose 30 min à 1 h (pratique courante). | Rele et Mohile, J Cosmet Sci 2003 ([Semantic Scholar](https://www.semanticscholar.org/paper/Effect-of-mineral-oil,-sunflower-oil,-and-coconut-Rele-Mohile/cc8938a99d4f541dad4530dc3499828a2ccb0456)) |
| Huile et pellicules | Huile de coco, olive, argan : déconseillées sur un cuir chevelu à pellicules (Malassezia) ; huile de coco fractionnée (MCT) et squalane jugées plus sûres (sources de marques). Dans l'ebook : huile légère type coco fractionnée sur le cuir chevelu, huile sur les longueurs seulement en cas de pellicules. | [Dermazen](https://www.dermazen.com/blogs/news/the-truth-about-oils-for-seborrheic-dermatitis-dandruff-fungal-acne-what-to-use-and-avoid), [Octaskin](https://octaskin.com/blogs/blog/mct-oil-seborrheic-dermatitis) |

Écarté : chiffres « 39 % / 17 % » de l'étude coco (non vérifiés dans le résumé), chaleur ou serviette chaude pour le masque (pas de preuve trouvée).

## Plan (étapes 3 et 4)
Angle méthode pas à pas. 12 pages : couverture · mot d'intro · pourquoi tes cheveux manquent d'éclat · ta routine en 3 gestes (ordre) · produit 1 le choisir · produit 1 l'utiliser · produit 2 masque nourrissant · produit 3 masque à l'huile · planning de la semaine selon le type de cheveux · règles d'or · mémo · à toi de jouer + message privé. Textes exacts : `contenu.md` (généré par `work/ecrire_prompts.py`).

## Génération (étape 6)
`python3 scripts/kie_image.py --model gpt-image-2-text-to-image --prompt-file prompts/pages/NN.txt --out sorties/pages/NN-v1.png --ratio 3:4 --resolution 1K`
