"""Hero scene: the open Regal bifold and the coiled Monarch belt (the real cutouts) on a dark
honed stone slab, warm key light from the upper left, soft reflection, deep charcoal to warm
brown background, left 40% kept clear. Writes assets/hero/scene-{2400,1600,1000}.jpg and
scene-portrait.jpg. Run from new-site/: python3 build/hero_scene.py"""
import numpy as np, scipy.ndimage as ndi, os
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = "/tmp/claude-0/-home-user-stagr/b0e31eb3-8a4f-5a34-82c5-b9945756f249/scratchpad/"
W, H = 2400, 1350; HOR = int(H * .50)
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); u = xx / W; v = yy / H

# ---- background: charcoal to warm brown, lit from the upper left, warm pool right of centre ----
char = np.array([24, 23, 23], np.float32); brown = np.array([62, 38, 26], np.float32)
t = np.clip((u - .25) * 1.1 + (v - .2) * .5, 0, 1)
bg = char[None, None] * (1 - t[..., None]) + brown[None, None] * t[..., None]
key = np.exp(-(((u - .62) / .34) ** 2 + ((v - .38) / .30) ** 2))[..., None] * np.array([70, 44, 24], np.float32)[None, None]
bg = bg + key
bg = ndi.gaussian_filter(bg, (40, 40, 0))

# ---- slab: honed stone with fine grain and faint veins, perspective falloff ----
grain = ndi.gaussian_filter(rng.normal(0, 1, (H, W)).astype(np.float32), 1.2) * 6
veins = ndi.gaussian_filter(rng.normal(0, 1, (H // 8, W // 8)).astype(np.float32), 6)
veins = np.asarray(Image.fromarray(veins).resize((W, H), Image.BICUBIC)) * 9
slab = np.array([44, 42, 41], np.float32)[None, None] + (grain + veins)[..., None] * np.array([1, .98, .95], np.float32)[None, None]
depth = np.clip((v - HOR / H) / (1 - HOR / H), 0, 1)                       # 0 at the back edge, 1 at the front
slab *= (0.55 + 0.75 * depth)[..., None]                                      # the front is nearer the light
pool = np.exp(-(((u - .60) / .30) ** 2 + ((depth - .35) / .55) ** 2))[..., None] * np.array([58, 40, 24], np.float32)[None, None]
slab += pool
# the back edge of the slab catches the light as a thin line
edge = np.exp(-((yy - HOR) / 2.2) ** 2) * np.exp(-(((u - .6) / .5) ** 2)) * 70
slab += edge[..., None]
img = np.where((yy >= HOR)[..., None], slab, bg)
# vignette
vig = 1 - 0.55 * np.clip(((u - .5) / .62) ** 2 + ((v - .5) / .70) ** 2, 0, 1)
img *= vig[..., None]
base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
base = base.filter(ImageFilter.GaussianBlur(0.6))

# ---- the products ----
def load(p): return Image.open(p).convert("RGBA")
wallet = load(SP + "wallet-open-cut.png"); belt = load(f"{SITE}/assets/cutouts/inside-belt.webp")
def fit(im, w): return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
def relight(im, strength=.22):
    """warm key from the upper left: brighter top-left, cooler and darker bottom-right"""
    a = np.array(im).astype(np.float32); h, w = a.shape[:2]; gy, gx = np.mgrid[0:h, 0:w]
    g = 1 + strength * (0.5 - (gx / w * .6 + gy / h * .4))
    a[..., :3] = np.clip(a[..., :3] * g[..., None] * np.array([1.03, .99, .95])[None, None], 0, 255)
    return Image.fromarray(a.astype(np.uint8))
def shadow(canvas, im, x, y, spread=.05, alpha=190, blur=28, lift=0):
    al = np.array(im)[..., 3]; ys, xs = np.where(al > 60); bx0, bx1, by1 = x + xs.min(), x + xs.max(), y + ys.max()
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh); hh = int((bx1 - bx0) * spread) + 6
    d.ellipse([bx0 - 10, by1 - hh - lift, bx1 + 10, by1 + hh - lift], fill=(8, 5, 3, alpha))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
def reflect(canvas, im, x, y, strength=.28, fade=.9):
    al = np.array(im)[..., 3]; ys = np.where(al.max(1) > 60)[0]; bottom = y + ys.max()
    r = im.transpose(Image.FLIP_TOP_BOTTOM); r = r.crop((0, im.height - 1 - ys.max(), im.width, im.height))
    rr = np.array(r).astype(np.float32); h = rr.shape[0]
    g = np.clip(1 - np.arange(h) / (h * fade), 0, 1) ** 1.6 * strength
    rr[..., 3] *= g[:, None]; rr[..., :3] *= .85
    rim = Image.fromarray(rr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    canvas.alpha_composite(rim, (x, bottom + 2))

canvas = base.copy()
# wallet right of centre, standing on the slab
wal = relight(fit(wallet, int(W * .34))); wx, wy = int(W * .58), int(H * .79) - wal.height
shadow(canvas, wal, wx, wy, spread=.045, alpha=200, blur=30)
reflect(canvas, wal, wx, wy, strength=.26)
canvas.alpha_composite(wal, (wx, wy))
# belt coiled in front, buckle catching the light, overlapping the wallet's corner
bel = relight(fit(belt, int(W * .33)), .18); bx, by = int(W * .42), int(H * .90) - bel.height
shadow(canvas, bel, bx, by, spread=.06, alpha=210, blur=26)
reflect(canvas, bel, bx, by, strength=.22, fade=.8)
canvas.alpha_composite(bel, (bx, by))

out = canvas.convert("RGB")
out = ImageEnhance.Contrast(out).enhance(1.06)
for w in (2400, 1600, 1000):
    o = out.copy(); o.thumbnail((w, w), Image.LANCZOS); o.save(f"{SITE}/assets/hero/scene-{w}.jpg", quality=88, optimize=True, progressive=True)
pw = int(H * 3 / 4); x = int(W * .62 - pw / 2); x = max(0, min(x, W - pw))
p = out.crop((x, 0, x + pw, H)); p.thumbnail((1000, 1334), Image.LANCZOS); p.save(f"{SITE}/assets/hero/scene-portrait.jpg", quality=86, optimize=True, progressive=True)
pv = out.copy(); pv.thumbnail((1400, 1400)); pv.save(SP + "shots/scene.jpg", quality=85); print("ok")
