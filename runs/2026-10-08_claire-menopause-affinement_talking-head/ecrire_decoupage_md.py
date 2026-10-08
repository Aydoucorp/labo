# Génère decoupage.md (livrable du mode A) et prompts/*.txt à partir de decoupage.json et audio_avatar/clips_avatar.json.
import json
d = json.load(open("decoupage.json")); P = d["plans"]; DUR = d["duree"]
clips = {c["id"]: c for c in json.load(open("audio_avatar/clips_avatar.json"))}
W = json.load(open("mots_mms.json"))["words"]

def fr(x): return f"{x:.1f}".replace(".", ",")

SPEECH = {
 "S01": "Deux femmes sur trois constatent un affinement de leurs cheveux à la ménopause. Pourquoi ?",
 "A01": "Et la baisse du taux de collagène peut amincir le cuir chevelu, ce qui offre moins de soutien à ces follicules pileux. Mais voici des solutions qui fonctionnent !",
 "A02": "Un manque de fer ou un problème de thyroïde peut aggraver la chute, et cela se corrige. Pensez aussi à prendre un complément de collagène, pour soutenir votre cuir chevelu",
 "A03": "C'est un geste doux et simple, à faire avec régularité pendant plusieurs mois. Si vous voulez plus de détails, j'ai créé un guide, Comment traiter l'affinement des cheveux à la ménopause, rien que pour vous. Commentez GUIDE et je vous enverrai gratuitement mon guide en message privé.",
}
PRON = {
 "S01": 'Pronunciation: "ménopause" is pronounced may-no-POZE.',
 "A01": 'Pronunciation: "collagène" is pronounced ko-la-JEN; "pileux" is pronounced pee-LEU.',
 "A02": 'Pronunciation: "thyroïde" is pronounced tee-ro-EED (three syllables); "collagène" is pronounced ko-la-JEN.',
 "A03": 'Pronunciation: "GUIDE" is the French word guide, pronounced GHEED.',
}
EMO = {
 "S01": 'Upbeat, alert and energetic. "Deux femmes sur trois constatent un affinement de leurs cheveux à la ménopause" lively, with emphasis on "deux femmes sur trois"; short pause; "Pourquoi ?" curious and punchy, eyebrows raised, slight head tilt.',
 "A01": 'Confident, animated and clear. "Et la baisse du taux de collagène peut amincir le cuir chevelu" explanatory, emphasis on "collagène"; "ce qui offre moins de soutien à ces follicules pileux" a little lower; short pause; "Mais voici des solutions qui fonctionnent !" enthusiastic, big warm smile.',
 "A02": 'Direct and informative, then reassuring. "Un manque de fer ou un problème de thyroïde" counting, emphasis on "fer" and "thyroïde"; "peut aggraver la chute" serious; "et cela se corrige" reassuring with a light smile; short pause; "Pensez aussi à prendre un complément de collagène, pour soutenir votre cuir chevelu" practical and friendly.',
 "A03": 'Encouraging, warm and practical, then cheerful and bright. "C\'est un geste doux et simple, à faire avec régularité pendant plusieurs mois" gentle; short pause; "Si vous voulez plus de détails, j\'ai créé un guide" friendly; the guide title said clearly; "rien que pour vous" warm; short pause; "Commentez GUIDE et je vous enverrai gratuitement mon guide en message privé" bright and engaging, emphasis on "GUIDE".',
}
GESTE = {
 "S01": "Gaze slightly off-camera toward an unseen interviewer, then a quick look into the camera on 'Pourquoi'. Small concerned frown on 'affinement'.",
 "A01": "Gaze slightly off-camera toward an unseen interviewer. One open hand slowly lowers on 'amincir'; small nod on 'follicules pileux'; big smile and a small nod on 'Mais voici des solutions qui fonctionnent'.",
 "A02": "Gaze slightly off-camera toward an unseen interviewer. Raises one finger on 'fer', a second finger on 'thyroïde'; reassuring nod on 'et cela se corrige'; open palm turned to the side on 'complément de collagène'.",
 "A03": "Gaze slightly off-camera with soft gentle hand movements on 'doux et simple'; from 'Si vous voulez plus de détails' looks straight into the camera; warm smile on 'rien que pour vous'; light smile and small nod on the last phrase.",
}

