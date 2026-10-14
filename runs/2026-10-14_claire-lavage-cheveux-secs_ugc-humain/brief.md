# Brief : Claire, cheveux secs après le lavage (UGC humain face caméra)

- Date : 2026-10-14
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Concept : ugc-humain (skill `skills/ugc-humain-v1`), face caméra parlé, méthode écran noir pour la synchro
- Casting : Claire. Références : `references/claire-pied.jpg` (en pied, col roulé rose, pantalon camel, bottines, fournie par l'utilisatrice ou l'utilisateur) + `Claire/avatar/avatar-face.jpg`
- Script : `script-elevenlabs.txt` (fourni, validé, balises d'émotion ElevenLabs). Voix : `audio/voix.mp3` (ElevenLabs, voix « Elise », 71,3 s)
- Produit : aucun (pas de produit à montrer, astuces seulement)
- Appel à l'action : commenter « SUITE »
- Référence : `references/video-reference.mp4` (TikTok, 86,5 s, 576x1024)
- Résolutions choisies : images 1K (GPT Image 2, 6 cr), vidéo 720p (Seedance 2.5, 38 cr/s avec la voix en vidéo de référence)

## Analyse de la vidéo de référence

- Une seule prise continue : la créatrice debout dans un couloir (porte en bois, mur clair, lumière de fenêtre), plan taille, tient un petit micro sans fil noir près de la bouche, beaucoup de gestes de la main libre (doigt levé pour « No. », mains ouvertes pour expliquer).
- Montage : titre fixe en haut (« HAIR DRY AFTER WASHING? do this instead »), sous-titres mot par mot au centre, incrustations par-dessus (b-rolls en vignette, captures d'articles surlignés, schéma « Conditioner / Shampoo / Conditioner », photo de cheveu au microscope), fond rose pâle quand le b-roll passe en grand avec la créatrice détourée en bas.
- Mécanique : accroche problème, 3 astuces annoncées par un numéro, chaque astuce = un geste + une preuve visuelle, appel à commenter.
- On garde : la prise continue face caméra, le micro tenu, les gestes, le titre fixe et les sous-titres, les incrustations par astuce. On ne reprend pas : la personne, les images, les captures d'articles.

## Points d'attention

- Le script vouvoie (« vos cheveux », « commentez ») alors que la charte de Claire tutoie. Voix déjà enregistrée : signalé, non modifié.
- Pas de chiffre ni de promesse santé dans le script. « Cheveux brillants et soyeux » reste une formulation de bénéfice, pas un résultat garanti.

## Calage de la voix (MMS, `work/mots.json`, 212 mots alignés)

| Phrase | Début | Fin |
|---|---|---|
| Si vos cheveux deviennent secs… pour éviter ça. | 0,08 | 5,42 |
| Parce que tout le monde a droit… après un lavage ! | 5,65 | 9,40 |
| Premièrement, … méthode du lavage « sandwich » … | 9,61 | 17,78 |
| En fait, cette première couche … effet asséchant du shampoing… | 18,01 | 23,78 |
| c'est exactement ce qui provoque la casse. | 24,34 | 25,98 |
| Deuxièmement, gardez votre shampoing uniquement sur le cuir chevelu. | 26,41 | 30,15 |
| Ne le laissez pas couler … entraîner la casse. | 30,59 | 36,73 |
| Troisièmement : la serviette en microfibre est indispensable ! | 37,13 | 40,63 |
| Les serviettes de bain classiques … frottements… | 40,90 | 44,23 |
| et le cheveu, lorsqu'il est mouillé, … vulnérable à la casse. | 44,61 | 48,31 |
| Frotter une serviette éponge … refléter correctement la lumière. | 48,75 | 55,63 |
| Il ne paraîtra donc pas aussi beau, brillant et doux ! | 55,95 | 58,80 |
| En plus, une serviette en microfibre sèchera … plus rapidement. | 59,11 | 62,97 |
| Et si vous ne souhaitez pas dépenser d'argent, … l'affaire ! | 63,29 | 68,33 |
| Commentez SUITE si vous voulez la suite des astuces ! | 68,72 | 71,11 |

## Image de départ

- Commande : `python3 scripts/kie_image.py --model gpt-image-2-image-to-image --ref references/claire-pied.jpg references/claire-visage.jpg references/fond-porte.jpg --prompt-file prompts/img/depart.txt --out sorties/depart/depart-vN.png --ratio 9:16 --resolution 1K`
- v1 et v2 (12 cr) : jugées trop « IA » par l'utilisatrice ou l'utilisateur (v2 préférée). v3 et v4 (12 cr) : prompt réécrit pour un rendu iPhone brut (peau réelle, cils naturels, cheveux décoiffés, bruit de capteur, pose non posée). En attente de validation.
- Extraits de voix des blocs face caméra : `audio/extraits/F1.wav` (0,00 à 9,50), `F2.wav` (17,90 à 26,20), `F3.wav` (36,93 à 44,42), `F4.wav` (63,13 à 71,31).

## Statut (2026-10-14)

Projet arrêté à la demande, avant la production des clips face caméra.
- Méthode retenue après tests : gabarit d'Alexis Aurion (voix ElevenLabs en `@Video1` écran noir déclarée « AUDIO-ONLY… master timeline », « say every word ONCE », `@Image1` créatrice sans première image imposée, `@Image2` décor et cadrage, jeu vivant, timeline ancrée sur les mots, son activé). Test F2 480p : 29/29 mots reproduits, 5/5 bilabiales fermées. Voir `journal.md` et `tests-alexis/`.
- Prêt à reprendre : `prompts/video/alexis/F1.txt` à `F4.txt`, extraits de voix `audio/extraits/F1.wav`, `F2.wav`, `F3.wav`, `F4.wav`, image `retenues/depart.png`, liste des b-rolls `brolls-a-trouver.html`. Son de montage choisi : voix ElevenLabs.
- Crédits dépensés sur ce run : environ 3 790 cr (images 24, F1 v1 760, tests A/B/C 748, F1 v2 760, F2 v1 646, test skill d'origine 567, test Alexis 289).
