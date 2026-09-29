# Brique ALIGNEMENT (CRÉATION FULL B-ROLL ARTISTE)

Quatre scripts Python 3.11, CPU seulement, qui transforment une voix off française et son script en fichiers `work/words.json`, `work/features.json` et `work/beats_draft.json` (contrats sections 1, 2 et 3 de `CONTRACTS.md`). Le module `broll_common.py` (tokenisation, décodage ffmpeg, nombres en français) est partagé par les quatre et doit rester dans le même dossier.

## Installation

Prérequis : `ffmpeg` et `ffprobe` dans le PATH, accès à pypi.org et huggingface.co (téléchargement des modèles au premier lancement).

```
pip install --break-system-packages -U "setuptools>=70" wheel
pip install --break-system-packages -r scripts/requirements-align.txt
```

Note sur `ctc-forced-aligner` : la version 1.0.2 de PyPI compile une petite extension C++ avec `setup.py`. Sur Ubuntu, le setuptools système (68.x) fait échouer le build avec `AttributeError: install_layout`. Il faut d'abord mettre setuptools à jour (première ligne ci-dessus, avec `--ignore-installed` si pip refuse de désinstaller le paquet Debian). La bibliothèque n'a pas besoin de torch : elle utilise onnxruntime et télécharge le modèle MMS forced aligner en ONNX (1,26 Go) dans `~/ctc_forced_aligner/model.onnx`. Chemin modifiable avec `--ctc-model`.

Modèles faster-whisper : `Systran/faster-whisper-small` (environ 480 Mo), `medium` (1,5 Go), `large-v3` (3 Go), mis en cache dans `~/.cache/huggingface`.

## Ordre d'exécution

Depuis le dossier du projet (celui qui contient `voix.mp3` et `script.txt`), tous les chemins sont relatifs :

```
# 0. optionnel : resserrer les silences AVANT l'alignement
python3 scripts/tighten_vo.py voix.mp3 --out work/vo_tight.wav --max-pause 0.5 --keep 0.25
#    puis utiliser work/vo_tight.wav à la place de voix.mp3 dans TOUTES les étapes suivantes

# 1. alignement mot à mot (le script est la vérité du texte)
python3 scripts/align.py voix.mp3 script.txt --out work/words.json

# 2. mesures acoustiques
python3 scripts/audio_features.py voix.mp3 work/words.json --out work/features.json

# 3. proposition mécanique de beats (profil ADS ou EDU)
python3 scripts/propose_beats.py work/words.json work/features.json --profile ADS --out work/beats_draft.json
```

Chaque script affiche `--help`, écrit ses messages sur stderr et retourne un code non nul en cas d'échec (fichier absent, ffmpeg en erreur, aucune méthode d'alignement disponible, incohérence interne).

## align.py

`align.py AUDIO SCRIPT.txt --out work/words.json [--method auto|ctc|whisper] [--model small|medium|large-v3] [--language fr] [--numbers fr|be] [--no-snap] [--ctc-model CHEMIN]`

Étapes : conversion de l'audio en wav 16 kHz mono (écrit à côté du fichier de sortie, `work/<nom>_16k.wav`), tokenisation du script, alignement, interpolation des mots manquants, recalage des frontières sur l'énergie, contrôle de monotonie, écriture du JSON.

Cascade `--method auto` (défaut) :

1. `ctc` : alignement forcé avec ctc-forced-aligner (modèle MMS, ONNX). Chaque mot est transcrit en lettres latines prononcées (accents retirés, nombres et symboles épelés en français : "97" devient "quatre-vingt-dix-sept", "%" devient "pour cent", "12€" devient "douze euros", "1er" devient "premier"), un jeton `<star>` entre chaque mot absorbe les silences. Le `score` est la probabilité moyenne des trames de lettres du mot (0 à 1).
2. `whisper` : si ctc n'est pas installé ou échoue. faster-whisper (int8, beam 5, `word_timestamps=True`) transcrit, puis les mots reconnus sont réconciliés avec ceux du script par Needleman-Wunsch sur des atomes normalisés (sans accents ni casse, "97%" devient les atomes "97" et "%", "c" + "'est" est recollé en "c'est"). Un appariement est accepté si la similarité difflib est au moins 0,6. Les mots du script non appariés reçoivent des timestamps interpolés entre voisins appariés, au prorata de leur longueur, avec `score` null.