def seedance(cid):
    c = clips[cid]; sq = c["format"] == "1:1"
    framing = "square framing, head and shoulders" if sq else "seated at the desk, waist up"
    return f"""Create a {c['duree_a_demander']}-second {c['format']} photorealistic podcast talking-head shot. One continuous locked-off shot, natural real-time speed, framing identical to @Image1 ({framing}).

REFERENCES: @Image1 is the exact first frame and the only reference for identity (face, eyes, hair, skin details), wardrobe, microphone, desk, background, lighting and framing. @Audio1 is the reference of HER voice: reproduce exactly this voice (same timbre, pitch, accent, pace, intonation and pauses). Do not use any other voice.

SPEECH: She speaks French, in her own voice from @Audio1, saying exactly these words and nothing else:
"{SPEECH[cid]}"
{PRON[cid]}

EMOTION AND DELIVERY: {EMO[cid]}

PERFORMANCE: {GESTE[cid]} Natural blinking and breathing, subtle head movements, lips perfectly synchronized with every syllable, mouth closed and still before the first word and after the last word. Hands stay below the microphone and never cover the mouth. No repetitive gesture loop.

AUDIO: Only her voice, close podcast microphone sound, quiet room tone. No music, no sound effects, no other voice.
CONTINUITY: Same person, clothes, microphone, desk, background and lighting as @Image1 for the whole shot. Camera never moves, never zooms, never cuts. No text, no subtitles, no captions, no logo."""

STYLE = "flat vector educational illustration, clean dark outlines, solid warm cream background (#FAF6F3), palette terracotta (#A8553A), light terracotta (#C9805F), plum (#7A4351), dark brown, soft sage green (#8C9B86), silver grey (#B4ADA4)"
IMG = {
 "image-E1": f"Vertical 9:16 {STYLE}, of a single hair follicle in cross-section under the scalp, a long healthy hair strand growing upward from a round bulb, a few small round light-terracotta spheres (hormones) floating around the bulb, a thin skin layer at the top. Clear readable shapes, subject centered, generous empty space at the top and bottom for labels. Educational, precise, calm. No text, no labels, no letters, no numbers, no watermark.",
 "animation-E1": "10-second educational animation, vertical. Static camera with a very slow push-in. Step by step: the small light-terracotta spheres around the bulb fade and disappear one by one, then the hair strand loosens and slowly slides up out of the follicle, then small plum hexagonal molecules drift in toward the bulb, then the follicle slowly shrinks and a new, much thinner hair strand grows from it. Timed to the voice-over as follows: spheres fade 0.3 to 1.5 s ; strand loosens and slides out 1.7 to 3.6 s ; plum molecules drift in 5.0 to 6.5 s ; follicle shrinks and thinner strand grows 7.5 to 9.2 s. Smooth, scientific, clean motion, no sudden cuts. Keep exactly the same subject, style, colors and background as the first frame. No text, no labels, no letters, no new objects, no people.",
 "image-I1": f"Square 1:1 {STYLE}, of an amber glass dropper bottle with a small sprig of fresh rosemary and two golden drops falling onto a hair parting seen from above, natural dark hair with a few silver strands. Diagram-style picto, centered with generous empty space around it, flat shapes, no photographic texture. Calm, precise, minimal, no face. No text, no labels, no letters, no numbers, no watermark.",
 "image-I2": f"Square 1:1 {STYLE}, of two hands gently massaging the top of a head of natural dark wavy hair with a few silver strands, seen from above, small curved motion lines around the fingertips. Diagram-style picto, centered with generous empty space around it, flat shapes, no photographic texture. Calm, precise, minimal, no face. No text, no labels, no letters, no numbers, no watermark.",
 "objet-O1": "A single plain white jar of collagen powder with an unlabeled lid slightly open and a small wooden spoon of fine white powder resting against it, photorealistic studio product shot, three-quarter view, soft studio light, crisp edges, isolated on a fully transparent background, no ground shadow, no plate, no text, no label, no logo.",
}
for k, v in IMG.items(): open(f"prompts/{k}.txt", "w").write(v + "\n")
for cid in clips: open(f"prompts/seedance-{cid}.txt", "w").write(seedance(cid) + "\n")

