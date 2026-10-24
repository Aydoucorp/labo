# Génère brolls-a-generer.html : prompts des b-rolls de la vidéo « tempes, réponse à un commentaire ».
import html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
S3D = ("Scientific 3D medical render, same style as the reference images: semi-realistic cutaway of scalp skin in soft pink and peach layers with a cream fat layer, "
       "hair follicles and glossy dark-brown hairs, terracotta and cream palette, dark plum gradient background, soft warm studio light with a gentle orange glow, "
       "clean and readable, vertical 9:16, the key element in the upper two thirds, the lower third calm for subtitles. No text, no letters, no labels, no logo.")
MOT3D = "Slow, smooth camera, one clear action readable at a glance without sound, no cuts, no morphing, same look from the first to the last frame."
AV = ("Image 1 is the woman: same face, same freckles and fine lines, same brown eyes, same long medium-dark brown hair, same terracotta knit sweater, same apparent age. "
      "Realistic smartphone photo, natural window light, natural skin texture, no beauty filter. No text, no logo, no watermark.")
plans = [
 dict(id="B1", t="7,75 à 13,30 s (5,6 s)", phrase="Ici, les follicules restent ancrés moins longtemps, donc tu vois plus de chute et des cheveux plus courts.",
  but="On voit un follicule de la tempe qui garde son cheveu moins longtemps : le cheveu tombe vite, le suivant repousse plus court.", genre="3D prune (style des premières vidéos)",
  entree="Image : texte seul (tu peux ajouter style-3d-prune-08.jpg en référence de style). Vidéo : l'image obtenue en input.", fichier="B1-ancrage-3d.mp4",
  img=S3D + " Scene: a cutaway block of temple scalp skin, one hair follicle anchored in it with a long healthy hair; next to it, a faint ghost outline shows where a previous hair used to be.",
  vid=S3D + " " + MOT3D + " The long hair loosens in its follicle and slides out after only a short moment, falling away; a new hair starts growing from the same follicle but stops much shorter and finer, then also loosens and slides out early. A soft terracotta glow highlights the follicle each time it lets go. What must be obvious: here, hairs stay anchored for a shorter time, so they fall sooner and stay shorter."),
 dict(id="B2a", t="13,30 à 16,40 s", phrase="Cette zone subit de la tension constante : queues de cheval…",
  but="Gros plan de la tempe tirée par une queue de cheval serrée.", genre="Image avatar (animée au montage)", entree="Image : retenues/cadrage.png en input. Pas de vidéo.", fichier="B2a-queue-de-cheval.png",
  img=AV + " Close-up in three-quarter view of her right temple and hairline: she is pulling her hair back very tightly into a high ponytail with both hands, the hair at the temple is visibly stretched and pulled, the skin of the temple slightly lifted by the tension."),
 dict(id="B2b", t="16,40 à 17,28 s", phrase="…chignons flous…",
  but="Chignon flou noué haut, la tempe tirée.", genre="Image avatar (animée au montage)", entree="Image : retenues/cadrage.png en input. Pas de vidéo.", fichier="B2b-chignon-flou.png",
  img=AV + " Close-up in three-quarter view of her head from the side: her hair is gathered into a messy top bun, the hair at her temple and hairline is pulled up toward the bun, a few loose strands, the tension at the temple visible."),
 dict(id="B2c", t="17,28 à 17,88 s", phrase="…bandeaux…",
  but="Bandeau en tissu serré qui appuie sur les tempes.", genre="Image avatar (animée au montage)", entree="Image : retenues/cadrage.png en input. Pas de vidéo.", fichier="B2c-bandeau.png",
  img=AV + " Close-up of her face and forehead from slightly to the side: she wears a wide fabric headband pushed back on her hair, pressing tightly right over her temples and hairline."),
 dict(id="B2d", t="17,88 à 19,40 s", phrase="…lunettes de soleil sur la tête…",
  but="Lunettes de soleil posées sur la tête, les branches appuient sur les tempes.", genre="Image avatar (animée au montage)", entree="Image : retenues/cadrage.png en input. Pas de vidéo.", fichier="B2d-lunettes.png",
  img=AV + " Close-up in three-quarter view: sunglasses pushed up on top of her head like a headband, the arms of the glasses pressing into the hair right at her temples, outdoors on a sunny terrace."),
 dict(id="B3", t="26,85 à 31,75 s (4,9 s)", phrase="La plupart des femmes concentrent leur shampoing à l'arrière de la tête et oublient complètement les tempes.",
  but="Sous la douche, elle mousse seulement l'arrière de la tête ; ses tempes restent sans mousse.", genre="Vidéo avatar", entree="Image : retenues/cadrage.png en input. Vidéo : l'image obtenue en input.", fichier="B3-douche.mp4",
  img=AV + " She is in a bright shower, seen from the side and slightly behind, wet hair, shampoo foam only on the back of her head, the hair at her temples and front hairline wet but completely without foam. Steam, soft bathroom light. Bare shoulders only, tasteful framing from the shoulders up.",
  vid="Vertical 9:16 smartphone video starting from the input image, same woman, same shower. She scrubs the back of her head with both hands, lots of foam at the back, while her temples and front hairline stay clearly without any foam the whole time. Natural movements, water running, slight handheld feel, tasteful framing from the shoulders up, no text, no logo. She does not speak."),
 dict(id="B4", t="31,75 à 36,60 s (4,85 s)", phrase="Résultat, les dépôts de produits, la transpiration et les traces de fond de teint ou de crème du visage…",
  but="Gros plan de la tempe : film de crème, traces beiges de fond de teint et gouttes de transpiration à la racine des cheveux.", genre="Vidéo avatar (macro)", entree="Image : retenues/cadrage.png en input. Vidéo : l'image obtenue en input.", fichier="B4-depots-tempe.mp4",
  img=AV + " Extreme macro close-up of her temple hairline: beige foundation residue and a shiny film of face cream caught at the roots of the fine hairs, small beads of sweat on the skin, a few product flakes. Realistic macro photo, natural light.",
  vid="Vertical 9:16 macro smartphone video starting from the input image: very slow glide along her temple hairline, the beige foundation traces and the shiny cream film at the roots catch the light, a bead of sweat slowly runs down among the fine hairs. Realistic, no text, no logo."),
 dict(id="B5", t="36,60 à 40,45 s (3,85 s)", phrase="…stagnent plus longtemps à cet endroit, ce qui peut aggraver la chute.",
  but="Les dépôts s'accumulent à l'entrée du follicule de la tempe, la peau rougit, le cheveu se détache.", genre="3D prune (style des premières vidéos)", entree="Image : texte seul. Vidéo : l'image obtenue en input.", fichier="B5-depots-3d.mp4",
  img=S3D + " Scene: close cutaway of temple scalp skin with one follicle and its hair; on the skin surface around the hair, small beige and translucent particles (product residue, sweat, makeup) begin to gather.",
  vid=S3D + " " + MOT3D + " The beige and translucent residue particles pile up and form a sticky layer that clogs the opening of the follicle; the skin around it turns a soft irritated red, the bulb dims, and the hair slowly loosens and comes out. What must be obvious: residues stuck at the temple make the hair fall."),
 dict(id="B6", t="44,30 à 49,60 s (5,3 s)", phrase="Ton visage paraît moins lifté, ta ligne frontale paraît fragile, et te coiffer devient plus compliqué.",
  but="Devant le miroir, elle regarde ses tempes clairsemées, puis essaie de coiffer le devant et soupire.", genre="Vidéo avatar", entree="Image : retenues/cadrage.png en input. Vidéo : l'image obtenue en input.", fichier="B6-miroir.mp4",
  img=AV + " She stands in front of her bathroom mirror, seen over her shoulder with her reflection visible: her hair down, the temples and front hairline visibly thin, she lifts her hair at the temple with her fingertips, a slightly worried expression in the reflection.",
  vid="Vertical 9:16 smartphone video starting from the input image: in the mirror she lifts the hair at her temples to look at the thin hairline, lets it fall, then tries to style the front with a round brush, the hair falls flat again, she sighs and puts the brush down, slightly discouraged. Natural movements, realistic, no text, no logo. She does not speak."),
]
def bloc(titre, txt, k):
    return f'<div class="p"><div class="ph"><span>{titre}</span><button onclick="cp(\'{k}\',this)">Copier</button></div><pre id="{k}">{html.escape(txt)}</pre></div>'
