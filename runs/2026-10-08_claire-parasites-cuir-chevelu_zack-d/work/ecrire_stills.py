#!/usr/bin/env python3
"""Écrit jobs/stills.json (21 stills de chaîne S01..S21) avec les blocs verbatim du skill zack-d-style (references/PROMPTS.md)."""
import json, os
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = (" The environment is exactly the world in the attached background reference image: keep its colours, gradient, grid, horizon height and lighting unchanged. "
       "This world is an infinite canvas: it continues unbroken past every edge of the frame, and the camera is inside it. No ceiling, no roof structure, no walls, "
       "and no platform edge or visible boundary where the ground ends. The grid is an environmental overlay with no thickness, no edges and no physical surface, "
       "not a platform or slab; everything rests naturally with a soft contact shadow. Pixar-style friendly stylized 3D, rounded forms, soft even lighting, one subject, "
       "clean negative space, must read on a phone in one second. Portrait 9:16. No text, no captions, no labels.")
NEG = ("No text, no captions, no labels, no UI, no platform, no stage set, no ceiling, no walls, no dramatic lighting, no photographic noise, "
       "no photorealism on characters, no extra characters, no floating objects.")
OPEN = "Attach references: the first attached image is the background world."
CHAR = (" The woman is exactly the character in the attached character sheet: same face, green-grey eyes, light freckles, shoulder-length wavy brown hair "
        "with caramel strands, pale-blue knit crew-neck sweater, light-wash jeans and white sneakers, same rendering.")
CHAR_REF = " The second attached image is the character sheet."
BLOC = (" The scalp cross-section is the same stylized block as in the attached cross-section reference: a cube of pale-pink scalp skin with glossy brown hair "
        "strands rising from it, soft rounded layers and follicles with round bulbs.")
BLOC_REF = " The second attached image is the scalp cross-section reference."
PARA = (" The parasites are tiny cute stylized bugs, exactly like the ones in the attached parasite reference: small rounded grey-brown bodies, six short legs, "
        "big round eyes, friendly cartoon look, never scary, no gore.")
PARA_DESC = (" The parasites are tiny cute stylized bugs: small rounded grey-brown bodies, six short legs, big round eyes, friendly cartoon look, never scary, no gore.")
PARA_REF = " The second attached image is the parasite reference."
P, C, M, S02 = "jobs/OUT/PLATE-grid.png", "jobs/OUT/CHAR-sheet.png", "jobs/OUT/M-cuir-chevelu.png", "jobs/OUT/S02.png"
S = {}
def add(n, refs, body, neg_extra=""):
    pre = OPEN
    if C in refs: pre += CHAR_REF
    if M in refs: pre += BLOC_REF
    if S02 in refs: pre += PARA_REF
    lock = (CHAR if C in refs else "") + (BLOC if M in refs else "") + (PARA if S02 in refs else "")
    S[n] = {"name": n, "refs": refs, "prompt": pre + " " + body + lock + ENV, "negative": NEG + neg_extra}
