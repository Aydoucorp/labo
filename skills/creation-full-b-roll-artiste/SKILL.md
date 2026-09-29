---
name: creation-full-b-roll-artiste
description: "Skill à déclencheur unique. Utiliser uniquement quand l'utilisateur écrit la phrase exacte « création full b-roll artiste » (avec ou sans accents ou majuscules). Ne jamais le déclencher sur un autre mot clé, même pour un montage vidéo, un b-roll ou une shot list. Il transforme une voix off (audio) et son script en vidéo verticale full B-roll en deux temps : mode BRIEF (alignement mot à mot, segmentation en beats, choix du B-roll exact à chercher ou filmer pour chaque passage, shot list HTML interactive) puis mode MONTAGE (à partir des rushes nommés par ID : montage, sous-titres karaoké, mixage, rendu MP4, contrôle qualité)."
---

# CRÉATION FULL B-ROLL ARTISTE

L'audio commande. La voix off est la vérité du temps, le script est la vérité du texte, et chaque image doit confirmer ce que la voix dit à l'instant où elle le dit. Ce skill sert deux moments distincts d'un même projet, dans le même dossier.

Lis `CONTRACTS.md` (formats JSON) la première fois, puis les références au moment où tu en as besoin :

- `references/pipeline.md` : commandes exactes, installation, dépannage. À lire avant de lancer un script.
- `references/segmentation.md` : du brouillon mécanique aux beats avec fonction, mot pivot et plans.
- `references/broll-direction.md` : hiérarchie de choix du plan, types, liste noire, lookbook, requêtes, prompts IA.
- `references/shot-cards.md` : séquences prêtes par univers (maison, peau, hygiène, animal, preuve, CTA, 3D).
- `references/montage-rules.md` : grammaire des transitions, Ken Burns, punch, sous-titres, son, zones sûres.
- `references/sources.md` : banques gratuites et payantes, requêtes, 3D scientifique, génération IA.
- `references/qc.md` : ce que vérifie le contrôle qualité et ce que tu regardes toi-même.

## Quel mode ?

- L'utilisateur fournit une voix off et un script (pas de rushes) → **mode BRIEF**.
- Le dossier contient `brief.json` et des fichiers dans `rushes/` → **mode MONTAGE**.
- Il fournit voix, script et rushes d'un coup → BRIEF puis MONTAGE, en lui montrant la shot list entre les deux (les rushes manquants se voient tout de suite).
- Il veut retoucher une vidéo déjà rendue → édite `work/timeline.json` et relance le rendu (voir `pipeline.md` section 3), pas tout le pipeline.

## Paramètres à fixer avant de commencer

Demande ce qui manque, en une seule question groupée, et déduis le reste :

1. `profile` : `ADS` (publicité, 15 à 45 s) ou `EDU` (éducatif organique, 45 à 90 s). Si l'utilisateur ne le dit pas : ADS quand la voix dure moins de 45 s et nomme un produit avec un appel à l'action, EDU sinon. Le profil change les durées de plans, la fréquence des relances, la famille de transitions et la part de plans produit ; il ne change pas l'usage.
2. `platform` : tiktok par défaut (zones sûres les plus contraignantes), reels, shorts, youtube ou meta-feed.
3. Marque, produit, univers : ce qui doit apparaître à l'image et ce qui est interdit (concurrents, allégations).
4. Lookbook en 5 lignes (lumière, palette, décor, personnes, suffixe de style en anglais) : propose-le à partir de l'univers de la marque et fais-le valider en une phrase.
5. Sous-titres : par défaut karaoké mot à mot blanc avec contour, boîte rouge centrée pendant le hook. Autre style seulement sur demande, avec une référence visuelle.

Si l'utilisateur est absent ou pressé, choisis et écris tes hypothèses en tête de la réponse.

## Mode BRIEF, pas à pas

