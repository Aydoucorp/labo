# Règles de montage : ce que build_timeline.py applique et ce que tu peux ajuster

Le montage dynamique vient à 80 % du calage sur la voix et de l'alternance des plans, à 20 % des effets. La grammaire ci-dessous est implémentée dans `scripts/build_timeline.py` ; tu peux la surcharger en éditant `work/timeline.json` avant le rendu (chaque clip porte sa `transition_in`, son `kenburns`, son `punch`, sa `speed`).

## 1. Calage

- Un plan commence à `shot.start` du brief, qui a déjà été placé 0,3 à 0,5 s avant le mot pivot (voir `segmentation.md`). Le montage ne recalcule pas ce point.
- Le son d'ambiance du rush entrant démarre en même temps que son image (le J-cut audio d'une demi-seconde est une option future ; pour l'instant l'ambiance à -25 dB suffit à « ancrer » le plan).
- Le dernier clip finit exactement à la fin de l'audio ; aucun trou, aucune image morte.

## 2. Grammaire des transitions (`transition_in` du clip entrant)

| Contexte de la coupe | Transition | Frames | Son |
|---|---|---|---|
| Réel → 3DSCI ou 3DSCI → réel (priorité 1, même à l'intérieur d'une séquence) | `zoomthrough` (on rentre dans la matière, on en ressort) | 8 | whoosh |
| Même séquence (03a → 03b) ou même section | `cut` | 0 | ambiance seulement |
| Changement de section | famille du profil : `whip` (ADS) ou `zoomthrough` (EDU), direction alternée gauche/droite | 8 | whoosh -14 dB |
| Fin du HOOK → plan suivant | `flash` (autorisé seulement en sortie de HOOK) | 3 | whoosh |
| Avant/après (descriptions ou `must_show` contiennent avant et après) | `wipe` | 8 | whoosh court |
| EDU seulement, deux plans calmes (énergie <= 2, caméra statique) | `dissolve` | 10 | aucun |
| Tout le reste | `cut` | 0 | aucun |

Garde-fous : après une transition visible, toute autre transition visible dans les `visible_max_per_window_s` (8 s) suivantes redevient un cut, sauf le zoomthrough d'entrée ou de sortie de 3DSCI qui passe toujours (et réinitialise la fenêtre), parce qu'il porte du sens et non de la décoration ; une seule famille de transitions par vidéo (la famille du profil) ; le tout premier clip est un cut ; jamais de flash hors sortie de HOOK ; jamais de fondu au noir avant la fin.

Pourquoi si peu d'effets : chaque transition visible coûte 8 à 10 images pendant lesquelles rien de nouveau n'est lisible. Deux d'affilée et le spectateur voit le montage au lieu du contenu.

## 3. Mouvement dans le plan

- **Ken Burns** sur les plans dont la caméra est `static` et sur les images fixes : zoom de 1,00 à 1,06 (ADS) ou 1,05 (EDU), origine (0.5, 0.42), sens alterné push puis pull d'un plan statique au suivant. Jamais sur un rush déjà en mouvement (double mouvement = mal de mer).
- **Punch-in** : au plus un par clip, sur un mot appuyé (`features.emphasis`) situé hors des 8 premières et 8 dernières frames, échelle 1,10 (ADS) ou 1,08 (EDU) sur 6 frames, jamais sur deux clips consécutifs, tick doux à -18 dB.
- **Vitesse** : 1,0 par défaut. Un rush trop court est rattrapé dans cet ordre : ralenti jusqu'à 1/`speed_ramp_max` (0,8 en ADS), puis boomerang de son propre rush (aller-retour, muet), puis substitution par un voisin de la même séquence, puis par le même type le plus proche, puis carte MOTION. On préfère toujours le propre rush du plan, même imparfait, à l'image d'un autre plan : l'image doit confirmer la voix. Un rush lent mais long peut être accéléré jusqu'à `speed_ramp_max` pour tomber sur la coupe avec de l'énergie : édite `speed` dans la timeline si `best_window.py` signale un score de mouvement faible.
- **Fenêtre du rush** : `best_window.py` prend la portion la plus vivante, évite les 0,3 premières secondes (souvent instables) et préfère une entrée sur une montée de mouvement (cut on action).