add("S01", [P, C], "Low hero angle, camera near the ground looking up. The woman stands full body, centered, scratching her scalp with both hands, eyes squeezed, mildly annoyed and itchy face.")
add("S02", [P], "Extreme macro at the surface of a scalp: glossy brown hair strands rise like a forest of tall trunks from smooth pale-pink skin that fills the ground of the frame. Three tiny parasites hide between the roots, peeking out." + PARA_DESC + " No face, no torso, no person.", " No person, no face.")
add("S03", [P, S02], "Wide prop island seen from slightly above: a giant glass jar of solid snow-white coconut oil, lid closed, no label, a halved coconut lying beside it, towers in the center. At its base, three tiny parasites look up at it, terrified, huddled together.", " No label on the jar, no brand, no person.")
add("S04", [P, C], "Medium shot from the waist up, three-quarter angle. The woman holds a glass jar of solid snow-white coconut oil in both hands at chest height, no label, and is just lifting its lid, curious smile.", " No label on the jar, no brand.")
add("S05", [P, C], "Close shot from slightly above. The woman holds the open coconut oil jar in one hand and in the other a spoon heaped with a big scoop of white coconut oil, raised just above the top of her head, about to spread it.", " No label on the jar, no brand.")
add("S06", [P, C], "Top-down view looking straight down at the top of the woman's head: a generous layer of glossy white coconut oil spread on her brown hair along the parting; her hand holds a small amber glass dropper bottle with no label above her head, one clear drop falling from the dropper. A few green tea-tree leaves are tucked against the bottle.", " No label on the bottle, no brand, no face visible.")
add("S07", [P], "Extreme macro on a single glossy brown hair strand crossing the frame diagonally; several small oval pearly-white eggs are glued along it; a large clear drop of oil with a faint green tint hangs just above the eggs, about to land. No face, no torso, no person.", " No person, no face.")
add("S08", [P, C], "Medium shot from the waist up, camera at eye level, slightly in front of her: the woman stands upright in a natural relaxed pose, shoulders square to the camera, head straight, body not twisted, both hands on the top of her head, fingertips massaging glossy oil into her hair at the roots, the oil shining on the strands from root to tip, calm content face.", " No twisted body, no looking back over the shoulder, no contorted arms.")
add("S09", [P, S02], "Extreme macro on a glossy brown hair strand: one tiny parasite clings to it with its six legs, looking sideways; a thick slow wave of white coconut oil flows along the strand toward it from the top of the frame. No face, no torso, no person.", " No person, no face.")
add("S10", [P, S02], "Extreme macro, three-quarter angle: the same tiny parasite is now fully enclosed inside a round translucent bubble of white oil stuck on the hair strand, waving its little legs, puzzled. No face, no torso, no person.", " No person, no face, no blood.")
add("S11", [P, C], "Wide shot from above: the woman sleeps peacefully lying on a big soft white pillow placed on the ground, a light blanket over her, her oiled hair wrapped in a white towel turban; the whole world is tinted a calm deep night blue.", " No bed frame, no furniture other than the pillow.")
add("S12", [P, C], "Medium shot from the waist up: the woman, eyes closed and relaxed, tilts her head forward under a clear stream of water falling from above out of frame, rinsing her hair, water splashing softly; bright morning light.", " No shower head, no bathroom, no tiles, no soap bottle.")
add("S13", [P, S02], "Extreme macro at the scalp surface between glossy hair roots: a clear stream of water flows across the pink skin, carrying away tiny grey motionless parasites lying on their backs and empty broken eggshells toward the bottom of the frame. No face, no torso, no person.", " No person, no face, no blood.")
add("S14", [P, C], "Three-quarter view, full body: the woman with dry clean wavy hair scratches the top of her head with one hand, puzzled frown; a faint soft red glow shows on her scalp.")
add("S15", [P, M], "Macro cutaway: the scalp cross-section cube fills the frame in three-quarter view; its top skin surface is red, dry and slightly cracked with a few pale flakes lifting off; no parasites anywhere. No face, no torso, no person.", " No person, no face, no insects, no blood.")
add("S16", [P, M], "Macro cutaway: the same scalp cross-section cube seen from the opposite three-quarter angle; a soft sage-green soothing liquid wave flows over the red top surface, the skin under the wave already turning calm healthy pink. No face, no torso, no person.", " No person, no face, no insects.")
add("S17", [P, C], "Wide prop island: the woman, tiny, full body, stands smiling among giant natural ingredients many times her size: a huge fresh aloe vera leaf, a cluster of giant white chamomile flowers and a big wooden bowl of rolled oats.", " No jars with labels, no brand.")
add("S18", [P, C], "Full body shot, the woman seen entirely from head to feet, standing upright, centered: she holds a wooden bowl at waist height in one hand and stirs a smooth creamy pale-green paste with a wooden spoon in the other; a small aloe leaf and a few chamomile flowers lie on the ground at her feet; gentle smile.", " No label, no brand, no cropped legs, no cropped feet.")
add("S19", [P, C], "Full body shot, the woman seen entirely from head to feet, standing upright, centered, facing the camera: she holds up in both hands at chest height a small closed booklet with a plain terracotta-coloured cover (#A8553A), completely blank, warm proud smile.", " No text on the booklet, no title, no letters, no logo, no cropped legs, no cropped feet.")
add("S20", [P, C], "Low angle: a large closed booklet with a plain blank terracotta cover (#A8553A) stands upright inside a softly glowing cyan ring on the ground; the woman, tiny next to it, full body, points at it with a big smile.", " No text on the booklet, no title, no letters, no logo.")
add("S21", [P], "Frontal view: a large closed booklet with a plain blank terracotta cover (#A8553A) stands upright alone inside a softly glowing cyan ring on the ground, centered in the lower half, lots of clean empty space above.", " No text on the booklet, no title, no letters, no logo, no person.")
json.dump(list(S.values()), open(os.path.join(RUN, "jobs/stills.json"), "w"), indent=1, ensure_ascii=False)
print(len(S), "stills")
