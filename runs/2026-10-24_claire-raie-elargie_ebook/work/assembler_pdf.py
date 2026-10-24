# Assemble les pages retenues en deux PDF : web (léger, envoi en message privé) et HQ.
import pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
pages = sorted((R / "retenues" / "pages").glob("*.png"))
W, H = 1086, 1448
imgs = [Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS) for p in pages]
web = [im.resize((900, 1200), Image.LANCZOS) for im in imgs]
web[0].save(R / "retenues" / "raie-elargie-web.pdf", save_all=True, append_images=web[1:], quality=80, optimize=True, resolution=150)
imgs[0].save(R / "retenues" / "raie-elargie-hq.pdf", save_all=True, append_images=imgs[1:], quality=95, resolution=200)
print(len(pages), "pages")
