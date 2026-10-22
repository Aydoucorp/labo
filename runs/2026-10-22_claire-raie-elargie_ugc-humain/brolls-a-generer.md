# B-rolls : format hybride (C4 et C6 sans visage)

Les clips C4 et C6 ne sont plus générés en Wan : la voix ElevenLabs passe sur des b-rolls.
Wan 3.0 ne fait plus que C1, C2, C3, C5, C7 (29 s, écran noir) : environ 464 cr, soit 2,32 $.

## C4 (15,86 à 23,52 s)
| Moment | Texte | Plan | Source |
|---|---|---|---|
| 15,86 à 20,30 | À chaque cycle de pousse, le cheveu revient un peu plus fin… un peu plus fragile | Animation 3D : follicule qui rétrécit en trois temps | bibliothèque br-0015 (gratuit) |
| 20,35 à 23,52 | jusqu'au jour où ta queue de cheval te paraît deux fois moins épaisse | Queue de cheval fine tenue dans la main | **à trouver (réel) ou à générer par l'utilisateur : prompt P1** |

## C6 (30,40 à 37,59 s)
| Moment | Texte | Plan | Source |
|---|---|---|---|
| 30,40 à 32,10 | Tu dois soutenir le follicule. | Animation 3D : le cheveu continue de pousser, particules dorées | bibliothèque br-0013 (gratuit) |
| 32,38 à 35,20 | Tu dois calmer cette inflammation au niveau du cuir chevelu | Animation 3D : cuir chevelu rouge enflammé qui se calme | **à générer par l'utilisateur : prompt P2** |
| 35,28 à 37,59 | avant que tes cheveux ne s'affinent encore davantage | Jeune femme brune qui écarte sa raie | bibliothèque br-0070, réel (gratuit) |

## P1 : queue de cheval fine (4 s, 9:16)
Si une vidéo réelle existe (filmée ou trouvée), elle passe avant ce prompt.

```
Vertical 9:16 smartphone video, 4 seconds. Seen from behind and slightly to the side, a woman in her mid forties with long medium-dark brown hair stands in a bright bathroom in front of a mirror. She has pulled her hair into a low ponytail and holds the ponytail in one hand just below the hair tie, squeezing it between her fingers to show how thin and sparse it has become: the ponytail is visibly thin, barely thicker than a finger, the ends wispy and see-through. She slowly lifts it a little toward the camera, then lets it drop. Her face is not visible. Natural daylight, shot on iPhone, realistic skin and hair texture, slight handheld feel, no text, no logo.
```

## P2 : inflammation du cuir chevelu qui se calme (4 s, 9:16)
Mettre `references/style-3d-follicule.jpg` en image de départ ou de style pour garder le rendu de la bibliothèque.

```
3D medical animation, vertical 9:16, 4 seconds, same style as the reference image: a cutaway block of scalp skin floating on a dark plum background, soft pink skin layers, a cream fat layer at the bottom, one hair follicle with its hair in the centre, soft studio lighting, clean premium medical render. At the start, the skin around the follicle is swollen and glows an angry red, with small red inflammation particles pulsing around the bulb, and the hair looks thin. Over the 4 seconds, the red glow cools down and fades into a calm healthy pink, the particles dissolve, the bulb plumps up slightly and the hair looks a bit stronger. Slow gentle push-in camera. No text, no labels, no logo.
```

## Mise à jour : b-rolls non 3D faits à partir de l'avatar (choix de l'utilisateur)
Image en entrée : `sorties/cadrage-v2.png` (même avatar, même tenue, même décor que les clips Wan). Pas de parole sur ces plans : bouche fermée, la voix ElevenLabs passe par-dessus.
P1 ci-dessus est remplacé par P1-avatar ; P3-avatar remplace br-0070 (35,28 à 37,59 s), br-0070 reste en secours.

### P1-avatar : queue de cheval fine (5 s)
```
Vertical 9:16 smartphone video, 5 seconds, continuing from the input image: same woman, same red and white striped T-shirt, same room, same fixed phone camera, no camera movement. She does not speak, mouth closed. She gathers her hair into a low ponytail over her right shoulder with both hands, then brings the ponytail forward close to the lens and wraps her thumb and index finger around it just below the hair tie, showing how thin it has become: the ponytail is visibly thin and sparse, the ends wispy and see-through. She looks at it, then at the lens with a disappointed, slightly worried expression and a small sigh. Natural daylight from the front-left, realistic hair and skin texture, shot on iPhone, no text, no logo.
```

