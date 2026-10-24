# Génère 1-brolls-tempes-commentaire.html : prompts « bodybuildés » des b-rolls (aucune liberté laissée au modèle).
import html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent

STYLE3D = """STYLE: scientific 3D medical animation, semi-realistic, clean and premium, exactly like a medical explainer render: smooth soft-matte skin tissue, glossy hair shafts, subtle subsurface glow. Colour palette locked: skin epidermis pale cream-pink #F3D5C5, dermis soft pink #E9A99A with thin red capillaries #B5483F, fat layer cream-yellow #F2DDB0, hair shaft glossy dark brown #3B2A22, follicle bulb terracotta-pink #C9805F with a warm orange inner glow #F0A050. Background: smooth dark plum gradient, #3A1E2B in the centre fading to #22101A at the edges, completely empty, no floor, no horizon.
LIGHTING: one soft warm key light from the upper left, a thin warm rim light on the edges of the skin block, gentle soft shadows, no harsh contrast, no lens flare."""
FORBID3D = """FORBIDDEN: any text, letter, number, label, arrow, icon, UI or watermark; humans, faces, hands, eyes; blood, wounds or gore; cartoon or flat 2D style; more follicles than described; morphing or melting of the skin block; any change of background colour; camera shake; cuts or scene changes; zoom other than described; extra objects."""

VIDB1 = f"""FORMAT: vertical 9:16, 6 seconds, one single continuous shot, no cuts.
{STYLE3D}
CAMERA: perfectly side-on view of the cut face of the skin block, eye level with the skin surface, 50 mm lens look. Static from 0.0 s to 4.0 s, then a very slow push-in of about 10 % from 4.0 s to 6.0 s. The block is centred horizontally and fills 70 % of the frame width; the skin surface sits at 50 % of the frame height; the lower 25 % of the frame is empty dark plum background (room for subtitles).
SUBJECT: one rectangular cutaway block of human scalp skin seen in cross-section, three clearly separated layers from top to bottom: thin epidermis, thick dermis with fine capillaries, cream-yellow fat layer. Exactly ONE hair follicle in the centre of the block: a narrow tube going straight down from the surface into the dermis, ending in a rounded bulb with a warm orange glow. Exactly ONE long glossy dark-brown hair rises straight up out of the surface from this follicle, reaching the top of the frame.
ACTION TIMELINE (follow exactly):
0.0 to 1.5 s: everything still and healthy: the long hair stands straight, the bulb glows warm and steady.
1.5 to 2.5 s: the bulb glow fades, the bulb shrinks slightly and lets go; the long hair slides upward out of the follicle and floats out of the top of the frame.
2.5 to 4.0 s: a new hair grows out of the same follicle, visibly half as thick as the first one, and it stops growing at only half the height the first hair reached; the bulb glow is weaker.
4.0 to 5.0 s: this second, shorter hair already loosens and slides out, floating away upward, much sooner than the first.
5.0 to 6.0 s: the follicle stays empty with a faint glow; a third, very thin hair just starts to peek out of the surface.
MUST STAY IDENTICAL FROM FIRST TO LAST FRAME: the skin block, its position, its three layers, the single follicle, the colours, the lighting, the background.
MESSAGE THAT MUST BE OBVIOUS WITHOUT SOUND: at the temples, hairs stay anchored for a shorter time, so they fall sooner and grow back shorter.
{FORBID3D}"""

