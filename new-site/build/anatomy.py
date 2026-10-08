"""High-resolution cutouts for the home anatomy section, cut from the full-size shoot
frames with rembg. Writes assets/anatomy/{wallet,belt}.webp (2400) and -1200.
Run from new-site/: python3 build/anatomy.py [--preview]"""
import os, sys
import numpy as np, scipy.ndimage as ndi
from PIL import Image, ImageOps
from rembg import remove, new_session
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(SITE), "source-images", "Kignsman")
W1 = f"{SRC}/Waqas-20260907T201410Z-1-001/Waqas"
OUT = f"{SITE}/assets/anatomy"; os.makedirs(OUT, exist_ok=True)
sess = new_session("isnet-general-use")
# key: (file, crop box as fractions l,t,r,b, drop dark islands inside the subject)
PICKS = {
    "wallet": (f"{SRC}/Kignsman/KRW_1447.JPG", (.26, .20, .72, .78), False),
    "belt":   (f"{SITE}/assets/hero/slide-belts-2400.jpg", (.26, .22, .90, .88), False),   # the supplied coiled tan belt
}
def cut(key, f, box, drop_dark):
    im = ImageOps.exif_transpose(Image.open(f)).convert("RGB"); W, H = im.size
    c = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    out = np.array(remove(c, session=sess).convert("RGBA"))
    al = out[..., 3].astype(np.float32); al[al < 28] = 0
    mask = al > 40
    # keep the biggest connected piece only (drops loose shells, beans and threads)
    lab, n = ndi.label(ndi.binary_opening(mask, iterations=2))
    if n > 1:
        sizes = ndi.sum(mask, lab, range(1, n + 1)); keep = lab == (1 + int(np.argmax(sizes)))
        keep = ndi.binary_dilation(keep, iterations=6); al[~keep] = 0
    if drop_dark:
        # coffee beans inside the coil: dark, desaturated-brown blobs; the belt is tan and bright
        rgb = out[..., :3].astype(np.float32) / 255; v = rgb.max(2); s = (v - rgb.min(2)) / np.maximum(v, 1e-3)
        beans = (v < 0.30) & (al > 0)
        beans = ndi.binary_opening(beans, iterations=2); beans = ndi.binary_dilation(beans, iterations=3)
        al[beans] = 0
    out[..., 3] = al.astype(np.uint8)
    ys, xs = np.where(out[..., 3] > 0); pad = int(max(out.shape[:2]) * .03)
    x0, x1 = max(0, xs.min() - pad), min(out.shape[1], xs.max() + pad + 1); y0, y1 = max(0, ys.min() - pad), min(out.shape[0], ys.max() + pad + 1)
    crop = Image.fromarray(out[y0:y1, x0:x1]); print(key, crop.size)
    return crop
for key, (f, box, dd) in PICKS.items():
    crop = cut(key, f, box, dd)
    if "--preview" in sys.argv:
        bg = Image.new("RGBA", crop.size, (255, 255, 255, 255)); bg.alpha_composite(crop); bg = bg.convert("RGB"); bg.thumbnail((1200, 1200)); bg.save(f"{SITE}/build/_composite-debug/anat-{key}.jpg", quality=85); continue
    big = crop.copy(); big.thumbnail((2400, 2400), Image.LANCZOS); big.save(f"{OUT}/{key}.webp", "WEBP", quality=90, method=6)
    small = crop.copy(); small.thumbnail((1200, 1200), Image.LANCZOS); small.save(f"{OUT}/{key}-1200.webp", "WEBP", quality=88, method=6)
print("done")
