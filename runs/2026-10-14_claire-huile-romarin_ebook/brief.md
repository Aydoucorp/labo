# Brief : ebook 002 « Le rituel à l'huile de romarin » (ebook full value)

- Date : 2026-10-14
- Marque : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- Skill : `skills/ebook-full-value` (récupéré de la branche `claude/trusting-carson-sott4i`)
- Reel associé : `references/video-reel.mp4` = vidéo publiée par les_cheveux_de_claire, c'est la créa `creas/full-b-roll-artiste/2026-10-12_full-b-roll-artiste_005.mp4` (huile de romarin, run `runs/2026-10-12_claire-chhavi1351_decoupe/`), CTA « Commente GUIDE pour avoir le guide gratuitement ».
- Base : ebook 001 « Le rituel romarin et massage » (`runs/2026-10-03_claire-batana-chute-40-ans_ebook/` sur la branche `claude/trusting-carson-sott4i`, créa `creas/ebook/2026-10-03_ebook_001.pdf`), fait pour le reel batana « chute à 40 ans ».

## Ce que promet le reel (ce que la lectrice attend en commentant GUIDE)

« Mes cheveux avant ces shots d'huile de romarin » ; « J'avais tout essayé. Rien ne marchait » ; « Puis j'ai commencé à utiliser ces shots d'huile de romarin régulièrement » ; « Juste ce qu'il faut de romarin pour que ça marche » ; « 100 % d'origine végétale » ; « Chute de cheveux réduite en seulement 14 jours » ; « Mes cheveux repoussent enfin » (ligne frontale) ; « Résultats visibles en seulement 4 semaines » ; « Utilisation régulière = différence visible » ; « La bonne dose. De vrais résultats ».
Images : tempes et ligne du front dégarnies, huile déposée à la fiole sur la raie, repousse sur le front, cheveux longs bruns.

## Écart entre l'ebook 001 et le reel (analyse du 14/10)

| Point | Ebook 001 | Reel | Décision ebook 002 |
|---|---|---|---|
| Âge | « Vers 40 ans, les hormones bougent » (p. 3), chevelure poivre et sel dessinée | Femme sans âge affiché, cheveux bruns | Aucun âge (demande utilisateur : « on ne veut pas spécifier l'âge ») ; causes listées sans âge ; chevelure dessinée longue brune ondulée |
| Zone | Raie et dessus de la tête | Tempes et ligne du front | Étape « tempes et ligne du front » ajoutée (p. 7), massage et mémo idem (p. 8, 10), photos de suivi des tempes et du front (p. 9) |
| Délais | Mois 2-3 « un peu plus de cheveux sur la brosse, c'est normal », rendez-vous à 6 mois | 14 jours, 4 semaines | Calendrier Jour 1 / Semaines 2 à 4 / Mois 2 et 3 / Mois 6, sans phase de chute annoncée, sans promesse chiffrée inventée ; clôture « Utilisation régulière, différence visible » (mots du reel) |
| Vocabulaire | « Deux gestes qui ne vont pas l'un sans l'autre » | « La bonne dose », « utilisation régulière », « 100 % végétal » | Repris en titres, badges et mémo (couverture, p. 3, 5, 10) |
| Produit | Mélange maison, batana citée | Fioles prêtes à l'emploi (marque masquée) | Mélange maison gardé, phrase « Pas besoin d'un produit compliqué » ; batana retirée (huiles de base : jojoba ou amande douce) |
| Massage | Cœur du rituel | Absent | Gardé (bonus, sourcé) |

Mots interdits de la Brand DNA respectés (pas de « stopper la chute », « miracle », « retrouver tes cheveux d'avant »). Écart assumé avec la Brand DNA : chevelure dessinée brune et non poivre et sel, pour coller au reel et ne donner aucun âge.

## Sources (inchangées depuis l'ebook 001, hors de l'ebook)

| Point | Ce qu'on retient | Source |
|---|---|---|
| Huile de romarin | Essai randomisé, 100 personnes, 6 mois, 2 applications par jour : hausse du nombre de cheveux, sans différence avec le minoxidil 2 %. | Panahi et coll., Skinmed 2015;13(1):15-21 |
| Massage | 4 min par jour, 24 semaines : cheveux plus épais (0,085 à 0,092 mm). | Koyama et coll., Eplasty 2016 |
| Massage, ressenti | 327 personnes, environ 7 sur 10 disent une stabilisation ou une repousse (autodéclaré). | English et Barazesh, Dermatol Ther 2019 |
| Sécurité | Dilution prudente (environ 1 %), test cutané, pas d'huile essentielle enceinte, allaitante, épileptique, cuir chevelu lésé. | Synthèses de sécurité aromathérapie ; ANSM |
| Chute normale, pousse | 50 à 100 cheveux par jour ; environ 1 cm par mois. | American Academy of Dermatology |
| Causes sans âge | Stress, maladie, régime (effluvium télogène), carence en fer, thyroïde, variations hormonales. | PMC7394174, PMC10766245, PMC12839778 |

## Contenu et prompts

- Textes exacts : `contenu.md`. Prompts : `prompts/pages/01.txt` à `11.txt`, générés par `work/ecrire_prompts.py` (copie du script de l'ebook 001, textes modifiés ; même lock DA sauf la chevelure).
- Pages modifiées par rapport au 001 : 1 (titre, sous-titres, badges), 2 (tempes, « J'avais tout essayé », bonne dose), 3 (âge retiré, carte « la bonne dose et la régularité »), 4 (titre « Pourquoi ça marche », carte duo), 5 (titre « La bonne dose », intro, batana retirée), 7 (6 étapes avec tempes et front, « chaque jour »), 8 (cercles sur raie, tempes et front), 9 (nouveau calendrier), 10 (cartes bonne dose, bons gestes, régularité), 11 inchangée sauf DA. Page 6 (sécurité) inchangée. Toutes les pages sont à regénérer (chevelure dessinée changée).

## Génération (à faire)

GPT Image 2 via KIE, 3:4, 11 pages. Coût selon la résolution choisie par l'utilisateur : 1K 6 cr par page (66 cr), 2K 10 cr (110 cr), 4K 16 cr (176 cr). L'ebook 001 avait été fait en 1K.

Commande par page : `python3 scripts/kie_image.py --model gpt-image-2-text-to-image --prompt-file prompts/pages/NN.txt --out sorties/pages/NN-v1.png --ratio 3:4 --resolution 1K`

Bloqué au 14/10 : clé `KIE_API_KEY` absente de cette session. Contrôle après génération selon le skill (texte exact, accents, pas de signature parasite, taille 1086x1448, chevelure identique sur toutes les pages), puis PDF web et HQ, créa `creas/ebook/AAAA-MM-JJ_ebook_002.pdf` (+ `-hq.pdf`).
