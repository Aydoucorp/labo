# Bulle « Réponse au commentaire » façon TikTok, calée sur la capture de référence (537 px de large -> 1080 px, x2,011)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
FD = "/home/user/labo/runs/2026-10-24_claire-tempes-commentaire_ugc-humain/work/polices/"
K = 2.011
def S(v): return int(round(v * K))
def bulle(fond, prenom, texte_lignes, photo=None, x=47, y=273, w=220):
    im = Image.open(fond).convert("RGBA")
    f_rep = ImageFont.truetype(FD + "TikTokSans-400.ttf", S(8.6))
    f_txt = ImageFont.truetype(FD + "TikTokSans-700.ttf", S(11.8))
    pad_l, top = 41, 16  # début du texte (après la photo), haut de la 1re ligne, en px de la capture
    lh = 16.4
    h = top + 14 + lh * len(texte_lignes) + 8
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # ombre douce
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.rounded_rectangle([S(x), S(y + 1), S(x + w), S(y + h + 1)], radius=S(7), fill=(0, 0, 0, 60))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(S(3))))
    d.rounded_rectangle([S(x), S(y), S(x + w), S(y + h)], radius=S(7), fill=(255, 255, 255, 255))
    # queue en bas à gauche
    d.polygon([(S(x + 4), S(y + h - 6)), (S(x + 15), S(y + h - 1)), (S(x + 1), S(y + h + 8))], fill=(255, 255, 255, 255))
    # photo de profil
    cx, cy, r = x + 21, y + 38, 11
    if photo:
        p = Image.open(photo).convert("RGB")
        c = min(p.size); p = p.crop(((p.width - c) // 2, (p.height - c) // 2, (p.width + c) // 2, (p.height + c) // 2)).resize((S(2 * r), S(2 * r)), Image.LANCZOS)
        m = Image.new("L", p.size, 0); ImageDraw.Draw(m).ellipse([0, 0, p.size[0] - 1, p.size[1] - 1], fill=255)
        lay.paste(p, (S(cx - r), S(cy - r)), m)
    else:
        d.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill=(205, 190, 180, 255))
    d.text((S(x + pad_l), S(y + top)), f"Réponse au commentaire de {prenom}", font=f_rep, fill=(110, 110, 110, 255), anchor="ls")
    for i, l in enumerate(texte_lignes):
        d.text((S(x + pad_l), S(y + top + 14 + lh * (i + 1) - 4)), l, font=f_txt, fill=(22, 22, 22, 255), anchor="ls")
    return Image.alpha_composite(im, lay)
if __name__ == "__main__":
    out = bulle("fond.png", "Sylvie", ["J'ai perdu beaucoup de", "cheveux partout sur ma tête", "et surtout sur mes tempes"], photo=sys.argv[1] if len(sys.argv) > 1 else None)
    out.convert("RGB").save("maquette-bulle.png")
    out.convert("RGB").crop((60, 500, 620, 860)).save("maquette-bulle-zoom.png")
