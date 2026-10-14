# Tests de synchro Seedance 2.5, méthode écran noir (2026-10-14)

Image de départ : `retenues/depart.png` (v4). Prompt sobre : `prompt-sobre.txt` (repris du test validé du 2026-10-10 : tête presque immobile, mains immobiles, aucune timeline). 480p, 9:16.

| Test | Voix | Clip | Son généré | Tâche KIE | Coût |
|---|---|---|---|---|---|
| A | 0 à 5,5 s (`F1a.wav`) | 6 s | oui | 9d9bc1113273df6a68e8ca409314609a | 204 cr |
| B | 0 à 5,5 s | 6 s | non | 7436339106c8a50f8bbcd89572660737 | 204 cr |
| C | 0 à 9,5 s (`F1.wav`) | 10 s | oui | fa7718011fb1fcb8c1e00bd79a27017b | 340 cr |

## Contrôle par phonèmes (forme de la bouche à des instants où elle est connue)

Planches : `levres-points-cles.jpg` (phrase 1), `levres-points-cles-phrase2.jpg` (phrase 2). Bilabiales (b, m, p) : bouche fermée attendue ; voyelles ouvertes : bouche ouverte.

Phrase 1 (0 à 5,5 s), 7 points : silence, a, b, m, a, p, ou.

| Clip | Points justes |
|---|---|
| F1 v1 (720p, gestes, 10 s) | 6/7 |
| A (5,5 s, son on) | 5/7 (p de « pour » ouvert) |
| B (5,5 s, son off) | 7/7 |
| C (9,5 s, son on) | 5/7 |

Phrase 2 (5,5 à 9,5 s), 8 points : pause, P, m, b, i, p, a, fin.

| Clip | Points justes |
|---|---|
| F1 v1 | 2/8 (la bouche suit la parole inventée par Seedance) |
| C | 3/8 (mieux que F1 mais faux sur les bilabiales et bouche ouverte après le dernier mot) |

## Conclusion

- La méthode tient sur environ 5 s. Au-delà, même avec un prompt sobre, la bouche se détache de la voix.
- Le son généré désactivé (B) donne le meilleur résultat sur l'échantillon : Seedance n'invente pas de parole concurrente.
- La mesure automatique par corrélation (`scripts/mesure_levres.py`) est trop bruitée pour trancher (corrélations 0,3 à 0,6, même sur la référence validée) : le contrôle par phonèmes est plus fiable.
