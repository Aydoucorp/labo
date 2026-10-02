# Montage : Claire, signes du mauvais après-shampoing (UGC humain, format A)

- Script : `montage/montage.py` (FFmpeg).
- Image : les 10 plans tirés des 3 clips Seedance, mis à l'échelle en 1080x1920 (lanczos), 30 i/s, son des clips coupé.
- Version 3 (demande de l'utilisateur) : au début de chaque plan, Seedance tient l'image de départ immobile 0,2 à 0,5 s, ce qui donne l'impression qu'elle est figée. Ces images sont coupées plan par plan (relevé à l'œil sur les 24 premières images de chaque plan : 0,33 / 0,33 / 0,25 / 0,25 / 0,50 / 0,42 / 0,42 / 0,25 / 0,25 / 0,17 s). Durée 28,0 s au lieu de 31,1 s.
- Les textes changent sur les coupes réellement mesurées dans le film rendu (scdet), pour éviter un décalage d'une image.
- Textes : le script de l'utilisateur, une phrase par plan (`montage/textes/01.txt` à `10.txt`), Montserrat Bold 50 px, blanc, contour noir, ombre, centré à y = 330 (sous la zone haute de TikTok), affiché pendant tout le plan.
- Musique : piste de la pub d'origine (`audio/musique-originale.m4a`, 26,5 s), prolongée par un fondu enchaîné sur elle-même à partir de 6 s pour couvrir 31 s, fondu de sortie de 1,5 s, normalisée à -14 LUFS (mesuré -13,9).
- Contrôles : 10 images de contrôle (un plan chacune), textes lisibles et hors zones de l'interface, identité de Claire constante, aucune marque visible.
- Plans découpés pour la bibliothèque : `retenues/plans/01.mp4` à `10.mp4` (bibliothèque br-0059 à br-0068).
- Point d'attention : la musique est protégée par des droits ; acceptable pour un test, à remplacer par un son commercial de TikTok pour une diffusion payante.
