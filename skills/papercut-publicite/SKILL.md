---
name: papercut-publicite
description: "Créer une publicité Paper Cut : collage de papier déchiré, photos découpées, mots courts, stop-motion et voix off externe, sans musique ni sous-titres par défaut."
---

# Créer des vidéos tendance en style papercut

## Fidélité du style et de la méthode

Avant d’écrire les prompts, lire [references/signature.md](references/signature.md) puis [references/prompts.md](references/prompts.md). La signature contient les détails de matière, anatomie, cadre, mouvement et son propres à ce module. Les recopier dans les prompts utiles ; ne pas les remplacer par un simple nom de style.

Adapter la marque, le sujet, le casting original, le produit et la langue. Conserver la grammaire visuelle et le mode audio du module. Une demande explicite de l’élève peut les changer : expliquer alors l’adaptation. Ne pas appliquer une règle d’un autre module parce que ses personnages se ressemblent.

## Adapter à la marque de l'élève

Avant le script, lis son Brand DNA s'il est fourni. Sinon, construis ici une fiche courte avec les informations disponibles : produit ou service, cible, problème, promesse, preuves vérifiables, ton, palette, éléments visuels et appel à l'action. Aucun fichier au nom imposé ni autre skill n'est nécessaire. Distingue les faits des hypothèses et demande seulement les données décisives manquantes.

Utilise les photos produit et les captures de l'élève. N'importe aucun personnage, slogan, prix, avis, dosage, résultat ni nom provenant d'une autre campagne. Le héros, les accessoires et la métaphore doivent servir cette marque. Les noms de styles du module servent de repères visuels, pas de marques à ajouter aux images. La durée affichée du tutoriel n'est pas la durée de la publicité à produire.

Les instructions ci-dessous décrivent le processus de départ du module. Les demandes explicites de l'élève priment sur les choix de durée, de langue, de format et de sous-titres. Si sa demande change une signature du format, explique l'adaptation sans changer silencieusement le procédé.

## Signature

Collage scrapbook à plat : couches de papier déchiré, photographies découpées, lettres de journal, marques de feutre, touches de peinture et ombres de superposition. Le titre principal vit dans le collage. Une voix off raconte ; aucun visage n'a besoin de parler.

## Processus

1. **Script.** Une ligne = une idée = un collage. Résume chaque idée par un titre court, souvent un à trois mots, dans la langue de la publicité. Une ligne à deux idées doit être divisée ou réécrite.
2. **Voix.** Récupère ou produis la narration et mesure ses unités avant les durées définitives. Un compte de mots peut estimer, jamais remplacer cette mesure.
3. **Moodboard émotionnel.** Choisis papier de base, couleur du problème, couleur de résolution, encre et matières. Conserve les rôles émotionnels de la palette ; rapproche les teintes de la marque seulement lorsque cela reste cohérent. Écris le bloc de style une fois et réutilise-le.
4. **Storyboard.** Chaque collage indique : phrase VO, titre exact, sous-texte éventuel, visuel découpé, marque de feutre, peinture, couleur dominante, mouvement, durée et présence du produit. Relis tous les titres avant de générer.
5. **Images.** Compose quelques couches lisibles. Le produit est une découpe fidèle aux photos fournies. Les seuls textes lisibles sont ceux explicitement prévus ; n'ajoute pas de faux calendrier ou de microtexte décoratif.
6. **Texte fiable.** Vérifie chaque lettre. Si le modèle déforme le titre, compose-le séparément avec l'apparence de lettres découpées puis intègre-le au collage ; ne paye pas des animations sur un texte fautif.
7. **Animation.** Déplacement de couches, apparition de titre, tampon ou léger tremblement posé à la main. Conserve les découpes exactes et les lettres : pas de morphing ni de réécriture. Bruitages de papier sans voix ni musique intégrées.
8. **Montage.** Cale les collages sur la narration entière. Les titres intégrés portent déjà la lecture : pas de sous-titres redondants par défaut. Si l'élève demande l'accessibilité, fournis un SRT ou une zone distincte sans couvrir le collage. Par défaut, bruitages papier et voix seuls, sans musique ; ajouter de la musique seulement si demandée.

