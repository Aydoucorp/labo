# Couverture Facebook : page organique « Les cheveux de Claire »

- Date : 2026-10-12
- Demande : « fait moi une photo de couverture facebook pour la page organic »
- Choix de l'utilisatrice ou de l'utilisateur : marque Les cheveux de Claire ; couverture « normale », sans représentation de Claire ; texte = nom + signature posés en vraies polices ; résolution 1K, option la moins chère.
- Charte : `Claire/BRAND-DNA-CLAIRE.md` (crème #FAF6F3, terracotta #A8553A, prune #7A4351, sauge décorative ; Fraunces pour le titre, Source Sans 3 pour le texte).

## Génération
- Modèle : Nano Banana 2.1 (`nano-banana-2-1`, KIE), texte vers image, 16:9, 1K (sortie 1376x768), 4 cr par image.
- Commande : `python3 scripts/kie_image.py --model nano-banana-2-1 --prompt-file prompts/<v>.txt --out sorties/<v>-v1.png --ratio 16:9 --resolution 1K`
- 3 variantes (prompts dans `prompts/`) : a-coiffeuse (coiffeuse en chêne, flacons ambrés, peigne, serviette terracotta, eucalyptus) · b-vue-dessus (vue de dessus sur lin, brosse, peigne, romarin, huile, masque, serviette prune) · c-mur-ombres (mur plâtre avec ombres de feuillage, étagère, pot terracotta, serviette prune).
- Consigne commune : centre de l'image vide pour le texte, aucun texte, étiquette, logo, personne ni cheveux.

## Texte
- `work/composer.py fond.png sortie.png --apercu apercu.png` : recadrage 16:9, mise à l'échelle en 1640x923, « Les cheveux de Claire » en Fraunces 600 (opsz 72) 112 px terracotta, « Tes cheveux ont changé. Toi aussi. » en Source Sans 3 400 46 px encre, halo crème très doux pour la lisibilité. Polices dans `work/fonts/`.
- Format Facebook : le mobile affiche l'image 16:9 entière, l'ordinateur un bandeau central 2,63:1 (cadre rouge des aperçus `work/apercu-*.png`). Le texte est centré dans ce bandeau.

## Coût
3 x 4 cr = 12 crédits (0,06 $).