Correction du biais whisper : quand la méthode est whisper, un décalage global est estimé en cherchant le décalage (à 10 ms près, plus ou moins 350 ms) qui maximise la part de parole dans le coeur (60 % central) de chaque mot. Il n'est appliqué que si le gain est net (au moins 0,05) : c'est le cas de large-v3 (mots 150 à 300 ms trop tôt), pas de small ni medium dont les erreurs sont mot à mot.

Recalage sur l'énergie (désactivable avec `--no-snap`) : enveloppe RMS au pas de 10 ms, seuil adaptatif (plancher p10 plus 35 % de l'écart au niveau de parole p80). Une frontière posée dans un silence est ramenée à la parole, une frontière posée dans la parole est étendue d'au plus 60 ms. Entre deux mots qui se touchent, on ne bouge que si un silence d'au moins 40 ms existe à moins de 80 ms.

Règles de tokenisation (détaillées en tête de `broll_common.py`) : découpage sur les espaces ; **les élisions avec apostrophe forment un seul mot** ("l'eau", "c'est", "qu'une", "aujourd'hui") ; les mots composés avec trait d'union restent un mot ; un nombre est un mot ("20", "1,5", "97%") et un symbole isolé aussi ("%", "€") ; la ponctuation de queue va dans `punct_after` avec les valeurs fermées du contrat ("," "." "?" "!" ":" "..." ; ";" vaut ","), en gardant la plus forte si plusieurs ; guillemets, parenthèses et tirets isolés ne sont pas des mots. `script_hash` est le sha1 des mots normalisés joints par des espaces.

