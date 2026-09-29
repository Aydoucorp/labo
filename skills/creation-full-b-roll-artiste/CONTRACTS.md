# CRÉATION FULL B-ROLL ARTISTE : contrats de données

Tous les fichiers sont du JSON UTF-8. Les temps sont en secondes (float, 3 décimales) sauf dans `timeline.json` où tout est en frames (int) à `fps` fixe. Les identifiants de plans sont des chaînes (`"03"`, `"03a"`).

Arborescence d'un projet (créée par le skill) :

```
projet/
  voix.mp3 (ou .wav)          entrée
  script.txt                  entrée
  brief.json                  sortie mode 1 (vérité machine)
  brief.html                  sortie mode 1 (shot list interactive)
  rushes/                     dépôt des fichiers par l'utilisateur, nommés par ID
  work/                       intermédiaires (jamais livrés)
    words.json  features.json  beats_draft.json
    inventory.json  windows.json  clips/  captions.json  timeline.json
    preview.mp4  contact_sheet.jpg
  out/
    final_9x16.mp4  final.srt  qc_report.md  timeline.json (copie)
```

## 1. words.json (align.py)

```json
{
  "audio": "voix.mp3",
  "duration_s": 42.310,
  "language": "fr",
  "method": "ctc-forced-aligner | faster-whisper+script",
  "script_hash": "sha1 du script normalisé",
  "words": [
    {"i": 0, "w": "Tu", "start": 0.120, "end": 0.310, "score": 0.98, "punct_after": ""},
    {"i": 1, "w": "frottes", "start": 0.310, "end": 0.740, "score": 0.95, "punct_after": ","}
  ]
}
```

`w` est le mot tel qu'il apparaît dans le script (casse et accents conservés), `punct_after` la ponctuation qui le suit dans le script (`""`, `","`, `"."`, `"?"`, `"!"`, `":"`, `"..."`). Les mots sont dans l'ordre du script, sans trou. `score` est la confiance d'alignement (0 à 1, null si inconnue).

## 2. features.json (audio_features.py)

```json
{
  "duration_s": 42.310,
  "loudness_lufs": -18.2,
  "pauses": [{"start": 3.210, "end": 3.460, "dur": 0.250, "after_word_i": 11}],
  "emphasis": [{"word_i": 12, "t": 4.100, "z": 2.3}],
  "energy": {"hop_s": 0.050, "rms_db": [-32.1, -28.4, "..."]},
  "speech_rate_wps": 2.9
}
```

`pauses` : silences >= 0.18 s entre deux mots (le champ `after_word_i` donne le mot qui précède la pause). `emphasis` : mots dont l'énergie RMS dépasse la moyenne locale de plus de 1,5 écart-type (mots appuyés par la voix). `energy.rms_db` : enveloppe pour la forme d'onde du HTML.

## 3. beats_draft.json (propose_beats.py, proposition mécanique que Claude affine)

```json
{
  "profile": "ADS",
  "beats": [
    {"id": "01", "start": 0.000, "end": 1.850, "word_from": 0, "word_to": 5,
     "text": "Tu frottes ton sol tous les jours,",
     "cut_reason": "pause+ponctuation",
     "energy": 4,
     "suggested_split": null}
  ]
}
```

Règle : les frontières sont toujours des frontières de mots ; `cut_reason` explique le choix (`pause`, `ponctuation`, `pause+ponctuation`, `duree_max`, `connecteur`). `suggested_split` est non nul quand le beat dépasse la durée max du profil et propose des sous-frontières (séquence 3 valeurs).

## 4. brief.json (produit par Claude en mode 1, validé par validate_brief.py, consommé par build_brief.py et le mode 2)

