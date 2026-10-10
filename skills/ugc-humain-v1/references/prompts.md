# Gabarits UGC V1

Remplis tous les champs et retire les blocs inapplicables. Les recettes servent une nouvelle marque, un produit ou un service selon le brief.

## Portrait

```text
Photorealistic [RATIO] smartphone still of a fictional adult [IDENTITY], wearing [WARDROBE], in [APPROVED EVERYDAY ENVIRONMENT]. [FRAMING AND CAMERA HEIGHT]. They look into the recording lens as if mid-conversation. [STARTING HANDS AND PRODUCT STATE]. Leave room for [PLANNED ACTION]. [WINDOW LIGHT AND DIRECTION]. Visible natural pores, believable fine lines, subtle asymmetry and ordinary fabric texture. The recording phone is behind its own lens and never visible. No beauty filter, extra objects or added text.
```

## Vidéo (paroles natives, hors méthode du studio)

```text
Create a [DURATION]-second [RATIO] photorealistic smartphone UGC video in [LANGUAGE]. Natural real-time speed. [PLANNED SHOTS AND CUTS].
REFERENCES: [ACTUAL CASTING IMAGE: IDENTITY, CLOTHES, APPROVED ROOM], [PRODUCT IMAGE IF NEEDED: EXACT GEOMETRY AND PRINT], [ACTUAL CONTENT IMAGE IF NEEDED: SHAPE, SCALE, COLOUR], [OPTIONAL PERFORMANCE VIDEO: RHYTHM AND TEXTURE ONLY].
CAMERA: [FIXED CAMERA OR BRIEF OPENING PLACEMENT FROM ITS OWN POINT OF VIEW]. No visible recording phone. [FRAMING AND HAND SPACE].
PERFORMANCE: Engaged conversational delivery, varied small gestures, natural breaths and blinks. No constant grin, repetitive gestures or frozen expression.
TIMELINE: [EACH LOCAL START–END, SHOT, EXACT SPOKEN LINE, ACTION, HAND AND OBJECT STATE].
PRODUCT CONTINUITY: [INITIAL LOCATION, GRIP, ACTION, INSERT STATE, RETURN STATE, FINAL LOCATION]. Preserve actual proportions, unmirrored print, finger contact and light. [RULES SPECIFIC TO CONTENT OR SERVICE].
AUDIO: One consistent original voice [DESCRIPTION], including speech over inserts. Exact lines, clear speech, natural pauses, accurate visible lip sync and quiet room tone.
CONSTRAINTS: [ONLY THE CONSTRAINTS THAT SERVE THIS BRIEF]. Preserve approved identity, clothes, room and light; no added dialogue or invented graphics.
```

## Vidéo dialoguée, méthode écran noir (méthode du studio, Seedance 2.5)

Références envoyées dans l'ordre : `@Image1` casting validé, `@Image2` produit si besoin, `@Video1` écran noir portant la voix ElevenLabs. Jamais le texte à dire dans le prompt. Les intervalles de la timeline viennent de la voix mesurée (Whisper ou MMS), sans citer les phrases.

```text
Create a [DURATION]-second [RATIO] photorealistic smartphone UGC video. Natural real-time speed. [PLANNED SHOTS AND CUTS].
REFERENCES: @Image1 is the approved casting: identity, clothes and room. [@Image2 is the product: exact geometry and print.] @Video1 is a black screen carrying [her/his] recorded voice: ignore its picture completely.
LIP SYNC: The soundtrack of @Video1 is [her/his] dialogue, already timed: [she/he] speaks exactly what @Video1 says, exactly when @Video1 says it, with the same pace and the same pauses. [Her/His] lips follow the voice of @Video1 frame by frame whenever the mouth is visible. [Her/His] voice is the voice of @Video1. After the last word of @Video1, [she/he] says nothing more.
CAMERA: [FIXED CAMERA OR BRIEF OPENING PLACEMENT FROM ITS OWN POINT OF VIEW]. No visible recording phone. [FRAMING AND HAND SPACE].
PERFORMANCE: Engaged conversational expression matching the tone of the voice, varied small gestures, natural breaths and blinks. No constant grin, repetitive gestures or frozen expression.
TIMELINE: [EACH LOCAL START–END TAKEN FROM THE VOICE, SHOT, ACTION, HAND AND OBJECT STATE, NO QUOTED WORDS].
PRODUCT CONTINUITY: [INITIAL LOCATION, GRIP, ACTION, INSERT STATE, RETURN STATE, FINAL LOCATION]. Preserve actual proportions, unmirrored print, finger contact and light.
AUDIO: Only [her/his] voice from @Video1, quiet room tone. No music, no other voice, no added words.
CONSTRAINTS: [ONLY THE CONSTRAINTS THAT SERVE THIS BRIEF]. Preserve approved identity, clothes, room and light; no invented graphics, no text, no subtitles.
```

Au montage : son Seedance coupé, voix ElevenLabs d'origine, clip coupé à la durée de la voix.

## Blocs de recette à adapter

**Emballage ou flacon fermé.** Décris un début mains vides si prévu ; à l'insert la main montre l'objet ; au retour, cette même main le tient encore. L'état du bouchon ou de la fermeture reste constant. Pour une entrée dans un plan sans coupe, décris aussi la saisie physique.

**Contenu séparé.** Identifie séparément la photo de l'emballage et celle du contenu. À l'insert : un seul élément, dans la main choisie, taille réelle ; emballage sur une surface. Au retour : même élément, même main, même emballage et état d'ouverture. Ne laisse pas croire que le modèle connaît un contenu non montré.

**Installation du téléphone.** Le cadre se déplace légèrement comme porté par la main, descend sur un support hors champ, se stabilise ; quelques doigts quittent le bord de l'objectif. Tout est vu par l'unique appareil qui enregistre. La surface visible ne reçoit pas ce téléphone.

## Continuation

```text
Continue the attached approved clip for [DURATION] more seconds, same [RATIO], starting from its actual last frame and audio state.
CONTINUITY: [PERSON, CLOTHES, ROOM, CAMERA, LIGHT, ORIGINAL VOICE, HANDS, PRODUCT LOCATION AND PRECISE STATE].
Do not repeat “[LAST LINE]” or restart the hook.
NEW TIMELINE: [EXACT NEW WORDS, ACTIONS AND LOCAL TIMES].
[FINAL STATE]. No object reset, duplicated product or unexplained change in the demonstration.
```
