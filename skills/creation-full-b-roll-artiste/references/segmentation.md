# Segmentation : de la voix off aux beats et aux plans

Objectif : transformer `work/beats_draft.json` (découpe mécanique) en `beats[]` du `brief.json`, c'est à dire des unités de sens avec une fonction narrative, un mot pivot et une liste de plans. C'est l'étape où la compréhension du texte compte le plus. Les scripts donnent les temps, toi tu donnes le sens.

## 1. Ce que le brouillon contient déjà

`propose_beats.py` a posé des frontières uniquement sur des frontières de mots, en privilégiant ponctuation forte + pause, et a visé la durée cible du profil. Chaque beat a `energy` (1 à 5, dérivée de l'intensité et du débit de la voix), `cut_reason` et parfois `suggested_split` (instants où couper un beat trop long en 2 ou 3 plans).

Ce brouillon est bon sur le rythme, aveugle sur le sens. Trois cas fréquents à corriger :

- Deux beats mécaniques portent la même idée visuelle (« Résultat, des traces, » puis « une odeur bizarre, ») : ce sont deux plans d'une même séquence, pas deux beats. Fusionne en un beat avec deux plans (`03a`, `03b`).
- Un beat contient un pivot d'idée au milieu (« Eviclean, c'est une feuille nettoyante qui se dissout dans l'eau en 3 secondes ») : le produit apparaît sur « Eviclean », le mécanisme sur « se dissout ». Coupe en deux beats à la frontière de mot la plus proche d'une pause, même petite.
- Une énumération courte (« Zéro plastique, zéro résidu, juste un sol vraiment propre ») : un beat, trois plans très courts (rythme en escalier), chacun calé sur son mot.

## 2. Sections et fonctions narratives

Découpe d'abord le script en sections (`sections[]`), puis attribue une `function` à chaque beat. Les sections sont des blocs contigus, les fonctions peuvent alterner à l'intérieur.

| Section | Fonctions typiques | Ce qu'on attend visuellement |
|---|---|---|
| HOOK | HOOK, PROMESSE | Une image qui change dans la première seconde, le résultat ou la contradiction montrés d'emblée |
| PROB | PROBLEME, AGITATION | Le geste pénible, la conséquence visible, la frustration |
| MECA | MECANISME | Le « comment ça marche », souvent invisible à l'oeil : 3D, macro, schéma |
| PREUVE | PREUVE | Avant/après, chiffre, test, avis, démonstration réelle |
| PROD | PRODUIT, BENEFICE | Le produit en main, en usage, le résultat obtenu |
| OBJ | OBJECTION | La réponse à un doute (prix, sécurité, effort) |
| CTA | CTA | Le geste d'achat, l'écran, le produit qui arrive |
| CHUTE | CHUTE | La boucle refermée : même image que le hook, en mieux |

Grille de structure à vérifier (`script_diagnostic`) : hook de 1 à 3 s avec une promesse ; validation visuelle de la promesse dans les 10 premières secondes (une PREUVE ou un PRODUIT visible tôt) ; relance verbale ou visuelle toutes les 10 à 15 s ; CTA placé vers 60 à 70 % de la durée, jamais collé à la fin ; chute qui reprend les mots du hook. Quand le script ne respecte pas la grille, note-le dans `script_diagnostic.notes` et compense au montage (par exemple un plan PREUVE très tôt même si le texte n'en parle qu'à 20 s), sans réécrire la voix.

## 3. Le mot pivot

Chaque beat a un `pivot_word` : le mot que l'image doit « confirmer ». C'est presque toujours le nom concret ou le verbe d'action le plus fort (« serpillière », « se dissout », « 97 % », « clique »). Les mots appuyés par la voix (`features.emphasis`) sont des candidats prioritaires : la voix insiste, l'image insiste au même endroit.

Règle de calage : le plan qui porte le pivot commence 0,3 à 0,5 s avant `pivot_t` (le spectateur voit, puis entend la confirmation, comme le recommande la pratique du J-cut). Concrètement, si le pivot est le premier mot du beat, le plan commence à la fin du beat précédent moins 0,3 à 0,5 s, et tu raccourcis d'autant le plan précédent. `pivot_t` = `start` du mot pivot dans `words.json`.

C'est une cible, pas une contrainte du validateur. Repli quand la tête du beat (les mots avant le pivot) est trop courte pour faire un plan à part entière : le plan commence au début du beat, l'avance sur le pivot est alors plus grande que 0,5 s et c'est acceptable tant que l'image reste littéralement liée au texte lu pendant cette avance. Jamais de plan sous le minimum de sa section pour respecter le calage. Les frontières de beats peuvent donc s'écarter des frontières de mots (elles suivent les plans) ; c'est prévu.

## 4. Durées et séquences de 3 valeurs

Les bornes par section sont dans `assets/profiles.json` (`shot.<SECTION>.min/target/max`). Un beat plus long que `max` ne devient jamais un plan long : il devient une séquence de 2 ou 3 plans du même sujet, en changeant de valeur à chaque plan (large pour situer, moyen pour l'action, détail ou macro pour la matière). C'est la règle « tourne par séquences de 3 plans, jamais un plan isolé », transformée en automatisme. Utilise `suggested_split` comme point de départ, mais coupe de préférence sur une frontière de proposition ou une virgule.

Trois exceptions volontaires :

- Un plan PREUVE peut tenir la durée max entière quand il montre une transformation continue (une tache qui disparaît) : couper casserait la preuve.
- Un plan 3DSCI peut aller jusqu'à max si l'animation raconte une progression (les fibres qui capturent, puis relâchent).
- Dans le HOOK, préfère deux plans de 0,8 s à un plan de 1,6 s : l'image doit changer dans la première seconde.

Contrainte de relance : aucune fenêtre de `relance_max_s` (5 s en ADS, 8 s en EDU) sans changement de plan. Le validateur le vérifie.

## 5. Niveau d'abstraction et énergie

`abstraction` guide le choix du type de B-roll (voir `broll-direction.md`) :

- `concret` : la voix nomme un objet, un geste, un lieu visible.
- `consequence` : la voix décrit un état ou un résultat (propre, sale, doux, terne).
- `mecanisme` : la voix explique un fonctionnement invisible (molécules, fibres, couches de peau).
- `abstrait` : la voix parle d'une notion (temps, confiance, liberté, argent).
- `emotion` : la voix exprime ou provoque une émotion (ras-le-bol, soulagement, fierté).

`energy` vient du brouillon mais tu peux l'ajuster de ±1 selon le sens (une promesse chuchotée reste un moment fort). L'énergie pilote la valeur de plan par défaut (5 : détail ou macro très rapproché ; 1 : large calme), la présence de punch au montage et le choix de transition.

## 6. Contrôles avant d'écrire le brief

- Les plans couvrent l'audio de 0 à `duration_s` sans trou ni chevauchement (le dernier plan finit exactement à `duration_s`).
- Pas deux `value` identiques consécutives, pas deux `camera` identiques consécutives, y compris entre la fin d'un beat et le début du suivant.
- Le premier plan du HOOK dure au plus 1 s, ou bien un changement (punch, overlay) intervient avant 1 s.
- Aucun plan sous `min` de sa section (0,6 s en HOOK).
- Chaque `pivot_t` est dans son beat, et `pivot_word` est bien un mot du `text`.
- Les numéros de plans suivent l'ordre chronologique (`01`, `02a`, `02b`, `03`...), sans trou.

Puis lance `validate_brief.py` et corrige jusqu'à zéro erreur.

## 7. Option : resserrer la voix

Quand la voix off contient des silences longs, une vidéo full B-roll paraît s'arrêter, même avec l'image qui bouge. `tighten_vo.py` compresse ces silences. Ordre pratique : aligne d'abord la voix d'origine (c'est `features.pauses` qui révèle les pauses), propose le resserrage seulement si une pause dépasse 0,7 s ou si plusieurs dépassent 0,5 s sans tomber sur une coupe de plan (une pause rhétorique de 0,5 s qui coïncide avec un changement d'image est un atout, pas un défaut). Si l'utilisateur accepte, lance `tighten_vo.py --max-pause 0.7`, puis REFAIS alignement, features et beats sur `work/vo_tight.wav`, qui devient `audio.file` du brief.