### P3-avatar : elle écarte sa raie (4 s)
```
Vertical 9:16 smartphone video, 4 seconds, continuing from the input image: same woman, same red and white striped T-shirt, same room, same fixed phone camera, no camera movement. She does not speak, mouth closed. She bows her head toward the lens so the top of her head fills the upper part of the frame, and with the fingertips of both hands she parts her hair along the centre parting, showing a widened part line with the scalp visible along it and finer, sparser hair on each side. She holds the parting open for a moment, the hair slightly trembling between her fingers. Natural daylight from the front-left, sharp detail on the hair strands and scalp, realistic, shot on iPhone, no text, no logo.
```

## Mise à jour 2 : images debout générées par l'utilisateur, puis vidéos
Input des images : `sorties/cadrage-v2.png`. I1 (debout de face) donne la vidéo V-raie, I2 (debout de profil, queue de cheval) donne la vidéo V-queue.

### I1 : debout, de face
```
Using the input image as the strict reference, create a new photo of the exact same woman: identical face, facial features, skin texture with freckles and fine lines, brown eyes, apparent age (mid forties), identical long wavy medium-dark brown hair with a centre parting, same red and white striped short-sleeve T-shirt, white smartwatch on her left wrist, thin black hair tie on her right wrist. Do not beautify her skin.
This time she is standing, facing the camera squarely, in the same room: blue-grey wainscoting and off-white wall behind her, beige linen curtain on the right. Medium shot from the top of her head to the hips, phone at eye level on a stand, both arms relaxed along her body, calm neutral expression, mouth closed, looking into the lens. Her centre parting is clearly visible and slightly wide.
Natural soft window light from the front-left, shot on iPhone, realistic smartphone photo, deep depth of field, vertical 9:16. No text, no logo, no watermark.
```

### I2 : debout, de profil, queue de cheval
```
Using the input image as the strict reference, create a new photo of the exact same woman: identical face, facial features, skin texture with freckles and fine lines, brown eyes, apparent age (mid forties), same medium-dark brown hair colour, same red and white striped short-sleeve T-shirt, white smartwatch on her left wrist. Do not beautify her skin.
This time she is standing in strict side profile, facing the left of the frame, in the same room: blue-grey wainscoting and off-white wall behind her, beige linen curtain at the right edge. Her hair is pulled back into a low ponytail at the nape of her neck with a thin black hair tie: the ponytail is noticeably thin and sparse, barely thicker than a finger, the ends wispy and see-through, a few fine flyaways at the hairline. Medium shot from the top of her head to the hips, phone at eye level on a stand, arms relaxed, calm slightly worried expression, mouth closed.
Natural soft window light from the front-left, shot on iPhone, realistic smartphone photo, deep depth of field, vertical 9:16. No text, no logo, no watermark.
```

### V-raie (à partir de I1, 4 s), sur « …avant que tes cheveux ne s'affinent encore davantage »
```
Vertical 9:16 smartphone video, 4 seconds, starting from the input image: same woman, same room, fixed phone camera, no zoom. She does not speak, mouth closed. She steps a little closer to the lens and bows her head forward so the top of her head comes toward the camera, then with the fingertips of both hands she parts her hair along the centre parting, showing a widened part line with the scalp visible along it and finer, sparser hair on each side. She holds the parting open for a moment. Natural daylight, sharp detail on the hair strands and scalp, realistic, shot on iPhone, no text, no logo.
```

### V-queue (à partir de I2, 5 s), sur « …ta queue de cheval te paraît deux fois moins épaisse »
```
Vertical 9:16 smartphone video, 5 seconds, starting from the input image: same woman in side profile, same room, fixed phone camera, no zoom. She does not speak, mouth closed. She reaches back with her right hand, takes her thin ponytail and brings it forward over her shoulder, then wraps her thumb and index finger around it just below the hair tie and slides her fingers down to the wispy ends, showing how thin and sparse it is. She looks down at it with a disappointed, slightly worried expression and a small sigh. Natural daylight, realistic hair and skin texture, shot on iPhone, no text, no logo.
```

