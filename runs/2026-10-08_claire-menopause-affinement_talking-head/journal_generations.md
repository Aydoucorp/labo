# Journal des générations · Claire · Affinement ménopause · Talking head n°2

Tarif KIE : 1 crédit ≈ 0,005 $.

| Étape | Variante | Modèle | ID de tâche | État | Fichier | Statut | Coût |
|---|---|---|---|---|---|---|---|
| Test image de départ 9:16 (pull bleu) | gpt v1 | gpt-image-2-image-to-image 1K | c12d918776e7f69412a4c9380229d58b | success | `sorties/config/depart_9x16_gpt_v1.png` | **retenue** (choix : GPT Image 2) | 6 cr |
| Test image de départ 9:16 (pull bleu) | gpt v2 | gpt-image-2-image-to-image 1K | 06b065ceda911a77bd3c970d1db4d4c5 | success | `sorties/config/depart_9x16_gpt_v2.png` | non retenue | 6 cr |
| Test image de départ 9:16 (pull bleu) | nb21 v1 | nano-banana-2-1 1K | abcc376186f63591c092924a38e93d2d | success | `sorties/config/depart_9x16_nb21_v1.png` | non retenue | 4 cr |
| Test image de départ 9:16 (pull bleu) | nb21 v2 | nano-banana-2-1 1K | 2bb024d54559886e448ede709ca76fb5 | success | `sorties/config/depart_9x16_nb21_v2.png` | non retenue | 4 cr |

| Image de départ 9:16 deuxième caméra | v1 | gpt-image-2-image-to-image 1K | ce7f7d4b7cbfe00cfc4c5f9e682d33ab | success | `sorties/config/depart_9x16_camera2_gpt_v1.png` | non retenue (angle peu marqué, environ 15°) | 6 cr |
| Image de départ 1:1 | v1 | gpt-image-2-image-to-image 1K | 4b1b3c70aa5bebb43854232c4af5d57f | success | `sorties/config/depart_1x1_gpt_v1.png` | à valider | 6 cr |
| Image de départ animation E1 (9:16) | v1 | gpt-image-2-text-to-image 1K | e44d5977c39aeb68eeb44017398bb280 | success | `generations/image-E1_v1.png` | à valider | 6 cr |
| Image infographie I1 (1:1) | v1 | gpt-image-2-text-to-image 1K | 8d2ebc59ff6dbc2a58d521cab5b41617 | success | `generations/image-I1_v1.png` | à valider | 6 cr |
| Image infographie I2 (1:1) | v1 | gpt-image-2-text-to-image 1K | eb028314132be5b1205e21a7a8b15319 | success | `generations/image-I2_v1.png` | à valider | 6 cr |
| Objet O1 collagène (1:1, fond vert détouré) | v1 | gpt-image-2-text-to-image 1K | b2554d2bf1b7ff9ce314e408df9926ad | success | `generations/objet-O1_v1.png` | à valider | 6 cr |
| Image de départ 9:16 deuxième caméra | v2 | gpt-image-2-image-to-image 1K, refs : départ principale, photo de profil, photo de face, prompt `depart-9x16-camera2-v2.txt` | c873c96aa38bbac4081e3a7c61e17dcb | success | `sorties/config/depart_9x16_camera2_gpt_v2.png` | à valider (angle environ 35°, nettement différent) | 6 cr |
Références envoyées (dans cet ordre) : `Claire/avatar/avatar-face.jpg`, `Claire/avatar/avatar-profil.jpg`, `Claire/talking-head/_config/depart_9x16.png`. Prompt : `prompts/config/depart-9x16.txt`. Comparatif : `sorties/config/comparatif-depart-9x16.jpg`.

Deuxième caméra et 1:1 : générées à partir de `depart_9x16_gpt_v1.png` (+ photos de Claire). Prompts : `prompts/config/depart-9x16-camera2.txt`, `prompts/config/depart-1x1.txt`. Planche : `sorties/config/planche-images-depart.jpg`.

O1 : GPT Image 2 sur fond vert uni (#00B140), puis détourage par clé de couleur (`generations/objet-O1_v1_detoure.png`). Planche : `generations/planche-generations.jpg`.

**Total à ce stade : 62 cr (environ 0,31 $).**
