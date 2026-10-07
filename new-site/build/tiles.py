# Compose studio-style hero tiles from the product cutouts: a soft gradient backdrop,
# a contact shadow under each piece, written as JPEG at full size and 800px.
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os
SITE = "/home/user/stagr/new-site"
CUT = f"{SITE}/assets/cutouts"
OUT = f"{SITE}/assets/hero"

def backdrop(w, h, top, bottom, glow=None, glow_at=(0.5, 0.55), glow_r=0.6):
    t = np.array(top, float); b = np.array(bottom, float)
    y = np.linspace(0, 1, h)[:, None, None]
    img = t * (1 - y) + b * y
    img = np.repeat(img, w, axis=1)
    if glow:
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.hypot((xx - glow_at[0] * w) / (glow_r * w), (yy - glow_at[1] * h) / (glow_r * h))
        m = np.clip(1 - d, 0, 1)[..., None] ** 2
        img = img * (1 - 0.55 * m) + np.array(glow, float) * 0.55 * m
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def shadow(canvas, box, strength=120, blur=38, squash=0.22):
    x0, y0, x1, y1 = box
    w = x1 - x0; h = int((y1 - y0) * squash)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cy = y1 - h * 0.45
    d.ellipse([x0 + w * 0.06, cy - h / 2, x1 - w * 0.06, cy + h / 2], fill=(20, 12, 6, strength))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer)

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

# 1. the big tile: belts and a wallet on a warm studio backdrop (portrait)
W, H = 1400, 1750
c = backdrop(W, H, (214, 190, 160), (118, 84, 56), glow=(236, 220, 196), glow_at=(0.5, 0.42), glow_r=0.75)
place(c, "outlaw-1", 420, 1270, 640)
place(c, "monarch-1", 1010, 1320, 620)
place(c, "kingsmann-brown-1", 700, 1500, 560)
save(c, "tile-main")

# 2. wallets tile: three wallets on sage (square)
W, H = 1200, 1200
c = backdrop(W, H, (156, 164, 142), (92, 100, 82), glow=(196, 202, 180), glow_at=(0.5, 0.45), glow_r=0.7)
place(c, "regal-black-1", 420, 660, 500, rot=4)
place(c, "kingsmann-brown-1", 770, 790, 540, rot=-3)
place(c, "maverick-brown-1", 330, 960, 320)
save(c, "tile-wallets")

# 3. belts tile: two coils on terracotta (square)
c = backdrop(W, H, (196, 136, 104), (116, 66, 44), glow=(224, 176, 140), glow_at=(0.5, 0.45), glow_r=0.7)
place(c, "regent-1", 430, 640, 600)
place(c, "nova-1", 790, 880, 600)
save(c, "tile-belts")
