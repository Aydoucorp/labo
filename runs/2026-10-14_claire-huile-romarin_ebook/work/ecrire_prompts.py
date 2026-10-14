#!/usr/bin/env python3
"""Ebook 002 « huile de romarin » (reel Claire chhavi / créa full-b-roll-artiste 005) : contenu exact de chaque page
et prompts GPT Image 2 (skill ebook-full-value). Adapté de l'ebook 001 : aucun âge, tempes et ligne du front, calendrier
cohérent avec la vidéo (« la bonne dose », « utilisation régulière »), chevelure brune comme dans la vidéo.

Écrit `contenu.md` (textes des pages, lisible) et `prompts/pages/NN.txt` (un prompt autonome par page :
lock DA, verrous, contenu exact, rappel des verrous). Relancer après toute retouche de texte.
"""
import pathlib

RUN = pathlib.Path(__file__).resolve().parent.parent
N = 11  # nombre de pages

DA = """BOOK PAGE DESIGN, art direction locked (identical on every page of this 11-page ebook, as if made by the same hand):
- Format: portrait 3:4 digital book page, read on a phone. Generous margins, airy layout, clear hierarchy, large readable text.
- Background: warm cream #FAF6F3 on the whole page. Cards and separators: darker cream #EFE7E0 with softly rounded corners.
- Colors, exact hex only: terracotta #A8553A (titles, numbers, key accents), light terracotta #C9805F (badges, small flat shapes), plum #7A4351 (secondary accents, strong contrast), ink #2E2A26 (all body text). Silver #B4ADA4 and sage #8C9B86 are decorative only (leaves, thin lines) and never carry text.
- Lettering: titles in an elegant soft high-contrast serif with warm rounded details, terracotta or plum. Body text in a clean humanist sans-serif, ink color. The handwritten signature in a relaxed natural handwriting, terracotta. These are style instructions only, never written on the page.
- Brand mark: at the top center of every page except the cover, the small text "Les cheveux de Claire" in the title serif, terracotta, with a tiny sage rosemary sprig to its left. Strictly identical on every page.
- Page number: bottom center, small ink digit alone, no word, no brackets, no dash.
- Illustration style: soft flat vector illustration with a subtle paper grain, rounded shapes, gentle shadows, botanical details (rosemary sprigs in sage), amber glass dropper bottle, hands drawn simply. Whenever hair is drawn, it is always the same: long, thick, softly wavy dark brown hair with warm chocolate highlights, loose and natural (never a bun, never grey or white strands). Same treatment and palette on every page. No photography, no 3D.
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
- Big title, terracotta, on two lines: "Le rituel à l'huile de romarin"
- Under it, in plum, slightly smaller: "La bonne dose, les bons gestes, chaque jour"
- Subtitle, ink: "Ta méthode naturelle, pas à pas, pour aider tes cheveux à repousser"
- Three small pill badges in a row, darker cream with ink text: "100 % végétal" "10 minutes par jour" "Pas à pas"
- Central illustration: an amber glass dropper bottle lying among fresh rosemary sprigs, a few golden oil drops, two simple hands with oiled fingertips gently massaging the top of a head of long wavy dark brown hair seen from above (no face).
- Bottom, warm line in plum: "Offert avec le cœur par Les cheveux de Claire\""""},
 {"titre": "Le mot d'intro", "contenu": """Letter page. A large darker cream card with a tiny rosemary sprig in the corner.
- Title, terracotta: "Avant de commencer"
- Letter text, ink, in short paragraphs:
"Le jour où j'ai vu mes tempes se dégarnir et ma raie s'élargir dans le miroir, j'ai eu peur. J'avais tout essayé. Rien ne marchait."
"Puis j'ai découvert l'huile de romarin. Et surtout, la bonne façon de l'utiliser."
"Ce que j'ai compris : la différence ne vient pas de l'huile seule. Elle vient de la bonne dose, appliquée chaque jour, et massée là où elle compte : sur la peau."
"Dans ce guide, je te donne la méthode exacte, geste par geste, celle que j'aurais aimé avoir dès le premier jour."
"10 minutes par jour, des gestes simples et doux. Tu vas adorer ce rendez-vous avec toi-même."
"Je t'embrasse,"
- Handwritten signature, terracotta: "Claire\""""},
 {"titre": "Le reframe", "contenu": """Reframe page.
- Title, terracotta: "Respire, d'abord"
- Text, ink: "Perdre 50 à 100 cheveux par jour, c'est normal. Ils sont remplacés au fil du cycle du cheveu."
- Text, ink: "Stress, fatigue, changements hormonaux, alimentation : à tout moment de la vie, les cheveux peuvent tomber plus. Ils le montrent souvent avant nous."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Tes cheveux ont besoin de deux choses : la bonne dose, et de la régularité."
- Text under the card, ink: "Et la bonne nouvelle : tu peux commencer dès ce soir."
- Illustration: a calm rosemary sprig and a few fallen hairs drawn softly on the cream background."""},
 {"titre": "Pourquoi ça marche", "contenu": """Evidence page, three stacked darker cream cards, each with a small terracotta icon (bottle, hand, speech bubble).
- Title, terracotta: "Pourquoi ça marche"
- Card 1 title, plum: "L'huile de romarin"
  Card 1 text, ink: "100 personnes, 6 mois, 2 applications par jour : le romarin a fait aussi bien que le minoxidil 2 % sur le nombre de cheveux."
- Card 2 title, plum: "Le massage"
  Card 2 text, ink: "4 minutes de massage par jour pendant 24 semaines : des cheveux plus épais, mesurés au microscope."
- Card 3 title, plum: "Le ressenti des massages"
  Card 3 text, ink: "Sur 327 personnes qui massaient leur cuir chevelu, environ 7 sur 10 disent avoir vu leur chute se stabiliser."
- Bottom card in a light terracotta outlined box, ink text: "Le secret, c'est le duo : l'huile de romarin à la bonne dose, et le massage qui la fait pénétrer. Ensemble, ils forment ton rituel.\""""},
 {"titre": "La bonne dose", "contenu": """Recipe page.
- Title, terracotta: "La bonne dose : ton mélange maison"
- Intro, ink: "Pas besoin d'un produit compliqué : tu prépares toi-même ton mélange 100 % végétal."
- Section label, plum: "Il te faut"
- Three ingredient rows, each with a small flat illustration on the left:
  "Un flacon pipette en verre ambré de 10 mL"
  "Une huile végétale douce : jojoba ou amande douce"
  "De l'huile essentielle de romarin"
- Highlighted dosage card, terracotta background #A8553A with cream text, large: "1 goutte de romarin pour 10 mL d'huile au début. 2 gouttes au maximum."
- Section label, plum: "La préparation"
- Four numbered steps, terracotta numbers, ink text:
  "1. Verse l'huile végétale dans le flacon."
  "2. Ajoute la goutte d'huile essentielle."
  "3. Ferme et roule le flacon entre tes mains."
  "4. Note la date, range à l'abri de la lumière.\""""},
 {"titre": "Avant de commencer", "contenu": """Safety page, reassuring tone, two cards.
- Title, terracotta: "Les règles de sécurité"
- Card 1 title, plum: "Le test des 48 heures"
  Card 1 text, ink: "Dépose une goutte de ton mélange au pli du coude. Attends 48 heures. Rougeur ou démangeaison ? On n'utilise pas."
- Card 2 title, plum: "Pas d'huile essentielle si"
  Card 2 list, ink, each line with a small plum dot:
  "Tu es enceinte ou tu allaites"
  "Tu es épileptique"
  "Ton cuir chevelu est irrité ou abîmé"
- Line, ink: "Jamais pure sur la peau, jamais près des yeux. Ça pique ou ça brûle ? Tu rinces et tu arrêtes."
- Bottom card, plum background #7A4351 with cream text: "Chute brutale, par plaques, cuir chevelu douloureux ou grosse fatigue ? Parles-en à ton médecin. Un bilan sanguin (fer, thyroïde) peut tout changer."
- Small illustration: a hand with one drop on the inner elbow area, drawn simply."""},
 {"titre": "Le rituel", "contenu": """Step by step page, a vertical sequence of six steps with small flat illustrations (hair seen from above, dropper on a parting line, no face).
- Title, terracotta: "Ton rituel, en 10 minutes"
- Subtitle, plum: "Chaque jour, le soir de préférence"
- Steps, terracotta numbers in light terracotta circles, ink text:
  "1. Sur cheveux secs et démêlés, trace une raie."
  "2. Avec la pipette, dépose quelques gouttes au ras de la peau, le long de la raie."
  "3. Décale ta raie de 2 cm et recommence, sur tout le dessus de la tête."
  "4. N'oublie pas les tempes et la ligne du front : quelques gouttes, du bout des doigts."
  "5. Sans attendre, masse 5 minutes du bout des doigts huilés : c'est le massage qui fait pénétrer l'huile (page suivante)."
  "6. Laisse poser au moins 1 heure, ou toute la nuit avec une serviette sur l'oreiller."
- Tip card, darker cream, ink text: "Au lavage : shampoing doux, deux passages si besoin. Une demi-cuillère à café de mélange suffit pour toute la tête.\""""},
 {"titre": "Le massage qui fait pénétrer l'huile", "contenu": """Massage method page, a 2 by 3 grid feel: five small step cards plus one rule card. Each step card has a simple illustration of two hands with oiled fingertips on a head of hair seen from above or from behind (no face), a tiny golden oil drop near the parting.
- Title, terracotta: "Le massage qui fait pénétrer l'huile"
- Rule line under the title, plum: "Juste après avoir déposé l'huile. La pulpe des doigts, jamais les ongles. Tu fais bouger la peau, pas les cheveux."
- Step cards, terracotta minute label then ink text:
  "1 minute" "Petits cercles des tempes vers le sommet du crâne."
  "1 minute" "Appuie, relâche, en avançant de la nuque vers le front."
  "1 minute" "Pince doucement la peau entre tes doigts et étire."
  "1 minute" "Petits cercles sur la raie, les tempes et le front."
  "1 minute" "Mains en griffe, remonte de la nuque vers le haut."
- Rule card, terracotta background #A8553A with cream text: "Ferme mais jamais douloureux. 5 minutes, chaque fois que tu mets l'huile.\""""},
 {"titre": "Ton calendrier", "contenu": """Timeline page, a vertical timeline with four milestones in terracotta, connected by a thin sage line.
- Title, terracotta: "Ton calendrier, semaine après semaine"
- Intro, ink: "Ta clé, c'est la régularité : le rituel complet, huile et massage, chaque jour."
- Milestone 1 title, plum: "Jour 1"
  text, ink: "Test du pli du coude, puis photo de ta raie, de tes tempes et de ton front, même lumière, même endroit. Ton point de départ."
- Milestone 2 title, plum: "Semaines 2 à 4"
  text, ink: "Le rituel devient une habitude. Garde un œil sur ta brosse et sur ton oreiller. Continue, chaque jour compte."
- Milestone 3 title, plum: "Mois 2 et 3"
  text, ink: "Compare avec ta photo du jour 1, en regardant de près tes tempes et ta ligne du front."
- Milestone 4 title, plum: "Mois 6"
  text, ink: "Compare tes photos et regarde le chemin parcouru."
- Bottom card, darker cream, ink text: "Un cheveu pousse d'environ 1 cm par mois. Utilisation régulière, différence visible.\""""},
 {"titre": "Le mémo", "contenu": """Memo page, four darker cream cards in a 2 by 2 grid, each with a small terracotta icon and a plum card title.
- Title, terracotta: "Le mémo à garder"
- Card 1 title: "La bonne dose" text, ink: "1 à 2 gouttes de romarin pour 10 mL d'huile. Jamais pure."
- Card 2 title: "Les bons gestes" text, ink: "L'huile sur la raie, les tempes et le front, puis 5 minutes de massage."
- Card 3 title: "La régularité" text, ink: "Le rituel complet chaque jour. La peau bouge, pas les cheveux."
- Card 4 title: "La patience" text, ink: "Une photo par mois pour voir le chemin parcouru.\""""},
 {"titre": "À toi de jouer", "contenu": """Closing page, warm and encouraging.
- Title, terracotta: "À toi de jouer"
- Text, ink: "Pas besoin d'attendre le bon moment. Le bon moment, c'est ce soir."
- Highlighted card, terracotta background #A8553A with cream text, label then action:
  "Ce soir"
  "Prépare ton flacon et fais le test du pli du coude. Dans 48 heures, ton premier rituel complet, huile et massage."
- Text, ink: "Ton cuir chevelu va adorer ce moment. Et toi aussi."
- Signature line in plum serif italic: "Tes cheveux ont changé. Toi aussi."
- Bottom, small ink text: "Retrouve-moi sur Instagram @les_cheveux_de_claire"
- Illustration: two hands holding an amber dropper bottle with rosemary sprigs, soft and warm."""},
]
assert len(PAGES) == N

md = ["# Contenu de l'ebook 002 « Le rituel à l'huile de romarin »\n",
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
