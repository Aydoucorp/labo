# Découpage : raie élargie (UGC humain, Wan 3.0 + méthode Alexis écran noir)

Voix ElevenLabs « sidonie » : 43,73 s, alignée mot à mot (`work/mots.json`, MMS CTC).
Toutes les pauses font moins de 0,5 s : pas de resserrage de la voix.
Coupes placées dans les pauses : chaque coupe devient un jump-cut, comme dans la référence (11 coupes en 36 s).

| Clip | Voix (s) | Durée Wan | Texte | Jeu (d'après la référence) |
|---|---|---|---|---|
| C1 | 0,00 à 2,82 | 3 s | Si ta raie s'élargit comme ça, cette vidéo est pour toi. | pointe vers le bas (photo des raies incrustée au montage) |
| C2 | 3,22 à 8,81 | 6 s | Cet élargissement progressif au milieu de la tête… c'est généralement une perte de densité d'origine hormonale. | mains jointes devant la poitrine, regard entendu sur « hormonale » |
| C3 | 9,14 à 15,40 | 7 s | Et voici ce que la plupart des femmes ne voient pas. Ce n'est PAS une chute spectaculaire… c'est une miniaturisation. | penchée vers l'objectif, pincement des doigts sur « miniaturisation » |
| C4 | 15,86 à 23,52 | 8 s | À chaque cycle de pousse, le cheveu revient un peu plus fin… un peu plus fragile, jusqu'au jour où ta queue de cheval te paraît deux fois moins épaisse. | explique, main ouverte ; voix plus grave sur la fin (schéma du follicule incrusté au montage au début) |
| C5 | 23,90 à 30,11 | 7 s | Couper tes pointes n'y changera rien… Le collagène n'y changera rien. Et l'ignorer n'y changera CERTAINEMENT rien. | énumération main gauche, yeux fermés et haussement d'épaules, poing sur « CERTAINEMENT » |
| C6 | 30,40 à 37,59 | 8 s | Tu dois soutenir le follicule. Tu dois calmer cette inflammation au niveau du cuir chevelu avant que tes cheveux ne s'affinent encore davantage. | ferme, urgente, mains qui appuient |
| C7 | 37,97 à 43,48 | 6 s | Si tu te reconnais, pense à t'abonner et à commenter « guide », parce que la plupart des femmes s'en rendent compte trop tard. | plus enjouée, pointe l'objectif sur « t'abonner », confidence sur la fin |

Total : 45 s générées. Chaque clip reçoit sa voix en `@Video1` écran noir (durée de la voix), et l'image de cadrage.
Coût Wan 3.0 480p (8 cr/s généré + 8 cr/s de vidéo de référence) : environ 45 × 8 + 44 × 8 ≈ 710 cr.

## Incrustations (au montage, pas dans Wan)
- 0,0 à 2,8 s : texte d'accroche en haut + photo comparative de raies en bas (image à recréer, modèle le moins cher).
- 15,9 à 19 s environ : schéma de la miniaturisation du follicule (image à recréer).
- Sous-titres mot par mot, majuscules blanches à ombre légère, à gauche à hauteur d'épaule (faits au montage, gratuits).
