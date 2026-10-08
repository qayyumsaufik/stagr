"""Category card images for the home "Explore pieces by category" block, cut 3:2 from the
source shoot. Run: python3 build/categories.py"""
from PIL import Image, ImageOps, ImageEnhance
import os, rawpy
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(SITE), "source-images", "Kignsman")
W1 = f"{SRC}/Waqas-20260907T201410Z-1-001/Waqas"
OUT = f"{SITE}/assets/categories"
# key: (file, focus x, focus y, zoom)  focus = where the 3:2 crop is centred, zoom = fraction of the short side kept
PICKS = {
    "all-wallets": (f"{SRC}/Kignsman/wallet.jpeg", .5, .5, 1.0),
    "bifold":      (f"{SRC}/Regal/KRW_1438.JPG", .5, .55, 1.0),
    "trifold":     (f"{SRC}/Majestic/KRW_1440.JPG", .5, .5, 1.0),
    "minimalist":  (f"{SRC}/Maverick/KRW_1432.JPG", .5, .5, 1.0),
    "long":        (f"{SRC}/Rodeo/KRW_1415.JPG", .5, .5, 1.0),
    "all-belts":   (f"{W1}/DSC08953.JPG", .5, .5, 1.0),
    "nova":        (f"{W1}/DSC09013.JPG", .5, .5, 1.0),
    "outlaw":      (f"{W1}/DSC08977.JPG", .5, .5, 1.0),
    "regent":      (f"{W1}/DSC08997.JPG", .5, .5, 1.0),
    "monarch":     (f"{W1}/DSC08961.JPG", .5, .5, 1.0),
}
def load(f):
    if f.lower().endswith(".arw"):
        with rawpy.imread(f) as r: return Image.fromarray(r.postprocess(use_camera_wb=True, output_bps=8))
    return ImageOps.exif_transpose(Image.open(f)).convert("RGB")
for key, (f, fx, fy, zoom) in PICKS.items():
    im = load(f); W, H = im.size
    short = min(H, W * 2 / 3) * zoom
    ch = int(short); cw = int(short * 3 / 2)
    x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
    c = im.crop((x0, y0, x0 + cw, y0 + ch))
    if "DSC" in f: c = ImageEnhance.Brightness(c).enhance(1.06); c = ImageEnhance.Contrast(c).enhance(1.08)
    for w in (900, 500):
        o = c.copy(); o.thumbnail((w, w), Image.LANCZOS)
        o.save(f"{OUT}/{key}{'' if w == 900 else '-500'}.jpg", quality=84, optimize=True, progressive=True)
    print(key, c.size)

# ---- the three feature tiles under the collection (light cards, photo fills the right/bottom) ----
TILES = {
    "tile-made":  (f"{SRC}/Kignsman/WhatsApp Image 2025-03-11 at 10.20.41 AM (1).jpeg", .6, .5, .9),   # tools + two bifolds on stone
    "tile-bulk":  (f"{W1}/DSC08953.JPG", .5, .55, 1.0),                                         # open bifold with cards, tools
    "tile-note":  (f"{SRC}/Regal/KRW_1441.JPG", .5, .6, .9),                                            # wallet on its gift box
}
for key, (f, fx, fy, zoom) in TILES.items():
    im = load(f); W, H = im.size
    short = min(H, W * 2 / 3) * zoom; ch = int(short); cw = int(short * 3 / 2)
    x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
    c = im.crop((x0, y0, x0 + cw, y0 + ch))
    for w in (1400, 800):
        o = c.copy(); o.thumbnail((w, w), Image.LANCZOS)
        o.save(f"{SITE}/assets/hero/{key}{'' if w == 1400 else '-800'}.jpg", quality=84, optimize=True, progressive=True)
    print(key, c.size)

# ---- collection page heroes and category rows (3:2, 1800 / 900) ----
COLL = {
    "hero-wallets": (f"{SRC}/Majestic/WhatsApp Image 2025-03-11 at 10.20.46 AM.jpeg", .5, .5, 1.0),
    "hero-belts":   (f"{W1}/DSC08966.JPG", .5, .5, 1.0),
    "inside-belts": (f"{W1}/DSC08998.JPG", .5, .5, 1.0),
}
for key, (f, fx, fy, zoom) in COLL.items():
    im = load(f); W, H = im.size
    short = min(H, W * 2 / 3) * zoom; ch = int(short); cw = int(short * 3 / 2)
    x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
    c = im.crop((x0, y0, x0 + cw, y0 + ch))
    if "DSC" in f: c = ImageEnhance.Brightness(c).enhance(1.06); c = ImageEnhance.Contrast(c).enhance(1.08)
    for w in (2000, 1200, 800):
        o = c.copy(); o.thumbnail((w, w), Image.LANCZOS)
        o.save(f"{OUT}/{key}-{w}.jpg", quality=84, optimize=True, progressive=True)
    ph = c.height; pw = int(ph * 3 / 4); x = (c.width - pw) // 2
    o = c.crop((x, 0, x + pw, ph)); o.thumbnail((900, 1200), Image.LANCZOS); o.save(f"{OUT}/{key}-portrait.jpg", quality=84, optimize=True, progressive=True)
    print(key, c.size)
for key, (f, fx, fy, zoom) in PICKS.items():
    im = load(f); W, H = im.size
    short = min(H, W * 2 / 3) * zoom; ch = int(short); cw = int(short * 3 / 2)
    x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
    c = im.crop((x0, y0, x0 + cw, y0 + ch))
    if "DSC" in f: c = ImageEnhance.Brightness(c).enhance(1.06); c = ImageEnhance.Contrast(c).enhance(1.08)
    o = c.copy(); o.thumbnail((1400, 1400), Image.LANCZOS); o.save(f"{OUT}/{key}-1400.jpg", quality=84, optimize=True, progressive=True)
print("done")

# ---- second frame for categories that hold one product (fills the row beside the card) ----
ALT = {
    "trifold-alt": (f"{SRC}/Majestic/WhatsApp Image 2025-03-11 at 10.21.24 AM (1).jpeg", .5, .5, 1.0),
    "nova-alt":    (f"{W1}/DSC09003.JPG", .5, .5, 1.0),
    "outlaw-alt":  (f"{W1}/DSC08978.JPG", .5, .5, 1.0),
    "regent-alt":  (f"{W1}/DSC09007.JPG", .5, .5, 1.0),
    "monarch-alt": (f"{W1}/DSC08972.JPG", .5, .5, 1.0),
}
for key, (f, fx, fy, zoom) in ALT.items():
    im = load(f); W, H = im.size
    short = min(H, W * 2 / 3) * zoom; ch = int(short); cw = int(short * 3 / 2)
    x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
    c = im.crop((x0, y0, x0 + cw, y0 + ch))
    if "DSC" in f: c = ImageEnhance.Brightness(c).enhance(1.06); c = ImageEnhance.Contrast(c).enhance(1.08)
    for w in (1400, 900):
        o = c.copy(); o.thumbnail((w, w), Image.LANCZOS); o.save(f"{OUT}/{key}{'' if w == 900 else '-1400'}.jpg", quality=84, optimize=True, progressive=True)
    print(key, c.size)
