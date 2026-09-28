# Génère decoupage.md (livrable du mode A) à partir de mots.json, audio_avatar/clips_avatar.json et du plan ci-dessous.
import json
mots = json.load(open("mots.json"))
clips = {c["id"]: c for c in json.load(open("audio_avatar/clips_avatar.json"))}
DUR = 56.35

# Correction des mots d'après le script (le script fait autorité sur les mots)
FIX = {"carence,": "carences,", "légumineuse.": "légumineuses.", "de": None}
def texte(a, b):
    ws = [w["w"] for w in mots if w["s"] >= a - 0.01 and w["e"] <= b + 0.01]
    s = " ".join(ws).replace(" '", "'").replace(" %", " %").replace("« guide »", "« GUIDE »")
    s = s.replace("carence,", "carences,").replace("légumineuse.", "légumineuses.").replace("peroxyde de l'hydrogène", "peroxyde d'hydrogène")
    return s

# (id, début, fin, type, zoom, surimpression, ce qu'on voit, règle, mot déclencheur, source)
P = [
 ("P01", 0.00, 5.90, "Écran partagé", "1:1", "Bandeau titre (couture)", "Haut : avatar au micro. Bas : femme de 35 à 45 ans qui écarte ses cheveux et montre des racines grises (2 plans : raie avec racines grises, puis tempes grisonnantes en gros plan).", "Accroche, recette 1", "Plan bas 2 sur « ce » (3,28 s)", "S01 + b-roll B01, B02"),
 ("P02", 5.90, 9.80, "Avatar", "C", "Gros chiffre « 30 % » (label « héréditaire »)", "Avatar serré, léger penché en avant sur le chiffre.", "R8 (chiffre clé)", "« 30 » à 6,56 s (apparition 6,50 s)", "A01"),
 ("P03", 9.80, 14.20, "Avatar + preuve", "B", "Capture de la source du chiffre, surlignée", "Avatar, puis carte blanche qui monte avec la capture de la source, surligneur sur la phrase clé.", "R6", "Carte à 10,65 s (0,6 s après « Les »)", "A01 + preuve PR1"),
 ("P04", 14.20, 23.10, "Animation éducative", "-", "Étiquettes : Follicule, Catalase, H₂O₂, Pigment", "Coupe d'un follicule pileux en pictos plats. Une enzyme (catalase) neutralise des bulles de peroxyde ; puis les bulles s'accumulent et la mèche se décolore de l'intérieur.", "R5", "Follicule 14,40 s · Catalase 16,64 s · H₂O₂ 18,50 s · décoloration 20,78 s", "Animation E1"),
 ("P05", 23.10, 25.60, "Avatar", "A", "-", "Avatar, explication posée, paume ouverte.", "Retour avatar après l'animation", "-", "A02"),
 ("P06", 25.60, 28.85, "B-roll (carte)", "-", "-", "Gros plan d'une raie aux racines blanches, lent zoom avant.", "R1", "Coupe 0,14 s avant « la catalase »", "B-roll B03"),
 ("P07", 28.85, 31.50, "Avatar", "C", "-", "Avatar, compte 3 doigts sur « Trois carences ».", "R8 + geste", "Geste sur « Trois » (29,06 s)", "A03"),
 ("P08", 31.50, 35.30, "Avatar", "B", "-", "Avatar, énumère B12, cuivre, fer sur les doigts.", "R8 (noms abstraits)", "-", "A03"),
 ("P09", 35.30, 43.35, "Infographie à lignes", "-", "3 lignes : Cuivre, B12, Fer", "Fond crème, 3 lignes illustrées par des cheveux (pas par les nutriments) : chaque ligne apparaît sur son nom, la phrase se surligne pendant qu'elle est dite.", "R7 + R2", "Cuivre 35,78 s · B12 39,52 s · Fer 40,30 s", "Images I1, I2, I3"),
 ("P10", 43.35, 44.65, "Avatar", "A", "-", "Insert avatar « Dans l'assiette ».", "Relance d'attention", "-", "A04"),
 ("P11", 44.65, 49.35, "Micro-montage (cartes)", "-", "-", "5 photos d'aliments en carte arrondie, une par nom : foie, fruits de mer, œufs, viande rouge, légumineuses.", "R7 (micro-montage)", "foie 44,78 · fruits de mer 45,44 · œufs 46,50 · viande rouge 47,20 · légumineuses 48,18", "Images I4 à I8"),
 ("P12", 49.35, 51.35, "B-roll (plein écran)", "-", "-", "Femme de 40 à 50 ans, pieds nus dehors au soleil du matin, tasse à la main.", "R4", "Coupe 0,23 s avant « Et un peu de soleil »", "B-roll B04"),
 ("P13", 51.35, 53.70, "Avatar", "B", "-", "Avatar, regard caméra, sourire léger.", "CTA", "-", "A05"),
 ("P14", 53.70, 56.35, "Avatar", "C", "Mot « GUIDE » + bouton « S'abonner »", "Avatar serré, regard caméra, « GUIDE » en grand sur la poitrine, bouton « S'abonner » qui se clique à la fin.", "CTA", "« GUIDE » à 54,60 s · bouton à 55,20 s", "A05"),
]

