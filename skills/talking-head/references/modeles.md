# Modèles de génération

Le skill désigne des modèles, pas un fournisseur. Passe par le service ou le connecteur réellement disponible dans la session. Si des instructions propres au service utilisé sont installées ailleurs (un dossier ou un skill dédié), suis-les pour les noms exacts des champs, l'envoi des fichiers et le suivi des tâches. N'invente aucun identifiant de modèle, aucune route et aucun paramètre : vérifie-les dans la documentation actuelle du service avant la première génération.

## Les modèles et leur rôle

| Étape | Modèle | Réglages retenus |
|---|---|---|
| Image de départ de l'avatar (9:16 et 1:1) | **GPT Image 2** en édition depuis la référence de l'avatar ; **Soul** pour un nouveau casting fictif | 1K, 9:16 puis 1:1 de la même scène |
| Scènes vidéo de l'avatar (plein écran et écran partagé) | **Seedance 2.5** | image de départ + extrait de la voix off, 1080p, même ratio que l'image, 4 à 30 s, caméra verrouillée |
| Images statiques, ronds d'infographie, images dramatiques | **GPT Image 2** | 1K ; 9:16, 1:1 ou 16:9 selon l'usage |
| Objets détourés | **GPT Image 2** | 1K, fond transparent, 1:1 |
| Animations éducatives | image de départ **GPT Image 2** (9:16, 1K) puis **MiniMax H3** image vers vidéo | 4 à 15 s, 768P ou 2K, ratio de l'image de départ |
| B-roll de secours | **MiniMax H3** texte vers vidéo | 9:16, 4 à 6 s, 768P |

Même logique que Hotline pour tout ce qui bouge : d'abord l'image de départ validée, ensuite la vidéo générée à partir de cette image.

## Seedance 2.5 pour l'avatar : ce qu'il faut savoir

- Durée d'un clip : 4 à 30 s. Un passage d'avatar plus long est coupé en deux clips à une pause ; un passage plus court est allongé avec des marges d'audio (script `couper_audio.py --min 4 --max 30`).
- Ratios utiles : 9:16 (plein écran) et 1:1 (écran partagé). Résolution 1080p pour que les zooms B et C restent nets.
- Voix : l'extrait de la voix off est fourni en référence audio (2 à 30 s). Le modèle ne doit pas inventer une autre voix. Le son du clip est de toute façon coupé au montage : seule compte la synchro des lèvres.
- Image de départ et audio de référence : selon l'interface, ces deux modes peuvent s'exclure. Dans ce cas, donne l'image de départ comme image de référence, et écris dans le prompt qu'elle est la première image exacte et la seule référence d'identité (gabarit 2 de `prompts.md`).
- Clip test obligatoire au premier passage d'une configuration (5 à 8 s) : identité, cadre, micro, lèvres syllabe par syllabe, silences bouche fermée. Tant qu'il n'est pas validé, ne lance pas la série.
- Réglages qui fonctionnent : notés dans `_config/charte.json` (mode utilisé, formulation du prompt, génération du son activée ou non) et réutilisés tels quels.

## Avant de payer

- Liste des générations prévues : clips avatar (nombre et secondes), images, objets détourés, animations (nombre et secondes), b-rolls de secours.
- Estimation si le tarif est connu ; sinon génère un seul élément, lis le coût réel, puis extrapole et annonce le total.
- Vérifie que chaque référence nommée dans un prompt a réellement été envoyée. Un chemin local ou un mot comme « Image 1 » ne vaut pas un fichier téléversé.
- Une demande de prompts ou de découpage n'autorise pas une génération payante.

## Journal

`journal_generations.md` dans le dossier de la vidéo, une ligne par tâche : plan ou clip, version, modèle, prompt exact, références envoyées, réglages, identifiant de tâche, statut, coût, fichier obtenu, défauts observés. Un délai dépassé ne prouve pas l'échec : vérifie le statut avant de relancer. Corrige le défaut ciblé, réutilise les résultats valides, garde les originaux (`_v1`, `_v2`).

## Dépannage

| Symptôme | Correction |
|---|---|
| Identité de l'avatar qui dérive | joindre 2 à 3 photos de référence, rappeler « identity strictly preserved », repartir de l'image de départ validée |
| Clip avatar qui ne démarre pas sur l'image de départ | renforcer « Image 1 = exact first frame », raccourcir le clip, relancer uniquement ce clip |
| Lèvres décalées ou qui bougent pendant un silence | extrait audio plus court, timeline mot à mot dans le prompt, « mouth closed and still during silences » |
| Geste qui boucle ou mains devant la bouche | intention de geste unique et datée, « hands below the microphone », « no repetitive gesture loop » |
| Texte parasite dans une image | « no text, no letters, no numbers » et régénérer |
| Fond transparent absent | vérifier 1K et l'option fond transparent |
| Animation H3 qui change de sujet | moins d'étapes, « keep exactly the same subject », image de départ plus simple |
