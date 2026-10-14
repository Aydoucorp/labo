# Journal de production : UGC Claire lavage

| Date | Élément | Version | Modèle et réglages | Références | Tâche KIE | Coût | Statut et défauts |
|---|---|---|---|---|---|---|---|
| 2026-10-14 | Image de départ | v1 | GPT Image 2 image vers image, 1K, 9:16, `prompts/img/depart.txt` | claire-pied, claire-visage, fond-porte | e58caea12af26d8b478d64db16284fca | 6 cr | OK. Micro bien sous la bouche, porte un peu décalée, poignée hors champ |
| 2026-10-14 | Image de départ | v2 | idem | idem | f6f904640d32653d058926d1b57df411 | 6 cr | OK. Décor plus fidèle (poignée visible), cadrage un peu plus serré, main gauche coupée en bas |
| 2026-10-14 | Image de départ | v3 | GPT Image 2 image vers image, 1K, 9:16, `prompts/img/depart-v3.txt` (rendu iPhone brut, peau réelle, pas de pose, en pleine phrase) | idem | dedf4b2b00fa0bfa3eca40e42d25e9bf | 6 cr | OK. Bouche ouverte en pleine phrase, main gauche en geste, cadre légèrement de travers |
| 2026-10-14 | Image de départ | v4 | idem, `prompts/img/depart-v4.txt` (entre deux mots, demi-sourire) | idem | 9c47a72291c0ef11a547e9a6425370e9 | 6 cr | OK. Lèvres fermées, micro avec bonnette, pose détendue |
| 2026-10-14 | Clip F1 (accroche, 0 à 9,50 s) | v1 | Seedance 2.5, 720p, 9:16, 10 s, generate_audio, `prompts/video/F1.txt` | @Image1 `retenues/depart.png` (v4), @Video1 `audio/extraits/F1_ecran-noir.mp4` | d169e474350d7d056d189f417eb7527e | 760 cr | Image naturelle, identité, micro et décor stables, gestes conformes à la timeline. Synchro (enveloppe audio Seedance / voix) : ±20 ms de 0 à 4,5 s ; après 4,5 s le son Seedance devient du charabia, mesure non fiable, contrôle visuel nécessaire. Version montage : `sorties/clips/F1-v1_voix-origine.mp4` |
