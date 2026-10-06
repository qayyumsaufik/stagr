#!/usr/bin/env python3
"""Assemble the Stagr site (v2, STILL-style chrome).

    python3 build/build.py [page ...]     # writes new-site/*.html

Each page module in build/pages/ exposes `render(ctx) -> dict | [dict]` with
keys file, title, description, css, body, js and optional flags
(loader, header_dark, nav). base.css is inlined so every page is
self-contained for CSS; js/stagr.js is shared.
"""
import importlib.util, json, os, sys, html as html_mod

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "data")

GSAP_VER = "3.13.0"
CDN = {k: f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{GSAP_VER}/{k}.min.js" for k in ("gsap", "ScrollTrigger", "SplitText", "DrawSVGPlugin", "Flip", "Observer")}
CDN["lenis"] = "https://unpkg.com/lenis@1.3.4/dist/lenis.min.js"

BLOOM = {"Bifold": "#D9B07A", "Trifold": "#CDA373", "Minimalist": "#DABF9A", "Long": "#C8976A", None: "#C9B290"}
SWATCH = {"Brown": "#6E4328", "Black": "#1A1512", "Tan": "#B0773F", "Coffee": "#4A3024"}


def load_json(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html_mod.escape(str(s), quote=True)


def cutouts_for(p):
    """Transparent cutout files for a product, per colour, in display order."""
    out = []
    for im in p["images"]:
        base = os.path.basename(im["src"]).replace("-800", "").rsplit(".", 1)[0]
        # studio file names: <id>-<colour>-<n> for wallets, <id>-<n> for belts
        name = base if p["line"] == "wallet" else base.replace(f"-{p['defaultColour'].lower()}-", "-")
        src = f"assets/cutouts/{name}.webp"
        if os.path.exists(os.path.join(SITE, src)):
            out.append({"colour": im["colour"].capitalize(), "src": src, "small": src.replace(".webp", "-600.webp")})
    return out


def compact_products(products):
    out = []
    for p in products:
        q = {k: v for k, v in p.items() if k not in ("flags", "details", "materials", "lifestyleImages", "images", "badges")}
        q["cutouts"] = cutouts_for(p)
        q["bloom"] = BLOOM.get(p["style"])
        q["lifestyle"] = [{k: v for k, v in im.items() if k in ("src", "srcSmall", "alt", "width", "height")} for im in p["lifestyleImages"]]
        out.append(q)
    return out


def inline_data(ctx):
    b = ctx["brand"]
    data = {"products": compact_products(ctx["products"]),
            "brand": {"freeDeliveryThreshold": b["shipping"]["freeDeliveryThreshold"], "deliveryFee": b["shipping"]["deliveryFee"], "whatsapp": b["contact"]["whatsapp"]["link"]}}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


ICON = {
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    "arrow": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "arrow-l": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    "arrow-r": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 4v11a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.5 3 2.5 5 5.5 5"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 20l1.3-3.8A8 8 0 1 1 8.4 19L4 20z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8a4 4 0 0 1-2-2l.8-1-1-2L9 9.5z"/></svg>',
    "zoom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg>',
}


def chrome(ctx, page):
    B = ctx["brand"]
    on_dark = " on-dark" if page.get("header_dark") else ""
    nav_links = page.get("nav") or [("Wallets", "wallets.html"), ("Belts", "belts.html"), ("Story", "about.html")]
    links = "".join(f'<a href="{h}" class="nav-underline">{t}</a>' for t, h in nav_links)
    menu_links = [("Home", "index.html"), ("Wallets", "wallets.html"), ("Belts", "belts.html"), ("Story", "about.html"), ("Shop", "index.html#shop")]
    menu = "".join(f'<a class="menu-link" href="{h}"><sup>0{i + 1}</sup>{t}</a>' for i, (t, h) in enumerate(menu_links))
    socials = "".join(f'<a href="{B["social"]["links"][k]}" aria-label="{n}" target="_blank" rel="noopener">{ICON[i]}</a>' for k, n, i in [("instagram", "Instagram", "insta"), ("facebook", "Facebook", "fb"), ("tiktok", "TikTok", "tiktok"), ("whatsapp", "WhatsApp", "wa")])
    loader = ""
    if page.get("loader"):
        pills = [("14%", "20%", False), ("68%", "16%", True), ("8%", "58%", False), ("70%", "74%", False), ("40%", "80%", True), ("30%", "36%", True)]
        texts = ["100% crazy horse leather", "Handmade in Pakistan", "Saddle stitched", "Cash on delivery", "Rs 1,740 to Rs 3,500", "Solid brass"]
        pops = "".join(f'<span class="pop{" light" if l else ""}" style="--x:{x};--y:{y}">{t}</span>' for (x, y, l), t in zip(pills, texts))
        loader = f'''
<div class="loader" role="status" aria-live="polite" aria-label="Loading">
  <div class="pills" aria-hidden="true">{pops}</div>
  <div class="mark" aria-hidden="true"><span class="word">STAGR</span><span class="ldot"></span></div>
  <div class="count" aria-hidden="true">000</div>
  <button type="button" class="skip-btn">Skip</button>
</div>'''
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(page["title"])}</title>
<meta name="description" content="{esc(page.get("description", B["descriptor"]))}">
<meta name="theme-color" content="#efede6">
<link rel="icon" type="image/png" href="assets/brand/stagr-mark-brass.png">
<link rel="preload" as="font" type="font/woff2" href="fonts/soehne-buch.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/soehne-breit-extrafett.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/tiempos-headline-light.woff2" crossorigin>
<script>(function(){{try{{var d=document.documentElement,t=localStorage.getItem('stagr-theme');if(t)d.setAttribute('data-theme',t);if(sessionStorage.getItem('stagr-transition')==='1'){{d.classList.add('is-entering');sessionStorage.removeItem('stagr-transition');}}if(sessionStorage.getItem('stagr-loaded')==='1'||matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('no-loader');}}catch(e){{}}}})();</script>
<style>
{ctx["base_css"]}
/* ---------- page: {page["title"]} ---------- */
{page.get("css", "")}
</style>
</head>
<body id="top" data-page="{page.get("key", "")}">
<a class="skip" href="#main">Skip to content</a>
{loader}
<div class="fade" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><div class="ring"><span></span></div><div class="dot"></div></div>

<nav class="nav{on_dark}" aria-label="Primary">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Stagr, home">STAGR<span class="dot"></span></a>
    <div class="links">{links}</div>
    <div class="right">
      <a class="shop" href="{page.get("shop_href", "index.html#shop")}">Shop {ICON["arrow"]}</a>
      <button type="button" class="icon-btn" data-cart-open aria-label="Open cart">{ICON["bag"]}<span class="cart-count" aria-hidden="true">0</span></button>
      <button type="button" class="burger" data-menu-open aria-expanded="false" aria-controls="menu" aria-label="Open menu"><i></i><i></i></button>
    </div>
  </div>
</nav>

<div class="menu" id="menu" aria-hidden="true">
  <div class="menu-top"><span class="brand wordmark" style="font-size:1.25rem">STAGR<span class="dot"></span></span><button type="button" class="icon-btn" data-menu-close aria-label="Close menu">{ICON["close"]}</button></div>
  <div class="menu-links">{menu}</div>
  <div class="menu-foot"><span>{B["domain"]} · {B["origin"]}</span><span><a href="{B["contact"]["whatsapp"]["link"]}" target="_blank" rel="noopener">WhatsApp</a> &nbsp;·&nbsp; <a href="{B["social"]["links"]["instagram"]}" target="_blank" rel="noopener">Instagram</a> &nbsp;·&nbsp; <button type="button" class="theme-toggle" aria-pressed="false">Dark mode</button></span></div>
</div>

<main id="main">
{page["body"]}
</main>

<footer class="footer">
  <div class="wrap">
    <div class="news">
      <div><p class="label">Newsletter</p><h2 class="h3" style="margin-top:14px;max-width:16ch">{B["newsletter"]["body"].split(".")[0]}.</h2></div>
      <div><form class="input-row" data-notify><label class="sr-only" for="news-email">Email address</label><input class="input" id="news-email" type="email" placeholder="Email address" required autocomplete="email"><button class="btn btn--text" type="submit">Sign up {ICON["arrow"]}</button></form><p class="small muted" data-notify-status style="margin-top:10px;min-height:1.5em">Two emails a month. Nothing else.</p></div>
    </div>
    <div class="cols">
      <div><span class="brand wordmark" style="font-size:1.25rem">STAGR<span class="dot"></span></span><p class="small muted" style="margin-top:14px;max-width:28ch">{B["descriptor"]} {B["origin"]}.</p><div class="socials" style="margin-top:18px">{socials}</div></div>
      <div><h4>Site</h4><ul><li><a href="index.html#range">Range</a></li><li><a href="index.html#inside">Inside</a></li><li><a href="about.html">Story</a></li><li><a href="index.html#shop">Shop</a></li></ul></div>
      <div><h4>Shop</h4><ul><li><a href="wallets.html">Wallets</a></li><li><a href="belts.html">Belts</a></li><li><a href="about.html#bulk">Bulk orders</a></li><li><a href="{B["contact"]["whatsapp"]["link"]}" target="_blank" rel="noopener">WhatsApp</a></li></ul></div>
      <div><h4>Help</h4><ul><li><a href="index.html#delivery">Delivery &amp; returns</a></li><li><a href="about.html#faq">Questions</a></li><li><a href="#">Privacy</a></li><li><a href="#">Terms</a></li></ul></div>
    </div>
    <div class="legal"><span>© 2026 {B["domain"]}</span><span>{B["shipping"]["footerLine"]}</span></div>
  </div>
</footer>

<div class="cart-backdrop" aria-hidden="true"></div>
<aside class="cart" aria-hidden="true" aria-label="Cart">
  <div class="cart-head"><span class="t">Cart <span class="small muted cart-count-inline"></span></span><button type="button" class="icon-btn" data-cart-close aria-label="Close cart">{ICON["close"]}</button></div>
  <div class="cart-body">
    <div class="cart-empty"><p class="h4">Your cart is empty.</p><p class="small muted">Leather, by the piece.</p><button type="button" class="btn btn--ghost btn--sm" data-cart-close style="margin-top:8px">Continue</button></div>
  </div>
  <div class="cart-foot" hidden>
    <p class="small muted" data-ship-text></p>
    <div class="ship-bar"><i data-ship-bar></i></div>
    <div class="between" style="align-items:baseline"><span class="label">Subtotal</span><span class="num price" style="font-size:1.4rem" data-subtotal>Rs 0</span></div>
    <button type="button" class="btn btn--wide" data-checkout-open>Checkout {ICON["arrow"]}</button>
    <p class="small muted" style="text-align:center">Cash on delivery across Pakistan. Delivery 3 to 5 working days.</p>
  </div>
</aside>
<div class="checkout" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Checkout">
  <div class="checkout-panel">
    <button type="button" class="icon-btn close" data-checkout-close aria-label="Close">{ICON["close"]}</button>
    <p class="label">Cash on delivery</p>
    <h2 class="h3">Send your order on WhatsApp.</h2>
    <p class="small muted">We confirm by message, pack it, and you pay the courier at the door. Nothing is taken up front.</p>
    <div class="order" data-order></div>
    <a class="btn btn--wide" data-wa href="{B["contact"]["whatsapp"]["link"]}" target="_blank" rel="noopener">Send on WhatsApp {ICON["arrow"]}</a>
    <p class="small muted">Prefer to call? {B["contact"]["phone"]["value"]}</p>
  </div>
</div>
<div class="toast" role="status" aria-live="polite"></div>

<script src="{CDN["gsap"]}"></script>
<script src="{CDN["ScrollTrigger"]}"></script>
<script src="{CDN["SplitText"]}"></script>
<script src="{CDN["DrawSVGPlugin"]}"></script>
<script src="{CDN["Flip"]}"></script>
<script src="{CDN["Observer"]}"></script>
<script src="{CDN["lenis"]}"></script>
<script>window.STAGR_DATA = {inline_data(ctx)};</script>
<script src="js/stagr.js"></script>
<script>
{page.get("js", "")}
</script>
</body>
</html>
'''


def load_page(name):
    path = os.path.join(HERE, "pages", name + ".py")
    spec = importlib.util.spec_from_file_location("page_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    with open(os.path.join(HERE, "base.css"), encoding="utf-8") as f:
        base_css = f.read()
    products_doc = load_json("products.json")
    ctx = {"products": products_doc["products"], "products_doc": products_doc, "brand": load_json("brand.json"), "base_css": base_css, "icon": ICON, "esc": esc, "cutouts": cutouts_for, "bloom": BLOOM, "swatch": SWATCH}
    pages = sys.argv[1:] or ["index", "collection", "product", "about"]
    for name in pages:
        if not os.path.exists(os.path.join(HERE, "pages", name + ".py")):
            print("skip (no module):", name); continue
        outputs = load_page(name).render(ctx)
        if isinstance(outputs, dict):
            outputs = [outputs]
        for page in outputs:
            out = os.path.join(SITE, page.get("file", name + ".html"))
            with open(out, "w", encoding="utf-8") as f:
                f.write(chrome(ctx, page))
            print("wrote", os.path.relpath(out, SITE), f"{os.path.getsize(out) // 1024} KB")


if __name__ == "__main__":
    main()
