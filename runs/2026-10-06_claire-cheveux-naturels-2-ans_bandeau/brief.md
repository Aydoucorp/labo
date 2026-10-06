# Brief · Claire · 2 ans à laisser repousser ses cheveux naturels (bandeau + CTA NATUREL)

Date : 2026-10-06
Concept : montage léger sur une vidéo existante (série full-b-roll-artiste).

## Demande

- Vidéo source : transition vers les cheveux blancs naturels (12,6 s, 720×1280, musique) : cheveux teints en noir avec racine blanche, puis démarcation, mèches éclaircies, et résultat final en carré blanc argenté. Seul texte : « 2 years of growing out my natural hair color » (0 à 4,3 s).
- Traduire le hook, ajouter un motion à la fin pour faire commenter « NATUREL » (apprendre à accepter ses cheveux naturels et à en prendre soin).

## Réglages

- Hook : bandeau rouge `#E0202A`, texte blanc, « 2 ans à laisser repousser / ma couleur naturelle », sur la boîte de son texte (63, 178, 657, 292 en px source), de 0 à 4,3 s (texte détecté jusqu'à l'image 128). TikTok Sans SemiBold 60 px.
- Le résultat final (carré blanc, haut noir) est à l'écran dès 10,0 s : laissé net jusqu'à 11,6 s ; dernière image (12,6 s) prolongée jusqu'à 15,0 s avec zoom lent 1,2 %/s.
- Flou + assombrissement dès 11,6 s, carte CTA à 11,85 s : carte crème, « Commente », pastille « NATUREL » terracotta (TikTok Sans Bold 112 px), « pour apprendre à accepter / tes cheveux naturels / et à en prendre soin », barre de commentaire qui tape « NATUREL », flèche vers l'icône commentaires.
- Son d'origine jusqu'à 12,5 s, raccord (fondu enchaîné 0,15 s) sur la reprise à 8,52 s (similarité spectrale 0,74), fondu de sortie 0,8 s, SFX `whoosh_soft` + `tick_soft` sur la carte.
- Sortie 1080×1920, 15,0 s, H.264 CRF 18, AAC 192 kb/s.

## Reproduire

```
python3 montage.py --frames 1.5,11,13.5   # images de contrôle
python3 montage.py                        # rendu complet
```

## Sorties

- `sorties/claire-cheveux-naturels-fr_v1.mp4` (en attente de validation), `sorties/planche-contact_v1.jpg`