# Synthèse
cat = {}
def k(p):
    t = p["type"]
    if t.startswith("Écran"): return "Écran partagé"
    if t == "Avatar": return "Avatar + surimpression" if p["surimpression"] != "-" else "Avatar"
    if t.startswith("Avatar"): return "Avatar + surimpression"
    if t.startswith("Animation"): return "Animation"
    if t.startswith("Infographie"): return "Infographie"
    return "B-roll"
for p in P: cat[k(p)] = cat.get(k(p), 0) + p["fin"] - p["debut"]
av = sum(v for kk, v in cat.items() if kk.startswith("Avatar") or kk.startswith("Écran"))
L = []; A = L.append
A("# Découpage · Claire · Affinement des cheveux à la ménopause · Talking head\n")
A("**État : découpage livré (mode A). Aucun média généré, aucune dépense.** Temps calés sur l'alignement forcé MMS du texte exact du script (`mots_mms.json`).\n")
A("## 1. Synthèse\n")
A("- **Format détecté** : mécanisme + solutions (3 causes hormonales, puis 3 solutions et un CTA guide). Cible avatar 55 à 60 %.")
A(f"- **Durée** : {fr(DUR)} s · **débit** : {len(W)/DUR*60:.0f} mots/min · **{len(P)} plans** · durée moyenne {fr(DUR/len(P))} s")
A("- **Répartition** : " + " · ".join(f"{kk} {fr(v)} s ({v/DUR*100:.0f} %)" for kk, v in cat.items()))
A(f"- **Avatar visible (écran partagé compris)** : {fr(av)} s ({av/DUR*100:.0f} %), juste sous la cible de 55 % : le script détaille des gestes concrets (prise de sang, massage, huile) qui gagnent à être montrés.")
A(f"- **Clips avatar** : {len(clips)} (1 en 1:1 pour l'écran partagé, {len(clips)-1} en 9:16), **{sum(c['duree_a_demander'] for c in clips.values())} s à générer** (Seedance 2.5).")
A("- **Images** : 2 (lignes d'infographie) + 1 image de départ d'animation · **objet détouré** : 1 (collagène) · **animation éducative** : 1 (9,2 s) · **b-rolls à trouver** : 7 (aucun repris de la bibliothèque, à ta demande) · **preuve à fournir** : 0")
A("- **Transitions spéciales** : 3 (cercle entrée animation 4,30 s ; flash « Mais voici des solutions » 19,10 s ; cercle entrée infographie 40,75 s)")
A("- **Plus long bloc sans avatar** : 31,30 à 45,80 s (14,5 s : b-roll, démo en 2 plans, infographie qui se construit). Sous la limite de 15 s. Animation 4,30 à 13,50 s (9,2 s).")
A("- **Écarts script / audio** : aucun. Alignement MMS sur les 202 mots du script, un seul mot à score faible (« cinq », mot court, temps cohérent). Whisper entendait « eustrogène » et « empourageantes » : ce sont des erreurs de reconnaissance, la voix dit bien « œstrogènes » et « encourageantes ».")
A("- **Voix au montage** (charte du 2026-09-28) : voix off ElevenLabs d'origine partout, son Seedance coupé, chaque clip avatar recalé phrase par phrase sur la voix off.\n")
A("## 2. Tableau de découpage\n")
A("| # | Début | Fin | Durée | Texte exact | Type | Zoom | Surimpression | Ce qu'on voit | Règle | Mot déclencheur | Source |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|")
for p in P:
    A(f"| {p['id']} | {fr(p['debut'])} | {fr(p['fin'])} | {fr(p['fin']-p['debut'])} s | {p['texte']} | {p['type']} | {p['zoom']} | {p['surimpression']} | {p['voir']} | {p['regle']} | {p['declencheur']} | {p['source']} |")
