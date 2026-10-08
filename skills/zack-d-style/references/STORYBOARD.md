# Storyboard — règles de découpage (toute marque)

## Niveaux d'échelle
A DEHORS (perso plein pied ou buste, podium / prop island) · B SURFACE (macro de la zone, prop island avec perso minuscule) · C DEDANS (macro cutaway : coupe, follicule, cellule, mécanisme). **Un seam ne saute jamais deux niveaux** : A→B→C→B→A. Le retour A montre le RÉSULTAT de ce qui s'est passé en C.

## Beats
- NORMAL : 1 beat = 1 phrase (2 si courtes, < 5 s au total). SPEEDY : 1 beat = 1 phrase ; phrase > 3,5 s → 2 beats coupés à une virgule / « : » / « . » interne, still intermédiaire `Sxxb`.
- Chaque beat : `job` (ce que la ligne prouve) · `action` (UN verbe) · `shot type` · `angle` (low hero / top-down / orbite / macro / plongée — varier) · `couleur-état` · `seam-out`.
- Outro silencieux : podium produit dans l'anneau cyan, 3 s, fond propre pour la caption.
- Le hook ne montre pas le produit. Les chiffres (avis, clients) = numéraux or extrudés avec le perso minuscule devant.

## Squelette validé (run de référence dermato v3/v4, transposable à toute marque)
hook A (situation gênante) → B macro du problème → C colonie/cause glow cyan → C se nourrit (jaune) → C acides / rouge → B rayon X cellules → B plaques géantes + perso minuscule → A/B solutions rejetées gris (prop island produits géants sans marque) → C intact (« la racine n'a rien vu ») → C flèche rouge (cycle) → A créateurs cassent la flèche + posent le produit dans l'anneau → podium produit ouvert → C bleu/cyan descend → C cause disparaît → B surface calme vert → A résultat (perso) → A chiffres or → podium outro.

## Timings
`shots_timing.json` donne début/fin par ligne. Un leg va du début de sa ligne au début de la ligne suivante (les blancs de VO sont absorbés). `target_s` = cette durée ; `duration` Kling = 5 (normal) ou 3 (speedy) ; écart de vitesse toléré ±30 %, sinon recouper.
