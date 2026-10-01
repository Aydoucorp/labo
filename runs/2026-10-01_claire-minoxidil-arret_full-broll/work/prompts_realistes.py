# Prompts IA « rendu humain » des plans réels (UGC, STOCK) : photo puis vidéo de smartphone, imparfaites et vécues.
# Importé par work/ecrire_brief.py, qui remplace ai_prompt de ces plans. En anglais : les modèles d'image et de vidéo
# rendent mieux le réalisme photo en anglais. Même femme et même salle de bain partout pour la continuité.

FEMME = ("a 46-year-old French woman with shoulder-length wavy chestnut-brown hair and a few scattered grey strands at "
         "the roots, natural unretouched skin with visible pores, fine lines and a few freckles, short unpainted nails")
SDB = ("a small lived-in French apartment bathroom: white ceramic sink with faint water spots, beige wall tiles with grey "
       "grout, a frosted window on the left, a folded cream cotton towel, a glass with a toothbrush")
PHOTO = ("Candid vertical smartphone photo (9:16), taken handheld on an iPhone main camera by a real person at home, "
         "natural available light only, slightly imperfect framing, mild sensor noise, true-to-life muted colors, "
         "phone-like depth of field (background only slightly soft).")
PHOTO_NON = ("It must look like an ordinary unedited phone photo, not an advertisement, not a stock photo, not CGI. "
             "No studio lighting, no glossy or waxy skin, no airbrushing, no perfect symmetry, no cinematic color grading, "
             "no heavy bokeh, no extra or merged fingers, no readable text, no logo, no watermark.")
VIDEO = ("Handheld smartphone video, vertical 9:16, real-time speed, slight natural hand shake and tiny focus "
         "adjustments, natural motion blur on quick movements, constant ambient daylight.")
VIDEO_NON = ("Keep exactly the same person, hands, objects and setting as the start image. No slow motion, no smooth "
             "gimbal or drone move, no morphing, no extra fingers, no text, no lighting change.")

