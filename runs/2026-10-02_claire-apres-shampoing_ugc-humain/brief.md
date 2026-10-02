# Brief : Claire, les signes du mauvais après-shampoing (UGC humain)

- Date : 2026-10-02
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Concept : ugc-humain (skill `skills/ugc-humain-v1`)
- Avatar : `Claire/avatar/avatar-face.jpg` (identité autorisée par l'utilisateur)
- Offre : le guide (non physique) ; recette « service » du skill, pas d'emballage
- Appel à l'action : commenter « GUIDE »
- Référence : `references/pub-concurrente.mp4` (TikTok, 26,5 s, 720x1280)

## Analyse de la pub de référence

- Format : pas de parole. Une femme muette, une suite d'environ 9 plans courts (2 à 4 s) tournés à des moments différents (douche, séchage, brossage, tenues différentes), un texte à l'écran par signe, musique tendance.
- Accroche : texte « signs you're using the wrong conditioner… » sur un geste concret (après-shampoing versé dans la main sous la douche).
- Mécanique : liste de signes, chacun montré par un geste quotidien reconnaissable (doigts coincés au séchage, brosse qui accroche, pointes sèches, racines grasses), puis la solution (« the right conditioner… ») et un renvoi vers le profil.
- Ce qu'on garde : le rythme (un signe = un plan = une phrase), les gestes quotidiens, la tenue décontractée, la caméra posée, la lumière naturelle.
- Ce qu'on ne reprend pas : le texte, la musique, la personne, les produits montrés.

## Script de l'utilisateur et découpage proposé (un signe par plan)

| Plan | Phrase | Image |
|---|---|---|
| 01 | Voici les signes que vous utilisez le mauvais après-shampoing : | Sous la douche, elle verse l'après-shampoing (flacon sans marque) dans sa main |
| 02 | vos cheveux ont l'air secs et abîmés, | Face caméra, cheveux secs et frisottants, moue |
| 03 | et vos doigts s'accrochent dans les nœuds pendant le séchage. | Sèche-cheveux en main, les doigts restent bloqués dans une mèche |
| 04 | Il devient difficile de séparer vos mèches sous la douche même avec le produit, | Sous la douche, cheveux mouillés, elle tire sur une mèche emmêlée |
| 05 | et vous trouvez de petits nœuds persistants après le brushing. | Gros plan des doigts qui défont un petit nœud |
| 06 | Le brossage est laborieux, | La brosse reste coincée à mi-longueur |
| 07 | vos longueurs semblent sèches, raides ou cassantes, | Elle montre ses pointes à la caméra |
| 08 | et des nœuds se reforment aussitôt après le passage de la brosse. | Gros plan d'une mèche qui s'emmêle juste après la brosse |
| 09 | Vos cheveux peuvent aussi paraître lourds, plats et gras aux racines. | Racines plates, elle soulève une mèche qui retombe |
| 10 | Commente « GUIDE » pour savoir quel après-shampoing choisir. | Cheveux brossés et souples, elle regarde la caméra, sourire léger |

## Points de charte

- Pas de promesse de résultat ni d'avant/après garanti : le dernier plan montre un geste calme, pas une transformation.
- Pas de marque d'après-shampoing visible (flacon neutre).

## Modèles du skill

- Portraits : GPT Image 2 (retouche à partir de l'avatar de Claire en référence). Soul seulement pour un nouveau casting.
- Vidéo : Seedance 2.5 (KIE `bytedance/seedance-2-5`). Tarifs relevés le 2026-10-02 : 480p 28 cr/s, 720p 63 cr/s, 1080p 158 cr/s sans vidéo de référence ; 17, 38 et 95 cr/s avec une vidéo de référence.
- GPT Image 2 : 1K 6 cr, 2K 10 cr, 4K 16 cr.

## Générations

Choix de l'utilisateur (2026-10-02) : format A (plans muets, textes et musique ajoutés au montage, musique reprise de la vidéo d'origine), images 1K, vidéo 720p.

### Portraits (étape 1)

- Modèle : GPT Image 2 image vers image (`gpt-image-2-image-to-image`), 1K, 9:16, référence `Claire/avatar/avatar-face.jpg`. Script : `python3 scripts/kie_image.py --model gpt-image-2-image-to-image --prompt-file prompts/img/<plan>.txt --ref Claire/avatar/avatar-face.jpg --out sorties/portraits/<plan>-v<n>.png --ratio 9:16 --resolution 1K`
- Prompts : `prompts/img/<plan>.txt` (scène du plan + bloc d'identité et de réalisme commun).
- Incidents : plan 01 refusé une fois par le filtre de contenu (douche en brassière, 0 cr) puis refait en débardeur noir ; 03, 04, 09 relancés après une erreur d'envoi temporaire.
- Retouches : 05, 06, 08 refaits en v2 (sourire contraire au texte, expression agacée demandée).
- Retenus : 01 v1, 02 v1, 03 v1, 04 v1, 05 v2, 06 v2, 07 v1, 08 v2, 09 v1, 10 v1. Planche : `sorties/portraits/planche-portraits-v2.jpg`.
- Coût : 13 images x 6 cr = 78 cr.

### Vidéo (étape 2)

- Portraits validés par l'utilisateur (« on garde »). Musique d'origine conservée (test, pas forcément publié).
- Modèle : Seedance 2.5 (`bytedance/seedance-2-5`), 720p, 9:16, `generate_audio` désactivé, plusieurs images de référence (@Image1 à @Image4 = image de départ de chaque plan). Script : `python3 scripts/kie_seedance.py --prompt-file prompts/video/<clip>.txt --image <portraits> --out sorties/clips/<clip>-v1.mp4 --duration <s> --resolution 720p`
- Prompts : `prompts/video/A.txt` (plans 01 à 04, 13 s), `B.txt` (05 à 08, 11 s), `C.txt` (09 et 10, 7 s), sur le gabarit du skill (références, caméra, jeu muet, timeline, continuité, audio, contraintes).
- Coupes mesurées (scdet) : A 2,63 / 5,33 / 9,17 s ; B 2,96 / 4,79 / 7,04 s ; C 3,67 s. Les 10 plans sont conformes à la timeline.
- Coût : 819 + 693 + 441 = 1 953 cr (63 cr/s).

## Montage

Voir `montage.md`. Créa finale : `creas/ugc-humain/2026-10-02_ugc-humain_001.mp4`. Coût total du run : 2 031 cr (environ 10,16 $).