VIDB5 = f"""FORMAT: vertical 9:16, 4 seconds, one single continuous shot, no cuts.
{STYLE3D}
CAMERA: close-up of a cutaway block of temple skin, camera slightly above the skin surface (about 20 degrees above it) so we see both the cut face of the layers and the top of the skin surface around the hair. 50 mm lens look. Slow steady push-in from 100 % to 115 % over the 4 seconds, centred on the follicle opening. The follicle opening sits at 45 % of the frame height; the lower 25 % of the frame stays empty dark plum background (room for subtitles).
SUBJECT: one cutaway block of scalp skin with three layers (epidermis, dermis with capillaries, fat). Exactly ONE hair follicle in the centre with exactly ONE healthy glossy dark-brown hair coming out of its opening; the bulb at the bottom glows warm orange.
ACTION TIMELINE (follow exactly):
0.0 to 1.0 s: clean healthy skin surface. Small particles start falling gently onto the surface around the hair: matte beige foundation particles #D9B38C, glossy translucent cream droplets, tiny clear sweat droplets.
1.0 to 2.5 s: the particles pile up around the hair and merge into a sticky beige-translucent layer that fills and clogs the opening of the follicle; the skin right around the opening turns a soft irritated red #C8504A.
2.5 to 4.0 s: the bulb glow dims to a dull grey-pink, the hair loosens and slowly slides upward out of the clogged opening and drifts away.
MUST STAY IDENTICAL FROM FIRST TO LAST FRAME: the skin block, its position, the single follicle, the colours, the lighting, the background.
MESSAGE THAT MUST BE OBVIOUS WITHOUT SOUND: residues of products, makeup and sweat stuck at the temple clog the follicle and make the hair fall.
{FORBID3D}"""

HAUT = """INPUT: Image 1 is the woman (identity and hair reference only).
FORMAT: vertical 9:16 photo, realistic, shot on a smartphone.
CAMERA: directly ABOVE her head, lens pointing straight down at 90 degrees, phone held about 40 cm above the top of her head, 26 mm smartphone lens. Her head is slightly tilted forward so that ONLY the top of the head is visible. Framing: the crown and the front hairline fill the centre of the frame, the front hairline at about 35 % from the top of the frame, both temples clearly visible on the left and right of the hairline. Her shoulders appear only at the bottom corners, in a plain BLACK fine-knit sweater (NOT the terracotta sweater of Image 1).
HAIR (copy Image 1 exactly): long, thick, medium-dark brown, one even natural colour with soft warm highlights, soft waves in the lengths, healthy density, NO grey, NO blonde, NO highlights stripes.
LIGHT: soft natural daylight from a window at the front-left, gentle soft shadows, no flash, true-to-life colours, sharp focus on the roots, the hairline and the temples.
BACKGROUND: out of focus far below her: a plain warm beige floor, nothing else."""
FORBIDH = """FORBIDDEN: the terracotta sweater or any colour other than black on her shoulders; her face, eyes, nose, mouth or ears seen from the front; hands; other people; any text, logo or watermark; grey or blonde hair; wigs; cartoon or illustration look; beauty filter; extra accessories not described."""

AVATAR = """INPUT: Image 1 is the woman: copy exactly her face, facial features, freckles, fine lines, brown eyes, apparent age (mid forties), body build and her long medium-dark brown hair (one even colour, soft waves, no grey, no blonde).
FORMAT: vertical 9:16, realistic smartphone photo, natural skin texture with visible pores, freckles and fine lines, no beauty filter, true-to-life colours."""
FORBIDA = """FORBIDDEN: a different face or age; grey or blonde hair; text, logo, watermark, brand names; extra people; nudity (shoulders only); cartoon or illustration look; harsh flash; heavy makeup."""