## Contrôles

Titre et sous-texte exacts, pas de langue parasite, produit fidèle, couches et ombres cohérentes, lettres stables pendant l'animation, absence de trou entre collages, voix complète. Une image fixe voulue doit être distinguée d'une animation qui n'a pas bougé.

## Outils de référence, facultatifs

Images : Nano Banana 2 ; animation : Omni avec bruitages papier ; voix off externe. Texte composé séparément si nécessaire.

## Public et environnement : élèves de la formation

Ce skill est distribué à des élèves qui l'installent dans leur propre Claude. Pars d'un environnement neuf : ils ne disposent ni des outils internes du formateur, ni de son serveur, ni de ses fichiers, comptes, clés API, connecteurs ou logiciels. Ne leur demande jamais de retrouver une infrastructure privée. Le workflow doit fonctionner pour leur marque et leurs ressources, sans autre skill obligatoire.

Ne suppose pas que Whisper, Palmier, FFmpeg ou un générateur de médias soient installés. Distingue toujours trois états : logiciel installé sur l'ordinateur, logiciel accessible à cette session de Claude, et connexion effectivement testée. Une installation sur le Mac ou le PC de l'élève ne donne pas automatiquement accès à ce logiciel depuis Claude. Un outil exécuté dans l'environnement de Claude n'est pas pour autant installé sur l'ordinateur de l'élève.

### Accompagner l'élève quand un outil manque

1. Identifie le besoin concret de l'étape : transcrire, créer une image, animer, produire une voix, monter ou exporter. Regarde d'abord les outils et ressources réellement accessibles. Ne demande pas une liste technique complète à un débutant si les capacités de la session suffisent à avancer.
2. Explique simplement le rôle de l'outil manquant et le livrable qu'il permet d'obtenir. Propose en priorité l'outil déjà disponible chez l'élève lorsqu'il répond au besoin.
3. Si une installation est utile, propose-la comme une option, pas comme un prérequis implicite. Avant de donner des commandes, identifie le système de l'élève et la surface utilisée (Claude web, application, Cowork ou Claude Code), puis vérifie les instructions officielles actuelles, la compatibilité, les prérequis et les éventuels coûts. Si la documentation n'est pas accessible, indique ce qui reste à vérifier au lieu d'inventer une procédure ou une adresse de téléchargement.
4. Pour installer ou configurer sur son ordinateur, utilise seulement un accès réellement disponible et son autorisation. Si cet accès manque, accompagne-le pas à pas. Ne prétends pas avoir installé, connecté ou testé un logiciel sans résultat observable. Ne demande pas de coller une clé secrète dans la conversation : utilise le mécanisme de connexion sécurisé prévu par le service.
5. Après configuration, fais un essai court avec un fichier adapté : transcription d'un extrait, import d'un clip ou export de quelques secondes. Vérifie le fichier produit et l'accès depuis Claude. Ne lance pas toute une production pour découvrir si la connexion fonctionne.
6. Si l'élève ne souhaite pas installer, propose une alternative : fonction de transcription de son éditeur, service qu'il utilise déjà, travail manuel guidé ou dossier de préparation à exécuter ailleurs. Continue les étapes indépendantes du logiciel manquant. Si la demande porte sur une vidéo finale, précise l'étape restante et accompagne sa réalisation ; ne confonds pas le dossier de prompts avec la vidéo terminée.

### Whisper : transcription facultative

Whisper sert à transcrire la parole ; une implémentation compatible peut également fournir des repères temporels utiles au montage. Il ne génère pas la voix et ne réalise pas le montage. Tu peux proposer son installation si l'élève veut une transcription locale et si son environnement le permet. Vérifie l'implémentation choisie et ses prérequis, y compris le modèle à télécharger et les éventuelles dépendances. Ne suppose pas une commande, un fichier de modèle ou un chemin déjà présent.

