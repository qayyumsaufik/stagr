"""wallets.html and belts.html — collection pages (one module, two outputs)."""
import json

SWATCH = {"Brown": "#7B4A2B", "Black": "#1A1512", "Tan": "#B0773F", "Coffee": "#4A3024"}


def card(ctx, p, i):
    fmt = lambda n: "Rs " + format(n, ",d")
    a, b = p["images"][0], (p["images"][1] if len(p["images"]) > 1 else p["images"][0])
    meta = (p["style"] or "Belt") + " · " + " / ".join(p["colours"])
    swatches = "".join(f'<span class="dot" style="--sw:{SWATCH.get(c, "#7B4A2B")}" title="{c}"></span>' for c in p["colours"])
    save = round((1 - p["price"] / p["compareAtPrice"]) * 100) if p.get("compareAtPrice") else 0
    return f'''
<article class="card" data-item data-id="{p["id"]}" data-colours="{",".join(p["colours"])}" data-style="{p["style"] or "Belt"}" data-price="{p["price"]}" data-index="{i}" data-name="{p["name"]}">
  <div class="card-top">
  <a class="card-link" href="product-{p["id"]}.html" data-cursor="View" aria-label="{p["name"]}">
    <div class="media media--studio">
      <img src="{a["src"]}" srcset="{a["srcSmall"]} 800w, {a["src"]} 1600w" sizes="(min-width: 1024px) 30vw, 50vw" alt="{a["alt"]}" width="{a["width"]}" height="{a["height"]}" loading="lazy">
      <img class="alt" src="{b["src"]}" srcset="{b["srcSmall"]} 800w, {b["src"]} 1600w" sizes="(min-width: 1024px) 30vw, 50vw" alt="" width="{b["width"]}" height="{b["height"]}" loading="lazy" aria-hidden="true">
      {f'<span class="badge">Save {save}%</span>' if save else ''}
    </div>
  </a>
  <button type="button" class="btn btn--sm btn--wide quick" data-quick="{p["id"]}">Quick view</button>
  </div>
  <div class="card-body">
    <div><a class="card-name" href="product-{p["id"]}.html">{p["name"]}</a><div class="card-meta">{meta}</div><div class="card-dots">{swatches}</div><div class="card-rule"></div></div>
    <div class="price">{fmt(p["price"])}{f'<s>{fmt(p["compareAtPrice"])}</s>' if p.get("compareAtPrice") else ''}</div>
  </div>
</article>'''


