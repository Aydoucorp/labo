# Montage : tempes, partie 1 (v1 complète, 2026-10-23)

Sortie : `montage/final_9x16.mp4` (commande : `python3 work/montage.py --b1 rushes/b1-tempe-utilisateur-v1.mp4 --b3 rushes/b3-follicule-3d-utilisateur-v1.mp4 --b4 rushes/b4-tempes-3d-utilisateur-v1.mp4 --avant sorties/avant-v2.png --apres sorties/apres-v1.png --out montage/final_9x16.mp4`) (1080x1920, 30 i/s, 64,99 s). Script : `work/montage.py` (relançable avec `--b1`, `--b4`, `--avant`, `--apres`).
Son : voix ElevenLabs Victoria seule (loudnorm -14 LUFS), son Wan coupé, pas de musique.

| Timeline | Plan | Source |
|---|---|---|
| 0,00 à 8,20 | W1 (début source 0,5 s) | `sorties/clips/W1-v1.mp4` |
| 8,20 à 14,75 | W8 en deux morceaux (seconde moitié avancée de 0,23 s) | `sorties/clips/W8-v1.mp4` |
| 14,75 à 18,05 | W2 | `sorties/clips/W2-v1.mp4` |
| 18,05 à 21,70 | B1 : tempe dégarnie de l'avatar (IA, utilisateur), début source 0,3 s | `rushes/b1-tempe-utilisateur-v1.mp4` |
| 21,70 à 25,50 | **motion design** B2 : cycle de pousse de plus en plus court | `sorties/motion/B2-motion.mp4` |
| 25,50 à 27,85 | B3 : 3D style Drew sur fond crème, le follicule qui se fragilise (IA, utilisateur), début 1,2 s, étiquette « Follicule fragilisé » | `rushes/b3-follicule-3d-utilisateur-v1.mp4` |
| 27,85 à 29,40 | W3 | `sorties/clips/W3-v1.mp4` |
| 29,40 à 34,45 | B4 : 3D style Drew sur fond crème, tête translucide puis follicules épais / fins (IA, utilisateur), début 0,5 s, étiquettes « Tempes », « Haut de la tête » / « Tempes » | `rushes/b4-tempes-3d-utilisateur-v1.mp4` | |
| 34,45 à 42,55 | W4 | `sorties/clips/W4-v1.mp4` |
| 42,55 à 44,25 | W5 (début source 0,47 s) | `sorties/clips/W5-v1.mp4` |
| 44,25 à 49,05 | **motion design** B5a : courbe des hormones (périménopause, ménopause), puis les tempes qui s'allument | `sorties/motion/B5a-motion.mp4` |
| 49,05 à 52,00 | **motion design** B5b : jauges œstrogène (baisse) et cortisol (augmente) | `sorties/motion/B5b-motion.mp4` |
| 52,00 à 54,85 | W6 en deux morceaux (recalé à « devient ») | `sorties/clips/W6-v1.mp4` |
| 54,85 à 64,99 | W7 | `sorties/clips/W7-v1.mp4` |

Habillage : accroche « Tes tempes / s'affinent ? » de 0 à 2,85 s ; sous-titres 2 lignes, ligne lue en terracotta clair `#C9805F` ; photos avant / après générées par IA (`sorties/avant-v2.png`, `sorties/apres-v1.png`), 320 px de large dans les coins hauts, sur « de ça » (9,85 s) et « à ça » (10,80 s) jusqu'à 13,30 s ; mention IA dans la description de la publication (choix de l'utilisateur).

Anomalie de la bibliothèque : le fichier de br-0031 (« gros plan de tempes qui grisonnent ») contient une hélice d'ADN sur fond étoilé. Signalé à l'utilisateur, fiche non modifiée.

Motion design (choix de l'utilisateur : mélange motion design + 3D style Drew) : `work/motion.py`, rendu 1080x1920 30 i/s aux couleurs et typos de Claire, calé au mot près sur `work/mots.json`, gratuit. Sur ces passages, les sous-titres passent en encre #2E2A26 avec la ligne lue en terracotta #A8553A, sans contour (lisibles sur le fond crème).

Sur les fonds crème (motion design, B3, B4), sous-titres en encre avec un fin contour crème. Étiquettes des 3D en Fraunces prune (polices dans `montage/polices/`).
