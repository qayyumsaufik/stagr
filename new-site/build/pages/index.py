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
    inside_imgs = [{"src": "assets/cutouts/inside-belt.webp", "small": "assets/cutouts/inside-belt-600.webp"}, {"src": "assets/cutouts/inside-wallet.webp", "small": "assets/cutouts/inside-wallet-600.webp"}]
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

    # ---------------- 03b anatomy: the piece, taken apart ----------------
    # callout: (title, note, crop n, dot x%, dot y%); dots are on the top image unless the callout sits under the low image
    IC = {
        "hide": '<path d="M7 5h10l3 5-2 9H6L4 10z"/><path d="M9 9h6"/>',
        "stitch": '<path d="M4 15c3-6 7-6 10 0s7 6 10 0"/><path d="M8 11l1 2M15 13l1 2"/>',
        "buckle": '<rect x="4" y="7" width="16" height="10" rx="2"/><path d="M4 12h9"/><circle cx="13" cy="12" r="1.2"/>',
        "holes": '<rect x="3" y="8" width="18" height="8" rx="4"/><circle cx="8" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="16" cy="12" r="1.2"/>',
        "edge": '<path d="M3 15l9-9 9 9"/><path d="M6 15l6-6 6 6"/>',
        "layers": '<path d="M12 4l9 5-9 5-9-5z"/><path d="M3 14l9 5 9-5"/>',
        "leaf": '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14z"/><path d="M5 19l8-8"/>',
        "cards": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/>',
        "notes": '<rect x="3" y="7" width="18" height="10" rx="1"/><circle cx="12" cy="12" r="2"/>',
        "slim": '<rect x="9" y="3" width="6" height="18" rx="1"/><path d="M9 8h6M9 16h6"/>',
    }
    anatomy = [
        dict(key="belt", tab="Belts", name="Handcrafted leather belt", tags="Timeless style / Premium quality / Built to last",
             top=dict(img="monarch-1", w=740, h=560), low=dict(img="monarch-2", w=1024, h=433), href="belts.html", cta="Shop belts",
             left=[("Solid buckle", "Solid buckle on a removable screw post, so you can change it without tools.", 4, 16, 62),
                   ("Reinforced stitching", "One row of saddle stitch in waxed linen thread. It cannot unravel the way a machine seam can.", 2, 42, 80),
                   ("Burnished edges", "Bevelled, sanded and burnished four times, then sealed with beeswax.", 3, 6, 34)],
             right=[("Genuine full-grain leather", "Crazy horse cowhide, treated with wax for a rugged surface and a patina that deepens with wear.", 1, 82, 24),
                    ("Keeper loop", "Holds the tail of the strap flat and in place.", 5, 58, 62),
                    ("Tapered tip", "A rounded tip that threads cleanly through the buckle and keeper.", 6, 88, 58)],
             low_calls=[("Adjustment holes", "Sizes 30 to 44, measured from the buckle bar to the hole you use.", 7, 30, 80),
                        ("Ideal thickness", "3.5 mm, cut in one piece along the spine of the hide.", 8, 50, 96),
                        ("Develops a patina", "Every scuff stays. Honey today, chestnut in a year.", 9, 76, 76)],
             icons=[("hide", "Full-grain leather"), ("stitch", "Hand stitched"), ("buckle", "Solid buckle"), ("holes", "Sizes 30 to 44"), ("edge", "Burnished edges"), ("layers", "3.5 mm, one piece"), ("leaf", "Develops a patina")]),
        dict(key="wallet", tab="Wallets", name="Handcrafted bifold wallet", tags="Timeless style / Premium quality / Everyday function",
             top=dict(img="kingsmann-brown-1", w=916, h=678), low=dict(img="kingsmann-brown-2", w=1321, h=635), href="wallets.html", cta="Shop wallets",
             left=[("Full-grain leather", "Crazy horse cowhide, treated with wax, that softens and darkens with every carry.", 1, 16, 40),
                   ("Hand-stitched construction", "One row of saddle stitch, two needles, waxed linen thread.", 2, 32, 8),
                   ("Burnished edges", "Bevelled, sanded and burnished, then sealed with beeswax.", 3, 7, 88)],
             right=[("Slim profile", "Skived at the fold so it stays flat in a jacket pocket.", 4, 94, 48),
                    ("Embossed stag", "The Stagr mark pressed into the leather, no foil.", 5, 78, 76),
                    ("Develops a patina", "The waxed surface marks and deepens with use, so no two age the same way.", 6, 80, 28)],
             low_calls=[("Four card slots", "Two each side, cut so a card sits flush.", 7, 30, 25),
                        ("Note section", "One full-width section for folded notes.", 8, 50, 30),
                        ("Compact everyday carry", "Cards and notes in a wallet that still fits a front pocket.", 9, 86, 72)],
             icons=[("hide", "Full-grain leather"), ("stitch", "Hand stitched"), ("edge", "Burnished edges"), ("cards", "Four card slots"), ("notes", "Note section"), ("slim", "Slim profile"), ("leaf", "Develops a patina")]),
    ]
    def an_call(piece, c, side, target):
        t, note, n, x, y = c
        return f'''<li class="an-call an-call--{side}" data-an-call data-an-target="{target}" data-an-x="{x}" data-an-y="{y}"><span class="an-circle"><img src="assets/details/anat-{piece}-{n}.webp" alt="" width="360" height="360" loading="lazy" draggable="false"></span><span class="an-text"><b>{t}</b><span>{note}</span></span></li>'''
    def an_panel(i, d):
        k = d["key"]; cutimg = lambda im, size: f"assets/cutouts/{im}{size}.webp"
        return f'''
<div class="an-panel" data-an-panel="{i}" {"hidden" if i else ""}>
  <div class="an-head"><p class="an-kicker"><span>The anatomy of a</span></p><h3 class="an-name">{d["name"]}</h3><p class="an-tags">{d["tags"].replace(" / ", '<i>/</i>')}</p></div>
  <div class="an-body">
    <svg class="an-lines" data-an-lines aria-hidden="true"></svg>
    <ul class="an-col an-col--l" role="list">{"".join(an_call(k, c, "l", "top") for c in d["left"])}</ul>
    <div class="an-stage" data-an-top><div class="an-box" style="aspect-ratio:{d["top"]["w"]} / {d["top"]["h"]}"><img data-an-img src="{cutimg(d["top"]["img"], "")}" alt="{d["name"]}" width="{d["top"]["w"]}" height="{d["top"]["h"]}" loading="lazy" decoding="async" draggable="false"></div></div>
    <ul class="an-col an-col--r" role="list">{"".join(an_call(k, c, "r", "top") for c in d["right"])}</ul>
    <div class="an-low" data-an-low><div class="an-box" style="aspect-ratio:{d["low"]["w"]} / {d["low"]["h"]}"><img data-an-img src="{cutimg(d["low"]["img"], "")}" alt="" width="{d["low"]["w"]}" height="{d["low"]["h"]}" loading="lazy" decoding="async" draggable="false"></div></div>
    <ul class="an-col an-col--low" role="list">{"".join(an_call(k, c, "low", "low") for c in d["low_calls"])}</ul>
  </div>
  <ul class="an-icons" role="list">{"".join(f'<li data-an-icon><span class="an-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{IC[ic]}</svg></span><span>{lbl}</span></li>' for ic, lbl in d["icons"])}</ul>
  <p class="an-cta"><a class="btn btn--tan" href="{d["href"]}">{d["cta"]} {I["arrow"]}</a></p>
</div>'''
    an_panels = "".join(an_panel(i, d) for i, d in enumerate(anatomy))
    an_pills = "".join(f'<button type="button" class="pill" data-an-pill="{i}" aria-pressed="{str(i == 0).lower()}">{d["tab"]}</button>' for i, d in enumerate(anatomy))

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
    cards = "".join(ctx["ccard"](ctx, p, i) for i, p in enumerate(P))
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
@media (max-width: 767px) { .bulk-band::before { display: none; } .bulk-inner { flex-wrap: wrap; gap: 12px 14px; padding-top: 18px; padding-bottom: 18px; } .bulk-icon { margin-left: 0; } .bulk-text { flex: 1 1 calc(100% - 54px); min-width: 0; } .bulk-text b { font-size: .9375rem; } .bulk-btn { flex: 1 1 100%; justify-content: center; } }

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
.more { padding: clamp(32px, 5vw, 64px) 0 clamp(16px, 2vw, 24px); background: var(--bone); color: var(--ink); }
.bento { display: grid; gap: 14px; grid-template-columns: 1fr; }
.ftile { position: relative; display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; background: #F4F2EE; color: var(--ink); box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 12px 30px -20px rgba(26,27,29,.2); transition: transform .4s var(--ease-out), box-shadow .4s ease; }
.ftile:hover { transform: translateY(-3px); box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 26px 44px -22px rgba(26,27,29,.28); }
.ftile-copy { padding: clamp(18px, 2.2vw, 26px) clamp(20px, 2.4vw, 30px) clamp(14px, 1.8vw, 20px); }
.ftile h2 { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.5rem, 1.1rem + 1.3vw, 2.1rem); line-height: 1.06; letter-spacing: -.012em; }
.ftile p { margin-top: 6px; max-width: 44ch; font-size: .9375rem; line-height: 1.45; color: var(--fg-2); }
.ftile-main h2 { font-size: clamp(1.8rem, 1.2rem + 1.8vw, 2.6rem); }
.ftile-pic { position: relative; flex: 1; min-height: 0; overflow: hidden; }
.ftile img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 55% 55%; transform: scale(1.02); transition: transform 1.1s var(--ease-out); }
.ftile:hover img { transform: scale(1.06); }
.ftile { aspect-ratio: 16 / 11; }
.ftile-main { aspect-ratio: 4 / 3; }
.pair img { position: absolute; height: auto; filter: drop-shadow(0 40px 60px rgba(0,0,0,.45)); }
.pair .p-belt { left: -6%; top: 2%; width: 78%; transform: rotate(-8deg); }
.pair .p-wallet { right: -4%; bottom: 4%; width: 72%; }
@media (min-width: 640px) and (max-width: 1023px) { .bento { grid-template-columns: 1fr 1fr; } .ftile-main { grid-column: 1 / -1; aspect-ratio: 16 / 8; } }
@media (max-width: 639px) { .bento { gap: 10px; } .ftile, .ftile-main { aspect-ratio: 4 / 3.4; } }
@media (min-width: 1024px) { .bento { grid-template-columns: 56fr 44fr; grid-template-rows: 1fr 1fr; gap: 16px; height: clamp(560px, 64vw * .62, 720px); } .ftile { aspect-ratio: auto !important; } .ftile-main { grid-row: 1 / 3; } }

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
.inside-float { position: relative; z-index: 1; width: min(54vh, 100%); aspect-ratio: 1; display: grid; place-items: center; pointer-events: none; }
.inside-pills { position: relative; z-index: 2; }
.inside-float img { position: absolute; width: 100%; height: auto; max-height: 100%; object-fit: contain; filter: drop-shadow(0 40px 60px rgba(0,0,0,.5)); }
.inside-right { max-width: 420px; justify-self: end; width: 100%; }
.inside-right .spec > div { padding: 8px 0; }
@media (max-height: 820px) { .inside-measure, .inside-foot { display: none; } .inside-desc { margin-top: 10px; font-size: .9375rem; } .inside-point { margin-top: 12px; padding-top: 10px; } .inside-cta { margin-top: 12px; min-height: 44px; } .inside-float { width: min(46vh, 100%); } .inside-pills .pill { min-height: 34px; } }
.inside-desc { margin-top: 14px; color: rgba(239,237,230,.8); max-width: 40ch; }
.inside-bar { height: 1px; background: rgba(239,237,230,.15); margin-top: 10px; }
.inside-point { margin-top: 18px; padding-top: 14px; border-top: 1px solid rgba(239,237,230,.15); font-size: .9375rem; color: var(--bone); display: flex; gap: 10px; align-items: baseline; }
.inside-point span { color: var(--accent); font-weight: 500; }
.inside-cta { margin-top: 18px; width: 100%; justify-content: center; }
.inside-bar i { display: block; height: 100%; width: 100%; background: var(--accent); transform-origin: left; transform: scaleX(0); }
.inside-foot { text-align: center; font-size: 11px; letter-spacing: .3em; text-transform: uppercase; color: rgba(239,237,230,.5); padding-top: 12px; }
/* mobile deck */
.inside-mobile { padding: var(--section-sm) 0 56px; }
.inside-mobile .mstage { position: relative; height: 58vw; display: grid; place-items: center; margin: 8px 0 20px; touch-action: pan-y; }
.inside-mobile .inside-pills { margin-top: 16px; }
.inside-mobile .inside-lead { margin-top: 12px; }
.inside-mobile .inside-halo { width: 60vw; height: 60vw; transform: scale(1.3); }
.inside-mobile .inside-float { width: 62vw; }
.deck { display: flex; gap: 5vw; overflow-x: auto; scroll-snap-type: x mandatory; padding: 8px 9vw 16px; scrollbar-width: none; }
.deck::-webkit-scrollbar { display: none; }
.deck-card { flex: 0 0 82vw; scroll-snap-align: center; }
.deck-card .inside-name { opacity: 0; }
.deck-card [data-deck-item] { opacity: 0; margin-top: 12px; }
.inside-mobile .mdots button { color: rgba(239,237,230,.35); }

