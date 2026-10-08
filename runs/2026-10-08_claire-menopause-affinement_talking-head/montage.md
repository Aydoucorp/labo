# Montage · Claire · Affinement des cheveux à la ménopause · Talking head n°2

**Version 1 montée et contrôlée (3 passes, tout OK).** Fichiers dans `retenues/` :
- `claire-menopause-affinement-talking-head-v1-vitesse100.mp4` : 59,57 s, 1080×1920, 30 i/s, H.264 + AAC, -14,2 LUFS, pic -1,5 dBFS.
- `…-vitesse090.mp4` (66,2 s) et `…-vitesse085.mp4` (70,1 s) : vidéo entière ralentie, voix sans changement de hauteur (demande « on va slowly le tout »). Vitesse finale à choisir par l'utilisateur.

## Voix et synchro des lèvres

- Voix off ElevenLabs d'origine sur toute la vidéo, son des clips Seedance coupé.
- Clips de Claire recalés **mot par mot** sur la voix off (`montage/recaler_mots.py`) : chaque mot reconnu dans le clip est apparié au même mot de la voix off (alignement de séquences tolérant aux mots déformés), image accélérée ou ralentie entre deux mots, vitesse bornée entre 0,65 et 1,6. Sorties : `avatar/recale/`.
  - S01 (accroche, plan de 3/4 profil, `S01_profil_v1`) : 12 ancres, vitesse 0,81 à 1,58.
  - A01 : 26 ancres, 0,89 à 1,53 · A02 (2e caméra) : 28 ancres, 0,65 à 1,37 · A03 : 46 ancres, 0,67 à 1,52.
- Clips prolongés de 0,6 s (dernière image figée, bouche fermée) pour couvrir la fin des plans.

## Plans (temps du découpage, alignement MMS)

| Temps | Plan | Contenu |
|---|---|---|
| 0,00 → 4,30 | Écran partagé | S01 profil en haut, B01/B02 en bas, bandeau « 2 femmes sur 3 voient leurs cheveux s'affiner à la ménopause » |
| 4,30 → 13,50 | Animation E1 | Ouverture en cercle ; étiquettes Œstrogènes, Phase de croissance, DHT, Follicule sur leur mot |
| 13,50 → 16,70 | Avatar A01, zoom A | |
| 16,70 → 19,10 | B03 (raie, à partir de 1,9 s) | |
| 19,10 → 21,20 | Avatar A01, zoom C | Flash terracotta « Mais voici des solutions » |
| 21,20 → 22,75 | B04 (prise de sang, à partir de 42 s) | |
| 22,75 → 31,30 | Avatar A02 (2e caméra), zooms B, C, A | Pot de collagène détouré à 28,3 s |
| 31,30 → 33,13 | B05 (de dos, à partir de 2 s) | |
| 33,13 → 36,68 | B06 (massage, à partir de 44 s) | |
| 36,68 → 40,75 | B07 (gouttes de romarin, IA) | |
| 40,75 → 45,80 | Infographie 2 lignes | Huile de romarin, Massage quotidien ; « encourageantes » surligné |
| 45,80 → 59,56 | Avatar A03, zooms B, A, B, C | Carte du guide à 52,3 s ; « GUIDE » à 56,4 s ; bouton S'abonner |

## Contrôles

`montage/controle_1`, `controle_2`, `controle_3` (rapports et planches). Corrections : clip d'accroche trop court, écran vide au début de l'infographie, sous-titre « D-H-T » aligné sur le script, reliquats de sous-titres après l'animation et l'infographie, piste son plus longue que l'image. Mots signalés par Whisper (« eustrogène », « empourageantes ») : erreurs de reconnaissance, la voix off dit bien les mots du script.

Construction : `python3 montage/construire_montage.py` puis `bash .claude/skills/talking-head/scripts/rendre.sh montage`.