def page(ctx, line):
    P = [p for p in ctx["products"] if p["line"] == line]
    B = ctx["brand"]
    I = ctx["icon"]
    other = "belt" if line == "wallet" else "wallet"
    L = B["lines"][line] if "lines" in B else None
    title = "Wallets" if line == "wallet" else "Belts"
    other_title = "Belts" if line == "wallet" else "Wallets"
    blurb = ctx["products_doc"]["lines"][line]["blurb"]
    hero_img = ("assets/lifestyle/upbuck-open.jpg", "Upbuck long wallet open with cards on burlap", 1800, 1200) if line == "wallet" else ("assets/lifestyle/heritage-02.jpg", "Three Stagr belts in tan, brown and black laid on wood", 1200, 1500)
    colours = sorted({c for p in P for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black", "Coffee"].index(c) if c in ["Brown", "Tan", "Black", "Coffee"] else 9)
    styles = sorted({p["style"] for p in P if p["style"]}, key=lambda s: ["Bifold", "Trifold", "Minimalist", "Long"].index(s) if s in ["Bifold", "Trifold", "Minimalist", "Long"] else 9)
    cards = "".join(card(ctx, p, i) for i, p in enumerate(P))
    colour_pills = "".join(f'<button type="button" class="pill" data-filter="colour" data-value="{c}" aria-pressed="false"><span class="dot" style="--sw:{SWATCH.get(c, "#7B4A2B")}"></span>{c}</button>' for c in colours)
    style_pills = "".join(f'<button type="button" class="pill" data-filter="style" data-value="{s}" aria-pressed="false">{s}</button>' for s in styles)
    price_pills = ('<button type="button" class="pill" data-filter="price" data-value="0-2000" aria-pressed="false">Under Rs 2,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="2000-3000" aria-pressed="false">Rs 2,000 – 3,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="3000-99999" aria-pressed="false">Over Rs 3,000</button>')
    prices = [p["price"] for p in P]
    cross = [p for p in ctx["products"] if p["line"] == other][:3]
    cross_cards = "".join(card(ctx, p, i) for i, p in enumerate(cross))
    products_json = json.dumps([{k: p[k] for k in ("id", "name", "style", "tagline", "price", "compareAtPrice", "colours", "defaultColour", "images", "line")} for p in P], ensure_ascii=False).replace("</", "<\\/")

    css = r'''
.col-hero { padding-top: calc(var(--header-h) + clamp(40px, 8vw, 96px)); padding-bottom: clamp(40px, 6vw, 80px); }
.col-hero .grid { align-items: end; }
.col-hero .display { max-width: 9ch; }
.col-hero .lead { margin-top: 24px; }
.col-hero .count { margin-top: 32px; }
.col-hero-img { --ar: 4 / 5; }
@media (min-width: 768px) { .col-hero-img { --ar: 3 / 4; } }
.col-hero-img.media-wide { --ar: 3 / 2; }

/* filter bar */
.filters { position: relative; z-index: 3; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 16px 0; }
.filters .wrap { display: grid; gap: 14px; }
.filter-groups { display: flex; flex-wrap: wrap; gap: 20px 32px; align-items: center; }
.filter-group { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.filter-group .label { color: var(--ink-3); margin-right: 4px; }
.filter-group .pill { min-height: 40px; padding: 0 16px; }
.filters .select { min-height: 40px; width: auto; padding: 0 32px 0 0; font-size: var(--fs-small); font-weight: 600; }
.filter-meta { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
.filter-meta .clear { display: none; }
.filter-meta .clear.is-on { display: inline-flex; }
@media (min-width: 1024px) { .filters .wrap { grid-template-columns: 1fr auto; align-items: center; } .filter-meta { justify-content: flex-end; } }

/* sticky mini nav */
.mini-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 85; background: var(--bg); border-bottom: 1px solid var(--line); transform: translateY(-110%); transition: transform .5s var(--ease-out); }
.mini-nav.is-on { transform: none; }
.mini-nav .wrap { display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 56px; }
.mini-nav .mn-title { font-family: var(--font-display); font-size: 1.25rem; display: flex; align-items: baseline; gap: 10px; }
.mini-nav .mn-title .small { color: var(--ink-3); }
.mini-nav .mn-actions { display: flex; gap: 8px; }
.mini-nav .mn-actions .btn { --h: 38px; padding: 0 16px; }

/* grid */
.catalog { padding-block: clamp(40px, 6vw, 80px) var(--section); }
.product-grid { display: grid; gap: clamp(16px, 2.4vw, 32px) var(--gap); grid-template-columns: repeat(2, minmax(0, 1fr)); position: relative; }
@media (min-width: 1024px) { .product-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (min-width: 1440px) { .product-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.product-grid .card.is-hidden { display: none; }
.card .card-link { display: block; }
.card .card-dots { display: flex; gap: 6px; margin-top: 8px; }
.card .card-dots .dot { width: 12px; height: 12px; border-radius: 50%; background: var(--sw); box-shadow: inset 0 0 0 1px rgba(0,0,0,.2); }
.card .card-top { position: relative; }
.empty { display: none; padding: 64px 0; text-align: center; }
.empty.is-on { display: block; }

/* quick view */
.qv-backdrop { position: fixed; inset: 0; z-index: 100; background: var(--overlay); opacity: 0; visibility: hidden; transition: opacity .4s ease, visibility 0s linear .4s; }
.qv-backdrop.is-open { opacity: 1; visibility: visible; transition-delay: 0s; }
.qv { position: fixed; z-index: 101; inset: auto 0 0 0; max-height: 92svh; overflow: auto; background: var(--bg); color: var(--ink); transform: translateY(102%); visibility: hidden; transition: transform .6s var(--ease-out), visibility 0s linear .6s; border-radius: 12px 12px 0 0; }
.qv.is-open { transform: none; visibility: visible; transition-delay: 0s; }
@media (min-width: 1024px) { .qv { inset: 50% auto auto 50%; width: min(960px, 92vw); max-height: 88vh; transform: translate(-50%, -50%) scale(.96); opacity: 0; border-radius: 4px; transition: transform .5s var(--ease-out), opacity .4s ease, visibility 0s linear .5s; visibility: hidden; } .qv.is-open { transform: translate(-50%, -50%) scale(1); opacity: 1; visibility: visible; transition-delay: 0s; } }
.qv-inner { display: grid; }
@media (min-width: 1024px) { .qv-inner { grid-template-columns: 1fr 1fr; } }
.qv-media { position: relative; }
.qv-media .media { --ar: 1 / 1; border-radius: 0; }
@media (min-width: 1024px) { .qv-media .media { --ar: 4 / 5; height: 100%; } }
.qv-thumbs { position: absolute; left: 16px; bottom: 16px; display: flex; gap: 8px; }
.qv-thumbs button { width: 48px; height: 48px; border-radius: 4px; overflow: hidden; background: #F2EFEA; border: 2px solid transparent; }
.qv-thumbs button[aria-pressed="true"] { border-color: var(--ink); }
.qv-thumbs img { width: 100%; height: 100%; object-fit: contain; mix-blend-mode: multiply; }
.qv-body { padding: clamp(20px, 3vw, 40px); display: grid; gap: 18px; align-content: start; }
.qv-close { position: absolute; top: 12px; right: 12px; z-index: 2; }
.qv .h3 { max-width: 14ch; }
'''

    body = f'''
<section class="col-hero" aria-labelledby="col-title">
  <div class="wrap grid">
    <div class="col-12 lg:col-6">
      <p class="label label-row" data-reveal="up">Collection · {len(P)} styles</p>
      <h1 class="display" id="col-title" data-lines="now" data-delay=".2" style="margin-top:20px">{title}</h1>
      <p class="lead" data-reveal="up" data-delay=".5">{blurb}</p>
      <p class="small muted count" data-reveal="up" data-delay=".6">From {"Rs " + format(min(prices), ",d")} to {"Rs " + format(max(prices), ",d")} · Cash on delivery · 3 to 5 days across Pakistan</p>
    </div>
    <div class="col-12 lg:col-5 lg:start-8">
      <div class="media col-hero-img {"media-wide" if line == "wallet" else ""} reveal-img" data-from="right"><img src="{hero_img[0]}" srcset="{hero_img[0].replace('.jpg', '-800.jpg')} 800w, {hero_img[0]} 1600w" sizes="(min-width: 1024px) 40vw, 100vw" alt="{hero_img[1]}" width="{hero_img[2]}" height="{hero_img[3]}" fetchpriority="high"></div>
    </div>
  </div>
</section>

<div class="mini-nav" aria-hidden="true">
  <div class="wrap">
    <span class="mn-title">{title} <span class="small" data-count-mini>{len(P)}</span></span>
    <div class="mn-actions"><button type="button" class="btn btn--ghost btn--sm" data-scroll-to="#filters">Filters</button><a class="btn btn--ghost btn--sm" href="{other}s.html">{other_title}</a></div>
  </div>
</div>

<section class="filters" id="filters" aria-label="Filter and sort">
  <div class="wrap">
    <div class="filter-groups" data-stagger=".04">
      <div class="filter-group"><span class="label">Colour</span><button type="button" class="pill" data-filter="colour" data-value="" aria-pressed="true">All</button>{colour_pills}</div>
      {f'<div class="filter-group"><span class="label">Style</span><button type="button" class="pill" data-filter="style" data-value="" aria-pressed="true">All</button>{style_pills}</div>' if styles else ''}
      <div class="filter-group"><span class="label">Leather</span><button type="button" class="pill" aria-pressed="true" disabled title="Every Stagr piece is crazy horse leather">Crazy horse</button></div>
      <div class="filter-group"><span class="label">Price</span><button type="button" class="pill" data-filter="price" data-value="" aria-pressed="true">All</button>{price_pills}</div>
    </div>
    <div class="filter-meta">
      <span class="small muted"><span data-count>{len(P)}</span> pieces</span>
      <button type="button" class="btn btn--flat btn--sm clear" data-clear>Clear filters</button>
      <label class="sr-only" for="sort">Sort</label>
      <select class="select" id="sort" data-sort><option value="default">Featured</option><option value="price-asc">Price, low to high</option><option value="price-desc">Price, high to low</option><option value="name">Name, A to Z</option></select>
    </div>
  </div>
</section>

<section class="catalog" aria-label="{title}">
  <div class="wrap">
    <div class="product-grid" data-grid data-stagger=".07">{cards}</div>
    <div class="empty" data-empty><p class="h3">Nothing matches that yet.</p><p class="muted" style="margin-top:10px">Loosen a filter and the shelf fills up again.</p><p style="margin-top:24px"><button type="button" class="btn btn--ghost btn--sm" data-clear>Clear filters</button></p></div>
  </div>
</section>

<section class="section-sm theme-dark" aria-labelledby="cross-title">
  <div class="wrap">
    <div class="between" style="margin-bottom:clamp(28px,4vw,48px)"><div><p class="label label-row" data-reveal="up" style="color:var(--c-saddle)">Complete the look</p><h2 class="h2" id="cross-title" data-lines style="margin-top:16px">{"A belt to match" if line == "wallet" else "A wallet to match"}</h2></div><a class="btn btn--ghost" href="{other}s.html">All {other_title.lower()}</a></div>
    <div class="product-grid" style="grid-template-columns:repeat(3,minmax(0,1fr))" data-stagger=".08">{cross_cards}</div>
  </div>
</section>

<section class="trust-section" aria-label="Delivery, returns and service">
  <div class="wrap"><div class="trust" data-stagger=".08">{"".join(f'<div class="trust-item"><span class="t">{t["title"]}</span><span class="s">{t["sub"]}</span></div>' for t in B["trust"]["items"])}</div></div>
</section>

<div class="qv-backdrop" data-qv-close aria-hidden="true"></div>
<div class="qv" role="dialog" aria-modal="true" aria-label="Quick view" aria-hidden="true" data-lenis-prevent>
  <button type="button" class="btn btn--icon qv-close" data-qv-close aria-label="Close quick view">{I["close"]}</button>
  <div class="qv-inner">
    <div class="qv-media"><div class="media media--studio"><img data-qv-img src="" alt="" width="1448" height="1086"></div><div class="qv-thumbs" data-qv-thumbs></div></div>
    <div class="qv-body">
      <p class="label" data-qv-meta></p>
      <h2 class="h3" data-qv-name></h2>
      <p class="price h4" data-qv-price></p>
      <p class="muted" data-qv-tagline></p>
      <div><p class="label" style="margin-bottom:10px">Colour · <span data-qv-colour style="text-transform:none;letter-spacing:0"></span></p><div class="swatches" data-qv-swatches></div></div>
      <div class="row" style="gap:12px"><button type="button" class="btn" data-qv-add>Add to cart</button><a class="btn btn--flat" data-qv-link href="#">Full details {I["arrow"]}</a></div>
      <p class="small muted">Cash on delivery · 3 to 5 days across Pakistan · 14-day returns</p>
    </div>
  </div>
</div>
'''

    js = r'''
const COLLECTION = __PRODUCTS__;
const SWATCH = { Brown: "#7B4A2B", Black: "#1A1512", Tan: "#B0773F", Coffee: "#4A3024" };
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, Flip = window.Flip;
  const q = (s, r) => (r || document).querySelector(s), qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const grid = q("[data-grid]"), cards = qa("[data-item]", grid), empty = q("[data-empty]");
  const state = { colour: "", style: "", price: "", sort: "default" };

  /* ---- sticky mini nav after the editorial header scrolls out ---- */
  const mini = q(".mini-nav"), hero = q(".col-hero");
  if (mini && hero) {
    const check = () => { const r = hero.getBoundingClientRect(); const on = r.bottom < 0; mini.classList.toggle("is-on", on); mini.setAttribute("aria-hidden", String(!on)); };
    window.addEventListener("scroll", check, { passive: true }); check();
  }

  /* ---- filters with Flip ---- */
  const passes = c => {
    const colours = c.dataset.colours.split(","), price = +c.dataset.price;
    if (state.colour && colours.indexOf(state.colour) < 0) return false;
    if (state.style && c.dataset.style !== state.style) return false;
    if (state.price) { const [lo, hi] = state.price.split("-").map(Number); if (price < lo || price > hi) return false; }
    return true;
  };
  const sorters = { default: (a, b) => +a.dataset.index - +b.dataset.index, "price-asc": (a, b) => +a.dataset.price - +b.dataset.price, "price-desc": (a, b) => +b.dataset.price - +a.dataset.price, name: (a, b) => a.dataset.name.localeCompare(b.dataset.name) };
  const apply = () => {
    const state0 = Flip && G && !S.reduced ? Flip.getState(cards) : null;
    cards.slice().sort(sorters[state.sort] || sorters.default).forEach(c => grid.appendChild(c));
    let n = 0;
    cards.forEach(c => { const ok = passes(c); c.classList.toggle("is-hidden", !ok); if (ok) n++; });
    qa("[data-count], [data-count-mini]").forEach(el => el.textContent = n);
    empty.classList.toggle("is-on", n === 0);
    const active = !!(state.colour || state.style || state.price);
    qa("[data-clear]").forEach(b => b.classList.toggle("is-on", active));
    if (state0) Flip.from(state0, { duration: .8, ease: "power3.out", stagger: .03, absolute: true, scale: true, onEnter: els => G.fromTo(els, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .6, ease: "power3.out" }), onLeave: els => G.to(els, { opacity: 0, y: 16, duration: .35 }) });
    ST && ST.refresh();
  };
  qa("[data-filter]").forEach(b => b.addEventListener("click", () => {
    const k = b.dataset.filter, v = b.dataset.value;
    state[k] = state[k] === v ? "" : v;
    qa('[data-filter="' + k + '"]').forEach(x => x.setAttribute("aria-pressed", String(x.dataset.value === state[k])));
    apply();
  }));
  qa("[data-clear]").forEach(b => b.addEventListener("click", () => { state.colour = state.style = state.price = ""; qa("[data-filter]").forEach(x => x.setAttribute("aria-pressed", String(x.dataset.value === ""))); apply(); }));
  const sort = q("[data-sort]"); sort && sort.addEventListener("change", () => { state.sort = sort.value; apply(); });

  /* ---- quick view ---- */
  const qv = q(".qv"), qvb = q(".qv-backdrop"); let qvOpen = false, last = null, cur = null, colour = "";
  const fmt = S.fmt;
  const renderQv = () => {
    const p = cur; const imgs = p.images.filter(i => i.colour.toLowerCase() === colour.toLowerCase());
    const main = q("[data-qv-img]", qv); main.src = imgs[0].src; main.alt = imgs[0].alt;
    q("[data-qv-thumbs]", qv).innerHTML = imgs.map((im, i) => '<button type="button" aria-pressed="' + (i === 0) + '" aria-label="View ' + (i + 1) + '"><img src="' + im.srcSmall + '" alt="" width="200" height="150"></button>').join("");
    qa("[data-qv-thumbs] button", qv).forEach((b, i) => b.addEventListener("click", () => { qa("[data-qv-thumbs] button", qv).forEach(x => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); if (G && !S.reduced) G.fromTo(main, { opacity: 0 }, { opacity: 1, duration: .4 }); main.src = imgs[i].src; }));
    q("[data-qv-colour]", qv).textContent = colour;
    q("[data-qv-swatches]", qv).innerHTML = p.colours.map(c => '<label class="swatch" style="--sw:' + (SWATCH[c] || "#7B4A2B") + '"><input type="radio" name="qv-colour" value="' + c + '"' + (c === colour ? " checked" : "") + '><span class="sw"></span><span class="sr-only">' + c + '</span></label>').join("");
    qa("[data-qv-swatches] input", qv).forEach(r => r.addEventListener("change", () => { colour = r.value; renderQv(); }));
    q("[data-qv-add]", qv).onclick = () => { S.addToCart(p.id, colour, null, 1); closeQv(); };
  };
  const openQv = id => {
    cur = COLLECTION.find(p => p.id === id); if (!cur || !qv) return; colour = cur.defaultColour; last = document.activeElement;
    q("[data-qv-meta]", qv).textContent = (cur.style || "Belt") + " · Crazy horse leather";
    q("[data-qv-name]", qv).textContent = cur.name;
    q("[data-qv-price]", qv).innerHTML = fmt(cur.price) + (cur.compareAtPrice ? "<s>" + fmt(cur.compareAtPrice) + "</s>" : "");
    q("[data-qv-tagline]", qv).textContent = cur.tagline;
    q("[data-qv-link]", qv).href = "product-" + cur.id + ".html";
    renderQv();
    qv.classList.add("is-open"); qvb.classList.add("is-open"); qv.setAttribute("aria-hidden", "false"); qvOpen = true; S.lock(true);
    setTimeout(() => q(".qv-close", qv).focus(), 300);
  };
  const closeQv = () => { if (!qvOpen) return; qv.classList.remove("is-open"); qvb.classList.remove("is-open"); qv.setAttribute("aria-hidden", "true"); qvOpen = false; S.lock(false); last && last.focus && last.focus(); };
  S.closeLightbox = closeQv;
  document.addEventListener("click", e => { const b = e.target.closest("[data-quick]"); if (b) { e.preventDefault(); openQv(b.dataset.quick); } });
  qa("[data-qv-close]").forEach(b => b.addEventListener("click", closeQv));
}
STAGR.onReady.push(initAnimations);
'''.replace("__PRODUCTS__", products_json)

    return {
        "file": f"{line}s.html",
        "title": f"{title} — handmade crazy horse leather",
        "description": blurb,
        "css": css,
        "body": body,
        "js": js,
    }


def render(ctx):
    return [page(ctx, "wallet"), page(ctx, "belt")]