/* ---- 03b anatomy ---- */
.anatomy { background: var(--bone); color: var(--ink); padding: clamp(56px, 7vw, 96px) 0 clamp(40px, 5vw, 64px); overflow: hidden; }
.anatomy .inside-pills { display: flex; gap: 8px; justify-content: center; margin-top: 14px; }
.an-panel[hidden] { display: none; }
.an-head { text-align: center; display: grid; gap: 6px; justify-items: center; margin-top: clamp(24px, 3vw, 36px); }
.an-kicker { display: flex; align-items: center; gap: 16px; font-size: .75rem; letter-spacing: .32em; text-transform: uppercase; color: var(--fg-2); }
.an-kicker::before, .an-kicker::after { content: ""; width: clamp(40px, 8vw, 120px); height: 1px; background: var(--accent-deep); opacity: .6; }
.an-name { font-family: var(--font-display); font-weight: 400; font-size: clamp(1.9rem, 1.2rem + 2.6vw, 3.4rem); line-height: 1.05; letter-spacing: .02em; text-transform: uppercase; }
.an-tags { font-size: .75rem; letter-spacing: .3em; text-transform: uppercase; color: var(--fg-2); }
.an-tags i { font-style: normal; margin: 0 .9em; color: var(--accent-deep); }
.an-body { position: relative; display: grid; gap: 18px; margin-top: clamp(24px, 3vw, 40px); }
.an-lines { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; pointer-events: none; z-index: 2; display: none; }
.an-lines path { fill: none; stroke: var(--accent-deep); stroke-width: 1; stroke-linejoin: round; stroke-linecap: round; opacity: .85; }
.an-lines circle { fill: var(--accent); stroke: var(--bone); stroke-width: 1.5; }
.an-box { position: relative; width: 100%; }
.an-box img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 18px 26px rgba(26,27,29,.22)); }
.an-stage { width: min(100%, 440px); margin: 0 auto; }
.an-low { width: min(100%, 520px); margin: 0 auto; }
.an-col { display: grid; gap: 14px; }
.an-call { display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 12px; align-items: center; }
.an-circle { width: 64px; height: 64px; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 1.5px var(--accent-deep), 0 0 0 5px rgba(139,74,31,.12), 0 14px 22px -10px rgba(26,27,29,.35); transform: scale(0); }
.an-circle img { width: 100%; height: 100%; display: block; }
.an-text { display: grid; gap: 3px; }
.an-text b { font-family: var(--font-display); font-weight: 400; font-size: 1.05rem; line-height: 1.15; letter-spacing: .03em; text-transform: uppercase; }
.an-text b::after { content: ""; display: block; width: 100%; height: 1px; margin-top: 5px; background: var(--accent-deep); opacity: .55; }
.an-text span { font-size: .8125rem; line-height: 1.45; color: var(--fg-2); }
.an-icons { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 16px; margin-top: clamp(28px, 4vw, 44px); padding-top: 22px; border-top: 1px solid var(--line-strong); }
.an-icons li { display: flex; align-items: center; gap: 10px; font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; color: var(--fg); }
.an-ic { flex: none; width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--accent-deep); display: grid; place-items: center; color: var(--accent-deep); }
.an-ic svg { width: 22px; height: 22px; }
.an-cta { display: flex; justify-content: center; margin-top: 26px; }
@media (min-width: 1024px) {
  .an-body { grid-template-columns: minmax(0, 3fr) minmax(0, 4fr) minmax(0, 3fr); grid-template-areas: "l stage r" "low low low" "lc lc lc"; column-gap: clamp(24px, 3vw, 56px); row-gap: 28px; align-items: center; }
  .an-lines { display: block; }
  .an-col--l { grid-area: l; } .an-stage { grid-area: stage; width: 100%; max-width: 520px; } .an-col--r { grid-area: r; } .an-low { grid-area: low; width: min(100%, 640px); } .an-col--low { grid-area: lc; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 28px; align-items: start; width: min(100%, 880px); margin: 0 auto; }
  .an-col--l, .an-col--r { gap: 26px; }
  .an-call { grid-template-columns: 88px minmax(0, 1fr); gap: 16px; }
  .an-circle { width: 88px; height: 88px; }
  .an-col--low .an-call { grid-template-columns: 76px minmax(0, 1fr); align-items: start; }
  .an-col--low .an-circle { width: 76px; height: 76px; }
  .an-icons { grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 12px; }
  .an-icons li { flex-direction: row; }
  .an-icons li + li { border-left: 1px solid var(--line); padding-left: 14px; }
}
@media (min-width: 1280px) { .an-text b { font-size: 1.15rem; } .an-text span { font-size: .875rem; } }
@media (max-width: 1023px) { .an-head { margin-top: 24px; } .an-col--low .an-call, .an-call { align-items: center; } }
@media (max-width: 767px) { .an-kicker::before, .an-kicker::after { width: 28px; } .an-name { font-size: 1.6rem; } .an-tags { font-size: .6875rem; letter-spacing: .2em; } .an-icons { grid-template-columns: 1fr 1fr; } .an-icons li { font-size: .6875rem; } }
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
.promise { background: var(--ink); color: var(--bone); padding: 0; overflow: hidden; }
.promise-title { font-family: var(--font-wordmark); font-weight: 800; font-size: clamp(2.2rem, 1.6rem + 3vw, 4.4rem); letter-spacing: -.02em; text-transform: uppercase; line-height: .95; margin-top: 14px; }
.pquotes { display: grid; gap: 32px; margin-top: 48px; }
@media (min-width: 768px) { .pquotes { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 40px; } }
.pquote blockquote { font-size: clamp(1.1rem, 1rem + .6vw, 1.5rem); line-height: 1.35; color: rgba(239,237,230,.92); }
.pquote figcaption { color: rgba(239,237,230,.5); }
.press-marquee { margin-top: 0; border-top: 1px solid rgba(239,237,230,.15); padding: 10px 0; will-change: transform; }
.press-marquee .track > span { font-family: var(--font-display); font-weight: 300; font-size: clamp(1rem, .9rem + .5vw, 1.25rem); color: var(--bone); }
.press-marquee .track .mq-dot { color: var(--accent); font-size: .75rem; }
.press-marquee .track .outline { color: transparent; -webkit-text-stroke: 1px rgba(239,237,230,.6); }
.press-marquee .row2 { margin-top: 12px; }

