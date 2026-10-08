---
name: zack-d-style
description: "ZACK VIDEO LA CUISINE — produit une pub vidéo complète au format Zack D. Films (monde bleu quadrillé, semi-3D Pixar, personnage-ancre, coupes anatomiques macro, une caméra continue avec transitions dessinées, 9:16) pour N'IMPORTE QUELLE marque et N'IMPORTE QUEL utilisateur : Brand DNA → script explicatif « voilà ce qui se passe dans ton corps » (une ligne = un plan) → VO faite par l'utilisateur (TTS au choix) → calage Whisper → plate + character sheet + bloc macro → storyboard → stills (modèle image KIE au choix, défaut gpt-image-2) → validation → clips chaînés start/end (modèle vidéo au choix : KIE Kling 3.0 pro par défaut, ou tout endpoint FAL image-to-video) → dossier de montage + SRT. Deux recettes : NORMAL (5 s/plan) ou SPEEDY (3 s/plan). Déclenche dès qu'on dit « Zack D », « vidéo Zack D », « vidéo Zack », « style Zack D. Films », « explique le mécanisme en animation », « monde bleu quadrillé »."
---

# ZACK VIDEO LA CUISINE — pub Zack D. Films, toute marque, tout utilisateur, tout modèle

Process validé sur deux marques (dermato 05/09/26, boisson 16/09/26). Rien n'est en dur : marque, personnage, mécanisme, langue, modèles et clés viennent de l'utilisateur.

