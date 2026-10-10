# Modèles de génération

Le skill désigne des modèles, pas un fournisseur. Passe par le service ou le connecteur réellement disponible dans la session. Si des instructions propres au service utilisé sont installées ailleurs (un dossier ou un skill dédié), suis-les pour les noms exacts des champs, l'envoi des fichiers et le suivi des tâches. N'invente aucun identifiant de modèle, aucune route et aucun paramètre : vérifie-les dans la documentation actuelle du service avant la première génération.

## Les modèles et leur rôle

| Étape | Modèle | Réglages retenus |
|---|---|---|
| Image de départ de l'avatar (9:16 et 1:1) | **GPT Image 2** en édition depuis la référence de l'avatar ; **Soul** pour un nouveau casting fictif | 1K, 9:16 puis 1:1 de la même scène |
| Scènes vidéo de l'avatar (plein écran et écran partagé) | **Seedance 2.5** | image de départ (`@Image1`) + extrait de la voix off **en vidéo écran noir** (`@Video1`), prompt sans le texte, `generate_audio: true`, même ratio que l'image, durée de l'extrait, caméra verrouillée ; au montage, voix off d'origine |
| Images statiques, ronds d'infographie, images dramatiques | **GPT Image 2** | 1K ; 9:16, 1:1 ou 16:9 selon l'usage |
| Objets détourés | **GPT Image 2** | 1K, fond transparent, 1:1 |
| Animations éducatives | image de départ **GPT Image 2** (9:16, 1K) puis **MiniMax H3** image vers vidéo | 4 à 15 s, 768P ou 2K, ratio de l'image de départ |
| B-roll de secours | **MiniMax H3** texte vers vidéo | 9:16, 4 à 6 s, 768P |

Même logique que Hotline pour tout ce qui bouge : d'abord l'image de départ validée, ensuite la vidéo générée à partir de cette image.

## Seedance 2.5 pour l'avatar : ce qu'il faut savoir

- **Méthode du studio (règle de l'utilisateur, 2026-10-10)** : l'extrait de voix off ElevenLabs part en **vidéo écran noir** (`@Video1`, `reference_video_urls`), le prompt ne contient **ni le texte à dire ni consigne de rythme**, `generate_audio: true`. Les lèvres suivent alors la voix d'origine (écart mesuré ≤ 0,02 s). Au montage, le son Seedance est coupé et la voix off d'origine est posée telle quelle. Gabarit 2 de `prompts.md`, script `scripts/kie_seedance.py --voix-ecran-noir`.
- Durée d'un clip : celle de l'extrait, arrondie à la seconde supérieure (4 s minimum ; au-delà de 30 s, couper à une pause). Une seconde de trop et Seedance invente des mots à la fin. Un passage plus court que 4 s est allongé avec des marges d'audio (script `couper_audio.py --min 4`).
- Ratios utiles : 9:16 (plein écran) et 1:1 (écran partagé). Résolution choisie par l'utilisateur à chaque projet (règle du studio).
- **Coût** : KIE facture la vidéo de référence en plus du clip, au tarif « avec vidéo » : (durée de l'extrait + durée du clip) x 17 cr/s en 480p, 38 cr/s en 720p, 95 cr/s en 1080p. Sans vidéo de référence (ancienne méthode) : 28, 63 et 158 cr/s.
- **Balises** : `@Image1` (image de départ), `@Video1` (écran noir), dans l'ordre d'envoi. « Image 1 » écrit en texte libre n'est pas relié au fichier.
- Image de départ : sur KIE, première image imposée et références audio ou vidéo s'excluent. Donne l'image de départ comme image de référence (`@Image1`) et écris dans le prompt qu'elle est la première image exacte et la seule référence d'identité.
- Clip test obligatoire au premier passage d'une configuration (5 à 8 s) : identité, cadre, micro, image non assombrie par l'écran noir, écart lèvres / voix avec `scripts/comparer_synchro.py`, silences bouche fermée. Tant qu'il n'est pas validé, ne lance pas la série.
- Réglages qui fonctionnent : notés dans `_config/charte.json` et réutilisés tels quels.
- **Historique des tests (ne plus utiliser ces méthodes)** :
  - 2026-09-28 : voix en référence audio `@Audio1` + texte exact dans le prompt : la voix Seedance imite l'extrait mais à son propre rythme, retard de 0,3 à 1 s ; timeline mot à mot dans le prompt : pas mieux. Audio en simple référence avec `generate_audio: false` : lèvres non synchronisées. Volcengine lip sync après coup : rendu peu naturel. Kling AI Avatar : moins réaliste, sous-titres parasites.
  - 2026-10-08 : « lier explicitement l'audio à la parole » : retard jusqu'à 0,92 s ; écran noir mais texte et consignes de rythme dans le prompt : synchro parfaite sur 5 mots puis dérive jusqu'à 0,80 s.
  - 2026-10-10 : écran noir + prompt sans texte (astuce relevée sur X) : écart moyen 0,01 s, max 0,02 s. Retenu.

## Avant de payer

- Liste des générations prévues : clips avatar (nombre et secondes), images, objets détourés, animations (nombre et secondes), b-rolls de secours.
- Estimation si le tarif est connu ; sinon génère un seul élément, lis le coût réel, puis extrapole et annonce le total.
- Vérifie que chaque référence nommée dans un prompt (`@Image1`, `@Video1`…) a réellement été envoyée, dans le même ordre. Un chemin local ne vaut pas un fichier téléversé.
- Une demande de prompts ou de découpage n'autorise pas une génération payante.

## Journal

`journal_generations.md` dans le dossier de la vidéo, une ligne par tâche : plan ou clip, version, modèle, prompt exact, références envoyées, réglages, identifiant de tâche, statut, coût, fichier obtenu, défauts observés. Un délai dépassé ne prouve pas l'échec : vérifie le statut avant de relancer. Corrige le défaut ciblé, réutilise les résultats valides, garde les originaux (`_v1`, `_v2`).

## Dépannage

| Symptôme | Correction |
|---|---|
| Identité de l'avatar qui dérive | joindre 2 à 3 photos de référence, rappeler « identity strictly preserved », repartir de l'image de départ validée |
| Clip avatar qui ne démarre pas sur l'image de départ | renforcer « @Image1 is the exact first frame », raccourcir le clip, relancer uniquement ce clip |
| Mot mal prononcé dans la voix Seedance | sans importance : la voix Seedance est remplacée par la voix off d'origine au montage |
| Lèvres décalées ou qui bougent pendant un silence | vérifier que le prompt ne contient pas le texte à dire, que la voix part bien en `@Video1` (pas `@Audio1`), que la durée du clip colle à l'extrait ; « mouth closed and still before the first word and after the last word of @Video1 » ; en dernier recours, recalage mot par mot (`montage-controle.md`, section « Secours ») |
| Mots ajoutés à la fin du clip | durée du clip trop longue : la ramener à la durée de l'extrait, et couper le clip à cette durée au montage |
| Image assombrie | rappeler « Ignore its picture completely » pour `@Video1` |
| Geste qui boucle ou mains devant la bouche | intention de geste unique et datée, « hands below the microphone », « no repetitive gesture loop » |
| Texte parasite dans une image | « no text, no letters, no numbers » et régénérer |
| Fond transparent absent | vérifier 1K et l'option fond transparent |
| Animation H3 qui change de sujet | moins d'étapes, « keep exactly the same subject », image de départ plus simple |
