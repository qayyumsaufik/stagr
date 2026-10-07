"""wallets.html and belts.html — collection pages, in the same language as the home page.

Full-bleed photo hero with the line name, piece count and two buttons; a row of
category cards; one section per category (serif heading, photo from the shoot on
the left, rail of catalogue cards on the right); a band to the full shop grid;
a cross-sell rail for the other line; the "Why people choose Stagr" block.
"""


def page(ctx, line):
    P = [p for p in ctx["products"] if p["line"] == line]
    by = {p["id"]: p for p in ctx["products"]}
    B = ctx["brand"]
    I = ctx["icon"]
    other = "belt" if line == "wallet" else "wallet"
    title = "Wallets" if line == "wallet" else "Belts"
    other_title = "Belts" if line == "wallet" else "Wallets"
    fmt = lambda n: "Rs " + format(n, ",d")
    n_p, min_p = len(P), min(p["price"] for p in P)

    if line == "wallet":
        hero = dict(img="hero-wallets", alt="An open Stagr bifold holding cards, beside thread and tools on burlap", kicker=f"Wallets · {n_p} pieces, from {fmt(min_p)}", h1="Folded, skived,<br>stitched by hand.", sub="Bifolds, trifolds, minimalist and long wallets, cut from full crazy horse hides and lined in calf. Boxed with a handwritten note.")
        groups = [
            dict(key="bifold", name="Bifold wallets", short="Bifold", ids=["kingsmann", "regal"], line1="The everyday fold.", sub="Cards one side, notes the other. Flat in a jacket pocket."),
            dict(key="trifold", name="Trifold wallets", short="Trifold", ids=["majestic"], line1="Three folds, one hide.", sub="A flip-out card flap and room for everything."),
            dict(key="minimalist", name="Minimalist", short="Minimalist", ids=["maverick", "purefold"], line1="For a front pocket.", sub="A few cards, a folded note, nothing else."),
            dict(key="long", name="Long wallets", short="Long", ids=["rodeo", "upbuck"], line1="Cards, notes, a snap.", sub="Full-length slots, a snap closure, a phone-sized pocket."),
        ]
    else:
        hero = dict(img="hero-belts", alt="Four Stagr belts laid on a walnut bench", kicker=f"Belts · {n_p} pieces, from {fmt(min_p)} · Sizes 30 to 44", h1="Cut along<br>the spine.", sub="Straps are cut where the hide is tightest, so a belt holds its shape instead of curling. Solid buckle on a removable screw post.")
        groups = [
            dict(key="nova", name="Nova", short="Nova", ids=["nova"], line1="Two sides, one belt.", sub="Black on one face, brown on the other, with a swivel buckle."),
            dict(key="outlaw", name="Outlaw", short="Outlaw", ids=["outlaw"], line1="Rugged, with a brass buckle.", sub="The thickest strap in the range. Wears in, never out."),
            dict(key="regent", name="Regent", short="Regent", ids=["regent"], line1="Black, cut in one piece.", sub="The quiet one, for a suit or a dark jean."),
            dict(key="monarch", name="Monarch", short="Monarch", ids=["monarch"], line1="Tan that deepens with wear.", sub="Starts honey, ends chestnut. Every scuff stays."),
        ]
    for g in groups:
        g["products"] = [by[i] for i in g["ids"]]
        g["from"] = min(p["price"] for p in g["products"])
        g["colours"] = sorted({c for p in g["products"] for c in p["colours"]})

    cat_cards = "".join(f'<a class="ex-card" href="#{g["key"]}" data-reveal data-delay="{i * .06}"><span class="ex-media"><img src="assets/categories/{g["key"]}-500.jpg" srcset="assets/categories/{g["key"]}-500.jpg 500w, assets/categories/{g["key"]}.jpg 900w" sizes="(min-width: 1024px) 22vw, (min-width: 640px) 30vw, 46vw" alt="{g["name"]}" width="900" height="600" loading="lazy"></span><b>{g["name"]}</b><span>{len(g["products"])} {"style" if len(g["products"]) == 1 else "styles"} · from {fmt(g["from"])}</span></a>' for i, g in enumerate(groups))

    def cat_section(i, g):
        cards = "".join(ctx["ccard"](ctx, p, P.index(p)) for p in g["products"])
        return f'''
<section class="cat on-bone{" cat--single" if len(g["products"]) == 1 else " cat--two" if len(g["products"]) == 2 else ""}" id="{g["key"]}" aria-labelledby="cat-{g["key"]}">
  <div class="wrap" data-rail>
    <div class="cat-head">
      <div><p class="label" data-reveal>{g["name"]} · {len(g["products"])} {"style" if len(g["products"]) == 1 else "styles"} · {" / ".join(g["colours"])}</p><h2 class="explore-title cat-title" id="cat-{g["key"]}" data-reveal data-delay=".05">{g["line1"]}</h2><p class="explore-sub" data-reveal data-delay=".1">{g["sub"]}</p></div>
      <div class="rail-nav" data-reveal data-delay=".15"><button type="button" class="rail-btn" data-rail-prev aria-label="Previous" style="transform:scaleX(-1)">{I["arrow"]}</button><button type="button" class="rail-btn" data-rail-next aria-label="Next">{I["arrow"]}</button></div>
    </div>
    <div class="cat-row">
      <figure class="cat-photo" data-reveal><img src="assets/categories/{g["key"]}.jpg" srcset="assets/categories/{g["key"]}.jpg 900w, assets/categories/{g["key"]}-1400.jpg 1400w" sizes="(min-width: 1024px) 34vw, 100vw" alt="{g["name"]}" width="1400" height="933" loading="lazy"></figure>
      <div class="rail-track cc-track cat-track" data-rail-track data-reveal data-delay=".1">{cards}</div>
      {f'<figure class="cat-photo cat-photo-2" data-reveal data-delay=".15"><img src="assets/categories/{g["key"]}-alt.jpg" srcset="assets/categories/{g["key"]}-alt.jpg 900w, assets/categories/{g["key"]}-alt-1400.jpg 1400w" sizes="(min-width: 1024px) 34vw, 100vw" alt="{g["name"]}, another view" width="1400" height="933" loading="lazy"></figure>' if len(g["products"]) == 1 else ""}
    </div>
  </div>
</section>'''

    cat_sections = "".join(cat_section(i, g) for i, g in enumerate(groups))
    cross = [p for p in ctx["products"] if p["line"] == other]
    cross_cards = "".join(ctx["ccard"](ctx, p, i) for i, p in enumerate(cross))

    css = r'''
/* ---- hero ---- */
.chero { position: relative; height: calc(100svh - 76px); min-height: 560px; max-height: 860px; overflow: hidden; background: var(--ink); color: var(--bone); display: flex; align-items: flex-end; }
.chero picture, .chero img { position: absolute; inset: 0; width: 100%; height: 100%; }
.chero img { object-fit: cover; object-position: 50% 55%; transform: scale(1.04); will-change: transform; }
.chero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(26,27,29,.55) 0%, rgba(26,27,29,0) 28%, rgba(26,27,29,0) 45%, rgba(26,27,29,.78) 100%), linear-gradient(90deg, rgba(26,27,29,.5) 0%, rgba(26,27,29,0) 60%); pointer-events: none; }
.chero-copy { position: relative; z-index: 2; width: 100%; padding-bottom: clamp(48px, 8vh, 96px); }
.chero-copy > * { max-width: 720px; }
.hero-kicker { font-size: .6875rem; letter-spacing: .3em; text-transform: uppercase; color: rgba(239,237,230,.8); }
.hero-h1 { margin-top: 14px; font-family: var(--font-display); font-weight: 500; font-size: clamp(2.6rem, 1.2rem + 4.2vw, 5.375rem); line-height: 1; text-shadow: 0 2px 30px rgba(0,0,0,.45); }
.hero-sub { margin-top: 18px; max-width: 46ch; font-size: clamp(.9375rem, .9rem + .25vw, 1.0625rem); line-height: 1.55; color: rgba(239,237,230,.88); text-shadow: 0 1px 14px rgba(0,0,0,.45); }
.hero-ctas { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
.btn--tan { background: var(--accent-deep); border-color: var(--accent-deep); color: var(--bone); }
.btn--tan:hover { background: var(--accent); border-color: var(--accent); color: var(--ink); }
.chero .btn--ghost { color: var(--bone); border-color: rgba(239,237,230,.55); background: rgba(26,27,29,.2); backdrop-filter: blur(6px); }
.chero .btn--ghost:hover { background: var(--bone); color: var(--ink); }
/* ---- category strip ---- */
.cstrip { padding: clamp(40px, 6vw, 72px) 0 clamp(8px, 2vw, 16px); background: var(--bone); color: var(--ink); }
.cstrip .explore-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; margin-bottom: clamp(20px, 3vw, 32px); }
.cstrip .explore-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.explore-all { display: inline-flex; align-items: center; gap: 8px; font-size: .8125rem; font-weight: 500; color: var(--accent-deep); white-space: nowrap; }
.explore-all svg { width: 14px; height: 14px; transition: transform .3s var(--ease-out); }
.explore-all:hover svg { transform: translateX(3px); }
.explore-grid { display: grid; gap: 14px; }
.ex-card { display: grid; justify-items: center; text-align: center; gap: 4px; color: var(--ink); }
.ex-media { position: relative; display: block; width: 100%; aspect-ratio: 3 / 2; border-radius: 8px; overflow: hidden; background: var(--ink); margin-bottom: 10px; }
.ex-media img { width: 100%; height: 100%; object-fit: cover; display: block; transform: scale(1.02); transition: transform .9s var(--ease-out); }
.ex-card:hover .ex-media img { transform: scale(1.08); }
.ex-card b { font-weight: 600; font-size: .9375rem; }
.ex-card span:last-child { font-size: .8125rem; color: var(--fg-2); }
/* ---- one section per category ---- */
.cat { padding: clamp(40px, 6vw, 80px) 0; background: var(--bone); color: var(--ink); }
.cat + .cat { padding-top: 0; }
.cat-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: clamp(20px, 3vw, 28px); }
.cat-title { font-size: clamp(1.8rem, 1.2rem + 2vw, 3rem); }
.cat-row { display: grid; gap: 16px; grid-template-columns: 1fr; }
.cat-photo { position: relative; overflow: hidden; border-radius: 14px; background: var(--ink); aspect-ratio: 3 / 2; }
.cat-photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.cat-track { --rail-w: calc((100% - 12px) / 2); gap: 12px; }
.wrap:not(.has-overflow) .rail-nav { visibility: hidden; }
@media (min-width: 1024px) { .cat-row { grid-template-columns: minmax(0, 4fr) minmax(0, 8fr); gap: 20px; align-items: stretch; } .cat-photo { aspect-ratio: auto; min-height: 100%; } .cat-track { --rail-w: calc((100% - 20px) / 2); gap: 20px; min-width: 0; } .cat--single .cat-row { grid-template-columns: minmax(0, 4fr) minmax(0, 3.2fr) minmax(0, 4.8fr); } .cat--single .cat-track { --rail-w: 100%; } }
@media (max-width: 1023px) { .cat-photo-2 { display: none; } .cat--single .cat-track { --rail-w: 100%; } }
@media (min-width: 640px) and (max-width: 1023px) { .cat--single .cat-row { grid-template-columns: 1fr 1fr; } .cat--single .cat-track { --rail-w: 100%; } }
@media (min-width: 1400px) { .cat-track { --rail-w: calc((100% - 40px) / 3); } .cat--two .cat-track { --rail-w: calc((100% - 20px) / 2); } }
/* ---- all band + cross ---- */
.all-band { padding: clamp(40px, 6vw, 80px) 0; background: var(--ink); color: var(--bone); text-align: center; }
.all-band .explore-title { color: var(--bone); max-width: 20ch; margin: 0 auto; }
.all-band .explore-sub { color: rgba(239,237,230,.78); margin: 14px auto 24px; max-width: 48ch; }
.cross { padding: clamp(40px, 6vw, 80px) 0 0; background: var(--bone); color: var(--ink); }
.cross .cat-head { margin-bottom: clamp(20px, 3vw, 28px); }
.cross .cc-foot { margin-top: 14px; }
@media (max-width: 1023px) { .cstrip .explore-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 767px) {
  .chero { height: 100svh; min-height: 560px; max-height: 820px; }
  .chero img { object-position: 50% 40%; }
  .chero::after { background: linear-gradient(180deg, rgba(26,27,29,.6) 0%, rgba(26,27,29,.05) 30%, rgba(26,27,29,.15) 48%, rgba(26,27,29,.86) 100%); }
  .chero-copy { padding-bottom: 56px; }
  .hero-ctas .btn { flex: 1 1 auto; justify-content: center; }
  .cstrip .explore-head { flex-direction: column; align-items: flex-start; gap: 10px; }
  .cstrip .explore-grid { gap: 10px; }
  .cat-head { flex-direction: column; align-items: flex-start; }
}
'''

    body = f'''
<section class="chero" aria-label="{title}">
  <picture><source media="(max-width: 767px)" srcset="assets/categories/{hero["img"]}-portrait.jpg"><img data-hero-img src="assets/categories/{hero["img"]}-1200.jpg" srcset="assets/categories/{hero["img"]}-800.jpg 800w, assets/categories/{hero["img"]}-1200.jpg 1200w, assets/categories/{hero["img"]}-2000.jpg 2000w" sizes="100vw" alt="{hero["alt"]}" width="2000" height="1333" fetchpriority="high" decoding="async"></picture>
  <div class="wrap chero-copy">
    <p class="hero-kicker" data-hero-item>{hero["kicker"]}</p>
    <h1 class="hero-h1" data-hero-item>{hero["h1"]}</h1>
    <p class="hero-sub" data-hero-item>{hero["sub"]}</p>
    <div class="hero-ctas" data-hero-item><a class="btn btn--tan" href="#{groups[0]["key"]}">Browse {title.lower()} {I["arrow"]}</a><a class="btn btn--ghost" href="shop.html?line={title.lower()}">View all pieces</a></div>
  </div>
</section>

<section class="cstrip" aria-labelledby="cstrip-title">
  <div class="wrap">
    <div class="explore-head">
      <div><h2 class="explore-title" id="cstrip-title" data-reveal>{title} by category</h2><p class="explore-sub" data-reveal data-delay=".1">Start with the right cut. Everything else follows.</p></div>
      <a class="explore-all" href="shop.html?line={title.lower()}" data-reveal data-delay=".15">View all {title.lower()} {I["arrow"]}</a>
    </div>
    <div class="explore-grid">{cat_cards}</div>
  </div>
</section>
{cat_sections}
<section class="all-band" aria-labelledby="all-title">
  <div class="wrap">
    <h2 class="explore-title" id="all-title" data-reveal>Every {title.lower()[:-1]}, side by side.</h2>
    <p class="explore-sub" data-reveal data-delay=".1">Filter by colour, style and price, sort, and compare all {n_p} {title.lower()} in one grid.</p>
    <a class="btn btn--tan" href="shop.html?line={title.lower()}" data-reveal data-delay=".2">View all {title.lower()} {I["arrow"]}</a>
  </div>
</section>

<section class="cross" aria-labelledby="cross-title">
  <div class="wrap" data-rail>
    <div class="cat-head">
      <div><p class="label" data-reveal>Complete the look</p><h2 class="explore-title cat-title" id="cross-title" data-reveal data-delay=".05">{"A belt to match." if line == "wallet" else "A wallet to match."}</h2></div>
      <a class="explore-all" href="{other}s.html" data-reveal data-delay=".1">All {other_title.lower()} {I["arrow"]}</a>
    </div>
    <div class="rail-track cc-track" data-rail-track data-reveal data-delay=".1">{cross_cards}</div>
    <div class="cc-foot"><span></span><div class="rail-nav"><button type="button" class="rail-btn" data-rail-prev aria-label="Previous" style="transform:scaleX(-1)">{I["arrow"]}</button><button type="button" class="rail-btn" data-rail-next aria-label="Next">{I["arrow"]}</button></div></div>
  </div>
</section>

{ctx["why"](ctx)}
'''

    js = r'''
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, reduced = S.reduced;
  if (!G) return;
  const img = $("[data-hero-img]"), items = $$("[data-hero-item]");
  if (!reduced) { G.set(items, { y: 18, opacity: 0 }); }
  S.onLoaderDone.push(() => { if (reduced) return; G.fromTo(img, { scale: 1.14 }, { scale: 1.04, duration: 2.6, ease: "power2.out", clearProps: "transform" }); G.to(items, { y: 0, opacity: 1, duration: .7, ease: "power3.out", stagger: .08, delay: .2, clearProps: "transform" }); });
  $$(".cstrip, .cat, .all-band, .cross, #why, footer").forEach((el) => S.initReveals(el));
  $$(".cat-photo img").forEach((im) => { if (reduced) return; G.fromTo(im, { scale: 1.1 }, { scale: 1, ease: "none", scrollTrigger: { trigger: im.parentElement, start: "top bottom", end: "bottom top", scrub: true } }); });
  S.initRails(document);
  // deep links from the mega menu: wallets.html#long, ?style=Long
  const want = (new URLSearchParams(location.search).get("style") || "").toLowerCase();
  if (want && !location.hash) { const el = $("#" + want); if (el) setTimeout(() => S.scrollTo(el, 1), 800); }
  $$('a[href^="#"]').forEach((a) => a.addEventListener("click", (e) => { const el = $(a.getAttribute("href")); if (!el) return; e.preventDefault(); S.scrollTo(el, 1.1); }));
  window.addEventListener("load", () => ST.refresh());
}
STAGR.onReady.push(initAnimations);
'''

    return {
        "file": f"{line}s.html",
        "key": line + "s",
        "title": f"{title} — STAGR.",
        "description": ctx["products_doc"]["lines"][line]["blurb"],
        "css": css,
        "body": body,
        "js": js,
        "header_dark": True,
        "shop_href": f"shop.html?line={title.lower()}",
    }


def render(ctx):
    return [page(ctx, "wallet"), page(ctx, "belt")]