```json
{
  "schema": "broll-director/brief/1",
  "project": {
    "name": "eviclean-feuilles-hook3",
    "profile": "ADS",
    "platform": "tiktok",
    "ratio": "9:16", "width": 1080, "height": 1920, "fps": 30,
    "language": "fr",
    "brand": "Eviclean",
    "lookbook": {
      "light": "lumière naturelle de fenêtre, tons chauds",
      "palette": "blanc, bois clair, vert doux",
      "setting": "cuisine et salle de bain modernes, sol clair",
      "people": "mains de femme 35-50 ans, pas de visage en gros plan",
      "style_suffix_en": "natural window light, warm tones, shallow depth of field, handheld feel"
    },
    "subtitles": {"style": "default", "hook_style": "red-box"}
  },
  "audio": {"file": "voix.mp3", "duration_s": 42.310},
  "script_diagnostic": {
    "hook_ok": true, "promise_validated_by_s": 8.4, "cta_position_pct": 66,
    "loop_closed": true, "notes": ["..."]
  },
  "sections": [
    {"id": "HOOK", "start": 0.000, "end": 2.100},
    {"id": "PROB", "start": 2.100, "end": 9.800}
  ],
  "beats": [
    {
      "id": "03",
      "section": "PROB",
      "function": "PROBLEME",
      "start": 4.100, "end": 6.350,
      "text": "tu frottes, tu rinces, et ça colle encore.",
      "pivot_word": "colle", "pivot_t": 5.620,
      "energy": 3,
      "abstraction": "concret",
      "shots": [
        {
          "id": "03a",
          "start": 4.100, "end": 5.200,
          "type": "UGC",
          "value": "moyen",
          "camera": "handheld",
          "description": "Une main frotte un sol de cuisine avec une serpillière classique, effort visible.",
          "query_en": "hand scrubbing kitchen floor with mop, close view, natural window light",
          "query_fr": "main qui frotte le sol de la cuisine avec une serpillière",
          "ai_prompt": {
            "image": "Photo réaliste, vue rapprochée d'une main de femme qui frotte un sol carrelé clair avec une serpillière, cuisine moderne, lumière naturelle de fenêtre, format vertical 9:16",
            "motion": "Mouvement de frottement énergique, légère caméra à l'épaule, 3 secondes"
          },
          "min_rush_s": 2.1,
          "orientation": "vertical",
          "filename": "03a_PROB_UGC_main-frotte-sol.mp4",
          "overlay_text": null,
          "sfx": null,
          "must_show": ["serpillière", "sol"],
          "fallback": {"type": "STOCK", "query_en": "mopping tiled floor close up"}
        }
      ]
    }
  ],
  "shooting_plan": [
    {"location": "cuisine", "shots": ["03a", "03b", "07a"]}
  ]
}
```

Champs fermés :

- `profile` : `ADS` | `EDU`
- `platform` : `tiktok` | `reels` | `shorts` | `youtube` | `meta-feed`
- `function` : `HOOK` | `PROMESSE` | `PROBLEME` | `AGITATION` | `MECANISME` | `PREUVE` | `PRODUIT` | `BENEFICE` | `OBJECTION` | `CTA` | `CHUTE`
- `section.id` : `HOOK` | `PROB` | `MECA` | `PREUVE` | `PROD` | `BENEF` | `OBJ` | `CTA` | `CHUTE` (au moins HOOK et CTA ou CHUTE)
- `abstraction` : `concret` | `consequence` | `mecanisme` | `abstrait` | `emotion`
- `shot.type` : `STOCK` | `UGC` | `PRODUIT` | `3DSCI` | `MOTION` | `SCREEN` | `SOCIAL` | `IAGEN`
- `shot.value` : `large` | `moyen` | `detail` | `macro` | `topdown` | `pov`
- `shot.camera` : `static` | `push` | `pull` | `pan` | `handheld` | `orbit` | `tilt`
- `orientation` : `vertical` | `horizontal` | `any`
- `energy` : 1 à 5