cards = ""
for p in plans:
    blocs = bloc("Prompt image", p["img"], p["id"] + "-img") + (bloc("Prompt vidéo", p["vid"], p["id"] + "-vid") if p.get("vid") else "")
    cards += f'''<section class="card"><div class="top"><span class="id">{p["id"]}</span><span class="genre">{p["genre"]}</span><span class="t">{p["t"]}</span></div>
<p class="phrase">« {html.escape(p["phrase"])} »</p><p class="but"><b>On doit comprendre :</b> {html.escape(p["but"])}</p>
<p class="meta"><b>Input :</b> {html.escape(p["entree"])}<br><b>Nom du fichier à me renvoyer :</b> <code>{p["fichier"]}</code></p>{blocs}</section>'''
css = open(pathlib.Path("/home/user/labo/runs/2026-10-23_claire-tempes-affinement_ugc-humain/brolls-a-generer.html")).read()
style = css[css.index("<style>"):css.index("</style>") + 8]
script = css[css.index("<script>"):css.index("</script>") + 9]
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>B-rolls tempes commentaire</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
{style}</head><body><main>
<h1>B-rolls à générer · Tempes, réponse à un commentaire</h1>
<div class="intro"><ul>
<li>Chaque b-roll colle à 100 % à la phrase dite, se comprend sans le son et reste agréable à regarder.</li>
<li>3D : le style des premières vidéos (fond prune, coupe de peau semi-réaliste, lueur orange douce), en plus explicite. Références de style : <code>references/style-3d-prune-08.jpg</code> et <code>-10.jpg</code>.</li>
<li>Avatar : <code>retenues/cadrage.png</code> en input (pull terracotta). B2a à B2d sont des images seules : je les anime au montage, une par mot.</li>
<li>Génère d'abord l'image, envoie-la-moi, puis lance la vidéo avec l'image en input. Si ton outil fait des vidéos plus longues, je prends les bonnes secondes.</li>
<li>Les plans « micro-tensions » et « zone délicate » sont en face caméra et en motion design, rien à générer.</li>
</ul></div>
{cards}
</main>{script}</body></html>'''
(R / "1-brolls-tempes-commentaire.html").write_text(page)
print("ok")
