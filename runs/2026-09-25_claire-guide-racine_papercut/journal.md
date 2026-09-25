# Journal des générations

Tarif KIE standard : 1 crédit ≈ 0,005 $ (page tarifs kie.ai, relevée le 2026-09-25).

| Réf / plan | Variante | Moteur | Prompt | Références | ID de tâche | État | Fichier reçu | Contrôle visuel | Coût |
|---|---|---|---|---|---|---|---|---|---|
| R1 couverture | v1 | nano-banana-2 2K 2:3 | `references/prompts/r1-couverture.txt` | — | d05344dad6f88afcac245190ee4c5bbc | success | `sorties/references/r1-couverture-v1.png` | rejetée : visage visible | 12 cr |
| R3 palette | v1 | nano-banana-2 1K 9:16 | `references/prompts/r3-palette-matieres.txt` | — | 0f6faeab41ae12d440ded1c0965b9c8a | success | `sorties/references/r3-palette-matieres-v1.png` | rejetée : codes couleur écrits, un faux | 8 cr |
| R4 spécimen | v1 | nano-banana-2 1K 9:16 | `references/prompts/r4-specimen-titres.txt` | — | 89c72ba3f8876c8165d5d97948d97d47 | success | `sorties/references/r4-specimen-titres-v1.png` | **retenue** | 8 cr |
| R1 couverture | v2 | nano-banana-2 2K 2:3 | `references/prompts/r1-couverture-v2.txt` | — | e780309ed1f711122434ce7eb500ccbc | success | `sorties/references/r1-couverture-v2.png` | rejetée : front et cils visibles | 12 cr |
| R3 palette | v2 | nano-banana-2 1K 9:16 | `references/prompts/r3-palette-matieres-v2.txt` | — | 78712e8aaee78ef1ce0c36029648012b | success | `sorties/references/r3-palette-matieres-v2.png` | **retenue** | 8 cr |
| R1 couverture | v3 (retouche) | nano-banana-2 2K 2:3 | `references/prompts/r1-couverture-v3-retouche.txt` | R1 v2 | ddd14ca5edc347aa3229ceac29871da2 | success | `sorties/references/r1-couverture-v3.png` | rejetée : retouche sans effet | 12 cr |
| R1 couverture | v4 | nano-banana-2 2K 2:3 | `references/prompts/r1-couverture-v4.txt` | — | 970e648a05c4b08a62958e3eafa97b36 | success | `sorties/references/r1-couverture-v4.png` | **retenue** | 12 cr |
| R2 packshot | v1 | nano-banana-2 2K 4:5 | `references/prompts/r2-packshot.txt` | R1 v4 | a6203cb0ce37bae7aeae157cdc830243 | success | `sorties/references/r2-packshot-v1.png` | **retenue** | 12 cr |
| P01 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P01.txt` | R3, R4 | b28af8ab647841620e70c61566dfa0a9 | success | `sorties/plans/P01-img-v1.png` | **retenue** | 12 cr |
| P02 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P02.txt` | R3, R4 | a6ace702f891e50d176205555e599265 | success | `sorties/plans/P02-img-v1.png` | rejetée : visage visible | 12 cr |
| P02 image | v2 | nano-banana-2 2K 9:16 | `prompts/img-v2/P02.txt` | R3, R4 | cf09f583f5d50f3b0ddc2fd21d213519 | success | `sorties/plans/P02-img-v2.png` | **retenue** | 12 cr |
| P03 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P03.txt` | R3, R4 | 4c8339c574d7cb84419a1465c3af8633 | success | `sorties/plans/P03-img-v1.png` | **retenue** | 12 cr |
| P04 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P04.txt` | R3, R4 | ff9eebd2724e88763b8ea9426bc51515 | success | `sorties/plans/P04-img-v1.png` | rejetée : « COUPÉ COURTÉ » | 12 cr |
| P04 image | v2 | nano-banana-2 2K 9:16 | `prompts/img-v2/P04.txt` | R3, R4 | 9e7e135f67717a138c7dd6b10a404724 | success | `sorties/plans/P04-img-v2.png` | **retenue** | 12 cr |
| P05 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P05.txt` | R3, R4 | 6fb74fe22d5191070f91e652cb8a2c4c | success | `sorties/plans/P05-img-v1.png` | **retenue** | 12 cr |
| P06 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P06.txt` | R3, R4 | d45b85ec7c3e06792236d16620906361 | success | `sorties/plans/P06-img-v1.png` | rejetée : portrait de femme (personnage) | 12 cr |
| P06 image | v2 | nano-banana-2 2K 9:16 | `prompts/img-v2/P06.txt` | R3, R4 | 2b78aabcf984d777548fe353bd458bda | success | `sorties/plans/P06-img-v2.png` | **retenue** | 12 cr |
| P07 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P07.txt` | R3, R4 | 858c78ddcf2c20de4347470eb94d4173 | success | `sorties/plans/P07-img-v1.png` | rejetée : « QUIANTITÉ » | 12 cr |
| P07 image | v2 | nano-banana-2 2K 9:16 | `prompts/img-v2/P07.txt` | R3, R4 | 2b570ace33d1488e652f010b417f2939 | success | `sorties/plans/P07-img-v2.png` | **retenue** | 12 cr |
| P08 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P08.txt` | R3, R4 | f18089ce30716abd3a5b179626020cc6 | success | `sorties/plans/P08-img-v1.png` | rejetée : « CUÍR » | 12 cr |
| P08 image | v2 | nano-banana-2 2K 9:16 | `prompts/img-v2/P08.txt` | R3, R4 | 828fec9ea197a3af90895402da0a5c97 | success | `sorties/plans/P08-img-v2.png` | **retenue** | 12 cr |
| P09 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P09.txt` | R3, R4 | abd960711cdb41b65568d894af77ac26 | success | `sorties/plans/P09-img-v1.png` | **retenue** | 12 cr |
| P10 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P10.txt` | R3, R4 | 1858cdea102add6d6094b3802219a7f7 | success | `sorties/plans/P10-img-v1.png` | rejetée : « pas aux ciseaux » recopié | 12 cr |
| P10 image | v2 | nano-banana-2 2K 9:16 | `prompts/img-v2/P10.txt` | R3, R4 (sans R4) | f08e30c7abf4cae678100420c0f9e40e | success | `sorties/plans/P10-img-v2.png` | **retenue** | 12 cr |
| P11 image | v1 | nano-banana-2 2K 9:16 | `prompts/img/P11.txt` | R3, R4, R2 | d859fda8b24de783b8d6e298871cc66f | success | `sorties/plans/P11-img-v1.png` | **retenue** | 12 cr |
| P01 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P01.txt` | 1re image `retenues/plans/P01.png` | 035f062051b48c3fcd22712df4bc70c7 | success | `sorties/clips/P01-clip-v1.mp4` | **retenu** | 63 cr |
| P02 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P02.txt` | 1re image `retenues/plans/P02.png` | 7a9f7e5c3c39d9f61312eb507f60ee70 | success | `sorties/clips/P02-clip-v1.mp4` | **retenu** | 63 cr |
| P03 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P03.txt` | 1re image `retenues/plans/P03.png` | 775ca3dfba19b677394267736935bf16 | success | `sorties/clips/P03-clip-v1.mp4` | **retenu** | 63 cr |
| P04 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P04.txt` | 1re image `retenues/plans/P04.png` | c5836d561e643f95340ce3aa3957996b | success | `sorties/clips/P04-clip-v1.mp4` | **retenu** | 63 cr |
| P05 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P05.txt` | 1re image `retenues/plans/P05.png` | acaa0f6b1ba591e638e862c90d2bdf10 | success | `sorties/clips/P05-clip-v1.mp4` | **retenu** | 63 cr |
| P06 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P06.txt` | 1re image `retenues/plans/P06.png` | 663e7c4d0bc5ef23398953d647e8fe68 | success | `sorties/clips/P06-clip-v1.mp4` | retenu (flou de mouvement du tampon vers 0,9 s) | 63 cr |
| P07 clip | v1 | gemini-omni-flash-1-1 1080p 6 s | `prompts/ani/P07.txt` | 1re image `retenues/plans/P07.png` | 2600f8643c613e908607b3dfcff8aef6 | success | `sorties/clips/P07-clip-v1.mp4` | retenu, recalé au montage par gels de pose (étiquettes sur chaque « ni ») | 84 cr |
| P08 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P08.txt` | 1re image `retenues/plans/P08.png` | 99c4b707d6321a8f0f8317aecb84dbee | success | `sorties/clips/P08-clip-v1.mp4` | **retenu** | 63 cr |
| P09 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P09.txt` | 1re image `retenues/plans/P09.png` | fb793930414392f90039eac2d91a06a8 | success | `sorties/clips/P09-clip-v1.mp4` | **retenu** | 63 cr |
| P10 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P10.txt` | 1re image `retenues/plans/P10.png` | a22d2d91861f70e1844f866b27121767 | success | `sorties/clips/P10-clip-v1.mp4` | **retenu** | 63 cr |
| P11 clip | v1 | gemini-omni-flash-1-1 1080p 4 s | `prompts/ani/P11.txt` | 1re image `retenues/plans/P11.png` | 91ef37af9c5754183236370b69dfa5d0 | success | `sorties/clips/P11-clip-v1.mp4` | retenu, 0,00-0,90 s écarté (doublon du livret), gardé 0,90-3,32 s | 63 cr |

**Références : 84 crédits. Plans (images + clips) : 918 crédits. Total : 1 002 crédits ≈ 5,01 $.** Solde KIE : 9 280,8 → 8 278,8 crédits (vérifié).

Contrôles clips : aucune parole détectée (Whisper) dans les 11 pistes audio, seulement des bruitages papier.
