# Dessine la maquette de mise en page 9:16 (tailles de mots, zones, place du packshot) en pixels exacts.
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
CREME=(250,246,243); TERRA=(168,85,58); PRUNE=(122,67,81); SAUGE=(140,155,134); ENCRE=(46,42,38); GRIS=(180,173,164)
F="/usr/share/fonts/truetype/dejavu/"
def f(n,s): return ImageFont.truetype(F+n,s)
def hatch(d,box,col):
    x0,y0,x1,y1=box
    for k in range(x0-(y1-y0),x1,28): d.line([(max(k,x0),y0+max(0,x0-k)),(min(k+(y1-y0),x1),y1-max(0,k+(y1-y0)-x1))],fill=col,width=2)
def panel(title,sub,packshot):
    im=Image.new("RGB",(W,H),CREME); d=ImageDraw.Draw(im)
    hatch(d,(0,0,W,220),GRIS); hatch(d,(0,1540,W,H),GRIS)
    d.text((W//2,110),"ZONE INTERFACE · laisser vide (220 px)",font=f("DejaVuSans-Bold.ttf",30),fill=ENCRE,anchor="mm")
    d.text((W//2,1730),"ZONE INTERFACE + LÉGENDE · laisser vide (380 px)",font=f("DejaVuSans-Bold.ttf",30),fill=ENCRE,anchor="mm")
    d.rectangle((60,220,W-60,1540),outline=GRIS,width=3)
    d.text((70,1545-40 if not packshot else 225),"marge latérale 60 px",font=f("DejaVuSans.ttf",24),fill=GRIS)
    # titre
    ty0,ty1=(260,560) if packshot else (260,620)
    d.rectangle((60,ty0,W-60,ty1),outline=TERRA,width=5)
    fs=260
    while f("DejaVuSans-Bold.ttf",fs).getlength(title)>920: fs-=4
    d.text((W//2,(ty0+ty1)//2),title,font=f("DejaVuSans-Bold.ttf",fs),fill=ENCRE,anchor="mm")
    d.text((72,ty0+8),"TITRE 1-3 mots · lettres 170-260 px (9-13 % de H) · largeur ≤ 960 px",font=f("DejaVuSans.ttf",24),fill=TERRA)
    if packshot:
        pw,ph=620,775; cx,cy=W//2,1110
        card=Image.new("RGBA",(pw,ph),(0,0,0,0)); cd=ImageDraw.Draw(card)
        cd.rectangle((0,0,pw-1,ph-1),fill=(239,231,224,255),outline=TERRA,width=6)
        cd.text((pw//2,ph//2-40),"PACKSHOT",font=f("DejaVuSans-Bold.ttf",64),fill=ENCRE,anchor="mm")
        cd.text((pw//2,ph//2+40),"couverture du guide",font=f("DejaVuSans.ttf",36),fill=ENCRE,anchor="mm")
        cd.text((pw//2,ph//2+95),"620 × 775 px (57 % de W)",font=f("DejaVuSans.ttf",30),fill=ENCRE,anchor="mm")
        card=card.rotate(-3,expand=True,resample=Image.BICUBIC)
        im.paste(card,(cx-card.width//2,cy-card.height//2),card)
        d.text((W//2,1515),"centré · incliné 3° · bord déchiré blanc + ombre",font=f("DejaVuSans.ttf",26),fill=TERRA,anchor="mm")
    else:
        d.rectangle((60,630,W-60,720),outline=PRUNE,width=4)
        d.text((W//2,675),sub,font=f("DejaVuSerif.ttf",64),fill=ENCRE,anchor="mm")
        d.text((72,634),"note feutre 60-90 px (≈ 1/3 du titre)",font=f("DejaVuSans.ttf",22),fill=PRUNE)
        d.rectangle((60,740,W-60,1500),outline=SAUGE,width=5)
        d.text((W//2,1100),"VISUEL DÉCOUPÉ",font=f("DejaVuSans-Bold.ttf",60),fill=SAUGE,anchor="mm")
        d.text((W//2,1180),"1 seul foyer · 3-4 couches · 740-1500 px",font=f("DejaVuSans.ttf",32),fill=SAUGE,anchor="mm")
    return im
a=panel("RACINE","pas aux ciseaux",False); b=panel("MES RECETTES","",True)
out=Image.new("RGB",(W*2+40,H+120),(255,255,255)); d=ImageDraw.Draw(out)
d.text((W//2,60),"Plans P01-P10 (gabarit standard)",font=f("DejaVuSans-Bold.ttf",40),fill=ENCRE,anchor="mm")
d.text((W+40+W//2,60),"Plan P11 (packshot)",font=f("DejaVuSans-Bold.ttf",40),fill=ENCRE,anchor="mm")
out.paste(a,(0,120)); out.paste(b,(W+40,120)); out.save("r5-maquette-mise-en-page.png")
