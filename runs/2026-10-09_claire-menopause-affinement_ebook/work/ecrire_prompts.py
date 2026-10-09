#!/usr/bin/env python3
"""Ebook « Comment traiter l'affinement des cheveux à la ménopause » : contenu exact et prompts GPT Image 2 (skill ebook-full-value).

Offert aux commentatrices « GUIDE » du talking head n°2 (runs/2026-10-08_claire-menopause-affinement_talking-head).
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
- Illustration style: soft flat vector illustration with a subtle paper grain, rounded shapes, gentle shadows, botanical details (rosemary sprigs in sage), amber glass dropper bottle, hands drawn simply. Whenever hair is drawn, it is always the same: wavy salt-and-pepper hair, dark brown base with irregular white strands, loose and natural (never a bun, never uniform brown). Same treatment and palette on every page. No photography, no 3D.
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
- Big title, terracotta, on three lines: "Comment traiter l'affinement des cheveux à la ménopause"
- Under it, in plum, slightly smaller: "Ta méthode en 3 gestes, pas à pas"
- Subtitle, ink: "Des cheveux plus forts et un cuir chevelu plein de vie, à partir de ce soir"
- Three small pill badges in a row, darker cream with ink text: "Naturel" "3 gestes" "Pas à pas"
- Central illustration: a still life on the cream background: an amber glass dropper bottle among fresh rosemary sprigs, a glass of water with a small spoon of white powder beside it, a halved orange, and a small sheet of paper with a tiny drop icon (a blood test request, no readable text). Above them, the top of a head of wavy salt-and-pepper hair seen from above, with two simple hands gently massaging it (no face).
- Bottom, warm line in plum: "Offert avec le cœur par Les cheveux de Claire\""""},
 {"titre": "Le mot d'intro", "contenu": """Letter page. A large darker cream card with a tiny rosemary sprig in the corner.
- Title, terracotta: "Avant de commencer"
- Letter text, ink, in short paragraphs:
"Un matin, j'ai attaché mes cheveux et ma queue de cheval tenait dans ma main. Plus fine, plus légère. Personne ne m'avait prévenue que la ménopause passait aussi par là."
"Alors j'ai fait ce que je fais toujours : j'ai cherché. Et j'ai trouvé une méthode simple, en 3 gestes, qui agit sur ce qui se passe vraiment sous tes cheveux."
"Un geste pour comprendre ce dont ton corps a besoin. Un geste pour nourrir ton cuir chevelu de l'intérieur. Un geste pour réveiller tes racines chaque soir."
"Dans ce guide, je te donne tout : quoi faire, combien, quand, et dans quel ordre."
"Tu vas voir, c'est plus simple que tu ne le crois. Et ça change tout."
"Je t'embrasse,"
- Handwritten signature, terracotta: "Claire\""""},
 {"titre": "Ce qui se passe", "contenu": """Explanation page, calm and reassuring.
- Title, terracotta: "Ce qui se passe sous tes cheveux"
- Text, ink: "Tu es loin d'être la seule : plus d'une femme sur deux voit ses cheveux s'affiner autour de 50 ans."
- Three small darker cream cards stacked, each with a small terracotta icon (a falling leaf, a shrinking circle, a thin layer):
  Card 1 title, plum: "Les œstrogènes baissent" text, ink: "Tes cheveux quittent plus tôt leur phase de pousse."
  Card 2 title, plum: "Les androgènes prennent plus de place" text, ink: "Ils font rétrécir peu à peu les racines, et le cheveu pousse plus fin."
  Card 3 title, plum: "Le collagène diminue" text, ink: "Ton cuir chevelu s'amincit et soutient moins bien tes racines."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Tes cheveux ont changé. Toi aussi. Ce n'est pas un problème à régler, c'est une nouvelle façon de faire.\""""},
 {"titre": "La méthode", "contenu": """Overview page, three large numbered steps stacked vertically, each in a darker cream card with a big terracotta number and a small flat illustration on the right.
- Title, terracotta: "Ta méthode en 3 gestes"
- Text, ink: "Chaque geste répond à une des causes. Ensemble, ils couvrent tout."
- Step 1, number "1", title plum: "Vérifie ce qui se cache dans ton sang" text, ink: "Une prise de sang, une fois, pour corriger ce qui freine tes cheveux." Illustration: a small sheet with a drop icon, no readable text.
- Step 2, number "2", title plum: "Nourris ton cuir chevelu de l'intérieur" text, ink: "Du collagène, chaque jour, dans ta boisson du matin." Illustration: a glass with a spoon of white powder.
- Step 3, number "3", title plum: "Réveille tes racines chaque soir" text, ink: "5 minutes de massage avec ton huile au romarin." Illustration: an amber dropper bottle and a rosemary sprig.
- Bottom line, terracotta serif: "3 gestes. Quelques minutes par jour. Et tes cheveux te disent merci.\""""},
 {"titre": "Geste 1", "contenu": """Step page.
- Small badge, light terracotta #C9805F with cream text: "GESTE 1"
- Title, terracotta: "La prise de sang qui change tout"
- Text, ink: "Un manque de fer ou une thyroïde au ralenti peuvent faire tomber tes cheveux bien plus que la ménopause. Ce sont deux causes très fréquentes, et elles se corrigent."
- Section label, plum: "Comment faire"
- Four numbered steps, terracotta numbers, ink text:
  "1. Prends rendez-vous chez ton médecin traitant cette semaine."
  "2. Demande ton bilan avec la liste de la page suivante."
  "3. Fais ta prise de sang à jeun, le matin."
  "4. Si un résultat est bas, ton médecin te dit comment le remonter."
- Highlighted card, terracotta background #A8553A with cream text: "Ne prends pas de fer au hasard : ta prise de sang te dit exactement ce dont ton corps a besoin."
- Illustration: a small calendar page with a circled day and a tiny drop icon, no readable text."""},
 {"titre": "Bonus analyses", "contenu": """Bonus checklist page, designed to be shown to the doctor.
- Small badge, light terracotta #C9805F with cream text: "BONUS"
- Title, terracotta: "Ta liste à montrer au médecin"
- Five checklist rows in a darker cream card, each with an empty terracotta checkbox, the test name in plum and a short ink explanation:
  "NFS" "Pour vérifier qu'il n'y a pas d'anémie."
  "Ferritine" "Tes réserves de fer, la plus importante pour tes cheveux."
  "TSH" "Pour savoir si ta thyroïde fonctionne bien."
  "Vitamine D" "Souvent basse, à vérifier."
  "Zinc" "Utile à la pousse du cheveu."
- Section label, plum: "La phrase à dire"
- Speech bubble card, plum background #7A4351 with cream text: "Mes cheveux s'affinent depuis la ménopause. Pouvez-vous me prescrire une NFS, une ferritine et une TSH, et si possible la vitamine D et le zinc ?"
- Small text, ink: "Garde tes résultats : ils sont ton point de départ.\""""},
 {"titre": "Geste 2", "contenu": """Step page.
- Small badge, light terracotta #C9805F with cream text: "GESTE 2"
- Title, terracotta: "Le collagène, ton allié du matin"
- Text, ink: "Ton cuir chevelu est une peau. Après la ménopause, il fabrique moins de collagène. Alors on lui en apporte, chaque jour."
- Highlighted card, terracotta background #A8553A with cream text, large: "Chez des femmes de 45 à 60 ans, 5 g de collagène par jour pendant 6 mois : nettement moins de cheveux perdus au coiffage."
- Section label, plum: "Ton mode d'emploi"
- Four rows with small terracotta icons, ink text:
  "Choisis du collagène hydrolysé en poudre, marin ou bovin."
  "Prends 5 g par jour, la dose indiquée sur ton pot."
  "Mélange-le à ton café, ton thé, ton yaourt ou un verre d'eau."
  "Ajoute un kiwi ou une orange dans ta journée : la vitamine C aide ton corps à fabriquer son collagène."
- Illustration: a mug and a small spoon of white powder, a halved kiwi and an orange."""},
 {"titre": "Geste 3, ton huile", "contenu": """Recipe page.
- Small badge, light terracotta #C9805F with cream text: "GESTE 3"
- Title, terracotta: "Ton huile du soir au romarin"
- Text, ink: "Après 6 mois d'huile de romarin, le nombre de cheveux augmente. Préparée comme ici, elle devient ton rituel."
- Section label, plum: "Il te faut"
- Three ingredient rows, each with a small flat illustration on the left:
  "Un flacon pipette en verre ambré de 10 mL"
  "Une huile végétale légère, comme le jojoba"
  "De l'huile essentielle de romarin à cinéole"
- Highlighted dosage card, terracotta background #A8553A with cream text, large: "1 goutte de romarin pour 10 mL d'huile au début. 2 gouttes au maximum."
- Section label, plum: "La préparation"
- Three numbered steps, terracotta numbers, ink text:
  "1. Verse l'huile végétale dans le flacon."
  "2. Ajoute la goutte d'huile essentielle et ferme."
  "3. Roule le flacon entre tes mains pour mélanger. Garde-le à l'abri de la lumière."
- Illustration: an amber dropper bottle, a small jojoba bottle without label and rosemary sprigs."""},
 {"titre": "Geste 3, le massage", "contenu": """Method page with a simple illustrated sequence.
- Title, terracotta: "Le massage de 5 minutes"
- Text, ink: "4 minutes de massage par jour pendant 24 semaines : des cheveux plus épais. Voici le geste, chaque soir."
- Five numbered steps in a vertical sequence, terracotta numbers, ink text, each with a tiny flat illustration of hands on the top of a head of wavy salt-and-pepper hair seen from above (no face):
  "1. Fais une raie et dépose 2 ou 3 gouttes d'huile directement sur la peau."
  "2. Recommence tous les 2 cm, sur tout le dessus de la tête."
  "3. Pose la pulpe de tes doigts sur ton cuir chevelu, sans les ongles."
  "4. Fais de petits cercles fermes : c'est la peau qui bouge, pas les cheveux."
  "5. Avance du front vers la nuque, puis sur les côtés, pendant 5 minutes."
- Highlighted card, plum background #7A4351 with cream text: "Laisse agir toute la nuit, et lave tes cheveux comme d'habitude le lendemain.\""""},
 {"titre": "Règles de sécurité", "contenu": """Safety page, calm and positive, a darker cream card with soft rounded corners.
- Title, terracotta: "Tes règles d'or"
- Text, ink: "Quelques réflexes simples pour profiter de ta méthode en toute sérénité."
- Six short rows, each with a small sage leaf bullet, ink text:
  "Fais un test dans le pli du coude 24 heures avant ton premier massage."
  "L'huile essentielle de romarin se dilue toujours, jamais pure sur la peau."
  "Pas de romarin en cas de grossesse, d'allaitement, d'épilepsie ou d'hypertension non stabilisée."
  "Allergique au poisson ? Choisis un collagène bovin."
  "Le fer ou la vitamine D se prennent après ta prise de sang, sur conseil de ton médecin."
  "Une chute brutale, des plaques ou un cuir chevelu douloureux : montre-le à ton médecin."
- Illustration: a small rosemary sprig and an amber bottle, soft and calm."""},
 {"titre": "Le mémo", "contenu": """Memo page, four darker cream cards in a 2 by 2 grid, each with a small terracotta icon and a plum card title.
- Title, terracotta: "Le mémo à garder"
- Card 1 title: "Une fois" text, ink: "Ta prise de sang : NFS, ferritine, TSH, vitamine D, zinc."
- Card 2 title: "Chaque matin" text, ink: "5 g de collagène dans ta boisson, et un fruit riche en vitamine C."
- Card 3 title: "Chaque soir" text, ink: "Ton huile au romarin sur la raie, puis 5 minutes de massage."
- Card 4 title: "Chaque mois" text, ink: "Une photo de ta raie, à la même lumière, pour voir tes progrès.\""""},
 {"titre": "À toi de jouer", "contenu": """Closing page, warm and encouraging, with a strong invitation to write.
- Title, terracotta: "À toi de jouer"
- Text, ink: "Le meilleur moment pour commencer, c'est aujourd'hui."
- Highlighted card, terracotta background #A8553A with cream text, label then action:
  "Aujourd'hui"
  "Prends rendez-vous pour ta prise de sang, et prépare ton flacon de romarin ce soir."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Et maintenant, écris-moi !"
- Text, ink: "Envoie-moi un message privé : dis-moi ce que tu as pensé du guide, pose-moi toutes tes questions, et raconte-moi ton premier soir de massage. Je lis tous tes messages et je te réponds."
- Signature line in plum serif italic: "Tes cheveux ont changé. Toi aussi."
- Bottom, small ink text: "Retrouve-moi sur Instagram @les_cheveux_de_claire"
- Illustration: a small envelope with a heart next to an amber dropper bottle and rosemary sprigs."""},
]
assert len(PAGES) == N

md = ["# Contenu de l'ebook « Comment traiter l'affinement des cheveux à la ménopause »\n",
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
