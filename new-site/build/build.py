#!/usr/bin/env python3
"""Assemble the Stagr site.

    python3 build/build.py            # writes new-site/*.html

Each page module in build/pages/ exposes `render(ctx) -> dict` with keys
title, description, css, body, js and optional flags. This script wraps the
body in the shared chrome (head, header, split menu, cart drawer, footer,
scripts) and inlines base.css so every page is self-contained for CSS.
"""
import importlib.util, json, os, sys, html as html_mod

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "data")

GSAP_VER = "3.13.0"
CDN = {
    "gsap": f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{GSAP_VER}/gsap.min.js",
    "ScrollTrigger": f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{GSAP_VER}/ScrollTrigger.min.js",
    "SplitText": f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{GSAP_VER}/SplitText.min.js",
    "Flip": f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{GSAP_VER}/Flip.min.js",
    "Observer": f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{GSAP_VER}/Observer.min.js",
    "lenis": "https://unpkg.com/lenis@1.3.4/dist/lenis.min.js",
}
FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Manrope:wght@400..700&display=swap"


def load_json(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html_mod.escape(str(s), quote=True)


def compact_products(products):
    """Strip extraction-only fields before inlining into pages."""
    out = []
    for p in products:
        q = {k: v for k, v in p.items() if k not in ("flags",)}
        q["images"] = [{k: v for k, v in im.items() if k in ("src", "alt", "width", "height", "colour")} for im in p["images"]]
        q["lifestyleImages"] = [{k: v for k, v in im.items() if k in ("src", "alt", "width", "height")} for im in p["lifestyleImages"]]
        out.append(q)
    return out


def inline_data(ctx):
    data = {
        "products": compact_products(ctx["products"]),
        "brand": {
            "freeDeliveryThreshold": ctx["brand"]["shipping"]["freeDeliveryThreshold"],
            "freeDeliveryCopy": ctx["brand"]["shipping"]["freeDeliveryCopy"],
            "cartEmpty": ctx["brand"]["cart"]["empty"],
        },
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# --------------------------------------------------------------------------
# SVG icons
# --------------------------------------------------------------------------
ICON = {
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    "arrow": '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "arrow-l": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    "arrow-r": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 4v11a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.5 3 2.5 5 5.5 5"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 20l1.3-3.8A8 8 0 1 1 8.4 19L4 20z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8a4 4 0 0 1-2-2l.8-1-1-2L9 9.5z"/></svg>',
    "zoom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg>',
}

# Antler mark as a CSS mask (currentColor) so it recolours with the theme.
MARK = '<i class="mark-icon" aria-hidden="true"></i>'


def chrome(ctx, page):
    brand = ctx["brand"]
    on_dark = " on-dark" if page.get("header_dark") else ""
    loader = ""
    if page.get("loader"):
        loader = f'''
<div class="loader" id="loader" aria-hidden="true">
  <div class="grain"></div>
  <div class="mark"><img src="assets/brand/stagr-lockup-brass.png" alt="" width="538" height="392"></div>
  <div class="count">000</div>
  <div class="word">Nothing but leather</div>
  <div class="bar"></div>
  <button type="button" class="skip-btn">Skip</button>
</div>'''

    menu_art = ctx["products"][4]["images"][0]["src"]
    links = [("Home", "index.html", ctx["products"][7]["images"][0]["src"]),
             ("Wallets", "wallets.html", ctx["products"][4]["images"][0]["src"]),
             ("Belts", "belts.html", ctx["products"][0]["images"][0]["src"]),
             ("About", "about.html", "assets/lifestyle/ranger-open.jpg")]
    menu_links = "".join(
        f'<a class="menu-link" href="{h}" data-art="{a}"><sup>0{i+1}</sup><span class="u-line">{t}</span></a>'
        for i, (t, h, a) in enumerate(links))

    year = "2026"
    foot = brand["footer"]
    socials = "".join(
        f'<a href="{brand["social"]["links"][k]}" aria-label="{n}" target="_blank" rel="noopener">{ICON[i]}</a>'
        for k, n, i in [("instagram", "Instagram", "insta"), ("facebook", "Facebook", "fb"), ("tiktok", "TikTok", "tiktok"), ("whatsapp", "WhatsApp", "wa")])

    head_links = ('<a class="nav-link u-line" href="wallets.html">Wallets</a>'
                  '<a class="nav-link u-line" href="belts.html">Belts</a>'
                  '<a class="nav-link u-line" href="about.html">About</a>')

    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(page["title"])} — Stagr</title>
<meta name="description" content="{esc(page.get("description", brand["descriptor"]))}">
<meta name="theme-color" content="#F6F2EC">
<link rel="icon" type="image/png" href="assets/brand/stagr-mark-brass.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<script>(function(){{try{{var d=document.documentElement,t=localStorage.getItem('stagr-theme');if(t)d.setAttribute('data-theme',t);if(sessionStorage.getItem('stagr-transition')==='1')d.classList.add('is-entering');if(sessionStorage.getItem('stagr-loaded')==='1'||matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('no-loader');}}catch(e){{}}}})();</script>
<style>
{ctx["base_css"]}
/* ---------- page: {page["title"]} ---------- */
{page.get("css", "")}
</style>
</head>
<body class="{page.get("body_class", "")}">
<a class="skip" href="#main">Skip to content</a>
{loader}
<div class="curtain" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><path d="M12 3v18M4 7l8 6 8-6"/></svg></div>
<div class="cursor" aria-hidden="true"><div class="ring"><span></span></div><div class="dot"></div></div>

<header class="header{on_dark}" id="top">
  <div class="wrap">
    <div class="nav-left">
      <button type="button" class="burger" data-menu-open aria-expanded="false" aria-controls="menu" aria-label="Open menu"><i></i><i></i></button>
      {head_links}
    </div>
    <a class="logo" href="index.html" aria-label="Stagr, home">{MARK}<span class="wordmark">Stagr</span></a>
    <div class="nav-right">
      <button type="button" class="icon-btn theme-toggle" aria-label="Toggle dark mode" aria-pressed="false">{ICON["sun"]}{ICON["moon"]}</button>
      <button type="button" class="icon-btn" data-cart-open aria-label="Open your bag">{ICON["bag"]}<span class="cart-count" aria-hidden="true">0</span></button>
    </div>
  </div>
</header>

<nav class="menu" id="menu" aria-hidden="true" aria-label="Site menu">
  <div class="menu-panel l"></div>
  <div class="menu-panel r"></div>
  <div class="menu-inner">
    <div class="menu-top">
      <span class="label" style="color:var(--c-saddle)">Menu</span>
      <button type="button" class="menu-close" data-menu-close aria-label="Close menu">{ICON["close"]}</button>
    </div>
    <div class="menu-links">{menu_links}</div>
    <div class="menu-foot">
      <span>{brand["domain"]} · {brand["origin"]}</span>
      <span><a href="{brand["contact"]["whatsapp"]["link"]}" target="_blank" rel="noopener">WhatsApp</a> &nbsp;·&nbsp; <a href="{brand["social"]["links"]["instagram"]}" target="_blank" rel="noopener">Instagram</a></span>
    </div>
    <div class="menu-art media media--studio"><img src="{menu_art}" alt="" width="1448" height="1086" loading="lazy"></div>
  </div>
</nav>

<div class="drawer-backdrop" aria-hidden="true"></div>
<aside class="drawer" aria-hidden="true" aria-label="Your bag" data-lenis-prevent>
  <div class="drawer-head"><span class="h4">{brand["cart"]["title"]}</span><button type="button" class="btn--icon btn" data-cart-close aria-label="Close bag">{ICON["close"]}</button></div>
  <div class="drawer-body"></div>
  <div class="drawer-foot" hidden>
    <div class="small muted" data-delivery-note></div>
    <div class="progress"><i data-delivery-progress></i></div>
    <div class="between" style="align-items:baseline"><span class="label">Subtotal</span><span class="price h4" data-subtotal>Rs 0</span></div>
    <button type="button" class="btn btn--wide" data-checkout>{brand["cart"]["checkout"]}{ICON["arrow"]}</button>
    <p class="small muted center" style="margin:0">{brand["cart"]["sub"]}</p>
  </div>
</aside>

<main id="main">
{page["body"]}
</main>

<footer class="footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-col news">
        <a class="logo" href="index.html" aria-label="Stagr, home" style="display:inline-flex;align-items:center;gap:10px;margin-bottom:18px">{MARK}<span class="wordmark">Stagr</span></a>
        <p class="small" style="max-width:32ch;color:rgba(246,242,236,.72)">{brand["descriptor"]} {brand["origin"]}.</p>
        <form class="input-row" style="margin-top:28px;max-width:420px" data-newsletter>
          <label class="sr-only" for="news-email">Email address</label>
          <input class="input" id="news-email" type="email" name="email" placeholder="Your email" required autocomplete="email">
          <button class="btn btn--sm" type="submit">{brand["newsletter"]["cta"]}</button>
        </form>
        <p class="small" style="margin-top:10px;color:rgba(246,242,236,.6)">{brand["newsletter"]["body"]}</p>
      </div>
      <div class="foot-col"><h4>Shop</h4><ul><li><a href="belts.html">Belts</a></li><li><a href="wallets.html">Wallets</a></li><li><a href="index.html#featured">Featured</a></li></ul></div>
      <div class="foot-col"><h4>Help</h4><ul><li><a href="product.html#details">Size guide</a></li><li><a href="index.html#trust">Delivery &amp; returns</a></li><li><a href="{brand["contact"]["whatsapp"]["link"]}" target="_blank" rel="noopener">Contact on WhatsApp</a></li></ul></div>
      <div class="foot-col"><h4>Company</h4><ul><li><a href="about.html">About</a></li><li><a href="about.html#craft">How it is made</a></li><li><a href="about.html#bulk">Bulk orders</a></li></ul></div>
      <div class="foot-col"><h4>Follow</h4><div class="socials">{socials}</div><p class="small" style="margin-top:14px;color:rgba(246,242,236,.6)">{brand["social"]["handle"]}</p></div>
    </div>
    <div class="foot-bottom">
      <span>© {year} {brand["domain"]}</span>
      <span>{brand["shipping"]["footerLine"]}</span>
      <nav aria-label="Legal"><a href="#" class="u-line">Privacy</a><a href="#" class="u-line">Terms</a></nav>
    </div>
  </div>
  <div class="marquee marquee--big foot-marquee" data-marquee data-speed="80" aria-hidden="true">
    <div class="track"><span>Stagr</span><span class="alt">—</span><span>Nothing but leather</span><span class="alt">—</span><span>Handmade in Pakistan</span><span class="alt">—</span></div>
  </div>
</footer>
<div class="toast" role="status" aria-live="polite"></div>

<script src="{CDN["gsap"]}"></script>
<script src="{CDN["ScrollTrigger"]}"></script>
<script src="{CDN["SplitText"]}"></script>
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


def main(only=None):
    with open(os.path.join(HERE, "base.css"), encoding="utf-8") as f:
        base_css = f.read()
    base_css += "\nhtml.is-entering .curtain{transform:none}\nhtml.no-loader .loader{display:none}\n.mark-icon{display:inline-block;width:34px;height:13px;background:currentColor;-webkit-mask:url(assets/brand/stagr-mark-dark.png) center/contain no-repeat;mask:url(assets/brand/stagr-mark-dark.png) center/contain no-repeat;vertical-align:middle}\n.logo{display:inline-flex;align-items:center;gap:10px}\n.wordmark{font-family:var(--font-display);font-size:1.5rem;letter-spacing:-.01em;line-height:1;font-variation-settings:\"opsz\" 48}\n"
    ctx = {
        "products": load_json("products.json")["products"],
        "brand": load_json("brand.json"),
        "base_css": base_css,
        "icon": ICON,
        "esc": esc,
    }
    pages = sys.argv[1:] or ["design_system", "index", "wallets", "belts", "product", "about"]
    for name in pages:
        path = os.path.join(HERE, "pages", name + ".py")
        if not os.path.exists(path):
            print("skip (no module):", name); continue
        mod = load_page(name)
        outputs = mod.render(ctx)
        if isinstance(outputs, dict):
            outputs = [outputs]
        for page in outputs:
            out = os.path.join(SITE, page.get("file", name.replace("_", "-") + ".html"))
            with open(out, "w", encoding="utf-8") as f:
                f.write(chrome(ctx, page))
            print("wrote", os.path.relpath(out, SITE), f"{os.path.getsize(out)//1024} KB")


if __name__ == "__main__":
    main()