GESTES = {
 "S01": "subtle concerned frown on 'gris', small head shake on 'ce n'est pas juste la génétique'",
 "A01": "leans in slightly on '30 %' around 0.7 s; open palm on 'c'est votre corps qui vous envoie un signal'",
 "A02": "open palm while explaining 'Avec l'âge ou en cas de carences'",
 "A03": "raises three fingers on 'Trois' around 0.3 s, then counts on fingers during 'la vitamine B12, le cuivre et le fer'",
 "A04": "small nod on 'Dans l'assiette'",
 "A05": "looks straight at the camera for the call to action, warm light smile on the last phrase 'mon guide gratuit'",
}
FORMAT = {"S01": "1:1", "A01": "9:16", "A02": "9:16", "A03": "9:16", "A04": "9:16", "A05": "9:16"}

def seedance(cid):
    c = clips[cid]; s0, e0 = c["clipStart"], c["clipEnd"]
    lines = []
    # une ligne par phrase de l'extrait (regroupement sur les pauses)
    ws = [w for w in mots if w["s"] >= s0 - 0.01 and w["e"] <= e0 + 0.01]
    grp = []; 
    for i, w in enumerate(ws):
        grp.append(w)
        nxt = ws[i+1] if i + 1 < len(ws) else None
        if nxt is None or nxt["s"] - w["e"] >= 0.25:
            t = " ".join(x["w"] for x in grp).replace(" '", "'")
            t = t.replace("carence,", "carences,").replace("légumineuse.", "légumineuses.").replace("peroxyde de l'hydrogène", "peroxyde d'hydrogène")
            lines.append(f'{grp[0]["s"]-s0:.1f}-{grp[-1]["e"]-s0:.1f} s: "{t}"')
            grp = []
    square = " Square framing identical to Image 1, head and shoulders." if FORMAT[cid] == "1:1" else ""
    gaze = "toward the camera for the call to action" if cid == "A05" else "slightly off-camera toward an unseen interviewer"
    return f"""Create a {c['duree_a_demander']}-second {FORMAT[cid]} photorealistic podcast talking-head shot, French speech. One continuous locked-off shot, natural real-time speed.{square}
REFERENCES: Image 1 = the exact first frame and the only identity, wardrobe, microphone, desk, background, lighting and framing reference. Audio 1 = the exact voice to lip-sync, from its first to its last syllable; do not change, speed up or replace it.
STARTING STATE: The person from Image 1, seated in the same pose, same framing, mouth closed, hands resting on the desk below the microphone. Only this person is visible.
PERFORMANCE: Natural podcast delivery, gaze {gaze}, subtle head movements, blinking, natural breathing, small nods on key words. {GESTES[cid][0].upper() + GESTES[cid][1:]}. Hands stay below the microphone and never cover the mouth. No repetitive gesture loop.
TIMELINE AND EXACT WORDS: {" ; ".join(lines)}.
AUDIO: Lip sync only to Audio 1, precise on every syllable. Mouth closed and still during silences. No music, no added sound effects, no other voice.
CONTINUITY: Same person, clothes, microphone, desk, background and lighting as Image 1 for the whole shot. Camera never moves, never zooms, never cuts. No text, no subtitles, no logo."""

L = []
A = L.append
# Synthèse
cats = {}
for p in P:
    k = {"Écran partagé": "Écran partagé", "Avatar": "Avatar", "Avatar + preuve": "Avatar + surimpression"}.get(p[3], p[3])
    if p[3] == "Avatar" and p[5] != "-": k = "Avatar + surimpression"
    if p[3].startswith("B-roll") or p[3].startswith("Micro"): k = "B-roll / photos"
    if p[3].startswith("Infographie"): k = "Infographie"
    if p[3].startswith("Animation"): k = "Animation"
    cats[k] = cats.get(k, 0) + p[2] - p[1]