plans = [
 dict(id="B1", genre="Vidéo 3D, texte seul", t="7,75 à 13,30 s (5,6 s)", phrase="Ici, les follicules restent ancrés moins longtemps, donc tu vois plus de chute et des cheveux plus courts.",
  but="Un seul follicule : le cheveu se détache vite, le suivant repousse deux fois plus fin et plus court, et tombe encore plus tôt.", entree="Aucune : vidéo directement à partir du texte.", fichier="B1-ancrage-3d.mp4", vid=VIDB1),
 dict(id="B2a", genre="Image avatar, vue du dessus", t="13,30 à 16,40 s", phrase="Cette zone subit de la tension constante : queues de cheval…",
  but="Vue du dessus : queue de cheval haute et très serrée, les tempes étirées.", entree="retenues/cadrage.png", fichier="B2a-queue-de-cheval.png",
  img=HAUT + """
SUBJECT: her hair is pulled back extremely tightly into a high ponytail fixed at the crown with a thin black hair tie; from above, every strand runs in tight straight parallel lines from the front hairline and from both temples back to the hair tie; at both temples the hair is visibly stretched thin and pulled, the pale skin of the temples showing between the stretched strands; the ponytail itself falls back out of frame at the top.
""" + FORBIDH),
 dict(id="B2b", genre="Image avatar, vue du dessus", t="16,40 à 17,28 s", phrase="…chignons flous…",
  but="Vue du dessus : chignon flou au sommet de la tête, les tempes tirées vers lui.", entree="retenues/cadrage.png", fichier="B2b-chignon-flou.png",
  img=HAUT + """
SUBJECT: her hair is twisted into a loose messy bun sitting exactly on the top of her head, in the centre of the frame, held by a brown hair tie, with a few loose strands sticking out; from above, all the hair from the front hairline and from both temples is pulled up toward the bun in visible tight lines, the hair at both temples stretched and lifted.
""" + FORBIDH),
 dict(id="B2c", genre="Image avatar, vue du dessus", t="17,28 à 17,88 s", phrase="…bandeaux…",
  but="Vue du dessus : bandeau en tissu prune posé juste derrière la ligne frontale, qui écrase les tempes.", entree="retenues/cadrage.png", fichier="B2c-bandeau.png",
  img=HAUT + """
SUBJECT: her hair is down and she wears a wide (about 5 cm) plain fabric headband in a muted plum colour #7A4351, placed just behind the front hairline; from above, the headband crosses the head in a curve from one temple to the other, and at both temples it visibly presses the hair flat against the head, the band slightly digging into the hair there.
""" + FORBIDH),
 dict(id="B2d", genre="Image avatar, vue du dessus", t="17,88 à 19,40 s", phrase="…lunettes de soleil sur la tête…",
  but="Vue du dessus : lunettes de soleil remontées sur la tête, les branches enfoncées dans les cheveux aux tempes.", entree="retenues/cadrage.png", fichier="B2d-lunettes.png",
  img=HAUT.replace("BACKGROUND: out of focus far below her: a plain warm beige floor, nothing else.", "BACKGROUND: out of focus far below her: light stone paving of a sunny terrace, nothing else.") + """
SUBJECT: her hair is down and a pair of dark tortoiseshell sunglasses is pushed up on top of her head like a headband, sitting just behind the front hairline; from above, the dark frame crosses the front of the head and the two arms of the glasses press firmly into the hair right at both temples, the hair visibly squeezed under them. Soft outdoor daylight.
""" + FORBIDH),
 dict(id="B3", genre="Vidéo avatar (image puis vidéo)", t="26,85 à 31,75 s (4,9 s)", phrase="La plupart des femmes concentrent leur shampoing à l'arrière de la tête et oublient complètement les tempes.",
  but="Sous la douche, la mousse seulement à l'arrière de la tête, les tempes mouillées mais sans mousse.", entree="Image : retenues/cadrage.png. Vidéo : l'image obtenue.", fichier="B3-douche.mp4",
  img=AVATAR + """
CAMERA: three-quarter rear view from her right side, at head height, 1 m away, framing from the top of her head to her bare shoulders, her right temple and right front hairline clearly visible in profile.
SCENE: she stands in a bright white-tiled shower, light steam, soft daylight from a frosted window. Her hair is wet and darker, slicked back. Thick white shampoo foam covers ONLY the back of her head (from the crown to the nape); the front hairline and the temple are wet but completely WITHOUT any foam, clearly bare and shiny. Both her hands are at the back of her head, fingers in the foam.
""" + FORBIDA,
  vid="""FORMAT: vertical 9:16, 5 seconds, one continuous shot, starting exactly from the input image, same woman, same shower, same framing.
CAMERA: static, at head height, slight natural handheld micro-movement only, no zoom.
ACTION TIMELINE:
0.0 to 3.5 s: she scrubs the back of her head energetically with both hands, the foam grows thicker at the back and on the crown; water runs down.
3.5 to 5.0 s: she keeps scrubbing the back; her temple and front hairline stay wet and shiny but completely WITHOUT foam the whole time, and her hands never touch the temples.
MUST STAY IDENTICAL: her face, hair colour, the shower, the light. She does not speak.
FORBIDDEN: foam on the temples or the front hairline; hands touching the temples; nudity below the shoulders; text, logo, brand names; cuts; zoom."""),
 dict(id="B4", genre="Vidéo avatar macro (image puis vidéo)", t="31,75 à 36,60 s (4,85 s)", phrase="Résultat, les dépôts de produits, la transpiration et les traces de fond de teint ou de crème du visage…",
  but="Macro de la tempe : traces beiges de fond de teint, film brillant de crème et gouttes de transpiration à la racine des cheveux.", entree="Image : retenues/cadrage.png. Vidéo : l'image obtenue.", fichier="B4-depots-tempe.mp4",
  img=AVATAR + """
CAMERA: extreme macro close-up of her right temple hairline, phone macro mode, about 5 cm from the skin, the hairline running diagonally across the frame from the upper left to the lower right; the skin of the temple fills the lower half, the first fine baby hairs and the roots of her brown hair fill the upper half.
SCENE: along the roots and the fine baby hairs: matte beige traces of foundation caught between the hairs, a thin shiny film of face cream on the skin at the roots, three or four small clear beads of sweat on the skin, a few tiny dried product flakes. Natural soft daylight from the left grazing the skin so the residue and the sweat catch the light.
""" + FORBIDA,
  vid="""FORMAT: vertical 9:16, 5 seconds, one continuous macro shot, starting exactly from the input image.
CAMERA: very slow smooth glide along the hairline from the lower right to the upper left, about 1 cm of travel in total, constant macro distance, no zoom.
ACTION TIMELINE:
0.0 to 2.5 s: the beige foundation traces and the shiny cream film at the roots catch the light as the camera glides.
2.5 to 5.0 s: one bead of sweat slowly runs down the temple through the fine baby hairs, leaving a shiny trail across a beige foundation trace.
MUST STAY IDENTICAL: skin tone, hair colour, the residue, the light.
FORBIDDEN: text, logo; face or eyes in frame; extra objects; hands; cuts; morphing of the skin."""),
 dict(id="B5", genre="Vidéo 3D, texte seul", t="36,60 à 40,45 s (3,85 s)", phrase="…stagnent plus longtemps à cet endroit, ce qui peut aggraver la chute.",
  but="Les dépôts s'accumulent et bouchent l'entrée du follicule, la peau rougit, le cheveu se détache.", entree="Aucune : vidéo directement à partir du texte.", fichier="B5-depots-3d.mp4", vid=VIDB5),
 dict(id="B6", genre="Vidéo avatar (image puis vidéo)", t="44,30 à 49,60 s (5,3 s)", phrase="Ton visage paraît moins lifté, ta ligne frontale paraît fragile, et te coiffer devient plus compliqué.",
  but="Devant le miroir, elle soulève ses cheveux aux tempes, voit la ligne frontale clairsemée, essaie de coiffer le devant à la brosse, les cheveux retombent, elle soupire.", entree="Image : retenues/cadrage.png. Vidéo : l'image obtenue.", fichier="B6-miroir.mp4",
  img=AVATAR + """
CAMERA: over-the-shoulder shot from behind her left shoulder, at head height, the bathroom mirror filling most of the frame so we see her reflection face-on from the chest up; her real shoulder and back of the head blurred in the foreground left.
SCENE: a bright simple bathroom, white wall, round mirror, soft daylight from the side. She wears the same terracotta knit sweater, her hair is down. In the reflection, with the fingertips of her right hand she lifts the hair at her right temple, revealing a visibly thinner temple and a fragile, slightly receded front hairline; her expression in the reflection is slightly worried, eyebrows drawn together. A round brush lies on the sink edge.
""" + FORBIDA,
  vid="""FORMAT: vertical 9:16, 6 seconds, one continuous shot, starting exactly from the input image, same woman, same bathroom, same framing.
CAMERA: static over-the-shoulder, slight natural handheld micro-movement, no zoom.
ACTION TIMELINE:
0.0 to 2.0 s: in the mirror she lifts the hair at her temple and looks closely at the thin hairline, worried.
2.0 to 4.5 s: she lets the hair fall, picks up the round brush from the sink and tries to lift and style the front of her hair; as soon as she lets go, the hair falls flat again.
4.5 to 6.0 s: she puts the brush down, lets out a small sigh, shoulders drop slightly, discouraged.
MUST STAY IDENTICAL: her face, hair colour, sweater, the bathroom, the light. She does not speak.
FORBIDDEN: a different face; text, logo, brand names; extra people; cuts; zoom; the reflection not matching her movements."""),
]
def bloc(titre, txt, k):
    return f'<div class="p"><div class="ph"><span>{titre}</span><button onclick="cp(\'{k}\',this)">Copier</button></div><pre id="{k}">{html.escape(txt)}</pre></div>'
