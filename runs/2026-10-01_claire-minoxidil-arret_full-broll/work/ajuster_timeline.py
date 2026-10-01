# Ajustements manuels de la timeline après build_timeline.py (à relancer si la timeline est reconstruite) :
# les sorties de 3D vers le réel passent en cut (on garde le zoomthrough pour entrer dans la 3D et aux changements de section).
import json
p = 'work/timeline.json'; t = json.load(open(p))
for c in t['clips']:
    if c['shot_id'] in ('09', '11', '15a', '16'):
        c['transition_in'] = {"type": "cut", "frames": 0, "dir": None}
json.dump(t, open(p, 'w'), ensure_ascii=False, indent=1)
# 21a : la vidéo montre déjà « Guide » et le sous-titre le dit, on retire la mention en double
t = json.load(open(p))
t['overlays'] = [o for o in t['overlays'] if o['text'] != 'Commente « Guide »']
json.dump(t, open(p, 'w'), ensure_ascii=False, indent=1)
