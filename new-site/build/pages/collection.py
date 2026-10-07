"""wallets.html and belts.html — collection pages.

Opening: a static showcase in the style of the Daniel Roth reference. A
full-bleed photo on the left, a bone panel on the right with the category
name, "Collection", the product cutout, a counter on the left, the list of
categories on the right, a caps line and a "Discover the collection" button.
Clicking a category swaps the photo, cutout and text. Nothing is tied to
scroll. Below it: an intro line, one section per category with its pieces,
a link to the full shop grid, a cross-sell row and the delivery strip.
"""
import json

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

    # ---- categories ----
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
        g["products"] = [by[i] for i in g["ids"]]
        g["cut"] = cut(g["products"][0])[0]
        g["from"] = min(p["price"] for p in g["products"])
        g["count"] = len(g["ids"])
        g["colours"] = sorted({c for p in g["products"] for c in p["colours"]})
        # a second photo for the section below, different from the showcase one
        pool = [im for p in g["products"] for im in p["lifestyleImages"] if im["src"] != g["photo"]]
        portrait = [im for im in pool if im["height"] > im["width"]]
        g["photo2"] = (portrait or pool)[0]
    n = len(groups)
    groups_json = json.dumps([{
        "key": g["key"], "name": g["name"], "line1": g["line1"], "line2": g["line2"], "href": "#" + g["key"],
        "models": [{"name": p["name"].split(" ")[0], "href": f"product-{p['id']}.html"} for p in g["products"]],
        "meta": f'{g["count"]} {"style" if g["count"] == 1 else "styles"} · from {fmt(g["from"])}',
    } for g in groups], ensure_ascii=False).replace("</", "<\\/")

    photos = "".join(f'<div class="sc-photo" data-sc-photo="{i}" style="opacity:{1 if i == 0 else 0};--tint:{TINT[g["key"]]}"><img src="{g["photo"]}" srcset="{g["photo"].replace(".jpg", "-800.jpg")} 800w, {g["photo"]} 1600w" sizes="(min-width: 1024px) 60vw, 100vw" alt="" width="1200" height="1500" {"fetchpriority=high" if i == 0 else "loading=lazy"}></div>' for i, g in enumerate(groups))
    cuts = "".join(f'<div class="sc-cut" data-sc-cut="{i}" style="opacity:{1 if i == 0 else 0}"><img src="{g["cut"]["src"]}" alt="{g["name"]} {title.lower()[:-1]} in {g["cut"]["colour"].lower()}" width="900" height="900" decoding="async" {"" if i == 0 else "loading=lazy"}></div>' for i, g in enumerate(groups))
    cats = "".join(f'<li role="presentation"><button type="button" role="tab" aria-selected="{str(i == 0).lower()}" class="{"is-on" if i == 0 else ""}" data-sc-cat="{i}">{g["name"]}</button></li>' for i, g in enumerate(groups))
    g0 = groups[0]
    models0 = " <span aria-hidden=true>·</span> ".join(f'<a href="product-{p["id"]}.html">{p["name"].split(" ")[0]}</a>' for p in g0["products"])
    if g0["count"] == 1 and g0["products"][0]["name"].split(" ")[0].lower() == g0["name"].lower():
        models0 = f'<a href="product-{g0["ids"][0]}.html">{g0["count"]} style · from {fmt(g0["from"])}</a>'

    # ---- category sections ----
    def cat_section(i, g):
        cards = "".join(ctx["pcard"](ctx, p, P.index(p), compact=True) for p in g["products"])
        im = g["photo2"]
        return f'''
<section class="cat on-bone{" cat--few" if g["count"] <= 2 else ""}" id="{g["key"]}" aria-labelledby="cat-{g["key"]}">
  <div class="wrap" data-rail>
    <div class="cat-head">
      <div><p class="label" data-reveal><b>0{i + 2}</b><span class="slash">/</span>{g["name"]} {title.lower()} · {g["count"]} {"style" if g["count"] == 1 else "styles"} · from {fmt(g["from"])}</p><h2 class="h2" id="cat-{g["key"]}" data-text-reveal="lines" style="margin-top:12px">{g["line1"]} {g["line2"]}.</h2></div>
      <div class="rail-nav" data-reveal data-delay=".15"><button type="button" class="rail-btn" data-rail-prev aria-label="Previous" style="transform:scaleX(-1)">{I["arrow"]}</button><button type="button" class="rail-btn" data-rail-next aria-label="Next">{I["arrow"]}</button></div>
    </div>
    <div class="cat-row">
      <figure class="cat-photo" data-reveal><img src="{im["src"]}" srcset="{im["srcSmall"]} 800w, {im["src"]} {im["width"]}w" sizes="(min-width: 1024px) 30vw, 100vw" alt="{im["alt"]}" width="{im["width"]}" height="{im["height"]}" loading="lazy"></figure>
      <div class="rail-track cat-track" data-rail-track data-reveal data-delay=".1">{cards}</div>
    </div>
  </div>
</section>'''

    cat_sections = "".join(cat_section(i, g) for i, g in enumerate(groups))
    cross = [p for p in ctx["products"] if p["line"] == other][:3]
    cross_cards = "".join(ctx["pcard"](ctx, p, i, quick=False) for i, p in enumerate(cross))
    colours = sorted({c for p in P for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black"].index(c) if c in ["Brown", "Tan", "Black"] else 9)

    css = r'''
/* ---- showcase (Daniel Roth style, static) ---- */
.showcase { position: relative; background: var(--ink); color: var(--bone); overflow: hidden; }
.sc-frame { position: relative; height: 100vh; min-height: 720px; }
.sc-photos { position: absolute; inset: 0; }
.sc-photo { position: absolute; inset: 0; }
.sc-photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 30% 50%; transform: scale(1.08); will-change: transform; }
.sc-photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, color-mix(in srgb, var(--tint) 55%, transparent), color-mix(in srgb, var(--tint) 20%, transparent) 60%, rgba(26,27,29,.35)); mix-blend-mode: multiply; }
.sc-brand { position: absolute; left: var(--gutter); top: calc(var(--nav-h) + 16px); z-index: 3; font-size: .75rem; letter-spacing: .24em; text-transform: uppercase; color: rgba(239,237,230,.75); }
.sc-panel { position: absolute; right: var(--gutter); top: calc(var(--nav-h) + 8px); bottom: 32px; width: min(44vw, 640px); background: var(--bone); color: var(--ink); padding: clamp(24px, 3vw, 44px); display: grid; grid-template-rows: auto 1fr auto; overflow: hidden; }
.sc-head { text-align: center; }
.sc-title { font-family: var(--font-display); font-weight: 300; font-size: clamp(2.4rem, 1.6rem + 3vw, 4.6rem); line-height: 1; letter-spacing: .02em; text-transform: uppercase; }
.sc-kicker { margin-top: 12px; }
.sc-cats { position: absolute; right: clamp(24px, 3vw, 44px); top: 50%; transform: translateY(-50%); text-align: right; display: grid; gap: 12px; font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; z-index: 2; }
.sc-cats button { color: var(--mist); transition: color .3s ease; position: relative; padding: 2px 0; }
.sc-cats button::after { content: ""; position: absolute; left: 0; right: 0; bottom: -2px; height: 1px; background: var(--ink); transform: scaleX(0); transform-origin: right; transition: transform .4s var(--ease-out); }
.sc-cats button:hover { color: var(--ink); }
.sc-cats button.is-on { color: var(--ink); }
.sc-cats button.is-on::after { transform: scaleX(1); transform-origin: left; }
.sc-count { position: absolute; left: clamp(24px, 3vw, 44px); top: 50%; transform: translateY(-50%); font-size: .75rem; letter-spacing: .2em; color: var(--mist); font-variant-numeric: tabular-nums; }
.sc-stage { position: relative; align-self: center; justify-self: center; width: min(44%, 280px); aspect-ratio: 1; display: grid; place-items: center; }
.sc-cut { position: absolute; inset: 0; display: grid; place-items: center; }
.sc-cut img { width: 100%; height: auto; max-height: 100%; object-fit: contain; filter: drop-shadow(0 30px 40px rgba(26,27,29,.28)); }
.sc-foot { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; }
.sc-models { font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; display: flex; flex-wrap: wrap; gap: 6px 8px; }
.sc-models a { color: var(--ink); border-bottom: 1px solid var(--line-strong); transition: border-color .3s ease; }
.sc-models a:hover { border-color: var(--ink); }
.sc-line { margin-top: 12px; font-size: .8125rem; letter-spacing: .12em; text-transform: uppercase; line-height: 1.7; color: var(--mist); max-width: 24ch; }
.sc-cta { flex: 0 0 auto; }
@media (max-width: 1023px) {
  .sc-frame { height: auto; min-height: 0; }
  .sc-photos { position: relative; height: 60svh; }
  .sc-photo::after { background: linear-gradient(180deg, rgba(26,27,29,.6) 0%, rgba(26,27,29,0) 32%), linear-gradient(90deg, color-mix(in srgb, var(--tint) 45%, transparent), color-mix(in srgb, var(--tint) 15%, transparent)); mix-blend-mode: normal; }
  .sc-brand { display: none; }
  .sc-panel { position: relative; right: auto; top: auto; bottom: auto; width: auto; margin: -40px 20px 0; padding: 24px 20px 28px; display: grid; gap: 16px; z-index: 2; }
  .sc-stage { width: 58%; margin: 4px auto; }
  .sc-cats { position: static; transform: none; text-align: left; display: flex; flex-wrap: wrap; gap: 8px; }
  .sc-cats button { min-height: 36px; padding: 0 12px; border: 1px solid var(--line-strong); color: var(--fg-2); }
  .sc-cats button::after { display: none; }
  .sc-cats button.is-on { background: var(--ink); color: var(--bone); border-color: var(--ink); }
  .sc-count { position: static; transform: none; display: block; text-align: center; }
  .sc-foot { flex-direction: column; align-items: flex-start; gap: 18px; }
  .sc-line { max-width: none; }
}

/* ---- intro line under the showcase ---- */
.col-intro { padding: var(--section-sm) 0 clamp(16px, 3vw, 32px); }
.col-intro .display { font-size: clamp(2.6rem, 1.6rem + 4vw, 5.5rem); line-height: 1; }
.col-intro .lead { margin-top: 18px; }
.col-facts { max-width: 420px; }

/* ---- one section per category: fixed photo on the left, rail of cards on the right ---- */
.cat { padding: clamp(32px, 5vw, 64px) 0; border-top: 1px solid var(--line); }
.cat-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: clamp(20px, 3vw, 32px); }
.cat-head .h2 { max-width: 22ch; }
.cat-row { display: grid; gap: 16px; grid-template-columns: 1fr; }
.cat-photo { position: relative; overflow: hidden; background: var(--ink); aspect-ratio: 16 / 9; }
.cat-photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.cat-track { --rail-w: 78vw; }
@media (min-width: 640px) { .cat-track { --rail-w: calc((100% - 16px) / 2); } }
@media (min-width: 1024px) {
  .cat-row { grid-template-columns: minmax(0, 3fr) minmax(0, 9fr); gap: 20px; align-items: stretch; }
  .cat-photo { aspect-ratio: auto; min-height: 100%; }
  .cat-track { --rail-w: calc((100% - 32px) / 3); min-width: 0; }
}
@media (min-width: 1440px) { .cat-track { --rail-w: calc((100% - 32px) / 3); } }
.wrap:not(.has-overflow) .rail-nav { visibility: hidden; }
@media (min-width: 1024px) { .cat--few .cat-row { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); } .cat--few .cat-track { --rail-w: calc((100% - 16px) / 2); } }

/* ---- all + cross + delivery ---- */
.all-band { padding: var(--section-sm) 0; border-top: 1px solid var(--line); text-align: center; }
.all-band .h2 { margin: 12px auto 18px; max-width: 16ch; }
.all-band .lead { margin: 0 auto 28px; max-width: 42ch; }
.cross { padding: var(--section-sm) 0; }
.cross .between { margin-bottom: 32px; }
.shop-grid { display: grid; gap: 16px; grid-template-columns: 1fr; }
@media (min-width: 640px) { .shop-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .shop-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; } }
.delivery { display: grid; gap: 28px; padding: var(--section-sm) 0; }
@media (min-width: 768px) { .delivery { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.delivery h3 { font-family: var(--font-display); font-weight: 300; font-size: 1.5rem; }
.delivery p { color: var(--fg-2); font-size: .9375rem; margin-top: 8px; max-width: 26ch; }
'''

    body = f'''
<section class="showcase on-ink" aria-label="{title} collections" data-showcase>
  <div class="sc-frame">
    <div class="sc-photos" data-sc-photos>{photos}</div>
    <p class="sc-brand">{B["origin"]} · Crazy horse leather</p>
    <div class="sc-panel on-bone" data-sc-panel>
      <div class="sc-head"><h1 class="sc-title" data-sc-title>{g0["name"]}</h1><p class="label sc-kicker" data-sc-item>Collection</p></div>
      <span class="sc-count" data-sc-count data-sc-item>01 – 0{n}</span>
      <ul class="sc-cats" data-sc-cats role="tablist" aria-label="{title} categories" data-sc-item>{cats}</ul>
      <div class="sc-stage" data-sc-stage>{cuts}</div>
      <div class="sc-foot">
        <div><p class="sc-models" data-sc-models data-sc-item>{models0}</p><p class="sc-line" data-sc-line data-sc-item>{g0["line1"]}<br>{g0["line2"]}</p></div>
        <a class="btn sc-cta" data-sc-cta data-sc-item href="#{g0["key"]}">Discover the collection {I["arrow"]}</a>
      </div>
    </div>
  </div>
</section>

<section class="col-intro on-bone" aria-labelledby="col-title">
  <div class="wrap grid" style="align-items:end">
    <div class="col-12 lg:col-7"><p class="label" data-reveal><b>01</b><span class="slash">/</span>All {title.lower()} · {len(P)} styles</p><h2 class="display" id="col-title" data-text-reveal="chars" style="margin-top:14px">{title}<span class="dotc">.</span></h2><p class="lead" data-reveal data-delay=".2">{blurb}</p></div>
    <dl class="col-12 lg:col-4 lg:start-8 spec col-facts" data-reveal data-delay=".3">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [("Leather", "Crazy horse, full grain"), ("Pieces", f"{len(P)} styles"), ("Colours", " / ".join(colours)), ("From", fmt(min(prices)))] + ([("Sizes", "30 to 44")] if line == "belt" else []))}</dl>
  </div>
</section>
{cat_sections}
<section class="all-band on-bone" aria-labelledby="all-title">
  <div class="wrap">
    <p class="label" data-reveal><b>0{n + 2}</b><span class="slash">/</span>The full shelf</p>
    <h2 class="h2" id="all-title" data-text-reveal="lines">Every {title.lower()[:-1]}, side by side.</h2>
    <p class="lead" data-reveal data-delay=".15">Filter by colour, style and price, sort, and compare all {len(P)} {title.lower()} in one grid.</p>
    <a class="btn" href="shop.html?line={title.lower()}" data-reveal data-delay=".25">View all {title.lower()} {I["arrow"]}</a>
  </div>
</section>

<section class="cross on-ink" aria-labelledby="cross-title">
  <div class="wrap">
    <div class="between"><div><p class="label" data-reveal><b style="color:var(--bone)">0{n + 3}</b><span class="slash">/</span>Complete the look</p><h2 class="h2" id="cross-title" data-text-reveal="lines" style="margin-top:12px">{"A belt to match." if line == "wallet" else "A wallet to match."}</h2></div><a class="btn btn--ghost" href="{other}s.html" data-reveal>All {other_title.lower()} {I["arrow"]}</a></div>
    <div class="shop-grid">{cross_cards}</div>
  </div>
</section>

<section class="on-bone" aria-label="Delivery and returns"><div class="wrap"><div class="delivery">{"".join(f'<div data-reveal data-delay="{i * .1}"><h3>{t["title"]}</h3><p>{t["sub"]}</p></div>' for i, t in enumerate(B["trust"]["items"]))}</div></div></section>
'''

    js = r'''
const GROUPS = __GROUPS__;
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, reduced = S.reduced, isMobile = S.isMobile;
  if (!G) return;

  /* ================= showcase: click a category, nothing scroll-bound ================= */
  const panel = $("[data-sc-panel]"), photos = $$("[data-sc-photo]"), cuts = $$("[data-sc-cut]"), cats = $$("[data-sc-cat]"), count = $("[data-sc-count]");
  const title = $("[data-sc-title]"), models = $("[data-sc-models]"), line = $("[data-sc-line]"), cta = $("[data-sc-cta]");
  const n = GROUPS.length; let active = 0, titleSplit = null, floatTween = null;
  const pad = (i) => "0" + (i + 1);
  const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const fill = (g) => {
    if (titleSplit) titleSplit.revert(); titleSplit = null;   // revert first: SplitText restores the old markup
    title.textContent = g.name;
    models.innerHTML = g.models.length === 1 && g.models[0].name.toLowerCase() === g.name.toLowerCase() ? '<a href="' + g.models[0].href + '">' + esc(g.meta) + '</a>' : g.models.map((m) => '<a href="' + m.href + '">' + esc(m.name) + "</a>").join(' <span aria-hidden="true">·</span> ');
    line.innerHTML = esc(g.line1) + "<br>" + esc(g.line2);
    cta.href = g.href;
  };
  const riseTitle = () => { G.set(title, { opacity: 1 }); if (reduced) return; titleSplit = S.charRise(title, { from: 110, to: { duration: .6, stagger: .03, overwrite: "auto" } }); };
  const floatCut = (i) => { if (floatTween) floatTween.kill(); floatTween = null; if (reduced) return; floatTween = G.to($("img", cuts[i]), { y: -8, duration: 3.2, yoyo: true, repeat: -1, ease: "sine.inOut", delay: 1 }); };
  const setActive = (next, instant) => {
    if (next === active && !instant) return;
    const fwd = next > active, prev = active; active = next; const g = GROUPS[next];
    cats.forEach((b, i) => { b.classList.toggle("is-on", i === next); b.setAttribute("aria-selected", String(i === next)); });
    if (count) count.textContent = pad(next) + " – " + pad(n - 1);
    if (instant || reduced) {
      photos.forEach((ph, i) => G.set(ph, { opacity: i === next ? 1 : 0 }));
      cuts.forEach((c, i) => G.set(c, { opacity: i === next ? 1 : 0, x: 0, rotation: 0, scale: 1 }));
      fill(g); G.set([title, models, line], { opacity: 1, y: 0 }); return;
    }
    photos.forEach((ph, i) => { G.to(ph, { opacity: i === next ? 1 : 0, duration: .9, ease: "power2.inOut", overwrite: "auto" }); if (i === next) G.fromTo($("img", ph), { scale: 1.16, xPercent: fwd ? 2 : -2 }, { scale: 1.08, xPercent: 0, duration: 1.6, ease: "power3.out", overwrite: "auto" }); });
    cuts.forEach((c, i) => { if (i === next) G.fromTo(c, { opacity: 0, x: fwd ? 60 : -60, rotation: fwd ? 6 : -6, scale: .9 }, { opacity: 1, x: 0, rotation: 0, scale: 1, duration: .8, ease: "power3.out", delay: .1, overwrite: "auto" }); else G.to(c, { opacity: 0, x: fwd ? -40 : 40, scale: .92, duration: .4, ease: "power2.in", overwrite: "auto" }); });
    G.set($("img", cuts[prev]), { y: 0 }); floatCut(next);
    G.to([title, models, line], { y: -10, opacity: 0, duration: .2, ease: "power2.in", overwrite: "auto", onComplete: () => { fill(g); G.set(title, { y: 0 }); riseTitle(); G.fromTo([models, line], { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power2.out", stagger: .06, overwrite: "auto" }); } });
  };
  cats.forEach((b, i) => b.addEventListener("click", () => setActive(i)));
  const list = $("[data-sc-cats]");
  list && list.addEventListener("keydown", (e) => { const d = e.key === "ArrowDown" || e.key === "ArrowRight" ? 1 : e.key === "ArrowUp" || e.key === "ArrowLeft" ? -1 : 0; if (!d) return; e.preventDefault(); const next = (active + d + n) % n; setActive(next); cats[next].focus(); });
  // deep links: wallets.html#long, wallets.html?style=Long, belts.html#nova
  const want = (location.hash || "").slice(1).toLowerCase() || (new URLSearchParams(location.search).get("style") || "").toLowerCase();
  const start = Math.max(0, GROUPS.findIndex((g) => g.key === want));
  if (start) setActive(start, true);
  // entrance, once the loader has gone
  G.set(panel, { opacity: 0, x: isMobile ? 0 : 40, y: isMobile ? 24 : 0 });
  G.set($$("[data-sc-item]", panel), { opacity: 0 });
  G.set(title, { opacity: 0 });
  S.onLoaderDone.push(() => {
    G.to(panel, { opacity: 1, x: 0, y: 0, duration: 1, ease: "power3.out", delay: .1 });
    G.fromTo($("img", photos[active]), { scale: 1.2 }, { scale: 1.08, duration: 2, ease: "power3.out" });
    G.set(title, { opacity: 1 }); riseTitle();
    G.fromTo($$("[data-sc-item]", panel), { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power2.out", stagger: .05, delay: .3, overwrite: "auto" });
    G.fromTo(cuts[active], { opacity: 0, y: 30, scale: .9 }, { opacity: 1, y: 0, scale: 1, duration: 1, ease: "power3.out", delay: .35 });
    floatCut(active);
  });

  /* ================= everything below the fold ================= */
  $$(".col-intro, .cat, .all-band, .cross, footer").forEach((el) => S.initReveals(el));
  $$(".cat-photo img").forEach((img) => { if (reduced) return; G.fromTo(img, { scale: 1.1 }, { scale: 1, ease: "none", scrollTrigger: { trigger: img.parentElement, start: "top bottom", end: "bottom top", scrub: true } }); });
  S.initRails(document);
  // "Discover the collection" scrolls with Lenis
  cta && cta.addEventListener("click", (e) => { const target = $(cta.getAttribute("href")); if (!target) return; e.preventDefault(); S.scrollTo(target, 1.2); });
}
STAGR.onReady.push(initAnimations);
'''.replace("__GROUPS__", groups_json)

    return {
        "file": f"{line}s.html",
        "key": line + "s",
        "title": f"{title} — STAGR.",
        "description": blurb,
        "css": css,
        "body": body,
        "js": js,
        "header_dark": True,
        "shop_href": f"shop.html?line={title.lower()}",
    }


def render(ctx):
    return [page(ctx, "wallet"), page(ctx, "belt")]