1. Crée `work/`, `out/`, `rushes/`.
2. Lance `align.py`, `audio_features.py`, `propose_beats.py` (commandes dans `pipeline.md`). Vérifie l'avertissement de score bas : s'il apparaît, le script ne correspond pas à la voix, corrige le script avec l'utilisateur avant d'aller plus loin. Si `features.pauses` montre une pause de plus de 0,7 s (ou plusieurs de plus de 0,5 s hors coupes), propose `tighten_vo.py` et, si accepté, refais ces trois étapes sur `work/vo_tight.wav`.
3. Lis le script en entier, puis `work/beats_draft.json`. Découpe en sections, attribue les fonctions narratives, choisis le mot pivot de chaque beat et cale les plans 0,3 à 0,5 s avant lui (`segmentation.md`). Transforme tout passage trop long en séquence de 2 ou 3 valeurs.
4. Pour chaque plan, applique la hiérarchie de `broll-direction.md` : littéral concret, conséquence visible, mécanisme (3DSCI ou MOTION), métaphore ancrée dans l'univers, réaction humaine. Renseigne type, valeur, caméra, description en une phrase, requêtes EN et FR, prompt IA image + motion, `must_show`, durée minimale du rush, fallback, nom de fichier `{id}_{section}_{type}_{slug}.mp4` (slug de 2 à 4 mots en ASCII sans accents, par exemple `03a_PROB_UGC_serpilliere-seau.mp4` ; l'utilisateur doit pouvoir le retaper). Pars des cartes de `shot-cards.md` quand l'univers correspond.
5. Écris `brief.json` (schéma `CONTRACTS.md` section 4), avec `script_diagnostic` (hook, validation de la promesse avant 10 s, CTA à 60 à 70 %, boucle fermée) et `shooting_plan` (plans UGC et PRODUIT regroupés par lieu).
6. `validate_brief.py brief.json --fix-slugs` jusqu'à zéro erreur, puis `build_brief.py` avec l'audio, les features et les words.
7. Livre `brief.html` et `brief.json`. Dans la réponse : la structure trouvée (sections et durées), le nombre de plans par type, ce que l'utilisateur doit filmer lui-même (résumé du plan de tournage), ce qui est généré (MOTION) et ce qui a un prompt IA prêt (3DSCI, IAGEN), la nomenclature de dépôt en une ligne, et les notes du diagnostic de script s'il y en a.

Ce qui fait la qualité d'un brief : au moins la moitié des plans en littéral concret ; aucun plan de la liste noire ; le produit filmé par l'utilisateur dès que la voix en parle ; le lookbook présent dans toutes les requêtes ; la promesse validée à l'image avant 10 s quand le texte le permet (sinon noté dans le diagnostic) ; le HOOK qui change d'image dans la première seconde ; la CHUTE qui reprend le cadrage du HOOK.

## Mode MONTAGE, pas à pas

1. `inventory.py` : lis `missing` et `substitutions`. Présente les manquants à l'utilisateur avec les trois options (déposer, substituer, remplacer par MOTION) et attends sa réponse s'il est là ; sinon applique les substitutions proposées et signale-le.
2. `best_window.py`, `prep_clips.py`, `make_captions.py`, `build_timeline.py` (avec `--music` si fourni). La grammaire de `montage-rules.md` est appliquée automatiquement : cuts par défaut, une famille de transitions aux changements de section, zoomthrough pour entrer dans la 3D, flash en sortie de hook, Ken Burns alterné sur les plans statiques, punch sur les mots appuyés, ambiance à -25 dB.
3. Rends d'abord des images de contrôle (`render.py --frames`) aux moments clés : milieu du hook, un mot de karaoké, une transition, un overlay. Regarde-les. Corrige la timeline si quelque chose cloche (transition trop voyante, texte hors zone sûre, sujet coupé par le recadrage).
4. Rendu final, puis `qc.py`. Score minimum 90 ; en dessous, applique les corrections du rapport et relance. Regarde la planche contact : chaque vignette doit correspondre à ce que la voix dit à cet instant (compare avec le brief).
5. Livre `out/final_9x16.mp4`, `out/final.srt`, `out/qc_report.md`, `out/contact_sheet.jpg`. Dans la réponse : durée, nombre de plans, transitions visibles utilisées, score QC, et les 2 ou 3 points que l'utilisateur devrait vérifier lui-même (par exemple un rush horizontal recadré, une substitution).

## Règles d'écriture des sorties

- Tout ce qui est destiné à l'utilisateur (brief, descriptions, rapport, réponse) est en français, sans tirets cadratins : virgules, points, parenthèses ou retours à la ligne.
- Les requêtes de recherche sont en anglais (`query_en`) et en français (`query_fr`) ; les prompts IA sont neutres vis à vis du fournisseur, les instructions propres à un fournisseur vivent hors du skill.
- Un plan que tu ne peux pas décrire honnêtement en une phrase concrète (« on voit une main qui... ») n'est pas prêt : reformule ou change de niveau dans la hiérarchie.
- N'invente jamais un avis client, un chiffre ou une preuve : si le script en cite, ils sont montrés en SCREEN ou MOTION à partir de ce que l'utilisateur fournit.

## Limites connues

- Alignement CPU : 20 s de calcul pour 40 s de voix ; rendu Remotion : environ 8 s par seconde de vidéo sur 2 CPU. Prévenir l'utilisateur pour une vidéo de 90 s (12 minutes de rendu).
- La détection de visage sert au recadrage 9:16 ; pour un sujet non humain décentré, fournir un rush vertical.
- La segmentation mécanique ne comprend pas le sens : ta relecture (étape 3 du mode BRIEF) n'est pas optionnelle.
- Le skill ne cherche pas et ne télécharge pas les rushes lui-même (banques et licences varient) ; il fournit les liens de recherche pré-remplis et les prompts.