## 4. Sous-titres

Deux styles, un seul fichier `captions.json` (mot à mot).

- **Corps (`default`)** : pages de 3 à 4 mots, Montserrat ExtraBold 68 px, blanc, contour noir 6 px, ombre douce, chaque mot apparaît avec un pop (1,15 vers 1,0 en 4 frames), le mot en cours à 1,08, les mots à venir à 85 % d'opacité. Position : centré, à 60 % de la hauteur (dans la zone sûre TikTok : jamais sous y = 1500 ni au dessus de y = 220).
- **Hook (`red-box`)**, frames avant `hook_end_frame` : mêmes mots, 76 px blanc sur boîte rouge #E0202A arrondie, centrée au milieu de l'écran, la boîte suit la largeur de la page et pop à l'entrée.
- Le texte à l'écran (overlays) ne répète jamais une phrase du sous-titre : un overlay `stat` porte un seul chiffre ou mot clé (« 97 % », « 3 s »), à 42 % de hauteur, pendant que le sous-titre continue en bas. Que ce mot soit aussi dans le sous-titre est voulu, c'est l'insistance.
- Pas de sous-titres : passer `captions.style = "none"` dans la timeline.

Pour changer de police, de taille ou de couleurs, les constantes sont en tête de `assets/remotion/src/components/Captions.tsx`. Si l'utilisateur fournit une référence visuelle de style, reproduis-la là (police, graisse, contour, ombre, animation) et documente le nouveau style sous un nouveau nom.

## 5. Son

- Voix off normalisée à `vo_lufs` (-16 LUFS) en deux passes loudnorm après le rendu, true peak -1,5 dB.
- Ambiance de chaque rush conservée à `ambience_db` (-25 dB) sous la voix ; silence si le rush n'a pas de piste.
- Whoosh sur chaque transition visible, tick sur chaque punch, impact bas sur la première frame du hook. Les trois sfx sont synthétiques (`assets/sfx/`, générés par `make_sfx.py`), donc sans licence à gérer ; l'utilisateur peut les remplacer par les siens en gardant les noms de fichiers.
- Musique optionnelle (`--music`) à `music_db` (-22 dB ADS, -24 dB EDU), constante : la voix est présente en continu, un ducking dynamique n'apporte rien ici.

## 6. Zones sûres et habillage

`profiles.json > platform_safe_zone` donne les marges par plateforme (TikTok : 220 px en haut, 420 px en bas, 60 à gauche, 130 à droite). Sous-titres, overlays, barre de progression et logo respectent ces marges. Barre de progression (`--progress-bar`) et logo (`--logo`) sont désactivés par défaut.

## 7. Rendu

- Préview 540x960 (`--preview`) pour valider le calage, puis final 1080x1920 H.264 CRF 18, 30 fps, AAC.
- Sur 2 CPU, compter environ 8 s de rendu par seconde de vidéo (le coût est l'extraction des frames vidéo, la préview n'est pas beaucoup plus rapide). Images de contrôle (`--frames`) en quelques secondes : utilise-les pour vérifier un point précis sans rendre toute la vidéo.
- Chrome : `render.py` cherche `/opt/pw-browsers/chromium` puis un headless shell Playwright, sinon laisse Remotion télécharger son navigateur. En cas de mémoire insuffisante, relance automatique en concurrence 1 avec cache réduit.

## 8. Ce qu'il faut regarder avant de livrer

La planche contact (`out/contact_sheet.jpg`, une image par plan) et le rapport `out/qc_report.md`. Les trois questions qui comptent : le premier plan change-t-il dans la première seconde ? Chaque plan montre-t-il ce que la voix dit à cet instant (compare la planche au brief) ? Y a-t-il un moment où rien ne bouge pendant plus de 5 s ? Si l'une des réponses est mauvaise, corrige la timeline ou le brief, ne corrige pas le rendu à la main.
