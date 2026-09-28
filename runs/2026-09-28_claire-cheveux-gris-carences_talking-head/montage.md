# Montage · Claire · Cheveux gris et carences · Talking head

**Livré :** `creas/talking-head/2026-09-28_talking-head_001.mp4` (copie : `retenues/film/claire-cheveux-gris-carences-talking-head-v1.mp4`) · 56,7 s · 1080×1920 · 30 i/s · H.264 + AAC · -14,5 LUFS, pic -1,2 dBFS.

## Voix

Voix hybride (choix validé) : sur les passages avatar, la voix générée par Seedance 2.5 dans chaque clip (lèvres synchrones) ; sur les autres plans, la voix off ElevenLabs d'origine. Chaque morceau est ramené au même volume (-18 LUFS) avec des fondus de 20 à 30 ms, puis l'ensemble est normalisé à -14 LUFS.

| Morceau | Source | Extrait | Sur la vidéo |
|---|---|---|---|
| S01 | clip avatar S01 | 0,20 → 5,77 s | 0,00 → 5,57 s |
| A01 | clip avatar A01 | 0,15 → 8,97 s | 5,57 → 14,39 s |
| M1 | voix off | 14,25 → 22,75 s | 14,39 → 22,89 s |
| A02 | clip avatar A02 (v2) | 0,32 → 3,36 s | 22,89 → 25,93 s |
| M2 | voix off | 25,64 → 28,48 s | 25,93 → 28,77 s |
| A03 | clip avatar A03 | 0,14 → 6,73 s | 28,77 → 35,36 s |
| M3 | voix off | 35,40 → 42,95 s | 35,36 → 42,91 s |
| A04 | clip avatar A04 | 1,48 → 2,74 s | 42,91 → 44,17 s |
| M4 | voix off | 44,64 → 51,08 s | 44,17 → 50,61 s |
| A05 | clip avatar A05 | 0,03 → 6,00 s | 50,61 → 56,58 s |

## Plans

| Temps | Plan | Contenu |
|---|---|---|
| 0,0 → 5,6 | Écran partagé | Avatar S01 en haut ; b-roll 01 (racines grises) puis b-roll 02 (ADN) en bas ; bandeau « Cheveux blancs à 35 ans ? Ce n'est pas que la génétique » |
| 5,6 → 14,4 | Avatar A01 (zoom C puis B) | Flash d'entrée ; gros chiffre « 30 % héréditaire » |
| 14,4 → 22,9 | Animation E1 (muette) | Ouverture en cercle ; étiquettes Follicule, Catalase, H₂O₂, Pigment sur leur mot |
| 22,9 → 25,9 | Avatar A02 (zoom A) | |
| 25,9 → 28,8 | B-roll 03 plein écran | Premières secondes, son coupé |
| 28,8 → 35,4 | Avatar A03 (zoom C puis B) | Compte sur les doigts |
| 35,4 → 42,9 | Infographie | Cuivre, B12, Fer avec I1 à I3 ; surlignage sur la phrase dite |
| 42,9 → 44,2 | Avatar A04 (zoom A) | « Dans l'assiette » |
| 44,2 → 49,5 | Cartes aliments | I4 à I8, une carte par aliment prononcé |
| 49,5 → 50,6 | B-roll 04 plein écran | Recadré 16:9 → 9:16, son coupé |
| 50,6 → 56,6 | Avatar A05 (zoom B puis C) | Flash d'entrée ; « GUIDE » ; bouton « S'abonner » @les_cheveux_de_claire |

Sous-titres karaoké (boîte crème, texte encre), coupés à chaque changement de plan ; masqués pendant l'accroche, l'animation, l'infographie et le CTA.

## Contrôles (3 passes)

1. Rendu v1 : planches de coupe et planches générales. Corrigé : sous-titres qui enjambaient deux plans ; fond noir visible pendant les ouvertures en cercle. Voix complète vérifiée (Whisper) : tout le script, dans l'ordre, sans doublon ; silence de 1,1 s avant « Dans l'assiette » raccourci.
2. Rendu v2 : sous-titres et transitions corrects. Corrigé : bouton « S'abonner » visible trop peu de temps (apparition avancée à « GUIDE »).
3. Rendu v3 final : image, voix complète, volume (-14,5 LUFS, pic -1,2 dBFS), format 1080×1920 30 i/s vérifiés sur le fichier exporté.

## Reproduire

Depuis le dossier du run : `python3 montage/construire_montage.py`, puis dans `montage/` : `bash <skill>/scripts/rendre.sh .` et `bash <skill>/scripts/finaliser.sh out/video.mp4 out/final.mp4`.
