#!/usr/bin/env python3
"""Ebook « Les 3 produits qui transforment tes cheveux » : contenu exact et prompts GPT Image 2 (skill ebook-full-value).

Offert aux commentatrices « CHEVEUX » de la vidéo « Les 3 produits indispensables pour transformer tes cheveux ».
DA verrouillée reprise du 1er ebook (runs/2026-10-03_claire-batana-chute-40-ans_ebook).
Écrit `contenu.md` et `prompts/pages/NN.txt`. Relancer après toute retouche de texte.
"""
import pathlib

RUN = pathlib.Path(__file__).resolve().parent.parent
N = 12  # nombre de pages

DA = """BOOK PAGE DESIGN, art direction locked (identical on every page of this 12-page ebook, as if made by the same hand):
- Format: portrait 3:4 digital book page, read on a phone. Generous margins, airy layout, clear hierarchy, large readable text.
- Background: warm cream #FAF6F3 on the whole page. Cards and separators: darker cream #EFE7E0 with softly rounded corners.
- Colors, exact hex only: terracotta #A8553A (titles, numbers, key accents), light terracotta #C9805F (badges, small flat shapes), plum #7A4351 (secondary accents, strong contrast), ink #2E2A26 (all body text). Silver #B4ADA4 and sage #8C9B86 are decorative only (leaves, thin lines) and never carry text.
- Lettering: titles in an elegant soft high-contrast serif with warm rounded details, terracotta or plum. Body text in a clean humanist sans-serif, ink color. The handwritten signature in a relaxed natural handwriting, terracotta. These are style instructions only, never written on the page.
- Brand mark: at the top center of every page except the cover, the small text "Les cheveux de Claire" in the title serif, terracotta, with a tiny sage rosemary sprig to its left. Strictly identical on every page.
- Page number: bottom center, small ink digit alone, no word, no brackets, no dash.
- Illustration style: soft flat vector illustration with a subtle paper grain, rounded shapes, gentle shadows, botanical details (small sage leaves and sprigs), plain unlabeled bottles and jars (a tall shampoo bottle, a wide cream jar, an amber glass dropper bottle), hands drawn simply. Whenever hair is drawn, it is always the same: wavy salt-and-pepper hair, dark brown base with irregular white strands, loose and natural (never a bun, never uniform brown). Same treatment and palette on every page. No photography, no 3D.
- Mood: warm, calm, reassuring, a friend who looked into it. Never clinical, never an advertising look."""

LOCKS = """STRICT RULES:
1. All text is in French with correct accents. Do not translate any word. Copy every quoted text exactly, character for character.
2. Show ONLY the quoted texts listed below. Add no other text, slogan, tip, badge, label or watermark.
3. Show no organizational element: no page number in brackets, no technical title, no section label, no layout note.
4. Never write the name of a font.
5. Draw no human face, no head, no person seen from the front. Hands and the top of a head of hair seen from above are allowed.
6. Show the brand name exactly "Les cheveux de Claire" and the signature exactly "Claire", never translated, shortened or altered.
7. No third-party commercial brand, no logo on bottles (plain amber bottles, plain labels).
8. No invented number or price: only the numbers written in the quoted texts.
9. No em dash, no en dash, no visible slash, no markdown symbol (no hash, no asterisk).
10. The handwritten signature "Claire" appears only where it is listed in the page content, nowhere else."""

