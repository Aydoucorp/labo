#!/usr/bin/env python3
"""Écrit jobs/legs.json (21 clips Kling 3.0) à partir de storyboard.json : prompt = Camera motion + Subject motion + queue verbatim du skill."""
import json, os
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = " One continuous camera move, smooth and physical, no cuts. Pixar-style stylized 3D in a bright cyan-blue grid world. No captions. No text."
NB = " The booklet cover stays completely blank."
P = {
"B01": ("Camera starts low looking up at the woman, then pushes forward fast into her hair and dives down between the strands to the scalp surface, ending on the macro forest of hair of the end frame.", "The woman scratches her scalp with both hands, annoyed and itchy."),
"B02": ("Camera glides low between the giant hair trunks past the tiny bugs, then pulls back fast and rises, ending on the wide prop island of the end frame.", "The tiny cute bugs peek out and scurry between the roots."),
"B03": ("Camera pulls back and rises while the giant jar shrinks into the woman's hands, ending on the medium shot of the end frame.", "The tiny bugs look up at the giant coconut oil jar, tremble and run away out of frame."),
"B04": ("Camera rises slightly to a higher angle and pulls back to show her full body, ending on the framing of the end frame.", "She opens the lid, dips a spoon into the white coconut oil and lifts a big scoop above her head."),
"B05": ("Camera cranes up to a high top-down angle above her head, ending on the framing of the end frame.", "She spreads the scoop of white oil on the top of her head along her parting, then raises a small amber dropper bottle above her head."),
"B06": ("Camera pushes forward fast down into her hair along the parting and dives onto a single hair strand, ending on the extreme macro of the end frame.", "One clear drop falls from the dropper into the oil on her hair."),
"B07": ("Camera holds on the hair strand, then pulls back fast out of the hair, ending on the medium shot of the woman of the end frame.", "The green-tinted drop lands on the white eggs; the eggs turn grey, crack open and stay empty."),
"B08": ("Camera pushes forward fast into her hair at the roots and dives along one glossy strand, ending on the macro of the end frame.", "Her fingertips massage the oil from the roots to the tips, the hair turns glossy."),
"B09": ("Camera orbits a quarter turn around the hair strand with a slow push-in, ending on the framing of the end frame.", "The thick wave of white oil flows down the strand and wraps the tiny bug completely inside a round translucent bubble."),
"B10": ("Camera pulls back fast out of the hair and rises to a high wide view while the world darkens to a calm night blue, ending on the wide shot of the end frame.", "Inside the oil bubble the tiny bug waves its legs, slows down, stops and turns grey, cartoon style, no gore."),
"B11": ("Camera slowly pushes in, then rises to eye level, ending on the medium shot of the end frame.", "She sleeps peacefully; the night blue brightens into morning light; she is now standing, rinsing her hair under a clear stream of water."),
"B12a": ("Camera pushes forward fast into her wet hair and dives down to the scalp surface, ending on the macro of the end frame.", "Clear water runs through her hair, rinsing it."),
"B12b": ("Camera pulls back fast out of the hair and drops to ground level, ending on the full body shot of the end frame.", "The water stream carries the grey motionless bugs and empty eggshells away out of the bottom of the frame, the scalp left clean."),
"B13": ("Camera pushes forward fast into the red glow on her scalp and dives through the skin, ending on the cross-section cube of the end frame.", "She scratches the top of her head, puzzled; a faint red glow pulses on her scalp."),
"B14": ("Camera orbits half a turn around the cross-section cube to the opposite three-quarter angle, ending on the framing of the end frame.", "The red dry cracked skin surface sheds a few pale flakes, then a soft sage-green soothing liquid starts to flow over it."),
"B15": ("Camera pulls back fast and rises, ending on the wide prop island of the end frame.", "The sage-green wave covers the whole surface and the red fades into calm healthy pink."),
"B16a": ("Camera pushes in toward the woman while the giant ingredients shrink, ending on the full body shot of the end frame.", "She gathers a little aloe, chamomile and oats into a wooden bowl and starts stirring a pale-green paste."),
"B16b": ("Camera slowly pushes in, keeping her full body in frame, ending on the framing of the end frame.", "She stirs the green paste, then the bowl softly turns into a small closed terracotta booklet in her hands." + NB),
"B17": ("Camera pulls back and drops to a low angle, ending on the framing of the end frame.", "The terracotta booklet grows large and stands upright inside a softly glowing cyan ring on the ground beside her; she points at it with a big smile." + NB),
"B18": ("Camera slowly pushes in to a frontal centered view, ending on the framing of the end frame.", "The woman waves and walks out of frame, leaving the booklet alone in the glowing cyan ring." + NB),
"B19": ("Camera very slowly pushes in.", "The cyan ring glows softly, the booklet stays still." + NB),
}
sb = json.load(open(os.path.join(RUN, "storyboard.json")))
legs = []
for l in sb:
    cam, sub = P[l["name"]]
    legs.append({"name": l["name"], "start": l["start"], "end": l["end"], "vo_start": l["vo_start"], "vo_end": l["vo_end"], "target_s": l["target_s"],
                 "duration": l["duration"], "lines": l["lines"], "prompt": f"Camera motion: {cam} Subject motion: {sub}" + Q})
json.dump(legs, open(os.path.join(RUN, "jobs/legs.json"), "w"), indent=1, ensure_ascii=False)
print(len(legs), "legs,", sum(int(x["duration"]) for x in legs), "s")
