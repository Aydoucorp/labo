# Génère brolls-a-generer.html (prompts b-roll de la vidéo tempes, partie 1)
import html, pathlib
STYLE = ("Hyper-realistic cinematic 3D medical animation, like a premium anatomy documentary: glossy, wet-looking, finely detailed anatomical materials "
"(skin layers in pink and peach, hair follicles, arteries in saturated red, veins in deep blue), the subject isolated in the centre on a pure black background, "
"lit by a single soft spotlight from above with a subtle rim light, deep shadows, high contrast, crisp micro detail, shallow depth of field on macro shots, "
"a few tiny floating particles in the air. Vertical 9:16, the subject in the upper two thirds of the frame, the lower third kept dark and empty for subtitles. "
"Absolutely no text, letters, numbers, labels, arrows, watermarks or logos.")
MOTION = ("Slow cinematic camera move (orbit, push-in or fly-through), one single clear transformation, readable at a glance by someone watching without sound. "
"No cuts, no scene change, no shake. Same look and lighting as the input image from the first to the last frame.")
plans = [
 dict(id="B1", t="18,05 à 21,70 s (3,6 s)", phrase="À cet âge, c'est au niveau des tempes que les cheveux commencent à s'affiner.",
  but="On voit sur l'avatar une tempe qui se dégarnit : cheveux fins et clairsemés, peau visible.", genre="Photo réaliste (avatar)",
  entree="Image : mets `cadrage-v2.png` (l'avatar) en input. Vidéo : l'image obtenue en input.",
  etiquettes="aucune", fichier="B1-tempe.mp4",
  img=("Image 1 is the woman: same face, same medium-dark brown hair colour and texture, same skin tone with freckles and fine lines, same oatmeal knit sweater, same tiny stud earring. "
   "New photo, vertical 9:16, shot on iPhone, close-up of the right side of her head in three-quarter profile: her right temple and hairline fill most of the frame, her eye and cheekbone at the edge of the frame, "
   "her hair pulled back tightly into a low ponytail. The temple is visibly thinning: the hair at the temple and in front of the ear is sparse, fine and short, the skin of the temple shows through, "
   "the corner of the hairline slightly receded, with a few wispy baby hairs. Natural soft window light from the front-left, blurred sage-green wall behind, sharp detail on the hair strands and skin, "
   "realistic, no beauty filter. No text, no logo, no watermark."),
  vid=("Vertical 9:16 handheld smartphone video, starting from the input image and keeping the same close-up: the thinning temple stays the subject the whole time and stays as sparse as in the input image, never fuller. "
   "Dynamic real gestures, never stiff: her fingertips come into frame and pull the hair back from the temple in one quick movement to reveal the sparse area, then run along the receding corner of the hairline, "
   "push the fine baby hairs aside, and press lightly on the temple. Natural handheld micro-shake, natural daylight, sharp detail on the hair and skin, realistic, shot on iPhone, no text, no logo. She does not speak.")),
 dict(id="B2", t="21,70 à 24,90 s (3,2 s)", phrase="C'est l'un des signes les plus révélateurs que le cycle de pousse se raccourcit…",
  but="On comprend que le temps de pousse de chaque cheveu devient de plus en plus court.", genre="3D pédagogique",
  entree="Image : texte seul. Vidéo : l'image obtenue en input.", etiquettes="« CYCLE DE POUSSE », puis « DE PLUS EN PLUS COURT »", fichier="B2-cycle.mp4",
  img=STYLE + ' Scene: a glossy cross-section block of human scalp skin floating in the black void, its layers clearly visible, one hair follicle inside it and a long, healthy, shiny dark-brown hair growing straight up from it. A thin glowing golden ring floats horizontally around the hair at the skin surface, like a timer, fully lit.',
  vid=STYLE + " " + MOTION + ' Starting from the input image, in time-lapse: the hair grows long and strong while the golden ring stays fully lit; the hair detaches and falls away into the dark; a new hair grows but the golden ring is now only half lit, and this hair stops at half the length and falls out sooner; a third hair grows even shorter, the ring only a quarter lit. Slow orbit around the block. What must be obvious: each growth cycle is shorter than the one before.'),
 dict(id="B3", t="24,90 à 27,85 s (3 s)", phrase="…et que les follicules de cette zone se fragilisent.",
  but="On voit un follicule sain qui s'affaiblit sous nos yeux.", genre="3D pédagogique",
  entree="Aucune : vidéo en texte seul.", etiquettes="« FOLLICULE FRAGILISÉ »", fichier="B3-follicule.mp4",
  img=STYLE + ' Scene: macro view deep inside the scalp: a single plump, glossy hair follicle bulb, healthy pink-red, wrapped in a fine network of bright red blood vessels, a thick shiny dark hair shaft rising from it, floating in a dark tissue environment with a soft spotlight.',
  vid=STYLE + " " + MOTION + ' Starting from the input image: the camera slowly pushes in on the bulb while it visibly weakens: the red blood vessels around it thin out and retract, the bulb shrinks, loses its colour and turns dull grey-pink, the hair shaft becomes thinner and lighter, and fine cracks spread across the follicle wall. What must be obvious: this follicle is becoming fragile.'),
 dict(id="B4", t="29,40 à 34,45 s (5 s)", phrase="Parce que tes tempes ont certains des follicules les plus fins et les plus délicats de tout ton cuir chevelu.",
  but="On voit où sont les tempes, puis la différence entre les follicules du haut de la tête (épais) et ceux des tempes (très fins).", genre="3D pédagogique",
  entree="Aucune : vidéo en texte seul.", etiquettes="« TEMPES » sur la zone, puis « HAUT DE LA TÊTE » à gauche et « TEMPES » à droite", fichier="B4-tempes.mp4",
  img=STYLE + ' Scene: a translucent glass-like 3D head of a woman in three-quarter view, isolated on black, the skull faintly visible inside and a dense network of bright red blood vessels running across the scalp and face; the hair is suggested as a faint translucent volume pulled back. Both temple areas glow warm orange-red, the rest of the head stays dim.',
  vid=STYLE + " " + MOTION + ' Starting from the input image: slow orbit toward the glowing temple, then the camera dives through the skin into a macro view of the follicles: on the left, three big deep follicles with thick shiny dark hairs (top of the head); on the right, three tiny shallow follicles with very thin, fine, almost transparent hairs that sway gently (the temple). The camera holds on this side-by-side comparison. What must be obvious: the temple follicles are much finer and more fragile than the others.'),
 dict(id="B5a", t="44,25 à 49,05 s (4,8 s)", phrase="Pendant la périménopause et la ménopause, les fluctuations hormonales touchent d'abord les tempes.",
  but="On voit les hormones qui fluctuent, et les tempes qui réagissent en premier.", genre="3D pédagogique",
  entree="Image : texte seul. Vidéo : l'image obtenue en input.", etiquettes="« PÉRIMÉNOPAUSE », « HORMONES »", fichier="B5a-hormones.mp4",
  img=STYLE + ' Scene: a holographic X-ray style 3D body of a woman, head to hips, front view, translucent blue-grey skin with the red blood vessel network and organs faintly visible, on a very dark blue-black background with a subtle scan-line glow.',
  vid=STYLE + " " + MOTION + ' Starting from the input image: soft pink pulses of light rise irregularly from the lower abdomen, swelling and fading like waves, travelling up through the chest and neck to the head; when they reach the head, both temples are the first areas to light up and flicker in bright warm orange, like warning lights, while the rest of the scalp stays calm. Slow push-in toward the head. What must be obvious: hormonal swings hit the temples first.'),
 dict(id="B5b", t="49,05 à 52,00 s (3 s)", phrase="Ton œstrogène baisse, ton cortisol augmente…",
  but="On voit un niveau qui baisse (œstrogène) et un niveau qui monte (cortisol) autour d'un follicule de la tempe.", genre="3D pédagogique",
  entree="Image : texte seul. Vidéo : l'image obtenue en input.", etiquettes="« ŒSTROGÈNE ↓ » à gauche, « CORTISOL ↑ » à droite", fichier="B5b-oestrogene-cortisol.mp4",
  img=STYLE + ' Scene: macro view of a single temple hair follicle with a thin hair in glossy pink tissue, isolated in dark space; on the left side, a dense cloud of soft glowing pink spheres surrounds it; on the right side, a few small sharp amber crystals.',
  vid=STYLE + " " + MOTION + ' Starting from the input image, both at the same time: the glowing pink spheres on the left dim and drift away until almost none remain, while the sharp amber crystals on the right multiply fast and swarm around the follicle; the follicle tightens, its surroundings turn an irritated red and the thin hair trembles. End on the contrast: almost no pink left, the follicle surrounded by amber. What must be obvious: one protective element goes down, a stress element goes up, and the follicle suffers.'),
]

