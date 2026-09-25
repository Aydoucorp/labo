# Brief · Claire · Guide racine · Paper Cut

- **Date** : 2026-09-25
- **Marque** : Les cheveux de Claire (`Claire/BRAND-DNA-CLAIRE.md`)
- **Skill** : `papercut-publicite` (collage papier déchiré, stop-motion, voix off externe, bruitages papier, sans musique ni sous-titres)
- **Format** : 9:16 vertical, 31,72 s
- **Produit** : guide gratuit de recettes pour le cuir chevelu (lead magnet). Pas de couverture réelle fournie → couverture provisoire en papier déchiré au plan P11.
- **Appel à l'action** : « Commente GUIDE »
- **Script** : `script.txt`, conservé tel quel à la demande de l'utilisateur.
- **Voix off** : `audio/voix-off-finale.m4a` (ElevenLabs v3, AAC mono 44,1 kHz, 31,72 s), fournie par l'utilisateur, finale.

## Mesure de la voix

- Outils : ffmpeg 7.0.2 (binaire imageio-ffmpeg) pour la durée et les silences, faster-whisper 1.2.1 modèle `medium` (CPU int8) pour l'horodatage mot à mot → `audio/mots-horodates.json`.
- Silences détectés (-40 dB, ≥ 0,25 s) : 4,01-4,40 · 6,88-7,27 · 27,45-27,86 · 29,15-29,42.
- **Écart à vérifier à l'écoute** : Whisper entend « tomber **partout** » là où le script dit « tomber **par touffes** ». Le titre de P01 (« ÇA TOMBE ») marche dans les deux cas.

## Palette et style

Rôles émotionnels du module conservés, teintes rapprochées du brand DNA :

| Rôle module | Teinte Claire |
|---|---|
| Papier de base | Crème `#FAF6F3` |
| Problème / mythe | Terracotta `#A8553A` (P01-P05, P10) |
| Contraste / verdict | Prune `#7A4351` (P06-P07) |
| Résolution | Sauge `#8C9B86` (P08-P09, P11), décor uniquement, jamais de texte |
| Encre des titres | Encre `#2E2A26` |

**Adaptation assumée** : les titres restent en lettres de journal découpées, condensées et grasses (signature du module), et non en Fraunces. La typo de marque pourra servir sur la couverture réelle du guide.

Photos découpées de cheveux conformes au brand DNA : poivre et sel irrégulier, ondulé coiffé à la main, lumière de fenêtre, rendu smartphone. Jamais de brushing de salon, d'argenté uniforme ni de rendu pub shampoing.

## Contrôle brand DNA du script (à trancher avant génération)

Le script est conservé tel quel. Le test « avant publication » du brand DNA relève ces points :

1. **Signal d'alarme sans renvoi pro.** « Tomber par touffes… des trous » relève du pilier *Densité et chute*, qui prévoit un « renvoi systématique au professionnel ». La voix off n'en contient pas.
2. **« Les dermatologues sont formels »** : autorité citée sans source. Il faut une source vérifiable, à noter ici, ou une reformulation.
3. **« Tout ce qui fonctionne s'applique sur le cuir chevelu »** : affirmation absolue à portée santé (règle « aucune allégation santé »).
4. **« Ton problème se traite à la racine » + recettes à appliquer** : peut se lire comme une promesse que des recettes maison traitent la chute (« une promesse qu'on ne peut pas tenir »). À surveiller aussi pour la validation des pubs santé sur Meta.

Modifier la voix off implique de la régénérer et de recaler le storyboard. La génération d'images peut attendre cette décision.

## Outils de génération

- Clé KIE en place (`.env`), solde vérifié à 49,8 crédits le 2026-09-24.
- Connecteur Higgsfield disponible.
- Modèles, tarifs et durées d'animation minimales **à vérifier au moment de produire**. Rien n'a été généré ni payé à ce stade.

## Fichiers

- `script.txt` : script d'origine
- `audio/voix-off-finale.m4a`, `audio/mots-horodates.json`
- `storyboard.md` : 11 plans calés sur la voix
- `prompts.md` : prompts image et animation, entièrement remplis
- `montage.md` : feuille de montage
- `journal.md` : journal des générations
- `build_storyboard.py` : source du storyboard et des prompts
