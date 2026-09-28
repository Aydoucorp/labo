# Montage (FFmpeg + Remotion) et contrôles

Le montage est fait par code : FFmpeg prépare et contrôle les médias, Remotion assemble et anime à partir d'un fichier `montage.json`. Le gabarit testé est dans `montage-remotion/` (Remotion 4.0.529, polices locales Montserrat et Playfair Display, licence OFL). Remotion est gratuit pour un particulier ou une entreprise de 3 salariés maximum.

## Mise en place (une fois par projet vidéo)

1. Copie `montage-remotion/` dans le dossier du projet, puis `npm install` (Node 18 ou plus).
2. Range les médias dans `public/` : `public/audio/voix.mp3`, `public/avatar/`, `public/broll/`, `public/edu/`, `public/images/`, `public/preuves/`, `public/detoures/`. Les chemins de `montage.json` sont relatifs à `public/`.
3. Normalise les vidéos : `bash <dossier du skill>/scripts/preparer_medias.sh dossier_source public/broll` (30 i/s, H.264, sans son). Même chose pour les clips avatar et les animations H3.
4. Rendu : `bash <dossier du skill>/scripts/rendre.sh <dossier_projet_montage>` lance le rendu en arrière-plan (log dans `out/rendu.log`, fin signalée par `out/FINI`). Sur une petite machine, compte environ 20 s de calcul par seconde de vidéo en 1080 x 1920 : ne bloque pas la conversation, vérifie le log régulièrement. Un brouillon rapide : ajoute `--scale=0.5`.
5. Une image fixe pour vérifier un moment : `npx remotion still src/index.js Main out/t.png --props=montage.json --frame=<image>`.
6. Si Chromium n'est pas trouvé, passe `--browser-executable=<chemin>` ; le script cherche d'abord `/opt/pw-browsers/`.

## Voix hybride (recette validée)

Les clips avatar portent leur propre voix (générée par Seedance, lèvres synchrones). La piste voix du montage est donc reconstruite :

