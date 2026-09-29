# Pipeline : commandes exactes, installation, dépannage

`$S` désigne le dossier `scripts/` du skill, `$A` le dossier `assets/`. Toutes les commandes se lancent depuis le dossier du projet (celui qui contient la voix et le script). Les scripts trouvent seuls `profiles.json` et le projet Remotion à côté d'eux.

## 0. Installation (une fois par environnement)

```bash
pip install --break-system-packages -U "setuptools>=70" wheel
pip install --break-system-packages -r $S/requirements-align.txt   # ctc-forced-aligner, faster-whisper, onnxruntime, numpy, scipy
export PATH=/opt/node22/bin:$PATH                                   # si Node n'est pas déjà dans le PATH
cd $A/remotion && npm install && cd -                               # Remotion (1 à 3 min, fait aussi par render.py au premier rendu)
```

Modèles téléchargés au premier usage : MMS forced aligner ONNX (1,26 Go, huggingface.co) et, en secours, faster-whisper small (480 Mo). Chromium : `/opt/pw-browsers/chromium` est détecté automatiquement ; sinon Remotion télécharge le sien.

Vérification rapide : `python3 $S/align.py --help` et `ls $A/remotion/node_modules/remotion` ne doivent pas échouer.

## 1. Mode BRIEF (voix + script → brief.html)

```bash
mkdir -p work out rushes
# optionnel : resserrer les silences AVANT tout le reste (puis utiliser work/vo_tight.wav partout)
python3 $S/tighten_vo.py voix.mp3 --out work/vo_tight.wav --max-pause 0.5 --keep 0.25

python3 $S/align.py voix.mp3 script.txt --out work/words.json            # 20 à 60 s pour 40 s de voix selon la charge (ctc), 12 s en whisper
python3 $S/audio_features.py voix.mp3 work/words.json --out work/features.json
python3 $S/propose_beats.py work/words.json work/features.json --profile ADS --out work/beats_draft.json
```

Puis, toi : lis `work/beats_draft.json`, `work/words.json`, `work/features.json` et le script ; écris `brief.json` en suivant `segmentation.md` et `broll-direction.md` (schéma dans `CONTRACTS.md` section 4). Ensuite :

```bash
python3 $S/validate_brief.py brief.json --fix-slugs      # corrige jusqu'à 0 erreur
python3 $S/build_brief.py brief.json --out brief.html --audio voix.mp3 --features work/features.json --words work/words.json
```

Livrables du mode 1 : `brief.html` (à ouvrir dans un navigateur, fonctionne hors ligne) et `brief.json` (à conserver pour le mode 2).

## 2. Mode MONTAGE (rushes → final_9x16.mp4)

Préalable : l'utilisateur a déposé ses fichiers dans `rushes/`, nommés par ID (`03a_...mp4` ou au minimum `03a.mp4`).

```bash
python3 $S/inventory.py brief.json rushes/ --out work/inventory.json
#   → lis work/inventory.json : liste `missing` et `substitutions`. Si des plans manquent, propose à l'utilisateur
#     (a) déposer le fichier, (b) accepter la substitution, (c) remplacer par un MOTION. Ne rends pas avec des trous non assumés.
python3 $S/best_window.py work/inventory.json brief.json --out work/windows.json
python3 $S/prep_clips.py brief.json work/inventory.json work/windows.json --out work/clips/     # ~8 s par clip
python3 $S/make_captions.py work/words.json brief.json --out work/captions.json
python3 $S/build_timeline.py brief.json work/inventory.json work/windows.json work/features.json --out work/timeline.json [--music musique.mp3]
python3 $S/render.py work/timeline.json --out work/preview.mp4 --preview                       # ~8 s par seconde de vidéo
python3 $S/render.py work/timeline.json --out out/stills --frames 15,45,120                     # images de contrôle ciblées (rapide)
python3 $S/render.py work/timeline.json --out out/final_9x16.mp4                                # rendu final + loudnorm + srt
python3 $S/qc.py work/timeline.json out/final_9x16.mp4 brief.json --out out/qc_report.md        # score /100 + contact_sheet.jpg
```

Regarde `out/contact_sheet.jpg` et 3 à 5 images de contrôle avec l'outil de lecture d'images avant de livrer. Score QC minimum : 90. En dessous, applique les corrections proposées dans le rapport (souvent : éditer `work/timeline.json` puis relancer render et qc).

Livrables du mode 2 : `out/final_9x16.mp4`, `out/final.srt`, `out/qc_report.md`, `out/contact_sheet.jpg`, `out/timeline.json`.

## 3. Ajustements courants

- Changer une transition : éditer `clips[i].transition_in` dans `work/timeline.json` (`cut`, `whip`, `zoomthrough`, `flash`, `dissolve`, `wipe`, `punchcut`) puis relancer `render.py`.
- Sans sous-titres : `captions.style = "none"`. Sous-titres sans boîte rouge : `captions.hook_style = "default"`.
- Musique : `--music fichier` sur `build_timeline.py` (niveau `music_db` du profil, modifiable dans `audio.music_db`).
- Barre de progression ou logo : `render.py --progress-bar --logo logo.png`.
- Déclinaisons 1:1 ou 4:5 : relancer `prep_clips.py --width 1080 --height 1080` (ou 1350) dans un autre dossier `work_1x1/`, puis `build_timeline.py --out work_1x1/timeline.json` et `render.py`.
- Autre police ou style de sous-titres : constantes en tête de `assets/remotion/src/components/Captions.tsx`.

## 4. Dépannage

- `align.py` : « aucune méthode disponible » → installer les dépendances (section 0). `ctc-forced-aligner` refuse de compiler → mettre setuptools à jour d'abord. Avertissement « mots à score < 0,05 » (émis à partir de 3 mots concernés) → le script ne correspond pas exactement à la voix : corriger le script (c'est lui la vérité du texte) et relancer. Un ou deux mots à score bas isolés sont normaux (mots très courts, liaisons).
- Voix off avec chiffres ou marques : ctc les gère (« 97 % » prononcé « quatre-vingt-dix-sept pour cent »). Pour une voix belge : `--numbers be`.
- `validate_brief.py` : chaque erreur donne l'ID du plan et la règle ; les plus fréquentes sont un trou entre deux plans (arrondi), deux valeurs identiques consécutives, un `filename` qui ne suit pas `{id}_{section}_{type}_{slug}.mp4` (utiliser `--fix-slugs`).
- `render.py` : « Old Headless mode has been removed » est géré automatiquement (mode chrome-for-testing). Compositeur tué (mémoire) → relance automatique en concurrence 1 ; sinon `--cache-mb 256 --concurrency 1`. `npm install` qui échoue → vérifier l'accès à registry.npmjs.org et Node >= 18.
- Rush horizontal : recadré en cover centré sur le visage détecté, sinon sur le tiers supérieur. Si le sujet est coupé, fournir un rush vertical ou déplacer le sujet au centre.
- Rush trop court : ralenti jusqu'à 0,8x, puis substitution (voisin de séquence), puis boomerang. Mieux : fournir 2 s de plus.
- Rendu lent : normal sur 2 CPU (8 s par seconde de vidéo). Utiliser `--frames` pour vérifier des points précis plutôt que de rendre plusieurs fois.
