# Mode A du skill talking-head : écrit decoupage.json (plans, clips avatar, b-rolls), coupe les extraits audio,
# puis génère decoupage.md. Temps = alignement forcé MMS (mots_mms.json) sur le texte exact du script.
import json, subprocess
W = json.load(open("mots_mms.json"))["words"]
DUR = 59.56
SK = "../../.claude/skills/talking-head/scripts"

def texte(a, b):
    ws = [w for w in W if a - 0.01 <= w["start"] < b - 0.01]
    return " ".join(w["w"] + (w.get("punct_after") or "") for w in ws).replace(" ,", ",")

# (id, début, fin, type, zoom, surimpression, ce qu'on voit, règle, mot déclencheur, source)
P = [
 ("P01", 0.00, 4.30, "Écran partagé", "1:1", "Bandeau titre (couture)", "Haut : avatar au micro. Bas : femme d'environ 50 ans qui montre une queue de cheval devenue fine ou une raie élargie, puis gros plan de cheveux fins sur une brosse.", "Accroche, recette 1", "Plan bas 2 sur « cheveux » (2,20 s)", "S01 + b-rolls B01, B02 (à trouver)"),
 ("P02", 4.30, 13.50, "Animation éducative", "-", "Étiquettes : Œstrogènes, Phase de croissance, DHT, Follicule", "Coupe d'un follicule en pictos plats : les œstrogènes (petites sphères) s'éteignent, le cheveu quitte sa phase de croissance et se détache ; puis des molécules de DHT arrivent et le follicule rétrécit, le cheveu devient plus fin.", "R5", "Œstrogènes 5,00 · Phase de croissance 7,05 · DHT 10,10 · Follicule 12,65", "Animation E1"),
 ("P03", 13.50, 16.70, "Avatar", "A", "-", "Avatar, explication posée, main ouverte qui descend doucement sur « amincir ».", "Retour avatar après l'animation", "-", "A01"),
 ("P04", 16.70, 19.10, "B-roll (carte)", "-", "-", "Gros plan d'une raie poivre et sel, cuir chevelu visible entre des cheveux fins, lent zoom avant.", "R1", "Coupe 0,09 s avant « ce »", "B-roll B03 (à trouver)"),
 ("P05", 19.10, 21.20, "Avatar", "C", "-", "Avatar serré, grand sourire, petit hochement : le retournement.", "Retournement (arc 6)", "Flash à 19,10 s", "A01"),
 ("P06", 21.20, 22.75, "B-roll (plein écran)", "-", "-", "Prise de sang au pli du coude d'une femme de 45 à 55 ans, garrot, infirmière.", "R4", "Coupe 0,10 s avant « Faites »", "B-roll B04 (à trouver)"),
 ("P07", 22.75, 26.10, "Avatar", "B", "-", "Avatar, compte sur deux doigts : « fer », puis « thyroïde ».", "R8 + geste", "Doigts sur « fer » (23,43) et « thyroïde » (24,53)", "A02"),
 ("P08", 26.10, 27.20, "Avatar", "C", "-", "Avatar serré, sourire rassurant sur « et cela se corrige ».", "R8 (rassurance)", "-", "A02"),
 ("P09", 27.20, 31.30, "Avatar + objet détouré", "A", "Pot de collagène en poudre détouré qui pope près des mains", "Avatar, objet détouré (pot sans marque et cuillère de poudre) à côté de la main.", "R7 (objet cité)", "Objet sur « complément » (28,30)", "A02 + objet O1"),
 ("P10", 31.30, 33.13, "B-roll (plein écran)", "-", "-", "Femme de 45 à 55 ans qui secoue une chevelure souple et brillante, lumière de fenêtre.", "R2", "Coupe 0,11 s avant « et »", "B-roll B05 (à trouver)"),
 ("P11", 33.13, 36.68, "B-roll démo (plein écran)", "-", "-", "Deux mains massent le cuir chevelu du bout des doigts.", "R4 (démo)", "Coupe 0,10 s avant « Ensuite »", "B-roll B06 (à trouver)"),
 ("P12", 36.68, 40.75, "B-roll démo (plein écran)", "-", "-", "Une pipette fait tomber une ou deux gouttes d'huile essentielle de romarin dans un petit flacon d'huile végétale.", "R4 (démo)", "Coupe sur « avec »", "B-roll B07 (à trouver)"),
 ("P13", 40.75, 45.80, "Infographie à lignes", "-", "2 lignes : Huile de romarin, Massage quotidien ; « encourageantes » surligné", "Fond crème, 2 lignes illustrées (pictos du style de la charte), chacune apparaît sur son nom, puis le mot « encourageantes » se surligne.", "R7 + R2", "Huile de romarin 41,85 · Massage quotidien 43,10 · surligneur 45,00", "Images I1, I2"),
 ("P14", 45.80, 49.80, "Avatar", "B", "-", "Avatar chaleureux, gestes doux des deux mains sur « doux et simple ».", "R8 (nuance, conseil)", "-", "A03"),
 ("P15", 49.80, 52.33, "Avatar", "A", "-", "Avatar, regard caméra, sourire.", "CTA", "-", "A03"),
 ("P16", 52.33, 55.75, "Avatar + carte", "B", "Carte du guide (titre écrit au montage)", "Avatar, carte crème qui monte à côté de lui avec le titre « Comment traiter l'affinement des cheveux à la ménopause » et un brin de romarin.", "CTA", "Carte sur « Comment » (52,30)", "A03 + carte montage"),
 ("P17", 55.75, DUR, "Avatar", "C", "Mot « GUIDE » + bouton « S'abonner »", "Avatar serré, regard caméra, « GUIDE » en grand sur la poitrine, bouton « S'abonner » qui se clique à la fin.", "CTA", "« GUIDE » à 56,35 s · bouton à 58,40 s", "A03"),
]