MOTION_T = ("Slow cinematic camera move (orbit, push-in or fly-through), one single clear transformation, readable at a glance by someone watching without sound. "
"No cuts, no scene change, no shake.")
TEXTE_SEUL = {
 "B3": STYLE + " " + MOTION_T + " Opening shot: macro view deep inside the scalp, a single plump, glossy hair follicle bulb, healthy pink-red, wrapped in a fine network of bright red blood vessels, a thick shiny dark hair shaft rising from it, floating in a dark tissue environment under a soft spotlight. "
   "Then, as the camera slowly pushes in on the bulb, it visibly weakens: the red blood vessels around it thin out and retract, the bulb shrinks, loses its colour and turns dull grey-pink, the hair shaft becomes thinner and lighter, and fine cracks spread across the follicle wall. What must be obvious: this follicle is becoming fragile.",
 "B4": STYLE + " " + MOTION_T + " Opening shot: a translucent glass-like 3D head of a woman in three-quarter view, isolated on black, the skull faintly visible inside and a dense network of bright red blood vessels running across the scalp and face, the hair suggested as a faint translucent volume pulled back; both temple areas glow warm orange-red while the rest of the head stays dim. "
   "Then a slow orbit toward the glowing temple, and the camera dives through the skin into a macro view of the follicles: on the left, three big deep follicles with thick shiny dark hairs (top of the head); on the right, three tiny shallow follicles with very thin, fine, almost transparent hairs that sway gently (the temple). The camera holds on this side-by-side comparison. What must be obvious: the temple follicles are much finer and more fragile than the others.",
}

