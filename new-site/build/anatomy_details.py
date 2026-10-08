"""Round detail crops for the home "Anatomy" section, cut from the product cutouts.
Writes assets/details/anat-<piece>-<n>.webp (360px, round alpha on bone).
Run from new-site/: python3 build/anatomy_details.py"""
from PIL import Image, ImageDraw, ImageFilter
import os
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{SITE}/assets/details"; os.makedirs(OUT, exist_ok=True)
# piece: [(source cutout, centre x%, centre y%, radius % of width)] in callout order 1..9
SPEC = {
    "belt": [("monarch-1", 60, 20, 9), ("monarch-2", 60, 70, 6), ("monarch-1", 80, 42, 9),
             ("monarch-1", 18, 66, 12), ("monarch-1", 55, 62, 10), ("monarch-2", 82, 78, 7),
             ("monarch-2", 30, 80, 8), ("monarch-1", 93, 32, 7), ("monarch-2", 62, 22, 7)],
    "wallet": [("kingsmann-brown-1", 40, 40, 9), ("kingsmann-brown-1", 50, 9, 8), ("kingsmann-brown-1", 89, 13, 8),
               ("kingsmann-brown-1", 8, 50, 6), ("kingsmann-brown-1", 77, 75, 10), ("kingsmann-brown-1", 30, 60, 9),
               ("kingsmann-brown-2", 30, 25, 9), ("kingsmann-brown-2", 50, 30, 8), ("kingsmann-brown-2", 86, 72, 8)],
}
SIZE = 360
for piece, spots in SPEC.items():
    for n, (src, cx, cy, r) in enumerate(spots, 1):
        im = Image.open(f"{SITE}/assets/cutouts/{src}.webp").convert("RGBA"); W, H = im.size
        rp = int(W * r / 100); x, y = int(W * cx / 100), int(H * cy / 100)
        c = im.crop((x - rp, y - rp, x + rp, y + rp)).resize((SIZE, SIZE), Image.LANCZOS)
        bg = Image.new("RGBA", (SIZE, SIZE), (239, 237, 230, 255)); bg.alpha_composite(c)
        m = Image.new("L", (SIZE, SIZE), 0); ImageDraw.Draw(m).ellipse([2, 2, SIZE - 3, SIZE - 3], fill=255); m = m.filter(ImageFilter.GaussianBlur(.8))
        bg.putalpha(m); bg.save(f"{OUT}/anat-{piece}-{n}.webp", "WEBP", quality=90, method=6)
    print(piece, len(spots))