PAGES = [
 {"titre": "Couverture", "num": False, "contenu": """Cover layout, no brand mark at the top and no page number.
- Top: small rounded badge in light terracotta #C9805F with cream text: "LE GUIDE OFFERT"
- Big title, terracotta, on two lines: "Les 3 produits qui transforment tes cheveux"
- Under it, in plum, slightly smaller: "Et la routine exacte pour les utiliser"
- Subtitle, ink: "Des cheveux légers, nourris et brillants, semaine après semaine"
- Three small pill badges in a row, darker cream with ink text: "3 produits" "Pas à pas" "Tous types de cheveux"
- Central illustration: three plain unlabeled hair products standing side by side on the cream background, a tall clear shampoo bottle, a wide cream-colored mask jar with its lid beside it, an amber glass dropper bottle of oil, with small sage leaves around them; above them, the top of a head of wavy salt-and-pepper hair seen from above, glossy and full (no face).
- Bottom, warm line in plum: "Offert avec le cœur par Les cheveux de Claire\""""},
 {"titre": "Le mot d'intro", "contenu": """Letter page. A large darker cream card with a tiny sage sprig in the corner.
- Title, terracotta: "Avant de commencer"
- Letter text, ink, in short paragraphs:
"Pendant des années, ma salle de bain débordait de flacons. Et mes cheveux restaient ternes, secs au bout et plats à la racine."
"Le jour où j'ai compris, tout a changé : ce n'est pas le nombre de produits qui compte. Ce sont les 3 bons, utilisés dans le bon ordre, au bon rythme."
"Un produit pour remettre ton cuir chevelu à zéro. Un produit pour nourrir tes longueurs. Un produit pour protéger tes cheveux avant chaque lavage."
"Dans ce guide, je te donne tout : comment les choisir, combien en mettre, combien de temps, et ton planning de la semaine selon tes cheveux."
"Tu vas voir la différence dès les premiers lavages."
"Je t'embrasse,"
- Handwritten signature, terracotta: "Claire\""""},
 {"titre": "Le reframe", "contenu": """Explanation page, calm and reassuring.
- Title, terracotta: "Pourquoi tes cheveux manquent d'éclat"
- Three small darker cream cards stacked, each with a small terracotta icon (a water drop, a thin layer, a split end):
  Card 1 title, plum: "Un film invisible" text, ink: "Calcaire de l'eau, restes de produits et sébum s'accumulent. Tes cheveux deviennent lourds et ternes."
  Card 2 title, plum: "Des longueurs assoiffées" text, ink: "Avec les années, les lavages et la chaleur, les pointes perdent leur protection et cassent plus vite."
  Card 3 title, plum: "Un cuir chevelu oublié" text, ink: "C'est là que tes cheveux poussent. Il mérite autant d'attention que tes longueurs."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Tes cheveux n'ont pas besoin de plus de produits. Ils ont besoin des bons, au bon moment.\""""},
 {"titre": "La routine", "contenu": """Overview page, three large numbered steps stacked vertically, each in a darker cream card with a big terracotta number and a small flat illustration on the right.
- Title, terracotta: "Ta routine en 3 gestes"
- Text, ink: "Le jour du soin, toujours dans cet ordre :"
- Step 1, number "1", title plum: "Le masque à l'huile" text, ink: "Avant le shampoing, sur cheveux secs, pour protéger et nourrir." Illustration: an amber dropper bottle and a drop of golden oil.
- Step 2, number "2", title plum: "Le shampoing clarifiant" text, ink: "Il remet ton cuir chevelu à zéro et emporte l'huile et les résidus." Illustration: a tall clear shampoo bottle with a little foam.
- Step 3, number "3", title plum: "Le masque nourrissant" text, ink: "Sur les longueurs, pour hydrater et réparer." Illustration: a wide cream jar with a scoop of cream.
- Bottom line, terracotta serif: "Les autres jours, ton shampoing doux habituel suffit.\""""},
 {"titre": "Produit 1, le choisir", "contenu": """Product page.
- Small badge, light terracotta #C9805F with cream text: "PRODUIT 1"
- Title, terracotta: "Le shampoing clarifiant"
- Text, ink: "C'est le grand nettoyage : il enlève ce qu'un shampoing doux laisse derrière lui."
- Two side-by-side darker cream cards:
  Left card title, plum: "À chercher" with three rows, small sage check icons, ink text:
  "Un shampoing dit clarifiant ou purifiant"
  "Si ton eau est calcaire : EDTA, acide citrique ou acide phytique dans la liste"
  "Une texture limpide, souvent transparente"
  Right card title, plum: "À éviter" with three rows, small terracotta cross icons, ink text:
  "Les silicones (mots en -cone ou -siloxane)"
  "Les formules crème ou 2 en 1"
  "Les huiles lourdes dans la formule"
- Highlighted card, terracotta background #A8553A with cream text: "Un clarifiant ne nourrit pas : il nettoie. C'est pour ça qu'il va toujours avec le masque."
- Illustration: a tall clear shampoo bottle with no label and a little foam."""},
 {"titre": "Produit 1, l'utiliser", "contenu": """Method page.
- Small badge, light terracotta #C9805F with cream text: "PRODUIT 1"
- Title, terracotta: "Ton lavage clarifiant"
- Five numbered steps, terracotta numbers, ink text, each with a tiny flat illustration of hands and wavy salt-and-pepper hair seen from above (no face):
  "1. Mouille longuement tes cheveux à l'eau tiède."
  "2. Une noisette dans la paume, émulsionne avec un peu d'eau."
  "3. Applique sur le cuir chevelu seulement et masse 1 minute du bout des doigts."
  "4. Laisse la mousse glisser sur les longueurs en rinçant, sans frotter."
  "5. Rince bien, puis passe directement au masque nourrissant."
- Highlighted card, plum background #7A4351 with cream text: "Cheveux colorés ? Attends 2 semaines après ta coloration avant ton premier clarifiant.\""""},
 {"titre": "Produit 2", "contenu": """Product page.
- Small badge, light terracotta #C9805F with cream text: "PRODUIT 2"
- Title, terracotta: "Le masque nourrissant"
- Text, ink: "Il redonne à tes longueurs ce que le temps et les lavages leur ont pris."
- Section label, plum: "Les bons ingrédients"
- Four rows with small sage leaf bullets, ink text:
  "Céramides : elles réparent la protection du cheveu"
  "Alcools gras (cétylique, cétéarylique) : de bons alcools qui adoucissent"
  "Panthénol et glycérine : ils hydratent"
  "Beurres et huiles végétales : ils nourrissent les pointes"
- Section label, plum: "Ton mode d'emploi"
- Four numbered steps, terracotta numbers, ink text:
  "1. Essore tes cheveux dans une serviette."
  "2. Une noix de masque sur les mi-longueurs et les pointes, jamais sur les racines."
  "3. Démêle avec les doigts ou un peigne à dents larges, laisse poser 10 minutes."
  "4. Rince à l'eau tiède, puis fraîche pour la brillance."
- Illustration: a wide cream-colored jar with no label and a soft scoop of cream."""},
 {"titre": "Produit 3", "contenu": """Product page.
- Small badge, light terracotta #C9805F with cream text: "PRODUIT 3"
- Title, terracotta: "Le masque à l'huile"
- Highlighted card, terracotta background #A8553A with cream text, large: "Appliquée avant le shampoing, l'huile de coco limite la perte de protéines de tes cheveux au lavage."
- Two side-by-side darker cream cards:
  Left card title, plum: "Sur les longueurs" text, ink: "L'huile de coco vierge, chauffée entre tes mains. 1 à 2 cuillères à soupe selon la longueur."
  Right card title, plum: "Sur le cuir chevelu" text, ink: "Quelques gouttes d'une huile légère, comme l'huile de coco fractionnée, raie par raie."
- Section label, plum: "Ton mode d'emploi"
- Three numbered steps, terracotta numbers, ink text:
  "1. Sur cheveux secs, applique l'huile des longueurs aux pointes, puis quelques gouttes sur le cuir chevelu."
  "2. Masse ton cuir chevelu 2 à 3 minutes du bout des doigts."
  "3. Laisse poser de 30 minutes à 1 heure, puis lave avec ton shampoing."
- Illustration: an amber glass dropper bottle, a small open jar of white coconut oil and a halved coconut, no labels."""},
 {"titre": "Planning de la semaine", "contenu": """Planner page: a clean table in a darker cream card, three columns with plum headers, rows with terracotta row labels, ink text, thin sage separators.
- Title, terracotta: "Ton planning selon tes cheveux"
- Column headers, plum: "Fins ou gras" "Normaux" "Secs, colorés ou blancs"
- Row label "Masque à l'huile": "1 fois toutes les 2 semaines, longueurs seulement" "1 fois par semaine" "1 à 2 fois par semaine"
- Row label "Shampoing clarifiant": "1 fois par semaine" "1 fois toutes les 2 semaines" "1 fois toutes les 3 à 4 semaines"
- Row label "Masque nourrissant": "1 fois par semaine, texture légère" "1 à 2 fois par semaine" "2 fois par semaine"
- Text under the table, ink: "Les autres jours : ton shampoing doux habituel et un après-shampoing sur les longueurs."
- Highlighted card, plum background #7A4351 with cream text: "Le jour du clarifiant, enchaîne les 3 gestes : huile, clarifiant, masque.\""""},
 {"titre": "Règles d'or", "contenu": """Safety page, calm and positive, a darker cream card with soft rounded corners.
- Title, terracotta: "Tes règles d'or"
- Text, ink: "Quelques réflexes simples pour profiter de ta routine en toute sérénité."
- Six short rows, each with a small sage leaf bullet, ink text:
  "Nouveau produit ? Teste-le 24 heures avant dans le pli du coude."
  "Jamais plus d'un clarifiant par semaine : il nettoie fort."
  "Toujours un masque après le clarifiant."
  "Pellicules ou cuir chevelu qui gratte : l'huile reste sur les longueurs."
  "Eau tiède pour laver, jamais brûlante."
  "Une chute brutale ou un cuir chevelu douloureux : montre-le à ton médecin."
- Illustration: a small sage sprig and an amber dropper bottle, soft and calm."""},
 {"titre": "Le mémo", "contenu": """Memo page, four darker cream cards in a 2 by 2 grid, each with a small terracotta icon and a plum card title.
- Title, terracotta: "Le mémo à garder"
- Card 1 title: "L'ordre" text, ink: "Huile, puis clarifiant, puis masque."
- Card 2 title: "Le clarifiant" text, ink: "Sur le cuir chevelu seulement, jamais plus d'une fois par semaine."
- Card 3 title: "Le masque" text, ink: "Mi-longueurs et pointes, 10 minutes, rinçage frais."
- Card 4 title: "L'huile" text, ink: "Sur cheveux secs, 30 minutes à 1 heure avant le lavage.\""""},
 {"titre": "À toi de jouer", "contenu": """Closing page, warm and encouraging, with a strong invitation to write.
- Title, terracotta: "À toi de jouer"
- Text, ink: "Ta prochaine journée de lavage peut déjà tout changer."
- Highlighted card, terracotta background #A8553A with cream text, label then action:
  "Cette semaine"
  "Repère ton type de cheveux dans le planning et fais ton premier soin complet : huile, clarifiant, masque."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Et maintenant, écris-moi !"
- Text, ink: "Envoie-moi un message privé : dis-moi ce que tu as pensé du guide, pose-moi toutes tes questions, et raconte-moi ton premier soin complet. Je lis tous tes messages et je te réponds."
- Signature line in plum serif italic: "Tes cheveux ont changé. Toi aussi."
- Bottom, small ink text: "Retrouve-moi sur Instagram @les_cheveux_de_claire"
- Illustration: a small envelope with a heart next to the three plain products (shampoo bottle, cream jar, amber dropper bottle)."""},
]
assert len(PAGES) == N

