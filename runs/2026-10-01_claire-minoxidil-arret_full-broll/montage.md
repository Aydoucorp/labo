# Montage : Claire, arrêter le minoxidil (full b-roll artiste)

- Voix off : `voix.mp3` (79,57 s), alignement MMS (`work/words.json`).
- Pipeline du skill : `inventory.py` → `best_window.py` → `prep_clips.py` → `make_captions.py` → `build_timeline.py` → `work/ajuster_timeline.py` → `render.py` → `qc.py`.
- Sortie : `out/final_9x16.mp4` (1080x1920, 30 i/s), sous-titres `out/final.srt`, rapport `out/qc_report.md`, planche `out/contact_sheet.jpg`.

## Sources des 31 plans

| Plans | Source |
|---|---|
| 01a, 01d, 04a, 04b, 05a, 05b, 06b, 11, 13, 15a, 16, 18, 19, 20a, 20b | Rushes générés à la main avec les prompts réalistes, rapatriés du Drive (`rushes/drive/`) |
| 01b + 01c | Un seul rush (`01b et 01c.mp4`) coupé en deux : 0 à 2,45 s pour 01b, 2,45 à 4,92 s pour 01c (01c passe de carte texte à vidéo, avec la mention « « 50 % de mes cheveux ? » ») |
| 02 + 03 | Un seul rush 4K (`02 et 03.mp4`, 7,76 s) coupé en deux : 0 à 4,3 s pour 02, 4,3 à 7,76 s pour 03 |
| 09 | Image fixe (`09.jpeg`), voulue, animée en zoom lent 4,5 s |
| 07, 08, 10, 14a, 14b, 15b, 17, 21b | Animations 3D générées (Nano Banana 2 1K + MiniMax H3 768P) |
| 21a | Généré : image Nano Banana 2 1K avec « Guide » tapé dans le champ de commentaire, puis MiniMax H3 768P 4 s ; on garde les 3,6 premières secondes (le mot reste lisible) |
| 06a, 12 | Cartes texte générées par le skill (« NON. », « Effluvium télogène »), dégradé aux couleurs de la charte (prune, terracotta) |

## Réglages

- Profil EDU, sous-titres karaoké mot à mot, boîte rouge pendant l'accroche (0 à 5 s).
- Transitions : cuts par défaut ; zoomthrough seulement pour entrer dans la 3D (07, 10, 14a, 15b, 17) et aux changements de section (06a, 18, 21a) ; flash en sortie d'accroche (02). Les sorties de 3D vers le réel (09, 11, 15a, 16) sont en cut (`work/ajuster_timeline.py`).
- Mentions à l'écran : « 50 % de mes cheveux ? », « NON. », « Phase de pousse prolongée », « Alopécie androgénétique », « Effluvium télogène », « Stress · régime · carence », « Phase télogène = repos », « Testées face au minoxidil (études 2015 et 2021) », « Bonus : le massage ». La mention « Commente « Guide » » est retirée (doublon du sous-titre et de l'écran du téléphone).
- Skill amélioré pendant ce montage : `project.motion_palette` dans le brief impose les couleurs des cartes texte (dégradé linéaire).

## Coûts du run

- 8 animations 3D : 320 cr ; plan 21a : 40 cr ; total génération : 360 cr.