/* ---- 06 shop ---- */
.shop-sec { background: var(--bone); color: var(--ink); padding: clamp(32px, 5vw, 64px) 0 clamp(16px, 2vw, 24px); }
.coll-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 20px 32px; margin-bottom: clamp(20px, 3vw, 28px); }
.coll-tabs { display: flex; flex-wrap: wrap; gap: 8px; }
.ctab { min-height: 38px; padding: 0 18px; border: 1px solid var(--line-strong); border-radius: 999px; background: #fff; font-size: .875rem; font-weight: 600; color: var(--ink); transition: background-color .3s ease, color .3s ease, border-color .3s ease, box-shadow .3s ease; box-shadow: 0 1px 2px rgba(26,27,29,.05); }
.ctab:hover { border-color: var(--accent-deep); }
.ctab[aria-selected="true"] { background: var(--accent-deep); color: var(--bone); border-color: var(--accent-deep); }
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
      <picture><source media="(max-width: 767px)" srcset="assets/hero/slide-wallet-portrait.jpg"><img data-slide-img src="assets/hero/slide-wallet-1600.jpg" srcset="assets/hero/slide-wallet-900.jpg 900w, assets/hero/slide-wallet-1600.jpg 1600w, assets/hero/slide-wallet-2000.jpg 1672w" sizes="100vw" alt="Three Stagr wallets on dark marble: a black bifold standing, a brown bifold with the stag mark, and one open with cards" width="1672" height="941" fetchpriority="high" decoding="async"></picture>
      <div class="wrap slide-copy">
        <p class="hero-kicker" data-slide-item>Wallets <span aria-hidden="true">·</span> {n_wallets} pieces, from {fmt(min_wallet)}</p>
        <h1 class="hero-h1" data-slide-item><span class="serif-i">Folded, skived,</span><br>stitched by hand.</h1>
        <p class="hero-sub" data-slide-item>Bifolds, trifolds and long wallets, boxed with a handwritten note. Cash on delivery across Pakistan.</p>
        <div class="hero-ctas" data-slide-item><a class="btn btn--tan" href="wallets.html">Shop wallets {I["arrow"]}</a><a class="btn btn--ghost" href="shop.html">Everything</a></div>
      </div>
    </div>
    <div class="slide" data-slide="1" aria-roledescription="slide" aria-label="2 of 2" aria-hidden="true">
      <picture><source media="(max-width: 767px)" srcset="assets/hero/slide-belts-portrait.jpg"><img data-slide-img src="assets/hero/slide-belts-1600.jpg" srcset="assets/hero/slide-belts-900.jpg 900w, assets/hero/slide-belts-1600.jpg 1600w, assets/hero/slide-belts-2400.jpg 1672w" sizes="100vw" alt="Four Stagr belts on dark marble: a tan strap laid across the front, coils in black, tan and brown behind" width="1672" height="941" loading="lazy" decoding="async"></picture>
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
      <a class="btn btn--sm bulk-btn" href="bulk.html">Get a quote {I["arrow"]}</a>
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
      </div>
    </div>
    <div class="rail" data-rail>
      <div class="rail-track cc-track" data-rail-track data-shop-grid>{cards}</div>
    <div class="cc-foot"><p class="small muted"><span data-shop-count></span> shown · <a class="link" href="shop.html">View all pieces</a></p><div class="rail-nav" data-rail-nav><button type="button" class="rail-btn" data-rail-prev aria-label="Previous" style="transform:scaleX(-1)">{I["arrow"]}</button><button type="button" class="rail-btn" data-rail-next aria-label="Next">{I["arrow"]}</button></div></div>
    </div>
</section>

<section id="anatomy" class="anatomy on-bone" aria-labelledby="anatomy-title">
  <div class="wrap">
    <div class="inside-head" style="text-align:center"><h2 class="label" id="anatomy-title" data-reveal>Taken apart · every detail, named</h2><div class="inside-pills" data-reveal data-delay=".1">{an_pills}</div></div>
    {an_panels}
  </div>
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

<section id="promise" class="promise on-ink" aria-label="Stagr in a line">
  <div class="press-marquee" data-press-marquee aria-hidden="true">
    <div class="marquee"><div class="track" data-press-row="solid">{mq_solid}</div></div>
  </div>
</section>


<!-- feature tiles (how it is made / bulk / note) removed -->

<!-- range section hidden for now -->{ctx["why"](ctx)}

<!-- story section hidden for now -->

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

  /* ================= 03b ANATOMY ================= */
  function initAnatomy() {
    const section = $("#anatomy"); if (!section) return;
    const panels = $$("[data-an-panel]", section), pills = $$("[data-an-pill]", section); let active = 0, busy = false, entered = false;
    const desktop = () => window.matchMedia("(min-width: 1024px)").matches, NS = "http://www.w3.org/2000/svg";
    const route = (panel) => {
      const svg = $("[data-an-lines]", panel), body = $(".an-body", panel); svg.innerHTML = ""; if (!desktop()) return { paths: [], dots: [] };
      const br = body.getBoundingClientRect(); svg.setAttribute("viewBox", "0 0 " + br.width + " " + br.height);
      const boxes = { top: $("[data-an-top] .an-box", panel).getBoundingClientRect(), low: $("[data-an-low] .an-box", panel).getBoundingClientRect() };
      const paths = [], dots = [];
      $$("[data-an-call]", panel).forEach((call) => {
        const ir = boxes[call.dataset.anTarget], side = call.classList.contains("an-call--l") ? "l" : call.classList.contains("an-call--r") ? "r" : "low";
        const x1 = ir.left + ir.width * (+call.dataset.anX) / 100 - br.left, y1 = ir.top + ir.height * (+call.dataset.anY) / 100 - br.top;
        let x0, y0, d;
        if (side === "low") { const cr = $(".an-circle", call).getBoundingClientRect(); x0 = cr.left + cr.width / 2 - br.left; y0 = cr.top - 3 - br.top; const ky = y0 - (y0 - y1) * .5; d = "M" + x0 + " " + y0 + " L" + x0 + " " + ky + " L" + x1 + " " + y1; }
        else { const tr = $(".an-text", call).getBoundingClientRect(), cr = $(".an-circle", call).getBoundingClientRect(); const bt = $("b", call).getBoundingClientRect(); y0 = bt.bottom + 2 - br.top; x0 = (side === "l" ? tr.right + 6 : cr.left - 6) - br.left; const kx = x0 + (x1 - x0) * .45; d = "M" + x0 + " " + y0 + " L" + kx + " " + y0 + " L" + x1 + " " + y1; }
        const p = document.createElementNS(NS, "path"); p.setAttribute("d", d); svg.appendChild(p); paths.push(p);
        const c = document.createElementNS(NS, "circle"); c.setAttribute("cx", x1); c.setAttribute("cy", y1); c.setAttribute("r", 3.5); svg.appendChild(c); dots.push(c);
      });
      return { paths, dots };
    };
    const pieces = (panel) => ({ imgs: $$("[data-an-img]", panel), circles: $$(".an-circle", panel), texts: $$(".an-text", panel), head: $$(".an-head > *", panel), icons: $$("[data-an-icon]", panel), cta: $(".an-cta", panel) });
    const prime = (panel) => { const P = pieces(panel); G.set([...P.imgs, ...P.texts, ...P.head, ...P.icons, P.cta], { opacity: 0 }); G.set(P.circles, { scale: 0 }); };
    const play = (panel) => {
      const P = pieces(panel), L = route(panel);
      if (reduced) { G.set([...P.imgs, ...P.texts, ...P.head, ...P.icons, P.cta], { opacity: 1 }); G.set(P.circles, { scale: 1 }); G.set(L.paths, { drawSVG: "100%" }); busy = false; return; }
      G.set(L.dots, { scale: 0, transformOrigin: "50% 50%" });
      const tl = G.timeline({ defaults: { ease: "power3.out" }, onComplete: () => { busy = false; } });
      tl.fromTo(P.head, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .6, stagger: .08, clearProps: "transform" }, 0)
        .fromTo(P.imgs, { opacity: 0, y: 24, scale: .96 }, { opacity: 1, y: 0, scale: 1, duration: .9, stagger: .12, clearProps: "transform" }, .15)
        .fromTo(P.circles, { scale: 0 }, { scale: 1, duration: .6, ease: "back.out(1.8)", stagger: .07 }, .55);
      if (L.paths.length && window.DrawSVGPlugin) tl.fromTo(L.paths, { drawSVG: "0%" }, { drawSVG: "100%", duration: .55, ease: "power2.inOut", stagger: .07 }, .75);
      tl.to(L.dots, { scale: 1, duration: .35, ease: "back.out(3)", stagger: .07 }, 1.05)
        .fromTo(P.texts, { opacity: 0, x: (i, el) => el.closest(".an-call--l") ? -10 : el.closest(".an-call--r") ? 10 : 0, y: (i, el) => el.closest(".an-call--low") ? 8 : 0 }, { opacity: 1, x: 0, y: 0, duration: .5, stagger: .07, clearProps: "transform" }, .9)
        .fromTo(P.icons, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: .45, stagger: .05, clearProps: "transform" }, 1.5)
        .fromTo(P.cta, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: .45, clearProps: "transform" }, 1.8);
    };
    panels.forEach(prime);
    const setActive = (next) => {
      if (next === active || busy) return; busy = true; const prev = active; active = next; pills.forEach((p, i) => p.setAttribute("aria-pressed", String(i === next)));
      const out = panels[prev], P = pieces(out);
      G.to([...P.imgs, ...P.texts, ...P.head, ...P.icons, P.cta, ...$$("path, circle", $("[data-an-lines]", out))], { opacity: 0, duration: .22, ease: "power2.in", overwrite: "auto" });
      G.to(P.circles, { scale: 0, duration: .22, ease: "power2.in", overwrite: "auto", onComplete: () => { out.hidden = true; panels[next].hidden = false; prime(panels[next]); play(panels[next]); ST.refresh(); } });
    };
    pills.forEach((p, i) => p.addEventListener("click", () => setActive(i)));
    ST.create({ trigger: section, start: "top 60%", once: true, onEnter: () => { entered = true; busy = true; play(panels[active]); } });
    let rt = 0; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (!entered) return; const L = route(panels[active]); G.set(L.paths, { drawSVG: "100%" }); G.set(L.dots, { scale: 1, transformOrigin: "50% 50%" }); }, 120); });
    window.addEventListener("load", () => { if (entered) { const L = route(panels[active]); G.set(L.paths, { drawSVG: "100%" }); G.set(L.dots, { scale: 1, transformOrigin: "50% 50%" }); } });
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
    const marquee = $("[data-press-marquee]"), solid = $('[data-press-row="solid"]');
    if (reduced) return;
    const rows = [G.to(solid, { xPercent: -50, duration: 38, ease: "none", repeat: -1 })];
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
    tabs.forEach((t) => t.addEventListener("click", () => { if (t.dataset.tab === current) return; current = t.dataset.tab; tabs.forEach((x) => x.setAttribute("aria-selected", String(x === t))); grid.scrollTo({ left: 0, behavior: "auto" }); S.swapGrid(grid, () => filter(current)); }));
    filter("new");
    S.initCards(section);
  }

  /* ================= boot (top to bottom so pinned blocks measure in order) ================= */
  const startHero = initHero();
  initScrollHint(); S.initReveals($("#hero")); S.initReveals($("#explore")); initShop(); S.initReveals($("#shop")); initAnatomy(); S.initReveals($("#anatomy")); initInside(); S.initReveals($("#inside")); initPromise();
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
  if ($("#story")) { if (isMobile) initStoryMobile(); else initStoryDesktop(); }   // story hidden for now
  S.initReveals($("#why")); S.initReveals($("#story")); S.initReveals($("footer"));
  S.onLoaderDone.push(() => { startHero(); ST.refresh(); });
  // pinned sections measure once; re-measure after fonts and every image have settled so nothing pins early
  const again = () => ST.refresh();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(again);
  window.addEventListener("load", () => { again(); setTimeout(again, 600); });
  $$("img[loading=lazy]").forEach((im) => im.addEventListener("load", again, { once: true }));
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
