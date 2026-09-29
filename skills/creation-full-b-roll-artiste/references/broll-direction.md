# Direction artistique du B-roll : choisir le bon plan pour chaque beat

Le B-roll porte le contexte, la voix porte l'information. Si le spectateur ferme les yeux il doit encore comprendre ; s'il coupe le son il doit encore deviner de quoi on parle. Chaque plan est donc choisi pour confirmer ce que la voix dit au moment où elle le dit, pas pour « faire joli ».

## 1. Hiérarchie de matching (dans cet ordre, on s'arrête au premier niveau qui marche)

1. **Littéral concret**. La voix nomme un objet, un geste, un lieu → on montre exactement ça, à la valeur de plan que l'énergie demande. « ta serpillière » → la serpillière, en main, en mouvement. C'est le niveau à viser pour au moins la moitié des plans.
2. **Conséquence visible**. La voix décrit un état ou un résultat → on montre la preuve : la trace sur le sol, la peau qui brille, le sol qui reflète la fenêtre. Un avant/après vaut deux plans.
3. **Mécanisme invisible**. La voix explique un fonctionnement qu'on ne peut pas filmer → animation 3D scientifique (3DSCI) ou motion graphics (MOTION) : fibres qui capturent la graisse, molécule qui se dissout, couches de la peau. Toujours ancré dans une image réelle juste avant ou juste après (on « rentre » dans la matière au montage, voir `montage-rules.md`).
4. **Métaphore contrôlée**. Mot abstrait (temps, confiance, argent, liberté) → une métaphore tirée de l'univers du produit, jamais de la liste noire. « 20 minutes perdues » → l'horloge du four de la cuisine, pas un sablier ; « pour moins de 12 euros » → la boîte posée à côté d'un café, pas des billets.
5. **Réaction humaine**. Émotion → un visage ou un geste style UGC (le soupir devant le sol, le sourire devant le résultat), filmé de près, lumière naturelle.

Quand aucun niveau ne donne un plan honnête, garde le plan précédent une demi-seconde de plus (variation de valeur) plutôt que d'insérer un plan hors sujet. Un plan hors sujet coûte plus de crédibilité qu'un plan un peu long.

## 2. Liste noire (B-roll catalogue)

Interdits sauf demande explicite de l'utilisateur : sablier ou horloge en slow motion pour « le temps », poignée de main pour « la confiance », courbe qui monte sur écran pour « la croissance », personne qui rit devant une salade, billets qui tombent, planète Terre vue de l'espace pour « écologique », goutte d'eau en macro générique sans lien avec le produit, foule floue en accéléré, cadenas pour « sécurité », ampoule pour « idée », coucher de soleil pour « bien-être ». Ces images disent « stock » avant de dire quoi que ce soit d'autre.

## 3. Types de B-roll et où les trouver

| Code | Type | Quand | Où (détails dans `sources.md`) |
|---|---|---|---|
| STOCK | vidéo réelle de banque | ambiance neutre, lieux, gestes universels | Pexels, Pixabay, Mixkit, Coverr (gratuit) ; Artgrid, Storyblocks, Envato, Motion Array (payant) |
| UGC | à filmer soi-même au smartphone | tout ce qui touche au produit, au geste réel, au résultat | checklist de tournage générée par le brief |
| PRODUIT | packshot, in-use, macro texture | PROD, CTA, CHUTE | à filmer ou déjà en stock chez l'utilisateur |
| 3DSCI | animation scientifique ou anatomique | MECA, parfois PREUVE | banques (recherche « medical animation », « molecular ») ou génération IA à partir du prompt fourni |
| MOTION | texte animé, chiffre, schéma | chiffres, promesses chiffrées, listes courtes | généré par le skill lui-même, rien à chercher |
| SCREEN | capture d'écran : avis, commentaire, message, page produit | PREUVE, CTA | fourni par l'utilisateur |
| SOCIAL | extrait du contenu organique de l'utilisateur | PREUVE, CHUTE | fourni par l'utilisateur |
| IAGEN | image puis vidéo générées par IA | quand le plan est introuvable et qu'il ne peut pas être filmé | prompt image + prompt motion fournis dans le brief |

Part minimale de plans UGC + PRODUIT dans le corps : `product_share_min` du profil (40 % en ADS, 25 % en EDU). Un plan imparfait mais vrai bat un plan parfait mais hors sujet : dès que le texte parle du produit ou du geste réel, le type est UGC ou PRODUIT, pas STOCK.

Chaque plan a un `fallback` d'un autre type : STOCK pour un UGC générique, IAGEN pour un 3DSCI introuvable, et pour un plan PRODUIT (où ni STOCK ni IA ne conviennent) une autre présentation du vrai produit : packshot fixe ou image (animée en Ken Burns par le montage), SCREEN (page produit enregistrée) ou SOCIAL (extrait déjà publié).

