---
name: ebook-full-value
description: Crée un ebook lead-magnet "full value" (livre numérique offert en échange d'un commentaire sur un reel) à partir d'une problématique donnée en une ou deux phrases, pour n'importe quelle marque et n'importe quelle niche. Déclenche ce skill quand l'utilisateur veut créer un ebook, un guide offert, un lead magnet, un PDF à envoyer en DM, ou dit "fais-moi un ebook sur...", "guide offert", "lead magnet", "ebook pour ma niche". Le skill lit la Brand DNA du dossier, fait une deep research sérieuse pour trouver des solutions viables et sourcées, agence l'ebook pour un maximum de valeur, verrouille la cohérence graphique sur toutes les pages, puis génère chaque page en image via GPT Image 2 (API Kie, format 3:4 portrait, résolution 1K).
---

# Ebook Full-Value

Ce skill produit un ebook lead-magnet qui déclenche le "franchement merci pour les astuces" chez le lecteur. Un ebook = plusieurs pages, chaque page = une image générée. Le livre est offert gratuitement en échange d'un commentaire sous un reel (mot déclencheur), puis envoyé en message privé.

## Principe directeur

Plus de solutions que de problème. Au maximum 1 à 2 pages nomment le problème, tout le reste le résout concrètement. Le lecteur repart avec de l'applicable aujourd'hui. Tout ce qui est affirmé est vrai et sourcé (issu de la deep research), jamais inventé.

## Pré-requis dans le dossier

Un fichier Brand DNA (branding de la marque) doit être présent dans le dossier de travail. Il contient l'identité de la marque : nom, porte-parole, réseaux, couleurs, polices, logo, ton, style d'illustration. Lis-le AVANT tout le reste et appuie tout le travail dessus. Ne mets jamais d'identité de marque en dur dans ce skill : tout vient de la Brand DNA. Si aucun fichier Brand DNA n'est trouvé dans le dossier, demande à l'utilisateur où il se trouve avant de continuer.

## Workflow en 6 étapes

Exécute ces étapes dans l'ordre. Ne saute aucune étape.

### Étape 0 — Lire la Brand DNA

Lis le fichier Brand DNA du dossier. Extrais et garde sous la main, pour tout le reste du travail :
- Le nom exact de la marque (tel qu'il doit être affiché).
- Le nom du porte-parole / personnage (celui qui signe les pages et parle à la première personne).
- Le handle et les réseaux sociaux (pour le CTA de fin).
- Les couleurs exactes (codes hex) : fond, couleurs principales, accents, texte.
- Les polices : titre, corps de texte, signature.
- Le style du logo / brand mark et sa formulation exacte.
- Le ton de voix (tutoiement ou vouvoiement, registre, formules récurrentes).
- Le style d'illustration (ex. flat-vector, aquarelle, etc.) et la palette.
- La langue de l'ebook.
- S'il est permis ou non de représenter des visages humains.

Tout ce que tu produis ensuite (textes, prompts, DA) respecte strictement ces éléments.

### Étape 1 — Cadrer la problématique

L'utilisateur donne la problématique en une ou deux phrases. Analyse-la et reformule-la pour vérifier que tu as compris QUEL problème précis on résout chez le prospect, et quelle émotion est en jeu. Si tu as le moindre doute sur le problème réel, pose UNE question de clarification avant d'avancer. Ne devine pas. Ne commence la recherche qu'une fois le problème clairement compris.

### Étape 2 — Deep research sérieuse

Va sur le web et cherche en profondeur les solutions viables à la problématique. C'est cette recherche qui donne toute la valeur de l'ebook, donc elle doit être approfondie (plusieurs recherches sous différents angles, pas une seule requête).

Règle stricte sur les sources : n'utilise que des sources carrées. Privilégie les institutions (agences sanitaires, environnementales, publications officielles), les études, les publications avec citations et sources vérifiables, les sites d'expertise reconnue. Écarte le SEO bidon, les forums non sourcés, les blogs qui recopient des mythes, le contenu promotionnel déguisé. Si une astuce populaire est en réalité un mythe inefficace, écarte-la ou signale-la honnêtement.

Collecte et garde la trace de :
- Les vraies solutions applicables (gestes, méthodes, dosages, réflexes).
- Les faits et chiffres sourçables (avec la source).
- Les pièges et erreurs courantes à éviter.
- Les nuances honnêtes (ce qui marche vraiment vs ce qui est survendu).

Note les sources pour pouvoir les citer sobrement dans l'ebook quand c'est pertinent.

### Étape 3 — Choisir l'angle et agencer l'ebook

Selon la problématique et l'émotion, choisis UN angle dominant :
- **Éducatif** : expliquer un mécanisme que la personne n'avait jamais relié. Déclenche "ah je savais pas".
- **Résolution de dilemme** : la personne est coincée entre deux peurs, on ouvre une troisième voie. Déclenche "tu m'as débloqué".
- **Full astuces** : un maximum de tips concrets, groupés par catégorie ou par pièce. Déclenche "merci pour les astuces".
- **Argent / simplicité** : montrer un vrai calcul ou un gain concret. Déclenche "je vais gagner / économiser".

Puis construis le plan page par page en suivant la structure universelle ci-dessous. Vise 8 à 10 pages. Pour chaque page, décide précisément quoi mettre pour un maximum de valeur. Le cœur de l'ebook porte les solutions trouvées en deep research.

### Étape 4 — Rédiger le contenu

Écris le texte exact de chaque page. Applique le ton du porte-parole (lu dans la Brand DNA), les règles de contenu non négociables (plus bas), et appuie chaque solution sur la deep research. Du concret, zéro remplissage. Calibre l'émotion : on peut jouer la peur, le dégoût ou l'agacement au début, mais on finit toujours sur du rassurant et de l'actionnable.

### Étape 5 — Assembler les prompts de génération

Pour chaque page, produis un prompt autonome et complet, dans cet ordre précis :
1. Le bloc de lock DA (identité visuelle issue de la Brand DNA, voir "Cohérence DA").
2. Les verrous anti-déchets (voir plus bas).
3. Le contenu exact de la page (textes entre guillemets, à reproduire mot pour mot).
4. Le rappel final des verrous.

Les verrous et le rappel final sont TOUJOURS placés en dernier dans le prompt. C'est ce qui corrige les dérives du modèle d'image. Chaque prompt doit pouvoir être lancé seul, sans dépendre des autres.

### Étape 6 — Générer les images via l'API Kie

Génère chaque page en image avec GPT Image 2 via l'API Kie. Tu es déjà connecté à Kie : lance la génération. Specs obligatoires :
- Modèle : GPT Image 2.
- Format : 3:4 portrait (format livre numérique, lu au mobile).
- Résolution : 1K.
- Une page = une image.
- Génère page par page, dans l'ordre.

Après génération, propose d'assembler les images en un PDF (une version web légère pour l'envoi en message privé, et une version haute qualité), avec un nom de fichier court et clair.

## Structure universelle (8 à 10 pages)

Pages d'ouverture et de fermeture fixes, cœur adaptable à l'angle.

- **Page 1 — Couverture** : un badge court type "LE GUIDE OFFERT", un grand titre accrocheur, un sous-titre bénéfice, trois petits badges preuves, une illustration centrale, et une ligne chaleureuse de cadeau en bas. Pas de numéro de page sur la couverture.
- **Page 2 — Le mot d'intro** : une lettre du porte-parole, chaleureuse, qui crée le lien, pose la promesse de l'ebook, et se termine par la signature manuscrite du porte-parole.
- **Page 3 — Le reframe** : une seule page qui recadre le problème et rassure, avec une phrase forte mise en avant dans une carte. C'est le pivot émotionnel.
- **Pages 4 à N-2 — Le cœur de valeur** : la partie qui porte les solutions issues de la deep research. Selon l'angle : mécanisme + fait clé sourcé, ou astuces groupées par catégorie, ou méthode pas à pas, ou calcul concret. C'est ici que se joue le "merci". Chaque page reste claire et aérée.
- **Page N-1 — Le mémo** : quatre cartes récapitulatives en grille deux par deux, avec les points clés à retenir.
- **Page N — À toi de jouer** : clôture encourageante, le geste numéro un à faire aujourd'hui, et un appel à suivre la marque sur les réseaux (optionnel, selon la Brand DNA et le souhait de l'utilisateur).

