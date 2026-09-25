# Génère storyboard.md et prompts.md à partir des plans calés sur la voix off mesurée.
STYLE = """Handmade paper-cut collage / scrapbook / ransom-note aesthetic. Aged cream paper background (#FAF6F3 warm cream) with visible grain and subtle creases. Every element is a separate piece of TORN paper with rough deckled white edges and a soft realistic drop shadow, layered like a physical collage, each piece slightly tilted 2-5 degrees. Headline in a huge bold condensed sans-serif (Anton / Archivo Black feel) in warm black ink (#2E2A26) with distressed grunge ink texture, cut out like newspaper letters. Hand-drawn black marker elements: imperfect arrows, underlines, small 3-stroke impact marks. Painted watercolour splatter accents. Color story: cream paper base, terracotta (#A8553A) for problem/myth, sage green (#8C9B86) for the answer/resolution, plum (#7A4351) for strong contrast accents, warm black textured ink for type. Sage and silver-grey never carry text. Vertical 9:16, high contrast, ONE big claim per frame, photoreal cut-out photos detoured onto the paper. Cut-out hair photos: real hair of a woman around 45, irregular white strands on a dark brown base (salt and pepper), hand-styled waves, soft window light, natural smartphone photo look, never salon blow-dry, never uniform silver, never studio lighting, never a shampoo-ad look. NOT clean, NOT flat vector, NOT a digital slide — it must look physically cut and glued by hand."""

PLANS = [
 # id, debut, fin, phrase VO exacte (voix mesurée), titre, sous-texte, visuel, feutre, peinture, couleur, mouvement, produit
 ("P01",0.00,2.15,"Tes cheveux sont en train de tomber par touffes…","ÇA TOMBE",None,
  "cut-out photo of a wooden hairbrush holding a clump of salt-and-pepper hair, a few loose wavy hairs cut out and scattered on the paper",
  "3-stroke impact marks around the brush","small terracotta splatter","terracotta",
  "loose hair cut-outs drop onto the paper one by one in stepped stop-motion, headline letters land with a small jolt","non"),
 ("P02",2.15,4.20,"Et tu as peur de te retrouver avec des trous ?","DES TROUS ?",None,
  "cut-out top-down smartphone photo of a salt-and-pepper hair parting, next to a torn hole in the cream paper showing darker paper beneath",
  "marker circle around the torn hole","terracotta wash at the hole edge","terracotta",
  "the torn hole opens slightly wider in two stepped poses, question mark wobbles once","non"),
 ("P03",4.20,7.24,"Certaines personnes, et même certaines coiffeuses,","MÊME LES COIFFEUSES",None,
  "cut-out photo of a hairdresser's hands holding a comb and scissors (no face), two empty torn-paper speech bubbles",
  "marker underline under the headline","plum dots","terracotta",
  "speech bubbles pop in one after the other, hands shift a few millimetres","non"),
 ("P04",7.24,10.61,"te diront que si tes cheveux tombent, la coupe courte est une évidence.","COUPE COURTE",None,
  "large open scissors cut-out and a cut-off lock of wavy salt-and-pepper hair",
  "marker arrow pointing down at the lock","terracotta splatter","terracotta",
  "scissors close in two stepped poses, the lock slides down a few millimetres","non"),
 ("P05",10.61,13.84,"Parce qu'en coupant, ce qui repousse revient plus épais.","PLUS ÉPAIS ?","« on dit »",
  "paper strands of hair cut from brown and grey paper growing upward in steps, between big hand-drawn quotation marks",
  "hand-drawn quotation marks and a question mark","terracotta splatter","terracotta",
  "paper strands grow upward in three stepped poses","non"),
 ("P06",13.84,15.59,"Les dermatologues sont formels :","FAUX",None,
  "the torn « PLUS ÉPAIS ? » scrap from the previous plan, partly covered by a large rubber-stamp imprint",
  "none","plum ink stamp texture","plum",
  "the stamp FAUX slams down once with a small paper shake","non"),
 ("P07",15.59,20.53,"Couper ne change ni la quantité, ni l'épaisseur, ni la vitesse de repousse.","QUANTITÉ · ÉPAISSEUR · VITESSE",None,
  "three torn paper labels stacked vertically, a small scissors cut-out on the side crossed out with marker",
  "marker X on the scissors, a marker equals sign after each label","plum splatter","plum",
  "labels appear one by one on each « ni » (17.32 s, 18.32 s, 19.54 s)","non"),
 ("P08",20.53,23.39,"Tout ce qui fonctionne s'applique sur le cuir chevelu.","CUIR CHEVELU",None,
  "cut-out photo of fingertips gently parting salt-and-pepper hair to show the scalp, soft window light",
  "marker arrow pointing to the scalp","sage green splatter","sage",
  "fingertip cut-out moves slightly along the parting in two poses","non"),
 ("P09",23.39,26.46,"Ton problème se traite à la RACINE, pas aux ciseaux.","RACINE","pas aux ciseaux",
  "simple hand-drawn marker sketch of a hair strand with its root under a paper scalp line, small scissors cut-out on the side",
  "marker X crossing the scissors on « pas aux ciseaux » (25.80 s)","sage green wash around the root","sage",
  "root sketch gets a marker underline, then the X is drawn over the scissors","non"),
 ("P10",26.46,29.30,"Commente GUIDE et je t'envoie gratuitement","COMMENTE GUIDE","gratuit",
  "large torn-paper comment bubble, the word GUIDE in cut-out letters on a terracotta paper band",
  "marker arrow pointing down (towards the comments)","terracotta and sage dots","terracotta",
  "comment bubble pops in, arrow bounces twice","non"),
 ("P11",29.30,31.72,"mes recettes à appliquer sur ton cuir chevelu.","MES RECETTES",None,
  "torn-paper booklet cover (cream with a terracotta band) showing the word GUIDE, a blank recipe card cut-out tucked behind it",
  "marker underline under the headline","sage splatter","sage",
  "booklet slides in and settles, recipe card peeks out, hold on the final frame","oui (couverture provisoire, pas de vraie couverture fournie)"),
]