Carte MOTION : le skill génère lui-même un fond (dégradé sombre uni) et pose le texte dessus. Si tu veux que le chiffre s'affiche sur le plan réel précédent, ne crée pas de plan MOTION : garde le plan réel et renseigne `overlay_text` dessus.

## 4. Look book : une seule série d'images

Avant d'écrire les plans, fixe le `lookbook` du projet en 5 lignes (lumière, palette, décor, personnes, suffixe de style en anglais) et injecte le suffixe dans chaque `query_en` et chaque prompt IA. C'est ce qui fait que des rushes venus de Pexels, d'un smartphone et d'un générateur IA ressemblent à une même vidéo. Choisis les mêmes mains ou le même modèle pour tous les UGC, un décor récurrent, une heure de la journée.

Pour la continuité, la colorimétrie est normalisée au montage, mais rien ne rattrape une lumière de studio froide entre deux plans de cuisine au soleil : filtre au moment du choix.

## 5. Règles de composition de la liste

- Jamais deux valeurs de plan identiques d'affilée, jamais deux mouvements de caméra identiques d'affilée (le validateur bloque).
- Alterne les types quand c'est possible : réel → 3D → réel est une relance en soi.
- Une relance visuelle (changement de plan, texte, punch) au moins toutes les 5 s en ADS, 8 s en EDU.
- Le HOOK montre le résultat ou la contradiction, pas le problème seul : si le texte dit « tu frottes encore ? », le premier plan est le sol impeccable ou le geste absurde, et le deuxième la serpillière.
- La promesse est validée visuellement avant 10 s quand le texte le permet (un plan PREUVE ou PRODUIT, ou un indice du résultat dans un plan littéral : la zone déjà propre qui brille au fond du plan des traces). Si le script ne nomme le produit qu'après 10 s, ne triche pas avec un plan hors texte : note-le dans `script_diagnostic` et garde des plans littéraux.
- Le CTA montre le geste (pouce sur l'écran, boîte qui arrive, main qui prend le produit), pas un écran vide.
- La CHUTE reprend le cadrage du HOOK avec le résultat inversé (boucle fermée).
- Pas de réemploi d'un même rush à moins de `reuse_min_gap_s` ; un même sujet peut revenir sous une autre valeur.
- En 9:16, les sujets doivent tenir dans un cadre vertical : privilégie les plans rapprochés et les vues de dessus, évite les plans larges horizontaux qui seront recadrés.

## 6. Écrire une requête de recherche (`query_en`, `query_fr`)

Structure : **sujet + action précise + cadrage + lumière + technique**, un seul sujet par plan, 8 à 14 mots, en anglais pour les banques (les catalogues sont indexés en anglais), en français pour l'utilisateur et pour Pixabay/Pexels qui acceptent le français.

- Bon : « close up of hands wringing a microfiber cloth over a bucket, warm window light, shallow depth of field »
- Mauvais : « cleaning kitchen woman happy floor products » (collage de mots, aucun plan ne contient tout ça)

Précise le mouvement de caméra dans la requête seulement si la banque le supporte (Artgrid, Storyblocks) ; sinon laisse le champ `camera` guider le tri manuel. Termine par le suffixe de style du lookbook. Fournis aussi, dans `must_show`, les 1 à 3 éléments sans lesquels le plan est refusé (« serpillière », « sol carrelé ») : c'est le critère de tri de l'utilisateur quand il hésite entre deux résultats.

## 7. Écrire un prompt IA (`ai_prompt.image`, `ai_prompt.motion`)

Toujours fourni, même pour un plan STOCK ou UGC : c'est le repli quand rien n'est trouvé. Neutre vis à vis du fournisseur.

- `image` : description photographique complète en français (ou anglais si le modèle le préfère), sujet, action figée à l'instant le plus lisible, cadrage, lumière, décor, matière, « format vertical 9:16 », style réaliste (ou « rendu 3D scientifique, fond sombre, éclairage de studio » pour 3DSCI). Pas de texte dans l'image, pas de marque visible sauf si le produit de l'utilisateur est fourni en référence.
- `motion` : le mouvement attendu en une phrase, durée (2 à 4 s), mouvement de caméra (léger push, orbit lent, statique), ce qui doit bouger et ce qui doit rester stable, « pas de morphing, pas de changement de sujet ».

Pour 3DSCI, écris le prompt comme un brief à un animateur scientifique : échelle (« vue microscopique »), éléments nommés (« fibres de cellulose », « particules de graisse »), action (« les particules sont capturées puis emportées »), palette cohérente avec le lookbook, fond uni pour faciliter le recadrage.

## 8. Cartes de plans

`shot-cards.md` contient des séquences prêtes à l'emploi par univers (nettoyage et maison, peau et cosmétique, hygiène, animal, générique) avec les 3 valeurs, les requêtes types et les pièges. Pars d'une carte quand l'univers correspond, adapte le sujet, ne recopie jamais une requête sans y mettre le lookbook.