# plan : (scène de la photo, action de la vidéo)
SCENES = {
    "01a": (f"Close-up over the shoulder of {FEMME}: her right hand holds a small glass dropper filled with clear liquid "
            "just above the parting of her hair, a drop forming at the tip. Real roots with a few grey strands, a couple of "
            f"flyaway hairs. Daylight from a frosted window on the left, in {SDB}.",
            "The drop slowly forms and falls onto the parting; her hand trembles very slightly. 3 seconds."),
    "01b": ("Close-up of a used wooden paddle hairbrush lying on the edge of a white bathroom sink with faint water spots, "
            "its bristles tangled with a clump of shed chestnut hairs with a few grey ones, two loose hairs on the ceramic.",
            "The phone moves slowly closer to the clump of hair, slight hand shake. 2 seconds."),
    "01d": ("Top-down shot of a cheap printed yearly paper calendar lying flat on a light oak kitchen table, slightly curled "
            "corners, a pen and the edge of a coffee mug in frame, a woman's index finger resting on the first month. The "
            "printed grid is small and slightly out of focus, no readable words.",
            "Her finger slides slowly across the months from left to right. 2 seconds."),
    "02": (f"Shot from behind at shoulder height: {FEMME}, wearing a loose grey t-shirt, stands at the bathroom mirror, "
           "parting her hair with her left hand and applying drops from a small plain white dropper bottle to the parting "
           f"with her right hand. Her face is not visible, only a blurred partial reflection. Morning light, {SDB}.",
           "She dabs two or three drops along the parting and spreads them with a fingertip. 3 seconds."),
    "03": ("Extreme close-up of the scalp along a hair parting: a single clear drop of liquid sitting on the skin between "
           "chestnut and grey roots, natural skin texture, a few tiny flakes, soft daylight.",
           "The drop slowly spreads between the roots; very subtle handheld movement. 2 seconds."),
    "04a": ("Medium close-up inside a mirrored bathroom cabinet with everyday products out of focus and no readable labels: "
            "a woman's hand places a small plain white dropper bottle back on the shelf, fingers still touching it.",
            "She sets the bottle down, pauses a second with her fingers on it, then slowly withdraws her hand. 2 seconds."),
    "04b": ("Top-down shot of a white shower tray around the metal drain: several long wet shed chestnut hairs clumped near "
            "the drain, water droplets and a little soap residue on the surface.",
            "Slow handheld pan along the hairs toward the drain while a thin trickle of water flows. 2 seconds."),
    "05a": ("The same mirrored bathroom cabinet in warm evening lamp light: a woman's hand reaches in to take a small plain "
            "white dropper bottle off the shelf, products out of focus, no readable labels.",
            "Quick routine gesture: the hand grabs the bottle and leaves the frame. 2 seconds."),
    "05b": (f"Wide shot: {FEMME}, in a grey t-shirt and leggings, sits on the edge of the bathtub, head lowered, holding a "
            "small white dropper bottle with both hands on her knees; her face is turned away and partly hidden by her hair. "
            f"Overcast daylight, {SDB}.",
            "She slowly turns the bottle between her fingers and lets out a sigh; the phone rests on a shelf, almost static. 2 seconds."),
    "06b": (f"Close-up from the side of {FEMME}: her hand runs through her wavy hair near the temple, grey strands visible, "
            "a few flyaways catching window light; only her cheek is visible, not her eyes.",
            "Her fingers comb slowly through the hair from root to tip and the hair falls back naturally. 2 seconds."),
    "09": ("Top-down close-up of the crown of the head of a woman around 50 with fine chestnut hair: a widened centre parting "
           "where the scalp is clearly visible, real thin hair density, soft overhead daylight, slight phone-camera noise.",
           "Almost static; she breathes so the head moves a few millimetres. 3 seconds."),
    "11": ("Close-up of a white bathroom sink with a few water drops: several long fine chestnut hairs falling from above "
           "into the basin, some already lying on the wet ceramic near the drain.",
           "A few hairs drift down into the sink at real speed; the phone tilts down slightly to follow them. 3 seconds."),
    "13": (f"Medium shot at a kitchen table in late afternoon light: {FEMME}, side profile, rubs her temples with both "
           "hands in front of an open laptop, a plate with a few crackers and a half-finished glass of water next to it, "
           "papers and a phone on the table.",
           "She closes her eyes and slowly massages her temples; handheld. 3 seconds."),
    "15a": ("Close-up in the shower: a woman's wet open palm with several shed chestnut hairs stuck to it, water drops on the "
            "skin, blurred white tiles behind.",
            "Water runs over her palm and she tilts it slightly toward the phone. 2 seconds."),
    "16": (f"Extreme close-up of the front hairline of {FEMME}, against the window: short new baby hairs standing up along "
           "the hairline, backlit by daylight so they glow, real skin texture on the forehead.",
           "Very slow handheld push toward the baby hairs; a light breeze moves them slightly. 3 seconds."),
    "18": (f"Medium shot: {FEMME}, seen from the side with her face turned away, closes a bathroom vanity drawer with a "
           f"small white dropper bottle inside, {SDB}.",
           "She pushes the drawer shut, then runs a relaxed hand through her hair; handheld. 3 seconds."),
    "19": ("Top-down shot on a light oak table: two small amber glass dropper bottles without labels, one with a sprig of "
           "fresh rosemary beside it, one with a small ceramic bowl of green pumpkin seeds, both facing a small plain white "
           "dropper bottle. Morning window light with soft shadows, a crumpled linen napkin at the edge of the frame.",
           "Slow handheld push toward the two amber bottles. 4 seconds."),
    "20a": ("Close-up on a light oak table: a sprig of fresh rosemary next to an amber dropper bottle without label, and a "
            "small ceramic bowl of green pumpkin seeds beside a second amber bottle. Window light, a few seeds spilled.",
            "Slow handheld pan from the rosemary to the pumpkin seeds. 3 seconds."),
    "20b": (f"Medium close-up from behind and slightly above: {FEMME} massages her scalp with the fingertips of both hands, "
            "fingers pressing in small circles through her wavy hair, face not visible, bathroom daylight.",
            "Small circular fingertip movements at real speed; handheld. 2 seconds."),
    "21a": ("First-person view: a woman's hand holds a smartphone at chest height above a beige sofa, thumb over the "
            "keyboard, the screen shows a blurred generic comment section with nothing readable.",
            "The thumb types a short word; the screen lights the thumb; handheld. 2 seconds."),
}


def prompt(sid):
    scene, action = SCENES[sid]
    return {"image": f"{PHOTO} {scene} {PHOTO_NON}", "motion": f"{VIDEO} {action} {VIDEO_NON}"}
