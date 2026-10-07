"""wallets.html and belts.html — collection pages.

Opening: a full-height, scroll-pinned showcase in the style of the Daniel
Roth reference: full-bleed photo on the left, bone panel on the right with
the collection name, a cutout, a counter, the models listed, a caps line and
a "Discover the collection" button. One slide per collection. Then the
filterable grid, cross-sell and delivery strip.
"""
import json

SWATCH = {"Brown": "#6E4328", "Black": "#1A1512", "Tan": "#B0773F", "Coffee": "#4A3024"}
TINT = {"bifold": "#6B3F2A", "trifold": "#4A3A33", "minimalist": "#7A5A3A", "long": "#8B4A1F", "nova": "#2B2522", "outlaw": "#5A3A27", "regent": "#1F1F23", "monarch": "#8B5A2B"}


def page(ctx, line):
    P = [p for p in ctx["products"] if p["line"] == line]
    by = {p["id"]: p for p in ctx["products"]}
    B = ctx["brand"]
    I = ctx["icon"]
    cut = ctx["cutouts"]
    other = "belt" if line == "wallet" else "wallet"
    title = "Wallets" if line == "wallet" else "Belts"
    other_title = "Belts" if line == "wallet" else "Wallets"
    blurb = ctx["products_doc"]["lines"][line]["blurb"]
    prices = [p["price"] for p in P]
    fmt = lambda n: "Rs " + format(n, ",d")

    # ---- slides ----
    if line == "wallet":
        groups = [
            dict(key="bifold", name="Bifold", ids=["kingsmann", "regal"], photo="assets/lifestyle/kingsmen-01.jpg", line1="A fold that stays flat", line2="in a jacket pocket"),
            dict(key="trifold", name="Trifold", ids=["majestic"], photo="assets/lifestyle/majestic-01.jpg", line1="Three folds, one row", line2="of saddle stitch"),
            dict(key="minimalist", name="Minimalist", ids=["maverick", "purefold"], photo="assets/lifestyle/maverick-01.jpg", line1="The slim ones,", line2="for a front pocket"),
            dict(key="long", name="Long", ids=["rodeo", "upbuck"], photo="assets/lifestyle/rodeo-01.jpg", line1="Cards, notes and", line2="a snap closure"),
        ]
    else:
        groups = [
            dict(key="nova", name="Nova", ids=["nova"], photo="assets/lifestyle/nova-02.jpg", line1="Two sides. One belt.", line2="Made for every style"),
            dict(key="outlaw", name="Outlaw", ids=["outlaw"], photo="assets/lifestyle/outlaw-wide.jpg", line1="Rugged character,", line2="timeless craftsmanship"),
            dict(key="regent", name="Regent", ids=["regent"], photo="assets/lifestyle/onyx-01.jpg", line1="Classic elegance,", line2="crafted to last"),
            dict(key="monarch", name="Monarch", ids=["monarch"], photo="assets/lifestyle/monarch-01.jpg", line1="Premium character,", line2="a patina that deepens"),
        ]
    for g in groups:
        g["variants"] = []
        for pid in g["ids"]:
            p = by[pid]
            for c in cut(p):
                if c["colour"] not in [v["colour"] for v in g["variants"] if v["id"] == pid]:
                    g["variants"].append({"id": pid, "name": p["name"].split(" ")[0], "colour": c["colour"], "src": c["src"], "price": p["price"]})
        g["from"] = min(by[i]["price"] for i in g["ids"])
        g["count"] = len(g["ids"])
    n = len(groups)

    def variant_label(v, g):
        return f'{v["name"]} {v["colour"]}' if g["count"] > 1 or line == "belt" and len(g["variants"]) > 1 else v["colour"]

    photos = "".join(f'<div class="sc-photo" data-sc-photo="{i}" style="opacity:{1 if i == 0 else 0};--tint:{TINT[g["key"]]}"><img src="{g["photo"]}" srcset="{g["photo"].replace(".jpg", "-800.jpg")} 800w, {g["photo"]} 1600w" sizes="(min-width: 1024px) 60vw, 100vw" alt="" width="1200" height="1500" {"fetchpriority=high" if i == 0 else "loading=lazy"}></div>' for i, g in enumerate(groups))
    cuts = "".join(f'<div class="sc-cut" data-sc-cut="{i}" style="opacity:{1 if i == 0 else 0}"><img data-sc-cut-img src="{g["variants"][0]["src"]}" alt="{g["name"]} {title.lower()[:-1]}" width="900" height="900" decoding="async"></div>' for i, g in enumerate(groups))
    panels = "".join(f'''
<div class="sc-panel" data-sc-panel="{i}" {"hidden" if i else ""}>
  <h2 class="sc-title" data-sc-title>{g["name"]}</h2>
  <p class="label sc-kicker" data-sc-item>Collection · from {fmt(g["from"])}</p>
  <ul class="sc-variants" data-sc-variants>{"".join(f'<li><button type="button" class="{"is-on" if k == 0 else ""}" data-sc-variant="{v["src"]}" data-sc-href="product-{v["id"]}.html" data-sc-item>{variant_label(v, g)}</button></li>' for k, v in enumerate(g["variants"]))}</ul>
  <p class="sc-line" data-sc-item>{g["line1"]}<br>{g["line2"]}</p>
  <a class="btn sc-cta" data-sc-item data-sc-cta href="product-{g["ids"][0]}.html">Discover the collection {I["arrow"]}</a>
</div>''' for i, g in enumerate(groups))
    dots = "".join(f'<button type="button" data-sc-dot="{i}" aria-label="Show {g["name"]}" style="color:{"var(--ink)" if i == 0 else "var(--mist)"}">0{i + 1}</button>' for i, g in enumerate(groups))
    mpanels = "".join(f'''
<article class="sc-mcard on-bone" data-sc-mcard="{i}">
  <div class="sc-mcut"><img src="{g["variants"][0]["src"].replace(".webp", "-600.webp")}" alt="" width="600" height="600" loading="lazy"></div>
  <h2 class="sc-title" data-sc-mtitle>{g["name"]}</h2>
  <p class="label" data-sc-mitem>Collection · from {fmt(g["from"])}</p>
  <ul class="sc-variants" data-sc-mitem>{"".join(f'<li><a href="product-{v["id"]}.html">{variant_label(v, g)}</a></li>' for v in g["variants"])}</ul>
  <p class="sc-line" data-sc-mitem>{g["line1"]}<br>{g["line2"]}</p>
  <a class="btn" data-sc-mitem href="product-{g["ids"][0]}.html">Discover {I["arrow"]}</a>
</article>''' for i, g in enumerate(groups))

    # ---- grid ----
    colours = sorted({c for p in P for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black"].index(c) if c in ["Brown", "Tan", "Black"] else 9)
    styles = sorted({p["style"] for p in P if p["style"]}, key=lambda s: ["Bifold", "Trifold", "Minimalist", "Long"].index(s) if s in ["Bifold", "Trifold", "Minimalist", "Long"] else 9)
    cards = "".join(ctx["pcard"](ctx, p, i) for i, p in enumerate(P))
    cross = [p for p in ctx["products"] if p["line"] == other][:3]
    cross_cards = "".join(ctx["pcard"](ctx, p, i, quick=False) for i, p in enumerate(cross))
    colour_pills = "".join(f'<button type="button" class="pill" data-filter="colour" data-value="{c}" aria-pressed="false"><span class="sw" style="--sw:{SWATCH.get(c, "#6E4328")}"></span>{c}</button>' for c in colours)
    style_pills = "".join(f'<button type="button" class="pill" data-filter="style" data-value="{s}" aria-pressed="false">{s}</button>' for s in styles)
    price_pills = ('<button type="button" class="pill" data-filter="price" data-value="0-2000" aria-pressed="false">Under Rs 2,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="2000-3000" aria-pressed="false">Rs 2,000 – 3,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="3000-99999" aria-pressed="false">Over Rs 3,000</button>')
    products_json = json.dumps([{k: p[k] for k in ("id", "name", "style", "tagline", "price", "compareAtPrice", "colours", "defaultColour", "line", "sizes")} | {"cutouts": cut(p)} for p in P], ensure_ascii=False).replace("</", "<\\/")

    css = r'''
.dotc { color: var(--accent); }
/* ---- showcase (Daniel Roth style) ---- */
.showcase { position: relative; background: var(--ink); color: var(--bone); overflow: hidden; }
.sc-pin { position: relative; height: 100vh; }
.sc-photos { position: absolute; inset: 0; }
.sc-photo { position: absolute; inset: 0; }
.sc-photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 30% 50%; transform: scale(1.08); will-change: transform; }
.sc-photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, color-mix(in srgb, var(--tint) 55%, transparent), color-mix(in srgb, var(--tint) 20%, transparent) 60%, rgba(26,27,29,.35)); mix-blend-mode: multiply; }
.sc-brand { position: absolute; left: var(--gutter); top: calc(var(--nav-h) + 16px); z-index: 3; font-size: .75rem; letter-spacing: .24em; text-transform: uppercase; color: rgba(239,237,230,.75); }
.sc-panel-wrap { position: absolute; right: var(--gutter); top: calc(var(--nav-h) + 8px); bottom: 32px; width: min(44vw, 640px); background: var(--bone); color: var(--ink); display: grid; grid-template-rows: auto 1fr auto; padding: clamp(24px, 3vw, 44px); overflow: hidden; }
.sc-panel { position: absolute; inset: 0; padding: clamp(24px, 3vw, 44px); display: grid; grid-template-rows: auto 1fr auto; }
.sc-title { font-family: var(--font-display); font-weight: 300; font-size: clamp(2.4rem, 1.6rem + 3vw, 4.6rem); line-height: 1; letter-spacing: .02em; text-transform: uppercase; text-align: center; }
.sc-kicker { text-align: center; margin-top: 12px; }
.sc-variants { position: absolute; right: clamp(24px, 3vw, 44px); top: 50%; transform: translateY(-50%); text-align: right; display: grid; gap: 10px; font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; }
.sc-variants button, .sc-variants a { color: var(--fg-2); transition: color .3s ease; position: relative; }
.sc-variants button.is-on, .sc-variants a:hover, .sc-variants button:hover { color: var(--ink); }
.sc-variants button.is-on::after { content: ""; position: absolute; left: 0; right: 0; bottom: -3px; height: 1px; background: var(--ink); }
.sc-count { position: absolute; left: clamp(24px, 3vw, 44px); top: 50%; transform: translateY(-50%); font-size: .75rem; letter-spacing: .2em; color: var(--mist); font-variant-numeric: tabular-nums; }
.sc-stage { position: absolute; left: 50%; top: 50%; width: min(44%, 280px); aspect-ratio: 1; transform: translate(-50%, -52%); display: grid; place-items: center; }
.sc-cut { position: absolute; inset: 0; display: grid; place-items: center; }
.sc-cut img { width: 100%; height: auto; max-height: 100%; object-fit: contain; filter: drop-shadow(0 30px 40px rgba(26,27,29,.28)); }
.sc-line { align-self: end; font-size: .8125rem; letter-spacing: .12em; text-transform: uppercase; line-height: 1.7; color: var(--mist); max-width: 24ch; }
.sc-cta { position: absolute; right: clamp(24px, 3vw, 44px); bottom: clamp(24px, 3vw, 44px); }
.sc-dots { position: absolute; left: var(--gutter); bottom: 32px; z-index: 3; display: flex; gap: 16px; font-size: 12px; letter-spacing: .2em; color: rgba(239,237,230,.6); }
.sc-dots button { color: inherit !important; opacity: .55; transition: opacity .3s ease; }
.sc-dots button.is-on { opacity: 1; }
.sc-hint { position: absolute; left: 50%; bottom: 32px; transform: translateX(-50%); z-index: 3; }
.sc-hint .t { color: rgba(239,237,230,.6); }
.sc-hint .mouse { border-color: rgba(239,237,230,.4); }
@media (max-width: 1023px) {
  .sc-pin { height: auto; }
  .sc-photos { position: relative; height: 54svh; margin-top: var(--nav-top); }
  .sc-panel-wrap { position: relative; right: auto; top: auto; bottom: auto; width: auto; margin: -40px 20px 0; padding: 24px 20px; display: block; min-height: 0; z-index: 2; }
  .sc-panel { position: static; padding: 0; display: block; }
  .sc-stage { position: relative; left: auto; top: auto; transform: none; width: 60%; margin: 16px auto; }
  .sc-variants { position: static; transform: none; text-align: left; display: flex; flex-wrap: wrap; gap: 8px 16px; margin-top: 12px; }
  .sc-count { position: static; transform: none; display: block; margin-top: 8px; }
  .sc-line { margin-top: 18px; }
  .sc-cta { position: static; margin-top: 18px; }
  .sc-brand, .sc-hint { display: none; }
  .sc-dots { position: static; justify-content: center; padding: 20px 0 8px; color: rgba(239,237,230,.6); }
  .sc-mobile-track { display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 0 20px 24px; scrollbar-width: none; }
  .sc-mobile-track::-webkit-scrollbar { display: none; }
  .sc-mcard { flex: 0 0 86vw; scroll-snap-align: center; background: var(--bone); color: var(--ink); padding: 24px 20px; display: grid; gap: 12px; }
  .sc-mcut { width: 60%; margin: 0 auto; }
  .sc-mcut img { width: 100%; height: auto; filter: drop-shadow(0 20px 30px rgba(26,27,29,.25)); }
  .sc-mcard .sc-title { font-size: 2.2rem; }
  .sc-mcard .sc-variants { justify-content: center; }
  .sc-mcard .sc-line { text-align: center; max-width: none; }
  .sc-mcard .btn { justify-self: center; }
}

/* ---- intro line under the showcase ---- */
.col-intro { padding: var(--section-sm) 0 clamp(24px, 4vw, 48px); }
.col-intro .display { font-size: clamp(2.6rem, 1.6rem + 4vw, 5.5rem); line-height: 1; }
.col-intro .lead { margin-top: 18px; }
.col-facts { max-width: 420px; }

/* ---- filter bar ---- */
.filters { position: sticky; top: var(--nav-h); z-index: 30; background: color-mix(in srgb, var(--bg) 94%, transparent); backdrop-filter: blur(14px); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 12px 0; }
.filters .wrap { display: grid; gap: 12px; }
.filter-groups { display: flex; flex-wrap: wrap; gap: 10px 24px; align-items: center; }
.filter-group { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.filter-group .label { font-size: .6875rem; margin-right: 4px; }
.filter-group .pill { min-height: 34px; padding: 0 12px; font-size: .6875rem; }
.filter-meta { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
.filter-meta .clear { display: none; }
.filter-meta .clear.is-on { display: inline-flex; }
.filters .select { min-height: 34px; width: auto; padding: 0 24px 0 0; font-size: .75rem; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; border: 0; background: transparent url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%231A1B1D' stroke-width='1.6'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E") no-repeat right center; appearance: none; }
@media (min-width: 1024px) { .filters .wrap { grid-template-columns: 1fr auto; align-items: center; } .filter-meta { justify-content: flex-end; } }
@media (max-width: 767px) { .filters { position: static; } .filter-groups { overflow-x: auto; flex-wrap: nowrap; scrollbar-width: none; margin-inline: calc(var(--gutter) * -1); padding-inline: var(--gutter); } .filter-groups::-webkit-scrollbar { display: none; } .filter-group { flex-wrap: nowrap; } }

/* ---- grid ---- */
.catalog { padding: clamp(32px, 5vw, 64px) 0 var(--section-sm); }
.shop-grid { display: grid; gap: 16px; grid-template-columns: 1fr; }
@media (min-width: 640px) { .shop-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .shop-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; } }
.pcard.is-hidden { display: none; }
.empty { display: none; padding: 64px 0; text-align: center; }
.empty.is-on { display: block; }
.cross { padding: var(--section-sm) 0; }
.cross .between { margin-bottom: 32px; }
.delivery { display: grid; gap: 28px; padding: var(--section-sm) 0; border-top: 1px solid var(--line); }
@media (min-width: 768px) { .delivery { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.delivery h3 { font-family: var(--font-display); font-weight: 300; font-size: 1.5rem; }
.delivery p { color: var(--fg-2); font-size: .9375rem; margin-top: 8px; max-width: 26ch; }

/* ---- quick view ---- */
.qv-backdrop { position: fixed; inset: 0; z-index: 100; background: rgba(26,27,29,.45); opacity: 0; pointer-events: none; transition: opacity .35s ease; }
.qv-backdrop.is-open { opacity: 1; pointer-events: auto; }
.qv { position: fixed; z-index: 101; inset: auto 0 0 0; max-height: 92svh; overflow: auto; background: var(--bone); color: var(--ink); transform: translateY(102%); visibility: hidden; transition: transform .55s var(--ease-out), visibility 0s linear .55s; }
.qv.is-open { transform: none; visibility: visible; transition-delay: 0s; }
@media (min-width: 1024px) { .qv { inset: 50% auto auto 50%; width: min(980px, 92vw); max-height: 86vh; transform: translate(-50%, -50%) scale(.97); opacity: 0; transition: transform .45s var(--ease-out), opacity .35s ease, visibility 0s linear .45s; } .qv.is-open { transform: translate(-50%, -50%) scale(1); opacity: 1; } }
.qv-inner { display: grid; }
@media (min-width: 1024px) { .qv-inner { grid-template-columns: 1fr 1fr; } }
.qv-media { position: relative; aspect-ratio: 1; display: grid; place-items: center; background: rgba(26,27,29,.03); overflow: hidden; }
@media (min-width: 1024px) { .qv-media { aspect-ratio: auto; min-height: 100%; } }
.qv-media .bloom { --bloom-s: 70%; }
.qv-media img { position: relative; z-index: 1; width: 72%; height: auto; max-height: 80%; object-fit: contain; filter: drop-shadow(0 30px 40px rgba(26,27,29,.22)); }
.qv-thumbs { position: absolute; left: 16px; bottom: 16px; z-index: 2; display: flex; gap: 8px; }
.qv-thumbs button { width: 52px; height: 52px; border: 1px solid var(--line-strong); background: var(--bone); display: grid; place-items: center; }
.qv-thumbs button[aria-pressed="true"] { border-color: var(--ink); }
.qv-thumbs img { width: 80%; height: auto; }
.qv-body { padding: clamp(20px, 3vw, 40px); display: grid; gap: 16px; align-content: start; }
.qv-close { position: absolute; top: 10px; right: 10px; z-index: 3; }
'''

    body = f'''
<section class="showcase on-ink" aria-label="{title} collections" data-showcase>
  <div class="sc-pin" data-sc-pin>
    <div class="sc-photos" data-sc-photos>{photos}</div>
    <p class="sc-brand">{B["origin"]} · Crazy horse leather</p>
    <div class="sc-panel-wrap on-bone desk-only" data-sc-panelwrap>
      {panels}
      <span class="sc-count" data-sc-count>01 – 0{n}</span>
      <div class="sc-stage" data-sc-stage>{cuts}</div>
    </div>
    <div class="sc-mobile-track mob-only" data-sc-mtrack>{mpanels}</div>
    <div class="sc-dots">{dots}</div>
    <div class="scroll-hint sc-hint desk-only" aria-hidden="true"><span class="t">Scroll</span><span class="mouse"><i data-scroll-dot></i></span></div>
  </div>
</section>

<section class="col-intro on-bone" id="{"bifold" if line == "wallet" else "classic"}" aria-labelledby="col-title">
  <div class="wrap grid" style="align-items:end">
    <div class="col-12 lg:col-7"><p class="label" data-reveal><b>01</b><span class="slash">/</span>All {title.lower()} · {len(P)} styles</p><h1 class="display" id="col-title" data-text-reveal="chars" style="margin-top:14px">{title}<span class="dotc">.</span></h1><p class="lead" data-reveal data-delay=".2">{blurb}</p></div>
    <dl class="col-12 lg:col-4 lg:start-9 spec col-facts" data-reveal data-delay=".3">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [("Leather", "Crazy horse, full grain"), ("Pieces", f"{len(P)} styles"), ("Colours", " / ".join(colours)), ("From", fmt(min(prices)))] + ([("Sizes", "30 to 44")] if line == "belt" else []))}</dl>
  </div>
</section>

<section class="filters" id="filters" aria-label="Filter and sort">
  <div class="wrap">
    <div class="filter-groups">
      <div class="filter-group"><span class="label">Colour</span><button type="button" class="pill" data-filter="colour" data-value="" aria-pressed="true">All</button>{colour_pills}</div>
      {f'<div class="filter-group"><span class="label">Style</span><button type="button" class="pill" data-filter="style" data-value="" aria-pressed="true">All</button>{style_pills}</div>' if styles else ''}
      <div class="filter-group"><span class="label">Price</span><button type="button" class="pill" data-filter="price" data-value="" aria-pressed="true">All</button>{price_pills}</div>
    </div>
    <div class="filter-meta">
      <span class="small muted"><span data-count>{len(P)}</span> pieces</span>
      <button type="button" class="btn btn--text clear" data-clear>Clear</button>
      <label class="sr-only" for="sort">Sort</label>
      <select class="select" id="sort" data-sort><option value="default">Featured</option><option value="price-asc">Price, low to high</option><option value="price-desc">Price, high to low</option><option value="name">Name, A to Z</option></select>
    </div>
  </div>
</section>

<section class="catalog on-bone" aria-label="{title}">
  <div class="wrap">
    <div class="shop-grid" data-grid>{cards}</div>
    <div class="empty" data-empty><p class="h3">Nothing matches that yet.</p><p class="muted" style="margin-top:10px">Loosen a filter and the shelf fills up again.</p><p style="margin-top:24px"><button type="button" class="btn btn--ghost btn--sm" data-clear>Clear filters</button></p></div>
    <div class="delivery">{"".join(f'<div data-reveal data-delay="{i * .1}"><h3>{t["title"]}</h3><p>{t["sub"]}</p></div>' for i, t in enumerate(B["trust"]["items"]))}</div>
  </div>
</section>

<section class="cross on-ink" aria-labelledby="cross-title">
  <div class="wrap">
    <div class="between"><div><p class="label" data-reveal><b style="color:var(--bone)">02</b><span class="slash">/</span>Complete the look</p><h2 class="h2" id="cross-title" data-text-reveal="lines" style="margin-top:12px">{"A belt to match." if line == "wallet" else "A wallet to match."}</h2></div><a class="btn btn--ghost" href="{other}s.html" data-reveal>All {other_title.lower()} {I["arrow"]}</a></div>
    <div class="shop-grid">{cross_cards}</div>
  </div>
</section>

<div class="qv-backdrop" data-qv-close aria-hidden="true"></div>
<div class="qv" role="dialog" aria-modal="true" aria-label="Quick view" aria-hidden="true" data-lenis-prevent>
  <button type="button" class="icon-btn qv-close" data-qv-close aria-label="Close quick view">{I["close"]}</button>
  <div class="qv-inner">
    <div class="qv-media"><div class="bloom" data-qv-bloom style="--bloom:#D9B07A" data-bloom></div><img data-qv-img src="" alt="" width="900" height="900"><div class="qv-thumbs" data-qv-thumbs></div></div>
    <div class="qv-body">
      <div class="pcard-head" style="margin-top:0"><span class="pcard-num" data-qv-num></span><span class="label" data-qv-meta></span></div>
      <h2 class="h2" data-qv-name></h2>
      <p class="serif-i muted" data-qv-sub></p>
      <p class="muted" data-qv-tagline></p>
      <div><p class="label" style="margin-bottom:10px">Colour · <span data-qv-colour style="text-transform:none;letter-spacing:0"></span></p><div class="opts" data-qv-opts></div></div>
      <div data-qv-sizes hidden><p class="label" style="margin-bottom:10px">Size · <span data-qv-size style="text-transform:none;letter-spacing:0"></span></p><div class="opts" data-qv-size-opts></div></div>
      <div class="pcard-price"><span><span class="num" style="font-size:1.6rem" data-qv-price></span></span><a class="pcard-link" data-qv-link href="#">Full details {I["arrow"]}</a></div>
      <button type="button" class="btn btn--wide" data-qv-add>Add to cart</button>
      <p class="small muted">Cash on delivery · 3 to 5 days across Pakistan · 14-day returns</p>
    </div>
  </div>
</div>
'''

    js = r'''
const COLLECTION = __PRODUCTS__;
const SWATCH = { Brown: "#6E4328", Black: "#1A1512", Tan: "#B0773F", Coffee: "#4A3024" };
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, Flip = window.Flip, $ = S.$, $$ = S.$$, reduced = S.reduced, isMobile = S.isMobile, clamp = S.clamp;
  if (!G) return;

  /* ================= showcase ================= */
  const pin = $("[data-sc-pin]"), photos = $$("[data-sc-photo]"), panels = $$("[data-sc-panel]"), cuts = $$("[data-sc-cut]"), dots = $$("[data-sc-dot]"), count = $("[data-sc-count]"), stage = $("[data-sc-stage]");
  const n = photos.length; let active = 0, shown = 0, swapping = false, titleSplit = null;
  const pad = (i) => "0" + (i + 1);
  const bindVariants = (panel, i) => {
    const img = $("img", cuts[i]), cta = $("[data-sc-cta]", panel);
    $$("[data-sc-variant]", panel).forEach((b) => b.addEventListener("click", () => { $$("[data-sc-variant]", panel).forEach((x) => x.classList.toggle("is-on", x === b)); if (cta) cta.href = b.dataset.scHref; if (img.getAttribute("src") === b.dataset.scVariant) return; G.to(img, { opacity: 0, x: -14, duration: .2, ease: "power2.in", onComplete: () => { img.src = b.dataset.scVariant; G.fromTo(img, { opacity: 0, x: 18 }, { opacity: 1, x: 0, duration: .5, ease: "power3.out" }); } }); }));
  };
  const showPanel = (i) => {
    const panel = panels[i];
    G.fromTo($$("[data-sc-item]", panel), { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power2.out", stagger: .05, delay: .08, overwrite: "auto" });
    if (titleSplit) titleSplit.revert(); titleSplit = null;
    if (!reduced) titleSplit = S.charRise($("[data-sc-title]", panel), { from: 110, to: { duration: .6, stagger: .03, overwrite: "auto" } });
  };
  const swap = () => { if (shown === active || swapping) return; swapping = true; G.to(panels[shown], { y: -18, opacity: 0, duration: .22, ease: "power3.in", onComplete: () => { panels[shown].hidden = true; shown = active; panels[shown].hidden = false; G.set(panels[shown], { y: 0, opacity: 1 }); showPanel(shown); swapping = false; swap(); } }); };
  const setActive = (next) => {
    if (next === active) return; const fwd = next > active; active = next;
    photos.forEach((ph, i) => { G.to(ph, { opacity: i === next ? 1 : 0, duration: .9, ease: "power2.inOut", overwrite: "auto" }); if (i === next) G.fromTo($("img", ph), { scale: 1.16, xPercent: fwd ? 2 : -2 }, { scale: 1.08, xPercent: 0, duration: 1.6, ease: "power3.out", overwrite: "auto" }); });
    cuts.forEach((c, i) => { if (i === next) G.fromTo(c, { opacity: 0, x: fwd ? 60 : -60, rotation: fwd ? 6 : -6, scale: .9 }, { opacity: 1, x: 0, rotation: 0, scale: 1, duration: .8, ease: "power3.out", delay: .1, overwrite: "auto" }); else G.to(c, { opacity: 0, x: fwd ? -40 : 40, scale: .92, duration: .4, ease: "power2.in", overwrite: "auto" }); });
    dots.forEach((d, i) => d.classList.toggle("is-on", i === next));
    if (count) count.textContent = pad(next) + " – " + pad(n - 1);
    if (!isMobile) swap();
  };
  dots.forEach((d, i) => d.classList.toggle("is-on", i === 0));
  if (count) count.textContent = "01 – " + pad(n - 1);
  if (!isMobile) {
    panels.forEach(bindVariants);
    G.set($$("[data-sc-item]", panels[0]), { opacity: 0 });
    const trigger = ST.create({ trigger: pin, start: "top top", end: () => "+=" + (n * innerHeight), pin: true, pinSpacing: true, scrub: 1, snap: { snapTo: Array.from({ length: n }, (_, i) => i / (n - 1)), duration: { min: .25, max: .55 }, ease: "power2.inOut", directional: false, delay: .1 }, invalidateOnRefresh: true, refreshPriority: 2,
      onUpdate: (self) => { const step = 1 / (n - 1); let next = active; while (next < n - 1 && self.progress > (next + .5) * step + .04) next++; while (next > 0 && self.progress < (next - .5) * step - .04) next--; setActive(next); } });
    dots.forEach((d, i) => d.addEventListener("click", () => S.scrollToProgress(trigger, i / (n - 1), 1)));
    // entrance (after loader)
    const wrap = $("[data-sc-panelwrap]");
    G.set(wrap, { opacity: 0, x: 40 });
    S.onLoaderDone.push(() => { G.to(wrap, { opacity: 1, x: 0, duration: 1, ease: "power3.out", delay: .1 }); G.fromTo($("img", photos[0]), { scale: 1.2 }, { scale: 1.08, duration: 2, ease: "power3.out" }); showPanel(0); G.fromTo(cuts[0], { opacity: 0, y: 30, scale: .9 }, { opacity: 1, y: 0, scale: 1, duration: 1, ease: "power3.out", delay: .35 }); if (!reduced) G.to($("img", cuts[0]), { y: -8, duration: 3.2, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 1.4 }); });
    const dot = $("[data-scroll-dot]"); if (dot && !reduced) G.timeline({ repeat: -1, repeatDelay: .5 }).set(dot, { y: 0, opacity: 0 }).to(dot, { opacity: 1, duration: .25 }).to(dot, { y: 19, duration: 1, ease: "power2.inOut" }, .1).to(dot, { opacity: 0, duration: .3 }, .85);
  } else {
    const track = $("[data-sc-mtrack]"), titles = $$("[data-sc-mtitle]", track); let split = null;
    const reveal = (i) => { const t = titles[i], items = $$("[data-sc-mitem]", t.closest("article")); if (reduced) { G.set([t, ...items], { opacity: 1 }); return; } if (split) split.revert(); split = S.charRise(t, { from: 108, to: { duration: .55, stagger: .03, overwrite: "auto" } }); G.set(t, { opacity: 1 }); G.fromTo(items, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .45, ease: "power2.out", stagger: .05, delay: .1, overwrite: "auto" }); };
    titles.forEach((t, i) => { if (i) G.set([t, ...$$("[data-sc-mitem]", t.closest("article"))], { opacity: 0 }); });
    S.onLoaderDone.push(() => reveal(0));
    S.watchCarousel(track, (next, prev) => { setActive(next); const old = titles[prev]; G.to([old, ...$$("[data-sc-mitem]", old.closest("article"))], { opacity: 0, duration: .12, overwrite: "auto" }); reveal(next); });
    dots.forEach((d, i) => d.addEventListener("click", () => S.scrollCarouselTo(track, i)));
  }

  /* ================= intro + reveals ================= */
  S.initReveals($(".col-intro")); S.initReveals($(".catalog")); S.initReveals($(".cross"));

  /* ================= filters with Flip ================= */
  const grid = $("[data-grid]"), cards = $$("[data-product]", grid), empty = $("[data-empty]");
  const state = { colour: "", style: "", price: "", sort: "default" };
  const qs = new URLSearchParams(location.search); if (qs.get("colour")) state.colour = qs.get("colour"); if (qs.get("style")) state.style = qs.get("style");
  const passes = (c) => { const cols = c.dataset.colours.split(","), price = +c.dataset.price; if (state.colour && cols.indexOf(state.colour) < 0) return false; if (state.style && c.dataset.style !== state.style) return false; if (state.price) { const [lo, hi] = state.price.split("-").map(Number); if (price < lo || price > hi) return false; } return true; };
  const sorters = { default: (a, b) => +a.dataset.index - +b.dataset.index, "price-asc": (a, b) => +a.dataset.price - +b.dataset.price, "price-desc": (a, b) => +b.dataset.price - +a.dataset.price, name: (a, b) => a.dataset.name.localeCompare(b.dataset.name) };
  const apply = (animate) => {
    const st = animate && Flip && !reduced ? Flip.getState(cards) : null;
    cards.slice().sort(sorters[state.sort] || sorters.default).forEach((c) => grid.appendChild(c));
    let k = 0; cards.forEach((c) => { const ok = passes(c); c.classList.toggle("is-hidden", !ok); if (ok) k++; });
    $$("[data-count]").forEach((el) => el.textContent = k);
    empty.classList.toggle("is-on", k === 0);
    $$("[data-clear]").forEach((b) => b.classList.toggle("is-on", !!(state.colour || state.style || state.price)));
    ["colour", "style", "price"].forEach((key) => $$('[data-filter="' + key + '"]').forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.value === state[key]))));
    if (st) Flip.from(st, { duration: .7, ease: "power3.out", stagger: .03, absolute: true, scale: true, onEnter: (els) => G.fromTo(els, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .5, ease: "power2.out" }), onLeave: (els) => G.to(els, { opacity: 0, y: 12, duration: .3 }) });
    ST.refresh();
  };
  $$("[data-filter]").forEach((b) => b.addEventListener("click", () => { const k = b.dataset.filter, v = b.dataset.value; state[k] = state[k] === v ? "" : v; apply(true); }));
  $$("[data-clear]").forEach((b) => b.addEventListener("click", () => { state.colour = state.style = state.price = ""; apply(true); }));
  const sort = $("[data-sort]"); sort && sort.addEventListener("change", () => { state.sort = sort.value; apply(true); });
  if (state.colour || state.style) apply(false);

  /* ---- colour option swaps the card image ---- */
  cards.concat($$(".cross [data-product]")).forEach((card) => { const btn = $("[data-add]", card); $$("[data-colour-opts] input", card).forEach((r) => r.addEventListener("change", () => { btn.dataset.colour = r.value; const p = S.product(card.dataset.product); const im = p.cutouts.find((c) => c.colour.toLowerCase() === r.value.toLowerCase()); if (im) { const main = $("img.main", card); G.fromTo(main, { opacity: 0 }, { opacity: 1, duration: .4 }); main.src = im.small; } })); });

  /* ================= quick view ================= */
  const qv = $(".qv"), qvb = $(".qv-backdrop"); let open = false, last = null, cur = null, colour = "", size = null;
  const render = () => {
    const p = cur, imgs = p.cutouts.filter((c) => c.colour.toLowerCase() === colour.toLowerCase());
    const main = $("[data-qv-img]", qv); main.src = imgs[0].src; main.alt = p.name + " in " + colour;
    $("[data-qv-thumbs]", qv).innerHTML = imgs.map((im, i) => '<button type="button" aria-pressed="' + (i === 0) + '" aria-label="View ' + (i + 1) + '"><img src="' + im.small + '" alt="" width="100" height="100"></button>').join("");
    $$("[data-qv-thumbs] button", qv).forEach((b, i) => b.addEventListener("click", () => { $$("[data-qv-thumbs] button", qv).forEach((x) => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); G.fromTo(main, { opacity: 0 }, { opacity: 1, duration: .4 }); main.src = imgs[i].src; }));
    $("[data-qv-colour]", qv).textContent = colour;
    $("[data-qv-opts]", qv).innerHTML = p.colours.map((c) => '<label class="opt"><input type="radio" name="qv-colour" value="' + c + '"' + (c === colour ? " checked" : "") + '><span class="sw" style="--sw:' + (SWATCH[c] || "#6E4328") + '"></span>' + c + "</label>").join("");
    $$("[data-qv-opts] input", qv).forEach((r) => r.addEventListener("change", () => { colour = r.value; render(); }));
    const sz = $("[data-qv-sizes]", qv);
    if (p.sizes) { sz.hidden = false; $("[data-qv-size]", qv).textContent = size; $("[data-qv-size-opts]", qv).innerHTML = p.sizes.options.map((s) => '<label class="opt"><input type="radio" name="qv-size" value="' + s + '"' + (s === size ? " checked" : "") + ">" + s + "</label>").join(""); $$("[data-qv-size-opts] input", qv).forEach((r) => r.addEventListener("change", () => { size = +r.value; $("[data-qv-size]", qv).textContent = size; })); } else sz.hidden = true;
    $("[data-qv-add]", qv).onclick = () => { S.addToCart(p.id, colour, size, 1); closeQv(); };
  };
  const openQv = (id) => {
    cur = COLLECTION.find((p) => p.id === id); if (!cur) return; colour = cur.defaultColour; size = cur.sizes ? (cur.sizes.options[2] || cur.sizes.options[0]) : null; last = document.activeElement;
    $("[data-qv-num]", qv).textContent = "STAGR." + String(COLLECTION.indexOf(cur) + 1).padStart(2, "0");
    $("[data-qv-meta]", qv).textContent = cur.style || "Belt";
    $("[data-qv-name]", qv).innerHTML = cur.name.split(" ")[0] + '<span class="dotc">.</span>';
    $("[data-qv-sub]", qv).textContent = cur.name; $("[data-qv-tagline]", qv).textContent = cur.tagline;
    $("[data-qv-price]", qv).innerHTML = S.fmt(cur.price) + (cur.compareAtPrice ? '<s class="small muted" style="margin-left:.5em">' + S.fmt(cur.compareAtPrice) + "</s>" : "");
    $("[data-qv-link]", qv).href = "product-" + cur.id + ".html";
    render(); qv.classList.add("is-open"); qvb.classList.add("is-open"); qv.setAttribute("aria-hidden", "false"); open = true; S.lock("qv");
    setTimeout(() => $(".qv-close", qv).focus(), 300);
  };
  const closeQv = () => { if (!open) return; qv.classList.remove("is-open"); qvb.classList.remove("is-open"); qv.setAttribute("aria-hidden", "true"); open = false; S.unlock("qv"); last && last.focus && last.focus(); };
  S.closeOverlay = closeQv;
  document.addEventListener("click", (e) => { const b = e.target.closest("[data-quick]"); if (b) { e.preventDefault(); openQv(b.dataset.quick); } });
  $$("[data-qv-close]").forEach((b) => b.addEventListener("click", closeQv));
}
STAGR.onReady.push(initAnimations);
'''.replace("__PRODUCTS__", products_json)

    return {
        "file": f"{line}s.html",
        "key": line + "s",
        "title": f"{title} — STAGR.",
        "description": blurb,
        "css": css,
        "body": body,
        "js": js,
        "header_dark": True,
        "shop_href": "#filters",
    }


def render(ctx):
    return [page(ctx, "wallet"), page(ctx, "belt")]
