"""shop.html — every piece in one filterable grid, catalogue style.

Layout follows the reference the client sent (a t-shirt catalogue): title and
tagline, a row of round category thumbnails, dropdown filter pills with an
"All filters" side drawer, a sort control on the right, and a four-column
grid of cards with a badge, a wishlist heart, swatches, sizes and price.
Reached from "View all" in the mega menu, the collection pages and the nav.
Query: ?line=wallets|belts  ?cat=bifold  ?colour=Black,Brown  ?price=0-2000
       ?style=Bifold  ?sort=price-asc
"""
import json

SWATCH = {"Brown": "#6E4328", "Black": "#1A1512", "Tan": "#B0773F", "Coffee": "#4A3024"}
BADGE = {"best": "Bestseller", "new": "New in", "gift": "Gift pick"}
PRICES = [("0-2000", "Under Rs 2,000"), ("2000-3000", "Rs 2,000 – 3,000"), ("3000-99999", "Over Rs 3,000")]


def render(ctx):
    P = ctx["products"]
    B = ctx["brand"]
    I = ctx["icon"]
    cut = ctx["cutouts"]
    TAGS = ctx["tags"]
    by = {p["id"]: p for p in P}
    fmt = lambda n: "Rs " + format(n, ",d")
    colours = sorted({c for p in P for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black"].index(c) if c in ["Brown", "Tan", "Black"] else 9)
    styles = [("Bifold", "wallet"), ("Trifold", "wallet"), ("Minimalist", "wallet"), ("Long", "wallet"), ("Belt", "belt")]
    heart = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 20.5s-7.5-4.6-7.5-10A4.2 4.2 0 0 1 12 8.2a4.2 4.2 0 0 1 7.5 2.3c0 5.4-7.5 10-7.5 10z"/></svg>'
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 9l6 6 6-6"/></svg>'
    sliders = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>'

    # ---- categories: round thumbnails under the title ----
    # scope: which line modes show the category ("" = all pieces, "wallet", "belt")
    cats = [
        dict(key="all", label="All", scope=["", "wallet", "belt"], thumb="kingsmann"),
        dict(key="wallets", label="Wallets", scope=[""], thumb="regal", line="wallet"),
        dict(key="belts", label="Belts", scope=[""], thumb="monarch", line="belt"),
        dict(key="bifold", label="Bifold", scope=["", "wallet"], thumb="kingsmann", style="Bifold"),
        dict(key="trifold", label="Trifold", scope=["", "wallet"], thumb="majestic", style="Trifold"),
        dict(key="minimalist", label="Minimalist", scope=["", "wallet"], thumb="maverick", style="Minimalist"),
        dict(key="long", label="Long wallets", scope=["", "wallet"], thumb="rodeo", style="Long"),
        dict(key="double", label="Double-sided", scope=["", "belt"], thumb="nova", ids=["nova"]),
        dict(key="classic", label="Classic belts", scope=["", "belt"], thumb="outlaw", ids=["outlaw", "regent", "monarch"]),
        dict(key="black-belts", label="Black belts", scope=["belt"], thumb="regent", ids=["regent", "nova"]),
        dict(key="tan-belts", label="Tan belts", scope=["belt"], thumb="monarch", ids=["monarch"]),
    ]
    cats_html = "".join(f'<button type="button" class="sh-cat" role="tab" aria-selected="{str(c["key"] == "all").lower()}" data-cat="{c["key"]}" data-scope="{" ".join(c["scope"])}"><span class="sh-cat-ring"><img src="{cut(by[c["thumb"]])[0]["small"]}" alt="" width="300" height="300" loading="lazy"></span><span class="sh-cat-label">{c["label"]}</span></button>' for c in cats)
    cats_json = json.dumps([{k: v for k, v in c.items() if k in ("key", "line", "style", "ids")} for c in cats]).replace("</", "<\\/")

    cards = "".join(ctx["scard"](ctx, p, i) for i, p in enumerate(P))

    # ---- filter option lists (used twice: in the dropdowns and in the drawer) ----
    def opt(group, value, label, swatch=None):
        return f'<label class="sh-check"><input type="checkbox" data-f="{group}" value="{value}"><span class="sh-box"></span>{f"<span class=sw style=--sw:{swatch}></span>" if swatch else ""}<span class="sh-check-label">{label}</span><em data-count></em></label>'
    colour_opts = "".join(opt("colour", c, c, SWATCH.get(c, "#6E4328")) for c in colours)
    price_opts = "".join(opt("price", v, l) for v, l in PRICES)
    style_opts = "".join(f'<span data-style-line="{ln}">{opt("style", s, s + ("s" if s == "Belt" else ""))}</span>' for s, ln in styles)
    line_opts = opt("line", "wallet", "Wallets") + opt("line", "belt", "Belts")
    sorts = [("recommended", "Recommended"), ("new", "Newest"), ("price-asc", "Price, low to high"), ("price-desc", "Price, high to low"), ("name", "Name, A to Z")]
    sort_opts = "".join(f'<label class="sh-check sh-radio"><input type="radio" name="sort" value="{v}" {"checked" if v == "recommended" else ""}><span class="sh-box"></span><span class="sh-check-label">{l}</span></label>' for v, l in sorts)

    def pill(key, label, body):
        return f'<div class="sh-pill" data-dd="{key}"><button type="button" class="sh-pill-btn" aria-expanded="false" aria-haspopup="true"><span data-pill-label>{label}</span><i class="sh-pill-n" data-pill-n hidden></i>{chev}</button><div class="sh-dd" hidden><div class="sh-dd-body">{body}</div><div class="sh-dd-foot"><button type="button" class="btn btn--text" data-clear-group="{key}">Clear</button><button type="button" class="btn btn--sm" data-dd-close>Done</button></div></div></div>'

    css = r'''
.shop-top { padding: calc(var(--nav-top) + clamp(20px, 3vw, 36px)) 0 0; }
.shop-head { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; flex-wrap: wrap; }
.shop-head h1 { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.75rem, 1.2rem + 1.6vw, 2.5rem); line-height: 1.1; }
.shop-head p { color: var(--fg-2); font-size: .9375rem; }
/* category circles */
.sh-cats { display: flex; gap: clamp(10px, 1.5vw, 22px); margin-top: clamp(18px, 2.5vw, 28px); overflow-x: auto; scrollbar-width: none; padding: 4px 4px 8px; margin-inline: -4px; scroll-snap-type: x proximity; }
.sh-cats::-webkit-scrollbar { display: none; }
.sh-cat { flex: 0 0 auto; width: clamp(84px, 8vw, 108px); display: grid; justify-items: center; gap: 10px; color: var(--fg); scroll-snap-align: start; }
.sh-cat[hidden] { display: none; }
.sh-cat-ring { width: clamp(68px, 6.4vw, 88px); aspect-ratio: 1; border-radius: 50%; background: var(--surface); border: 1px solid var(--line); display: grid; place-items: center; overflow: hidden; box-shadow: 0 0 0 0 var(--fg); transition: box-shadow .3s ease, border-color .3s ease, transform .4s var(--ease-out); }
.sh-cat-ring img { width: 72%; height: 72%; object-fit: contain; filter: drop-shadow(0 6px 8px rgba(26,27,29,.18)); transition: transform .5s var(--ease-out); }
.sh-cat:hover .sh-cat-ring { border-color: var(--fg); }
.sh-cat:hover .sh-cat-ring img { transform: scale(1.06); }
.sh-cat[aria-selected="true"] .sh-cat-ring { border-color: var(--fg); box-shadow: 0 0 0 2px var(--fg); }
.sh-cat-label { font-size: .75rem; font-weight: 500; letter-spacing: .02em; text-align: center; line-height: 1.3; }
/* pills row */
.sh-bar { position: sticky; top: var(--nav-h); z-index: 30; background: color-mix(in srgb, var(--bg) 94%, transparent); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); padding: 10px 0; }
.sh-bar .wrap { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.sh-pills { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.sh-pill { position: relative; }
.sh-pill-btn, .sh-all-btn { min-height: 40px; padding: 0 14px 0 16px; border: 1px solid var(--line-strong); border-radius: 999px; background: var(--surface); display: inline-flex; align-items: center; gap: 8px; font-size: .8125rem; font-weight: 500; color: var(--fg); transition: border-color .3s ease, background-color .3s ease, color .3s ease; white-space: nowrap; }
.sh-pill-btn svg, .sh-all-btn svg { width: 14px; height: 14px; transition: transform .3s ease; }
.sh-pill-btn:hover, .sh-all-btn:hover { border-color: var(--fg); }
.sh-pill-btn[aria-expanded="true"] { background: var(--fg); color: var(--bg); border-color: var(--fg); }
.sh-pill-btn[aria-expanded="true"] svg { transform: rotate(180deg); }
.sh-pill.is-active .sh-pill-btn { border-color: var(--fg); }
.sh-pill-n { font-style: normal; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 999px; background: var(--accent); color: var(--bone); font-size: .6875rem; display: inline-grid; place-items: center; }
.sh-pill-n[hidden] { display: none; }
.sh-dd { position: absolute; left: 0; top: calc(100% + 8px); z-index: 40; min-width: 260px; background: var(--bg); color: var(--fg); border: 1px solid var(--line); box-shadow: 0 24px 48px rgba(26,27,29,.14); transform-origin: top left; }
.sh-dd[hidden] { display: none; }
.sh-dd-body { padding: 8px 6px; max-height: 60vh; overflow: auto; }
.sh-dd-foot { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 8px 12px 10px; border-top: 1px solid var(--line); }
.sh-check { position: relative; display: flex; align-items: center; gap: 10px; min-height: 40px; padding: 0 12px; border-radius: 6px; cursor: pointer; font-size: .875rem; }
.sh-check:hover { background: rgba(26,27,29,.04); }
.sh-check input { position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer; }
.sh-box { width: 18px; height: 18px; border: 1px solid var(--line-strong); border-radius: 4px; display: grid; place-items: center; flex: 0 0 auto; transition: background-color .2s ease, border-color .2s ease; }
.sh-radio .sh-box { border-radius: 50%; }
.sh-box::after { content: ""; width: 10px; height: 6px; border-left: 2px solid var(--bg); border-bottom: 2px solid var(--bg); transform: rotate(-45deg) translate(1px, -1px); opacity: 0; }
.sh-radio .sh-box::after { width: 8px; height: 8px; border: 0; border-radius: 50%; background: var(--bg); transform: none; }
.sh-check:has(input:checked) .sh-box { background: var(--fg); border-color: var(--fg); }
.sh-check:has(input:checked) .sh-box::after { opacity: 1; }
.sh-check:has(input:focus-visible) { outline: 2px solid var(--focus); outline-offset: -2px; }
.sh-check .sw { width: 16px; height: 16px; border-radius: 50%; background: var(--sw); box-shadow: inset 0 0 0 1px rgba(0,0,0,.18); flex: 0 0 auto; }
.sh-check-label { flex: 1; }
.sh-check em { font-style: normal; font-size: .6875rem; min-width: 22px; height: 20px; padding: 0 6px; border-radius: 999px; background: rgba(26,27,29,.06); display: inline-grid; place-items: center; color: var(--fg-2); }
.sh-check.is-empty { opacity: .45; }
.sh-right { display: flex; align-items: center; gap: 12px; flex: 0 0 auto; }
.sh-right .sh-dd { left: auto; right: 0; transform-origin: top right; }
.sh-count { font-size: .8125rem; color: var(--fg-2); white-space: nowrap; }
/* chips of active filters */
.sh-active { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 18px; }
.sh-active:empty { display: none; }
.sh-chip { display: inline-flex; align-items: center; gap: 8px; min-height: 32px; padding: 0 10px 0 12px; border-radius: 999px; background: var(--fg); color: var(--bg); font-size: .75rem; font-weight: 500; }
.sh-chip svg { width: 12px; height: 12px; }
.sh-clear-all { font-size: .75rem; letter-spacing: .1em; text-transform: uppercase; color: var(--fg-2); margin-left: 4px; }
.sh-clear-all:hover { color: var(--fg); }
/* drawer */
.sh-drawer-backdrop { position: fixed; inset: 0; z-index: 90; background: rgba(26,27,29,.4); opacity: 0; pointer-events: none; transition: opacity .35s ease; }
.sh-drawer-backdrop.is-open { opacity: 1; pointer-events: auto; }
.sh-drawer { position: fixed; top: 0; left: 0; bottom: 0; z-index: 91; width: min(380px, 92vw); background: var(--bg); color: var(--fg); transform: translateX(-102%); transition: transform .5s var(--ease-out); display: grid; grid-template-rows: auto 1fr auto; box-shadow: 24px 0 48px rgba(26,27,29,.12); }
.sh-drawer.is-open { transform: none; }
.sh-drawer-head { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; border-bottom: 1px solid var(--line); }
.sh-drawer-head h2 { font-size: 1rem; font-weight: 500; }
.sh-drawer-body { overflow: auto; padding: 8px 14px 24px; }
.sh-drawer-foot { display: flex; gap: 10px; padding: 14px 20px; border-top: 1px solid var(--line); }
.sh-drawer-foot .btn { flex: 1; }
.sh-group { padding: 14px 0 6px; border-bottom: 1px solid var(--line); }
.sh-group summary { list-style: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center; padding: 6px; font-weight: 500; font-size: .9375rem; }
.sh-group summary::-webkit-details-marker { display: none; }
.sh-group summary svg { width: 14px; height: 14px; transition: transform .3s ease; }
.sh-group[open] summary svg { transform: rotate(180deg); }
.sh-group-body { padding: 6px 0 8px; }
.sh-swatches { display: grid; grid-template-columns: repeat(auto-fill, minmax(48px, 1fr)); gap: 8px 8px; padding: 6px 6px 22px; }
.sh-swatch { position: relative; aspect-ratio: 1; border-radius: 8px; border: 1px solid var(--line); display: grid; place-items: center; cursor: pointer; }
.sh-swatch input { position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer; }
.sh-swatch .sw { width: 24px; height: 24px; border-radius: 50%; background: var(--sw); box-shadow: inset 0 0 0 1px rgba(0,0,0,.18); }
.sh-swatch:has(input:checked) { border-color: var(--fg); box-shadow: 0 0 0 1px var(--fg); }
.sh-swatch-label { position: absolute; left: 0; right: 0; bottom: -18px; font-size: .625rem; text-align: center; color: var(--fg-2); }
/* grid */
.sh-grid-wrap { padding: clamp(20px, 3vw, 32px) 0 var(--section-sm); }
.delivery { display: grid; gap: 28px; padding: var(--section-sm) 0 0; border-top: 1px solid var(--line); margin-top: var(--section-sm); }
@media (min-width: 768px) { .delivery { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.delivery h3 { font-family: var(--font-display); font-weight: 300; font-size: 1.5rem; }
.delivery p { color: var(--fg-2); font-size: .9375rem; margin-top: 8px; max-width: 26ch; }
@media (max-width: 767px) {
  .shop-head p { display: none; }
  .sh-bar { position: static; }
  .sh-bar .wrap { flex-wrap: wrap; }
  .sh-pills { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; margin-inline: calc(var(--gutter) * -1); padding-inline: var(--gutter); width: calc(100% + var(--gutter) * 2); }
  .sh-pills::-webkit-scrollbar { display: none; }
  .sh-pill:not([data-dd="sort"]) .sh-dd { display: none !important; }
  .sh-right { width: 100%; justify-content: space-between; }
}
'''

    body = f'''
<section class="shop-top on-bone" aria-labelledby="shop-title">
  <div class="wrap">
    <div class="shop-head"><h1 id="shop-title" data-shop-title>All pieces</h1><p>{B["descriptor"]} Cash on delivery across Pakistan.</p></div>
    <div class="sh-cats" role="tablist" aria-label="Categories" data-cats>{cats_html}</div>
  </div>
</section>

<div class="sh-bar" data-bar>
  <div class="wrap">
    <div class="sh-pills" data-pills>
      {pill("colour", "Colour", colour_opts)}
      {pill("price", "Price", price_opts)}
      {pill("style", "Style", style_opts)}
      <button type="button" class="sh-all-btn" data-drawer-open>All filters {sliders}</button>
    </div>
    <div class="sh-right">
      <span class="sh-count"><span data-count-total>{len(P)}</span> pieces</span>
      <div class="sh-pill" data-dd="sort"><button type="button" class="sh-pill-btn" aria-expanded="false" aria-haspopup="true"><span data-sort-label>Recommended</span>{chev}</button><div class="sh-dd" hidden><div class="sh-dd-body" data-sort-body>{sort_opts}</div></div></div>
    </div>
  </div>
</div>

<section class="sh-grid-wrap on-bone" aria-label="All pieces">
  <div class="wrap">
    <div class="sh-active" data-active></div>
    <div class="sh-grid" data-grid>{cards}</div>
    <div class="sh-empty" data-empty><p class="h3">Nothing matches that yet.</p><p class="muted" style="margin-top:10px">Loosen a filter and the shelf fills up again.</p><p style="margin-top:24px"><button type="button" class="btn btn--ghost btn--sm" data-clear-all>Clear filters</button></p></div>
    <div class="delivery">{"".join(f'<div data-reveal data-delay="{i * .1}"><h3>{t["title"]}</h3><p>{t["sub"]}</p></div>' for i, t in enumerate(B["trust"]["items"]))}</div>
  </div>
</section>

<div class="sh-drawer-backdrop" data-drawer-close aria-hidden="true"></div>
<aside class="sh-drawer" data-drawer aria-hidden="true" aria-label="All filters" data-lenis-prevent>
  <div class="sh-drawer-head"><h2>Select filters</h2><button type="button" class="icon-btn" data-drawer-close aria-label="Close filters">{I["close"]}</button></div>
  <div class="sh-drawer-body">
    <details class="sh-group" open><summary>Colour {chev}</summary><div class="sh-group-body sh-swatches">{"".join(f'<label class="sh-swatch" title="{c}"><input type="checkbox" data-f="colour" value="{c}"><span class="sw" style="--sw:{SWATCH.get(c, "#6E4328")}"></span><span class="sh-swatch-label">{c}</span></label>' for c in colours)}</div></details>
    <details class="sh-group" open><summary>Price {chev}</summary><div class="sh-group-body">{price_opts}</div></details>
    <details class="sh-group" open><summary>Style {chev}</summary><div class="sh-group-body">{style_opts}</div></details>
    <details class="sh-group" open><summary>Line {chev}</summary><div class="sh-group-body">{line_opts}</div></details>
  </div>
  <div class="sh-drawer-foot"><button type="button" class="btn btn--ghost" data-clear-all>Clear all</button><button type="button" class="btn" data-drawer-close>Show <span data-count-total>{len(P)}</span> pieces</button></div>
</aside>
'''

    js = r'''
const CATS = __CATS__;
const PRICE_LABEL = { "0-2000": "Under Rs 2,000", "2000-3000": "Rs 2,000 – 3,000", "3000-99999": "Over Rs 3,000" };
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, reduced = S.reduced;
  if (!G) return;
  S.initReveals($(".sh-grid-wrap")); S.initReveals($("footer"));

  const grid = $("[data-grid]"), cards = $$("[data-product]", grid), empty = $("[data-empty]"), catBtns = $$("[data-cat]"), title = $("[data-shop-title]");
  const state = { line: "", cat: "all", colour: [], price: [], style: [], sort: "recommended" };

  /* ---- read the URL ---- */
  const qs = new URLSearchParams(location.search);
  const ql = (qs.get("line") || "").toLowerCase(); if (ql.startsWith("wallet")) state.line = "wallet"; else if (ql.startsWith("belt")) state.line = "belt";
  if (qs.get("cat") && CATS.some((c) => c.key === qs.get("cat"))) state.cat = qs.get("cat");
  ["colour", "price", "style"].forEach((k) => { if (qs.get(k)) state[k] = qs.get(k).split(",").filter(Boolean); });
  if (qs.get("sort")) state.sort = qs.get("sort");
  // a style deep link from the mega menu acts like the matching category
  if (state.style.length === 1 && state.cat === "all") { const c = CATS.find((x) => x.style === state.style[0]); if (c) { state.cat = c.key; state.style = []; } }

  /* ---- predicates ---- */
  const cat = () => CATS.find((c) => c.key === state.cat) || CATS[0];
  const inCat = (c, k) => { if (k.line) return c.dataset.line === k.line; if (k.style) return c.dataset.style === k.style; if (k.ids) return k.ids.indexOf(c.dataset.product) >= 0; return true; };
  const group = { colour: (c, v) => c.dataset.colours.split(",").indexOf(v) >= 0, price: (c, v) => { const [lo, hi] = v.split("-").map(Number), p = +c.dataset.price; return p >= lo && p <= hi; }, style: (c, v) => c.dataset.style === v, line: (c, v) => c.dataset.line === v };
  const passGroup = (c, k) => !state[k].length || state[k].some((v) => group[k](c, v));
  const passLine = (c) => !state.line || c.dataset.line === state.line;
  const passes = (c, skip) => passLine(c) && inCat(c, cat()) && ["colour", "price", "style"].every((k) => k === skip || passGroup(c, k));
  const sorters = { recommended: (a, b) => +a.dataset.index - +b.dataset.index, new: (a, b) => (b.dataset.tags.indexOf("new") >= 0) - (a.dataset.tags.indexOf("new") >= 0) || +a.dataset.index - +b.dataset.index, "price-asc": (a, b) => +a.dataset.price - +b.dataset.price, "price-desc": (a, b) => +b.dataset.price - +a.dataset.price, name: (a, b) => a.dataset.name.localeCompare(b.dataset.name) };

  /* ---- paint everything but the grid ---- */
  const inputs = $$("[data-f]");
  const paint = () => {
    title.textContent = state.line === "wallet" ? "All wallets" : state.line === "belt" ? "All belts" : "All pieces";
    catBtns.forEach((b) => { const scopes = b.dataset.scope.split(" "); b.hidden = scopes.indexOf(state.line) < 0; b.setAttribute("aria-selected", String(b.dataset.cat === state.cat)); const lab = $(".sh-cat-label", b); if (b.dataset.cat === "all") lab.textContent = state.line === "wallet" ? "All wallets" : state.line === "belt" ? "All belts" : "All"; });
    $$("[data-style-line]").forEach((w) => { w.hidden = !!state.line && w.dataset.styleLine !== state.line; });
    // checkboxes mirror the state; the count is what ticking that option would show
    inputs.forEach((i) => { const k = i.dataset.f; if (k === "line") { i.checked = state.line === i.value; const em = $("em", i.parentElement); if (em) em.textContent = cards.filter((c) => c.dataset.line === i.value && ["colour", "price", "style"].every((g) => passGroup(c, g))).length; return; } i.checked = state[k].indexOf(i.value) >= 0; const n = cards.filter((c) => passes(c, k) && group[k](c, i.value)).length; const em = $("em", i.parentElement); if (em) em.textContent = n; i.parentElement.classList.toggle("is-empty", n === 0 && !i.checked); });
    $$("[data-dd]").forEach((p) => { const k = p.dataset.dd; if (!Array.isArray(state[k])) return; const n = state[k].length, badge = $("[data-pill-n]", p); badge.hidden = !n; badge.textContent = n; p.classList.toggle("is-active", n > 0); });
    $$('input[name="sort"]').forEach((r) => r.checked = r.value === state.sort);
    const sr = $('input[name="sort"][value="' + state.sort + '"]'); if (sr) $("[data-sort-label]").textContent = $(".sh-check-label", sr.parentElement).textContent;
    const chips = []; ["colour", "price", "style"].forEach((k) => state[k].forEach((v) => chips.push({ k, v, label: k === "price" ? PRICE_LABEL[v] : v + (k === "style" && v === "Belt" ? "s" : "") })));
    $("[data-active]").innerHTML = chips.map((c) => '<button type="button" class="sh-chip" data-chip="' + c.k + '" data-value="' + c.v + '">' + c.label + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg></button>').join("") + (chips.length ? '<button type="button" class="sh-clear-all" data-clear-all>Clear all</button>' : "");
    sync();
  };
  const mutate = () => {
    cards.slice().sort(sorters[state.sort] || sorters.recommended).forEach((c) => grid.appendChild(c));
    let k = 0; cards.forEach((c) => { const ok = passes(c); c.classList.toggle("is-hidden", !ok); if (ok) k++; });
    $$("[data-count-total]").forEach((el) => el.textContent = k);
    empty.classList.toggle("is-on", k === 0);
  };
  const sync = () => {
    const p = new URLSearchParams(); if (state.line) p.set("line", state.line + "s"); if (state.cat !== "all") p.set("cat", state.cat); ["colour", "price", "style"].forEach((k) => { if (state[k].length) p.set(k, state[k].join(",")); }); if (state.sort !== "recommended") p.set("sort", state.sort);
    const q = p.toString(); history.replaceState(null, "", location.pathname + (q ? "?" + q : ""));
  };
  const apply = (animate) => { paint(); if (animate) S.swapGrid(grid, mutate); else { mutate(); ST.refresh(); } };

  /* ---- events ---- */
  catBtns.forEach((b) => b.addEventListener("click", () => { const c = CATS.find((x) => x.key === b.dataset.cat); if (c.line) { state.line = c.line; state.cat = "all"; } else state.cat = c.key; if (c.line || c.style) state.style = []; apply(true); }));
  document.addEventListener("change", (e) => {
    const i = e.target.closest("[data-f]");
    if (i) { const k = i.dataset.f; if (k === "line") { state.line = i.checked ? i.value : ""; state.cat = "all"; } else { const has = state[k].indexOf(i.value); if (i.checked && has < 0) state[k].push(i.value); if (!i.checked && has >= 0) state[k].splice(has, 1); } apply(true); return; }
    if (e.target.name === "sort") { state.sort = e.target.value; apply(true); closeDd(); }
  });
  document.addEventListener("click", (e) => {
    const chip = e.target.closest("[data-chip]"); if (chip) { const k = chip.dataset.chip; state[k] = state[k].filter((v) => v !== chip.dataset.value); apply(true); return; }
    if (e.target.closest("[data-clear-all]")) { state.colour = []; state.price = []; state.style = []; state.cat = "all"; apply(true); return; }
    const cg = e.target.closest("[data-clear-group]"); if (cg) { state[cg.dataset.clearGroup] = []; apply(true); }
  });

  /* ---- dropdown pills ---- */
  let openDd = null;
  const closeDd = () => { if (!openDd) return; const dd = $(".sh-dd", openDd), btn = $(".sh-pill-btn", openDd); btn.setAttribute("aria-expanded", "false"); if (G && !reduced) G.to(dd, { opacity: 0, y: -6, duration: .18, ease: "power2.in", overwrite: true, onComplete: () => { dd.hidden = true; G.set(dd, { clearProps: "all" }); } }); else dd.hidden = true; openDd = null; };
  const showDd = (pill) => { if (openDd === pill) return closeDd(); closeDd(); openDd = pill; const dd = $(".sh-dd", pill), btn = $(".sh-pill-btn", pill); btn.setAttribute("aria-expanded", "true"); dd.hidden = false; if (G && !reduced) G.fromTo(dd, { opacity: 0, y: -6 }, { opacity: 1, y: 0, duration: .3, ease: "power3.out", overwrite: true, clearProps: "transform" }); };
  $$("[data-dd]").forEach((pill) => $(".sh-pill-btn", pill).addEventListener("click", (e) => { e.stopPropagation(); if (S.isMobile && pill.dataset.dd !== "sort") return openDrawer(); showDd(pill); }));
  $$("[data-dd-close]").forEach((b) => b.addEventListener("click", closeDd));
  document.addEventListener("click", (e) => { if (openDd && !openDd.contains(e.target)) closeDd(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeDd(); });

  /* ---- drawer ---- */
  const drawer = $("[data-drawer]"), backdrop = $(".sh-drawer-backdrop"); let drawerOpen = false, lastFocus = null;
  const openDrawer = () => { closeDd(); drawerOpen = true; drawer.classList.add("is-open"); backdrop.classList.add("is-open"); drawer.setAttribute("aria-hidden", "false"); S.lock("filters"); lastFocus = document.activeElement; setTimeout(() => $("[data-drawer-close]", drawer).focus(), 300); };
  const closeDrawer = () => { if (!drawerOpen) return; drawerOpen = false; drawer.classList.remove("is-open"); backdrop.classList.remove("is-open"); drawer.setAttribute("aria-hidden", "true"); S.unlock("filters"); lastFocus && lastFocus.focus && lastFocus.focus(); };
  $$("[data-drawer-open]").forEach((b) => b.addEventListener("click", openDrawer));
  $$("[data-drawer-close]").forEach((b) => b.addEventListener("click", closeDrawer));
  S.closeOverlay = () => { if (drawerOpen) closeDrawer(); };

  /* ---- wishlist hearts (kept in this browser) ---- */
  const WISH = "stagr-wishlist"; let wish = []; try { wish = JSON.parse(localStorage.getItem(WISH) || "[]"); } catch (e) {}
  const paintWish = () => $$("[data-wish]").forEach((b) => b.setAttribute("aria-pressed", String(wish.indexOf(b.dataset.wish) >= 0)));
  document.addEventListener("click", (e) => { const b = e.target.closest("[data-wish]"); if (!b) return; const id = b.dataset.wish, i = wish.indexOf(id); if (i >= 0) wish.splice(i, 1); else wish.push(id); try { localStorage.setItem(WISH, JSON.stringify(wish)); } catch (x) {} paintWish(); if (G && !reduced) G.fromTo(b, { scale: .8 }, { scale: 1, duration: .45, ease: "back.out(3)", clearProps: "transform" }); S.toast && S.toast(i >= 0 ? "Removed from saved" : "Saved for later"); });
  paintWish();

  /* ---- first paint: categories and cards rise in once ---- */
  apply(false);
  if (!reduced) G.fromTo(cards.filter((c) => !c.classList.contains("is-hidden")), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .7, ease: "power3.out", stagger: .04, delay: .2, clearProps: "opacity,transform", scrollTrigger: { trigger: grid, start: "top 85%", once: true } });
  if (!reduced) G.fromTo($$("[data-cat]:not([hidden])"), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .5, ease: "power2.out", stagger: .04, delay: .1, clearProps: "opacity,transform" });
}
STAGR.onReady.push(initAnimations);
'''.replace("__CATS__", cats_json)

    return {
        "file": "shop.html",
        "key": "shop",
        "title": "Shop — STAGR.",
        "description": f"All {len(P)} STAGR. wallets and belts. Filter by colour, style and price. Cash on delivery across Pakistan.",
        "css": css,
        "body": body,
        "js": js,
        "header_dark": False,
        "shop_href": "#shop-title",
    }
