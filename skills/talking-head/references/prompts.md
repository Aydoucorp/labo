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

Principe Hotline : la scène est générée à partir de l'image de départ, avec un modèle vidéo dialogué. Ici la voix n'est pas inventée par le modèle : c'est l'extrait de la voix off ElevenLabs qui pilote les lèvres.

Réglages : image de départ validée (9:16 pour le plein écran, 1:1 pour l'écran partagé) + extrait audio du clip (`audio_avatar/<ID>.wav`), même ratio que l'image, résolution 1080p, durée = durée de l'extrait arrondie à la seconde supérieure (4 à 30 s), caméra verrouillée.

Si l'interface ne permet pas de combiner « image de départ imposée » et « audio de référence » (cas fréquent : les deux modes s'excluent), passe l'image de départ comme image de référence et écris dans le prompt qu'elle est la première image exacte. Vérifie sur le clip test que le cadre et l'identité sont conservés.

```text
Create a [DURATION]-second [RATIO] photorealistic podcast talking-head shot, [LANGUAGE] speech. One continuous locked-off shot, natural real-time speed.
REFERENCES: Image 1 = the exact first frame and the only identity, wardrobe, microphone, desk, background, lighting and framing reference. Audio 1 = the exact voice to lip-sync, from its first to its last syllable; do not change, speed up or replace it.
STARTING STATE: The person from Image 1, seated in the same pose, same framing, mouth closed, [HANDS POSITION]. Only this person is visible.
PERFORMANCE: Natural podcast delivery, gaze slightly off-camera toward an unseen interviewer [or: toward the camera for the call to action], subtle head movements, blinking, natural breathing, small nods on key words. [GESTURE INTENTION with its moment, e.g. "raises two fingers on 'number two' around 1.2 s" / "counts on fingers during the list" / "open palm while explaining" / "leans in slightly on the key figure"]. Hands stay below the microphone and never cover the mouth. No repetitive gesture loop.
TIMELINE AND EXACT WORDS: [START-END s: "exact words from the transcript" ; reaction or gesture] [one line per phrase of the audio excerpt].
AUDIO: Lip sync only to Audio 1, precise on every syllable. Mouth closed and still during silences. No music, no added sound effects, no other voice.
CONTINUITY: Same person, clothes, microphone, desk, background and lighting as Image 1 for the whole shot. Camera never moves, never zooms, never cuts. No text, no subtitles, no logo.
```

Pour un clip d'écran partagé, précise « square framing identical to Image 1, head and shoulders ». Pour le CTA final, regard caméra et léger sourire à la dernière phrase.

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