A("# Découpage · Claire · Cheveux gris et carences · Talking head\n")
A("**État : découpage livré (mode A). Aucun média généré, aucune dépense.**\n")
A("## 1. Synthèse\n")
A(f"- **Format détecté** : mécanisme + solutions (cause cachée, puis carences et conseils). Cible avatar 55 à 60 %.")
A(f"- **Durée** : {DUR:.2f} s · **débit** : 155 mots/min · **{len(P)} plans** · durée moyenne {DUR/len(P):.1f} s")
tot = sum(cats.values())
A("- **Répartition** : " + " · ".join(f"{k} {v:.1f} s ({v/tot*100:.0f} %)" for k, v in cats.items()))
av = cats.get("Avatar", 0) + cats.get("Avatar + surimpression", 0) + cats.get("Écran partagé", 0)
A(f"- **Avatar visible (écran partagé compris)** : {av:.1f} s ({av/tot*100:.0f} %), un peu sous la cible : le script contient beaucoup de noms concrets (aliments, carences) qui gagnent à être illustrés.")
A(f"- **Clips avatar** : 6 (1 en 1:1 pour l'écran partagé, 5 en 9:16), **36 s à générer** (Seedance 2.5).")
A("- **Images** : 8 (3 lignes d'infographie, 5 aliments) + 1 image de départ d'animation · **objets détourés** : 0 · **animation éducative** : 1 (9 s) · **b-rolls à trouver** : 4 · **preuve à fournir** : 1")
A("- **Transitions spéciales** : 4 (flash sortie d'accroche 5,90 s ; cercle entrée animation 14,20 s ; cercle entrée infographie 35,30 s ; flash retour avatar 51,35 s)")
A("- **Plus long bloc sans avatar** : 14,20 à 23,10 s (8,9 s, animation qui évolue) et 35,30 à 43,35 s (8,1 s, infographie qui se construit). Sous la limite de 15 s.")
A("- **Écarts script / audio** : Whisper entend « peroxyde **de l'**hydrogène », « carence », « légumineuse » ; le script (« peroxyde d'hydrogène », « carences », « légumineuses ») fait foi pour les sous-titres. À réécouter : si la voix dit vraiment « de l'hydrogène », c'est la voix qui s'est trompée.\n")
A("## 2. Tableau de découpage\n")
A("| # | Début | Fin | Durée | Texte exact | Type | Zoom | Surimpression | Ce qu'on voit | Règle | Mot déclencheur | Source |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|")
for p in P:
    A(f"| {p[0]} | {p[1]:.1f} | {p[2]:.1f} | {p[2]-p[1]:.1f} s | {texte(p[1], p[2])} | {p[3]} | {p[4]} | {p[5]} | {p[6]} | {p[7]} | {p[8]} | {p[9]} |")
A("\nCoupes : toutes dans un silence, 0,05 à 0,3 s avant le premier mot de la phrase. Zooms avatar : jamais deux fois le même de suite (C, B · A · C, B · A · B, C).\n")
A("## 3. Clips avatar (Seedance 2.5)\n")
A("Seedance 2.5 sur KIE ne permet pas de combiner une première image imposée et un audio de référence : l'image de départ est envoyée comme **image de référence** et le prompt la déclare « exact first frame ». À vérifier sur le premier clip. Son du modèle coupé au montage.\n")
for cid in ["S01", "A01", "A02", "A03", "A04", "A05"]:
    c = clips[cid]
    A(f"### {cid} · {FORMAT[cid]} · extrait `audio_avatar/{cid}.wav` · {c['clipStart']:.2f} → {c['clipEnd']:.2f} s ({c['duree']:.2f} s, demander {c['duree_a_demander']} s)\n")
    A(f"- Image de départ : `_config/depart_{'1x1' if FORMAT[cid]=='1:1' else '9x16'}.png` · geste : {GESTES[cid]}")
    A(f"- `clipStart` pour le montage : {c['clipStart']:.3f}\n")
    A("```text\n" + seedance(cid) + "\n```\n")
open("decoupage_part1.md", "w").write("\n".join(L) + "\n")
print(cats)