cards = ""
for p in plans:
    b = ""
    if p.get("img"): b += bloc("Prompt image", p["img"], p["id"] + "-img")
    if p.get("vid"): b += bloc("Prompt vidéo" + (" (texte seul)" if not p.get("img") else ""), p["vid"], p["id"] + "-vid")
    cards += f'''<section class="card"><div class="top"><span class="id">{p["id"]}</span><span class="genre">{p["genre"]}</span><span class="t">{p["t"]}</span></div>
<p class="phrase">« {html.escape(p["phrase"])} »</p><p class="but"><b>On doit comprendre :</b> {html.escape(p["but"])}</p>
<p class="meta"><b>Input :</b> {html.escape(p["entree"])}<br><b>Nom du fichier à me renvoyer :</b> <code>{p["fichier"]}</code></p>{b}</section>'''
ref = open("/home/user/labo/runs/2026-10-23_claire-tempes-affinement_ugc-humain/brolls-a-generer.html").read()
style = ref[ref.index("<style>"):ref.index("</style>") + 8]; script = ref[ref.index("<script>"):ref.index("</script>") + 9]
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>B-rolls tempes commentaire</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
{style}</head><body><main>
<h1>1 · B-rolls à générer · Tempes, réponse à un commentaire</h1>
<div class="intro"><ul>
<li>Prompts « bodybuildés » : format, caméra, cadrage, couleurs exactes, déroulé seconde par seconde, ce qui ne doit pas bouger et ce qui est interdit. Le modèle n'a aucune liberté.</li>
<li>B1 et B5 (3D, style des premières vidéos sur fond prune) : <b>vidéo directement à partir du texte</b>, pas d'image.</li>
<li>B2a à B2d : images seules vues du dessus (input : <code>retenues/cadrage.png</code>), avec un <b>pull noir</b> (pas le pull terracotta), animées au montage, une par mot.</li>
<li>B3, B4, B6 : l'avatar doit garder son visage, donc image d'abord (input : <code>retenues/cadrage.png</code>), puis vidéo avec l'image obtenue.</li>
<li>Chaque b-roll colle à 100 % à la phrase dite et se comprend sans le son. Si ton outil génère plus long, je prends les bonnes secondes.</li>
</ul></div>
{cards}
</main>{script}</body></html>'''
(R / "1-brolls-tempes-commentaire.html").write_text(page)
for p in plans:
    for k in ("img", "vid"):
        if p.get(k): print(p["id"], k, len(p[k]), "caractères")
