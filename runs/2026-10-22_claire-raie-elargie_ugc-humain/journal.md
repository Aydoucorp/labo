# Journal : UGC raie élargie

| Date | Étape | Version | Réglages | Entrées | Task id | Coût | Résultat |
|---|---|---|---|---|---|---|---|
| 2026-10-22 | Clip C1 | v1 | `wan/3-0-video` 480P 9:16, 3 s, audio activé, `prompts/video/C1.txt` | @Image1 `sorties/cadrage-v2.png`, @Image2 `casting/de-face.png`, @Video1 `audio/clips/C1_ecran-noir.mp4` | a64b0f6fbd50ae97826ccaad56d05124 | 48 cr | Mots 11/13 (Whisper entend « t'as l'aise » sur les deux sons), écart max 0,02 s ; lèvres 1/1 |
| 2026-10-22 | Clip C2 | v1 | idem, 6 s | idem, C2 | 266fc8a690b99bc7d2f04627ee95dcf2 | 96 cr | Mots 18/18, écart max 0,02 s ; lèvres 3/3 ; geste sur la raie conforme |
| 2026-10-22 | Clip C3 | v1 | idem, 7 s | idem, C3 | abae203b27bf134df672c0e2af812442 | 112 cr | Mots 22/22, écart max 0,08 s ; lèvres 4/4 |
| 2026-10-22 | Clip C5 | v1 | idem, 7 s | idem, C5 | 6ecdfb7b5f9c20ccb47fe0dec9901760 | 112 cr | Mots 21/21 ; « Et » en avance de 0,34 s, puis retard de 0,10 à 0,12 s jusqu'à la fin ; lèvres 1/1 |
| 2026-10-22 | Clip C7 | v1 | idem, 6 s | idem, C7 | 43902336f16eb42c2061c41229973676 | 96 cr | Mots 26/26, avance constante de 0,12 s (lèvres 3/3 une fois la voix avancée de 0,12 s au montage). **Défaut : elle porte le pull crème de @Image2 au lieu de la marinière**, et le cadre se resserre. Relance à proposer (96 cr), sans @Image2. |

Total clips : 464 cr. Détails : `controle/` (mots, lèvres, planches). Aperçus avec la voix ElevenLabs : `sorties/apercus/`.
| 2026-10-22 | Clip C1 | v2 | 4 s, 0,5 s de silence en tête de la voix (`audio/clips/C1-pad_ecran-noir.mp4`), sans @Image2, tenue verrouillée (`prompts/video/C1-v2.txt`) | @Image1 `sorties/cadrage-v2.png` | 0eca5dbcd4a17ffb15a668466c0f2aa4 | 64 cr | Relancé à la demande de l'utilisateur (décalage perçu sur v1). Mots écart max 0,06 s, lèvres 1/1, marinière. Les 0,5 s de tête sont coupées au montage. |
| 2026-10-22 | Clip C7 | v2 | 6 s, sans @Image2, tenue et cadre verrouillés (`prompts/video/C7-v2.txt`) | @Image1 `sorties/cadrage-v2.png` | 152e8aaf57c3292390c2df20c18610aa | 96 cr | Marinière, cadre stable, mots 26/26 sans décalage (moyenne 0,00 s), lèvres 3/3. |
| 2026-10-22 | Montage v1 | v1 | `work/montage.py` | voir `montage.md` | | 0 | `montage/final_9x16.mp4`, 43,7 s |

Total du run : 21,6 cr d'images + 624 cr de clips = 645,6 cr (environ 3,23 $).
