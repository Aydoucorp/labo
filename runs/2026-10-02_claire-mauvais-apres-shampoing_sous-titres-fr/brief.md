# Brief · Claire · mauvais après-shampoing (sous-titres FR + CTA)

Date : 2026-10-02
Concept : montage léger sur une vidéo existante (skill création full b-roll artiste, sans b-roll ni voix off).

## Demande

- Vidéo source : TikTok trouvée via Trendtrack (id 7689539918963510559), 26,5 s, 720×1280, musique seule (pas de voix), sous-titres anglais incrustés.
- Remplacer ses sous-titres anglais par la traduction française fournie par l'utilisateur.
- Couper uniquement son CTA final « (my favorites are on my page!) » et le remplacer par un motion avec le CTA Claire.

## Décisions validées avec l'utilisateur

| Point | Choix |
|---|---|
| Texte CTA | « Commente GUIDE pour savoir quel après-shampoing choisir » |
| Masquage de ses sous-titres | Bandeau opaque (gratuit). Option IA chiffrée et écartée : FLUX 3 Video Edit (Higgsfield) à 1 crédit/s, 15 s max par passe, soit environ 25 crédits pour 2 passes ; compte Higgsfield à 0 crédit. |
| Style des sous-titres | Comme les siens : minuscules, phrase par phrase, mêmes positions et mêmes timings, typo TikTok Sans |
| Fin | Gel du dernier plan juste avant son CTA, flou progressif, carte motion Claire par dessus |

## Sous-titres (timings calés sur les siens, détectés image par image)

| # | Début | Fin | Texte FR |
|---|---|---|---|
| 1 | 0,00 | 9,20 | voici les signes que vous utilisez le mauvais après-shampoing... |
| 2 | 9,20 | 10,83 | vos cheveux ont l'air secs et abîmés... |
| 3 | 10,83 | 12,97 | vos doigts s'accrochent dans les nœuds pendant le séchage... |
| 4 | 12,97 | 14,90 | il devient difficile de séparer vos mèches sous la douche, même avec le produit... |
| 5 | 14,90 | 16,87 | vous trouvez de petits nœuds persistants après le brushing... |
| 6 | 16,87 | 18,80 | le brossage est laborieux... |
| 7 | 18,80 | 20,90 | vos longueurs semblent sèches, raides ou cassantes... |
| 8 | 20,90 | 22,47 | des nœuds se reforment aussitôt après le passage de la brosse... |
| 9 | 22,47 | 24,70 | vos cheveux peuvent aussi paraître lourds, plats et gras aux racines... |
| 10 | 24,70 | 26,85 | le bon après-shampoing ou masque capillaire peut réparer tout cela... |

## Réglages

- Sortie 1080×1920, 30 i/s, H.264 CRF 18, AAC 192 kb/s, durée 30,0 s. Agrandissement Lanczos depuis la source 720×1280.
- Bandeaux (v2, demande utilisateur) : terracotta `#A8553A` opaque avec texte crème `#FAF6F3` ; hook (sous-titre 1, 0 à 9,2 s) en rouge `#E0202A` avec texte blanc. v1 : noir opaque, texte blanc. Coins arrondis 26 px, TikTok Sans SemiBold 60 px, interligne 72 px, largeur de texte max 860 px, lignes équilibrées. Chaque bandeau couvre la boîte de son sous-titre anglais + marge (boîtes relevées dans `montage_soustitres.py`).
- Son CTA apparaît à 25,43 s (image 763). Gel sur l'image 761 (25,37 s) à partir de 25,40 s, zoom lent 1,2 %/s.
- Flou + assombrissement de 26,60 à 27,00 s (sigma jusqu'à 27, -32 % de luminosité).
- Carte CTA à 26,85 s : carte crème `#FAF6F3`, « Commente » encre `#2E2A26`, pastille « GUIDE » terracotta `#A8553A` (pop ressort puis pulsation à 2,2 s), « pour savoir quel après-shampoing choisir », barre de commentaire qui tape « GUIDE » lettre par lettre, flèche terracotta qui rebondit vers l'icône commentaires du rail TikTok.
- Musique : son d'origine jusqu'à 26,40 s, puis raccord (fondu enchaîné 0,15 s) sur la reprise à 21,55 s (point trouvé par similarité spectrale), fondu de sortie sur les 0,8 dernières secondes. SFX : `whoosh_soft` à l'arrivée de la carte, `tick_soft` 0,3 s après.

## Reproduire

```
python3 montage_soustitres.py --frames 2,14,25.3,28.6   # images de contrôle
python3 montage_soustitres.py                           # rendu complet
```

## Sorties

- `sorties/claire-mauvais-apres-shampoing-fr_v1.mp4` (bandeaux noirs, remplacée)
- `sorties/claire-mauvais-apres-shampoing-fr_v2.mp4` (bandeaux terracotta + hook rouge, rendu en attente)
- `sorties/planche-contact_v1.jpg`
