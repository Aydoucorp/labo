# Montage : raie élargie (v1, 2026-10-22)

Sortie : `montage/final_9x16.mp4` (1080x1920, 30 i/s, 43,73 s). Script : `work/montage.py` (relançable).
Son : voix ElevenLabs d'origine seule (`audio/voix.mp3`, loudnorm -14 LUFS), son Wan coupé, pas de musique.

| Timeline | Plan | Source | Début source |
|---|---|---|---|
| 0,00 à 3,00 | C1 | `sorties/clips/C1-v2.mp4` | 0,5 s (silence de tête coupé) |
| 3,00 à 8,95 | C2 | `sorties/clips/C2-v1.mp4` | 0 |
| 8,95 à 15,60 | C3 | `sorties/clips/C3-v1.mp4` | 0 |
| 15,60 à 20,30 | 3D follicule qui rétrécit | bibliothèque br-0015 (léger ralenti 0,95) | 0 |
| 20,30 à 23,70 | Queue de cheval, pull de pyjama, date « mars 2024 » | `rushes/v-queue-utilisateur-v2-pyjama.mp4` | 0,2 s |
| 23,70 à 30,25 | C5 | `sorties/clips/C5-v1.mp4` | 0 |
| 30,25 à 32,25 | 3D coupe du cuir chevelu, particules dorées (« soutenir le follicule ») | bibliothèque br-0012 | 1,0 s |
| 32,25 à 35,25 | 3D bulbe lumineux (« calmer cette inflammation ») | bibliothèque br-0013, **en attendant P2** (`--p2 fichier.mp4` pour le remplacer) | 0,8 s |
| 35,25 à 37,80 | Raie élargie, date « juin 2024 » | `rushes/v-raie-utilisateur-v1.mp4` | 0,9 s |
| 37,80 à 43,73 | C7 | `sorties/clips/C7-v2.mp4` | 0 |

Habillage :
- Accroche 0 à 2,85 s, en haut : « Si ta raie s'élargit / écoute bien » (Montserrat ExtraBold 74, blanc, contour noir).
- Insert raies (`sorties/insert-raies-nb-v1.png`) 0 à 2,85 s en bas ; insert follicule (`sorties/insert-follicule-nb-v1.png`) 14,30 à 15,60 s.
- Sous-titres mot à mot en majuscules (Montserrat Bold 70, blanc, ombre), à gauche à hauteur d'épaule, calés sur `work/mots.json`.
- Dates en haut à gauche (Montserrat ExtraBold 62, contour léger) sur les deux b-rolls de l'avatar (choix de l'utilisateur).
