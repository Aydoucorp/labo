# Contrôle qualité : ce que qc.py mesure, ce que tu regardes

## 1. Contrôles automatiques (score /100)

| Contrôle | Poids | Seuil | Correction typique |
|---|---|---|---|
| Couverture audio | 15 | 100 % de la voix couverte, aucun trou entre clips | corriger `start/end` d'un plan dans le brief ou la timeline |
| Plans trop courts | 10 | aucun clip < 0,8 s (HOOK >= 0,6 s) | fusionner deux plans ou allonger l'entrée |
| Plans trop longs | 5 | aucun clip > max de sa section (profil) | scinder en séquence de valeurs |
| Alternance des valeurs | 5 | jamais deux `value` identiques consécutives | changer la valeur d'un des deux plans |
| Réemploi de rush | 5 | même fichier source jamais réutilisé à moins de `reuse_min_gap_s` | prendre le fallback ou une autre fenêtre du rush |
| Relance visuelle | 10 | un changement (clip, punch, overlay, transition) dans chaque fenêtre de `relance_max_s` | ajouter un punch ou scinder |
| Hook | 5 | l'image change dans la première seconde | premier plan <= 1 s ou punch avant 1 s |
| Transitions espacées | 5 | transitions visibles espacées de `visible_max_per_window_s` | passer l'une des deux en cut |
| Image figée | 10 | `freezedetect` (n=0.003, d=0.8) : zéro occurrence | Ken Burns sur le plan concerné, ou autre fenêtre |
| Loudness | 10 | voix à `vo_lufs` ±1 LU | relancer la normalisation |
| Durée | 10 | fichier = durée de l'audio ±0,1 s | vérifier le dernier clip |
| Lisibilité | 10 | rendu lisible par ffprobe, h264 + aac, dimensions du profil | relancer le rendu |

Le rapport `out/qc_report.md` liste chaque contrôle avec la valeur mesurée, le seuil et la correction proposée, plus le chemin de la planche contact.

## 2. Ce que la machine ne voit pas (à faire toi-même)

Regarde la planche contact (`out/contact_sheet.jpg`, une vignette par plan, dans l'ordre) à côté du brief et réponds à quatre questions :

1. Chaque vignette montre-t-elle ce que la voix dit à cet instant ? Une vignette hors sujet = un plan à remplacer, pas une transition à ajouter.
2. Le sujet est-il entier après le recadrage 9:16 ? (Rush horizontal recadré, visage coupé, produit en bord de cadre.)
3. Les rushes ont-ils l'air d'une même série (lumière, couleurs) ? Un plan qui jure signale un lookbook non respecté à la recherche ; la normalisation colorimétrique ne le rattrape pas.
4. Le texte (sous-titres, overlays) est-il dans la zone sûre et lisible sur le fond ? Vérifie une image de contrôle sur un plan clair.

Rends 3 à 5 images de contrôle (`render.py --frames`) aux instants qui comptent : milieu du hook (boîte rouge), un mot en cours dans le corps, le milieu d'une transition visible, un punch, un overlay. Sur 2 CPU, chaque image coûte quelques secondes contre plusieurs minutes pour un rendu complet.

## 3. Avant de livrer

- Score >= 90 et aucun échec sur couverture, image figée, loudness.
- Les quatre questions ci-dessus ont une bonne réponse, ou les exceptions sont signalées à l'utilisateur.
- `out/timeline.json` est copié avec la vidéo : c'est ce fichier que l'on rééditera pour une variante (transition, musique, sous-titres) sans refaire la préparation.
