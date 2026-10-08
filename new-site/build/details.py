"""Circular zoom-in details for the home "Inside" section, cropped from the same cutouts
the stage shows. Writes assets/details/<piece>-<pos>.webp (360px, round alpha).
Run from new-site/: python3 build/details.py"""
from PIL import Image, ImageDraw, ImageFilter
import os
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{SITE}/assets/details"; os.makedirs(OUT, exist_ok=True)
# piece: source cutout, then pos: (centre x%, centre y%, radius as % of width)
PICKS = {
    "wallet": ("kingsmann-brown-1", {"tl": (50, 9, 8), "bl": (30, 55, 11), "tr": (89, 13, 8), "br": (77, 75, 11)}),
    "belt":   ("monarch-1", {"tl": (45, 27, 11), "bl": (18, 65, 13), "tr": (80, 42, 11), "br": (55, 62, 11)}),
}
SIZE = 360
for piece, (src, spots) in PICKS.items():
    im = Image.open(f"{SITE}/assets/cutouts/{src}.webp").convert("RGBA"); W, H = im.size
    for pos, (cx, cy, r) in spots.items():
        rp = int(W * r / 100); x, y = int(W * cx / 100), int(H * cy / 100)
        box = (x - rp, y - rp, x + rp, y + rp)
        c = im.crop(box).resize((SIZE, SIZE), Image.LANCZOS)
        # the cutout's transparent background shows as the section colour under the ring; fill it ink
        bg = Image.new("RGBA", (SIZE, SIZE), (26, 27, 29, 255)); bg.alpha_composite(c)
        m = Image.new("L", (SIZE, SIZE), 0); ImageDraw.Draw(m).ellipse([2, 2, SIZE - 3, SIZE - 3], fill=255); m = m.filter(ImageFilter.GaussianBlur(.8))
        bg.putalpha(m); bg.save(f"{OUT}/{piece}-{pos}.webp", "WEBP", quality=90, method=6)
    print(piece, "ok")
