"""wallets.html and belts.html — collection pages in the bone/ink system."""
import json

SWATCH = {"Brown": "#6E4328", "Black": "#1A1512", "Tan": "#B0773F", "Coffee": "#4A3024"}


def page(ctx, line):
    P = [p for p in ctx["products"] if p["line"] == line]
    B = ctx["brand"]
    I = ctx["icon"]
    cut = ctx["cutouts"]
    other = "belt" if line == "wallet" else "wallet"
    title = "Wallets" if line == "wallet" else "Belts"
    other_title = "Belts" if line == "wallet" else "Wallets"
    blurb = ctx["products_doc"]["lines"][line]["blurb"]
    prices = [p["price"] for p in P]
    fmt = lambda n: "Rs " + format(n, ",d")
    colours = sorted({c for p in P for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black"].index(c) if c in ["Brown", "Tan", "Black"] else 9)
    styles = sorted({p["style"] for p in P if p["style"]}, key=lambda s: ["Bifold", "Trifold", "Minimalist", "Long"].index(s) if s in ["Bifold", "Trifold", "Minimalist", "Long"] else 9)
    cards = "".join(ctx["pcard"](ctx, p, i) for i, p in enumerate(P))
    cross = [p for p in ctx["products"] if p["line"] == other][:3]
    cross_cards = "".join(ctx["pcard"](ctx, p, i, quick=False) for i, p in enumerate(cross))
    hero_a, hero_b = (cut(P[0])[0], cut(next(p for p in P if p["id"] == ("rodeo" if line == "wallet" else "monarch")))[0])
    colour_pills = "".join(f'<button type="button" class="pill" data-filter="colour" data-value="{c}" aria-pressed="false"><span class="sw" style="--sw:{SWATCH.get(c, "#6E4328")}"></span>{c}</button>' for c in colours)
    style_pills = "".join(f'<button type="button" class="pill" data-filter="style" data-value="{s}" aria-pressed="false">{s}</button>' for s in styles)
    price_pills = ('<button type="button" class="pill" data-filter="price" data-value="0-2000" aria-pressed="false">Under Rs 2,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="2000-3000" aria-pressed="false">Rs 2,000 – 3,000</button>'
                   '<button type="button" class="pill" data-filter="price" data-value="3000-99999" aria-pressed="false">Over Rs 3,000</button>')
    facts = [("Leather", "Crazy horse, full grain"), ("Pieces", f"{len(P)} styles"), ("Colours", " / ".join(colours)), ("From", fmt(min(prices)))]
    if line == "belt":
        facts.append(("Sizes", "30 to 44"))
    products_json = json.dumps([{k: p[k] for k in ("id", "name", "style", "tagline", "price", "compareAtPrice", "colours", "defaultColour", "line", "sizes")} | {"cutouts": cut(p)} for p in P], ensure_ascii=False).replace("</", "<\\/")

    css = r'''
.dotc { color: var(--accent); }
/* ---- header ---- */
.col-hero { position: relative; overflow: hidden; padding: calc(var(--nav-h) + clamp(32px, 6vw, 72px)) 0 clamp(32px, 5vw, 64px); }
.col-hero .grid { align-items: center; }
.col-hero .display { font-size: clamp(3.4rem, 2rem + 8vw, 9rem); line-height: .95; opacity: 0; }
.col-hero .lead { margin-top: 22px; }
.col-stage { position: relative; aspect-ratio: 1; display: grid; place-items: center; }
.col-stage .bloom { --bloom-s: 90%; }
.col-stage .ghost { font-size: clamp(10rem, 36vw, 24rem); }
.col-stage .pair { position: relative; width: 92%; aspect-ratio: 1; }
.col-stage .pair img { position: absolute; height: auto; filter: drop-shadow(0 30px 40px rgba(26,27,29,.22)); }
.col-stage .p-a { left: 0; top: 4%; width: 70%; transform: rotate(-6deg); }
.col-stage .p-b { right: 0; bottom: 2%; width: 64%; transform: rotate(5deg); }
@media (max-width: 1023px) { .col-stage { max-width: 420px; margin: 24px auto 0; } }
.col-facts { margin-top: 28px; max-width: 420px; }

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

/* ---- sticky mini nav (replaces the main nav after the header scrolls out) ---- */
.mini-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 55; height: var(--nav-h); background: color-mix(in srgb, var(--bg) 94%, transparent); backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); transform: translateY(-100%); transition: transform .5s var(--ease-out); display: flex; align-items: center; }
.mini-nav.is-on { transform: none; }
.mini-nav .wrap { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.mini-nav .mn-title { font-family: var(--font-display); font-weight: 300; font-size: 1.4rem; display: flex; align-items: baseline; gap: 10px; }
.mini-nav .mn-title .small { color: var(--fg-2); }
.mini-nav .mn-actions { display: flex; gap: 8px; align-items: center; }
@media (max-width: 767px) { .mini-nav { display: none; } }

/* ---- grid ---- */
.catalog { padding: clamp(32px, 5vw, 64px) 0 var(--section-sm); }
.shop-grid { display: grid; gap: 16px; grid-template-columns: 1fr; }
@media (min-width: 640px) { .shop-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .shop-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; } }
.pcard.is-hidden { display: none; }
.empty { display: none; padding: 64px 0; text-align: center; }
.empty.is-on { display: block; }

/* ---- cross-sell ---- */
.cross { padding: var(--section-sm) 0; }
.cross .between { margin-bottom: 32px; }

/* ---- delivery ---- */
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
<section class="col-hero on-bone" aria-labelledby="col-title" data-col-hero>
  <div class="wrap grid">
    <div class="col-12 lg:col-6">
      <p class="label" data-reveal><b>01</b><span class="slash">/</span>{"Wallets" if line == "wallet" else "Belts"} · {len(P)} styles</p>
      <h1 class="display" id="col-title" data-col-title style="margin-top:14px">{title}<span class="dotc">.</span></h1>
      <p class="lead" data-reveal data-delay=".3">{blurb}</p>
      <dl class="spec col-facts" data-reveal data-delay=".4">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)}</dl>
    </div>
    <div class="col-12 lg:col-5 lg:start-8">
      <div class="col-stage" data-col-stage><div class="bloom" style="--bloom:#D9B07A" data-bloom></div><span class="ghost">0{1 if line == "wallet" else 2}</span><div class="pair"><img class="p-a" src="{hero_a["src"]}" alt="" width="900" height="900" decoding="async"><img class="p-b" src="{hero_b["src"]}" alt="" width="900" height="900" decoding="async"></div></div>
    </div>
  </div>
</section>

<div class="mini-nav" aria-hidden="true">
  <div class="wrap">
    <a class="mn-title" href="#top">{title} <span class="small" data-count-mini>{len(P)}</span></a>
    <div class="mn-actions"><button type="button" class="btn btn--ghost btn--sm" data-scroll-to="#filters">Filters</button><a class="btn btn--ghost btn--sm" href="{other}s.html">{other_title}</a><button type="button" class="icon-btn" data-cart-open aria-label="Open cart">{I["bag"]}<span class="cart-count" aria-hidden="true">0</span></button></div>
  </div>
</div>

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
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, Flip = window.Flip, $ = S.$, $$ = S.$$, reduced = S.reduced;
  if (!G) return;
  const grid = $("[data-grid]"), cards = $$("[data-product]", grid), empty = $("[data-empty]");
  const state = { colour: "", style: "", price: "", sort: "default" };

  /* ---- header entrance ---- */
  const title = $("[data-col-title]"), stage = $("[data-col-stage]");
  const ready = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
  ready.then(() => { S.charRise(title, { to: { duration: .8, stagger: .04, delay: .1 } }); G.set(title, { opacity: 1 }); });
  G.fromTo(stage, { opacity: 0, y: 40, scale: .94 }, { opacity: 1, y: 0, scale: 1, duration: 1.2, ease: "power3.out", delay: .25 });
  G.fromTo($$(".pair img", stage), { y: 30, rotation: 0 }, { y: 0, duration: 1.4, ease: "power3.out", stagger: .12, delay: .3, clearProps: "y" });
  if (!reduced) $$(".pair img", stage).forEach((im, i) => G.to(im, { y: i ? 8 : -8, duration: 3.2 + i, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 1.8 }));
  S.initReveals($("[data-col-hero]")); S.initReveals($(".catalog")); S.initReveals($(".cross"));

  /* ---- sticky mini nav ---- */
  const mini = $(".mini-nav"), hero = $("[data-col-hero]"), nav = $(".nav");
  const check = () => { const on = hero.getBoundingClientRect().bottom < 0; mini.classList.toggle("is-on", on); mini.setAttribute("aria-hidden", String(!on)); nav.classList.toggle("is-hidden", on); };
  window.addEventListener("scroll", check, { passive: true }); check();

  /* ---- filters with Flip ---- */
  const passes = (c) => { const cols = c.dataset.colours.split(","), price = +c.dataset.price; if (state.colour && cols.indexOf(state.colour) < 0) return false; if (state.style && c.dataset.style !== state.style) return false; if (state.price) { const [lo, hi] = state.price.split("-").map(Number); if (price < lo || price > hi) return false; } return true; };
  const sorters = { default: (a, b) => +a.dataset.index - +b.dataset.index, "price-asc": (a, b) => +a.dataset.price - +b.dataset.price, "price-desc": (a, b) => +b.dataset.price - +a.dataset.price, name: (a, b) => a.dataset.name.localeCompare(b.dataset.name) };
  const apply = () => {
    const st = Flip && !reduced ? Flip.getState(cards) : null;
    cards.slice().sort(sorters[state.sort] || sorters.default).forEach((c) => grid.appendChild(c));
    let n = 0; cards.forEach((c) => { const ok = passes(c); c.classList.toggle("is-hidden", !ok); if (ok) n++; });
    $$("[data-count], [data-count-mini]").forEach((el) => el.textContent = n);
    empty.classList.toggle("is-on", n === 0);
    $$("[data-clear]").forEach((b) => b.classList.toggle("is-on", !!(state.colour || state.style || state.price)));
    if (st) Flip.from(st, { duration: .7, ease: "power3.out", stagger: .03, absolute: true, scale: true, onEnter: (els) => G.fromTo(els, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .5, ease: "power2.out" }), onLeave: (els) => G.to(els, { opacity: 0, y: 12, duration: .3 }) });
    ST.refresh();
  };
  $$("[data-filter]").forEach((b) => b.addEventListener("click", () => { const k = b.dataset.filter, v = b.dataset.value; state[k] = state[k] === v ? "" : v; $$('[data-filter="' + k + '"]').forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.value === state[k]))); apply(); }));
  $$("[data-clear]").forEach((b) => b.addEventListener("click", () => { state.colour = state.style = state.price = ""; $$("[data-filter]").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.value === ""))); apply(); }));
  const sort = $("[data-sort]"); sort && sort.addEventListener("change", () => { state.sort = sort.value; apply(); });
  $$("[data-scroll-to]").forEach((b) => b.addEventListener("click", () => S.scrollTo(b.dataset.scrollTo)));

  /* ---- colour option swaps the card image ---- */
  cards.concat($$(".cross [data-product]")).forEach((card) => { const btn = $("[data-add]", card); $$("[data-colour-opts] input", card).forEach((r) => r.addEventListener("change", () => { btn.dataset.colour = r.value; const p = S.product(card.dataset.product); const im = p.cutouts.find((c) => c.colour.toLowerCase() === r.value.toLowerCase()); if (im) { const main = $("img.main", card); G.fromTo(main, { opacity: 0 }, { opacity: 1, duration: .4 }); main.src = im.small; } })); });

  /* ---- quick view ---- */
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
        "shop_href": "#filters",
    }


def render(ctx):
    return [page(ctx, "wallet"), page(ctx, "belt")]
