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
        dict(name="Crazy<br>horse", sub="Full grain cowhide, hot waxed", desc=B["faqs"][0]["a"], rows=[("Source", "Full grain cowhide"), ("Finish", "Wax, hand rubbed"), ("Ages", "Darkens with use")], n=100, unit="% of every piece", bar=1.0,
             svg='<path data-bot d="M12 28c-6-6-4-16 4-20s16-2 20 4 6 14-2 18-16 4-22-2z"/><path data-bot d="M16 22c4-2 8-2 14 0"/>'),
        dict(name="Saddle<br>stitch", sub="Two needles, waxed linen thread", desc=B["craft"]["steps"][2]["body"], rows=[("Thread", "Waxed linen"), ("Needles", "Two, one row"), ("Why", "Cannot unravel")], n=2, unit="needles, one seam", bar=0.5,
             svg='<path data-bot d="M4 24l6-6 6 6 6-6 6 6 6-6 6 6"/><path data-bot d="M4 32l6-6 6 6 6-6 6 6 6-6 6 6"/>'),
        dict(name="Solid<br>brass", sub="Buckle on a removable screw post", desc=B["faqs"][0]["a"].split(":")[0] and "Solid brass buckle on a removable screw post, so you can change it without tools. No plated buckles dressed up as brass.", rows=[("Metal", "Solid brass"), ("Post", "Removable screw"), ("Plating", "None")], n=0, unit="plating, ever", bar=0.0,
             svg='<rect data-bot x="8" y="12" width="28" height="20" rx="6"/><path data-bot d="M8 22h22"/><circle data-bot cx="30" cy="22" r="2"/>'),
        dict(name="Beeswax<br>edge", sub="Bevelled, sanded, burnished four times", desc=B["craft"]["steps"][3]["body"], rows=[("Passes", "Four, by hand"), ("Seal", "Beeswax"), ("Checked", "Before it is packed")], n=4, unit="passes on every edge", bar=1.0,
             svg='<path data-bot d="M22 6c6 8 10 13 10 19a10 10 0 0 1-20 0c0-6 4-11 10-19z"/><path data-bot d="M18 26a4 4 0 0 0 4 4"/>'),
    ]
    inside_imgs = [cut("kingsmann"), cut("regal", 1), cut("monarch"), cut("regent")]
    inside_stack = lambda size: "".join(f'<img data-inside-img="{i}" src="{im[size]}" alt="" width="900" height="900" draggable="false" decoding="async" style="opacity:{1 if i == 0 else 0}">' for i, im in enumerate(inside_imgs))
    pills = "".join(f'<button type="button" class="pill" data-inside-pill="{i}" aria-pressed="{str(i == 0).lower()}">{d["name"].replace("<br>", " ")}</button>' for i, d in enumerate(inside))
    lefts = "".join(f'''
<div data-inside-left="{i}" {"hidden" if i else ""}>
  <div data-inside-hover><h3 class="inside-name" data-inside-name>{d["name"]}</h3></div>
  <div class="inside-sci" data-inside-sci><svg data-inside-svg viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" aria-hidden="true">{d["svg"]}</svg><span class="serif-i">{d["sub"]}</span></div>
</div>''' for i, d in enumerate(inside))
    rights = "".join(f'''
<div data-inside-right="{i}" {"hidden" if i else ""}>
  <p class="label"><b>0{i + 1}</b><span class="slash">/</span>04</p>
  <p class="inside-desc">{d["desc"]}</p>
  <dl class="spec" style="margin-top:20px">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in d["rows"])}<div><dt>Measure</dt><dd><span class="num" style="font-size:1.1rem" data-inside-dose="{d["n"]}">0</span> <span class="small muted">{d["unit"]}</span></dd></div></dl>
  <div class="inside-bar"><i data-inside-bar="{d["bar"]}"></i></div>
  <a class="btn btn--ghost btn--sm inside-cta" href="{"wallets.html" if i < 2 else "belts.html"}">Explore {"wallets" if i < 2 else "belts"} {I["arrow"]}</a>
</div>''' for i, d in enumerate(inside))
    deck = "".join(f'''
<article class="deck-card" data-halo="{["#D9B07A", "#C8976A", "#B8A58C", "#CDA373"][i]}">
  <p class="label"><b>0{i + 1}</b><span class="slash">/</span>04</p>
  <h3 class="inside-name" data-deck-title style="margin-top:12px">{d["name"].replace("<br>", " ")}</h3>
  <p class="serif-i muted" data-deck-item>{d["sub"]}</p>
  <p class="inside-desc" data-deck-item>{d["desc"]}</p>
  <dl class="spec" data-deck-item style="margin-top:16px">{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in d["rows"])}</dl>
  <p data-deck-item style="margin-top:18px"><a class="btn btn--ghost btn--sm" href="{"wallets.html" if i < 2 else "belts.html"}">Explore {"wallets" if i < 2 else "belts"} {I["arrow"]}</a></p>
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
    cards = "".join(ctx["pcard"](ctx, p, i, tags=" ".join(TAGS.get(p["id"], [])), quick=False, reveal=False) for i, p in enumerate(P))
    trust = B["trust"]["items"]

    css = r'''
/* ---- shared bits ---- */
.dotc { color: var(--accent); }
.rp-name, .inside-name { font-family: var(--font-display); font-weight: 300; font-size: clamp(2.6rem, 2rem + 4vw, 5.6rem); line-height: 1; letter-spacing: -.02em; }
.inside-name { font-family: var(--font-wordmark); font-weight: 800; font-size: clamp(1.9rem, 1.3rem + 2.4vw, 3.2rem); letter-spacing: -.01em; text-transform: uppercase; line-height: .95; }
.rp-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.rp-sub { margin-top: 10px; font-size: 1.05rem; }
.rp-copy { margin-top: 18px; max-width: 46ch; color: var(--fg-2); }
.rp-spec { margin-top: 22px; max-width: 420px; }

/* ---- 01 hero (desktop: pointer window; mobile: dark stage) ---- */
.hero { position: relative; width: 100%; min-height: 100svh; overflow: hidden; background: var(--ink); color: var(--bone); }
.hero-clip { position: absolute; inset: 0; background: var(--ink); z-index: 20; clip-path: circle(0px at 50% 48%); }
.hero-dolly { position: absolute; inset: 0; will-change: transform; }
.hero-parallax { position: absolute; inset: 0; display: grid; place-items: center; pointer-events: none; }
.hero-stage { position: absolute; inset: 0; }
.hero-float { position: absolute; left: 50%; top: 50%; width: min(52vh, 46vw); transform: translate(-50%, -50%); opacity: 0; }
.hero-float .pair { position: relative; width: 100%; aspect-ratio: 1; will-change: transform; }
.pair img { position: absolute; height: auto; filter: drop-shadow(0 40px 60px rgba(0,0,0,.45)); }
.pair .p-belt { left: -6%; top: 2%; width: 78%; transform: rotate(-8deg); }
.pair .p-wallet { right: -4%; bottom: 4%; width: 72%; }
.hero-float { width: min(60vh, 52vw); }
.hero-support { position: absolute; inset: 0 auto 0 0; z-index: 10; width: min(100%, 34vw); display: flex; flex-direction: column; justify-content: center; padding-left: var(--gutter); }
.hero-support .h3 { margin-top: 18px; max-width: 14ch; }
.hero-support p { color: rgba(239,237,230,.78); margin-top: 24px; max-width: 42ch; }
.hero-support .stats { margin-top: 28px; display: flex; gap: 20px; align-items: baseline; font-size: .8125rem; color: rgba(239,237,230,.6); }
.hero-support .stats .num { color: var(--bone); font-size: 1.1rem; }
.hero-overlay { position: absolute; inset: 0; z-index: 10; background: var(--bone); color: var(--ink); pointer-events: none; display: flex; flex-direction: column; }
.hero-overlay .title-wrap { flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.hero-title { font-family: var(--font-wordmark); font-weight: 800; font-size: 23vw; line-height: .78; letter-spacing: -.03em; white-space: nowrap; }
.hero-title [data-letter] { display: inline-block; opacity: 0; }
.hero-title .tdot { display: inline-block; width: .18em; height: .18em; background: var(--accent); margin-left: .05em; }
.hero-bottom { position: absolute; left: 0; right: 0; bottom: 0; display: flex; align-items: flex-end; justify-content: space-between; padding: 0 var(--gutter) 40px; gap: 24px; }
.hero-bottom .tag-line { font-family: var(--font-display); font-weight: 300; font-size: clamp(17px, 1.5vw, 24px); line-height: 1.15; letter-spacing: -.01em; }
.hero-bottom .meta { text-align: right; font-size: 11px; letter-spacing: .24em; text-transform: uppercase; line-height: 1.8; color: var(--mist); }
.hero-ring { position: absolute; top: 0; left: 0; z-index: 30; pointer-events: none; width: 459px; height: 459px; border-radius: 50%; background: radial-gradient(circle, transparent 56%, rgba(26,27,29,.1) 70%, transparent 84%); opacity: 0; transform: translate3d(-1000px, -1000px, 0); will-change: transform, opacity; }
.hero-mobile { position: relative; z-index: 10; display: flex; flex-direction: column; padding-top: calc(var(--nav-h) + 20px); }
.hero-mobile .hero-title { font-size: 19vw; line-height: .82; }
.hero-mobile .tag-line { font-family: var(--font-display); font-weight: 300; font-size: 26px; line-height: 1.1; margin-top: 16px; }
.hero-mobile .mstage { position: relative; height: 52svh; margin-top: 8px; }
.hero-mobile .mstage .bloom { --bloom-s: 70vw; }
.hero-mobile .mstage .hero-float { opacity: 0; width: 84vw; }
.hero-mobile .mmeta { padding: 0 20px 40px; font-size: 10px; letter-spacing: .24em; text-transform: uppercase; color: rgba(239,237,230,.5); }
.hero-mobile .msupport { padding: 24px 20px 80px; }
.hero-mobile .msupport .h3 { margin-top: 18px; }
.hero-mobile .msupport p.sup { margin-top: 22px; color: var(--bone); max-width: 44ch; }
.hero-mobile .stats { margin-top: 24px; display: flex; gap: 18px; font-size: .75rem; color: rgba(239,237,230,.6); }
.hero-mobile .stats .num { color: var(--bone); font-size: 1rem; }

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
.inside-pin { min-height: 100vh; display: flex; flex-direction: column; padding: calc(var(--nav-h) + 12px) var(--gutter) 32px; }
.inside-head { text-align: center; display: grid; justify-items: center; gap: 14px; }
.inside-title { font-family: var(--font-display); font-style: italic; font-weight: 300; font-size: clamp(2.6rem, 2rem + 3.4vw, 4.6rem); line-height: 1; opacity: 0; }
.inside-pills { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.inside .pill { border-color: rgba(239,237,230,.35); color: var(--bone); opacity: .65; }
.inside .pill[aria-pressed="true"] { background: var(--bone); color: var(--ink); border-color: var(--bone); opacity: 1; }
.inside-grid { flex: 1; display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 4fr) minmax(0, 5fr); gap: 24px; align-items: center; }
.inside-left { min-width: 0; }
.inside-sci { margin-top: 14px; display: flex; align-items: center; gap: 14px; color: rgba(239,237,230,.6); }
.inside-sci svg { width: 44px; height: 44px; flex: none; }
.inside-stage { position: relative; display: grid; place-items: center; min-height: 52vh; }
.inside-halo { position: absolute; inset: 0; margin: auto; width: 46vh; height: 46vh; transform: scale(1.6); border-radius: 50%; background: #D9B07A; opacity: .5; filter: blur(60px); pointer-events: none; }
.inside-float { position: relative; z-index: 1; width: min(44vh, 30vw); aspect-ratio: 1; display: grid; place-items: center; pointer-events: none; }
.inside-pills { position: relative; z-index: 2; }
.inside-float img { position: absolute; width: 100%; height: auto; max-height: 100%; object-fit: contain; filter: drop-shadow(0 40px 60px rgba(0,0,0,.5)); }
.inside-right { max-width: 420px; justify-self: end; width: 100%; }
.inside-desc { margin-top: 14px; color: rgba(239,237,230,.8); max-width: 40ch; }
.inside-bar { height: 1px; background: rgba(239,237,230,.15); margin-top: 10px; }
.inside-cta { margin-top: 22px; }
.inside-bar i { display: block; height: 100%; width: 100%; background: var(--accent); transform-origin: left; transform: scaleX(0); }
.inside-foot { text-align: center; font-size: 11px; letter-spacing: .3em; text-transform: uppercase; color: rgba(239,237,230,.5); padding-top: 24px; }
/* mobile deck */
.inside-mobile { padding: var(--section-sm) 0 56px; }
.inside-mobile .mstage { position: relative; height: 46vw; display: grid; place-items: center; margin: 8px 0 20px; }
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
.shop-sec { background: var(--bone); color: var(--ink); padding: var(--section-sm) 0 var(--section); }
.coll-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 20px 32px; margin-top: 12px; padding-bottom: 24px; border-bottom: 1px solid var(--line); }
.coll-tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.ctab { min-height: 44px; padding: 0 20px; border: 1px solid var(--line-strong); font-size: .75rem; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: var(--fg); transition: background-color .3s ease, color .3s ease, border-color .3s ease; }
.ctab:hover { border-color: var(--fg); }
.ctab[aria-selected="true"] { background: var(--ink); color: var(--bone); border-color: var(--ink); }
.pcard.is-hidden { display: none; }
.shop-grid { display: grid; gap: 16px; grid-template-columns: 1fr; margin-top: 32px; }
@media (min-width: 640px) { .shop-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .shop-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; } }
.delivery { display: grid; gap: 28px; margin-top: var(--section-sm); padding-top: 40px; border-top: 1px solid var(--line); }
@media (min-width: 768px) { .delivery { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.delivery h3 { font-family: var(--font-display); font-weight: 300; font-size: 1.5rem; }
.delivery p { color: var(--fg-2); font-size: .9375rem; margin-top: 8px; max-width: 26ch; }
.or-row { display: flex; align-items: center; gap: 20px; margin-top: var(--section-sm); }
.or-row .shop-rule { flex: 1; height: 1px; background: var(--line-strong); }
.or-row .label { white-space: nowrap; }
'''

    hero_cut = cut("kingsmann")
    hero_belt = cut("monarch")
    def pair(w, bl, size="src", a=""):
        return (f'<div class="pair"><img class="p-belt" src="{bl[size]}" alt="" width="900" height="900" draggable="false" decoding="async">'
                f'<img class="p-wallet" src="{w[size]}" alt="{a}" width="900" height="900" draggable="false" decoding="async"></div>')
    body = f'''
<section id="hero" class="hero on-ink" aria-label="Introduction">
  <div class="hero-clip" data-hero-clip>
    <div class="hero-dolly" data-hero-dolly>
      <div class="hero-parallax" data-hero-parallax><div class="bloom" style="--bloom:#D9B07A;--bloom-s:62vh" data-bloom></div></div>
    </div>
    <div class="hero-stage desk-only"><div class="hero-float" data-hero-float>{pair(hero_cut, hero_belt, "src", "Kingsmann bifold wallet and Monarch belt")}</div></div>
    <div class="hero-support desk-only" data-hero-support>
      <p class="label" data-support-item><b style="color:var(--bone)">01</b><span class="slash">/</span>The workshop</p>
      <h2 class="h3" data-support-item style="color:var(--bone)">{B["craft"]["heading"]}.</h2>
      <div class="rule" data-support-rule></div>
      <p data-support-item>{B["craft"]["body"]}</p>
      <div class="stats" data-support-item><span><span class="num">100</span> % crazy horse</span><span aria-hidden="true">·</span><span><span class="num">11</span> pieces</span><span aria-hidden="true">·</span><span><span class="num">3–5</span> days delivery</span></div>
    </div>
  </div>
  <div class="hero-overlay desk-only" data-hero-overlay>
    <div class="title-wrap"><h1 class="hero-title" data-hero-title><span class="sr-only">STAGR.</span><span data-letter aria-hidden="true">S</span><span data-letter aria-hidden="true">T</span><span data-letter aria-hidden="true">A</span><span data-letter aria-hidden="true">G</span><span data-letter aria-hidden="true">R</span><span data-letter aria-hidden="true" class="tdot"></span></h1></div>
    <div class="hero-bottom">
      <p class="tag-line">{B["hero"]["headline"][0]}<br>{B["hero"]["headline"][1]}</p>
      <div class="scroll-hint" data-hero-scrollhint aria-hidden="true"><span class="t">Scroll</span><span class="mouse"><i data-scroll-dot></i></span></div>
      <p class="meta">{B["origin"]}<br>Cash on delivery</p>
    </div>
  </div>
  <div class="hero-ring desk-only" data-hero-ring aria-hidden="true"></div>
  <div class="hero-mobile mob-only" data-hero-mobile>
    <div style="padding:0 20px"><h1 class="hero-title" data-hero-title-mobile><span class="sr-only">STAGR.</span><span data-letter aria-hidden="true">S</span><span data-letter aria-hidden="true">T</span><span data-letter aria-hidden="true">A</span><span data-letter aria-hidden="true">G</span><span data-letter aria-hidden="true">R</span><span data-letter aria-hidden="true" class="tdot"></span></h1><p class="tag-line">{B["hero"]["headline"][0]} {B["hero"]["headline"][1]}</p></div>
    <div class="mstage"><div class="bloom" style="--bloom:#D9B07A" data-bloom></div><div class="hero-float" data-hero-float-mobile>{pair(hero_cut, hero_belt, "small", "Kingsmann bifold wallet and Monarch belt")}</div></div>
    <p class="mmeta">{B["origin"]}<br>Cash on delivery</p>
    <div class="msupport">
      <div data-reveal><p class="label"><b style="color:var(--bone)">01</b><span class="slash">/</span>The workshop</p></div>
      <h2 class="h3" data-text-reveal="lines">{B["craft"]["heading"]}.</h2>
      <div data-reveal data-delay=".15"><div class="rule" style="margin-top:22px"></div></div>
      <p class="sup" data-illuminate>{B["craft"]["body"]}</p>
      <div data-reveal data-delay=".25"><div class="stats"><span><span class="num">100</span> % crazy horse</span><span>·</span><span><span class="num">11</span> pieces</span><span>·</span><span><span class="num">3–5</span> days</span></div></div>
    </div>
  </div>
</section>

<section id="range" class="range on-bone" aria-labelledby="range-title">
  <div class="range-pin desk-only" data-range-pin>
    <div class="range-bg">{stage_blooms}</div>
    <div class="range-head">
      <div><p class="label" data-range-label><b>02</b><span class="slash">/</span>The range</p><h2 class="range-title" id="range-title" data-range-title-main>Five ways to carry.</h2></div>
      <p class="range-count" data-range-count>1 / 5</p>
    </div>
    <div class="range-body">
      <div class="range-text" data-range-text>{panels}</div>
      <div class="range-stage" data-range-stage>{stage_ghosts}{stage_cuts}</div>
    </div>
    <div class="range-dots">{dots}</div>
  </div>
  <div class="range-mobile mob-only" data-range-mobile>
    <div class="mhead"><div data-reveal><p class="label"><b>02</b><span class="slash">/</span>The range</p></div><h2 class="h2" data-text-reveal="lines" style="margin-top:12px">Five ways to carry.</h2><p class="label" data-reveal data-delay=".2" style="margin-top:14px;font-size:.75rem">Swipe to browse</p></div>
    <div class="mtrack" data-mrange-track>{mcards}</div>
    <div class="mdots">{mdots}</div>
  </div>
</section>

<section id="inside" class="inside on-ink" aria-labelledby="inside-title">
  <div class="inside-pin desk-only" data-inside-pin>
    <div class="inside-head"><p class="label"><b style="color:var(--bone)">03</b><span class="slash">·</span>What every piece is made of</p><h2 class="inside-title" id="inside-title" data-inside-title>Inside.</h2><div class="inside-pills">{pills}</div></div>
    <div class="inside-grid">
      <div class="inside-left">{lefts}</div>
      <div class="inside-stage" data-inside-stage><div class="inside-halo" data-inside-halo></div><div class="inside-float" data-inside-float>{inside_stack("src")}</div></div>
      <div class="inside-right">{rights}</div>
    </div>
    <p class="inside-foot">One hide. One workshop. Nothing else.</p>
  </div>
  <div class="inside-mobile mob-only" data-inside-mobile>
    <div style="padding:0 20px;text-align:center"><p class="label" data-reveal><b style="color:var(--bone)">03</b><span class="slash">·</span>What every piece is made of</p><h2 class="inside-title" data-inside-title-mobile style="opacity:1;margin-top:10px">Inside.</h2></div>
    <div class="mstage"><div class="inside-halo" data-inside-halo-mobile></div><div class="inside-float" data-inside-float-mobile>{inside_stack("small")}</div></div>
    <div class="deck" data-deck-track>{deck}</div>
    <div class="mdots">{"".join(f'<button type="button" data-deck-dot="{i}" style="color:{"var(--bone)" if i == 0 else "rgba(239,237,230,.35)"}">0{i + 1}</button>' for i in range(4))}</div>
    <p class="inside-foot" style="padding:24px 20px 0">One hide. One workshop. Nothing else.</p>
  </div>
</section>

<section id="story" class="story on-bone" aria-labelledby="story-title">
  <div class="story-pin desk-only" data-story-pin>
    <div class="story-intro" data-story-intro><p class="label"><b>04</b><span class="slash">/</span>Story</p><h2 class="h1" id="story-title" data-story-title>{B["about"]["headline"]}.</h2><p class="lead">{B["about"]["intro"]} {B["about"]["sections"][2]["body"].split(".")[0]}.</p><div class="scroll-hint" style="margin-top:36px" aria-hidden="true"><span class="t">Scroll</span></div></div>
    <div class="story-stage" data-story-stage>{ghosts}{figures}{spanels}<div class="story-years"><div class="story-progress" data-story-progress></div>{years}</div></div>
  </div>
  <div class="story-mobile mob-only">
    <div data-reveal><p class="label"><b>04</b><span class="slash">/</span>Story</p></div>
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

<section id="promise" class="promise on-ink" aria-labelledby="promise-title">
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

<section id="shop" class="shop-sec on-bone" aria-labelledby="shop-title">
  <div class="wrap">
    <div data-reveal><p class="label"><b>06</b><span class="slash">/</span>Shop</p></div>
    <div class="coll-head">
      <h2 class="h2" id="shop-title" data-text-reveal="lines">The collection</h2>
      <div class="coll-tabs" role="tablist" aria-label="Filter the collection" data-reveal data-delay=".15">
        <button type="button" class="ctab" role="tab" aria-selected="true" data-tab="new">New in</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="best">Bestsellers</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="gift">Gifting</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="under">Under Rs 2,000</button>
        <button type="button" class="ctab" role="tab" aria-selected="false" data-tab="all">All</button>
      </div>
    </div>
    <div class="shop-grid" data-shop-grid>{cards}</div>
    <p class="small muted" style="margin-top:24px"><span data-shop-count></span> · Cash on delivery, 3 to 5 working days anywhere in Pakistan.</p>
    <div class="or-row" id="delivery"><span class="shop-rule" data-shop-rule style="transform-origin:right"></span><span class="label">How it reaches you</span><span class="shop-rule" data-shop-rule style="transform-origin:left"></span></div>
    <div class="delivery">{"".join(f'<div data-reveal data-delay="{i * .1}"><h3>{t["title"]}</h3><p>{t["sub"]}</p></div>' for i, t in enumerate(trust))}</div>
  </div>
</section>
'''

    js = r'''
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, clamp = S.clamp;
  const isMobile = S.isMobile, reduced = S.reduced, fine = S.fine, isRendered = S.isRendered;
  if (!G) return;

  /* ================= 01 HERO ================= */
  function initScrollHint() { const dot = $("[data-scroll-dot]"); if (!dot || !isRendered(dot)) return; if (reduced) { G.set(dot, { opacity: 1, y: 9 }); return; } G.timeline({ repeat: -1, repeatDelay: .5 }).set(dot, { y: 0, opacity: 0 }).to(dot, { opacity: 1, duration: .25 }).to(dot, { y: 19, duration: 1, ease: "power2.inOut" }, .1).to(dot, { opacity: 0, duration: .3, ease: "power1.in" }, .85); }

  function initHeroDesktop() {
    const hero = $("#hero"), clip = $("[data-hero-clip]"), ring = $("[data-hero-ring]"), dolly = $("[data-hero-dolly]"), parallax = $("[data-hero-parallax]"), overlay = $("[data-hero-overlay]"), hint = $("[data-hero-scrollhint]"), support = $("[data-hero-support]"), wrap = $("[data-hero-float]"), img = $(".pair", wrap);
    const BASE = 170, unit = () => window.innerHeight / 4.54;
    const w = { x: innerWidth / 2, y: .48 * innerHeight, entrance: 0, swell: 0, breath: 0, boost: 0, hasPointer: false };
    const lock = { v: 0 }, zoom = { v: 0 }, entrance = { v: 0 }, follow = { x: 0, y: 0, active: false }, bloomOff = { x: 0, y: 0 }, cs = { x: 0, y: 0, lean: 0 };
    let pointerActive = false, released = false, startedAt = 0;
    G.set(wrap, { opacity: 0 });
    const mx = G.quickTo(w, "x", { duration: .62, ease: "power2.out" }), my = G.quickTo(w, "y", { duration: .62, ease: "power2.out" });
    if (!reduced) G.to(w, { breath: 9, duration: 2.2, yoyo: true, repeat: -1, ease: "sine.inOut" });
    if (fine) {
      let lx = 0, ly = 0, lt = 0; const settle = G.delayedCall(.3, () => G.to(w, { swell: 0, duration: 1.1, ease: "power2.out", overwrite: "auto" })).pause();
      window.addEventListener("pointermove", (e) => { const now = performance.now(); if (!w.hasPointer) { w.hasPointer = true; lx = e.clientX; ly = e.clientY; lt = now; } mx(e.clientX); my(e.clientY); const el = Math.max(now - lt, 1), speed = Math.hypot(e.clientX - lx, e.clientY - ly) / el * 1000, swell = Math.min(130, speed / 2200 * 130); if (swell > w.swell + 1) G.to(w, { swell, duration: .3, ease: "power2.out", overwrite: "auto" }); settle.restart(true); lx = e.clientX; ly = e.clientY; lt = now; if (!reduced) { pointerActive = true; released = false; } }, { passive: true });
    }
    const render = (time, dms) => {
      const dt = Math.max(dms / 1000, .001), locked = lock.v;
      if (locked > .98 && !released) { released = true; pointerActive = false; w.hasPointer = false; mx(innerWidth / 2); my(.48 * innerHeight); }
      const falloff = Math.pow(1 - Math.min(locked / .6, 1), 3);
      if (pointerActive && locked < .999) { follow.x = clamp(w.x / innerWidth * 2 - 1, -1, 1) * falloff; follow.y = clamp(-(w.y / innerHeight * 2 - 1), -1, 1) * falloff; follow.active = true; } else follow.active = false;
      bloomOff.x += ((w.x - innerWidth / 2) * .85 * falloff - bloomOff.x) * .06; bloomOff.y += ((w.y - innerHeight / 2) * .85 * falloff - bloomOff.y) * .06;
      parallax.style.transform = "translate3d(" + bloomOff.x + "px," + bloomOff.y + "px,0)";
      const radius = Math.max(0, BASE * w.entrance + w.swell + w.breath * w.entrance + w.boost);
      clip.style.clipPath = "circle(" + radius.toFixed(1) + "px at " + w.x.toFixed(1) + "px " + w.y.toFixed(1) + "px)";
      ring.style.transform = "translate3d(" + w.x + "px," + w.y + "px,0) translate(-50%,-50%) scale(" + (radius / BASE).toFixed(3) + ")";
      ring.style.opacity = (w.entrance * clamp(1 - w.boost / 240, 0, 1)).toFixed(3);
      const tx = follow.active ? 2.5 * follow.x : 0, ty = follow.active ? 1.6 * follow.y : 0, ease = .09 + locked * .09, px = cs.x;
      cs.x += (tx - cs.x) * ease; cs.y += (ty - cs.y) * ease;
      const lean = clamp(-(.016 * (1 / dt * 1.4 * (cs.x - px))), -.22, .22) * (follow.active ? 1 - locked : 0); cs.lean += (lean - cs.lean) * .075;
      const u = unit(), settled = entrance.v, bob = startedAt && !reduced ? .06 * Math.sin(2 * Math.PI / 6 * (time - startedAt)) : 0;
      const x = cs.x * u, y = -(cs.y + bob) * u - 4 * u * (1 - settled), scale = (.8 + .2 * settled) * (1 + zoom.v), rot = -cs.lean * 180 / Math.PI - 14 * (1 - settled);
      wrap.style.opacity = settled.toFixed(3); wrap.style.transform = "translate(-50%,-50%) translate3d(" + x.toFixed(2) + "px,0,0)";
      img.style.transform = "translate3d(0," + y.toFixed(2) + "px,0) rotate(" + rot.toFixed(2) + "deg) scale(" + scale.toFixed(4) + ")";
    };
    G.ticker.add(render);
    if (!reduced) {
      const items = $$("[data-support-item]", support), rule = $("[data-support-rule]", support);
      G.set(items, { y: 26, opacity: 0 }); G.set(rule, { scaleX: 0, transformOrigin: "left center" });
      const tl = G.timeline({ defaults: { ease: "power2.inOut" }, scrollTrigger: { trigger: hero, start: "top top", end: "+=120%", pin: true, pinSpacing: true, scrub: true, invalidateOnRefresh: true, refreshPriority: 3 } });
      tl.to(w, { boost: () => 1.2 * Math.hypot(innerWidth, innerHeight), ease: "power2.in", duration: .55 }, 0).to(lock, { v: 1, ease: "power1.inOut", duration: .6 }, 0).to(overlay, { opacity: 0, ease: "none", duration: .15 }, .48).to(dolly, { scale: 1.09, duration: 1, ease: "none" }, 0).to(zoom, { v: .09, duration: 1, ease: "none" }, 0).to(hint, { opacity: 0, duration: .15 }, 0);
      const supportIn = G.timeline({ paused: true }); supportIn.to(items, { y: 0, opacity: 1, duration: .55, stagger: .08, ease: "power2.out" }); supportIn.to(rule, { scaleX: 1, duration: .5 }, .2);
      let shown = false;
      tl.eventCallback("onUpdate", () => { const p = tl.progress(); if (!shown && p > .58) { shown = true; supportIn.restart(); } else if (shown && p < .35) { shown = false; G.to(support, { opacity: 0, duration: .25, overwrite: "auto", onComplete: () => { supportIn.pause(0); G.set(items, { y: 26, opacity: 0 }); G.set(rule, { scaleX: 0 }); G.set(support, { opacity: 1 }); } }); } });
    } else { w.boost = 1.2 * Math.hypot(innerWidth, innerHeight); G.set(overlay, { opacity: 0 }); }
    return function start() { G.set($$("[data-letter]", overlay), { opacity: 1, y: 0 }); startedAt = G.ticker.time; G.to(w, { entrance: 1, duration: 1.2, delay: .15, ease: "power2.inOut" }); G.to(entrance, { v: 1, duration: 1.6, ease: "power4.out" }); };
  }
  function initHeroMobile() {
    const wrap = $("[data-hero-float-mobile]"), img = $(".pair", wrap), title = $("[data-hero-title-mobile]");
    G.set(wrap, { opacity: 0 });
    return function start() { const letters = $$("[data-letter]", title); if (reduced) { G.set(letters, { opacity: 1 }); G.set(wrap, { opacity: 1 }); return; } G.fromTo(letters, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .9, ease: "power2.out", stagger: .05 }); G.to(wrap, { opacity: 1, duration: 1.2 }); G.fromTo(img, { yPercent: -60, scale: .8, rotation: -14 }, { yPercent: 0, scale: 1, rotation: 0, duration: 1.6, ease: "power4.out", onComplete: () => G.to(img, { y: -8, duration: 3, yoyo: true, repeat: -1, ease: "sine.inOut" }) }); ST.refresh(); };
  }

  /* ================= 02 RANGE ================= */
  function initRangeDesktop() {
    const section = $("#range"), pin = $("[data-range-pin]"), title = $("[data-range-title-main]"), label = $("[data-range-label]"), count = $("[data-range-count]"), panels = $$("[data-range-panel]"), bgs = $$("[data-range-bloom]"), ghosts = $$("[data-range-ghost]"), cuts = $$("[data-range-cut]"), stage = $("[data-range-stage]"), dots = $$("[data-range-dot]");
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
    const STEPS = 3; let scrolling = null;
    const pick = (progress) => { const p = progress * STEPS; let next = active; while (next < STEPS && p > next + .5 + .1) next++; while (next > 0 && p < next - .5 - .1) next--; return next; };
    const trigger = ST.create({ trigger: section, start: "top top", end: () => "+=" + 3 * innerHeight, pin: true, pinSpacing: true, scrub: .6, snap: { snapTo: (v) => scrolling !== null ? v : G.utils.snap(1 / STEPS, v), duration: { min: .25, max: .6 }, ease: "power2.inOut", directional: false, delay: .15, inertia: false }, invalidateOnRefresh: true, onUpdate: (self) => { if (scrolling !== null) return; setActive(pick(self.progress)); } });
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
  const startHero = isMobile ? initHeroMobile() : initHeroDesktop();
  initScrollHint(); S.initReveals($("#hero"));
  if (isMobile) initRangeMobile(); else initRangeDesktop();
  S.initReveals($("#range"));
  initInside();
  if (isMobile) initStoryMobile(); else initStoryDesktop();
  S.initReveals($("#story"));
  initPromise(); S.initReveals($("#promise"));
  initShop(); S.initReveals($("#shop")); S.initReveals($("footer"));
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