## Adaptation au studio (prime sur le reste du skill)
- **Nom du concept** : « Zack D ». Créas finales dans `creas/zack-d-style/`, numérotées via `creas/registre.md`.
- **Dossier du run** : `runs/AAAA-MM-JJ_<marque>-<sujet>_zack-d/` (pas `<marque>/EDITING/zack/`). `jobs/` reste un sous-dossier direct du run.
- **Clés** : jamais de `.keys.json` ni `.kie_key`. Charger `set -a; . ./.env; set +a` à la racine du studio : les scripts lisent `KIE_API_KEY` dans l'environnement. Ne jamais afficher la clé.
- **Résolution** : avant le setup et avant les clips, demander la résolution de chaque média avec modèle et coût (images gpt-image-2 : 1K 6 cr, 2K 10 cr, 4K 16 cr ; clips Kling 3.0 sans son : std 720p 14 cr/s, pro 1080p 18 cr/s, 4K 67 cr/s). Le choix est écrit dans `run.json` (`image.resolution`, `video.mode`) ; `zack_img.py` lit `image.resolution`.
- **Calage** : MMS d'abord (préférence de l'utilisateur) : `skills/creation-full-b-roll-artiste/scripts/align.py VO.mp3 SCRIPT-FR-tts.txt --out mots_mms.json --method ctc --language fr`, puis `scripts/align_vo_mms.py <run> mots_mms.json SCRIPT-FR.txt` → `shots_timing.json`. `align_vo.py` (Whisper) reste le secours.
- **Script fourni par l'utilisateur** : si le script et la VO arrivent ensemble, ne pas réécrire le script ; le couper en lignes (une ligne = un plan) aux virgules et points, sans changer un mot.
- **« Cale la voix off sur les plans »** : l'utilisateur veut la vidéo montée. Livrer `EXPORTS/MONTAGE/APERCU-recale-avec-VO.mp4` comme version de travail, puis la vidéo finale (SRT incrusté seulement s'il le demande).
- **Montrer au lieu de `open`** : chaque contrôle passe par SendUserFile (planche des stills, puis clips), validation explicite avant chaque étape payante.
- **Produit** : s'il n'y a pas de produit de la marque dans le script, les objets génériques (pot d'huile, flacon) restent sans marque et sans texte.
- **Brand DNA** : lire `Claire/BRAND-DNA-CLAIRE.md` pour Claire ; signaler à l'utilisateur toute affirmation santé du script qui sort du Brand DNA, sans la réécrire d'office.
- **Bibliothèque** : consulter `bibliotheque/` avant de générer (règle du studio) ; enregistrer les clips retenus après le montage (`origine` IA).

## 0. Intake — à poser AVANT tout, en une liste courte
1. **La marque** : Brand DNA collé ou dossier de marque, sinon 5 lignes (produit, mécanisme / cause du problème, persona, promesse, ce qu'on n'a pas le droit de dire). **Photo réelle du produit** (jamais regénérée).
2. **Langue** du script et de la VO (le script est d'abord livré dans la langue de lecture de l'utilisateur pour validation, puis dans la langue du marché).
3. **Recette** : NORMAL (plans 4-5 s, ~18-20 plans / 80 s, posé) ou SPEEDY (plans ~3 s, ~32-36 plans / 80 s, une transition toutes les 3 s). Si la VO est déjà là, son rythme décide (≤ 3,5 s par ligne = speedy).
4. **Persona** : homme / femme, âge, tenue, accessoire. Une fiche personnage unique pour tout le run.
5. **Modèles** : l'utilisateur colle le **lien KIE ou FAL du modèle** qu'il veut pour les images et pour la vidéo. S'il ne colle rien → **défaut = gpt-image-2 (KIE) pour les stills et Kling 3.0 pro (KIE) pour les clips**, ce sont les modèles du process validé.
6. **Clés** : `<run>/.keys.json` → `{"kie": "...", "fal": "..."}` (KIE obligatoire : images + upload ; FAL seulement si le modèle vidéo est un endpoint FAL). Jamais affichées, jamais dans le skill.
Écrire dans `<run>/run.json` : `{"brand","recipe":"normal|speedy","lang","vo":"VO.mp3","script":"SCRIPT-<LANG>.txt","product_ref":"<photo>.png","image":{"model":"gpt-image-2"},"video":{"provider":"kie|fal","model":"kling-3.0/video","mode":"pro"}}`.

## 0 bis. Prérequis machine
`python3`, `ffmpeg` + `ffprobe`, `curl`, `pip install faster-whisper` (calage ; modèle `small` / `small.en`, ~500 Mo au 1er run), un compte KIE (kie.ai) avec crédits, un compte FAL si provider = fal, un TTS au choix pour la VO (ElevenLabs, Fish Audio…). Test : `ffmpeg -version && python3 -c "import faster_whisper"`.

## 1. Ce qui ne change jamais
- **Format Zack** : monde bleu quadrillé (plate `references/PLATE-grid.png`, réutilisable telle quelle ; jamais le mot « stage » dans un prompt), semi-3D Pixar-cute, **un sujet par frame**, personnage-ancre plein pied (character sheet), trois échelles A dehors / B prop island / C macro cutaway, un seam ne saute jamais deux niveaux (A→B→C→B→A).
- **L'utilisateur fait la VO** à partir du script livré en **un seul bloc sans saut de ligne** (les sauts de ligne créent des pauses dans les TTS). Il envoie le MP3.
- **L'utilisateur monte lui-même** : on livre un dossier de clips + fiche, jamais un master. Il gère la vitesse.
- **Chaîne start/end** : still de fin du clip N = still de début du clip N+1. Changer 1 still = regénérer 2 clips. **Tous les stills sont validés avant le premier clip.**
- **Go explicite avant chaque étape payante** (setup + stills ≈ 2 $, clips ≈ 9-10 $ pour 80 s).
- **Aucun fait de marque inventé** : claims, chiffres, garantie viennent du Brand DNA. Un claim non sourcé est livré mais flaggé.
- Pas de musique ni de sous-titres ajoutés (le SRT est fourni à part). `open` du dossier, jamais d'un mp4.

## 2. Déroulé
1. **Script** (langue de lecture) : angle pris dans le Brand DNA. Registre Zack : phrases courtes, présent, cause → effet, « voilà ce qui se passe dans ton corps », **une ligne = un plan** (20 lignes ≈ normal 80 s ; 24-28 lignes ≈ speedy 80 s). Le mécanisme est vulgarisé avec une image concrète (une serrure, une usine, une colonie…) qui devient le bloc macro. Le produit entre aux 2/3, nommé. Nombres en toutes lettres pour le TTS.
2. **Script langue du marché** en deux fichiers : `SCRIPT-<LANG>.txt` (une ligne par plan) et `SCRIPT-<LANG>-tts.txt` (un seul bloc). → l'utilisateur fait la VO.
3. **Calage** : `scripts/align_vo.py <run> VO.mp3 SCRIPT-<LANG>.txt <lang>` → `shots_timing.json` (début/fin de chaque ligne). Vérifier `mots non alignés: 0` ; match ≥ 0,9 en anglais, ≥ 0,6 acceptable dans les autres langues (modèle `small`).
4. **Setup** (`jobs/setup.json` via `scripts/zack_img.py`) : plate réutilisée · **character sheet** plein pied (image-to-image depuis un buste ou une photo de référence + plate ; recette dans `references/PROMPTS.md`) · **bloc macro** (le cube de coupe du mécanisme : peau + follicule, cerveau + serrures, intestin…). Contrôle visuel des 2-3 images.
5. **Storyboard** (`references/STORYBOARD.md`) : beat par beat avec temps VO, shot type (podium / prop island / macro cutaway / data object), angle varié, action en un verbe, couleur-état, seam-out. Speedy : ligne > 3,5 s coupée en 2 beats à une virgule (still `Sxxb`).
6. **Stills** : `jobs/stills.json` (refs dans l'ordre plate · PRODUIT en 2e · perso · bloc), lancés **en parallèle, 1 process par still, `sleep 1` entre deux**. Contrôle de chaque image en pleine résolution : identité, tenue, mains, produit lisible, aucun texte parasite, pas de plateau/scène. Rejets dans `jobs/_rejets/`, regénération par nom. → `open jobs/OUT` → validation → **go**.
7. **Clips** : `jobs/legs.json` (`name,start,end,vo_start,vo_end,target_s,duration,prompt`, prompt = *Camera motion* + *Subject motion* séparés + la queue « One continuous camera move… No captions. No text. »).
   - provider **kie** : `scripts/zack_clip.py jobs/legs.json <name>` en parallèle (1 process par clip, `sleep 1`). Défaut `kling-3.0/video` mode pro, `duration` entier 3-15, `image_urls:[start,end]`.
   - provider **fal** : `scripts/gen_clip_fal.py jobs/legs.json --par 6` (défaut `minimax/h3-max-turbo/image-to-video`, ou l'endpoint collé ; durée mini 5 s : le script retombe à 5 s si la durée est refusée).
8. **Livraison** : `scripts/make_delivery.py <run>` → `EXPORTS/MONTAGE/` (clips bruts nommés par ligne, clips recalés à la durée VO à titre indicatif, `FICHE-MONTAGE.txt`, VO, aperçu bout à bout). → `open EXPORTS/MONTAGE`.
9. **SRT** : quand l'utilisateur envoie son montage : `scripts/make_srt.py <montage.mp4> SCRIPT-<LANG>.txt <out.srt>` (blocs 2-5 mots, texte = le script, jamais Whisper brut).

## 3. Arborescence d'un run
```
<marque>/EDITING/zack/<vN>/
  run.json · .keys.json · SCRIPT-<LANG>.txt · SCRIPT-<LANG>-tts.txt · VO.mp3 · shots_timing.json · words_*.json · STORYBOARD.md
  jobs/setup.json · jobs/stills.json · jobs/legs.json · jobs/OUT/ (CHAR-sheet, M-<bloc>, S01…, L01…) · jobs/_rejets/ · jobs/logs/
  EXPORTS/MONTAGE/ (clips-bruts, clips-recales-VO, FICHE-MONTAGE.txt, VO, APERCU)
```
`jobs/` doit être un sous-dossier direct du run (les scripts remontent d'un cran pour lire `run.json` et les clés).

## 4. Montage (ce que l'utilisateur fait avec `EXPORTS/MONTAGE`)

**Version rapide** : `EXPORTS/MONTAGE/APERCU-recale-avec-VO.mp4` est déjà une vidéo complète (tous les clips recalés bout à bout, audio dessus, 1080×1920). Pour publier vite : prendre ce fichier, ajouter la musique et éventuellement les sous-titres, exporter. Le montage manuel ci-dessous sert seulement à ajuster une vitesse, ajouter un CTA ou remplacer un clip.
1. Projet 9:16 (1080×1920, 30 fps). VO en tête de timeline.
2. Clips `clips-recales-VO/` posés bout à bout dans l'ordre des numéros : déjà calés sur la VO, le bout à bout tombe juste. Sinon partir des `clips-bruts/` et régler la vitesse avec le facteur de `FICHE-MONTAGE.txt`.
3. Ne jamais couper la **fin** d'un clip (le tableau suivant est dedans) : accélérer à la place. Speedy : les lignes < 2 s demandent ×1,5-2, c'est normal.
4. Pas de transition ajoutée (les clips s'enchaînent déjà par le mouvement caméra). Sous-titres (SRT fourni), CTA : au choix. Export H.264 1080×1920.
5. **Musique** : le format Zack utilise un fond léger et rythmé. Référence du process : « Hide and Sneak » de The Fly Guy Five (catalogue **Epidemic Sound**, licence par abonnement : le fichier n'est pas fourni avec le skill, chaque utilisateur le télécharge avec son propre compte ou prend un équivalent : instrumental joueur, pizzicato / claps, ~110 bpm, sans voix). Posée par l'utilisateur au montage, à -18 dB sous la VO.

## 5. Pièges connus (payés)
- **Produit ignoré** quand il y a 3 refs : la photo produit doit être la **2e ref** et nommée dans le prompt (« the SECOND attached image is the product photo… exact copy, label legible, facing camera »), négatif « no blank label, no unbranded <objet> ».
- **Mauvais personnage** sur un still sans la fiche perso : tout still où le perso apparaît, même minuscule, attache la fiche (« the tiny woman/man is exactly the character in the attached character sheet »).
- **Accessoires** de la fiche (casquette…) : à retirer explicitement (prompt + négatif) sur les stills où il ne les porte pas. Continuité tenue = même verrou de tenue dans chaque prompt.
- **Macro qui redevient un plein pied** : sur une macro de peau/zone du perso, ne pas attacher la fiche ; attacher le still précédent et écrire « no face, no torso ».
- **Objets porteurs de texte** (enseignes, écrans avec UI, étiquettes) → texte parasite. Les chiffres autorisés = numéraux extrudés or avec le perso minuscule devant.
- gpt-image-2 2K : « Internal Error » aléatoire → le script retente puis replie en 1K. Filtre `nsfw` sur la peau rouge / gros plans : le retry passe en général.
- Kling : `duration` entier 3-15 ; deux images = [start, end] ; sans end = animation depuis le start seul (outro). Filtre copyright sur les noms de marque dans le **prompt vidéo** → prompt neutre (« the product »).
- Whisper dans une autre langue que l'anglais découpe les apostrophes (« c'est » → « c », « 'est ») et écrit les nombres en chiffres : la découpe des lignes longues doit matcher par préfixe / équivalents (`build_legs` du run de référence boisson).
- Un mp4 de 0 octet = téléchargement coupé → supprimer et relancer par nom.

## 6. Coût (tarifs KIE : 1 $ = 200 crédits · Kling 3.0 pro 18 cr/s = 0,09 $/s · gpt-image-2 2K = 0,05 $/image)
NORMAL (18 clips × 5 s + ~28 images) ≈ 9,50 $ · SPEEDY (34 clips × 3 s + ~50 images) ≈ 11,70 $. FAL H3 Max Turbo ≈ 0,02 $/s en promo (clips 5 s mini). Solde KIE : `GET https://api.kie.ai/api/v1/chat/credit` (÷ 200 = $).

## 7. Arbre de décision
Intake (marque, langue, recette, persona, modèles, clés) → script langue de lecture → validation → script marché + bloc TTS → l'utilisateur envoie la VO → calage → setup (plate, fiche, bloc) → storyboard → **go** → stills en parallèle → contrôle → `open jobs/OUT` → validation → **go** → clips (kie ou fal) → livraison → `open EXPORTS/MONTAGE` → SRT sur le montage final → note mémoire marque.
