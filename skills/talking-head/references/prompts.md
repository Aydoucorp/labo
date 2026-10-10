# Gabarits de prompts

Remplis tous les champs entre crochets et retire les blocs inutiles. Ne laisse jamais « comme dans l'exemple » ni une référence absente. Prompts techniques en anglais ; la langue parlée reste celle de la voix off ; tout texte à l'écran est ajouté au montage. Aucun texte, logo ni filigrane généré. Les réglages cités sont ceux du modèle : vérifie leur nom exact et leurs limites dans l'interface ou le connecteur réellement utilisé (voir `modeles.md`).

## 1. Image de départ de l'avatar (configuration, une seule fois)

Principe Hotline : l'image fixe l'identité, la tenue, le studio, la lumière, le cadre et la posture de départ. Elle est générée à partir de la référence de l'avatar avec un modèle d'image : **GPT Image 2** en édition depuis 1 à 3 photos de l'avatar (cas normal), ou **Soul** pour un nouveau casting fictif. Résolution 1K. Deux formats de la MÊME scène.

### 1a. Plein écran, 9:16

```text
Photorealistic vertical 9:16 podcast studio portrait. The same person as in the reference images, identity strictly preserved (face shape, skin tone, hair, age, beard or makeup, glasses if any). [WARDROBE: plain solid-color shirt or knit, no logo, no text]. Seated behind a dark desk, a black podcast microphone on a boom arm in front of the lower chest, mouth fully visible and never covered. Medium shot from the waist up, head in the upper third of the frame (face between 10% and 32% of image height), a little head room. Body turned slightly three-quarter, gaze slightly off-camera toward an unseen interviewer, relaxed and confident expression, mouth closed at rest. Hands visible and free near the desk. Dark studio background with soft falloff to near black, subtle rim light on hair and shoulders, soft key light from the front side, natural skin texture, realistic proportions, cinematic podcast look. The lower quarter of the frame stays dark and simple. No extra person, no text, no logo, no watermark.
```

### 1b. Écran partagé, 1:1 (joindre AUSSI l'image 9:16 validée)

```text
Same scene, same person, same clothes, same microphone and same lighting as the attached 9:16 studio portrait. Square framing for the top half of a split screen: head and shoulders plus the microphone, face centered horizontally and placed between 18% and 50% of image height, mouth fully visible and closed at rest. Nothing important in the top 6% and bottom 6% of the frame (they will be cropped). No text, no logo, no watermark.
```

Contradictions à corriger avant validation : avatar debout alors que la scène est assise, micro devant la bouche, visage trop bas, mains déformées, tenue avec logo, micro différent entre les deux formats. Valide une image par format, puis n'y touche plus : c'est l'image de départ de TOUS les clips avatar.

## 2. Scène vidéo de l'avatar (Seedance 2.5)

**Méthode du studio, règle de l'utilisateur (validée le 2026-10-10, à appliquer à chaque clip dialogué Seedance 2.5)** : la voix ElevenLabs de l'extrait est envoyée à Seedance **en vidéo écran noir** (`@Video1`), et le prompt **ne contient pas le texte à dire**. Seedance cale alors les lèvres sur la voix de la vidéo, au même moment. Mesure sur l'accroche du talking head n°2 (`scripts/comparer_synchro.py`) : écart moyen 0,01 s, max 0,02 s, contre 0,40 / 0,84 s avec la voix en référence audio et 0,34 / 0,82 s avec l'écran noir mais le script écrit dans le prompt. C'est le texte dans le prompt qui fait redire la phrase à Seedance à son propre rythme.

Réglages : `reference_image_urls` = [image de départ validée] (`@Image1`), `reference_video_urls` = [vidéo écran noir portant l'extrait de voix] (`@Video1`), `generate_audio: true`, même ratio que l'image, durée = durée de l'extrait arrondie à la seconde supérieure (pas plus : une seconde en trop et Seedance ajoute des mots, ex. un 2e « Pourquoi ? »), caméra verrouillée. Script du studio : `scripts/kie_seedance.py --voix-ecran-noir audio_avatar/A01.wav --generate-audio` (il fabrique `A01_ecran-noir.mp4` et calcule la durée).

Au montage : **son Seedance coupé, voix ElevenLabs d'origine posée telle quelle** (la voix générée par Seedance déforme encore des mots, ses lèvres, elles, suivent la voix d'origine). Le clip est coupé à la durée de l'extrait.

Coût (KIE facture la vidéo de référence en plus du clip, au tarif « avec vidéo ») : (durée de l'extrait + durée du clip) x 17 cr/s en 480p, 38 cr/s en 720p, 95 cr/s en 1080p. Exemple : extrait de 5 s, clip de 5 s en 720p = 380 cr.

Règles d'écriture :
- **Jamais le texte à dire** dans le prompt, ni sa transcription, ni consigne de débit, de pause ou d'articulation : la voix de `@Video1` décide de tout le rythme.
- Balises obligatoires dans l'ordre d'envoi : `@Image1` (image de départ), `@Video1` (écran noir). Pas de `@Audio1`.
- Dire que l'image de `@Video1` est à ignorer (sinon risque d'image assombrie) et que sa bande-son est la voix du personnage.
- Le jeu reste permis : expression du visage accordée au ton de la voix, regard, geste simple (sans le dater sur un mot).
- Quand l'extrait contient des mots d'autour (passage court allongé à 4 s), c'est sans conséquence : Seedance les articule aussi et le montage n'affiche que la partie utile.