def texts(p):
    t = [p[4]] + ([p[5]] if p[5] else [])
    if p[0]=="P06": t=["FAUX","PLUS ÉPAIS ?"]
    if p[0] in ("P10","P11"): t = t + (["GUIDE"] if p[0]=="P11" else [])
    return t

sb = ["# Storyboard · Claire · Guide racine · Paper Cut","",
      "Durées **mesurées** sur `audio/voix-off-finale.m4a` (31,72 s) par transcription horodatée mot à mot. Coupes placées dans les respirations entre deux mots.","",
      "| Plan | Début | Fin | Durée | Phrase VO (script) | Titre exact | Sous-texte | Visuel découpé | Feutre | Peinture | Couleur | Mouvement | Produit | Bruitage | Statut |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
pr = ["# Prompts par plan · Claire · Guide racine","",
      "Bloc de style commun (signature du module, adapté à la palette du brand DNA de Claire) copié en tête de chaque prompt image.","",
      "Moteurs visés : image Nano Banana 2 ou équivalent, animation Omni ou équivalent. **Rien n'a encore été généré.**",""]
for p in PLANS:
    pid,a,b,vo,title,sub,vis,marker,paint,col,move,prod = p
    d=b-a
    sb.append(f"| {pid} | {a:.2f} | {b:.2f} | {d:.2f} s | {vo} | {title} | {sub or '—'} | {vis} | {marker} | {paint} | {col} | {move} | {prod} | froissement / pose de papier | à générer |")
    allowed = ", ".join(f'"{x}"' for x in texts(p))
    img = f"""{STYLE}
References actually attached and their roles: {"none (the guide has no real cover yet: temporary torn-paper booklet)" if pid=="P11" else "none"}.
This is ONE flat paper collage image in 9:16.
Elements actually present: {vis}; headline "{title}"{f'; small handwritten note "{sub}"' if sub else ''}.
Setting and scale: flat tabletop collage seen from directly above, human-hand scale paper pieces, 3 to 4 layers.
Camera and eyeline: locked top-down view, collage filling the frame, safe margins for phone UI top and bottom.
Initial state BEFORE the action: {"hair pieces not yet fallen, only the brush and headline" if pid=="P01" else "all layers in place, ready for the stepped movement"}.
Light and functional palette: soft even daylight on paper, dominant {col}.
Product: {"temporary booklet cover with the word GUIDE, no other text on it" if pid=="P11" else "none"}.
Text inside the scene: ONLY {allowed}, spelled exactly with French accents. No other letters, no fake calendar, no micro-text, no logo.
Marker: {marker}. Paint: {paint}.
Preserve torn edges, drop shadows and the slight 2-5 degree tilt of each piece."""
    ani = f"""Use the approved starting image {pid}.
Animate the EXACT attached flat paper collage with stepped stop-motion paper movement: {move}. Preserve torn edges, letters, cut-out photos and every layer. Locked camera or very slow push. No morphing, no redraw, no 3D extrusion, letters must stay perfectly stable and identical.
Duration requested: {d:.2f} s measured on the final voice-over (generate at the engine's nearest allowed duration above it, trim in the edit).
Audio: paper rustle and paper placement sounds only, synced with each movement. No voice, no narration, no music.
Keep material, colours and scale consistent."""
    pr += [f"## {pid} · {a:.2f} → {b:.2f} s · {title}","",f"VO : « {vo} »","","### Image","","```text",img,"```","","### Animation","","```text",ani,"```",""]
open("storyboard.md","w").write("\n".join(sb)+"\n")
open("prompts.md","w").write("\n".join(pr))
print("total", sum(p[2]-p[1] for p in PLANS))
