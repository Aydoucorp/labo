# B-rolls 3D explicites (retour de l'utilisateur : les 3D de la bibliothèque n'illustrent pas assez la parole)

Principe : chaque plan montre littéralement la phrase dite, on comprend sans le son. Même style pour les 5 plans :
rendu 3D médical propre et pédagogique, fond crème clair uni, peau et follicules en tons pêche et rose, accents terracotta, lumière douce de studio, caméra lente.
Les étiquettes (mots, flèches) sont ajoutées au montage, en français et aux couleurs de Claire : les prompts demandent zéro texte (les modèles vidéo déforment les lettres).
Chaque plan : une image de départ, puis une vidéo à partir de cette image.

Bloc de style (à garder au début de chaque prompt) :
`Clean educational 3D medical animation, vertical 9:16, plain soft cream background, skin and hair follicles in soft peach and pink tones with terracotta accents, soft studio lighting, smooth slow camera, premium scientific explainer style like a high-end health documentary. No text, no letters, no labels, no numbers, no logo.`

## B2 (21,70 à 24,90 s) : « …le cycle de pousse se raccourcit »
Étiquette montage : « CYCLE DE POUSSE » puis « DE PLUS EN PLUS COURT ».
- Image : `[bloc de style] Side cross-section of a single hair follicle in the skin, a long healthy dark hair growing out of it, next to it a large circular ring around the follicle split into a long terracotta arc (growth phase) and a short grey arc (resting phase).`
- Vidéo (4 s) : `[bloc de style] Starting from the input image: the hair grows long, then falls out; a new hair starts growing but stops at half the length and falls out sooner; at the same time the terracotta growth arc of the ring visibly shrinks to half its size while the grey resting arc gets bigger. Clear cause and effect, the shortening is obvious at a glance.`

## B3 (24,90 à 27,85 s) : « …les follicules de cette zone se fragilisent »
Étiquette montage : « FOLLICULE FRAGILISÉ ».
- Image : `[bloc de style] Close-up cross-section of one hair follicle in the skin, healthy and plump, a thick dark hair, warm healthy glow around the bulb.`
- Vidéo (3 s) : `[bloc de style] Starting from the input image: the follicle slowly shrinks and weakens, the bulb gets smaller and paler, the warm glow fades, the hair becomes thinner and lighter, fine cracks appear in the follicle wall; slow push-in on the bulb.`

## B4 (29,40 à 34,45 s) : « …tes tempes ont certains des follicules les plus fins et les plus délicats de tout ton cuir chevelu »
Étiquettes montage : « TEMPES » sur la zone, puis « FINS ET FRAGILES » contre « ÉPAIS ET SOLIDES ».
- Image : `[bloc de style] Semi-transparent 3D head of a woman seen in three-quarter view, long hair suggested as a soft translucent shape, the temple area on the side of the forehead softly highlighted in terracotta.`
- Vidéo (5 s) : `[bloc de style] Starting from the input image: the camera glides in toward the highlighted temple and dives under the skin, revealing a row of follicles: on the left, follicles from the top of the head, big bulbs with thick strong hairs; on the right, the temple follicles, tiny bulbs with very thin delicate hairs. The difference in thickness is striking and obvious.`

## B5a (44,25 à 49,05 s) : « Pendant la périménopause et la ménopause, les fluctuations hormonales touchent d'abord les tempes »
Étiquettes montage : « PÉRIMÉNOPAUSE », « HORMONES ».
- Image : `[bloc de style] Semi-transparent 3D silhouette of a woman's head and shoulders, front view, a glowing wavy line (like a hormone level curve) floating in front of her chest.`
- Vidéo (5 s) : `[bloc de style] Starting from the input image: the wavy hormone curve swings up and down irregularly, and with each swing soft pink particles travel up through the body to the head; both temples are the first areas to light up in terracotta and pulse, while the rest of the scalp stays calm.`

## B5b (49,05 à 52,00 s) : « Ton œstrogène baisse, ton cortisol augmente… »
Étiquettes montage : « ŒSTROGÈNE ↓ » sur la gauche, « CORTISOL ↑ » sur la droite.
- Image : `[bloc de style] Cross-section of a temple hair follicle in the centre, on the left a glass level gauge filled high with soft pink glowing particles, on the right a glass level gauge filled low with orange particles.`
- Vidéo (3 s) : `[bloc de style] Starting from the input image: the pink gauge on the left drains down quickly and its pink particles around the follicle fade away, while the orange gauge on the right fills up and orange particles flood around the follicle, which tightens and turns slightly red, irritated.`