Sinon, utilise une transcription disponible dans un outil de l'élève ou guide un repérage manuel. Vérifie le texte et les timecodes par écoute lorsque l'audio est accessible : une transcription automatique peut omettre des mots. Sans accès à l'audio ni timecodes fournis, conserve des durées provisoires et indique que le calage reste à mesurer.

### Palmier : montage facultatif

Palmier est une option de montage, pas une dépendance du skill. Tu peux proposer de l'installer si l'élève souhaite l'utiliser, après vérification de sa disponibilité et de la procédure officielle pour son système. N'invente pas de lien de téléchargement, de port local, de serveur ou de commande de connexion. Si ces informations ne peuvent pas être vérifiées, demande la documentation du logiciel ou utilise l'éditeur déjà disponible.

Explique séparément l'installation du logiciel et son éventuelle connexion à Claude. Si une intégration compatible est proposée, vérifie sa documentation et les opérations réellement exposées avant de la configurer. Un logiciel ouvert n'est pas une preuve que Claude peut le piloter. Sans intégration, fournis une feuille de montage avec l'ordre des clips, les coupes, les pistes, les sous-titres et les réglages d'export ; accompagne l'élève dans son éditeur. FFmpeg est aussi une option seulement s'il est disponible et adapté, jamais une commande supposée installée.

## Utilisation dans Claude

### Choisir le bon module et le bon mode audio

Vérifie que le style et le dispositif demandés correspondent à ce module. Des univers visuels proches peuvent avoir des processus différents : figurine à visage fixe sous une narration, personnage qui dialogue dans le clip, ou clip calé sur une chanson. Suis le mode défini dans la section du module et n'applique pas automatiquement les règles d'un autre format. Si la demande est ambiguë entre deux tutoriels, demande uniquement cette précision avant les générations payantes ; continue le brief de marque en attendant.

### Si Claude ne peut pas créer de fichiers

Prépare les livrables textuels directement dans la conversation, sous des blocs distincts et nommés : brief, script, storyboard, prompts et feuille de montage. Explique comment les enregistrer. Si la création de fichiers est disponible, fournis des fichiers téléchargeables ou utilise le dossier effectivement accessible. N'annonce jamais un fichier, un téléchargement, un export ou un dossier qui n'a pas été créé. L'absence d'accès au disque de l'élève ne bloque pas la préparation du projet.

Ce skill est autonome. Adapte-le à la marque, au sujet, à la langue et aux outils de l'utilisateur. Aucun logiciel de production ni autre skill n'est requis pour préparer le travail.

Lis d'abord les éléments déjà fournis. Demande seulement les informations indispensables qui manquent : objectif, public, produit ou sujet, durée, format, langue, ressources disponibles et éventuelle limite de budget. N'impose pas une marque, un personnage, une langue ou une durée issus d'un exemple. Si le brief est suffisant, avance avec des hypothèses explicites.

Vérifie les capacités réellement accessibles dans cette session : génération d'images, vidéo, voix, transcription, montage et fichiers. Utilise les outils connectés lorsqu'ils conviennent. Consulte leur documentation avant d'utiliser des paramètres, durées ou fonctions spécifiques ; n'invente pas de connecteur ou de route API. Une fiche vocale ou une image de référence améliore la cohérence sans la garantir.

Sans outil de génération ou de montage, réalise quand même les livrables préparatoires : script, références décrites, storyboard, prompts complets et feuille de montage. Indique précisément ce qui reste à exécuter dans l'outil de l'utilisateur. Ne présente jamais un prompt comme un média généré, ni une estimation comme une mesure. L'installation du skill ne connecte aucun service payant automatiquement.

Conserve le texte approuvé, les caractéristiques produit et les preuves fournies. Distingue une métaphore visuelle d'une preuve réelle ; ne fabrique pas de chiffres, de témoignages ou de qualifications. Les sous-titres, la musique et les préférences de style suivent le brief. Pour un service payant, respecte le budget autorisé et relève les tarifs actuels si accessibles ; sinon laisse le coût à chiffrer. Conserve les identifiants des générations et leurs variantes pour reprendre sans payer inutilement deux fois.

