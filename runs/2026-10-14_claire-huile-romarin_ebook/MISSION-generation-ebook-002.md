# Mission : génère maintenant l'ebook 002 « Le rituel à l'huile de romarin » (Les cheveux de Claire)

**Consigne directe de l'utilisateur : génère l'ebook complet tout de suite, les 11 pages, en GPT Image 2 via KIE, format 3:4, résolution 1K (comme l'ebook 001), avec les textes ci-dessous recopiés tels quels. La résolution et les textes sont déjà validés : ne redemande rien, ne fais pas de pages d'essai, lance la génération dès la lecture de ce fichier.** Coût prévu : 11 pages x 6 crédits = 66 crédits (plus les éventuelles relances de pages défectueuses).

Avec ce fichier, l'utilisateur fournit l'ebook 001 (`2026-10-03_ebook_001.pdf`) : c'est la référence visuelle à égaler (mise en page, couleurs, typo, cartes, brand mark).

## Contexte

- Dépôt : `Aydoucorp/labo`. Tout le travail préparatoire est sur la branche `claude/loving-ride-tq5w1n`, dossier `runs/2026-10-14_claire-huile-romarin_ebook/` (brief.md, contenu.md, prompts/pages/01.txt à 11.txt, work/ecrire_prompts.py, references/video-reel.mp4). Si la session est sur une autre branche, récupérer ce dossier avec `git fetch origin claude/loving-ride-tq5w1n && git checkout origin/claude/loving-ride-tq5w1n -- runs/2026-10-14_claire-huile-romarin_ebook scripts/kie_image.py skills/ebook-full-value`.
- Skill à suivre : `skills/ebook-full-value/SKILL.md` (étapes 5 et 6, et la section « Contrôle après génération »).
- Ebook 002 = adaptation de l'ebook 001 (« Le rituel romarin et massage », fait pour le reel batana « chute à 40 ans ») au reel huile de romarin de Claire (créa `full-b-roll-artiste_005`, CTA « Commente GUIDE pour avoir le guide gratuitement »).
- Demandes de l'utilisateur : ne donner AUCUN âge, et que chaque page colle à la vidéo (la bonne dose, utilisation régulière, 100 % végétal, tempes et ligne du front, repousse). Les textes ci-dessous sont déjà validés dans cet esprit : les recopier tels quels.
- L'ebook 001 sert de référence de mise en page et de style (mêmes couleurs, typo, cartes, brand mark, numéro de page). Seule différence voulue : la chevelure dessinée est longue, brune et ondulée (plus de poivre et sel, pour ne suggérer aucun âge).

## Règles à respecter

1. Résolution : 1K, déjà choisie par l'utilisateur pour cette mission. Ne pas la redemander.
2. Pas de pages d'essai : générer les 11 pages d'affilée, dans l'ordre, puis faire le contrôle ci-dessous et relancer seulement les pages défectueuses. Montrer ensuite toutes les pages à l'utilisateur (SendUserFile, planche + PDF).
3. Ne jamais afficher la clé API. Noter chaque génération (taskId, crédits, fichier) dans le `brief.md` du run.
4. Commit et push après chaque étape.

## Génération

Pour chaque page NN (01 à 11), le prompt complet est dans `prompts/pages/NN.txt` (sinon l'assembler comme décrit plus bas) :

```
python3 scripts/kie_image.py --model gpt-image-2-text-to-image --prompt-file runs/2026-10-14_claire-huile-romarin_ebook/prompts/pages/NN.txt \
  --out runs/2026-10-14_claire-huile-romarin_ebook/sorties/pages/NN-v1.png --ratio 3:4 --resolution 1K
```

Assemblage d'un prompt si les fichiers ne sont pas disponibles : `DA` + ligne vide + `VERROUS` + ligne vide + `PAGE CONTENT (titre):` + contenu de la page + ligne du numéro de page (sauf couverture) + ligne « No handwritten signature » (sauf page 2) + ligne vide + `FINAL REMINDER, apply strictly:` + `VERROUS` + « Same art direction, colors, lettering, brand mark position and page number position as every other page of the book. »

## Contrôle après génération (obligatoire)

- Texte exact, accents corrects, aucune coquille ajoutée (ex. « complètte », « 1. cm »), aucun texte en plus.
- Pas de signature « Claire » manuscrite ailleurs qu'en page 2.
- Aucun âge visible, aucune mention « 40 ans », aucune chevelure grise ou poivre et sel : cheveux longs bruns ondulés partout, identiques d'une page à l'autre.
- Taille attendue en 1K : 1086x1448. Une sortie en 880x1184 (typo plus fine) est à relancer.
- Planche de toutes les pages côte à côte : elles doivent former un livre homogène, comme l'ebook 001.
- Relancer en v2, v3… les pages défectueuses seulement.

## Après validation des 11 pages

- Copier les versions retenues dans `retenues/pages/NN.png`.
- Assembler deux PDF, comme pour l'ebook 001 : `retenues/rituel-huile-romarin-web.pdf` (pages à 800 px de large, environ 1 Mo, pour l'envoi en message privé) et `retenues/rituel-huile-romarin-hq.pdf` (pleine résolution, JPEG qualité 93, page 150 x 200 mm).
- Créa finale : `creas/ebook/AAAA-MM-JJ_ebook_002.pdf` (version web) et `AAAA-MM-JJ_ebook_002-hq.pdf`. Lire `creas/registre.md` (concept `ebook`, dernier numéro 001) et le mettre à jour (compteur 002 + ligne d'historique : « Claire · rituel à l'huile de romarin, ebook offert du reel huile de romarin (créa full-b-roll-artiste 005, CTA « GUIDE »), sans âge »).
- Drive « Studio marketing » : dossier `creas/ebook` (ID `1FSOfuqxTlrpVsry0UU0rpiqX_A5BLIjx`), créer le dossier du run dans `runs` (ID `1C65QZGUKzNdwrqqUnPiX7Fg_d9Cp06oX`) avec `brief.md` et `contenu.md`, remplacer `registre.md` dans `creas` (ID `1FDZFVjSxYWmDJMos5vFhK_lw85pCLDQ2`), ajouter l'ID du nouveau dossier au tableau de `CLAUDE.md`. Les PDF sont envoyés à l'utilisateur (SendUserFile) s'il n'y a pas de clés Drive.
- Envoyer les deux PDF à l'utilisateur.

## Direction artistique verrouillée (DA, en tête de chaque prompt)

```
BOOK PAGE DESIGN, art direction locked (identical on every page of this 11-page ebook, as if made by the same hand):
- Format: portrait 3:4 digital book page, read on a phone. Generous margins, airy layout, clear hierarchy, large readable text.
- Background: warm cream #FAF6F3 on the whole page. Cards and separators: darker cream #EFE7E0 with softly rounded corners.
- Colors, exact hex only: terracotta #A8553A (titles, numbers, key accents), light terracotta #C9805F (badges, small flat shapes), plum #7A4351 (secondary accents, strong contrast), ink #2E2A26 (all body text). Silver #B4ADA4 and sage #8C9B86 are decorative only (leaves, thin lines) and never carry text.
- Lettering: titles in an elegant soft high-contrast serif with warm rounded details, terracotta or plum. Body text in a clean humanist sans-serif, ink color. The handwritten signature in a relaxed natural handwriting, terracotta. These are style instructions only, never written on the page.
- Brand mark: at the top center of every page except the cover, the small text "Les cheveux de Claire" in the title serif, terracotta, with a tiny sage rosemary sprig to its left. Strictly identical on every page.
- Page number: bottom center, small ink digit alone, no word, no brackets, no dash.
- Illustration style: soft flat vector illustration with a subtle paper grain, rounded shapes, gentle shadows, botanical details (rosemary sprigs in sage), amber glass dropper bottle, hands drawn simply. Whenever hair is drawn, it is always the same: long, thick, softly wavy dark brown hair with warm chocolate highlights, loose and natural (never a bun, never grey or white strands). Same treatment and palette on every page. No photography, no 3D.
- Mood: warm, calm, reassuring, a friend who looked into it. Never clinical, never an advertising look.
```

## Verrous (après la DA, et répétés en rappel final de chaque prompt)

```
STRICT RULES:
1. All text is in French with correct accents. Do not translate any word. Copy every quoted text exactly, character for character.
2. Show ONLY the quoted texts listed below. Add no other text, slogan, tip, badge, label or watermark.
3. Show no organizational element: no page number in brackets, no technical title, no section label, no layout note.
4. Never write the name of a font.
5. Draw no human face, no head, no person seen from the front. Hands and the top of a head of hair seen from above are allowed.
6. Show the brand name exactly "Les cheveux de Claire" and the signature exactly "Claire", never translated, shortened or altered.
7. No third-party commercial brand, no logo on bottles (plain amber bottles, plain labels).
8. No invented number or price: only the numbers written in the quoted texts.
9. No em dash, no en dash, no visible slash, no markdown symbol (no hash, no asterisk).
10. The handwritten signature "Claire" appears only where it is listed in the page content, nowhere else.
```

## Contenu exact des 11 pages (PAGE CONTENT de chaque prompt)

### Page 1 : Couverture

```
PAGE CONTENT (Couverture):
Cover layout, no brand mark at the top and no page number.
- Top: small rounded badge in light terracotta #C9805F with cream text: "LE GUIDE OFFERT"
- Big title, terracotta, on two lines: "Le rituel à l'huile de romarin"
- Under it, in plum, slightly smaller: "La bonne dose, les bons gestes, chaque jour"
- Subtitle, ink: "Ta méthode naturelle, pas à pas, pour aider tes cheveux à repousser"
- Three small pill badges in a row, darker cream with ink text: "100 % végétal" "10 minutes par jour" "Pas à pas"
- Central illustration: an amber glass dropper bottle lying among fresh rosemary sprigs, a few golden oil drops, two simple hands with oiled fingertips gently massaging the top of a head of long wavy dark brown hair seen from above (no face).
- Bottom, warm line in plum: "Offert avec le cœur par Les cheveux de Claire"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 2 : Le mot d'intro

```
PAGE CONTENT (Le mot d'intro):
Letter page. A large darker cream card with a tiny rosemary sprig in the corner.
- Title, terracotta: "Avant de commencer"
- Letter text, ink, in short paragraphs:
"Le jour où j'ai vu mes tempes se dégarnir et ma raie s'élargir dans le miroir, j'ai eu peur. J'avais tout essayé. Rien ne marchait."
"Puis j'ai découvert l'huile de romarin. Et surtout, la bonne façon de l'utiliser."
"Ce que j'ai compris : la différence ne vient pas de l'huile seule. Elle vient de la bonne dose, appliquée chaque jour, et massée là où elle compte : sur la peau."
"Dans ce guide, je te donne la méthode exacte, geste par geste, celle que j'aurais aimé avoir dès le premier jour."
"10 minutes par jour, des gestes simples et doux. Tu vas adorer ce rendez-vous avec toi-même."
"Je t'embrasse,"
- Handwritten signature, terracotta: "Claire"
Page number at the bottom center: "2"
```

### Page 3 : Le reframe

```
PAGE CONTENT (Le reframe):
Reframe page.
- Title, terracotta: "Respire, d'abord"
- Text, ink: "Perdre 50 à 100 cheveux par jour, c'est normal. Ils sont remplacés au fil du cycle du cheveu."
- Text, ink: "Stress, fatigue, changements hormonaux, alimentation : à tout moment de la vie, les cheveux peuvent tomber plus. Ils le montrent souvent avant nous."
- Highlighted card, plum background #7A4351 with cream text, large serif: "Tes cheveux ont besoin de deux choses : la bonne dose, et de la régularité."
- Text under the card, ink: "Et la bonne nouvelle : tu peux commencer dès ce soir."
- Illustration: a calm rosemary sprig and a few fallen hairs drawn softly on the cream background.
Page number at the bottom center: "3"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 4 : Pourquoi ça marche

```
PAGE CONTENT (Pourquoi ça marche):
Evidence page, three stacked darker cream cards, each with a small terracotta icon (bottle, hand, speech bubble).
- Title, terracotta: "Pourquoi ça marche"
- Card 1 title, plum: "L'huile de romarin"
  Card 1 text, ink: "100 personnes, 6 mois, 2 applications par jour : le romarin a fait aussi bien que le minoxidil 2 % sur le nombre de cheveux."
- Card 2 title, plum: "Le massage"
  Card 2 text, ink: "4 minutes de massage par jour pendant 24 semaines : des cheveux plus épais, mesurés au microscope."
- Card 3 title, plum: "Le ressenti des massages"
  Card 3 text, ink: "Sur 327 personnes qui massaient leur cuir chevelu, environ 7 sur 10 disent avoir vu leur chute se stabiliser."
- Bottom card in a light terracotta outlined box, ink text: "Le secret, c'est le duo : l'huile de romarin à la bonne dose, et le massage qui la fait pénétrer. Ensemble, ils forment ton rituel."
Page number at the bottom center: "4"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 5 : La bonne dose

```
PAGE CONTENT (La bonne dose):
Recipe page.
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
  "4. Note la date, range à l'abri de la lumière."
Page number at the bottom center: "5"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 6 : Avant de commencer

```
PAGE CONTENT (Avant de commencer):
Safety page, reassuring tone, two cards.
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
- Small illustration: a hand with one drop on the inner elbow area, drawn simply.
Page number at the bottom center: "6"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 7 : Le rituel

```
PAGE CONTENT (Le rituel):
Step by step page, a vertical sequence of six steps with small flat illustrations (hair seen from above, dropper on a parting line, no face).
- Title, terracotta: "Ton rituel, en 10 minutes"
- Subtitle, plum: "Chaque jour, le soir de préférence"
- Steps, terracotta numbers in light terracotta circles, ink text:
  "1. Sur cheveux secs et démêlés, trace une raie."
  "2. Avec la pipette, dépose quelques gouttes au ras de la peau, le long de la raie."
  "3. Décale ta raie de 2 cm et recommence, sur tout le dessus de la tête."
  "4. N'oublie pas les tempes et la ligne du front : quelques gouttes, du bout des doigts."
  "5. Sans attendre, masse 5 minutes du bout des doigts huilés : c'est le massage qui fait pénétrer l'huile (page suivante)."
  "6. Laisse poser au moins 1 heure, ou toute la nuit avec une serviette sur l'oreiller."
- Tip card, darker cream, ink text: "Au lavage : shampoing doux, deux passages si besoin. Une demi-cuillère à café de mélange suffit pour toute la tête."
Page number at the bottom center: "7"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 8 : Le massage qui fait pénétrer l'huile

```
PAGE CONTENT (Le massage qui fait pénétrer l'huile):
Massage method page, a 2 by 3 grid feel: five small step cards plus one rule card. Each step card has a simple illustration of two hands with oiled fingertips on a head of hair seen from above or from behind (no face), a tiny golden oil drop near the parting.
- Title, terracotta: "Le massage qui fait pénétrer l'huile"
- Rule line under the title, plum: "Juste après avoir déposé l'huile. La pulpe des doigts, jamais les ongles. Tu fais bouger la peau, pas les cheveux."
- Step cards, terracotta minute label then ink text:
  "1 minute" "Petits cercles des tempes vers le sommet du crâne."
  "1 minute" "Appuie, relâche, en avançant de la nuque vers le front."
  "1 minute" "Pince doucement la peau entre tes doigts et étire."
  "1 minute" "Petits cercles sur la raie, les tempes et le front."
  "1 minute" "Mains en griffe, remonte de la nuque vers le haut."
- Rule card, terracotta background #A8553A with cream text: "Ferme mais jamais douloureux. 5 minutes, chaque fois que tu mets l'huile."
Page number at the bottom center: "8"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 9 : Ton calendrier

```
PAGE CONTENT (Ton calendrier):
Timeline page, a vertical timeline with four milestones in terracotta, connected by a thin sage line.
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
- Bottom card, darker cream, ink text: "Un cheveu pousse d'environ 1 cm par mois. Utilisation régulière, différence visible."
Page number at the bottom center: "9"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 10 : Le mémo

```
PAGE CONTENT (Le mémo):
Memo page, four darker cream cards in a 2 by 2 grid, each with a small terracotta icon and a plum card title.
- Title, terracotta: "Le mémo à garder"
- Card 1 title: "La bonne dose" text, ink: "1 à 2 gouttes de romarin pour 10 mL d'huile. Jamais pure."
- Card 2 title: "Les bons gestes" text, ink: "L'huile sur la raie, les tempes et le front, puis 5 minutes de massage."
- Card 3 title: "La régularité" text, ink: "Le rituel complet chaque jour. La peau bouge, pas les cheveux."
- Card 4 title: "La patience" text, ink: "Une photo par mois pour voir le chemin parcouru."
Page number at the bottom center: "10"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```

### Page 11 : À toi de jouer

```
PAGE CONTENT (À toi de jouer):
Closing page, warm and encouraging.
- Title, terracotta: "À toi de jouer"
- Text, ink: "Pas besoin d'attendre le bon moment. Le bon moment, c'est ce soir."
- Highlighted card, terracotta background #A8553A with cream text, label then action:
  "Ce soir"
  "Prépare ton flacon et fais le test du pli du coude. Dans 48 heures, ton premier rituel complet, huile et massage."
- Text, ink: "Ton cuir chevelu va adorer ce moment. Et toi aussi."
- Signature line in plum serif italic: "Tes cheveux ont changé. Toi aussi."
- Bottom, small ink text: "Retrouve-moi sur Instagram @les_cheveux_de_claire"
- Illustration: two hands holding an amber dropper bottle with rosemary sprigs, soft and warm.
Page number at the bottom center: "11"
No handwritten signature anywhere on this page: the word "Claire" appears only inside the brand name.
```