`duration_s` est la durée réellement décodée par ffmpeg (sur un mp3, `ffprobe` annonce souvent 50 à 70 ms de plus à cause du padding de l'encodeur).

Un avertissement est affiché quand au moins 3 mots ont un score inférieur à 0,05 : c'est le signe habituel d'un script qui ne correspond pas exactement à la voix (phrase non enregistrée, mot changé). Les mots en trop sont alors tassés dans le silence le plus proche, les mots voisins restent corrects.

## audio_features.py

`audio_features.py AUDIO work/words.json --out work/features.json [--pause-min 0.18] [--hop 0.05]`

- `pauses` : pour chaque paire de mots voisins, plus long silence RMS (pas 10 ms, seuil adaptatif) entre le début du premier et la fin du second ; retenu si la durée est au moins 0,18 s. `after_word_i` est le dernier mot qui commence avant le milieu du silence. Chercher entre le début du premier mot et la fin du second (et pas seulement dans le trou entre les deux) rend la détection robuste aux frontières whisper approximatives.
- `emphasis` : énergie RMS (dB) de chaque mot d'au moins 120 ms, comparée à la moyenne et à l'écart-type des mots voisins (fenêtre glissante de 15 mots) ; retenu si `z` dépasse 1,5. `t` est l'instant du pic d'énergie dans le mot (fenêtre 30 ms), utile pour caler un punch. Les mots de moins de 120 ms sont ignorés (articles, liaisons, énergie non significative).
- `energy.rms_db` : enveloppe RMS en dB, une valeur par pas de 0,05 s.
- `loudness_lufs` : `ffmpeg loudnorm print_format=json` (champ `input_i`), sinon pyloudnorm, sinon null.
- `speech_rate_wps` : nombre de mots divisé par la durée entre le début du premier mot et la fin du dernier (pauses comprises).

## propose_beats.py

`propose_beats.py work/words.json work/features.json --profile ADS|EDU --out work/beats_draft.json [--profiles CHEMIN]`

Le profil est lu dans `assets/profiles.json` (à côté du dossier `scripts`, chemin modifiable).

- Candidats de coupe (toujours après un mot) : ponctuation forte (`. ! ? : ...`) score 3, pause détectée score 2 plus un bonus selon sa durée, virgule score 1 (1,5 avec pause), connecteur en début de proposition (mais, parce que, et là, donc, alors, résultat, sauf que, en fait, du coup, bref) score 1,5. Les scores s'additionnent.
- Assemblage par programmation dynamique sur les frontières de mots : coût de durée (cible `shot.default.target`, plage `[min, max]`, pénalités au delà), coût de coupe décroissant avec le score du candidat, pénalité quand un beat enjambe une frontière forte (fin de phrase avec pause). Une coupe hors candidat coûte cher (`cut_reason` `duree_max`) et n'est jamais posée après un mot outil (article, préposition, pronom), devant un symbole ni entre un nombre et son unité.
- Les beats qui commencent avant 2,0 s utilisent les bornes `shot.HOOK` du profil.
- L'instant de coupe est `max(fin du mot, début du mot suivant moins 0,08 s)` : l'image change juste avant que le mot suivant soit entendu. Le premier beat commence à 0, le dernier finit à `duration_s`, les beats sont contigus.
- `suggested_split` : pour un beat plus long que `max`, liste des instants (secondes, 3 décimales) des sous-frontières proposées : une valeur si le beat fait au plus 2 fois `max`, deux valeurs sinon (séquence de 2 ou 3 plans). Les sous-frontières privilégient les candidats internes (virgules, connecteurs, petites pauses) tout en restant proches d'un découpage régulier.
- `energy` : z-score du RMS moyen du beat (enveloppe `features.energy`) combiné à 60 % avec le z-score du débit local (mots par seconde parlée) à 40 %, puis rangé de 1 à 5 par seuils (-1, -0,33, 0,33, 1).
- `cut_reason` : `pause`, `ponctuation`, `pause+ponctuation`, `connecteur`, `duree_max`. Pour le dernier beat, la raison est celle de la ponctuation finale.

## tighten_vo.py

`tighten_vo.py AUDIO --out work/vo_tight.wav [--max-pause 0.5] [--keep 0.25] [--threshold-db X] [--edges] [--map work/vo_tight_map.json]`

Détection des silences sur l'enveloppe RMS (pas 10 ms, seuil adaptatif ou fixé avec `--threshold-db`). Tout silence plus long que `--max-pause` est ramené à `--keep` secondes en retirant son milieu (on garde le début et la fin, donc les respirations restent naturelles). Chaque coupe reçoit un fondu de sortie et un fondu d'entrée de 10 ms. Les silences de début et de fin sont conservés sauf `--edges`. Sortie wav PCM 16 bits mono à la fréquence d'échantillonnage d'origine. `--map` écrit la liste des coupes (temps source, temps cible). À lancer avant `align.py` : les timestamps de `words.json` se rapportent au fichier réellement aligné, il faut donc utiliser `vo_tight.wav` partout ensuite (features, timeline, mixage).

## Temps mesurés ici (2 CPU, sans GPU, voix de 40,5 s)

| Étape | Temps |
|---|---|
| Conversion wav 16 kHz | 0,2 s |
| align.py ctc (modèle déjà téléchargé) | 18 à 21 s, dont 2,6 s de chargement et 15 à 18 s d'inférence |
| align.py whisper small | 12 s (1,7 s de chargement, 10 s de transcription) |
| align.py whisper medium | 33 à 37 s (10 s de chargement, 26 s de transcription) |
| align.py whisper large-v3 | 47 à 60 s (6,5 s de chargement, 50 s de transcription), 3,7 Go de RAM |
| audio_features.py | 1 s |
| propose_beats.py | moins de 1 s |
| tighten_vo.py | moins de 1 s |
| Premier lancement | plus le téléchargement du modèle ctc (1,26 Go) ou whisper small (480 Mo) |

Le temps d'inférence ctc croît linéairement avec la durée de l'audio (fenêtres de 30 s). Mémoire : environ 2,5 Go de RAM pour ctc (modèle fp32), 1 Go pour whisper small int8, 3,7 Go pour large-v3. Sur une machine à 7 Go, ne pas lancer large-v3 en parallèle d'un alignement ctc (un run de test a été tué par le noyau, OOM, dans ce cas).

## Précision mesurée

Sur la voix de test (Piper fr_FR-siwis-medium, 117 mots) :

- ctc contre whisper small : écart médian 40 ms sur les débuts et les fins de mots, moyenne 75 ms (débuts) et 58 ms (fins), 80 % des débuts à moins de 100 ms. Les gros écarts (jusqu'à 450 ms) sont du côté whisper : il colle les petits mots ("et", "il") au silence qui les précède et place mal les mots inconnus ("Eviclean", "97 %"). Contrôle sur l'enveloppe RMS : les frontières ctc tombent à 20 ms près sur les vraies attaques et fins de mots.
- ctc contre whisper medium : moyenne 49 ms (débuts) et 44 ms (fins), médiane 40 et 30 ms, 90 % des débuts à moins de 100 ms.
- ctc contre whisper large-v3 : les timestamps bruts de large-v3 sont en avance de 150 à 300 ms (défaut connu du modèle) ; la correction de décalage global (estimée sur l'énergie, appliquée seulement quand le biais est net) ramène l'écart moyen de 194 ms à 85 ms. large-v3 reconnaît mieux le texte (0 mot interpolé) mais place moins bien : pour l'alignement, small ou medium sont préférables en secours.
- Écoute-contrôle (5 fenêtres de 3 mots extraites avec ffmpeg et re-transcrites par whisper amorcé avec le script) : 5 sur 5 confirmées. Les fenêtres extraites sont dans `test/work/clips_controle/`.

Méthode retenue par défaut : ctc. Elle n'a pas besoin de reconnaître le texte (elle le sait), donc aucun mot n'est interpolé, les noms de marque et les chiffres sont placés aussi bien que les autres mots, et les pauses sont respectées. whisper reste en secours automatique et sert quand le script n'est pas fiable (2 mots interpolés sur 117 ici, "ta" et "étale").

## Limites

- Le script doit correspondre à la voix. Une phrase du script non enregistrée est tassée dans le silence voisin avec un score proche de 0 (avertissement affiché) ; une phrase enregistrée mais absente du script est absorbée par les jetons `<star>` en ctc, ou ignorée en whisper. Dans les deux cas, les mots voisins restent bien placés mais il faut corriger le script.
- Les nombres sont épelés en français de France par défaut ; `--numbers be` bascule sur septante et nonante (Belgique, Suisse) pour la méthode ctc. Les heures ("10h30"), fractions et formules chimiques ne sont pas verbalisées : le mot est aligné sur ses seules lettres, avec un score bas.
- ctc-forced-aligner 1.0.2 : modèle fp32 de 1,26 Go, 2,5 Go de RAM, environ 0,4 s de calcul par seconde d'audio sur 2 CPU. Le paquet compile une extension C++ à l'installation (setuptools récent obligatoire).
- whisper : le mode secours interpole les mots que le modèle n'a pas reconnus ; sur une voix bruitée ou très rapide, le nombre de mots interpolés monte et les timestamps de ces mots sont approximatifs (score null).
- `emphasis` dépend de la dynamique réelle de la voix. Sur une voix synthétique très plate, les mots retenus sont peu significatifs. Sur une voix humaine compressée en mastering, baisser éventuellement le seuil dans le code (`z_min`).
- `propose_beats.py` est une proposition mécanique : il ne connaît ni les sections (HOOK, PROB...) ni le sens. Claude affine ensuite.
- Aucun chemin absolu dans les scripts : le seul chemin par défaut est `assets/profiles.json` relatif au dossier `scripts`.