def bloc(titre, txt, k):
    return f'<div class="p"><div class="ph"><span>{titre}</span><button onclick="cp(\'{k}\',this)">Copier</button></div><pre id="{k}">{html.escape(txt)}</pre></div>'
cards = ""
for p in [x for x in plans if x["id"] in ("B1", "B3", "B4")]:  # B2, B5a, B5b faits en motion design
    cards += f'''<section class="card"><div class="top"><span class="id">{p["id"]}</span><span class="genre">{p["genre"]}</span><span class="t">{p["t"]}</span></div>
<p class="phrase">« {html.escape(p["phrase"])} »</p>
<p class="but"><b>On doit comprendre :</b> {html.escape(p["but"])}</p>
<p class="meta"><b>Input :</b> {html.escape(p["entree"]).replace("`","")}<br><b>Étiquettes ajoutées au montage :</b> {html.escape(p["etiquettes"])}<br><b>Nom du fichier à me renvoyer :</b> <code>{p["fichier"]}</code></p>
{(bloc("Prompt vidéo, texte seul (sans image de départ)", TEXTE_SEUL[p["id"]], p["id"]+"-vid") if p["id"] in TEXTE_SEUL else bloc("Prompt image", p["img"], p["id"]+"-img") + bloc("Prompt vidéo", p["vid"], p["id"]+"-vid"))}</section>'''
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>B-rolls tempes</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FAF6F3;--card:#fff;--line:#EFE7E0;--ink:#2E2A26;--muted:#6b635c;--accent:#A8553A;--accent2:#C9805F;--plum:#7A4351;--code:#FAF6F3}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1f1b18;--card:#2a2522;--line:#3a332e;--ink:#f3ece6;--muted:#b9afa6;--code:#231f1c;--accent:#C9805F}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 "Source Sans 3",system-ui,sans-serif}}
main{{max-width:880px;margin:0 auto;padding:32px 16px 64px}}h1{{font-family:Fraunces,serif;font-weight:600;font-size:30px;margin:0 0 6px;color:var(--accent)}}
.intro{{color:var(--muted);margin:0 0 24px}}.intro li{{margin:4px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:0 0 20px}}
.top{{display:flex;gap:10px;align-items:center;flex-wrap:wrap}}.id{{background:var(--accent);color:#fff;font-weight:600;border-radius:8px;padding:2px 10px}}
.genre{{color:var(--plum);font-weight:600}}@media (prefers-color-scheme:dark){{.genre{{color:#d9a3b0}}}}.t{{margin-left:auto;color:var(--muted);font-size:14px}}
.phrase{{font-family:Fraunces,serif;font-size:19px;margin:12px 0 8px}}.but,.meta{{margin:6px 0;font-size:15px}}.meta{{color:var(--muted)}}
code{{background:var(--code);border:1px solid var(--line);border-radius:6px;padding:1px 6px}}
.p{{margin-top:14px}}.ph{{display:flex;justify-content:space-between;align-items:center;font-weight:600;margin-bottom:6px}}
pre{{white-space:pre-wrap;word-wrap:break-word;background:var(--code);border:1px solid var(--line);border-radius:10px;padding:12px;margin:0;font:13.5px/1.5 ui-monospace,Menlo,monospace}}
button{{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:6px 14px;font:600 14px "Source Sans 3",sans-serif;cursor:pointer}}button.ok{{background:var(--plum)}}
</style></head><body><main>
<h1>B-rolls à générer · Tempes, partie 1</h1>
<div class="intro"><ul>
<li>3 plans à générer : 1 photo réaliste de l'avatar (B1) et 2 animations 3D style Drew Canole (B3, B4), calées sur la phrase dite. Les plans B2, B5a et B5b sont déjà faits en motion design.</li>
<li>Pour chaque plan : génère d'abord l'image, envoie-la-moi pour vérification, puis lance la vidéo avec cette image en input.</li>
<li>Style des 3D inspiré de Drew Canole (analyse de 6 de ses vidéos TikTok) : anatomie hyper réaliste et brillante isolée sur fond noir, plongées microscopiques dans le cuir chevelu, corps en hologramme, une transformation littérale par plan, caméra lente.</li><li>Comme chez lui, les mots-clés s’affichent au montage en grand au centre ; je les pose aux couleurs de Claire (Fraunces italique blanc, mot fort en terracotta).</li>
<li>Aucun texte dans les images : les étiquettes en français sont posées au montage, aux couleurs de Claire.</li>
<li>Si ton outil génère des vidéos plus longues que le plan (8 s par exemple), garde le prompt tel quel : je prendrai les bonnes secondes au montage.</li>
</ul></div>
{cards}
</main><script>
function cp(id,b){{const t=document.getElementById(id).innerText;const done=()=>{{b.textContent="Copié";b.classList.add("ok");setTimeout(()=>{{b.textContent="Copier";b.classList.remove("ok")}},1500)}};
if(navigator.clipboard){{navigator.clipboard.writeText(t).then(done,()=>fb(t,done))}}else fb(t,done)}}
function fb(t,done){{const a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{{document.execCommand("copy");done()}}catch(e){{}}a.remove()}}
</script></body></html>'''
pathlib.Path("/home/user/labo/runs/2026-10-23_claire-tempes-affinement_ugc-humain/brolls-a-generer.html").write_text(page)
print("ok")