## Adapter le processus aux outils réellement disponibles

Les gabarits de prompts et l'ordre créatif sont portables ; les appels API d'une installation ne le sont pas. Ne copie aucune route, aucun port, aucun nom de serveur ni aucune commande issus d'une autre machine. Ne remplace pas une infrastructure privée supposée par une autre infrastructure privée supposée.

Si l'élève dispose déjà d'une application de création, d'un service vocal et d'un outil de montage, mappe chaque besoin vers leurs fonctions vérifiées : créer ou importer la voix, mesurer l'audio, générer une référence, produire une image, animer, récupérer le média, assembler et exporter. Découvre les opérations dans la documentation ou le connecteur réellement présent. Ne déduis pas qu'une route existe à partir du nom du module. Utilise les URL, ports et identifiants uniquement lorsqu'ils ont été fournis ou vérifiés dans cet environnement, sans les inscrire comme valeurs universelles dans le skill.

Si ElevenLabs est accessible, utilise-le pour la voix externe lorsque le module est narré. La règle reste : script approuvé → voix enregistrée → durée et phrases mesurées → découpage définitif. Sans voix disponible, prépare un storyboard provisoire puis recale-le dès réception du fichier. Les modules dialogués suivent la parole de leurs clips ; le clip musical suit sa chanson validée.

Si FFmpeg est disponible et que son usage convient à l'élève, il peut servir à inspecter les médias et à réaliser un montage programmatique ; vérifie les fonctions réellement installées. Palmier n'est pas obligatoire. Si un projet éditable est demandé, explique quel format ton outil peut réellement fournir. Sans accès à un logiciel, prépare les prompts et la feuille de montage tout en indiquant les opérations restant à exécuter. Ne conclus pas que tout le processus est inutilisable parce qu'une ancienne route API ne correspond pas à l'environnement.


## Fichiers de travail et reprise

Prépare dans le dossier choisi par l'élève : brief de marque, script, fiches personnages, storyboard, prompts, médias et exports. Le storyboard liste : ID, phrase exacte, mode audio, référence de personnage et de décor, cadre, état initial, mouvement, durée provisoire ou mesurée, produit visible, texte à composer au montage, bruitage et statut.

Garde un journal des générations : ID du plan, variante, prompt, références, ID de tâche, état fournisseur, fichier reçu, contrôle visuel et coût connu. Réutilise les résultats valides. Un timeout ne prouve pas l'échec : vérifie l'historique avant de renvoyer une tâche. Une nouvelle variante ne remplace jamais l'original avant contrôle. Les tarifs, formats et paramètres des modèles doivent être vérifiés dans les outils disponibles au moment de produire.

Les prompts modèles sont dans [references/prompts.md](references/prompts.md). Ils sont des gabarits de rédaction, pas des requêtes API. Remplace tous les champs entre crochets et n'envoie que les références utiles au plan. Adapte la langue du prompt au moteur ; le texte parlé et affiché conserve la langue de la publicité.

## Livraison et vérification

Livre les fichiers réellement créés avec des noms lisibles et un court état d'avancement. Un dossier de préparation doit comprendre le script, les fiches utiles, le storyboard, les prompts par plan et les consignes de montage. Si les médias ont été produits, ajoute le film et le projet éditable lorsque l'outil permet de le fournir.

Sur le film disponible, contrôle l'ordre et l'intégralité du texte, les noms et nombres prononcés, la cohérence visuelle, les coupes et la dernière réplique. Vérifie la synchronisation sur plusieurs passages, pas seulement la durée totale : viser un écart de durée audio/vidéo inférieur à 0,10 s ne prouve pas à lui seul le lip-sync. Confirme le format exporté, l'absence de trous involontaires et l'intelligibilité des voix. Déclare les contrôles impossibles faute d'accès aux médias.
