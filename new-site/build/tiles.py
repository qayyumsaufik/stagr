"""Compose the home hero tiles from the product cutouts: leather-tone backdrops with a
faint grain and vignette, a contact shadow under each piece. Writes assets/hero/tile-*.jpg
and an 800px variant. Run: python3 build/tiles.py"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUT = f"{SITE}/assets/cutouts"
OUT = f"{SITE}/assets/hero"
rng = np.random.default_rng(7)

def backdrop(w, h, top, bottom, glow=None, glow_at=(0.5, 0.55), glow_r=0.6, grain=7, vignette=0.28):
    t = np.array(top, float); b = np.array(bottom, float)
    y = np.linspace(0, 1, h)[:, None, None]
    img = np.repeat(t * (1 - y) + b * y, w, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]
    if glow:
        d = np.hypot((xx - glow_at[0] * w) / (glow_r * w), (yy - glow_at[1] * h) / (glow_r * h))
        m = np.clip(1 - d, 0, 1)[..., None] ** 2
        img = img * (1 - 0.5 * m) + np.array(glow, float) * 0.5 * m
    # vignette: corners fall off like a lit studio sweep
    d = np.hypot((xx - w / 2) / (0.78 * w), (yy - h * 0.5) / (0.85 * h))
    img = img * (1 - vignette * np.clip(d - 0.55, 0, 1)[..., None] ** 1.5)
    # grain: the faint tooth of full-grain hide
    img = img + rng.normal(0, grain, (h, w, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def shadow(canvas, box, strength=135, blur=40, squash=0.2):
    x0, y0, x1, y1 = box
    w = x1 - x0; h = int((y1 - y0) * squash)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cy = y1 - h * 0.45
    d.ellipse([x0 + w * 0.06, cy - h / 2, x1 - w * 0.06, cy + h / 2], fill=(18, 10, 4, strength))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))

def place(canvas, name, cx, cy, width, rot=0):
    im = Image.open(f"{CUT}/{name}.webp").convert("RGBA")
    s = width / im.width
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    x0 = int(cx - im.width / 2); y0 = int(cy - im.height / 2)
    a = np.array(im)[..., 3]; ys, xs = np.where(a > 40)
    shadow(canvas, (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()))
    canvas.alpha_composite(im, (x0, y0))

def save(canvas, name):
    rgb = canvas.convert("RGB")
    rgb.save(f"{OUT}/{name}.jpg", quality=86, optimize=True, progressive=True)
    small = rgb.copy(); small.thumbnail((800, 800), Image.LANCZOS)
    small.save(f"{OUT}/{name}-800.jpg", quality=84, optimize=True, progressive=True)
    print(name, rgb.size)

# main tile: saddle-tan sweep, two belts and a wallet low in the frame (portrait 4:5)
W, H = 1400, 1750
c = backdrop(W, H, (176, 132, 92), (84, 52, 30), glow=(222, 190, 150), glow_at=(0.5, 0.38), glow_r=0.8)
place(c, "outlaw-1", 430, 1200, 640)
place(c, "monarch-1", 1000, 1250, 620)
place(c, "kingsmann-brown-1", 700, 1420, 560)
save(c, "tile-main")

# wallets tile: dark coffee, warm rim light from above (portrait 3:4)
W, H = 1050, 1400
c = backdrop(W, H, (82, 56, 40), (28, 20, 16), glow=(150, 104, 70), glow_at=(0.5, 0.42), glow_r=0.75, grain=5)
place(c, "regal-black-1", 400, 760, 520, rot=5)
place(c, "kingsmann-brown-1", 690, 900, 560, rot=-4)
place(c, "maverick-brown-1", 300, 1090, 300)
save(c, "tile-wallets")

# belts tile: bone sand, ink text on top (portrait 3:4)
c = backdrop(W, H, (232, 222, 204), (186, 166, 136), glow=(246, 240, 228), glow_at=(0.5, 0.4), glow_r=0.8, grain=5, vignette=0.18)
place(c, "monarch-1", 520, 760, 720)
place(c, "nova-1", 640, 1060, 640)
save(c, "tile-belts")