```text
Locked [medium shot, seated at the desk, waist up / medium close-up, head and shoulders], [RATIO] photorealistic podcast shot, eye level, framing identical to @Image1. @Image1 is the exact first frame and the only reference for identity (face, eyes, hair, skin details), wardrobe, microphone, desk, background, lighting and framing.

LIP SYNC: @Video1 is a black screen carrying [her/his] recorded voice. Ignore its picture completely. Its soundtrack is [her/his] dialogue, already timed: [she/he] speaks exactly what @Video1 says, exactly when @Video1 says it, with the same pace and the same pauses. [Her/His] lips follow the voice of @Video1 frame by frame, from its first word to its last, and [her/his] mouth stays clearly visible. [Her/His] voice is the voice of @Video1. Before the first word and after the last word of @Video1, [her/his] mouth is closed and still and [she/he] says nothing more.
PERFORMANCE: [Gaze slightly off-camera toward an unseen interviewer / looks straight into the camera]. Facial expression matching the tone of the voice ([calm and caring / intriguing / smiling]). [Optional simple gesture, e.g. "one open-palm gesture"]. Keep the head almost still so the lips stay readable. Natural blinking and breathing. Hands stay below the microphone and never cover the mouth.
AUDIO: Only [her/his] voice from @Video1. No music, no sound effects, no other voice, no added words.
CONTINUITY: Same person, clothes, microphone, desk, background and lighting as @Image1 for the whole shot. Locked camera: never moves, never zooms, never cuts. No text, no subtitles, no captions, no logo.
```

Contrôle de chaque clip reçu : identité, cadre, image non assombrie, puis `scripts/comparer_synchro.py <clip.mp4> <extrait.wav>` (écart lèvres / voix ; au-dessus de 0,1 s, relancer le clip ou le recaler mot par mot, section « Secours » de `montage-controle.md`). La voix Seedance n'est pas contrôlée : elle est remplacée.

Pour le CTA final, regard caméra et léger sourire. Ne jamais écrire de phrase entre guillemets dans le prompt (risque de sous-titres incrustés).

Historique (ne plus utiliser) : voix en référence audio `@Audio1` avec le texte exact dans le prompt (recette du 2026-09-28, puis « lier explicitement l'audio à la parole » du 2026-10-08) : lèvres décalées de 0,3 à 1 s, recalage mot par mot obligatoire au montage.

## 3. Image statique (collage, plan d'illustration, rond d'infographie)

Modèle : GPT Image 2, 1K. Ratio : 9:16 plein écran ; 1:1 rond d'infographie ou carte ; 16:9 case de collage.

```text
[STYLE: photorealistic editorial photo / overhead food photography / macro beauty photo] of [PRECISE SUBJECT, the thing the viewer desires or fears, see grammaire R2], [ACTION OR STATE], [LIGHTING], [BACKGROUND consistent with the charter], subject centered with breathing room for captions. Consistent color grading: [CHARTER MOOD]. No text, no letters, no logo, no watermark.
```

Collage de 3 éléments : 3 images au même style (même lumière, même angle, même fond).

## 4. Objet détouré (surimpression sur l'avatar)

Modèle : GPT Image 2, 1K, fond transparent (option disponible en 1K), ratio 1:1.

```text
A single [OBJECT: blueberry muffin / glazed donut / raw salmon fillet], photorealistic studio product shot, three-quarter view, soft studio light, crisp edges, isolated on a fully transparent background, no ground shadow, no plate, no text, no logo.
```

Vérifie le canal de transparence avant usage. Le texte éventuel (« 10x Oméga 3 ») est posé au montage.

## 5. Animation éducative (image de départ + MiniMax H3)

Même principe que l'avatar : d'abord l'image de départ, puis la vidéo à partir de cette image.

### 5a. Image de départ, GPT Image 2, 9:16, 1K

Choisis UN style dans la charte et garde-le pour toutes les vidéos.

```text
Vertical 9:16 [STYLE: clean 3D medical render / flat vector educational illustration / vintage scientific engraving with deep red accents] of [PRECISE SUBJECT]. [BACKGROUND: solid charter color / pure white paper texture / pure black]. Clear readable shapes, subject centered, generous empty space at the top and bottom for labels. Educational, precise, calm. No text, no labels, no letters, no numbers, no watermark.
```

### 5b. Animation, MiniMax H3 image vers vidéo

Image 5a en première image, durée du plan arrondie à la seconde supérieure (4 à 15 s), 768P suffit (2K pour un plan long plein écran). Le ratio suit l'image de départ.

```text
[DURATION]-second educational animation, vertical. Static camera [or: very slow push-in]. Step by step: [STEP 1 at the start], then [STEP 2], then [STEP 3], timed to the voice-over as follows: [STEP : moment in seconds]. Smooth, scientific, clean motion, no sudden cuts. Keep exactly the same subject, style, colors and background as the first frame. No text, no labels, no letters, no new objects, no people.
```

Son du modèle coupé au montage ; étiquettes synchronisées posées au montage.

## 6. B-roll de secours (plan introuvable sur les réseaux)

Modèle : MiniMax H3 texte vers vidéo, 9:16, 4 à 6 s, 768P. Seulement avec l'accord de l'utilisateur.

```text
Handheld smartphone footage, vertical, realistic and slightly imperfect like a social media video: [PRECISE ACTION]. Natural daylight, real home setting, [PERSON PROFILE matching the target]. No text, no logo, no watermark, no subtitles.
```

## 7. Fiche de recherche b-roll (pour l'utilisateur)

```text
B-roll [N°] | [début]-[fin] ([durée] s, prévoir [durée + 1] s utiles)
À voir : [image concrète, règle appliquée]
Profil : [âge, genre, contexte proches de la cible]
Mots-clés FR : [5 à 8]   |   EN : [5 à 8]   |   Hashtags : [#...]
Format : vertical de préférence (sinon il ira en carte ou en bandeau 16:9)
À éviter : texte incrusté, filigrane, logo de marque
Nom du fichier : broll_[N°].mp4
```
