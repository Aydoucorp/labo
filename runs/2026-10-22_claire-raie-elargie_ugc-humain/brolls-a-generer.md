# B-rolls : format hybride (C4 et C6 sans visage)

Les clips C4 et C6 ne sont plus générés en Wan : la voix ElevenLabs passe sur des b-rolls.
Wan 3.0 ne fait plus que C1, C2, C3, C5, C7 (29 s, écran noir) : environ 464 cr, soit 2,32 $.

## C4 (15,86 à 23,52 s)
| Moment | Texte | Plan | Source |
|---|---|---|---|
| 15,86 à 20,30 | À chaque cycle de pousse, le cheveu revient un peu plus fin… un peu plus fragile | Animation 3D : follicule qui rétrécit en trois temps | bibliothèque br-0015 (gratuit) |
| 20,35 à 23,52 | jusqu'au jour où ta queue de cheval te paraît deux fois moins épaisse | Queue de cheval fine tenue dans la main | **à trouver (réel) ou à générer par l'utilisateur : prompt P1** |

## C6 (30,40 à 37,59 s)
| Moment | Texte | Plan | Source |
|---|---|---|---|
| 30,40 à 32,10 | Tu dois soutenir le follicule. | Animation 3D : le cheveu continue de pousser, particules dorées | bibliothèque br-0013 (gratuit) |
| 32,38 à 35,20 | Tu dois calmer cette inflammation au niveau du cuir chevelu | Animation 3D : cuir chevelu rouge enflammé qui se calme | **à générer par l'utilisateur : prompt P2** |
| 35,28 à 37,59 | avant que tes cheveux ne s'affinent encore davantage | Jeune femme brune qui écarte sa raie | bibliothèque br-0070, réel (gratuit) |

## P1 : queue de cheval fine (4 s, 9:16)
Si une vidéo réelle existe (filmée ou trouvée), elle passe avant ce prompt.

```
Vertical 9:16 smartphone video, 4 seconds. Seen from behind and slightly to the side, a woman in her mid forties with long medium-dark brown hair stands in a bright bathroom in front of a mirror. She has pulled her hair into a low ponytail and holds the ponytail in one hand just below the hair tie, squeezing it between her fingers to show how thin and sparse it has become: the ponytail is visibly thin, barely thicker than a finger, the ends wispy and see-through. She slowly lifts it a little toward the camera, then lets it drop. Her face is not visible. Natural daylight, shot on iPhone, realistic skin and hair texture, slight handheld feel, no text, no logo.
```

## P2 : inflammation du cuir chevelu qui se calme (4 s, 9:16)
Mettre `references/style-3d-follicule.jpg` en image de départ ou de style pour garder le rendu de la bibliothèque.

```
3D medical animation, vertical 9:16, 4 seconds, same style as the reference image: a cutaway block of scalp skin floating on a dark plum background, soft pink skin layers, a cream fat layer at the bottom, one hair follicle with its hair in the centre, soft studio lighting, clean premium medical render. At the start, the skin around the follicle is swollen and glows an angry red, with small red inflammation particles pulsing around the bulb, and the hair looks thin. Over the 4 seconds, the red glow cools down and fades into a calm healthy pink, the particles dissolve, the bulb plumps up slightly and the hair looks a bit stronger. Slow gentle push-in camera. No text, no labels, no logo.
```