Adapte le nombre de pages du cœur selon la richesse du sujet, en gardant toujours couverture + mot d'intro + reframe au début, et mémo + clôture à la fin.

## Règles de contenu non négociables

- **Vérité d'abord** : rien d'inventé. Tout fait ou chiffre vient de la deep research et doit être sourçable. Présente les chiffres en fourchette prudente (environ, peut atteindre). Un seul chiffre choc suffit.
- **Émotion mesurée** : on peut jouer l'émotion, mais jamais d'anxiogène gratuit. On finit toujours sur du rassurant et de l'actionnable.
- **Solutions réelles** : de vrais gestes, de vrais dosages, de vraies méthodes validées par la recherche. Aucun mythe internet.
- **Zéro marque commerciale tierce** : reste générique (le type de produit, pas la marque).
- **Prudence santé** : sur les sujets sensibles (bébé, animaux, peau, symptômes, santé), ne jamais promettre de guérison. Formuler "réduire l'exposition peut aider" et renvoyer vers un professionnel.
- **Langue et ponctuation** : langue et ton exactement ceux de la Brand DNA. Jamais de tiret cadratin (— ou –) : utiliser points, virgules, parenthèses, retours à la ligne. Aucun markdown visible dans les textes affichés (pas de dièse, pas d'astérisque, pas de tirets de séparation).

## Cohérence DA verrouillée (point critique)

L'identité visuelle issue de la Brand DNA doit être rigoureusement identique de la page 1 à la page N. Si on pose toutes les pages côte à côte, elles doivent former un livre homogène, comme sorti de la même main. Dans CHAQUE prompt de page, verrouille explicitement :

- **Les couleurs** : exactement les mêmes codes hex partout (fond, principales, accents, texte).
- **Les polices** : même police de titre, même police de corps, même police de signature, sur toutes les pages.
- **Le logo / brand mark** : en haut de chaque page (sauf couverture si la Brand DNA le prévoit ainsi), strictement identique partout, même formulation et même style.
- **Le numéro de page** : toujours à la même position (par défaut en bas au centre), numéroté de 1 à N, affiché comme un chiffre seul sans parenthèses ni mot autour.
- **Le style d'illustration** : même traitement et même palette partout.
- **La mise en page** : marges, cartes, espacements et ambiance homogènes.

## Verrous anti-déchets (dans chaque prompt, toujours en dernier)

Ces verrous corrigent les dérives observées des modèles d'image. Place-les en tête ET en rappel final de chaque prompt :

1. Tout le texte dans la langue de la Brand DNA, avec les accents corrects. Ne traduire aucun mot. Recopier le texte exactement comme écrit entre guillemets.
2. N'afficher QUE le texte listé. N'ajouter aucun texte, slogan, astuce, badge ou élément non listé.
3. N'afficher aucun élément d'organisation : pas de numéro de page entre parenthèses, pas de titre technique, pas d'étiquette de repérage.
4. N'afficher jamais un nom de police d'écriture (les indications de lettrage sont des consignes, pas du texte à dessiner).
5. Ne dessiner aucun visage humain, sauf si la Brand DNA l'autorise explicitement. (Les animaux mignons en style illustré sont permis si le sujet s'y prête.)
6. Le nom de marque et le nom du porte-parole sont affichés exactement comme dans la Brand DNA, jamais traduits, jamais raccourcis, jamais déformés.
7. Aucune marque commerciale tierce.
8. Aucun chiffre ou prix inventé : uniquement ceux écrits dans le contenu de la page.
9. Aucun tiret cadratin, aucune barre oblique visible, aucun symbole de formatage.

## Specs techniques de génération

- Modèle : GPT Image 2 via l'API Kie.
- Format : 3:4 portrait (format livre numérique lu au mobile).
- Résolution : 1K.
- Une page = une image, générées page par page dans l'ordre.

## Rappel du déroulé

Brand DNA d'abord, puis cadrage de la problématique (clarifier si besoin), puis deep research sérieuse sur sources carrées, puis choix de l'angle et plan page par page, puis rédaction du contenu vrai et actionnable, puis assemblage des prompts (verrous en dernier), puis génération des images via Kie en GPT Image 2, 3:4, 1K, puis proposition d'assemblage PDF.