1. Pour chaque clip avatar retenu : bornes de parole mesurées sur son son (`ffmpeg -af silencedetect=n=-40dB:d=0.15`, plus Whisper pour repérer une respiration prise pour un mot), marge de 0,12 s avant et 0,16 s après.
2. Pour chaque passage illustré : extrait de la voix off d'origine coupé dans ses silences (`mots.json`).
3. Morceaux mis bout à bout dans l'ordre du script, chacun ramené à -18 LUFS, fondus de 20 à 30 ms ; la piste obtenue devient `audio` dans `montage.json` et tous les temps sont recalculés sur elle (clip avatar : `clipStart` = début du morceau moins l'entrée coupée dans le clip).
4. Sous-titres : texte du script, temps de l'audio (Whisper sur les clips avatar) ; une nouvelle ligne à chaque morceau (`br: true` sur le premier mot) pour qu'aucune ligne n'enjambe deux plans.
5. Contrôle : Whisper sur la piste entière (tout le script, dans l'ordre, sans doublon, aucune pause de plus de 0,8 s).

Exemple complet : `runs/2026-09-28_claire-cheveux-gris-carences_talking-head/montage/construire_montage.py`.

## Variante : voix off d'origine partout (clips recalés)

Pour garder une voix parfaitement uniforme : son Seedance coupé, voix off ElevenLabs sur toute la vidéo, et chaque clip avatar recalé phrase par phrase sur la voix off (repères = début de chaque phrase dans le clip et dans la voix off ; entre deux repères, lecture légèrement accélérée ou ralentie, image par image). Les temps du montage sont alors ceux du découpage d'origine. Exemple : `construire_montage.py --voix-off` dans le run du 2026-09-28. Limite : la synchro des lèvres est calée par phrase, pas par syllabe ; éviter les vitesses hors de 0,7 à 1,3.

## Règles de calage

- La piste voix du montage (`audio`, voix hybride) est posée à 0 s. Tous les temps de `montage.json` sont des temps absolus de cette voix, en secondes.
- Chaque plan est converti en images à partir de ses temps absolus (pas de cumul d'arrondis). Les plans de base (`segments`) doivent se suivre sans trou ni chevauchement, de 0 à `durationSec`.
- Clip avatar : `clipStart` = temps absolu de l'image 0 du clip, c'est-à-dire le `clipStart` écrit par `couper_audio.py` (début du passage moins la marge). Le gabarit saute automatiquement le bon nombre d'images pour que les lèvres tombent sur la voix. Le son des clips est coupé.
- Un même clip avatar peut servir à plusieurs plans (changement de zoom A/B/C au milieu d'un passage) : même `src`, même `clipStart`, `start` différent.
- Passage coupé en deux clips par `couper_audio.py` (A01a, A01b) : le plan avatar passe au second clip dans la pause qui les sépare (0,05 s avant le premier mot du second). Change de zoom à ce moment pour rendre le raccord invisible.

## Référence de `montage.json`

```json
{
  "fps": 30, "width": 1080, "height": 1920, "durationSec": 62.4,
  "audio": "audio/voix.mp3", "bg": "#FAF6F3",
  "music": {"src": "audio/musique.mp3", "volume": 0.06},
  "theme": {"accent": "#E3262F", "accent2": "#FFD400", "subBox": "#FFFFFF", "subText": "#141414", "subDim": "#A3A3A3",
            "bannerBg": "#D7141A", "bannerText": "#FFFFFF", "infoBg": "#FFF1EA", "infoText": "#4A2A1A", "followBlue": "#1D8CF8"},
  "subtitles": {"words": [{"w": "Tes", "s": 0.0, "e": 0.18}], "maxWords": 4, "maxChars": 26, "size": 44, "hide": [[10.2, 11.0]]},
  "segments": [],
  "overlays": []
}
```

`subtitles.words` = le contenu de `mots.json` (transcription), corrigé d'après le script (orthographe, noms propres).

### Plans de base (`segments`)

Champs communs : `type`, `start`, `end`, `enter: "circle"` (entrée par cercle, `wipeX`/`wipeY` pour le centre), `subs` (`true`/`false` pour forcer), `subY` (hauteur des sous-titres, fraction de l'image).

| type | Usage | Champs |
|---|---|---|
| `avatar` | avatar plein écran | `src`, `clipStart`, `zoom` (`A`, `B`, `C` ou nombre), `faceY` (0,3 : centre du zoom), `drift` (léger zoom continu, vrai par défaut) |
| `split` | accroche | `src` (clip avatar 1:1), `clipStart`, `avatarPos`, `banner` (texte), `broll`: [{`src`, `start`, `end`, `from`, `rate`, `pos`, `kb`}] |
| `card` | b-roll en carte arrondie | `src` + `from`, ou `clips`: [{`src`, `start`, `end`, `from`, `rate`, `pos`, `kb`}], `cardW`, `cardH` |
| `letterbox` | b-roll horizontal en bandeau | `src`, `from`, `words` (au-dessus), `wordsBelow` |
| `full` / `image` | b-roll vertical, image IA plein écran | `src`, `from`, `rate`, `kb` (`in`/`out`), `fit`, `pos` |
| `edu` | animation éducative H3 | comme `full` (sous-titres masqués par défaut), ajoute les étiquettes en `overlays` |
| `plain` | fond uni (compteur, schéma) | `bg` (couleur ou dégradé CSS) |
| `collage` | 2 à 4 images empilées | `items`: [{`src`, `t` (apparition, facultatif), `from`}] |
| `infolist` | infographie à lignes | `rows`: [{`t`, `title`, `img`, `parts`: [{`s`, `bold`, `mark` (temps du surlignage)}]}], `bg` |
| `kinetic` | image dramatique + typo cinétique | `src`, `words`, `textY`, `size`, `align` |

`words` (typo cinétique) : [{`t`, `text`, `style` (`normal`, `light`, `accent`, `serif`, `giant`), `color`, `br` (retour à la ligne avant)}]. Un mot par entrée, `t` = attaque du mot moins 0,05 s.

Sous-titres masqués par défaut pendant : `split`, `edu`, `kinetic`, `letterbox`, `infolist`. Une ligne de sous-titres se termine toujours sur `.`, `!`, `?`, `:` ou avant un mot marqué `"br": true` (premier mot d'un plan). `bg` (racine) = couleur de fond visible pendant les ouvertures en cercle : mettre la couleur de fond de la charte.

### Surimpressions (`overlays`)

Champs communs : `type`, `start`, `end`, `hideSubs`, `subY`. Sous-titres masqués par défaut pendant `bignumber`, `doc`, `chapter`.

| type | Usage | Champs |
|---|---|---|
| `bignumber` | chiffre clé sur l'avatar | `text`, `label`, `y`, `size`, `color`, `glow` (halo, couleur CSS) |
| `doc` | capture de preuve + surligneur | `src`, `y`, `w`, `full`, `highlights`: [{`t`, `x`, `y`, `w`, `h`, `dur`, `color`}] (fractions de l'image) |
| `chapter` | titre de chapitre de liste | `number`, `title`, `media`, `mediaFrom`, `y`, `numColor` |
| `cutout` | objet détouré qui pope | `src`, `x`, `y`, `w`, `rotate`, `text`, `textT`, `textSize`, `textColor`, `textRotate` |
| `counter` | compteur animé | `from`, `to`, `countStart`, `countEnd`, `label`, `prefix`, `suffix`, `y`, `size`, `color` |
| `label` | étiquette d'animation | `text`, `sub`, `x`, `y`, `align`, `line` (px), `box`, `size`, `color` |
| `text` | texte libre | `text`, `x`, `y`, `size`, `color`, `serif`, `bg` |
| `inset` | média incrusté (comparatif) | `src`, `from`, `x`, `y`, `w`, `h`, `glow`, `fit` ; mettre `subY: 0.36` |
| `follow` | bouton « S'abonner » | `handle`, `avatar`, `y`, `clickAfter`, `text`, `doneText` |
| `flash` | transition lumineuse | `t` (moment de la coupe), `dur`, `color`, `at`, `strength` |

Positions `x`, `y`, `w`, `h` : fractions de la largeur ou de la hauteur de l'image (0 à 1).

## Ordre de travail du montage

1. Écris `montage.json` à partir de `decoupage.json` (mêmes temps), des fichiers réellement reçus et générés, et de la charte.
2. Rends 3 à 5 images fixes aux moments clés (accroche, première animation, une preuve, un chapitre, le CTA) et regarde-les avant le rendu complet.
3. Rendu complet en arrière-plan.
4. Contrôle avec `python3 <dossier du skill>/scripts/controler_montage.py out/final.mp4 montage.json script.txt --sortie controle_<passe>` : rapport OK / À CORRIGER (format, durée, volume, continuité des plans, médias, longueur des clips avatar, sous-titres, voix complète par Whisper, pauses) et planches d'images (8 images autour de chaque coupe, planches générales à 2 i/s). Trois passes minimum.
5. Regarde les planches (coupes, lèvres, textes), corrige `montage.json`, relance.
6. Finalise : `bash <dossier du skill>/scripts/finaliser.sh out/video.mp4 out/<nom>_final.mp4` (volume normalisé, lecture rapide sur mobile). C'est ce fichier qui est livré.

## Contrôles avant livraison

- Une seule voix, la voix maître, sans trou ni doublon ; durée de l'export = durée de la voix.
- Lèvres synchrones au début et à la fin de chaque clip avatar (planches de coupe).
- Chaque coupe tombe dans un silence, juste avant le premier mot de la phrase ; chaque élément animé apparaît 0 à 0,3 s avant son mot.
- Même visage, même tenue, même micro, même lumière dans tous les clips avatar.
- Aucun texte déformé généré par l'IA ; étiquettes et sous-titres identiques à l'audio (accents, noms propres).
- Sous-titres jamais sur la bouche ni sur un texte déjà à l'écran ; dernier cinquième de l'image libre.
- Volume : voix intelligible, pic sous -1 dBFS, environ -14 LUFS intégrés ; musique 20 dB sous la voix.
- Export 1080 x 1920, 30 i/s, H.264 + AAC. Vérifie le fichier exporté lui-même.

Si tu n'as pas pu regarder un moment (planche manquante), dis-le. « Prompts préparés » (ou découpage livré), « médias générés » et « vidéo montée et contrôlée » sont trois états différents.

## Feuille de montage CapCut (sur demande)

Pour chaque piste (voix, avatar, illustrations, surimpressions, sous-titres, musique) : fichier, début, fin, recadrage ou zoom, effet d'entrée. Commencer par poser la voix à 0 s.
