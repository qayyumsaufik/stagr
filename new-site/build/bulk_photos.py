"""Photographs for the bulk-orders page, cut from the full-size source frames.
Run from new-site/: python3 build/bulk_photos.py"""
from PIL import Image, ImageOps, ImageEnhance
import os, rawpy
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(SITE), "source-images", "Kignsman")
W1 = f"{SRC}/Waqas-20260907T201410Z-1-001/Waqas"
OUT = f"{SITE}/assets/bulk"
os.makedirs(OUT, exist_ok=True)
WA = lambda folder, t: f"{SRC}/{folder}/WhatsApp Image 2025-03-11 at {t}.jpeg"
# key: (file, focus x, focus y, aspect w/h, widths)
PICKS = {
    "hero":      (f"{W1}/DSC08957.JPG", .5, .5, 3 / 2, (2400, 1600, 1000)),
    "lineup":    (f"{W1}/DSC08955.JPG", .5, .5, 4 / 5, (1400, 800)),
    "gifts":     (f"{SRC}/Regal/KRW_1441.JPG", .5, .55, 4 / 3, (1600, 800)),
    "teams":     (f"{W1}/DSC08953.JPG", .5, .5, 4 / 3, (1600, 800)),
    "events":    (f"{SRC}/Rodeo/KRW_1416.JPG", .5, .5, 4 / 3, (1600, 800)),
    "mark":      (f"{W1}/DSC08962.JPG", .5, .5, 4 / 3, (1600, 800)),
    "boxed":     (f"{SRC}/Majestic/KRW_1440.JPG", .5, .5, 4 / 3, (1600, 800)),
    "mix":       (WA("Kignsman", "10.20.41 AM (1)"), .55, .5, 4 / 3, (1600, 800)),
}
def load(f):
    if f.lower().endswith(".arw"):
        with rawpy.imread(f) as r: return Image.fromarray(r.postprocess(use_camera_wb=True, output_bps=8))
    return ImageOps.exif_transpose(Image.open(f)).convert("RGB")
for key, (f, fx, fy, ar, widths) in PICKS.items():
    im = load(f); W, H = im.size
    cw = min(W, H * ar); ch = cw / ar
    cw, ch = int(cw), int(ch)
    x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
    c = im.crop((x0, y0, x0 + cw, y0 + ch))
    if "DSC" in f: c = ImageEnhance.Brightness(c).enhance(1.06); c = ImageEnhance.Contrast(c).enhance(1.08)
    for w in widths:
        o = c.copy(); o.thumbnail((w, w), Image.LANCZOS)
        o.save(f"{OUT}/{key}-{w}.jpg", quality=86, optimize=True, progressive=True)
    if key == "hero":
        ph = c.height; pw = int(ph * 3 / 4); x = (c.width - pw) // 2
        o = c.crop((x, 0, x + pw, ph)); o.thumbnail((1000, 1334), Image.LANCZOS); o.save(f"{OUT}/hero-portrait.jpg", quality=86, optimize=True, progressive=True)
    print(key, c.size)
