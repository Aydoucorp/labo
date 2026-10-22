# Compte-rendu d'Analyse Vidéo UGC pour Réplication IA

Ce document détaille l'analyse complète de la vidéo de référence selon les 6 piliers de l'authenticité UGC, afin de paramétrer vos outils d'IA (génération d'image, vidéo, voix et montage) avec une précision chirurgicale.

---

## 1. L'esthétique de l'image (Le "Look" smartphone)

* **Capteur et optique :** Filmé au smartphone en format vertical 9:16 avec la caméra frontale (grand-angle léger, environ 24-26 mm). On note une très légère distorsion de proximité lorsque ses mains s'approchent de l'objectif.
* **Profondeur de champ :** Pas de flou d'arrière-plan artificiel (mode portrait désactivé). Le sujet et le mur du fond sont relativement nets, typique d'un petit capteur de téléphone.
* **Éclairage :** Lumière naturelle douce mais directionnelle venant de face/légèrement en haut à gauche (probablement face à une grande fenêtre). Le reflet dans ses yeux est rectangulaire/diffus (pas de *ring light* circulaire visible). L'exposition est légèrement haute sur le visage, lissant naturellement le grain de peau sans effet plastique.
* **Colorimétrie et netteté :** Balance des blancs neutre à légèrement chaude sur la peau, contrastant avec le fond froid. Présence du *sharpening* (netteté numérique) typique de l'iPhone sur les mèches de cheveux et les cils.
* **Mots-clés pour le prompt :** 
  > `shot on iPhone 15 front camera, vertical 9:16, natural window lighting from front-left, deep depth of field, no bokeh, authentic skin texture, slight digital sharpening`

---

## 2. Les mouvements de caméra

* **Stabilité :** Le téléphone est **posé sur un support fixe** (trépied de bureau ou posé contre un objet). Il n'est pas tenu à la main (ses deux mains apparaissent dans le cadre à `0:05`).
* **Micro-mouvements :** Bien que le plan soit fixe, on observe de très subtiles micro-vibrations à certains moments (ex: quand elle bouge énergiquement ou tape des mains), donnant l'impression que le téléphone est posé sur la même table ou surface où elle s'appuie.
* **Cadrage :** Plan poitrine serré (*medium close-up*), caméra placée légèrement au-dessus du niveau des yeux (elle lève très légèrement le regard vers l'objectif), ce qui affine le visage — un classique du cadrage TikTok.
* **Réplication IA :** Ne pas appliquer de *handheld camera shake* constant. Garder une caméra fixe mais ajouter un très léger *table vibration* ponctuel ou utiliser les jump-cuts pour créer le mouvement.

---

## 3. Le décor (Le Background)

* **Composition :** Un angle de pièce simple mais texturé, divisé verticalement (environ 2/3 à gauche pour le mur, 1/3 à droite pour le rideau).
* **Éléments visuels :** 
  * **À gauche :** Un mur avec des boiseries/soubassements géométriques (*wainscoting*) peints en bleu-gris mat (bleu pigeon/ardoise clair).
  * **À droite :** Un rideau épais en lin ou tissu texturé beige/écru qui tombe verticalement.
  * **En bas à droite (visible brièvement selon ses mouvements) :** Le dossier d'un fauteuil ou canapé beige clair sur lequel elle est assise.
* **Rôle dans l'UGC :** C'est un décor "propre mais habité" (style maison nord-américaine moderne). Il apporte de la profondeur grâce aux lignes des boiseries et aux plis du rideau, sans aucun objet distrayant qui détournerait l'attention du visage.

---

## 4. L'acting et le langage corporel

* **Posture :** Assise, le buste légèrement penché en avant vers la caméra, créant un sentiment de confidence et d'intimité ("discours entre amies").
* **Gestuelle des mains (très active) :**
  * `0:00 - 0:02` : Elle pointe vers le bas (où s'affiche l'image incrustée).
  * `0:03 - 0:06` : Mains jointes/entrelacées devant la poitrine (accessoires visibles : montre connectée blanche à gauche, élastique à cheveux noir au poignet droit — **détail ultra-authentique**).
  * `0:10` : Geste de pincement avec les doigts pour illustrer le mot *"miniaturization"*.
  * `0:18 - 0:22` : Énumération rythmée avec la main gauche ouverte qui bat la mesure, puis poing fermé/main levée pour marquer l'emphase sur *"ignoring it"*.
  * `0:33` : Pointe directement vers l'objectif/le spectateur sur *"make sure you follow"*.
* **Expressions faciales et regard :** 
  * Contact visuel maintenu à 90 % avec l'objectif.
  * Haussements de sourcils fréquents pour appuyer les mots clés.
  * Micro-expression clé à `0:19` : elle ferme les yeux, hausse les épaules et fait une moue d'impuissance juste après *"Trimming your hair won't fix this"*.
  * Mouvements de tête constants (hochements, inclinaisons sur le côté) qui cassent toute rigidité.

---

## 5. Les imperfections de la voix et l'audio

* **Ton et prosodie :** Ton d'experte bienveillante, posé mais dynamique. Elle utilise beaucoup d'inflexions vocales (elle monte dans les aigus sur les questions implicites et descend dans les graves pour les constats sérieux).
* **Détails organiques à cloner (ElevenLabs / Audio-to-Audio) :**
  * **Le soupir audible (`0:19`) :** C'est l'élément le plus humain de la vidéo. Juste avant de dire *"Collagen won't fix this"*, elle lâche un vrai soupir d'exaspération/empathie.
  * **L'emphase vocale (`0:21`) :** Elle étire et accentue fortement le mot *"definitely"* (*"Ignoring it DE-FI-NITE-LY won't fix this"*) avec une légère friture vocale (*vocal fry*) en fin de phrase.
  * **Acoustique :** Son très sec et proche (micro d'iPhone à 40 cm), sans musique de fond, avec une très légère réverbération naturelle de pièce de vie (pas un son étouffé de cabine studio).

---

## 6. Le montage, le rythme et les éléments visuels (Post-Prod)

* **Les Jump-cuts :** La vidéo de 36 secondes comporte **11 coupes franches (jump-cuts)** : à `0:02`, `0:06`, `0:08`, `0:17`, `0:19`, `0:21`, `0:23`, `0:28`, `0:30`, `0:31`, et `0:33`.
* **Fonction des coupes :** Elles suppriment toutes les respirations d'inspiration (sauf le soupir volontaire à `0:19`). Sur chaque coupe, sa tête change légèrement de position (de quelques centimètres), ce qui maintient l'œil du spectateur en éveil.
* **Incrustations (Overlays) :**
  * `0:00 - 0:02` : Texte d'accroche (*Hook*) en haut en police blanche avec contour noir + photo comparative de raies de cheveux en bas.
  * `0:10 - 0:13` : Schéma médical de la miniaturisation du follicule pileux centré en bas.
* **Sous-titres (Captions) :** Affichage **mot par mot** (ou par groupe de 2 mots maximum), en majuscules blanches sans contour mais avec une ombre portée légère, positionnés à gauche à hauteur d'épaule/cou pour ne jamais couvrir sa bouche ni ses gestes.