A("\nCoupes : dans un silence, 0,05 à 0,3 s avant le premier mot (sauf P07 et P08, coupes d'angle sur l'avatar à une fin de groupe de mots, et P11 à P12, démo continue). Zooms avatar : A · C · B, C · A · B, A, B, C (jamais deux fois le même de suite).\n")
A("## 3. Clips avatar (Seedance 2.5)\n")
A("Recette validée (charte) : `reference_image_urls` = [image de départ] (`@Image1`), `reference_audio_urls` = [extrait] (`@Audio1`), `generate_audio: true`. Le son du clip sert aux lèvres ; au montage on garde la voix off et on recale chaque phrase.\n")
for cid, c in clips.items():
    ws = [w for w in W if c["clipStart"] - 0.01 <= w["start"] <= c["clipEnd"]]
    A(f"### {cid} · {c['format']} · `{c['fichier']}` · {fr(c['clipStart'])} → {fr(c['clipEnd'])} s ({fr(c['duree'])} s, demander {c['duree_a_demander']} s)\n")
    A(f"- Image de départ : `Claire/talking-head/_config/{'depart_1x1.png' if c['format']=='1:1' else ('depart_9x16_camera2.png' if cid=='A02' else 'depart_9x16.png')}` (pull bleu, 2026-10-08) · `clipStart` pour le montage : {c['clipStart']:.3f}")
    A("- Timeline des mots (temps dans le clip) : " + " ".join(f"{w['w']} {w['start']-c['clipStart']:.1f}" for w in ws))
    A(f"- Geste attendu : {GESTE[cid]}\n")
    A("```text\n" + seedance(cid) + "\n```\n")
A("## 4. Images, objet détouré et animation\n")
A("Style de la charte : pictos plats sur fond crème, palette de Claire. Aucun texte généré : les étiquettes sont posées au montage.\n")
A("### E1 · animation éducative (P02, 4,30 → 13,50 s)\n")
A("Étiquettes au montage : « Œstrogènes » 5,00 s · « Phase de croissance » 7,05 s · « DHT » 10,10 s · « Follicule » 12,65 s.\n")
A("**5a. Image de départ, GPT Image 2, 9:16** :\n\n```text\n" + IMG["image-E1"] + "\n```\n")
A("**5b. Animation, MiniMax H3 image vers vidéo, 10 s** :\n\n```text\n" + IMG["animation-E1"] + "\n```\n")
A("### I1, I2 · infographie à 2 lignes (P13, 40,75 → 45,80 s)\n")
A("Ligne 1 « Huile de romarin » sur « l'huile de romarin » (41,85 s), ligne 2 « Massage quotidien » sur « le massage quotidien » (43,10 s), surligneur sur « encourageantes » (45,00 s). GPT Image 2, 1:1.\n")
A("```text\n" + IMG["image-I1"] + "\n```\n\n```text\n" + IMG["image-I2"] + "\n```\n")
A("### O1 · objet détouré (P09, pope sur « complément » à 28,30 s)\n\nGPT Image 2, 1:1, fond transparent.\n\n```text\n" + IMG["objet-O1"] + "\n```\n")
A("### Carte du guide (P16, montage seul)\n\nCarte crème #FAF6F3 qui monte à côté de l'avatar à 52,30 s : titre « Comment traiter l'affinement des cheveux à la ménopause » en Fraunces terracotta, petit brin de romarin, « Les cheveux de Claire » en bas. Aucun coût.\n")
A("## 5. B-rolls à trouver\n")
A("Fiche : `brolls-a-trouver.html`. Dépôt : dossier `talking_head_broll_2/` à la racine du studio, fichiers `broll_01.mp4` à `broll_07.mp4`.\n")
A("| N° | Moment | Durée à trouver | Phrase | À voir |\n|---|---|---|---|---|")
for b in d["brolls"]:
    A(f"| {b['id']} | {fr(b['debut'])} → {fr(b['fin'])} s | {fr(b['fin']-b['debut']+1)} s | {b['phrase']} | {b['voir']} |")
A("\n## 6. Accroche : bandeau choisi, n° 2 (les deux autres pour mémoire)\n")
A("1. « Cheveux plus fins à la ménopause ? Voici pourquoi »\n2. « 2 femmes sur 3 voient leurs cheveux s'affiner à la ménopause »\n3. « Ménopause : vos cheveux s'affinent, ce n'est pas une fatalité »\n")
A("## 7. Preuves à fournir\n\nAucune.\n")
open("decoupage.md", "w").write("\n".join(L) + "\n")
print(cat, av)