## Mise à jour 3 : vidéos plus dynamiques, cadrées sur la queue de cheval et la raie (demande de l'utilisateur)
Remplacent V-raie et V-queue ci-dessus.

### V-queue-v2 (à partir de I2, 5 s)
```
Vertical 9:16 handheld smartphone video, 5 seconds, starting from the input image, then the phone moves in fast: within the first second the camera swings in close behind her shoulder so her ponytail fills most of the frame; her face stays out of frame or only as a soft edge, the ponytail is the subject. Dynamic real gestures, never stiff: with a quick flick of her head and her right hand she whips the thin ponytail forward over her shoulder toward the lens, grabs it at the hair tie and squeezes it tight in her fist to show how little hair there is, then pulls her fingers fast down the full length so the strands separate and the see-through wispy ends spread apart, gives it a little shake, and lets it drop limp against her shoulder. Natural handheld micro-shake, natural daylight, sharp detail on the strands, realistic, shot on iPhone, no text, no logo. She does not speak.
```

### V-raie-v2 (à partir de I1, 4 s)
```
Vertical 9:16 handheld smartphone video, 4 seconds, starting from the input image, then the phone moves in fast: she bends her head forward toward the lens in one quick movement while the camera pushes in close above her, so the top of her head and her centre parting fill the frame; her face is out of frame, the parting is the subject. Dynamic real gestures, never stiff: with the fingertips of both hands she briskly flips the hair from one side of the parting to the other, then spreads it wide apart along the part line in two quick strokes, revealing a widened parting with the scalp clearly visible and fine sparse hair on each side, and runs one fingertip along the bare line. Natural handheld micro-shake, natural daylight, sharp detail on the hair strands and scalp, realistic, shot on iPhone, no text, no logo. She does not speak.
```

## Mise à jour 4 : raie trop normale sur le premier essai (retour de l'utilisateur)
Cause : l'image de départ (I1, debout de face) montre des cheveux épais ; le modèle vidéo ne crée pas seul une raie élargie.
Correction : image de départ dédiée, déjà en gros plan sur la raie élargie, puis vidéo à partir de cette image.
Inputs de l'image : `sorties/cadrage-v2.png` (Image 1, l'avatar) + `references/raie-elargie-ref.png` (Image 2, moitié gauche de l'insert Nano Banana : l'aspect de la raie).

### I3 : gros plan raie élargie
```
Image 1 is the woman: same medium-dark brown hair colour and texture, same red and white striped T-shirt, same skin tone and hands, white smartwatch on her left wrist. Image 2 shows exactly how her parting must look: copy its widened part line and diffuse thinning.
New photo, vertical 9:16, shot on iPhone from directly above her head: she bends her head down toward the lens, the top of her head and her centre parting fill most of the frame, her face is not visible, only a bit of her forehead at the bottom edge and the red and white stripes of her T-shirt at the bottom corners. With the fingertips of both hands she holds the hair apart on each side of the parting. The parting is clearly widened like in Image 2: a broad diffuse band of pink scalp along the centre line, about two fingers wide, widening toward the crown, with sparse fine short hairs inside it and thinner, see-through hair on each side; not a normal thin parting line. Natural soft window light, sharp detail on the hair strands and scalp, realistic, no beauty filter. No text, no logo, no watermark.
```

### V-raie-v3 (à partir de I3, 4 s)
```
Vertical 9:16 handheld smartphone video, 4 seconds, starting from the input image and keeping the same close-up from above: the widened parting stays the subject and stays wide and clearly visible during the whole video, never fuller or denser than in the input image. Dynamic real gestures, never stiff: with her fingertips she briskly spreads the hair further apart along the part line in two quick strokes, the scalp showing more and more, then runs one fingertip slowly along the bare pink line from the front toward the crown, and slightly tilts her head so the light catches the bare scalp. Natural handheld micro-shake, natural daylight, sharp detail on the hair strands and scalp, realistic, shot on iPhone, no text, no logo. She does not speak.
```

## Reçu
- `rushes/v-raie-utilisateur-v1.mp4` (8 s, 720x1280, IA générée par l'utilisateur à partir de I3) : raie élargie bien visible du début à la fin, gestes des doigts de 1,0 à 3,5 s. Fenêtre retenue pour le montage : environ 1,0 à 3,4 s (pour 35,28 à 37,59 s de la voix). Validée par Claude, en attente de l'avis de l'utilisateur.