md = ["# Contenu de l'ebook « Les 3 produits qui transforment tes cheveux »\n",
      "Généré par `work/ecrire_prompts.py`. Textes exacts de chaque page (ce qui sera affiché).\n"]
for i, p in enumerate(PAGES, 1):
    num = "" if p.get("num") is False else f"\nPage number at the bottom center: \"{i}\""
    if i != 2:  # la signature manuscrite n'existe que sur le mot d'intro
        num += "\nNo handwritten signature anywhere on this page: the word \"Claire\" appears only inside the brand name."
    prompt = (f"{DA}\n\n{LOCKS}\n\nPAGE CONTENT ({p['titre']}):\n{p['contenu']}{num}\n\n"
              f"FINAL REMINDER, apply strictly:\n{LOCKS}\nSame art direction, colors, lettering, brand mark position and page number position as every other page of the book.")
    for c in "—–":
        assert c not in prompt, (i, c)
    (RUN / "prompts" / "pages" / f"{i:02d}.txt").write_text(prompt + "\n")
    md.append(f"## Page {i} : {p['titre']}\n")
    md += [l.strip() for l in p["contenu"].splitlines() if '"' in l]
    md.append("")
(RUN / "contenu.md").write_text("\n".join(md) + "\n")
print(f"{N} prompts écrits dans prompts/pages, contenu.md à jour")
