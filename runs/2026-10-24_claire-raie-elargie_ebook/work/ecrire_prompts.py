#!/usr/bin/env python3
"""Ebook « raie élargie » (offert aux commentatrices GUIDE de la vidéo UGC humain du 2026-10-22) : contenu exact de chaque page
et prompts GPT Image 2 (skill ebook-full-value). Même DA que les ebooks 001 et 002 de Claire. Sources dans brief.md.

Écrit `contenu.md` et `prompts/pages/NN.txt` (lock DA, verrous, contenu exact, rappel des verrous). Relancer après toute retouche.
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
- Illustration style: soft flat vector illustration with a subtle paper grain, rounded shapes, gentle shadows, botanical details (rosemary sprigs in sage), amber glass dropper bottle, simple hands, hair and scalp seen from above, simple cross-sections of hair growing from the skin. Whenever hair is drawn, it is always the same: long, thick, softly wavy dark brown hair with warm chocolate highlights, loose and natural (never a bun, never grey or white strands). Same treatment and palette on every page. No photography, no 3D.
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
- Big title, terracotta, on two lines: "Ta raie s'élargit ?"
- Under it, in plum, slightly smaller: "Le plan pour soutenir tes follicules"
- Subtitle, ink: "Des gestes simples et concrets, à commencer dès ce soir"
- Three small pill badges in a row, darker cream with ink text: "Naturel" "10 minutes par jour" "Pas à pas"
- Central illustration: the top of a head of long wavy dark brown hair seen from above with a centre parting, two simple hands gently massaging the scalp along the parting with their fingertips, a small amber dropper bottle and fresh rosemary sprigs beside it (no face).
- Bottom, warm line in plum: "Offert avec le cœur par Les cheveux de Claire\""""},
 {"titre": "Le mot d'intro", "contenu": """Letter page. A large darker cream card with a tiny rosemary sprig in the corner.
- Title, terracotta: "Avant de commencer"
- Letter text, ink, in short paragraphs:
"Tu l'as remarqué un matin, dans le miroir : ta raie paraît plus large qu'avant. Et depuis, tu ne vois plus qu'elle."
"Je connais ce moment. Personne ne m'avait prévenue que mes cheveux allaient changer comme ça."
"Alors j'ai cherché, j'ai lu, j'ai trié. Et j'ai compris une chose : ta raie ne s'élargit pas parce que tu perds tout d'un coup. Elle s'élargit parce que tes cheveux s'affinent, doucement."
"Un cheveu qui s'affine, ça se soutient. Avec des gestes simples, chaque jour."
"Dans ce guide, je te donne mon plan complet, pilier par pilier. Tout ce que j'aurais aimé savoir dès le premier jour."
"Je t'embrasse,"
- Handwritten signature, terracotta: "Claire\""""},
 {"titre": "Le reframe", "contenu": """Reframe page.
- Title, terracotta: "Ce n'est pas une chute"
- Text, ink: "Quand la raie s'élargit, les cheveux ne tombent pas en masse. À chaque cycle de pousse, ils repoussent un peu plus fins et un peu plus courts. On appelle ça la miniaturisation."
- Text, ink: "C'est la forme de perte de densité la plus fréquente chez les femmes, surtout quand les hormones changent, à la quarantaine et à la ménopause."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Sous un cheveu qui s'affine, le follicule est toujours là. Ton plan : le soutenir, chaque jour."
- Text under the card, ink: "Ton plan tient en 4 piliers : apaiser, masser, nourrir, protéger."
- Illustration: a simple flat cross-section of the skin with three hairs side by side, from a thick hair to a finer one to a very fine one, each growing from its follicle."""},
 {"titre": "Pilier 1 : apaiser", "contenu": """Tips page, four rows each with a small terracotta icon on the left (drop of water, bottle, fingertips, shower), then one highlighted card.
- Title, terracotta: "Pilier 1 : apaiser ton cuir chevelu"
- Intro, ink: "Un cuir chevelu calme, c'est le meilleur terrain pour tes follicules."
- Rows, ink:
  "Lave tes cheveux aussi souvent que tu en as besoin : un lavage fréquent ne les abîme pas."
  "Le shampoing sur le cuir chevelu, l'après-shampoing seulement sur les longueurs."
  "Eau tiède, pulpe des doigts, petits cercles. Jamais les ongles."
  "Rince longtemps, jusqu'à ce que l'eau coule claire."
- Highlighted card, terracotta background #A8553A with cream text: "Pellicules ou démangeaisons ? Un shampoing antipelliculaire au kétoconazole, 2 fois par semaine, laissé poser 3 à 5 minutes.\""""},
 {"titre": "Pilier 2 : masser", "contenu": """Massage method page. A fact card at the top, then four small step cards in a 2 by 2 grid, each with a simple illustration of two hands with fingertips on a head of long wavy dark brown hair seen from above (no face), then a bonus card.
- Title, terracotta: "Pilier 2 : masser chaque jour"
- Fact card, darker cream, plum text: "4 minutes de massage par jour pendant 24 semaines : des cheveux plus épais."
- Step cards, terracotta minute label then ink text:
  "1 minute" "Petits cercles des tempes vers le sommet du crâne."
  "1 minute" "Appuie, relâche, de la nuque vers le front."
  "1 minute" "Pince doucement la peau et étire-la."
  "1 minute" "Petits cercles tout le long de ta raie."
- Rule line, plum: "La pulpe des doigts, jamais les ongles. La peau bouge, pas les cheveux."
- Bonus card, light terracotta outline, ink text: "Le bonus : 1 goutte d'huile essentielle de romarin dans 10 mL d'huile végétale, sur la raie, avant le massage. Sur 6 mois, le romarin a fait aussi bien que le minoxidil 2 % sur le nombre de cheveux.\""""},
 {"titre": "Pilier 3 : nourrir", "contenu": """Nutrition page, three darker cream cards with small flat food illustrations (eggs, lentils, fish, spinach, an orange), then one plum card.
- Title, terracotta: "Pilier 3 : nourrir de l'intérieur"
- Intro, ink: "Tes cheveux sont faits de kératine, une protéine. Pour pousser, ils ont besoin de matière première."
- Card 1 title, plum: "Des protéines à chaque repas"
  text, ink: "Œufs, poisson, volaille, yaourt, lentilles, pois chiches."
- Card 2 title, plum: "Du fer, bien absorbé"
  text, ink: "Lentilles, viande rouge, épinards, avec un fruit riche en vitamine C dans le même repas."
- Card 3 title, plum: "Un bilan chez ton médecin"
  text, ink: "Demande à doser ta ferritine et ta vitamine D. Chez les femmes qui perdent leurs cheveux, la ferritine est souvent plus basse."
- Plum card #7A4351 with cream text: "Le piège : les gélules de biotine n'aident pas tes cheveux si tu n'en manques pas. Ton assiette passe d'abord.\""""},
 {"titre": "Pilier 4 : protéger", "contenu": """Tips page, four rows each with a small terracotta icon on the left (soft scrunchie, wide tooth comb, hair dryer, flat iron), then one card.
- Title, terracotta: "Pilier 4 : protéger chaque cheveu"
- Intro, ink: "Des cheveux qui s'affinent sont plus fragiles. Chaque geste doux compte."
- Rows, ink:
  "Des coiffures souples : attache bas et lâche. Les queues de cheval et chignons serrés tirent sur les racines."
  "Un peigne à dents larges, des pointes vers les racines, sur cheveux démêlés."
  "Sèche-cheveux en température douce, ou séchage à l'air libre."
  "Fer à lisser et boucleur : rarement, et jamais sur cheveux mouillés."
- Card, darker cream, plum text: "Moins de tension, moins de chaleur : tes cheveux fins te diront merci.\""""},
 {"titre": "Du volume dès aujourd'hui", "contenu": """Styling tips page, four illustrated steps (hair seen from above or from behind, long wavy dark brown hair, no face), then a card.
- Title, terracotta: "Du volume dès aujourd'hui"
- Intro, ink: "Pendant que tes follicules travaillent, quelques astuces de coiffure donnent tout de suite plus de densité à ta raie."
- Steps, terracotta numbers, ink text:
  "1. Change ta raie de côté, ou trace-la en zigzag : les cheveux se soulèvent à la racine."
  "2. Sèche tête en bas, puis finis à l'air froid pour fixer le volume."
  "3. Un spray texturisant sur les racines plutôt qu'une crème lourde."
  "4. Une coupe avec des dégradés légers donne plus de corps qu'une longueur toute droite."
- Card, light terracotta outline, ink text: "L'astuce en plus : une poudre teintée de la couleur de tes racines, posée au pinceau le long de la raie.\""""},
 {"titre": "Les règles de sécurité", "contenu": """Safety page, reassuring tone, two cards and one plum card.
- Title, terracotta: "Les règles de sécurité"
- Card 1 title, plum: "Pour le romarin"
  text, ink: "Toujours dilué, jamais pur. Test au pli du coude 48 heures avant. Pas d'huile essentielle si tu es enceinte, si tu allaites ou si tu es épileptique."
- Card 2 title, plum: "Quand voir un dermatologue"
  text, ink: "Chute brutale ou par plaques, cuir chevelu rouge ou douloureux, fortes démangeaisons : prends rendez-vous."
- Plum card #7A4351 with cream text: "Il pourra poser un vrai diagnostic, demander un bilan sanguin (fer, thyroïde, vitamine D) et te proposer un traitement validé, comme le minoxidil en lotion.\""""},
 {"titre": "Ton calendrier", "contenu": """Timeline page, a vertical timeline with five milestones in terracotta, connected by a thin sage line.
- Title, terracotta: "Ton calendrier"
- Milestone 1 title, plum: "Jour 1"
  text, ink: "Photo de ta raie vue du dessus, même lumière, même endroit. C'est ton point de départ."
- Milestone 2 title, plum: "Chaque jour"
  text, ink: "4 minutes de massage, gestes doux, coiffures souples."
- Milestone 3 title, plum: "Chaque semaine"
  text, ink: "2 shampoings au kétoconazole si ton cuir chevelu gratte. Protéines et fer au menu."
- Milestone 4 title, plum: "Mois 3"
  text, ink: "Compare avec ta photo du jour 1."
- Milestone 5 title, plum: "Mois 6"
  text, ink: "Le vrai rendez-vous : c'est là qu'on regarde le chemin parcouru."
- Bottom card, darker cream, ink text: "Un cheveu pousse d'environ 1 cm par mois. La régularité fait tout.\""""},
 {"titre": "Le mémo", "contenu": """Memo page, four darker cream cards in a 2 by 2 grid, each with a small terracotta icon and a plum card title.
- Title, terracotta: "Le mémo à garder"
- Card 1 title: "Apaiser" text, ink: "Shampoing sur la peau, eau tiède, kétoconazole si ça gratte."
- Card 2 title: "Masser" text, ink: "4 minutes par jour. La peau bouge, pas les cheveux."
- Card 3 title: "Nourrir" text, ink: "Protéines, fer, et un bilan ferritine et vitamine D."
- Card 4 title: "Protéger" text, ink: "Coiffures souples, peigne large, chaleur douce.\""""},
 {"titre": "À toi de jouer", "contenu": """Closing page, warm and encouraging.
- Title, terracotta: "À toi de jouer"
- Text, ink: "Pas besoin d'attendre le bon moment. Le bon moment, c'est ce soir."
- Highlighted card, terracotta background #A8553A with cream text, label then action:
  "Ce soir"
  "Prends la photo de ta raie, puis offre-toi tes 4 premières minutes de massage."
- Text, ink: "Tes follicules vont adorer ce rendez-vous. Et toi aussi."
- Signature line in plum serif italic: "Tes cheveux ont changé. Toi aussi."
- Bottom, small ink text: "Retrouve-moi sur Instagram @les_cheveux_de_claire"
- Illustration: two hands resting gently on a head of long wavy dark brown hair seen from above, a rosemary sprig beside it, soft and warm."""},
]
assert len(PAGES) == N

md = ["# Contenu de l'ebook « Ta raie s'élargit ? »\n",
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
