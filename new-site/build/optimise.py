#!/usr/bin/env python3
"""Optimise product and lifestyle images in new-site/assets.

Every image becomes a JPEG at two sizes: the master (long edge <= 1600px)
and a small variant (-800, long edge <= 800px) for cards/thumbnails.
products.json is rewritten so src points at the master and srcSmall at the
small variant. Safe to re-run: the source copies in assets/*/ are replaced
only after the first run (originals remain in the repo root).
"""
import json, os
from PIL import Image, ImageOps

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(SITE, "data", "products.json")
ROOT = os.path.dirname(SITE)


def out_paths(src):
    base, _ = os.path.splitext(src)
    return base + ".jpg", base + "-800.jpg"


def convert(source_repo_path, master, small):
    im = Image.open(os.path.join(ROOT, source_repo_path))
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    for path, edge, q in ((master, 1600, 82), (small, 800, 80)):
        c = im.copy()
        c.thumbnail((edge, edge), Image.LANCZOS)
        c.save(os.path.join(SITE, path), "JPEG", quality=q, optimize=True, progressive=True)
    return im.size


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = json.load(f)
    seen = {}
    total_before = total_after = 0
    for p in doc["products"]:
        for im in p["images"] + p["lifestyleImages"]:
            src = im["src"]
            master, small = out_paths(src)
            if src not in seen:
                before = os.path.getsize(os.path.join(ROOT, im["source"]))
                w, h = convert(im["source"], master, small)
                after = os.path.getsize(os.path.join(SITE, master))
                total_before += before; total_after += after
                mw, mh = Image.open(os.path.join(SITE, master)).size
                seen[src] = (master, small, mw, mh)
                if src != master and os.path.exists(os.path.join(SITE, src)):
                    os.remove(os.path.join(SITE, src))
            master, small, mw, mh = seen[src]
            im["src"], im["srcSmall"], im["width"], im["height"] = master, small, mw, mh
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(f"{len(seen)} images, {total_before//1024} KB -> {total_after//1024} KB (masters)")


if __name__ == "__main__":
    main()
