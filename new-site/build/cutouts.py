"""Re-cut every studio photo with rembg (isnet-general-use), crop to the subject and write
assets/cutouts/<name>.webp plus a 600px variant. Run: pip install rembg onnxruntime; python3 build/cutouts.py"""
import glob, os, json, sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
SITE = "/home/user/stagr/new-site"
prods = json.load(open(f"{SITE}/data/products.json"))["products"]
belt_colour = {p["id"]: p["defaultColour"].lower() for p in prods if p["line"] == "belt"}
sess = new_session("isnet-general-use")
masters = sorted(f for f in glob.glob(f"{SITE}/assets/products/*.jpg") if not f.endswith("-800.jpg"))
done = 0
for f in masters:
    base = os.path.basename(f)[:-4]
    pid = base.split("-")[0]
    name = base.replace(f"-{belt_colour[pid]}-", "-") if pid in belt_colour else base
    im = Image.open(f).convert("RGB")
    out = remove(im, session=sess).convert("RGBA")
    a = np.array(out)
    al = a[..., 3].astype(np.float32)
    # kill faint residue, keep soft edges, then crop with a 2% margin
    al[al < 10] = 0
    a[..., 3] = al.astype(np.uint8)
    ys, xs = np.where(a[..., 3] > 0)
    if len(xs) == 0: print("EMPTY", base); continue
    pad = int(max(a.shape[:2]) * 0.02)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad + 1)
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad + 1)
    crop = Image.fromarray(a[y0:y1, x0:x1])
    crop.save(f"{SITE}/assets/cutouts/{name}.webp", "WEBP", quality=90, method=6)
    small = crop.copy(); small.thumbnail((600, 600), Image.LANCZOS)
    small.save(f"{SITE}/assets/cutouts/{name}-600.webp", "WEBP", quality=88, method=6)
    done += 1
    print(name, crop.size, flush=True)
print("done", done)