CLIPS = [
 {"id": "S01", "debut": 0.11, "fin": 3.88, "format": "1:1"},
 {"id": "A01", "debut": 13.59, "fin": 21.01, "format": "9:16"},
 {"id": "A02", "debut": 22.84, "fin": 31.19, "format": "9:16"},
 {"id": "A03", "debut": 45.93, "fin": 59.55, "format": "9:16"},
]
def B(i,a,b,imp,voir,profil,fr,en,tags,ev="Texte incrusté, filigrane, logo de marque."):
    return {"id":i,"debut":a,"fin":b,"phrase":texte(a,b),"importance":imp,"voir":voir,"profil":profil,
            "mots_fr":fr,"mots_en":en,"hashtags":tags,"eviter":ev,"format":"vertical de préférence"}
BR = [
 B("B01",0.00,2.20,"Important · accroche (bas de l'écran partagé)","Une femme montre que ses cheveux se sont affinés : queue de cheval devenue fine entre ses doigts, ou raie élargie qu'elle écarte devant le miroir (recette 1 : le problème sur quelqu'un qui ressemble à la cible).","Femme de 48 à 58 ans, chez elle, lumière naturelle",["cheveux fins ménopause","perte de densité cheveux","queue de cheval fine","raie élargie femme","cheveux clairsemés femme","chute cheveux 50 ans"],["thinning hair menopause","thin ponytail","female hair thinning","widening part woman","hair loss menopause","thinning hair women over 50"],["#menopausehair","#thinninghair","#hairthinning","#chutedecheveux"]),
 B("B02",2.20,4.30,"Important · accroche (bas de l'écran partagé)","Gros plan de cheveux fins restés sur une brosse ou dans la main après le coiffage, la femme regarde, inquiète.","Femme de 48 à 58 ans, salle de bain",["cheveux sur la brosse","cheveux qui tombent","chute de cheveux brosse","cheveux dans la main"],["hair on brush","hair falling out brush","hair shedding","hair loss brush woman"],["#hairshedding","#hairloss","#chutedecheveux"]),
 B("B03",16.70,19.10,"Important","Gros plan d'une raie où le cuir chevelu se voit entre des cheveux fins (la conséquence visible, R1).","Femme de 48 à 58 ans, cheveux naturels bruns ou poivre et sel",["raie cuir chevelu visible","cheveux fins raie","cuir chevelu dégarni femme","densité cheveux"],["visible scalp part","thinning part closeup","scalp showing through hair","female pattern hair loss part"],["#thinninghair","#scalpcare","#femalehairloss"]),
 B("B04",21.20,22.75,"Important","Une prise de sang au pli du coude : garrot, aiguille ou tube qui se remplit (R4).","Femme de 45 à 55 ans, cabinet ou laboratoire, lumière claire",["prise de sang","bilan sanguin","laboratoire analyse","infirmière prise de sang","ferritine","bilan thyroïde"],["blood test","blood draw","phlebotomy","nurse drawing blood","lab test woman","blood work"],["#prisedesang","#bilansanguin","#bloodtest","#bloodwork"],"Gros plan trop sanglant, texte incrusté, logo de laboratoire."),
 B("B05",31.30,33.13,"Important","Une femme secoue ou passe la main dans une chevelure souple, brillante et dense (le résultat désiré, R2).","Femme de 45 à 55 ans, cheveux naturels bruns ou poivre et sel, lumière de fenêtre",["cheveux brillants","femme secoue cheveux","cheveux sains","chevelure épaisse","cheveux poivre et sel"],["healthy hair","hair flip","shiny hair woman","thick hair","grey hair woman","hair toss slow motion"],["#healthyhair","#hairflip","#cheveuxsains","#greyhair"],"Brushing de salon, publicité de shampoing, logo, texte incrusté."),
 B("B06",33.13,36.68,"Important · démo","Deux mains massent le cuir chevelu du bout des doigts, petits cercles, le soir (le geste sur son verbe « massez »).","Femme de 45 à 55 ans, salle de bain ou chambre, lumière douce",["massage cuir chevelu","masser cuir chevelu doigts","routine cheveux soir","massage crânien"],["scalp massage","fingertip scalp massage","scalp massage routine","hair growth massage"],["#scalpmassage","#massagecuirchevelu","#hairroutine","#hairgrowth"]),
 B("B07",36.68,40.75,"Important · démo","Une pipette fait tomber une ou deux gouttes d'huile essentielle de romarin dans un petit flacon d'huile végétale, puis le mélange sur la raie.","Mains seules, salle de bain ou plan de travail clair",["huile essentielle romarin","gouttes pipette huile","mélange huile cheveux","huile romarin cheveux","huile cuir chevelu"],["rosemary oil drops","rosemary essential oil","dropper oil","DIY hair oil","rosemary oil scalp"],["#rosemaryoil","#huilederomarin","#hairoil","#diyhair"],"Flacon de marque lisible, texte incrusté."),
]
json.dump({"duree": DUR, "plans": [dict(zip(["id","debut","fin","type","zoom","surimpression","voir","regle","declencheur","source"], p)) | {"texte": texte(p[1], p[2])} for p in P],
           "clips_avatar": CLIPS, "brolls": BR}, open("decoupage.json", "w"), ensure_ascii=False, indent=1)
subprocess.run(["python3", f"{SK}/couper_audio.py", "voix.mp3", "decoupage.json", "--mots", "mots.json", "--min", "4", "--max", "30"], check=True)
