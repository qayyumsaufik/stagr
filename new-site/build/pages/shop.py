"""shop.html — every piece in one filterable grid.

The collection pages open with the showcase and one section per category;
this page is the full shelf: Wallets / Belts tabs, colour, style and price
filters, sort, Flip-animated grid and the shared quick view. Reached from
"View all" in the mega menu, from the collection pages and from the nav.
Query: ?line=wallets|belts  ?colour=Brown  ?style=Bifold
"""

SWATCH = {"Brown": "#6E4328", "Black": "#1A1512", "Tan": "#B0773F", "Coffee": "#4A3024"}


def render(ctx):
    P = ctx["products"]
    B = ctx["brand"]
    I = ctx["icon"]
    fmt = lambda n: "Rs " + format(n, ",d")
    colours = sorted({c for p in P for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black"].index(c) if c in ["Brown", "Tan", "Black"] else 9)
    styles = ["Bifold", "Trifold", "Minimalist", "Long", "Belt"]
    cards = "".join(ctx["pcard"](ctx, p, i, reveal=False) for i, p in enumerate(P))
    n_w = len([p for p in P if p["line"] == "wallet"]); n_b = len(P) - n_w
    colour_pills = "".join(f'<button type="button" class="pill" data-filter="colour" data-value="{c}" aria-pressed="false"><span class="sw" style="--sw:{SWATCH.get(c, "#6E4328")}"></span>{c}</button>' for c in colours)
    style_pills = "".join(f'<button type="button" class="pill" data-filter="style" data-value="{s}" aria-pressed="false">{s}{"s" if s == "Belt" else ""}</button>' for s in styles)
    price_pills = ('<button type="button" class="pill" data-filter="price" data-value="0-2000" aria-pressed="false">Under Rs 2,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="2000-3000" aria-pressed="false">Rs 2,000 – 3,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="3000-99999" aria-pressed="false">Over Rs 3,000</button>')

    css = r'''
.shop-hero { padding: calc(var(--nav-top) + clamp(32px, 5vw, 72px)) 0 clamp(24px, 3vw, 40px); }
.shop-hero .display { font-size: clamp(2.8rem, 1.6rem + 4.5vw, 6rem); line-height: .98; margin-top: 14px; }
.shop-hero .lead { margin-top: 18px; }
.line-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-top: clamp(24px, 3vw, 40px); }
.ctab { min-height: 44px; padding: 0 20px; border: 1px solid var(--line-strong); font-size: .75rem; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: var(--fg); transition: background-color .3s ease, color .3s ease, border-color .3s ease; }
.ctab:hover { border-color: var(--fg); }
.ctab[aria-selected="true"] { background: var(--ink); color: var(--bone); border-color: var(--ink); }
.ctab small { opacity: .55; margin-left: 6px; letter-spacing: .08em; }

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
.catalog { padding: 0; }
.catalog-body { padding-block: clamp(32px, 5vw, 64px) var(--section-sm); }
.shop-grid { display: grid; gap: 16px; grid-template-columns: 1fr; }
@media (min-width: 640px) { .shop-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .shop-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; } }
@media (min-width: 1440px) { .shop-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.pcard.is-hidden { display: none; }
.empty { display: none; padding: 64px 0; text-align: center; }
.empty.is-on { display: block; }
.delivery { display: grid; gap: 28px; padding: var(--section-sm) 0; border-top: 1px solid var(--line); }
@media (min-width: 768px) { .delivery { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.delivery h3 { font-family: var(--font-display); font-weight: 300; font-size: 1.5rem; }
.delivery p { color: var(--fg-2); font-size: .9375rem; margin-top: 8px; max-width: 26ch; }
.back-lines { padding: 0 0 var(--section-sm); display: grid; gap: 16px; }
@media (min-width: 768px) { .back-lines { grid-template-columns: 1fr 1fr; } }
.back-line { position: relative; display: grid; align-content: end; min-height: 320px; padding: 28px; color: var(--bone); background: var(--ink); overflow: hidden; }
.back-line img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .72; transition: transform 1.2s var(--ease-out); }
.back-line:hover img { transform: scale(1.04); }
.back-line > * { position: relative; }
.back-line .h3 { margin-top: 8px; display: flex; align-items: center; gap: 10px; }
.back-line svg { width: 1em; height: 1em; flex: 0 0 auto; }
'''

    body = f'''
<section class="shop-hero on-bone" aria-labelledby="shop-title">
  <div class="wrap">
    <p class="label" data-reveal><b>01</b><span class="slash">/</span>The shop · {len(P)} pieces</p>
    <h1 class="display" id="shop-title" data-text-reveal="chars">Every piece<span class="dotc">.</span></h1>
    <p class="lead" data-reveal data-delay=".2">{B["descriptor"]} Cash on delivery across Pakistan, free over {fmt(B.get("freeDeliveryThreshold", 5000))}.</p>
    <div class="line-tabs" role="tablist" aria-label="Line" data-reveal data-delay=".3">
      <button type="button" class="ctab" role="tab" aria-selected="true" data-line="">All <small>{len(P)}</small></button>
      <button type="button" class="ctab" role="tab" aria-selected="false" data-line="wallet">Wallets <small>{n_w}</small></button>
      <button type="button" class="ctab" role="tab" aria-selected="false" data-line="belt">Belts <small>{n_b}</small></button>
    </div>
  </div>
</section>

<section class="catalog on-bone" aria-label="All pieces">
<div class="filters" id="filters" aria-label="Filter and sort">
  <div class="wrap">
    <div class="filter-groups">
      <div class="filter-group"><span class="label">Colour</span><button type="button" class="pill" data-filter="colour" data-value="" aria-pressed="true">All</button>{colour_pills}</div>
      <div class="filter-group"><span class="label">Style</span><button type="button" class="pill" data-filter="style" data-value="" aria-pressed="true">All</button>{style_pills}</div>
      <div class="filter-group"><span class="label">Price</span><button type="button" class="pill" data-filter="price" data-value="" aria-pressed="true">All</button>{price_pills}</div>
    </div>
    <div class="filter-meta">
      <span class="small muted"><span data-count>{len(P)}</span> pieces</span>
      <button type="button" class="btn btn--text clear" data-clear>Clear</button>
      <label class="sr-only" for="sort">Sort</label>
      <select class="select" id="sort" data-sort><option value="default">Featured</option><option value="price-asc">Price, low to high</option><option value="price-desc">Price, high to low</option><option value="name">Name, A to Z</option></select>
    </div>
  </div>
</div>
  <div class="wrap catalog-body">
    <div class="shop-grid" data-grid>{cards}</div>
    <div class="empty" data-empty><p class="h3">Nothing matches that yet.</p><p class="muted" style="margin-top:10px">Loosen a filter and the shelf fills up again.</p><p style="margin-top:24px"><button type="button" class="btn btn--ghost btn--sm" data-clear>Clear filters</button></p></div>
  </div>
</section>

<section class="shop-more on-bone" aria-label="Collections and delivery">
  <div class="wrap">
    <div class="back-lines">
      <a class="back-line" href="wallets.html"><img src="assets/lifestyle/kingsmen-02-800.jpg" alt="" width="800" height="1000" loading="lazy"><span class="label" style="color:rgba(239,237,230,.7)">Collection</span><span class="h3">Wallets, by category {I["arrow"]}</span></a>
      <a class="back-line" href="belts.html"><img src="assets/lifestyle/ranger-wide-800.jpg" alt="" width="800" height="450" loading="lazy"><span class="label" style="color:rgba(239,237,230,.7)">Collection</span><span class="h3">Belts, by category {I["arrow"]}</span></a>
    </div>
    <div class="delivery">{"".join(f'<div data-reveal data-delay="{i * .1}"><h3>{t["title"]}</h3><p>{t["sub"]}</p></div>' for i, t in enumerate(B["trust"]["items"]))}</div>
  </div>
</section>
'''

    js = r'''
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, Flip = window.Flip, $ = S.$, $$ = S.$$, reduced = S.reduced;
  if (!G) return;
  S.initReveals($(".shop-hero")); S.initReveals($(".shop-more")); S.initReveals($("footer"));

  const grid = $("[data-grid]"), cards = $$("[data-product]", grid), empty = $("[data-empty]"), tabs = $$("[data-line]");
  const state = { line: "", colour: "", style: "", price: "", sort: "default" };
  const qs = new URLSearchParams(location.search);
  const qline = (qs.get("line") || "").toLowerCase(); if (qline.startsWith("wallet")) state.line = "wallet"; else if (qline.startsWith("belt")) state.line = "belt";
  if (qs.get("colour")) state.colour = qs.get("colour"); if (qs.get("style")) state.style = qs.get("style");
  const passes = (c) => {
    if (state.line && c.dataset.line !== state.line) return false;
    if (state.colour && c.dataset.colours.split(",").indexOf(state.colour) < 0) return false;
    if (state.style && c.dataset.style !== state.style) return false;
    if (state.price) { const [lo, hi] = state.price.split("-").map(Number), price = +c.dataset.price; if (price < lo || price > hi) return false; }
    return true;
  };
  const sorters = { default: (a, b) => +a.dataset.index - +b.dataset.index, "price-asc": (a, b) => +a.dataset.price - +b.dataset.price, "price-desc": (a, b) => +b.dataset.price - +a.dataset.price, name: (a, b) => a.dataset.name.localeCompare(b.dataset.name) };
  const sync = () => {
    const p = new URLSearchParams(); if (state.line) p.set("line", state.line + "s"); if (state.colour) p.set("colour", state.colour); if (state.style) p.set("style", state.style);
    const q = p.toString(); history.replaceState(null, "", location.pathname + (q ? "?" + q : ""));
  };
  const apply = (animate) => {
    const st = animate && Flip && !reduced ? Flip.getState(cards) : null;
    cards.slice().sort(sorters[state.sort] || sorters.default).forEach((c) => grid.appendChild(c));
    let k = 0; cards.forEach((c) => { const ok = passes(c); c.classList.toggle("is-hidden", !ok); if (ok) k++; });
    $$("[data-count]").forEach((el) => el.textContent = k);
    empty.classList.toggle("is-on", k === 0);
    $$("[data-clear]").forEach((b) => b.classList.toggle("is-on", !!(state.colour || state.style || state.price)));
    tabs.forEach((t) => t.setAttribute("aria-selected", String(t.dataset.line === state.line)));
    ["colour", "style", "price"].forEach((key) => $$('[data-filter="' + key + '"]').forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.value === state[key]))));
    if (st) Flip.from(st, { duration: .7, ease: "power3.out", stagger: .03, absolute: true, scale: true, onEnter: (els) => G.fromTo(els, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .5, ease: "power2.out" }), onLeave: (els) => G.to(els, { opacity: 0, y: 12, duration: .3 }) });
    ST.refresh(); sync();
  };
  tabs.forEach((t) => t.addEventListener("click", () => { state.line = t.dataset.line; if (state.line === "belt" && state.style && state.style !== "Belt") state.style = ""; if (state.line === "wallet" && state.style === "Belt") state.style = ""; apply(true); }));
  $$("[data-filter]").forEach((b) => b.addEventListener("click", () => { const k = b.dataset.filter, v = b.dataset.value; state[k] = state[k] === v ? "" : v; apply(true); }));
  $$("[data-clear]").forEach((b) => b.addEventListener("click", () => { state.colour = state.style = state.price = ""; apply(true); }));
  const sort = $("[data-sort]"); sort && sort.addEventListener("change", () => { state.sort = sort.value; apply(true); });
  apply(false);
  // cards rise in once, in grid order
  if (!reduced) G.fromTo(cards.filter((c) => !c.classList.contains("is-hidden")), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .7, ease: "power3.out", stagger: .05, delay: .2, scrollTrigger: { trigger: grid, start: "top 85%", once: true } });
}
STAGR.onReady.push(initAnimations);
'''

    return {
        "file": "shop.html",
        "key": "shop",
        "title": "Shop — STAGR.",
        "description": f"All {len(P)} STAGR. wallets and belts. Filter by colour, style and price. Cash on delivery across Pakistan.",
        "css": css,
        "body": body,
        "js": js,
        "header_dark": False,
        "shop_href": "#filters",
    }
