"""index.html — home, STILL-style choreography adapted to Stagr."""
import json


def render(ctx):
    P = ctx["products"]
    B = ctx["brand"]
    I = ctx["icon"]
    by = {p["id"]: p for p in P}
    fmt = lambda n: "Rs " + format(n, ",d")
    cut = lambda pid, i=0: ctx["cutouts"](by[pid])[i]

    # ---------------- 02 range: five families ----------------
    families = [
        dict(key="bifold", num="01", tag="Bifold", name="Kingsmann", dot=True, sub="Bifold · Kingsmann & Regal", copy=f'{by["kingsmann"]["tagline"]} {ctx["products_doc"]["lines"]["wallet"]["blurb"]}', ids=["kingsmann", "regal"], cutout=cut("kingsmann"), bloom="#D9B07A", href="wallets.html"),
        dict(key="trifold", num="02", tag="Trifold", name="Majestic", dot=True, sub="Trifold · Majestic", copy=f'{by["majestic"]["tagline"]}. Three folds, one row of saddle stitch, cut from a single hide.', ids=["majestic"], cutout=cut("majestic"), bloom="#CDA373", href="wallets.html"),
        dict(key="minimal", num="03", tag="Minimalist", name="Maverick", dot=True, sub="Minimalist · Maverick & Purefold", copy=f'{by["maverick"]["tagline"]}. {by["purefold"]["tagline"]}. The slim ones, for a front pocket.', ids=["maverick", "purefold"], cutout=cut("maverick"), bloom="#DABF9A", href="wallets.html"),
        dict(key="long", num="04", tag="Long", name="Rodeo", dot=True, sub="Long · Rodeo & Upbuck", copy=f'{by["rodeo"]["tagline"]}. {by["upbuck"]["tagline"]}. Cards, notes and a snap closure.', ids=["rodeo", "upbuck"], cutout=cut("rodeo"), bloom="#C8976A", href="wallets.html"),
        dict(key="belts", num="05", tag="Belts", name="Monarch", dot=True, sub="Belts · Nova, Outlaw, Regent & Monarch", copy=ctx["products_doc"]["lines"]["belt"]["blurb"], ids=["nova", "outlaw", "regent", "monarch"], cutout=cut("monarch"), bloom="#C9B290", href="belts.html"),
    ]
    for f in families:
        items = [by[i] for i in f["ids"]]
        f["from"] = min(p["price"] for p in items)
        f["colours"] = " / ".join(sorted({c for p in items for c in p["colours"]}, key=lambda c: ["Brown", "Tan", "Black"].index(c) if c in ["Brown", "Tan", "Black"] else 9))
        f["count"] = len(items)
        f["names"] = ", ".join(p["name"].split(" ")[0] for p in items)
    belt_for = {"bifold": "nova", "trifold": "outlaw", "minimal": "regent", "long": "monarch", "belts": "nova"}
    for f in families:
        f["belt"] = cut(belt_for[f["key"]])

    def panel(f, i, mobile=False):
        rows = [("Leather", "Crazy horse"), ("Colours", f["colours"]), ("From", fmt(f["from"])), ("Pieces", f'{f["count"]} · {f["names"]}')]
        spec = "".join(f'<div data-stage-item><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
        return f'''
<div class="rpanel" data-range-panel="{i}" {"hidden" if i and not mobile else ""}>
  <div class="rp-head" data-stage-item><span class="pcard-num">STAGR.{f["num"]}</span><span class="label">{f["tag"]}</span></div>
  <h3 class="rp-name" data-range-title>{f["name"]}<span class="dotc">.</span></h3>
  <p class="serif-i muted rp-sub" data-stage-item>{f["sub"]}</p>
  <p class="rp-copy" data-stage-item>{f["copy"]}</p>
  <dl class="spec rp-spec">{spec}</dl>
  <p data-stage-item style="margin-top:18px"><a class="btn btn--text" href="{f["href"]}">Shop {f["tag"].lower() if f["tag"] != "Belts" else "belts"} {I["arrow"]}</a></p>
</div>'''

    panels = "".join(panel(f, i) for i, f in enumerate(families))
    stage_cuts = "".join(f'<div class="cut rcut" data-range-cut="{i}"><div class="pair{" belts" if f["key"] == "belts" else ""}"><img class="p-belt" src="{f["belt"]["src"]}" alt="" width="900" height="900" draggable="false" decoding="async"><img class="p-wallet" src="{f["cutout"]["src"]}" alt="{f["name"]} {f["tag"].lower()} in {f["cutout"]["colour"].lower()} crazy horse leather" width="900" height="900" draggable="false" decoding="async"></div></div>' for i, f in enumerate(families))
    stage_blooms = "".join(f'<div class="bloom" data-range-bloom="{i}" style="--bloom:{f["bloom"]};opacity:{1 if i == 0 else 0}" data-bloom></div>' for i, f in enumerate(families))
    stage_ghosts = "".join(f'<span class="ghost" data-range-ghost="{i}" style="opacity:{1 if i == 0 else 0}">{f["num"]}</span>' for i, f in enumerate(families))
    dots = "".join(f'<button type="button" data-range-dot="{i}" aria-label="Show {f["tag"]}" style="color:{"var(--fg)" if i == 0 else "var(--fg-2)"}">{f["num"]}</button>' for i, f in enumerate(families))
    mcards = "".join(f'''
<article class="mcard" data-mcard>
  <div class="cut mcut"><div class="bloom" style="--bloom:{f["bloom"]}" data-bloom></div><div class="pair{" belts" if f["key"] == "belts" else ""}"><img class="p-belt" src="{f["belt"]["small"]}" alt="" width="600" height="600" loading="lazy" draggable="false"><img class="p-wallet" src="{f["cutout"]["small"]}" alt="" width="600" height="600" loading="lazy" draggable="false"></div></div>
  <div class="rp-head"><span class="pcard-num">STAGR.{f["num"]}</span><span class="label">{f["tag"]}</span></div>
  <h3 class="rp-name" data-mcard-title>{f["name"]}<span class="dotc">.</span></h3>
  <p class="serif-i muted rp-sub" data-card-item>{f["sub"]}</p>
  <p class="rp-copy" data-card-item>{f["copy"]}</p>
  <dl class="spec rp-spec" data-card-item>{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in [("Leather", "Crazy horse"), ("Colours", f["colours"]), ("From", fmt(f["from"]))])}</dl>
  <p data-card-item style="margin-top:14px"><a class="btn btn--text" href="{f["href"]}">Shop {I["arrow"]}</a></p>
</article>''' for f in families)
    mdots = "".join(f'<button type="button" data-mrange-dot="{i}" style="color:{"var(--fg)" if i == 0 else "var(--fg-2)"}">{f["num"]}</button>' for i, f in enumerate(families))

    # ---------------- 03 inside: what every piece is made of ----------------
    inside = [
        dict(tab="Belts", name="Cut along<br>the spine", sub="Belts · 4 pieces · Sizes 30 to 44", desc="Straps are cut where the hide is tightest, so a belt holds its shape instead of curling. Solid buckle on a removable screw post, so you can change it without tools.",
             rows=[("Leather", "Full grain crazy horse"), ("Buckle", "Solid, on a screw post"), ("Sizes", "30 to 44")], point="Measure from the buckle bar, not the tip", n=4, unit="pieces", bar=4 / 11, href="belts.html", cta="Shop belts",
             svg='<rect data-bot x="8" y="12" width="28" height="20" rx="6"/><path data-bot d="M8 22h22"/><circle data-bot cx="30" cy="22" r="2"/>'),
        dict(tab="Wallets", name="Folded,<br>skived, stitched", sub="Wallets · 7 pieces · Stitched by hand", desc="Bifolds, trifolds and long wallets that soften and darken with every carry. Skived at the folds so each one stays flat in a jacket pocket.",
             rows=[("Leather", "Full grain crazy horse"), ("Stitch", "Saddle, waxed linen"), ("Styles", "Bifold, trifold, minimalist, long")], point="Choose the fold and the colour", n=7, unit="pieces", bar=7 / 11, href="wallets.html", cta="Shop wallets",
             svg='<path data-bot d="M4 24l6-6 6 6 6-6 6 6 6-6 6 6"/><path data-bot d="M4 32l6-6 6 6 6-6 6 6 6-6 6 6"/>'),
    ]
    N_INSIDE = len(inside)
    inside_imgs = [cut("monarch"), cut("kingsmann")]
    inside_stack = lambda size: "".join(f'<img data-inside-img="{i}" src="{im[size]}" alt="" width="900" height="900" draggable="false" decoding="async" style="opacity:{1 if i == 0 else 0}">' for i, im in enumerate(inside_imgs))
    pills = "".join(f'<button type="button" class="pill" data-inside-pill="{i}" aria-pressed="{str(i == 0).lower()}">{d["tab"]}</button>' for i, d in enumerate(inside))
    lefts = "".join(f'''
<div data-inside-left="{i}" {"hidden" if i else ""}>
  <div data-inside-hover><h3 class="inside-name" data-inside-name>{d["name"]}</h3></div>
  <div class="inside-sci" data-inside-sci><svg data-inside-svg viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" aria-hidden="true">{d["svg"]}</svg><span class="serif-i">{d["sub"]}</span></div>
</div>''' for i, d in enumerate(inside))
    rights = "".join(f'''
<div data-inside-right="{i}" {"hidden" if i else ""}>
  <p class="label"><b>0{i + 1}</b><span class="slash">/</span>0{N_INSIDE}</p>
  <p class="inside-desc">{d["desc"]}</p>
  <dl class="spec" style="margin-top:20px">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in d["rows"])}</dl>
  <div class="inside-measure"><dl class="spec"><div><dt>Measure</dt><dd><span class="num" style="font-size:1.1rem" data-inside-dose="{d["n"]}">0</span> <span class="small muted">{d["unit"]}</span></dd></div></dl><div class="inside-bar"><i data-inside-bar="{d["bar"]}"></i></div></div>
  <p class="inside-point"><span aria-hidden="true">+</span>{d["point"]}</p>
  <a class="btn btn--tan inside-cta" href="{d["href"]}">{d["cta"]} {I["arrow"]}</a>
</div>''' for i, d in enumerate(inside))
    deck = "".join(f'''
<article class="deck-card" data-halo="{["#CDA373", "#D9B07A"][i]}">
  <p class="label"><b>0{i + 1}</b><span class="slash">/</span>0{N_INSIDE}</p>
  <h3 class="inside-name" data-deck-title style="margin-top:12px">{d["tab"]}: {d["name"].replace("<br>", " ").lower()}</h3>
  <p class="serif-i muted" data-deck-item>{d["sub"]}</p>
  <p class="inside-desc" data-deck-item>{d["desc"]}</p>
  <dl class="spec" data-deck-item style="margin-top:16px">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in d["rows"])}</dl>
  <p class="inside-point" data-deck-item><span aria-hidden="true">+</span>{d["point"]}</p>
  <p data-deck-item style="margin-top:18px"><a class="btn btn--tan btn--wide" href="{d["href"]}">{d["cta"]} {I["arrow"]}</a></p>
</article>''' for i, d in enumerate(inside))

    # ---------------- 04 story: five chapters ----------------
    chapters = [
        dict(n="01", title="The name", text=B["about"]["sections"][0]["body"], img="assets/lifestyle/ranger-02.jpg", cap="FIG. 01 · The stag, embossed in crazy horse leather"),
        dict(n="02", title=B["craft"]["steps"][0]["title"], text=B["craft"]["steps"][0]["body"] + " " + B["about"]["sections"][1]["body"], img="assets/lifestyle/ranger-flat.jpg", cap="FIG. 02 · Graded hide, embossed strap tip"),
        dict(n="03", title=B["craft"]["steps"][1]["title"], text=B["craft"]["steps"][1]["body"], img="assets/lifestyle/onyx-flat.jpg", cap="FIG. 03 · A cut strap, backlit"),
        dict(n="04", title=B["craft"]["steps"][2]["title"], text=B["craft"]["steps"][2]["body"], img="assets/lifestyle/kingsmen-02.jpg", cap="FIG. 04 · Saddle stitch on a wallet edge"),
        dict(n="05", title=B["craft"]["steps"][3]["title"], text=B["craft"]["steps"][3]["body"] + " " + B["about"]["sections"][2]["body"], img="assets/lifestyle/monarch-01.jpg", cap="FIG. 05 · Finished belt, buckle on"),
    ]
    figures = "".join(f'<div class="story-figure" data-story-figure="{i}" style="opacity:{1 if i == 0 else 0}"><figure><div class="media ar-45"><img src="{c["img"]}" srcset="{c["img"].replace(".jpg", "-800.jpg")} 800w, {c["img"]} 1600w" sizes="(min-width: 768px) 34vw, 86vw" alt="{c["cap"]}" width="1200" height="1500" loading="lazy"></div><figcaption class="label" style="margin-top:12px;font-size:.75rem"><span style="color:var(--accent)">■</span> {c["cap"]}</figcaption></figure></div>' for i, c in enumerate(chapters))
    ghosts = "".join(f'<span class="ghost story-ghost" data-story-ghost="{i}" style="opacity:{1 if i == 0 else 0}">{c["n"]}</span>' for i, c in enumerate(chapters))
    spanels = "".join(f'<div class="story-panel" data-story-panel="{i}" {"hidden" if i else ""}><p class="label" data-story-item>Chapter {c["n"]}<span class="slash">·</span><b>{c["title"]}</b></p><div class="rule" data-story-item style="margin-top:18px"></div><h3 class="h3" data-story-item style="margin-top:22px">{c["title"]}.</h3><p class="body muted" data-story-item style="margin-top:16px">{c["text"]}</p></div>' for i, c in enumerate(chapters))
    years = "".join(f'<button type="button" data-story-year="{i}" style="color:{"var(--fg)" if i == 0 else "var(--fg-2)"}">{c["n"]}</button>' for i, c in enumerate(chapters))
    mstory_figs = "".join(f'<div class="mstory-figure" data-mstory-figure="{i}"><img src="{c["img"].replace(".jpg", "-800.jpg")}" alt="{c["cap"]}" width="800" height="1000" loading="lazy"></div>' for i, c in enumerate(chapters))
    mstory_ghosts = "".join(f'<span class="ghost" data-mstory-ghost="{i}" style="opacity:{1 if i == 0 else 0}">{c["n"]}</span>' for i, c in enumerate(chapters))
    mstory_panels = "".join(f'<div data-mstory-panel="{i}" {"hidden" if i else ""}><p class="label">Chapter {c["n"]}<span class="slash">·</span><b>{c["title"]}</b></p><h3 class="h3" data-mstory-title style="margin-top:14px">{c["title"]}.</h3><p class="body muted" data-mstory-text style="margin-top:14px">{c["text"]}</p></div>' for i, c in enumerate(chapters))
    myears = "".join(f'<button type="button" data-mstory-year="{i}" style="color:{"var(--fg)" if i == 0 else "var(--fg-2)"}">{c["n"]}</button>' for i, c in enumerate(chapters))

    # ---------------- 05 promise ----------------
    values = [B["about"]["values"][0], B["about"]["values"][2], B["about"]["values"][3]]
    quotes = "".join(f'<figure class="pquote" data-press-quote><blockquote class="serif-i" data-quote-visual>“{v["body"]}”</blockquote><figcaption class="label" style="margin-top:14px">{v["title"]}</figcaption></figure>' for v in values)
    ticker = B["ticker"]
    mq_solid = "".join(f'<span>{t}</span><span class="mq-dot">·</span>' for t in ticker * 2)
    mq_outline = "".join(f'<span class="outline">{t}</span><span class="mq-dot">·</span>' for t in list(reversed(ticker)) * 2)

    # ---------------- 06 shop ----------------
    TAGS = ctx["tags"]
    SW = ctx["swatch"]; BADGE = {"best": "Bestseller", "new": "New in", "gift": "Gift pick"}
    heart = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 20.5s-7.5-4.6-7.5-10A4.2 4.2 0 0 1 12 8.2a4.2 4.2 0 0 1 7.5 2.3c0 5.4-7.5 10-7.5 10z"/></svg>'
    def ccard(p, i):
        cuts = ctx["cutouts"](p); main = cuts[0]; same = [c for c in cuts if c["colour"] == main["colour"]]; alt = same[1] if len(same) > 1 else None
        tags = TAGS.get(p["id"], []); fmt = lambda n: "Rs " + format(n, ",d")
        off = round(100 - p["price"] / p["compareAtPrice"] * 100) if p.get("compareAtPrice") else 0
        badges = (f'<span class="cc-badge cc-sale">Sale -{off}%</span>' if off else "") + (f'<span class="cc-badge cc-best">&#9733; Bestseller</span>' if "best" in tags else "") + (f'<span class="cc-badge cc-new">New in</span>' if "new" in tags and "best" not in tags else "")
        swatches = "".join(f'<label class="cc-sw" title="{c}"><input type="radio" name="h-{p["id"]}" value="{c}" {"checked" if c == p["defaultColour"] else ""}><i style="--sw:{SW.get(c, "#6E4328")}"></i><span class="sr-only">{c}</span></label>' for c in p["colours"])
        meta = " / ".join(p["colours"]) + (" <i>·</i> Sizes 30 to 44" if p["line"] == "belt" else "")
        return f'''
<article class="ccard{" has-alt" if alt else ""}" data-product="{p["id"]}" data-tags="{" ".join(tags)}" data-line="{p["line"]}" data-style="{p["style"] or "Belt"}" data-colours="{",".join(p["colours"])}" data-price="{p["price"]}" data-index="{i}" data-name="{p["name"]}">
  <a class="cc-media" href="product-{p["id"]}.html" aria-label="{p["name"]}"><img class="main" src="{main["small"]}" alt="{p["name"]} in {main["colour"].lower()}" width="600" height="600" loading="lazy" draggable="false"><img class="alt" src="{(alt or main)["small"]}" alt="" width="600" height="600" loading="lazy" aria-hidden="true" draggable="false"><span class="cc-badges">{badges}</span></a>
  <div class="cc-body">
    <p class="cc-price"><b>{fmt(p["price"])}</b>{f'<s>{fmt(p["compareAtPrice"])}</s>' if p.get("compareAtPrice") else ""}</p>
    <h3 class="cc-name"><a href="product-{p["id"]}.html">{p["name"]}</a></h3>
    <p class="cc-meta">{meta}</p>
    <div class="cc-opts opts" data-colour-opts>{swatches}</div>
    <p class="cc-stock"><i></i>In stock</p>
    <div class="cc-foot"><button type="button" class="cc-add" data-add="{p["id"]}" data-colour="{p["defaultColour"]}" {"data-size=34" if p["line"] == "belt" else ""}><span aria-hidden="true">+</span> Add to cart</button><button type="button" class="cc-wish" data-wish="{p["id"]}" aria-pressed="false" aria-label="Save {p["name"]}">{heart}</button></div>
  </div>
</article>'''
    cards = "".join(ccard(p, i) for i, p in enumerate(P))
    trust = B["trust"]["items"]

    css = r'''
/* ---- shared bits ---- */
.dotc { color: var(--accent); }
.rp-name, .inside-name { font-family: var(--font-display); font-weight: 300; font-size: clamp(2.6rem, 2rem + 4vw, 5.6rem); line-height: 1; letter-spacing: -.02em; }
.inside-name { font-family: var(--font-wordmark); font-weight: 700; font-size: clamp(1.6rem, 1rem + 1.8vw, 2.5rem); letter-spacing: -.01em; line-height: 1.05; overflow-wrap: normal; word-break: keep-all; hyphens: none; }
.inside-kicker { text-align: center; color: rgba(239,237,230,.7); }
.inside-lead { margin: 0 auto; max-width: none; text-align: center; color: rgba(239,237,230,.78); font-size: .9375rem; line-height: 1.5; }
.on-ink .btn--tan { background: var(--accent-deep); border-color: var(--accent-deep); color: var(--bone); }
.on-ink .btn--tan:hover { background: var(--accent); border-color: var(--accent); color: var(--ink); }
.rp-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.rp-sub { margin-top: 10px; font-size: 1.05rem; }
.rp-copy { margin-top: 18px; max-width: 46ch; color: var(--fg-2); }
.rp-spec { margin-top: 22px; max-width: 420px; }

/* ---- 01 hero: belts left, wallets right, the words on the seam, bulk band beneath ---- */
.hero { position: relative; background: var(--ink); color: var(--bone); }
.slider { position: relative; height: calc(100svh - 76px); min-height: 620px; max-height: 980px; overflow: hidden; }
.slide { position: absolute; inset: 0; display: flex; align-items: flex-end; opacity: 0; visibility: hidden; }
.slide.is-on { opacity: 1; visibility: visible; }
.slide img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 55%; transform: scale(1.04); will-change: transform; }
.slide::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(26,27,29,.55) 0%, rgba(26,27,29,0) 28%, rgba(26,27,29,0) 45%, rgba(26,27,29,.78) 100%), linear-gradient(90deg, rgba(26,27,29,.5) 0%, rgba(26,27,29,0) 60%); pointer-events: none; }
.slide-copy { position: relative; z-index: 2; width: 100%; padding-bottom: clamp(84px, 11vh, 120px); max-width: none; }
.slide-copy > * { max-width: 760px; }
.hero-kicker { font-size: .6875rem; letter-spacing: .3em; text-transform: uppercase; color: rgba(239,237,230,.8); }
.hero-kicker span { margin: 0 6px; opacity: .6; }
.hero-h1 { margin-top: 14px; font-family: var(--font-display); font-weight: 500; font-size: clamp(2.6rem, 1.2rem + 4.2vw, 5.375rem); line-height: 1; letter-spacing: 0; text-shadow: 0 2px 30px rgba(0,0,0,.45); }
.hero-h1 .serif-i { font-family: var(--font-display); font-style: normal; }
.hero-sub { margin-top: 18px; max-width: 44ch; font-size: clamp(.9375rem, .9rem + .25vw, 1.0625rem); line-height: 1.55; color: rgba(239,237,230,.88); text-shadow: 0 1px 14px rgba(0,0,0,.45); }
.hero-ctas { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
.btn--tan { background: var(--accent-deep); border-color: var(--accent-deep); color: var(--bone); }
.btn--tan:hover { background: var(--accent); border-color: var(--accent); color: var(--ink); }
.hero .btn--ghost { color: var(--bone); border-color: rgba(239,237,230,.55); background: rgba(26,27,29,.2); backdrop-filter: blur(6px); }
.hero .btn--ghost:hover { background: var(--bone); color: var(--ink); }
.slider-ui { position: absolute; left: 0; right: 0; bottom: clamp(22px, 3vh, 36px); z-index: 3; display: flex; justify-content: space-between; align-items: center; gap: 16px; pointer-events: none; }
.slider-ui > * { pointer-events: auto; }
.slider-dots { display: flex; gap: 10px; }
.slider-dots button { width: 56px; height: 20px; display: grid; align-items: center; }
.slider-dots i { display: block; height: 2px; background: rgba(239,237,230,.35); position: relative; overflow: hidden; }
.slider-dots i::after { content: ""; position: absolute; inset: 0; background: var(--bone); transform: scaleX(var(--p, 0)); transform-origin: left; }
.slider-dots button[aria-selected="true"] i { background: rgba(239,237,230,.35); }
.slider-nav { display: flex; align-items: center; gap: 10px; }
.slider-count { font-size: .75rem; letter-spacing: .2em; color: rgba(239,237,230,.75); margin-right: 8px; font-variant-numeric: tabular-nums; }
.slider-count b { font-weight: 500; color: var(--bone); }
.half-arrow { width: 44px; height: 44px; border-radius: 50%; border: 1px solid rgba(239,237,230,.5); display: grid; place-items: center; color: var(--bone); background: rgba(26,27,29,.25); backdrop-filter: blur(6px); transition: background-color .3s ease, color .3s ease, border-color .3s ease; }
.half-arrow svg { width: 16px; height: 16px; }
.half-arrow:hover { background: var(--bone); color: var(--ink); border-color: var(--bone); }
/* bulk-order band */
.bulk-band { position: relative; background: var(--accent-deep); color: var(--bone); overflow: hidden; }
.bulk-band::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: clamp(60px, 7vw, 110px); background: var(--accent); clip-path: polygon(0 0, 100% 0, 55% 100%, 0 100%); opacity: .9; }
.bulk-inner { position: relative; display: flex; align-items: center; gap: 16px; min-height: 76px; padding-top: 10px; padding-bottom: 10px; }
.bulk-icon { width: 40px; height: 40px; border-radius: 50%; background: rgba(239,237,230,.14); display: grid; place-items: center; flex: 0 0 auto; margin-left: clamp(60px, 7vw, 110px); }
.bulk-icon svg { width: 20px; height: 20px; }
.bulk-text { flex: 1; display: grid; gap: 2px; font-size: .8125rem; color: rgba(239,237,230,.85); }
.bulk-text b { font-weight: 500; font-size: 1rem; color: var(--bone); }
.bulk-btn { flex: 0 0 auto; background: var(--bone); color: var(--ink); border-color: var(--bone); }
.bulk-btn:hover { background: var(--ink); color: var(--bone); border-color: var(--ink); }

/* ---- the three tiles under the hero: how it is made, bulk orders, a handwritten note ---- */
/* ---- explore by category ---- */
.explore { padding: clamp(40px, 6vw, 80px) 0 clamp(16px, 2vw, 24px); background: var(--bone); color: var(--ink); }
.explore-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; margin-bottom: clamp(20px, 3vw, 32px); }
.explore-title { font-family: var(--font-display); font-weight: 300; font-size: clamp(2rem, 1.3rem + 2.8vw, 3.9rem); line-height: 1.06; letter-spacing: -.012em; }
.explore-sub { margin-top: 12px; color: var(--fg-2); font-size: .9375rem; }
.explore-right { display: flex; flex-direction: column; align-items: flex-end; gap: 16px; }
.explore-tabs { display: inline-flex; padding: 4px; border-radius: 999px; background: rgba(26,27,29,.06); }
.explore-tabs button { min-height: 36px; padding: 0 18px; border-radius: 999px; font-size: .8125rem; font-weight: 500; color: var(--fg-2); transition: background-color .3s ease, color .3s ease; }
.explore-tabs button[aria-selected="true"] { background: var(--ink); color: var(--bone); }
.explore-all { display: inline-flex; align-items: center; gap: 8px; font-size: .8125rem; font-weight: 500; color: var(--accent-deep); }
.explore-all svg { width: 14px; height: 14px; transition: transform .3s var(--ease-out); }
.explore-all:hover svg { transform: translateX(3px); }
.explore-grid { display: grid; gap: 14px; grid-template-columns: repeat(5, minmax(0, 1fr)); }
.explore-grid[hidden] { display: none; }
.ex-card { display: grid; justify-items: center; text-align: center; gap: 4px; color: var(--ink); }
.ex-media { position: relative; display: block; width: 100%; aspect-ratio: 3 / 2; border-radius: 8px; overflow: hidden; background: var(--ink); margin-bottom: 10px; }
.ex-media img { width: 100%; height: 100%; object-fit: cover; display: block; transform: scale(1.02); transition: transform .9s var(--ease-out); }
.ex-card:hover .ex-media img { transform: scale(1.08); }
.ex-card b { font-weight: 600; font-size: .9375rem; }
.ex-card span:last-child { font-size: .8125rem; color: var(--fg-2); }
@media (max-width: 1023px) { .explore-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 639px) { .explore-head { flex-direction: column; align-items: flex-start; } .explore-right { align-items: flex-start; flex-direction: row; align-items: center; gap: 14px; flex-wrap: wrap; } .explore-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; } .ex-card b { font-size: .875rem; } }
.more { padding: 16px 0 0; background: var(--bone); color: var(--ink); }
.bento { display: grid; gap: 12px; grid-template-columns: 1fr; }
.tile { position: relative; display: block; overflow: hidden; border-radius: 8px; background: var(--ink); color: var(--bone); isolation: isolate; }
.tile::before { content: ""; position: absolute; inset: 10px; border: 1px dashed rgba(239,237,230,.32); border-radius: 4px; z-index: 3; pointer-events: none; transition: inset .5s var(--ease-out), border-color .4s ease; }
.tile:hover::before { inset: 14px; border-color: var(--accent); }
.tile img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transform: scale(1.04); transition: transform 1.2s var(--ease-out); will-change: transform; }
.tile:hover img { transform: scale(1.08); }
.tile::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(26,27,29,.62) 0%, rgba(26,27,29,.28) 40%, rgba(26,27,29,.05) 70%); pointer-events: none; }
.tile-copy { position: absolute; z-index: 2; left: clamp(22px, 3vw, 44px); right: clamp(22px, 3vw, 44px); top: clamp(22px, 3vw, 40px); }
.ltag { display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px 6px 9px; border-radius: 4px; background: rgba(26,27,29,.42); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); outline: 1px dashed rgba(239,237,230,.45); outline-offset: -4px; font-size: .625rem; letter-spacing: .2em; text-transform: uppercase; color: var(--bone); }
.ltag .rivet { width: 7px; height: 7px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #E8C48E, #8B5A2B 70%); box-shadow: 0 0 0 1px rgba(0,0,0,.25); }
.tile-h1 { margin-top: 16px; font-family: var(--font-display); font-weight: 300; font-size: clamp(2rem, 1.1rem + 2.6vw, 3.8rem); line-height: 1.02; letter-spacing: -.01em; text-shadow: 0 2px 28px rgba(26,27,29,.3); }
.tile-h1 .serif-i { font-family: var(--font-display); font-style: italic; }
.tile-sub { margin-top: 14px; max-width: 38ch; font-size: clamp(.875rem, .85rem + .2vw, 1rem); line-height: 1.55; color: rgba(239,237,230,.88); text-shadow: 0 1px 12px rgba(0,0,0,.35); }
.tile-btn { margin-top: 20px; background: var(--bone); color: var(--ink); border-color: var(--bone); }
.tile:hover .tile-btn { background: var(--accent); border-color: var(--accent); }
.tile-h2 { margin-top: 12px; font-family: var(--font-display); font-weight: 300; font-size: clamp(1.6rem, 1rem + 1.6vw, 2.4rem); line-height: 1.05; text-shadow: 0 2px 20px rgba(26,27,29,.3); }
.tile-side .tile-sub { margin-top: 10px; max-width: 34ch; }
.tile-link { display: inline-flex; align-items: center; gap: 8px; margin-top: 12px; font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; color: inherit; }
.tile-link svg { width: 13px; height: 13px; transition: transform .4s var(--ease-out); }
.tile:hover .tile-link svg { transform: translateX(4px); }
.tile-main { aspect-ratio: 4 / 5; }
.tile-main img { object-position: 50% 70%; }
.tile-side { aspect-ratio: 16 / 10; }
.tile-bulk img { object-position: 50% 100%; object-fit: cover; }
.tile-note img { object-position: 50% 40%; }
.pair img { position: absolute; height: auto; filter: drop-shadow(0 40px 60px rgba(0,0,0,.45)); }
.pair .p-belt { left: -6%; top: 2%; width: 78%; transform: rotate(-8deg); }
.pair .p-wallet { right: -4%; bottom: 4%; width: 72%; }
@media (max-width: 1023px) {
  .bento { grid-template-columns: 1fr 1fr; }
  .tile-main { grid-column: 1 / -1; aspect-ratio: 16 / 10; }
  .tile-side { aspect-ratio: 4 / 5; }
}
@media (max-width: 767px) {
  .slider { height: 100svh; min-height: 580px; max-height: 820px; }
  .slide img { object-position: 50% 40%; }
  .slide::after { background: linear-gradient(180deg, rgba(26,27,29,.6) 0%, rgba(26,27,29,.05) 30%, rgba(26,27,29,.15) 48%, rgba(26,27,29,.86) 100%); }
  .slide-copy { padding-bottom: 92px; }
  .hero-ctas .btn { flex: 1 1 auto; justify-content: center; }
  .slider-ui { bottom: 22px; }
  .slider-count { display: none; }
  .half-arrow { width: 40px; height: 40px; }
  .bulk-inner { flex-wrap: wrap; padding-top: 16px; padding-bottom: 16px; }
  .bulk-icon { margin-left: 0; }
  .bulk-band::before { display: none; }
  .bulk-btn { width: 100%; }
  .bento { grid-template-columns: 1fr; gap: 10px; }
  .tile-main { aspect-ratio: 4 / 5; }
  .tile-side { aspect-ratio: 4 / 3; }
}
@media (min-width: 1024px) {
  .more { padding: 14px 0 0; }
  .bento { grid-template-columns: 56fr 44fr; grid-template-rows: 1fr 1fr; gap: 14px; height: calc(100svh - 32px); min-height: 640px; max-height: 920px; }
  .tile { aspect-ratio: auto !important; }
  .tile-main { grid-row: 1 / 3; }
}

/* ---- 02 range (pinned on desktop) ---- */
.range { position: relative; background: var(--bone); color: var(--ink); overflow: hidden; }
.range-pin { position: relative; height: 100vh; display: flex; flex-direction: column; }
.range-bg { position: absolute; inset: 0; pointer-events: none; }
.range-head { position: relative; z-index: 2; padding: calc(var(--nav-h) + 20px) var(--gutter) 0; display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }
.range-title { font-family: var(--font-display); font-weight: 300; font-size: clamp(2rem, 1.4rem + 2.6vw, 3.6rem); line-height: 1.05; letter-spacing: -.012em; margin-top: 14px; opacity: 0; }
.range-body { position: relative; z-index: 2; flex: 1; display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 32px; padding: 0 var(--gutter) 40px; align-items: center; }
.range-text { position: relative; max-width: 520px; }
.rpanel { position: absolute; inset: auto 0; top: 50%; transform: translateY(-50%); }
.range-stage { position: relative; height: 100%; min-height: 60vh; }
.rcut { position: absolute; inset: 0; width: 100%; opacity: 0; }
.rcut .pair { position: relative; width: min(70vh, 40vw); aspect-ratio: 1; }
.rcut .pair img { filter: drop-shadow(0 40px 50px rgba(26,27,29,.25)); }
.pair.belts .p-belt { left: 0; top: 6%; width: 74%; transform: rotate(-10deg); }
.pair.belts .p-wallet { right: 0; bottom: 2%; width: 66%; transform: rotate(6deg); }
.range-dots { position: absolute; right: var(--gutter); bottom: 32px; z-index: 3; display: flex; gap: 18px; font-size: 12px; letter-spacing: .2em; }
.range-dots button { color: inherit; transition: color .3s ease; }
.range-count { font-size: 12px; letter-spacing: .2em; text-transform: uppercase; color: var(--mist); font-variant-numeric: tabular-nums; }
/* mobile carousel */
.range-mobile { position: relative; padding: var(--section-sm) 0 64px; }
.range-mobile .mhead { padding: 0 20px; }
.mtrack { display: flex; gap: 5vw; overflow-x: auto; scroll-snap-type: x mandatory; padding: 24px 9vw 16px; scrollbar-width: none; }
.mtrack::-webkit-scrollbar { display: none; }
.mcard { flex: 0 0 82vw; scroll-snap-align: center; }
.mcut { height: 74vw; }
.mcut .bloom { --bloom-s: 60vw; }
.mcut .pair { position: relative; width: 78%; aspect-ratio: 1; }
.mcut .pair img { filter: drop-shadow(0 20px 30px rgba(26,27,29,.22)); }
.mcard .rp-name { font-size: 2.8rem; margin-top: 10px; opacity: 0; }
.mcard [data-card-item] { opacity: 0; }
.mdots { display: flex; justify-content: center; gap: 18px; font-size: 12px; letter-spacing: .2em; margin-top: 10px; }
.mdots button { color: inherit; }

/* ---- 03 inside (dark, pinned) ---- */
.inside { position: relative; background: var(--ink); color: var(--bone); overflow: hidden; }
.inside-pin { height: 100svh; min-height: 0; display: flex; flex-direction: column; padding: calc(var(--nav-h) + 8px) var(--gutter) 16px; overflow: hidden; }
.inside-head { text-align: center; display: grid; justify-items: center; gap: 8px; }
.inside-title { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.8rem, 1.2rem + 2vw, 3.2rem); line-height: 1.04; letter-spacing: -.012em; color: var(--bone); opacity: 0; white-space: nowrap; }
.inside-pills { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.inside .pill { border-color: rgba(239,237,230,.35); color: var(--bone); opacity: .65; }
.inside .pill[aria-pressed="true"] { background: var(--bone); color: var(--ink); border-color: var(--bone); opacity: 1; }
.inside-grid { flex: 1; display: grid; grid-template-columns: minmax(0, 4fr) minmax(0, 4fr) minmax(0, 4fr); gap: 24px; align-items: center; }
.inside-left { min-width: 0; }
.inside-sci { margin-top: 14px; display: flex; align-items: center; gap: 14px; color: rgba(239,237,230,.6); }
.inside-sci svg { width: 44px; height: 44px; flex: none; }
.inside-stage { position: relative; display: grid; place-items: center; min-height: 0; align-self: stretch; }
.inside-halo { position: absolute; inset: 0; margin: auto; width: 46vh; height: 46vh; transform: scale(1.6); border-radius: 50%; background: #D9B07A; opacity: .5; filter: blur(60px); pointer-events: none; }
.inside-float { position: relative; z-index: 1; width: min(40vh, 28vw); aspect-ratio: 1; display: grid; place-items: center; pointer-events: none; }
.inside-pills { position: relative; z-index: 2; }
.inside-float img { position: absolute; width: 100%; height: auto; max-height: 100%; object-fit: contain; filter: drop-shadow(0 40px 60px rgba(0,0,0,.5)); }
.inside-right { max-width: 420px; justify-self: end; width: 100%; }
.inside-right .spec > div { padding: 8px 0; }
@media (max-height: 820px) { .inside-measure, .inside-foot { display: none; } .inside-desc { margin-top: 10px; font-size: .9375rem; } .inside-point { margin-top: 12px; padding-top: 10px; } .inside-cta { margin-top: 12px; min-height: 44px; } .inside-float { width: min(34vh, 26vw); } .inside-pills .pill { min-height: 34px; } }
.inside-desc { margin-top: 14px; color: rgba(239,237,230,.8); max-width: 40ch; }
.inside-bar { height: 1px; background: rgba(239,237,230,.15); margin-top: 10px; }
.inside-point { margin-top: 18px; padding-top: 14px; border-top: 1px solid rgba(239,237,230,.15); font-size: .9375rem; color: var(--bone); display: flex; gap: 10px; align-items: baseline; }
.inside-point span { color: var(--accent); font-weight: 500; }
.inside-cta { margin-top: 18px; width: 100%; justify-content: center; }
.inside-bar i { display: block; height: 100%; width: 100%; background: var(--accent); transform-origin: left; transform: scaleX(0); }
.inside-foot { text-align: center; font-size: 11px; letter-spacing: .3em; text-transform: uppercase; color: rgba(239,237,230,.5); padding-top: 12px; }
/* mobile deck */
.inside-mobile { padding: var(--section-sm) 0 56px; }
.inside-mobile .mstage { position: relative; height: 46vw; display: grid; place-items: center; margin: 8px 0 20px; touch-action: pan-y; }
.inside-mobile .inside-pills { margin-top: 16px; }
.inside-mobile .inside-lead { margin-top: 12px; }
.inside-mobile .inside-halo { width: 60vw; height: 60vw; transform: scale(1.3); }
.inside-mobile .inside-float { width: 44vw; }
.deck { display: flex; gap: 5vw; overflow-x: auto; scroll-snap-type: x mandatory; padding: 8px 9vw 16px; scrollbar-width: none; }
.deck::-webkit-scrollbar { display: none; }
.deck-card { flex: 0 0 82vw; scroll-snap-align: center; }
.deck-card .inside-name { opacity: 0; }
.deck-card [data-deck-item] { opacity: 0; margin-top: 12px; }
.inside-mobile .mdots button { color: rgba(239,237,230,.35); }

/* ---- 04 story (pinned timeline) ---- */
.story { position: relative; background: var(--bone); color: var(--ink); }
.story-pin { position: relative; height: 100vh; overflow: hidden; }
.story-intro { position: absolute; inset: 0; z-index: 20; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0 var(--gutter); }
.story-intro .h1 { margin-top: 18px; max-width: 14ch; opacity: 0; }
.story-intro .lead { margin-top: 20px; max-width: 46ch; text-align: center; }
.story-stage { position: absolute; inset: 0; opacity: 0; }
.story-ghost { font-size: clamp(16rem, 60vh, 40rem); -webkit-text-stroke: 1px rgba(26,27,29,.12); left: 38%; }
.story-figure { position: absolute; inset: 0; display: flex; align-items: center; justify-content: flex-end; padding-right: clamp(48px, 9vw, 160px); pointer-events: none; }
.story-figure figure { width: min(34vw, 420px); }
.story-panel { position: absolute; left: var(--gutter); top: 50%; transform: translateY(-50%); width: min(40vw, 480px); }
.story-years { position: absolute; right: var(--gutter); top: 50%; transform: translateY(-50%); display: grid; gap: 12px; font-size: 12px; letter-spacing: .2em; padding-left: 14px; border-left: 1px solid var(--line); }
.story-years button { color: inherit; text-align: left; transition: color .3s ease; }
.story-progress { position: absolute; left: -1px; top: 0; width: 1px; height: 100%; background: var(--ink); transform-origin: top; transform: scaleY(0); }
/* mobile runway */
.story-mobile { position: relative; padding: var(--section-sm) 20px 0; }
.mstory { position: relative; height: 420svh; }
.mstory-sticky { position: sticky; top: var(--nav-h); height: calc(100svh - var(--nav-h)); display: flex; flex-direction: column; }
.mstory-stage { position: relative; height: 46svh; }
.mstory-stage .ghost { font-size: 44vw; left: 50%; top: 42%; }
.mstory-figure { position: absolute; left: 50%; top: 4%; width: 70vw; height: 88%; transform: translateX(-50%); overflow: hidden; background: rgba(26,27,29,.045); clip-path: inset(0 0 92% 0); opacity: .4; }
.mstory-figure img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.12); }
.mstory-text { flex: 1; padding-top: 18px; }
.mstory-years { display: flex; gap: 16px; font-size: 12px; letter-spacing: .2em; padding: 12px 0 20px; }
.mstory-years button { color: inherit; }

/* ---- 05 promise ---- */
.promise { background: var(--ink); color: var(--bone); padding: var(--section-sm) 0; overflow: hidden; }
.promise-title { font-family: var(--font-wordmark); font-weight: 800; font-size: clamp(2.2rem, 1.6rem + 3vw, 4.4rem); letter-spacing: -.02em; text-transform: uppercase; line-height: .95; margin-top: 14px; }
.pquotes { display: grid; gap: 32px; margin-top: 48px; }
@media (min-width: 768px) { .pquotes { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 40px; } }
.pquote blockquote { font-size: clamp(1.1rem, 1rem + .6vw, 1.5rem); line-height: 1.35; color: rgba(239,237,230,.92); }
.pquote figcaption { color: rgba(239,237,230,.5); }
.press-marquee { margin-top: 64px; border-top: 1px solid rgba(239,237,230,.15); border-bottom: 1px solid rgba(239,237,230,.15); padding: 24px 0; will-change: transform; }
.press-marquee .track > span { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.6rem, 1.2rem + 2vw, 3rem); color: var(--bone); }
.press-marquee .track .mq-dot { color: var(--accent); font-size: 1rem; }
.press-marquee .track .outline { color: transparent; -webkit-text-stroke: 1px rgba(239,237,230,.6); }
.press-marquee .row2 { margin-top: 12px; }

/* ---- 06 shop ---- */
.shop-sec { background: var(--bone); color: var(--ink); padding: clamp(32px, 5vw, 64px) 0 clamp(16px, 2vw, 24px); }
.coll-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 20px 32px; margin-bottom: clamp(20px, 3vw, 28px); }
.coll-tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.ctab { min-height: 38px; padding: 0 18px; border: 1px solid var(--line-strong); border-radius: 999px; background: #fff; font-size: .875rem; font-weight: 600; color: var(--ink); transition: background-color .3s ease, color .3s ease, border-color .3s ease, box-shadow .3s ease; box-shadow: 0 1px 2px rgba(26,27,29,.05); }
.ctab:hover { border-color: var(--accent-deep); }
.ctab[aria-selected="true"] { background: var(--accent-deep); color: var(--bone); border-color: var(--accent-deep); }
/* catalogue cards */
.cc-grid { display: grid; gap: 16px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
@media (min-width: 768px) { .cc-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; } }
@media (min-width: 1200px) { .cc-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; } }
.ccard { display: flex; flex-direction: column; background: #fff; border-radius: 16px; padding: 12px; box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 10px 30px -18px rgba(26,27,29,.18); transition: transform .4s var(--ease-out), box-shadow .4s ease; }
.ccard:hover { transform: translateY(-3px); box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 24px 40px -20px rgba(26,27,29,.28); }
.ccard.is-hidden { display: none; }
.cc-media { position: relative; display: grid; place-items: center; aspect-ratio: 1; border-radius: 12px; background: #F3F1EC; overflow: hidden; }
.cc-media img { position: relative; z-index: 1; width: 82%; height: auto; max-height: 86%; object-fit: contain; filter: drop-shadow(0 14px 18px rgba(26,27,29,.16)); transition: opacity .4s ease, transform .6s var(--ease-out); }
.cc-media img.alt { position: absolute; inset: 0; margin: auto; opacity: 0; }
.ccard.has-alt:hover .cc-media img.main { opacity: 0; }
.ccard.has-alt:hover .cc-media img.alt { opacity: 1; }
.cc-badges { position: absolute; left: 10px; top: 10px; z-index: 2; display: grid; gap: 6px; justify-items: start; }
.cc-badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 4px; font-size: .6875rem; font-weight: 600; line-height: 1; }
.cc-sale { background: #5A1E1A; color: var(--bone); }
.cc-best { background: #D9A866; color: #3A2410; }
.cc-new { background: var(--ink); color: var(--bone); }
.cc-body { padding: 14px 6px 6px; display: grid; gap: 6px; }
.cc-price { display: flex; align-items: baseline; gap: 8px; }
.cc-price b { font-weight: 700; font-size: 1.1rem; color: var(--accent-deep); }
.cc-price s { font-size: .75rem; color: var(--fg-2); }
.cc-name { font-size: 1rem; font-weight: 600; line-height: 1.3; }
.cc-name a { color: var(--ink); }
.cc-meta { font-size: .75rem; color: var(--fg-2); }
.cc-meta i { font-style: normal; margin: 0 4px; opacity: .6; }
.cc-opts { gap: 6px; }
.cc-sw { position: relative; width: 22px; height: 22px; border-radius: 50%; border: 1px solid transparent; display: grid; place-items: center; cursor: pointer; }
.cc-sw input { position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer; }
.cc-sw i { width: 14px; height: 14px; border-radius: 50%; background: var(--sw); box-shadow: inset 0 0 0 1px rgba(0,0,0,.18); }
.cc-sw:has(input:checked) { border-color: var(--ink); }
.cc-stock { display: inline-flex; align-items: center; gap: 6px; font-size: .75rem; font-weight: 500; color: #1F7A3A; }
.cc-stock i { width: 6px; height: 6px; border-radius: 50%; background: #1F7A3A; }
.cc-foot { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 8px; }
.cc-add { min-height: 40px; padding: 0 16px; border-radius: 999px; background: var(--accent-deep); color: var(--bone); font-size: .875rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; transition: background-color .3s ease, color .3s ease; }
.cc-add:hover { background: var(--ink); }
.cc-wish { width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--line-strong); display: grid; place-items: center; color: var(--fg-2); background: #fff; transition: color .3s ease, border-color .3s ease; }
.cc-wish svg { width: 16px; height: 16px; }
.cc-wish:hover { color: var(--ink); border-color: var(--ink); }
.cc-wish[aria-pressed="true"] { color: var(--accent-deep); border-color: var(--accent-deep); }
.cc-wish[aria-pressed="true"] svg { fill: currentColor; }
@media (max-width: 767px) { .ccard { padding: 8px; border-radius: 12px; } .cc-body { padding: 10px 4px 4px; } .cc-name { font-size: .875rem; } .cc-price b, .cc-price s, .cc-add { white-space: nowrap; } .cc-price b { font-size: 1rem; } .cc-add { padding: 0 10px; font-size: .75rem; min-height: 36px; } .cc-wish { width: 32px; height: 32px; flex: 0 0 auto; } }
.delivery { display: grid; gap: 28px; margin-top: var(--section-sm); padding-top: 40px; border-top: 1px solid var(--line); }
@media (min-width: 768px) { .delivery { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.delivery h3 { font-family: var(--font-display); font-weight: 300; font-size: 1.5rem; }
.delivery p { color: var(--fg-2); font-size: .9375rem; margin-top: 8px; max-width: 26ch; }
.or-row { display: flex; align-items: center; gap: 20px; margin-top: var(--section-sm); }
.or-row .shop-rule { flex: 1; height: 1px; background: var(--line-strong); }
.or-row .label { white-space: nowrap; }
'''

    belts = [p for p in P if p["line"] == "belt"]; wallets = [p for p in P if p["line"] == "wallet"]
    n_belts, n_wallets = len(belts), len(wallets); min_belt, min_wallet = min(p["price"] for p in belts), min(p["price"] for p in wallets)
    fmt = lambda n: "Rs " + format(n, ",d")
    hero_cut = cut("kingsmann")
    hero_belt = cut("monarch")
    def pair(w, bl, size="src", a=""):
        return (f'<div class="pair"><img class="p-belt" src="{bl[size]}" alt="" width="900" height="900" draggable="false" decoding="async">'
                f'<img class="p-wallet" src="{w[size]}" alt="{a}" width="900" height="900" draggable="false" decoding="async"></div>')
    body = f'''
<section id="hero" class="hero on-ink" aria-label="Introduction">
  <div class="slider" data-slider aria-roledescription="carousel" aria-label="Belts and wallets">
    <div class="slide is-on" data-slide="0" aria-roledescription="slide" aria-label="1 of 2">
      <picture><source media="(max-width: 767px)" srcset="assets/hero/slide-wallet-portrait.jpg"><img data-slide-img src="assets/hero/slide-wallet-1600.jpg" srcset="assets/hero/slide-wallet-900.jpg 900w, assets/hero/slide-wallet-1600.jpg 1600w, assets/hero/slide-wallet-2000.jpg 2000w" sizes="100vw" alt="A Stagr long wallet open beside its gift box and a tan belt" width="2000" height="1333" fetchpriority="high" decoding="async"></picture>
      <div class="wrap slide-copy">
        <p class="hero-kicker" data-slide-item>Wallets <span aria-hidden="true">·</span> {n_wallets} pieces, from {fmt(min_wallet)}</p>
        <h1 class="hero-h1" data-slide-item><span class="serif-i">Folded, skived,</span><br>stitched by hand.</h1>
        <p class="hero-sub" data-slide-item>Bifolds, trifolds and long wallets, boxed with a handwritten note. Cash on delivery across Pakistan.</p>
        <div class="hero-ctas" data-slide-item><a class="btn btn--tan" href="wallets.html">Shop wallets {I["arrow"]}</a><a class="btn btn--ghost" href="shop.html">Everything</a></div>
      </div>
    </div>
    <div class="slide" data-slide="1" aria-roledescription="slide" aria-label="2 of 2" aria-hidden="true">
      <picture><source media="(max-width: 767px)" srcset="assets/hero/slide-belts-portrait.jpg"><img data-slide-img src="assets/hero/slide-belts-1600.jpg" srcset="assets/hero/slide-belts-900.jpg 900w, assets/hero/slide-belts-1600.jpg 1600w, assets/hero/slide-belts-2400.jpg 2400w" sizes="100vw" alt="Four Stagr belts laid on a walnut bench" width="2400" height="1474" loading="lazy" decoding="async"></picture>
      <div class="wrap slide-copy">
        <p class="hero-kicker" data-slide-item>Belts <span aria-hidden="true">·</span> {n_belts} pieces, from {fmt(min_belt)}</p>
        <h2 class="hero-h1" data-slide-item><span class="serif-i">{B["hero"]["headline"][0]}</span><br>{B["hero"]["headline"][1]}</h2>
        <p class="hero-sub" data-slide-item>Full-grain crazy horse, cut in one piece, with a solid buckle on a screw post. Sizes 30 to 44.</p>
        <div class="hero-ctas" data-slide-item><a class="btn btn--tan" href="belts.html">Shop belts {I["arrow"]}</a><a class="btn btn--ghost" href="shop.html">Everything</a></div>
      </div>
    </div>
    <div class="wrap slider-ui">
      <div class="slider-dots" role="tablist" aria-label="Choose slide"><button type="button" role="tab" aria-selected="true" data-slide-dot="0" aria-label="Wallets"><i></i></button><button type="button" role="tab" aria-selected="false" data-slide-dot="1" aria-label="Belts"><i></i></button></div>
      <div class="slider-nav"><span class="slider-count"><b data-slide-n>01</b> / 02</span><button type="button" class="half-arrow" data-slide-prev aria-label="Previous slide" style="transform:scaleX(-1)">{I["arrow"]}</button><button type="button" class="half-arrow" data-slide-next aria-label="Next slide">{I["arrow"]}</button></div>
    </div>
  </div>
  <div class="bulk-band" data-bulk-band>
    <div class="wrap bulk-inner">
      <span class="bulk-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/></svg></span>
      <p class="bulk-text"><b>Buying for a team? Meet Stagr bulk orders.</b><span>Ten pieces or more, embossed with your logo, boxed with a handwritten card.</span></p>
      <a class="btn btn--sm bulk-btn" href="about.html#bulk">Get a quote {I["arrow"]}</a>
    </div>
  </div>
</section>

<section id="explore" class="explore on-bone" aria-labelledby="explore-title">
  <div class="wrap">
    <div class="explore-head">
      <div><h2 class="explore-title" id="explore-title" data-reveal>Explore pieces<br>by category</h2><p class="explore-sub" data-reveal data-delay=".1">Start with the right cut. Everything else follows.</p></div>
      <div class="explore-right" data-reveal data-delay=".15">
        <div class="explore-tabs" role="tablist" aria-label="Line"><button type="button" role="tab" aria-selected="true" data-ex-tab="wallet">Wallets</button><button type="button" role="tab" aria-selected="false" data-ex-tab="belt">Belts</button></div>
        <a class="explore-all" data-ex-all href="shop.html?line=wallets">View all pieces {I["arrow"]}</a>
      </div>
    </div>
    <div class="explore-grid" data-ex-grid="wallet" role="tabpanel">
      {"".join(f'<a class="ex-card" href="{h}"><span class="ex-media"><img src="assets/categories/{k}-500.jpg" srcset="assets/categories/{k}-500.jpg 500w, assets/categories/{k}.jpg 900w" sizes="(min-width: 1024px) 18vw, (min-width: 640px) 30vw, 46vw" alt="{alt}" width="900" height="600" loading="lazy"></span><b>{t}</b><span>{sub}</span></a>' for k, h, t, sub, alt in [
        ("all-wallets", "wallets.html", "All wallets", "Seven styles, two colours", "A Stagr bifold open beside the tools that made it"),
        ("bifold", "wallets.html#bifold", "Bifold wallets", "The everyday fold", "Two Regal bifolds on a sheepskin"),
        ("trifold", "wallets.html#trifold", "Trifold wallets", "Three folds, one hide", "A Majestic trifold open on its gift box"),
        ("minimalist", "wallets.html#minimalist", "Minimalist", "For a front pocket", "A Maverick card holder with a tan belt behind"),
        ("long", "wallets.html#long", "Long wallets", "Cards, notes, a snap", "A Rodeo long wallet open beside its box")]) }
    </div>
    <div class="explore-grid" data-ex-grid="belt" role="tabpanel" hidden>
      {"".join(f'<a class="ex-card" href="{h}"><span class="ex-media"><img src="assets/categories/{k}-500.jpg" srcset="assets/categories/{k}-500.jpg 500w, assets/categories/{k}.jpg 900w" sizes="(min-width: 1024px) 18vw, (min-width: 640px) 30vw, 46vw" alt="{alt}" width="900" height="600" loading="lazy"></span><b>{t}</b><span>{sub}</span></a>' for k, h, t, sub, alt in [
        ("all-belts", "belts.html", "All belts", "Classic and double-sided", "Four Stagr belts laid on walnut"),
        ("nova", "belts.html#nova", "Nova", "Two sides, one belt", "The Nova belt with its swivel buckle"),
        ("outlaw", "belts.html#outlaw", "Outlaw", "Rugged, brass buckle", "The Outlaw belt coiled among coffee beans"),
        ("regent", "belts.html#regent", "Regent", "Black, cut in one piece", "The Regent belt coiled on a walnut bench"),
        ("monarch", "belts.html#monarch", "Monarch", "Tan, deepens with wear", "The Monarch belt coiled among shells and coffee beans")]) }
    </div>
  </div>
</section>

<section id="shop" class="shop-sec on-bone" aria-labelledby="shop-title">
  <div class="wrap">
    <div class="coll-head">
      <div><h2 class="explore-title" id="shop-title" data-reveal>The collection</h2><p class="explore-sub" data-reveal data-delay=".1">Cash on delivery, 3 to 5 working days anywhere in Pakistan.</p></div>
      <div class="coll-tabs" role="tablist" aria-label="Filter the collection" data-reveal data-delay=".15">
        <button type="button" class="ctab" role="tab" aria-selected="true" data-tab="new">New in</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="best">Bestsellers</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="gift">Gifting</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="under">Under Rs 2,000</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="all">All</button>
      </div>
    </div>
    <div class="cc-grid" data-shop-grid>{cards}</div>
    <p class="small muted" style="margin-top:20px"><span data-shop-count></span> shown · <a class="link" href="shop.html">View all pieces</a></p>
</section>

<section id="inside" class="inside on-ink" aria-labelledby="inside-title">
  <div class="inside-pin desk-only" data-inside-pin>
    <div class="inside-head"><p class="label inside-kicker">Your hide. Our bench.</p><h2 class="inside-title" id="inside-title" data-inside-title>Two lines. One great finish.</h2><p class="inside-lead">Every piece is cut from full hides by local artisans and saddle stitched by hand. Pick the line, then the cut.</p><div class="inside-pills">{pills}</div></div>
    <div class="inside-grid">
      <div class="inside-left">{lefts}</div>
      <div class="inside-stage" data-inside-stage><div class="inside-halo" data-inside-halo></div><div class="inside-float" data-inside-float>{inside_stack("src")}</div></div>
      <div class="inside-right">{rights}</div>
    </div>
    <p class="inside-foot">One hide. One workshop. Nothing else.</p>
  </div>
  <div class="inside-mobile mob-only" data-inside-mobile>
    <div style="padding:0 20px;text-align:center"><p class="label inside-kicker" data-reveal>Your hide. Our bench.</p><h2 class="inside-title" data-inside-title-mobile style="opacity:1;margin-top:10px">Two lines. One<br>great finish.</h2><p class="inside-lead" data-reveal data-delay=".1">Every piece is cut from full hides by local artisans and saddle stitched by hand. Pick the line, then the cut.</p><div class="inside-pills" data-reveal data-delay=".15">{"".join(f'<button type="button" class="pill" data-mpill="{i}" aria-pressed="{str(i == 0).lower()}">{d["tab"]}</button>' for i, d in enumerate(inside))}</div></div>
    <div class="mstage"><div class="inside-halo" data-inside-halo-mobile></div><div class="inside-float" data-inside-float-mobile>{inside_stack("small")}</div></div>
    <div class="deck" data-deck-track>{deck}</div>
    <div class="mdots">{"".join(f'<button type="button" data-deck-dot="{i}" style="color:{"var(--bone)" if i == 0 else "rgba(239,237,230,.35)"}">0{i + 1}</button>' for i in range(N_INSIDE))}</div>
    <p class="inside-foot" style="padding:24px 20px 0">One hide. One workshop. Nothing else.</p>
  </div>
</section>

<section id="more" class="more on-bone" aria-label="How it is made, bulk orders and the handwritten note">
  <div class="wrap bento">
    <a class="tile tile-main" href="about.html#craft" data-reveal aria-label="How it is made">
      <img src="assets/lifestyle/kingsmen-02-800.jpg" srcset="assets/lifestyle/kingsmen-02-800.jpg 800w, assets/lifestyle/kingsmen-02.jpg 1200w" sizes="(min-width: 1024px) 56vw, 100vw" alt="Close-up of the saddle stitching on a Stagr bifold" width="1200" height="1500" loading="lazy" decoding="async">
      <div class="tile-copy">
        <span class="ltag"><i class="rivet"></i>How it is made</span>
        <h2 class="tile-h1"><span class="serif-i">Cut, skived,</span><br>stitched by hand.</h2>
        <p class="tile-sub">{B["craft"]["body"]}</p>
        <span class="btn btn--sm tile-btn">See the process {I["arrow"]}</span>
      </div>
    </a>
    <a class="tile tile-side tile-bulk" href="about.html#bulk" data-reveal data-delay=".1" aria-label="Bulk orders">
      <img src="assets/hero/tile-bulk-800.jpg" srcset="assets/hero/tile-bulk-800.jpg 800w, assets/hero/tile-bulk.jpg 1500w" sizes="(min-width: 1024px) 44vw, 100vw" alt="Eight Stagr wallets laid out in two rows for a team order" width="1500" height="1000" loading="lazy" decoding="async">
      <div class="tile-copy"><span class="ltag"><i class="rivet"></i>{B["gifting"]["eyebrow"]}</span><h2 class="tile-h2">Bulk orders<span class="dotc">.</span></h2><p class="tile-sub">{B["gifting"]["points"][0]["body"]} {B["gifting"]["points"][1]["body"]}</p><span class="tile-link">Get a quote {I["arrow"]}</span></div>
    </a>
    <a class="tile tile-side tile-note" href="about.html#faq" data-reveal data-delay=".2" aria-label="A handwritten note">
      <img src="assets/lifestyle/majestic-01-800.jpg" srcset="assets/lifestyle/majestic-01-800.jpg 800w, assets/lifestyle/majestic-01.jpg 1200w" sizes="(min-width: 1024px) 44vw, 100vw" alt="A Stagr trifold wallet open on its gift box" width="1200" height="1500" loading="lazy" decoding="async">
      <div class="tile-copy"><span class="ltag"><i class="rivet"></i>{B["handwrittenNote"]["eyebrow"]}</span><h2 class="tile-h2">A handwritten note<span class="dotc">.</span></h2><p class="tile-sub">{B["handwrittenNote"]["body"]}</p><span class="tile-link">Add one at checkout {I["arrow"]}</span></div>
    </a>
  </div>
</section>

<!-- range section hidden for now --><section id="promise" class="promise on-ink" aria-labelledby="promise-title">
  <div class="wrap">
    <div data-reveal><p class="label"><b style="color:var(--bone)">05</b><span class="slash">/</span>{B["about"]["valuesTitle"]}</p></div>
    <h2 class="promise-title" id="promise-title" data-text-reveal="lines">Quietly made.</h2>
    <div class="pquotes">{quotes}</div>
  </div>
  <div class="press-marquee" data-press-marquee aria-hidden="true">
    <div class="marquee"><div class="track" data-press-row="solid">{mq_solid}</div></div>
    <div class="marquee row2"><div class="track" data-press-row="outline">{mq_outline}</div></div>
  </div>
</section>

<section id="story" class="story on-bone" aria-labelledby="story-title">
  <div class="story-pin desk-only" data-story-pin>
    <div class="story-intro" data-story-intro><p class="label"><b>06</b><span class="slash">/</span>Story</p><h2 class="h1" id="story-title" data-story-title>{B["about"]["headline"]}.</h2><p class="lead">{B["about"]["intro"]} {B["about"]["sections"][2]["body"].split(".")[0]}.</p><div class="scroll-hint" style="margin-top:36px" aria-hidden="true"><span class="t">Scroll</span></div></div>
    <div class="story-stage" data-story-stage>{ghosts}{figures}{spanels}<div class="story-years"><div class="story-progress" data-story-progress></div>{years}</div></div>
  </div>
  <div class="story-mobile mob-only">
    <div data-reveal><p class="label"><b>06</b><span class="slash">/</span>Story</p></div>
    <h2 class="h1" data-text-reveal="lines" style="margin-top:12px">{B["about"]["headline"]}.</h2>
    <p class="lead" data-illuminate style="margin-top:16px">{B["about"]["intro"]}</p>
    <div class="mstory" data-mstory>
      <div class="mstory-sticky">
        <div class="mstory-stage">{mstory_ghosts}{mstory_figs}</div>
        <div class="mstory-text">{mstory_panels}</div>
        <div class="mstory-years">{myears}</div>
      </div>
    </div>
  </div>
</section>

<section id="delivery-sec" class="on-bone" aria-label="How it reaches you" style="padding-bottom:var(--section-sm)"><div class="wrap"><div class="or-row" id="delivery"><span class="shop-rule" data-shop-rule style="transform-origin:right"></span><span class="label">How it reaches you</span><span class="shop-rule" data-shop-rule style="transform-origin:left"></span></div>
    <div class="delivery">{"".join(f'<div data-reveal data-delay="{i * .1}"><h3>{t["title"]}</h3><p>{t["sub"]}</p></div>' for i, t in enumerate(trust))}</div>
  </div>
</div></section>
'''

    js = r'''
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, clamp = S.clamp;
  const isMobile = S.isMobile, reduced = S.reduced, fine = S.fine, isRendered = S.isRendered;
  if (!G) return;

  /* ================= 01 HERO ================= */
  function initScrollHint() { const dot = $("[data-scroll-dot]"); if (!dot || !isRendered(dot)) return; if (reduced) { G.set(dot, { opacity: 1, y: 9 }); return; } G.timeline({ repeat: -1, repeatDelay: .5 }).set(dot, { y: 0, opacity: 0 }).to(dot, { opacity: 1, duration: .25 }).to(dot, { y: 19, duration: 1, ease: "power2.inOut" }, .1).to(dot, { opacity: 0, duration: .3, ease: "power1.in" }, .85); }

  function initHero() {
    const root = $("[data-slider]"), slides = $$("[data-slide]", root), dots = $$("[data-slide-dot]", root), count = $("[data-slide-n]", root), band = $("[data-bulk-band]");
    const n = slides.length, HOLD = 6.5; let active = 0, busy = false, timer = null, started = false;
    const items = (i) => $$("[data-slide-item]", slides[i]), img = (i) => $("[data-slide-img]", slides[i]);
    const pad = (i) => String(i + 1).padStart(2, "0");
    const paintDots = () => dots.forEach((d, i) => d.setAttribute("aria-selected", String(i === active)));
    // the active dot fills up over the hold, then we move on
    const arm = () => { clearTimeout(timer); dots.forEach((d) => $("i", d).style.setProperty("--p", 0)); if (reduced || document.hidden) return; const bar = $("i", dots[active]); G.fromTo(bar, { "--p": 0 }, { "--p": 1, duration: HOLD, ease: "none", overwrite: true }); timer = setTimeout(() => go(active + 1), HOLD * 1000); };
    const enter = (i, delay) => { if (reduced) { G.set(items(i), { opacity: 1, y: 0 }); return; } G.fromTo(img(i), { scale: 1.12 }, { scale: 1.04, duration: 2.6, ease: "power2.out", overwrite: true, delay }); G.fromTo(items(i), { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: .7, ease: "power3.out", stagger: .08, delay: delay + .25, overwrite: true, clearProps: "transform" }); };
    const go = (next, user) => {
      next = (next + n) % n; if (next === active || busy) return; busy = true;
      const from = slides[active], to = slides[next]; active = next; paintDots(); if (count) count.textContent = pad(next);
      to.classList.add("is-on"); to.setAttribute("aria-hidden", "false"); from.setAttribute("aria-hidden", "true");
      if (reduced) { from.classList.remove("is-on"); G.set(items(next), { opacity: 1 }); busy = false; arm(); return; }
      G.set(to, { zIndex: 2 }); G.set(from, { zIndex: 1 });
      G.fromTo(to, { opacity: 0 }, { opacity: 1, duration: 1, ease: "power2.inOut", onComplete: () => { from.classList.remove("is-on"); G.set([from, to], { clearProps: "zIndex,opacity" }); busy = false; } });
      G.to($$("[data-slide-item]", from), { opacity: 0, y: -10, duration: .35, ease: "power2.in", overwrite: true });
      enter(next, 0); arm();
    };
    dots.forEach((d, i) => d.addEventListener("click", () => go(i, true)));
    $("[data-slide-prev]", root).addEventListener("click", () => go(active - 1, true));
    $("[data-slide-next]", root).addEventListener("click", () => go(active + 1, true));
    root.addEventListener("keydown", (e) => { if (e.key === "ArrowRight") go(active + 1, true); if (e.key === "ArrowLeft") go(active - 1, true); });
    root.addEventListener("pointerenter", () => clearTimeout(timer)); root.addEventListener("pointerleave", () => { if (started) arm(); });
    document.addEventListener("visibilitychange", () => { if (!started) return; if (document.hidden) clearTimeout(timer); else arm(); });
    // swipe
    let sx = 0, sy = 0; root.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    root.addEventListener("touchend", (e) => { const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) go(active + (dx < 0 ? 1 : -1), true); }, { passive: true });
    if (!reduced) { G.set(items(0), { opacity: 0 }); if (band) G.set(band, { y: 24, opacity: 0 }); }
    return function start() { started = true; enter(0, 0); if (band && !reduced) G.to(band, { y: 0, opacity: 1, duration: .6, ease: "power3.out", delay: .6, clearProps: "transform" }); arm(); };
  }

  /* ================= 02 RANGE ================= */
  function initRangeDesktop() {
    const section = $("#range"); if (!section) return; const pin = $("[data-range-pin]"), title = $("[data-range-title-main]"), label = $("[data-range-label]"), count = $("[data-range-count]"), panels = $$("[data-range-panel]"), bgs = $$("[data-range-bloom]"), ghosts = $$("[data-range-ghost]"), cuts = $$("[data-range-cut]"), stage = $("[data-range-stage]"), dots = $$("[data-range-dot]");
    const n = panels.length, SIDE = [1, -1, 1, -1, 1], unit = () => stage.clientHeight / 3.509, deg = (r) => r * 180 / Math.PI;
    cuts.forEach((c, i) => G.set(c, i === 0 ? { x: 0, scale: 1, opacity: 1 } : { x: () => 3 * SIDE[i] * unit(), scale: .94, opacity: 0 }));
    G.fromTo(label, { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: .6, ease: "power2.out", scrollTrigger: { trigger: section, start: "top 80%", toggleActions: "play none none none" } });
    S.charRise(title, { to: { duration: .8, stagger: .022, scrollTrigger: { trigger: section, start: "top 80%", once: true } } }); G.set(title, { opacity: 1 });
    G.fromTo([panels[0].parentElement, stage], { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: "power2.out", stagger: .12, scrollTrigger: { trigger: section, start: "top 55%", once: true } });
    let active = 0, shown = 0, swapping = false, nameSplit = null;
    const showPanel = (panel) => { G.fromTo(panel, { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power3.out" }); G.fromTo($$("[data-stage-item]", panel), { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power2.out", stagger: .05, delay: .05 }); if (nameSplit) nameSplit.revert(); nameSplit = S.charRise($("[data-range-title]", panel), { from: 108, to: { duration: .55, stagger: .025, overwrite: "auto" } }); };
    const swapText = () => { if (shown === active || swapping) return; swapping = true; G.to(panels[shown], { y: -26, opacity: 0, duration: .25, ease: "power3.in", onComplete: () => { panels[shown].hidden = true; shown = active; panels[shown].hidden = false; showPanel(panels[shown]); swapping = false; swapText(); } }); };
    const setActive = (next) => {
      if (next === active) return; const fwd = next > active; active = next; const side = SIDE[next], u = unit();
      cuts.forEach((c, i) => { if (i === next) G.fromTo(c, { x: 3 * side * u, y: -.12 * u, rotation: deg(.16 * side), scale: .94, opacity: 0 }, { x: 0, y: 0, rotation: 0, scale: 1, opacity: 1, duration: .85, ease: "power2.out", delay: .1, overwrite: "auto" }); else G.to(c, { x: -2.2 * side * u, y: .1 * u, rotation: deg(-.14 * side), scale: .94, opacity: 0, duration: .45, ease: "power2.in", overwrite: "auto" }); });
      bgs.forEach((el, i) => G.to(el, { opacity: i === next ? 1 : 0, duration: .8, ease: "power2.inOut", overwrite: "auto" }));
      ghosts.forEach((el, i) => G.to(el, { opacity: i === next ? 1 : 0, y: i === next ? 0 : fwd ? -40 : 40, duration: .8, ease: "power2.inOut", overwrite: "auto" }));
      count.textContent = (next + 1) + " / " + n; dots.forEach((d, i) => d.style.color = i === next ? "var(--fg)" : "var(--fg-2)"); swapText();
    };
    const trigger = ST.create({ trigger: pin, start: "top top", end: () => "+=" + (n * innerHeight), pin: true, pinSpacing: true, scrub: 1, snap: { snapTo: Array.from({ length: n }, (_, i) => i / (n - 1)), duration: { min: .25, max: .55 }, ease: "power2.inOut", directional: false, delay: .1 }, invalidateOnRefresh: true, refreshPriority: 1,
      onUpdate: (self) => { const p = self.progress; const step = 1 / (n - 1); let next = active; while (next < n - 1 && p > (next + .5) * step + .04) next++; while (next > 0 && p < (next - .5) * step - .04) next--; setActive(next); } });
    dots.forEach((d, i) => d.addEventListener("click", () => S.scrollToProgress(trigger, i / (n - 1), 1)));
    ST.create({ trigger: section, start: "top 60%", once: true, onEnter: () => { nameSplit = S.charRise($("[data-range-title]", panels[0]), { from: 108, to: { duration: .7, stagger: .03 } }); } });
  }
  function initRangeMobile() {
    const track = $("[data-mrange-track]"); if (!track) return;
    const dots = $$("[data-mrange-dot]"), titles = $$("[data-mcard-title]", track); let split = null, started = false;
    const reveal = (i) => { const t = titles[i], items = $$("[data-card-item]", t.closest("article")); if (reduced) { G.set([t, ...items], { opacity: 1 }); return; } if (split) split.revert(); split = window.SplitText.create(t, { type: "words,chars", mask: "words", onSplit: (self) => { G.set(t, { opacity: 1 }); return G.fromTo(self.chars, { yPercent: 108 }, { yPercent: 0, duration: .55, ease: "power2.out", stagger: .03, overwrite: "auto" }); } }); G.fromTo(items, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .45, ease: "power2.out", stagger: .05, delay: .1, overwrite: "auto" }); };
    ST.create({ trigger: track, start: "top 85%", once: true, onEnter: () => { if (started) return; started = true; reveal(0); } });
    S.watchCarousel(track, (next, prev) => { started = true; dots.forEach((d, i) => d.style.color = i === next ? "var(--fg)" : "var(--fg-2)"); const old = titles[prev]; G.to([old, ...$$("[data-card-item]", old.closest("article"))], { opacity: 0, duration: .12, overwrite: "auto" }); reveal(next); });
    dots.forEach((d, i) => d.addEventListener("click", () => S.scrollCarouselTo(track, i)));
  }

  /* ================= 03 INSIDE ================= */
  function turnPiece(float, next) { const imgs = $$("[data-inside-img]", float); const show = () => imgs.forEach((im, i) => im.style.opacity = i === next ? 1 : 0); if (reduced) { show(); return; } G.timeline({ overwrite: true }).to(float, { scaleX: .8, rotation: -3, duration: .22, ease: "power2.in", onComplete: show }).to(float, { scaleX: 1, rotation: 0, duration: .6, ease: "power3.out" }); }
  function initInside() {
    const section = $("#inside"); if (!section) return;
    const colors = $$("[data-deck-track] article").map((el) => el.dataset.halo);
    if (isMobile) {
      const title = $("[data-inside-title-mobile]"); G.fromTo(title, { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .9, ease: "power2.out", scrollTrigger: { trigger: section, start: "top 75%", once: true } });
      const halo = $("[data-inside-halo-mobile]"), img = $("[data-inside-float-mobile]"), track = $("[data-deck-track]"), dots = $$("[data-deck-dot]"), titles = $$("[data-deck-title]", track); let split = null, pending = true;
      const reveal = (i) => { const t = titles[i], items = $$("[data-deck-item]", t.closest("article")); if (reduced) { G.set([t, ...items], { opacity: 1 }); return; } if (split) split.revert(); split = window.SplitText.create(t, { type: "words,chars", mask: "words", onSplit: (self) => { G.set(t, { opacity: 1 }); return G.fromTo(self.chars, { yPercent: 108 }, { yPercent: 0, duration: .5, ease: "power2.out", stagger: .02, overwrite: "auto" }); } }); G.fromTo(items, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .5, ease: "power2.out", stagger: .07, delay: .08, overwrite: "auto" }); };
      ST.create({ trigger: track, start: "top 85%", once: true, onEnter: () => { if (!pending) return; pending = false; reveal(0); } });
      S.watchCarousel(track, (next, prev) => { pending = false; dots.forEach((d, i) => d.style.color = i === next ? "var(--bone)" : "rgba(239,237,230,.35)"); G.to(halo, { backgroundColor: colors[next], duration: .5, overwrite: "auto" }); turnPiece(img, next); const old = titles[prev]; G.to([old, ...$$("[data-deck-item]", old.closest("article"))], { opacity: 0, duration: .12, overwrite: "auto" }); reveal(next); });
      dots.forEach((d, i) => d.addEventListener("click", () => S.scrollCarouselTo(track, i)));
      // tabs above the stage, and a swipe on the picture itself, both drive the deck
      const mpills = $$("[data-mpill]"); let cur = 0;
      const paintPills = (i) => mpills.forEach((p, k) => p.setAttribute("aria-pressed", String(k === i)));
      mpills.forEach((p, i) => p.addEventListener("click", () => S.scrollCarouselTo(track, i)));
      S.watchCarousel(track, (next) => { cur = next; paintPills(next); });
      const stage = $(".inside-mobile .mstage"); let sx = 0, sy = 0;
      stage.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
      stage.addEventListener("touchend", (e) => { const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.4) S.scrollCarouselTo(track, Math.max(0, Math.min(titles.length - 1, cur + (dx < 0 ? 1 : -1)))); }, { passive: true });
      return;
    }
    const title = $("[data-inside-title]"), halo = $("[data-inside-halo]"), img = $("[data-inside-float]"), pills = $$("[data-inside-pill]"), lefts = $$("[data-inside-left]"), rights = $$("[data-inside-right]");
    window.SplitText.create(title, { type: "chars", onSplit: (self) => G.fromTo(self.chars, { yPercent: 22, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .8, ease: "power2.out", stagger: .022, scrollTrigger: { trigger: section, start: "top 75%", once: true } }) }); G.set(title, { opacity: 1 });
    let active = 0, shown = 0, swapping = false, nameSplit = null;
    const parts = (i) => [$("[data-inside-name]", lefts[i]), $("[data-inside-sci]", lefts[i]), rights[i]];
    const stylePills = () => pills.forEach((p, i) => p.setAttribute("aria-pressed", String(i === active)));
    const show = (i) => {
      const [name, , right] = parts(i);
      G.fromTo(parts(i), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: .45, delay: .1, ease: "power3.out", stagger: .05, overwrite: "auto" });
      if (nameSplit) nameSplit.revert(); nameSplit = null;
      if (!reduced) nameSplit = window.SplitText.create(name, { type: "chars", onSplit: (self) => G.fromTo(self.chars, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .55, ease: "power2.out", stagger: .028, delay: .12, overwrite: "auto" }) });
      G.fromTo(halo, { scale: 1.45 }, { scale: 1.6, duration: .9, ease: "power2.out", overwrite: "auto" });
      if (window.DrawSVGPlugin) G.fromTo($$("[data-bot]", lefts[i]), { drawSVG: "0%" }, { drawSVG: "100%", duration: .9, ease: "power1.inOut", stagger: .08, delay: .15, overwrite: "auto" });
      const bar = $("[data-inside-bar]", right), dose = $("[data-inside-dose]", right);
      G.fromTo(bar, { scaleX: 0 }, { scaleX: parseFloat(bar.dataset.insideBar), duration: .8, delay: .25, ease: "power2.inOut", overwrite: "auto" });
      const c = { v: 0 }; G.to(c, { v: parseFloat(dose.dataset.insideDose), duration: .8, delay: .25, ease: "power2.out", onUpdate: () => dose.textContent = String(Math.round(c.v)) });
    };
    const swap = () => { if (shown === active || swapping) return; swapping = true; G.to(parts(shown), { opacity: 0, y: -26, duration: .22, ease: "power3.in", overwrite: "auto", onComplete: () => { lefts[shown].hidden = true; rights[shown].hidden = true; shown = active; lefts[shown].hidden = false; rights[shown].hidden = false; show(shown); swapping = false; swap(); } }); };
    const setActive = (next) => { if (next === active) return; active = next; stylePills(); G.to(halo, { backgroundColor: colors[next], duration: .5, overwrite: "auto" }); turnPiece(img, next); swap(); };
    // 4 topics sit at progress 0, 1/3, 2/3, 1 (the snap points); the active one only changes once
    // the scroll has moved clearly past the midpoint between two topics, so nothing flips on its own
    const STEPS = lefts.length - 1; let scrolling = null;
    const pick = (progress) => { const p = progress * STEPS; let next = active; while (next < STEPS && p > next + .5 + .1) next++; while (next > 0 && p < next - .5 - .1) next--; return next; };
    const trigger = ST.create({ trigger: section, start: "top top", end: () => "+=" + STEPS * innerHeight, pin: true, pinSpacing: true, scrub: .6, snap: { snapTo: (v) => scrolling !== null ? v : G.utils.snap(1 / STEPS, v), duration: { min: .25, max: .6 }, ease: "power2.inOut", directional: false, delay: .15, inertia: false }, invalidateOnRefresh: true, onUpdate: (self) => { if (scrolling !== null) return; setActive(pick(self.progress)); } });
    // a tab click switches straight away and glides the page to that topic's stop
    pills.forEach((p, i) => p.addEventListener("click", () => {
      if (i === active) return; scrolling = i; setActive(i);
      const y = trigger.start + (trigger.end - trigger.start) * i / STEPS, done = () => { scrolling = null; };
      clearTimeout(pills._t);
      if (S.lenis) S.lenis.scrollTo(y, { duration: .9, lock: true, force: true, onComplete: done }); else { window.scrollTo({ top: y, behavior: "smooth" }); }
      pills._t = setTimeout(done, 1400);   // safety net if the glide is interrupted
    }));
    G.set(parts(0), { opacity: 0 }); ST.create({ trigger: section, start: "top 60%", once: true, onEnter: () => show(0) });
    lefts.forEach((left) => { const hover = $("[data-inside-hover]", left); hover.addEventListener("pointerenter", () => { G.to(halo, { opacity: .7, scale: 1.75, duration: .6, overwrite: "auto" }); if (window.DrawSVGPlugin) G.fromTo($$("[data-bot]", left), { drawSVG: "0%" }, { drawSVG: "100%", duration: .7, ease: "power1.inOut", stagger: .06, overwrite: "auto" }); }); hover.addEventListener("pointerleave", () => G.to(halo, { opacity: .5, scale: 1.6, duration: .7, overwrite: "auto" })); if (!reduced) G.fromTo($("[data-inside-svg]", left), { rotation: -3.5, transformOrigin: "50% 50%" }, { rotation: 3.5, duration: 5, yoyo: true, repeat: -1, ease: "sine.inOut" }); });
    if (fine && !reduced) { const wrap = $("[data-inside-float]"); const sx = G.quickTo(wrap, "x", { duration: .9, ease: "power2.out" }), sy = G.quickTo(wrap, "y", { duration: .9, ease: "power2.out" }); section.addEventListener("pointermove", (e) => { sx((e.clientX / innerWidth - .5) * 22); sy((e.clientY / innerHeight - .5) * 12); }, { passive: true }); }
  }

  /* ================= 04 STORY ================= */
  function initStoryDesktop() {
    const pin = $("[data-story-pin]"), intro = $("[data-story-intro]"), stage = $("[data-story-stage]"), title = $("[data-story-title]"), ghosts = $$("[data-story-ghost]"), figures = $$("[data-story-figure]"), panels = $$("[data-story-panel]"), bar = $("[data-story-progress]"), years = $$("[data-story-year]");
    const total = panels.length, step = 1 / (total - 1); let active = 0, shown = 0, swapping = false;
    S.charRise(title, { to: { duration: .8, stagger: .016, scrollTrigger: { trigger: pin, start: "top 75%", once: true } } }); G.set(title, { opacity: 1 });
    const showPanel = (panel) => { G.fromTo(panel, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power3.out", overwrite: "auto" }); G.fromTo($$("[data-story-item]", panel), { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power2.out", stagger: .05, delay: .05, overwrite: "auto" }); };
    const swap = () => { if (shown === active || swapping) return; swapping = true; G.to(panels[shown], { y: -24, opacity: 0, duration: .22, ease: "power3.in", overwrite: "auto", onComplete: () => { panels[shown].hidden = true; shown = active; panels[shown].hidden = false; showPanel(panels[shown]); swapping = false; swap(); } }); };
    const setActive = (next) => { if (next === active) return; const fwd = next > active; active = next; figures.forEach((f, i) => { if (i === next) G.fromTo(f, { scale: fwd ? .86 : 1.14, opacity: 0, y: fwd ? 46 : -46 }, { scale: 1, opacity: 1, y: 0, duration: .9, ease: "power2.out", delay: .08, overwrite: "auto", force3D: true }); else G.to(f, { scale: i < next ? 1.14 : .86, opacity: 0, y: i < next ? -46 : 46, duration: .6, ease: "power2.in", overwrite: "auto", force3D: true }); }); ghosts.forEach((g, i) => G.to(g, { opacity: i === next ? 1 : 0, y: i === next ? 0 : fwd ? -60 : 60, duration: .9, ease: "power2.inOut", overwrite: "auto", force3D: true })); years.forEach((y, i) => y.style.color = i === next ? "var(--fg)" : "var(--fg-2)"); swap(); };
    const stops = panels.map((_, i) => .1 + i / (total - 1) * .9);
    const trigger = ST.create({ trigger: pin, start: "top top", end: () => "+=" + innerHeight * (total - .4), pin: true, pinSpacing: true, scrub: 1, snap: { snapTo: [0, ...stops], duration: { min: .25, max: .55 }, ease: "power2.inOut" }, invalidateOnRefresh: true,
      onUpdate: (self) => { const p = self.progress, out = clamp(p / .08, 0, 1); intro.style.opacity = String(1 - out); intro.style.transform = "translateY(" + -40 * out + "px)"; stage.style.opacity = String(clamp((p - .04) / .08, 0, 1)); const travel = clamp((p - .1) / .9, 0, 1); bar.style.transform = "scaleY(" + travel + ")"; let next = active; while (next < total - 1 && travel > (next + .5) * step + .05) next++; while (next > 0 && travel < (next - .5) * step - .05) next--; setActive(next); } });
    years.forEach((y, i) => y.addEventListener("click", () => S.scrollToProgress(trigger, stops[i], 1.2)));
  }
  function initStoryMobile() {
    const runway = $("[data-mstory]"); if (!runway) return;
    const ghosts = $$("[data-mstory-ghost]"), figures = $$("[data-mstory-figure]"), panels = $$("[data-mstory-panel]"), years = $$("[data-mstory-year]");
    let active = 0, within = 0, words = [], wordSplit = null, titleSplit = null;
    const paint = () => { const f = figures[active], open = Math.min(1, within / .42); f.style.clipPath = "inset(0% 0% " + (1 - open) * 92 + "% 0%)"; f.style.opacity = String(.4 + .6 * open); $("img", f).style.transform = "scale(" + (1.12 - .12 * Math.min(1, within / .55)) + ")"; const lit = clamp((within - .3) / .55, 0, 1); words.forEach((wd, i) => wd.style.opacity = String(clamp(lit * (words.length + 3) - i, .24, 1))); };
    const prepare = (i) => { const t = $("[data-mstory-title]", panels[i]), x = $("[data-mstory-text]", panels[i]); G.set([t, x], { opacity: 1, y: 0 }); if (wordSplit) wordSplit.revert(); wordSplit = window.SplitText.create(x, { type: "words", aria: "none" }); words = wordSplit.words || []; words.forEach((wd) => wd.style.opacity = ".24"); if (!reduced) { if (titleSplit) titleSplit.revert(); titleSplit = S.charRise(t, { from: 105, to: { duration: .5, stagger: .013, overwrite: "auto" } }); } paint(); };
    const setActive = (next) => { if (next === active) return; const prev = active, dir = next > prev ? 1 : -1; active = next; ghosts.forEach((g, i) => { if (i === next) G.fromTo(g, { opacity: 0, yPercent: 7 * dir }, { opacity: 1, yPercent: 0, duration: .6, overwrite: "auto" }); else G.to(g, { opacity: 0, duration: .4, overwrite: "auto" }); }); figures.forEach((f, i) => { if (i !== next) G.to(f, { opacity: 0, duration: .3, overwrite: "auto" }); }); years.forEach((y, i) => y.style.color = i === next ? "var(--fg)" : "var(--fg-2)"); const leaving = panels[prev]; G.to([$("[data-mstory-title]", leaving), $("[data-mstory-text]", leaving)], { opacity: 0, y: -12, duration: .16, overwrite: "auto", onComplete: () => { panels.forEach((p, i) => p.hidden = i !== active); prepare(active); } }); };
    const trigger = ST.create({ trigger: runway, start: "top top", end: "bottom bottom", onUpdate: (self) => { const next = Math.min(panels.length - 1, Math.floor(panels.length * self.progress)); within = clamp(panels.length * self.progress - next, 0, 1); setActive(next); paint(); } });
    prepare(0);
    years.forEach((y, i) => y.addEventListener("click", () => S.scrollToProgress(trigger, (i + .72) / panels.length, .9)));
  }

  /* ================= 05 PROMISE ================= */
  function initPromise() {
    const section = $("#promise"); if (!section) return;
    const marquee = $("[data-press-marquee]"), solid = $('[data-press-row="solid"]'), outline = $('[data-press-row="outline"]');
    $$("[data-press-quote]").forEach((fig, i) => { const q = $("[data-quote-visual]", fig), cap = $("figcaption", fig); if (!reduced) window.SplitText.create(q, { type: "lines", mask: "lines", autoSplit: true, aria: "none", onSplit: (self) => G.fromTo(self.lines, { yPercent: 115 }, { yPercent: 0, duration: .85, ease: "power2.out", stagger: .09, delay: .12 * i, scrollTrigger: { trigger: fig, start: "top 85%", once: true } }) }); G.fromTo(cap, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .6, delay: .45 + .12 * i, scrollTrigger: { trigger: fig, start: "top 85%", once: true } }); });
    if (reduced) return;
    const rows = [G.to(solid, { xPercent: -50, duration: 38, ease: "none", repeat: -1 }), G.fromTo(outline, { xPercent: -50 }, { xPercent: 0, duration: 52, ease: "none", repeat: -1 })];
    const state = { skew: 0 }, setSkew = G.quickSetter(marquee, "skewX", "deg"), limit = G.utils.clamp(-6, 6);
    ST.create({ trigger: section, start: "top bottom", end: "bottom top", onUpdate: (self) => { const v = self.getVelocity(), skew = limit(-(v / 420)); if (Math.abs(skew) > Math.abs(state.skew)) { state.skew = skew; G.to(state, { skew: 0, duration: .9, ease: "power2.out", overwrite: true, onUpdate: () => setSkew(state.skew) }); } const speed = G.utils.clamp(1, 4, 1 + Math.abs(v) / 1200); rows.forEach((r) => { G.to(r, { timeScale: speed, duration: .4, overwrite: "auto" }); G.to(r, { timeScale: 1, duration: 1.4, delay: .4, ease: "power2.out", overwrite: false }); }); } });
  }

  /* ================= 06 SHOP ================= */
  function initShop() {
    const section = $("#shop"); if (!section) return;
    G.fromTo($$("[data-shop-rule]"), { scaleX: 0 }, { scaleX: 1, duration: .6, ease: "power3.out", scrollTrigger: { trigger: "[data-shop-rule]", start: "top 88%", toggleActions: "play none none none" } });
    const grid = $("[data-shop-grid]"), cards = $$("[data-product]", grid), tabs = $$(".ctab"), countEl = $("[data-shop-count]");
    const filter = (tab) => { let n = 0; cards.forEach((c) => { const ok = tab === "all" || c.dataset.tags.split(" ").indexOf(tab) >= 0; c.classList.toggle("is-hidden", !ok); if (ok) n++; }); if (countEl) countEl.textContent = n + (n === 1 ? " piece" : " pieces"); };
    let current = "new";
    tabs.forEach((t) => t.addEventListener("click", () => { if (t.dataset.tab === current) return; current = t.dataset.tab; tabs.forEach((x) => x.setAttribute("aria-selected", String(x === t))); S.swapGrid(grid, () => filter(current)); }));
    filter("new");
    S.initCards(section);
  }

  /* ================= boot (top to bottom so pinned blocks measure in order) ================= */
  const startHero = initHero();
  initScrollHint(); S.initReveals($("#hero")); S.initReveals($("#explore")); initShop(); S.initReveals($("#shop")); initInside(); S.initReveals($("#inside")); S.initReveals($("#more"));
  (function initExplore() {
    const tabs = $$("[data-ex-tab]"), grids = $$("[data-ex-grid]"), all = $("[data-ex-all]"); if (!tabs.length) return;
    tabs.forEach((t) => t.addEventListener("click", () => {
      const key = t.dataset.exTab; if (t.getAttribute("aria-selected") === "true") return;
      tabs.forEach((x) => x.setAttribute("aria-selected", String(x === t)));
      if (all) all.href = "shop.html?line=" + key + "s";
      const show = grids.find((g) => g.dataset.exGrid === key), hide = grids.find((g) => !g.hidden);
      const swap = () => { hide.hidden = true; show.hidden = false; if (reduced) return; G.fromTo($$(".ex-card", show), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .45, ease: "power3.out", stagger: .05, clearProps: "opacity,transform" }); ST.refresh(); };
      if (reduced || !hide) swap(); else G.to($$(".ex-card", hide), { opacity: 0, y: -8, duration: .2, ease: "power2.in", stagger: .02, overwrite: true, onComplete: () => { G.set($$(".ex-card", hide), { clearProps: "opacity,transform" }); swap(); } });
    }));
  })();
  if (isMobile) initRangeMobile(); else initRangeDesktop();
  initPromise(); S.initReveals($("#promise"));
  if (isMobile) initStoryMobile(); else initStoryDesktop();
  S.initReveals($("#story")); S.initReveals($("#delivery-sec")); S.initReveals($("footer"));
  S.onLoaderDone.push(() => { startHero(); ST.refresh(); });
}
STAGR.onReady.push(initAnimations);
'''

    return {
        "file": "index.html",
        "key": "index",
        "title": "STAGR. Carried daily. Made slowly.",
        "description": B["descriptor"] + " " + B["origin"] + ". Cash on delivery across Pakistan.",
        "css": css,
        "body": body,
        "js": js,
        "loader": True,
        "header_dark": True,
        "nav": [("Range", "#range"), ("Inside", "#inside"), ("Story", "#story"), ("Shop", "#shop")],
        "shop_href": "#shop",
    }
