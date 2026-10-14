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

## Génération (2026-10-14)

GPT Image 2 (`gpt-image-2-text-to-image`) via KIE, 3:4, 1K, 11 pages d'affilée, prompts `prompts/pages/NN.txt` sans modification.

| Page | Version | Tâche KIE | Coût | Fichier | Statut |
|---|---|---|---|---|---|
| 01 | v1 | c9adf49b479f7fa268c5596b09e66719 | 6 cr | `sorties/pages/01-v1.png` | retenue |
| 02 | v1 | 27ca9f31c6aac272b81bc6c8ad9c26ea | 6 cr | `sorties/pages/02-v1.png` | retenue |
| 03 | v1 | f2cfe27ab195c03e9acdfa73ef24079f | 6 cr | `sorties/pages/03-v1.png` | retenue |
| 04 | v1 | 97481186f3d802ab99faf1338d2bbf0f | 6 cr | `sorties/pages/04-v1.png` | retenue |
| 05 | v1 | 04392ccb80920e341e567fcec3f27ea0 | 6 cr | `sorties/pages/05-v1.png` | retenue |
| 06 | v1 | 5c38d5655cad73f01630abaf4eec1472 | 6 cr | `sorties/pages/06-v1.png` | retenue |
| 07 | v1 | 20e2c98cd7bce2d0b93658d3612c2f6f | 6 cr | `sorties/pages/07-v1.png` | retenue |
| 08 | v1 | 22db746f228d6274078382ac00a473c7 | 6 cr | `sorties/pages/08-v1.png` | retenue |
| 09 | v1 | 99d218f06feb38268b633917fff9f881 | 6 cr | `sorties/pages/09-v1.png` | retenue |
| 10 | v1 | fa90d7ad8e01691fc493b9c243101b93 | 6 cr | `sorties/pages/10-v1.png` | retenue |
| 11 | v1 | e87677a5b2a169bff6e249d805fea764 | 6 cr | `sorties/pages/11-v1.png` | retenue |

Contrôle (skill, section « Contrôle après génération ») : 11 pages en 1086x1448 ; textes exacts et accents conformes ; signature « Claire » seulement en page 2 ; aucun âge ni chevelure grise, cheveux longs bruns ondulés identiques sur toutes les pages ; planche homogène (`sorties/planche-11-pages.jpg`). Aucune relance.

Coût total : 66 crédits (0,33 $).

## Livrables

- Pages retenues : `retenues/pages/01.png` à `11.png` (toutes en v1).
- PDF : `retenues/rituel-huile-romarin-web.pdf` (800 px, JPEG 80, 1,25 Mo) et `retenues/rituel-huile-romarin-hq.pdf` (pleine résolution, JPEG 93, 3,5 Mo), page 150 x 200 mm.
- Créa finale : `creas/ebook/2026-10-14_ebook_002.pdf` et `2026-10-14_ebook_002-hq.pdf`.
