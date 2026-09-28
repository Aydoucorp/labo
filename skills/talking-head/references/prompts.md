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

Principe Hotline : la scène est générée à partir de l'image de départ, avec un modèle vidéo dialogué. **Recette validée (2026-09-28)** : Seedance génère lui-même la voix et les lèvres (`generate_audio: true`), en imitant la voix de l'extrait ElevenLabs fourni comme référence audio. Les lèvres sont alors naturellement synchrones ; aucun synchroniseur labial après coup (rendu jugé peu naturel).

Réglages : mode « référence multimodale » (Seedance 2.5 sur KIE n'accepte pas première image + audio ensemble) : `reference_image_urls` = [image de départ validée], `reference_audio_urls` = [extrait audio du clip, 2 à 30 s], `generate_audio: true`, même ratio que l'image, durée = durée de l'extrait arrondie à la seconde supérieure (4 à 30 s), caméra verrouillée. Script : `scripts/kie_seedance.py --generate-audio` (dossier `scripts/` du studio).

**Balises de référence obligatoires** : dans le prompt, chaque fichier joint est désigné par sa balise, dans l'ordre d'envoi : `@Image1` (première image de `reference_image_urls`), `@Audio1` (premier audio de `reference_audio_urls`), puis `@Image2`, `@Audio2`… Jamais « Image 1 » ou « Audio 1 » en texte libre : sans la balise, le modèle ne relie pas la consigne au fichier (cause du décalage lèvres / voix sur les premiers clips).

Règles d'écriture de la parole :
- Texte exact entre guillemets, **chiffres et symboles écrits en toutes lettres** (« trente pour cent », « B douze »).
- **Prononciation** : pour chaque mot difficile ou mal prononcé au clip test, une ligne `Pronunciation:` (ex. « carences » = ka-RANSS, deux syllabes). Relancer uniquement le clip concerné.
- **Émotion phrase par phrase** : ton, débit, mot sur lequel insister, pause, geste daté.
- Quand l'extrait audio contient d'autres mots que ceux à dire (passage très court élargi à 4 s), ajouter « Only borrow the voice from @Audio1, not its words » ou fournir comme voix un autre extrait propre (ex. celui du clip A01).

```text
Create a [DURATION]-second [RATIO] photorealistic podcast talking-head shot. One continuous locked-off shot, natural real-time speed, framing identical to @Image1 ([seated at the desk, waist up] / [square framing, head and shoulders]).

REFERENCES: @Image1 is the exact first frame and the only reference for identity (face, eyes, hair, skin details), wardrobe, microphone, desk, background, lighting and framing. @Audio1 is the reference of HER/HIS voice: reproduce exactly this voice (same timbre, pitch, accent, pace, intonation and pauses). [Only borrow the voice from @Audio1, not its words.] Do not use any other voice.

SPEECH: [She/He] speaks [LANGUAGE], in [her/his] own voice from @Audio1, saying exactly these words and nothing else:
"[EXACT WORDS, numbers written in full]"
[Pronunciation: "word" is pronounced ...]

EMOTION AND DELIVERY: [tone of the whole clip]. "[phrase 1]" [how: calm / intriguing / slower / lower]; [short pause]; "[phrase 2]" with emphasis on "[key word]" [...].

PERFORMANCE: [Gaze slightly off-camera toward an unseen interviewer / looks straight into the camera for the call to action]. [GESTURE with its moment, e.g. "raises three fingers on 'trois'", "open palm on 'signal'"]. Natural blinking and breathing, subtle head movements, lips perfectly synchronized with every syllable, mouth closed and still before the first word and after the last word. Hands stay below the microphone and never cover the mouth. No repetitive gesture loop.

AUDIO: Only [her/his] voice, close podcast microphone sound, quiet room tone. No music, no sound effects, no other voice.
CONTINUITY: Same person, clothes, microphone, desk, background and lighting as @Image1 for the whole shot. Camera never moves, never zooms, never cuts. No text, no subtitles, no captions, no logo.
```

Contrôle de chaque clip reçu : transcription Whisper (mots exacts, prononciation), identité, cadre, lèvres. Les mots mal prononcés se corrigent par la ligne `Pronunciation:` et une relance du seul clip.

Pour le CTA final, regard caméra et léger sourire à la dernière phrase. Ne jamais citer une phrase entre guillemets hors de la section SPEECH (risque de sous-titres incrustés).

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
