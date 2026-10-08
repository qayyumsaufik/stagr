"""Real photographs for the product pages: two or three frames per product from the
source shoot, cut 4:3, written to assets/pdp/<id>-<n>.jpg (1600) and -800.
Run from new-site/: python3 build/pdp_photos.py"""
from PIL import Image, ImageOps, ImageEnhance
import os, rawpy
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(SITE), "source-images", "Kignsman")
W1 = f"{SRC}/Waqas-20260907T201410Z-1-001/Waqas"
OUT = f"{SITE}/assets/pdp"
os.makedirs(OUT, exist_ok=True)
WA = lambda folder, t: f"{SRC}/{folder}/WhatsApp Image 2025-03-11 at {t} AM.jpeg"
# id: [(file, focus x, focus y), ...]  first = the scene, second = open / in the hand, third = detail
PICKS = {
    "kingsmann": [(f"{SRC}/Kignsman/KRW_1447.JPG", .5, .5), (f"{SRC}/Kignsman/wallet.jpeg", .5, .5), (WA("Kignsman", "10.20.42"), .5, .5)],
    "majestic":  [(f"{SRC}/Majestic/KRW_1440.JPG", .5, .5), (WA("Majestic", "10.20.46"), .5, .5), (WA("Majestic", "10.20.44") .replace(" AM.jpeg", " AM (1).jpeg"), .5, .5)],
    "maverick":  [(f"{SRC}/Maverick/KRW_1432.JPG", .5, .5), (WA("Maverick", "10.20.33"), .5, .5), (WA("Maverick", "10.21.08"), .5, .5)],
    "purefold":  [(f"{SRC}/Purefold/KRW_1449.JPG", .5, .5), (WA("Purefold", "10.20.59").replace(" AM.jpeg", " AM (1).jpeg"), .5, .5), (f"{SRC}/Purefold/KRW_1452.JPG", .5, .5)],
    "regal":     [(f"{SRC}/Regal/KRW_1439.JPG", .5, .5), (WA("Regal", "10.20.34").replace(" AM.jpeg", " AM (1).jpeg"), .5, .5), (f"{SRC}/Regal/KRW_1437.JPG", .5, .5)],
    "rodeo":     [(f"{SRC}/Rodeo/KRW_1415.JPG", .5, .5), (WA("Rodeo", "10.21.13").replace(" AM.jpeg", " AM (2).jpeg"), .5, .5), (WA("Rodeo", "10.21.20"), .5, .5)],
    "upbuck":    [(f"{SRC}/upbuck/KRW_1425.JPG", .5, .5), (WA("upbuck", "10.20.56").replace(" AM.jpeg", " AM (1).jpeg"), .5, .5), (WA("upbuck", "10.20.51"), .5, .5)],
    "nova":      [(f"{W1}/DSC09013.JPG", .5, .55), (f"{W1}/DSC09000.JPG", .5, .5), (f"{W1}/DSC08999.JPG", .5, .5)],
    "outlaw":    [(f"{W1}/DSC08977.JPG", .5, .5), (f"{W1}/DSC08978.JPG", .5, .5), (f"{W1}/DSC08959.JPG", .5, .5)],
    "regent":    [(f"{W1}/DSC08997.JPG", .5, .5), (f"{W1}/DSC09007.JPG", .5, .5), (f"{W1}/DSC08995.JPG", .5, .5)],
    "monarch":   [(f"{W1}/DSC08961.JPG", .5, .5), (f"{W1}/DSC08966.JPG", .5, .5), (f"{W1}/DSC08965.JPG", .5, .5)],
}
def load(f):
    if f.lower().endswith(".arw"):
        with rawpy.imread(f) as r: return Image.fromarray(r.postprocess(use_camera_wb=True, output_bps=8))
    return ImageOps.exif_transpose(Image.open(f)).convert("RGB")
for pid, frames in PICKS.items():
    for n, (f, fx, fy) in enumerate(frames, 1):
        im = load(f); W, H = im.size
        short = min(H, W * 3 / 4); ch = int(short); cw = int(short * 4 / 3)
        x0 = int(min(max(fx * W - cw / 2, 0), W - cw)); y0 = int(min(max(fy * H - ch / 2, 0), H - ch))
        c = im.crop((x0, y0, x0 + cw, y0 + ch))
        if "DSC" in f: c = ImageEnhance.Brightness(c).enhance(1.06); c = ImageEnhance.Contrast(c).enhance(1.08)
        for w in (1600, 800):
            o = c.copy(); o.thumbnail((w, w), Image.LANCZOS)
            o.save(f"{OUT}/{pid}-{n}{'' if w == 1600 else '-800'}.jpg", quality=84, optimize=True, progressive=True)
    print(pid, len(frames))
