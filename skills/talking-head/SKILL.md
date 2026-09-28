---
name: talking-head
description: "Se déclenche uniquement quand l'utilisateur écrit « talking head » (ou /talking-head). Crée une vidéo talking head éducative 9:16 style podcast à partir d'un script et d'une voix off : découpage, génération des scènes, montage."
---

# Talking head éducative (avatar + voix off)

## Déclencheur

Ce skill ne s'active que sur le mot « talking head » (ou la commande /talking-head). Sans ce mot, ne l'utilise pas, même pour une demande de vidéo proche.

## Le format

Une seule voix off (le mp3 ElevenLabs de l'utilisateur) porte toute la vidéo. Par-dessus, on alterne :
- l'avatar assis à un bureau avec micro, caméra fixe, qui parle avec la voix de la voix off (imitée par Seedance, lèvres synchrones) ;
- une accroche en écran partagé (avatar en haut, b-roll en bas, bandeau titre) ;
- une animation éducative (3D ou motion design) pour le mécanisme invisible ;
- des images statiques, infographies, objets détourés et preuves ;
- des b-rolls trouvés sur Instagram et TikTok par l'utilisateur.

Aucun produit à vendre, aucun appel, une seule voix.

## Ce qui vient du skill Hotline (à respecter)

1. **D'abord l'image de départ** : l'avatar assis dans le studio, avec la bonne tenue, la bonne lumière, le bon cadrage et la posture de départ. Elle est générée à partir de la référence de l'avatar avec un modèle d'image : GPT Image 2 (édition depuis la référence) ou Soul (nouveau casting fictif).
2. **Ensuite la scène vidéo à partir de cette image**, avec un modèle vidéo dialogué : **Seedance 2.5**. La voix est générée par Seedance en même temps que les lèvres, en imitant l'extrait de la voix off ElevenLabs joint en référence (`@Audio1`) : les lèvres sont synchrones par construction.
3. **Jeu** : regard légèrement hors caméra, petites réactions, respiration, gestes utiles au propos, aucune boucle de geste répétitive, mains jamais devant la bouche.
4. **Continuité** : chaque clip repart de la même image de départ validée (même personne, tenue, micro, bureau, lumière, cadre). Ne relance pas le casting sans raison.
5. **Voix et lèvres générées ensemble** (`generate_audio: true`). Ne colle jamais une autre voix sur des lèvres déjà animées, et n'utilise pas de synchroniseur labial après coup.
6. **Références réellement jointes et balisées** : chaque image ou audio joint est désigné dans le prompt par sa balise `@Image1`, `@Image2`, `@Audio1`… (ordre d'envoi), jamais par « Image 1 » en texte libre. Un chemin local ne vaut pas un fichier téléversé.
7. **Prompts complets** : tous les champs remplis, aucune référence absente, jamais « comme dans l'exemple ».
8. **Une demande de prompts ou de découpage n'autorise pas une génération payante.** Ne redemande pas une autorisation déjà donnée.
9. **Journal** de chaque génération, contrôle des fichiers réellement obtenus, originaux conservés.
10. **Honnêteté** : « prompts préparés » (ou découpage livré), « médias générés » et « vidéo montée et contrôlée » sont trois états différents.

## Fichiers du skill

| Fichier | Quand le lire |
|---|---|
| `references/grammaire.md` | toujours, avant tout découpage : l'expertise tirée de 5 vidéos de référence (quel visuel sous quelle phrase, timing, rythme) |
| `references/prompts.md` | avant toute génération (image de départ, scène avatar Seedance 2.5, images, objets détourés, animations, b-roll de secours, fiches de recherche) |
| `references/modeles.md` | avant la première génération (rôle de chaque modèle, réglages, clip test, budget, journal) |
| `references/montage-controle.md` | avant le montage (gabarit Remotion, format de `montage.json`, contrôles) |
| `scripts/` (chemins relatifs au dossier du skill) | `transcrire.py`, `couper_audio.py`, `preparer_medias.sh`, `rendre.sh`, `controler.py`, `finaliser.sh` |
| `montage-remotion/` | gabarit de montage testé, piloté par `montage.json` (exemple : `montage.exemple.json`) |

Le skill ne désigne aucun fournisseur. Les générations passent par le service ou le connecteur disponible dans la session ; si des instructions propres à ce service sont installées ailleurs (dossier ou skill dédié), suis-les pour les noms exacts des champs, l'envoi des fichiers et le suivi des tâches.

## Ce que l'utilisateur fournit, et rien d'autre

- **Une seule fois** : 1 à 3 photos de son avatar.
- **À chaque vidéo** : le script final et la voix off ElevenLabs correspondante (mp3 ou wav).
- **Pendant la production** : les b-rolls qu'il télécharge depuis Instagram ou TikTok d'après les fiches de recherche (le skill ne télécharge rien sur ces plateformes), et les captures de preuve demandées.

Ne demande ni niche, ni cible, ni ton, ni langue : déduis-les du script et de l'audio. Ne demande pas de charte : propose-la à la première vidéo. Les faits du script sont vérifiés par l'utilisateur en amont : ne t'en occupe pas. Une capture de preuve affichée à l'écran est toujours une vraie capture fournie par l'utilisateur.

## Standards fixes

- **Format final** : 9:16, 1080 x 1920, 30 i/s, H.264 + AAC.
- **Clips avatar** (Seedance 2.5) : 9:16 pour le plein écran, **1:1** pour la moitié haute de l'écran partagé (recadré en 1080 x 960), 1080p, 4 à 30 s par clip.
- **Caméra fixe** sur tous les clips avatar. Le dynamisme vient des zooms au montage : A (100 %), B (environ 115 %), C (environ 130 %), comme les 3 caméras d'un vrai podcast.
- **Voix hybride** : sur les passages avatar, la voix générée par Seedance dans le clip (lèvres synchrones) ; ailleurs, la voix off ElevenLabs d'origine, jamais régénérée ni accélérée. Les morceaux sont mis bout à bout, ramenés au même volume, et le découpage est recalé sur cette nouvelle piste (`montage-controle.md`). Le son des b-rolls et des animations est toujours coupé.
- **Modèles** : GPT Image 2 en 1K (images de départ, images statiques, objets détourés), Soul (casting fictif si besoin), Seedance 2.5 (scènes avatar), MiniMax H3 (animations éducatives depuis une image de départ, b-roll de secours).
- **Montage** : FFmpeg + Remotion (gabarit fourni).
- **Aucun texte généré** dans les images et vidéos : tout texte est ajouté au montage.

## Les 4 modes

| Mode | Déclencheur | Ce qu'il fait | Coût |
|---|---|---|---|
| 0. Configuration | première utilisation, ou « change mon studio / ma charte » dans une session talking head | images de départ 9:16 et 1:1, clip test Seedance 2.5, charte | quelques images + 1 clip test |
| A. Découpage | « talking head » + script + voix off (mode par défaut) | décide quoi montrer à chaque phrase, découpe la voix pour les clips avatar, livre le plan complet | gratuit |
| B. Production | l'utilisateur valide le découpage et demande la production | génère les clips avatar, images, objets détourés, animations | payant |
| C. Montage | médias réunis (générations + b-rolls reçus) | monte, contrôle, exporte | gratuit |

Le mode A ne déclenche jamais de génération payante. En mode B, annonce l'estimation avant la première génération. Le mode A ne dépend pas du mode 0 : sans configuration, découpe avec une charte provisoire signalée comme telle, et fais la configuration avant le mode B.

## Mode 0 : configuration (une seule fois)

1. **Image de départ 9:16** (gabarit 1a) : GPT Image 2 en édition depuis les photos de l'avatar, 1K. 2 à 4 propositions, une validée. Si l'utilisateur veut un nouveau personnage fictif au lieu de son avatar : casting avec Soul, puis GPT Image 2 en édition depuis le portrait Soul validé pour obtenir la scène studio.
2. **Image de départ 1:1** (gabarit 1b) : même scène, en joignant aussi le 9:16 validé.
3. **Clip test Seedance 2.5** (gabarit 2, balises `@Image1` / `@Audio1`, `generate_audio: true`) : 5 à 8 s sur un extrait de voix off. Contrôle identité, cadre, micro, ressemblance de la voix, prononciation (Whisper), émotions, lèvres, bouche fermée dans les silences. Ajuste le prompt ou le mode d'envoi jusqu'à validation, puis note les réglages qui marchent.
4. **Charte** à faire valider : couleur principale et secondaire, style des sous-titres, couleur du bandeau d'accroche, fond des infographies, style unique des animations éducatives (pictos plats sur fond uni, gravure annotée, ou rendu 3D médical dans des cercles lumineux), pseudo et photo du bouton « S'abonner ».
5. **Rangement** dans le dossier de l'utilisateur : `_config/depart_9x16.png`, `_config/depart_1x1.png`, `_config/charte.json` (valeurs `theme` du montage, style d'animation, réglages Seedance validés). Relis-les à chaque vidéo au lieu de les recréer.

## Mode A : le découpage (livrable principal)

Lis `references/grammaire.md` en entier avant de commencer.

1. **Transcription** : `python3 scripts/transcrire.py voix.mp3` (faster-whisper, installable par pip). Le script fait autorité sur les mots, la transcription sur les temps : aligne-les et signale les écarts. Si la transcription est impossible, demande l'export horodaté d'ElevenLabs. Jamais d'estimation au comptage de mots.
2. **Format du script** : mécanisme, tuto, étude ou liste numérotée (grammaire, section 2). Il fixe le dosage d'avatar.
3. **Phrases visuelles** : coupe aux fins de phrase, virgules fortes et pauses. Chaque coupe tombe dans le silence, 0,05 à 0,3 s avant le premier mot.
4. **Choix du visuel** phrase par phrase : les 8 règles (R1 à R8) et leur priorité, les 4 recettes d'accroche, l'animation éducative, le micro-montage, les surimpressions.
5. **Rythme** : changement d'image toutes les 2 à 5 s, coupes d'angle A/B/C pendant les longs passages avatar, jamais deux fois le même zoom de suite, plus long bloc sans avatar sous 15 s, une seule animation éducative.
6. **Clips avatar** : un passage d'avatar ininterrompu = un clip, même s'il change de zoom. Deux passages séparés par moins de 1,5 s d'illustration peuvent partager un clip. L'écran partagé a son propre clip 1:1. Écris `decoupage.json` (clé `clips_avatar` : [{`id`, `debut`, `fin`, `format`}], `debut` et `fin` = premier et dernier mot du passage), puis `python3 scripts/couper_audio.py voix.mp3 decoupage.json --mots mots.json --min 4 --max 30`. Il écrit un extrait par clip, coupe à une pause les passages dont l'extrait (marges comprises) dépasserait 30 s, et donne le `clipStart` de chacun pour le montage.

**Le livrable** (`decoupage.md` lisible + `decoupage.json` + `audio_avatar/`) :

1. **Synthèse** : format détecté, durée, débit, nombre de plans, durée moyenne, répartition en secondes et en % (écran partagé, avatar, avatar + surimpression, animation, statique, b-roll), nombre de clips avatar et secondes à générer, nombre d'images, d'objets détourés, d'animations et de b-rolls à trouver, écarts entre script et audio.
2. **Tableau de découpage** :

| # | Début | Fin | Durée | Texte exact | Type | Zoom | Surimpression | Ce qu'on voit | Règle | Mot déclencheur | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|

   - Temps au dixième de seconde, calés sur les mots.
   - « Ce qu'on voit » décrit l'image concrète.
   - « Règle » = R1 à R8, accroche, animation ou micro-montage.
   - « Mot déclencheur » = le mot sur lequel un élément apparaît, avec son temps.
   - « Source » = clip avatar n°, image n°, animation n°, b-roll n°, preuve n°.
3. **Clips avatar** : pour chacun, l'extrait audio, sa durée, le format (9:16 ou 1:1), la timeline des mots, le geste attendu et son moment, et le prompt Seedance 2.5 complet (gabarit 2).
4. **Prompts** complets : images statiques, objets détourés, images de départ et animations H3 (étapes calées sur les mots).
5. **Fiches b-roll** : une par plan (gabarit 7), classées par importance.
6. **Accroche** : 3 propositions de bandeau (6 à 12 mots, promesse ou menace).
7. **Preuves à fournir** : captures nécessaires et zone à surligner.

## Mode B : production

Après validation du découpage et demande explicite. Lis `references/modeles.md` et `references/prompts.md`.

1. Liste des générations et estimation, annoncées avant la première.
2. **Clips avatar (Seedance 2.5)** : pour chaque clip, image de départ du bon format + extrait audio + prompt du découpage, avec les réglages validés en configuration. Lance d'abord le premier clip, contrôle-le (identité, cadre, lèvres), puis enchaîne les autres. Contrôle chaque clip reçu ; relance uniquement un clip défectueux.
3. **Animations** : image de départ GPT Image 2 (style de la charte), validée si le style est nouveau, puis MiniMax H3.
4. **Images statiques et objets détourés** : GPT Image 2, 1K.
5. **B-roll de secours** : seulement pour un plan que l'utilisateur n'a pas trouvé, et avec son accord.
6. Journal `journal_generations.md` à jour ; chaque résultat téléchargé dans le dossier de la vidéo, nommé selon le découpage.

## Mode C : montage

Lis `references/montage-controle.md`.

1. Vérifie que tout est là : voix, clips avatar (durée, format, résolution), b-rolls, générations, preuves, charte. Liste ce qui manque au lieu de deviner.
2. Normalise les vidéos (`preparer_medias.sh`), range-les dans `public/`, construis la **piste voix hybride** (voix Seedance des clips avatar + voix off ailleurs, section « Voix hybride » de `montage-controle.md`), puis écris `montage.json` avec tous les temps recalés sur cette piste et les sous-titres (texte du script, temps de l'audio).
3. Images fixes de contrôle aux moments clés, puis rendu complet en arrière-plan (`rendre.sh`), contrôle (`controler.py`), corrections, finalisation (`finaliser.sh`).
4. Livre la vidéo finale dans le dossier de l'utilisateur, avec `montage.json` (pour les retouches) et, sur demande, une feuille de montage CapCut.

Retouches (« ce zoom est trop long », « enlève ce b-roll ») : modifie `montage.json`, vérifie avec une image fixe, relance le rendu.

## Où travailler

Les fichiers de l'utilisateur vivent dans son dossier de projet. La transcription et le rendu demandent Python, Node et un navigateur sans interface : fais-les là où ils sont disponibles, en y copiant uniquement les médias nécessaires, puis renvoie la vidéo finale dans le dossier de l'utilisateur. Arborescence conseillée : `_config/`, puis un dossier par vidéo (`script.txt`, `voix.mp3`, `mots.json`, `decoupage.md`, `decoupage.json`, `audio_avatar/`, `avatar/`, `broll/`, `generations/`, `preuves/`, `montage/`, `export/`, `journal_generations.md`).

## Livraison

Livre uniquement les fichiers réellement créés et dis où ils sont. Signale ce qui reste à faire (b-rolls à trouver, preuves à fournir, contrôles non effectués). Si un média n'a pas pu être regardé ou écouté, dis-le.

N'utilise jamais de tiret cadratin ni de tiret demi-cadratin dans les textes produits pour l'utilisateur : utilise des points, des virgules, des parenthèses ou des retours à la ligne.