Contraintes vérifiées par `validate_brief.py` : les plans couvrent l'audio de 0 à `duration_s` sans trou ni chevauchement ; chaque plan dure entre `min` et `max` de sa section dans le profil (HOOK : min 0,6 s quel que soit le profil) ; le « corps » utilisé pour `product_share_min` = toutes les sections sauf HOOK, mesuré en durée ; `filename` = `{id}_{section}_{type}_{slug}.mp4` unique ; pas deux `value` identiques consécutives ; pas deux `camera` identiques consécutives ; `pivot_t` dans `[start, end]` du beat ; type `MOTION` n'a pas de `query_en` obligatoire mais a `overlay_text` ou `description` (et garde `value`, `camera`, `orientation`, qui comptent dans l'alternance) ; `min_rush_s` >= durée du plan ; `shooting_plan` liste tous les plans UGC et PRODUIT ; les frontières de beats suivent les plans et peuvent s'écarter des frontières de mots.

## 5. inventory.json (inventory.py)

```json
{
  "rushes_dir": "rushes",
  "shots": [
    {"id": "03a", "expected": "03a_PROB_UGC_main-frotte-sol.mp4",
     "file": "rushes/03a_main.mp4", "match": "prefix",
     "duration_s": 6.2, "width": 1080, "height": 1920, "fps": 30, "has_audio": true,
     "status": "ok | too_short | missing | bad_format"}
  ],
  "missing": ["07b"],
  "substitutions": [{"shot": "07b", "use": "07a", "reason": "voisin même séquence"}]
}
```

## 6. windows.json (best_window.py)

```json
{"shots": [{"id": "03a", "src": "rushes/03a_main.mp4", "in_s": 1.40, "out_s": 2.60,
            "motion_score": 0.71, "method": "frame-diff"}]}
```

## 7. captions.json (make_captions.py, format Remotion `Caption`)

```json
{"fps": 30, "hook_end_ms": 2100,
 "captions": [{"text": " Tu", "startMs": 120, "endMs": 310, "timestampMs": 215, "confidence": 0.98}]}
```

Convention Remotion : un espace devant chaque mot sauf le premier d'une page.

## 8. timeline.json (build_timeline.py, consommé par Remotion et qc.py)

```json
{
  "schema": "broll-director/timeline/1",
  "fps": 30, "width": 1080, "height": 1920, "duration_frames": 1270,
  "profile": "ADS",
  "audio": {
    "vo": "work/vo_norm.wav",
    "music": null, "music_db": -22,
    "ambience_db": -25
  },
  "clips": [
    {
      "shot_id": "03a",
      "src": "work/clips/03a.mp4",
      "from_frame": 123, "duration_frames": 33,
      "trim_before_frames": 42,
      "speed": 1.0,
      "kenburns": {"from": 1.0, "to": 1.06, "origin": [0.5, 0.45]},
      "punch": {"at_frame": 140, "scale": 1.10, "frames": 6},
      "transition_in": {"type": "cut", "frames": 0, "dir": null},
      "ambience": true,
      "ambience_db": -25
    }
  ],
  "captions": {"file": "work/captions.json", "style": "default", "hook_style": "red-box", "hook_end_frame": 63},
  "overlays": [
    {"type": "text", "text": "3 secondes", "from_frame": 300, "duration_frames": 45, "style": "stat", "anchor": "center"}
  ],
  "sfx": [{"src": "assets/sfx/whoosh_soft.wav", "at_frame": 63, "db": -14}],
  "endcard": null
}
```

`transition_in.type` : `cut` | `whip` | `zoomthrough` | `flash` | `dissolve` | `wipe` | `punchcut`. `dir` : `left` | `right` | `up` | `down` | null. Les clips sont déjà prêts (1080x1920, fps du projet, colorimétrie normalisée) : Remotion n'applique que des transformations (scale, translate, opacity) et le mixage audio.

Précisions :

- `speed` est le `playbackRate` du clip, borné à `[1/speed_ramp_max, speed_ramp_max]`. Un rush trop court est ralenti (jamais au delà de la borne basse) ; s'il reste trop court, `inventory.py` propose une substitution, puis `prep_clips.py` fabrique un aller-retour (boomerang) en dernier recours. L'accélération sert à donner de l'énergie à un rush lent quand il est assez long.
- Les chemins `sfx[].src` sont relatifs au dossier du skill (`assets/sfx/...`), tous les autres chemins sont relatifs au dossier du projet. `render.py` et `qc.py` résolvent les deux (projet d'abord, skill ensuite).
- Des champs additifs sont autorisés dans `windows.json` (`speed`, `padded`, `source_method`) et dans `timeline.clips[]` (`section`, `type`, `camera`, `value`, `source_rush`, `source_method`) ainsi que `timeline.safe_zone`. Remotion les ignore, `qc.py` les utilise.

## 9. qc_report.md (qc.py)

Markdown avec un score /100, la liste des contrôles (nom, résultat, valeur mesurée, seuil, correction proposée) et le chemin de la planche contact.
