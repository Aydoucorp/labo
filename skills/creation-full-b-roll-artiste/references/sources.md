# Sources de B-roll : banques, requêtes, animation scientifique, génération IA

Les liens de recherche pré-remplis sont générés automatiquement dans `brief.html` (Pexels, Pixabay, Mixkit, Coverr, Storyblocks, Artgrid, Envato Elements). Cette page sert à choisir la bonne source et à formuler les requêtes.

## 1. Banques gratuites (usage commercial sans attribution)

| Banque | Licence | Points forts | Limites |
|---|---|---|---|
| Pexels (videos) | licence Pexels, commercial, sans attribution | 120 000+ vidéos, filtre orientation portrait, accepte le français, API gratuite (200 requêtes/h) | beaucoup de plans « lifestyle » génériques |
| Pixabay (videos) | licence Pixabay, commercial, sans attribution | 70 000+ vidéos HD et 4K, API gratuite (100/min), URLs temporaires (télécharger tout de suite) | peu de vertical natif |
| Mixkit (Envato) | Mixkit Free License, commercial | bien catégorisé, qualité régulière, pas de compte | catalogue plus petit, pas d'API |
| Coverr | licence Coverr, commercial | clips cinéma, contenu IA marqué | catalogue restreint, 4K en payant |

À éviter pour un usage commercial sans lecture attentive : Vecteezy (attribution en gratuit), Wikimedia (CC BY), Unsplash vidéo, Internet Archive.

## 2. Banques payantes

| Banque | Modèle | Pour quoi |
|---|---|---|
| Artgrid | abonnement, illimité | rushes cinéma (RAW/LOG, 4K à 8K), filtres fins (mouvement de caméra, lumière), séries cohérentes d'un même tournage : idéal pour la continuité |
| Storyblocks | abonnement, illimité | 3 M+ vidéos 100 % humaines, vertical, fonds verts, plugin Adobe |
| Envato Elements | abonnement, illimité | 10 M+ clips, aussi motion graphics et templates |
| Motion Array | abonnement | templates et sfx en plus des clips |
| Pond5 | à l'unité ou abonnement | 48 M+ clips, recherche par image similaire |
| iStock / Shutterstock / Adobe Stock | abonnement ou crédits | les plus grands catalogues d'animations médicales et 3D (« medical animation », « molecular structure 3D », « skin layers ») |

Règle de choix : gratuit pour les ambiances neutres (lieux, textures, gestes universels), payant quand il faut une série cohérente ou une animation 3D, et jamais de stock pour le produit lui-même.

## 3. Formuler une requête

Structure : sujet + action précise + cadrage + lumière + technique, un seul sujet, 8 à 14 mots, en anglais. Exemple : « close up of hands wringing a microfiber cloth over a bucket, warm window light, shallow depth of field ». Ajoute le suffixe de style du lookbook à toutes les requêtes du projet pour obtenir des résultats homogènes.

Mots utiles par famille : cadrage (close up, macro, top down, over the shoulder, low angle, wide shot), mouvement (static, slow pan, handheld, tracking shot, orbit), lumière (natural window light, golden hour, soft daylight, studio light, backlit), technique (shallow depth of field, slow motion, 120 fps, 4K, vertical, portrait orientation), matière (texture, fabric, water, foam, glossy, matte).

Tri d'un résultat : vérifie `must_show` (les éléments obligatoires), l'orientation ou la possibilité de recadrer en 9:16 sans perdre le sujet, la durée (au moins `min_rush_s`), la lumière compatible avec le lookbook, et l'absence de texte ou de logo tiers dans l'image.

## 4. Animation 3D scientifique

Trois voies, par ordre de coût :

1. Banques (iStock, Shutterstock, Adobe Stock, Storyblocks) avec les requêtes « 3d medical animation skin layers », « microscopic fibers 3d animation », « molecule dissolving water 3d », « cellular absorption animation ». Résultat souvent horizontal : prévoir un recadrage sur la zone utile ou un fond flou.
2. Génération IA image → vidéo à partir du prompt fourni dans le brief (`ai_prompt.image` puis `ai_prompt.motion`). Écris l'image d'abord (composition, échelle, palette), puis anime-la (orbit lent, particules qui bougent, pas de morphing). Les modèles vidéo actuels tiennent 3 à 5 s de mouvement cohérent : ne demande pas plus par plan.
3. Commande à un animateur (VOKA, 3DforScience, Fusion Animation et équivalents) pour un mécanisme récurrent réutilisé dans toutes les vidéos de la marque : c'est un investissement rentable dès que le même mécanisme revient dans cinq créas.

## 5. Génération IA (IAGEN) : règles communes, quel que soit le fournisseur

- Toujours deux temps : une image fixe validée, puis la vidéo à partir de cette image. On ne relance pas la vidéo tant que l'image n'est pas exactement le plan voulu.
- Format vertical 9:16 dès l'image, pour éviter un recadrage qui coupe le sujet.
- Pas de texte ni de logo générés dans l'image (le skill ajoute les textes) ; pas de visage identifiable reconnaissable comme une vraie personne ; pas de produit concurrent.
- Un plan IA ne remplace jamais un plan PRODUIT : le vrai produit se filme.
- Nommer la sortie avec l'ID du plan (`07_MECA_IAGEN_fibres.mp4`) pour qu'elle tombe directement dans `rushes/`.

Les instructions propres à chaque fournisseur (endpoints, modèles, paramètres) vivent hors du skill, dans le dossier de l'utilisateur dédié à ce fournisseur.

## 6. Contenu propre (UGC, PRODUIT, SCREEN, SOCIAL)

Tourner au smartphone, à la lumière du jour, en 9:16, en 4K si possible, 10 s par prise (le montage n'en gardera que 2), les 3 valeurs par sujet (large, moyen, détail), sans zoom numérique (avancer physiquement ou faire un lent pas de côté). Garder le son d'ambiance. Pour les captures d'écran, enregistrer l'écran en vidéo (scroll lent) plutôt qu'une image fixe. Le brief génère la checklist par lieu.

## 7. Registre des sources

Pour chaque rush utilisé, note dans `rushes/SOURCES.md` : ID du plan, banque ou origine, URL ou identifiant, licence, date. Ça prend dix secondes par rush et ça évite toute question de droits sur une publicité qui tourne.
