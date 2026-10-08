"""Cutouts for the home "Inside" stage from the supplied hero frames (the stag-marked
bifold and the coiled tan belt). Writes assets/cutouts/inside-{wallet,belt}.webp.
Run from new-site/: python3 build/inside_cuts.py"""
import os, numpy as np, scipy.ndimage as ndi
from PIL import Image
from rembg import remove, new_session
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sess = new_session("isnet-general-use")
PICKS = {"wallet": (f"{SITE}/assets/hero/slide-wallet-2000.jpg", (.40, .16, .86, .86)), "belt": (f"{SITE}/assets/hero/slide-belts-2400.jpg", (.26, .22, .90, .88))}
for key, (f, box) in PICKS.items():
    im = Image.open(f).convert("RGB"); W, H = im.size
    c = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    out = np.array(remove(c, session=sess).convert("RGBA")); al = out[..., 3].astype(np.float32); al[al < 28] = 0
    mask = al > 40; lab, n = ndi.label(ndi.binary_opening(mask, iterations=2))
    if n > 1:
        sizes = ndi.sum(mask, lab, range(1, n + 1)); keep = ndi.binary_dilation(lab == (1 + int(np.argmax(sizes))), iterations=6); al[~keep] = 0
    out[..., 3] = al.astype(np.uint8)
    ys, xs = np.where(out[..., 3] > 0); pad = int(max(out.shape[:2]) * .03)
    crop = Image.fromarray(out[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad])
    crop.save(f"{SITE}/assets/cutouts/inside-{key}.webp", "WEBP", quality=90, method=6)
    small = crop.copy(); small.thumbnail((600, 600)); small.save(f"{SITE}/assets/cutouts/inside-{key}-600.webp", "WEBP", quality=88, method=6)
    print(key, crop.size)
