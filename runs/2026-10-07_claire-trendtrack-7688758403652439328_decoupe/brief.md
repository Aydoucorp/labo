# Brief · Claire · vidéo TikTok 7688758403652439328 (chute de cheveux au brossage), découpe pour VMake

Date : 2026-10-07

## Demande

- Vidéo source : TikTok trouvée via Trendtrack (id 7688758403652439328), 16,1 s, 576×1024, 30 i/s, 482 images. Brossage de cheveux noirs mouillés, beaucoup de cheveux tombés dans la brosse, boule de cheveux collée au carrelage puis dans la douche. Texte incrusté en français tout du long : « Là ça commence à me faire peur dites moi que je suis pas la seule 😓 ».
- L'utilisateur efface le texte avec VMake (5 s max par passage), puis l'utilisateur pose lui-même son hook ; Claude réassemble les parties nettoyées.

## Découpe (à l'image près, filtre `select`, H.264 CRF 14, son AAC 192 kb/s)

| Fichier | Images | Temps |
|---|---|---|
| `sorties/a-nettoyer/partie-1_0-5s.mp4` | 0 à 149 | 0 à 5 s |
| `sorties/a-nettoyer/partie-2_5-10s.mp4` | 150 à 299 | 5 à 10 s |
| `sorties/a-nettoyer/partie-3_10-15s.mp4` | 300 à 449 | 10 à 15 s |
| `sorties/a-nettoyer/partie-4_15-16s.mp4` | 450 à 481 | 15 à 16,07 s |

## Réassemblage (`assembler.py`)

- Parties nettoyées reçues : `source/nettoyees/partie-1.mp4` à `partie-4.mp4` (576×1024, 147 / 147 / 147 / 29 images).
- VMake a retiré les 3 premières images de chaque partie (décalage mesuré par comparaison avec l'original) : chaque partie est précédée de 3 copies de sa première image, soit 482 images au total, calées sur le son d'origine continu.
- Agrandissement Lanczos en 1080×1920, H.264 CRF 18, AAC 192 kb/s, 16,07 s. Pas de texte, pas de CTA : l'utilisateur ajoute son hook.

## Sorties

- `sorties/claire-chute-brossage-sans-texte_v1.mp4` (en attente de validation), `sorties/planche-contact_v1.jpg`
