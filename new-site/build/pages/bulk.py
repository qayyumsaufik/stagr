"""bulk.html — bulk and corporate orders, in the same language as the home page.

Full-bleed photo hero; four points from the brand data; "Made for" tiles; the
range you can order; how it works in four steps; personalisation and packaging
cards; an enquiry form that sends the request on WhatsApp; "Why people choose
Stagr".
"""


def render(ctx):
    B = ctx["brand"]
    I = ctx["icon"]
    esc = ctx["esc"]
    P = ctx["products"]
    G = B["gifting"]
    fmt = lambda n: "Rs " + format(n, ",d")
    wa = B["contact"]["whatsapp"]["link"]
    belts = [p for p in P if p["line"] == "belt"]; wallets = [p for p in P if p["line"] == "wallet"]
    lo, hi = min(p["price"] for p in P), max(p["price"] for p in P)

    POINT_ICONS = [
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M13 8l3 3"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><rect x="3" y="8" width="18" height="12" rx="1"/><path d="M3 12h18M12 8v12M7 8V5h10v3"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17" r="1.6"/><circle cx="17" cy="17" r="1.6"/></svg>',
    ]
    points = "".join(f'<li class="bk-point" data-reveal data-delay="{i * .07}"><span class="bk-point-ic">{POINT_ICONS[i]}</span><b>{pt["title"]}</b><p>{pt["body"]}</p></li>' for i, pt in enumerate(G["points"]))

    made_for = [
        ("gifts", "Client gifts", "A belt or a wallet with your mark on it, boxed with a card. Something a client keeps on them."),
        ("teams", "Staff gifts", "One consignment for the whole team, the same piece in everyone's hands, or a mix of sizes and colours."),
        ("events", "Festive giving", "Eid, year end, a launch or a wedding. Tell us the date and we work back from it."),
    ]
    tiles = "".join(f'''<a class="bk-tile" href="#enquire" data-reveal data-delay="{i * .08}"><div class="bk-tile-copy"><h3>{t}</h3><p>{body}</p></div><div class="bk-tile-pic"><img src="assets/bulk/{k}-800.jpg" srcset="assets/bulk/{k}-800.jpg 800w, assets/bulk/{k}-1600.jpg 1600w" sizes="(min-width: 1024px) 32vw, 100vw" alt="{t}" width="1600" height="1200" loading="lazy" decoding="async"></div></a>''' for i, (k, t, body) in enumerate(made_for))

    range_cards = f'''
<a class="bk-range-card" href="shop.html?line=belts" data-reveal><img src="assets/categories/all-belts.jpg" srcset="assets/categories/all-belts.jpg 900w, assets/categories/all-belts-1400.jpg 1400w" sizes="(min-width: 1024px) 32vw, 100vw" alt="Stagr belts" width="1400" height="933" loading="lazy"><span><b>Belts</b><em>{len(belts)} styles · sizes 30 to 44 · from {fmt(min(p["price"] for p in belts))}</em></span></a>
<a class="bk-range-card" href="shop.html?line=wallets" data-reveal data-delay=".08"><img src="assets/categories/all-wallets.jpg" srcset="assets/categories/all-wallets.jpg 900w, assets/categories/all-wallets-1400.jpg 1400w" sizes="(min-width: 1024px) 32vw, 100vw" alt="Stagr wallets" width="1400" height="933" loading="lazy"><span><b>Wallets</b><em>{len(wallets)} styles · bifold, trifold, minimalist, long · from {fmt(min(p["price"] for p in wallets))}</em></span></a>
<a class="bk-range-card" href="shop.html" data-reveal data-delay=".16"><img src="assets/bulk/mix-800.jpg" srcset="assets/bulk/mix-800.jpg 800w, assets/bulk/mix-1600.jpg 1600w" sizes="(min-width: 1024px) 32vw, 100vw" alt="Two Stagr wallets beside the tools that made them" width="1600" height="1200" loading="lazy"><span><b>A mix</b><em>Belts and wallets together, prepared as one consignment</em></span></a>'''

    steps = [
        ("01", "Tell us what you need", "Pieces, quantity, colours and the date you need them by. Use the form below or message us on WhatsApp."),
        ("02", "A quote within one working day", "One price per piece, the same as the shop, with timing for your order confirmed in writing."),
        ("03", "Embossed, boxed, noted", "Your logo or initials pressed into the leather. Each piece boxed, with a handwritten or printed note."),
        ("04", "Delivered across Pakistan", "To one office or to several addresses, in one consignment with one invoice."),
    ]
    steps_html = "".join(f'<li class="bk-step" data-reveal data-delay="{i * .08}"><em>{n}</em><b>{t}</b><p>{b}</p></li>' for i, (n, t, b) in enumerate(steps))

    fields = f'''
<div class="bk-field"><label for="bk-name">Full name</label><input id="bk-name" name="name" type="text" autocomplete="name" required></div>
<div class="bk-field"><label for="bk-company">Company</label><input id="bk-company" name="company" type="text" autocomplete="organization"></div>
<div class="bk-field"><label for="bk-email">Email</label><input id="bk-email" name="email" type="email" autocomplete="email"></div>
<div class="bk-field"><label for="bk-phone">Phone</label><input id="bk-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="bk-field"><label for="bk-qty">Quantity</label><input id="bk-qty" name="quantity" type="number" min="10" step="1" placeholder="10 or more" required></div>
<div class="bk-field"><label for="bk-date">Needed by</label><input id="bk-date" name="date" type="date"></div>
<div class="bk-field bk-field--wide"><label for="bk-products">Products</label><select id="bk-products" name="products"><option>Belts</option><option>Wallets</option><option>Both</option></select></div>
<div class="bk-field bk-field--wide"><label for="bk-notes">Anything else</label><textarea id="bk-notes" name="notes" rows="4" placeholder="Logo or initials to emboss, colours, sizes, delivery addresses"></textarea></div>'''

    css = r'''
/* ---- hero ---- */
.chero { position: relative; height: clamp(460px, 64svh, 640px); overflow: hidden; background: var(--ink); color: var(--bone); display: flex; align-items: flex-end; }
.chero picture, .chero img { position: absolute; inset: 0; width: 100%; height: 100%; }
.chero img { object-fit: cover; object-position: 50% 55%; transform: scale(1.04); will-change: transform; }
.chero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(26,27,29,.5) 0%, rgba(26,27,29,0) 28%, rgba(26,27,29,0) 45%, rgba(26,27,29,.8) 100%), linear-gradient(90deg, rgba(26,27,29,.5) 0%, rgba(26,27,29,0) 60%); pointer-events: none; }
.chero-copy { position: relative; z-index: 2; width: 100%; padding-bottom: clamp(36px, 6vh, 64px); }
.chero-copy > * { max-width: 720px; }
.hero-kicker { font-size: .6875rem; letter-spacing: .3em; text-transform: uppercase; color: rgba(239,237,230,.8); }
.hero-h1 { margin-top: 12px; font-family: var(--font-display); font-weight: 500; font-size: clamp(2.2rem, 1.1rem + 3.2vw, 4.2rem); line-height: 1; text-shadow: 0 2px 30px rgba(0,0,0,.45); }
.hero-sub { margin-top: 18px; max-width: 48ch; font-size: clamp(.9375rem, .9rem + .25vw, 1.0625rem); line-height: 1.55; color: rgba(239,237,230,.88); text-shadow: 0 1px 14px rgba(0,0,0,.45); }
.hero-ctas { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
.btn--tan { background: var(--accent-deep); border-color: var(--accent-deep); color: var(--bone); }
.btn--tan:hover { background: var(--accent); border-color: var(--accent); color: var(--ink); }
.chero .btn--ghost { color: var(--bone); border-color: rgba(239,237,230,.55); background: rgba(26,27,29,.2); backdrop-filter: blur(6px); }
.chero .btn--ghost:hover { background: var(--bone); color: var(--ink); }
/* ---- points ---- */
.bk-points { padding: clamp(28px, 4vw, 48px) 0 0; }
.bk-points ul { display: grid; gap: 12px; grid-template-columns: 1fr; }
.bk-point { background: #fff; border-radius: 14px; padding: 20px 22px; box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 10px 30px -18px rgba(26,27,29,.18); }
.bk-point-ic { display: block; width: 26px; height: 26px; color: var(--accent-deep); margin-bottom: 14px; }
.bk-point-ic svg { width: 100%; height: 100%; }
.bk-point b { display: block; font-weight: 600; font-size: 1rem; }
.bk-point p { margin-top: 4px; font-size: .9375rem; line-height: 1.45; color: var(--fg-2); }
@media (min-width: 640px) { .bk-points ul { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1024px) { .bk-points ul { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; } }
/* ---- section heads ---- */
.bk-sec { padding: clamp(48px, 7vw, 96px) 0 0; }
.bk-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: clamp(20px, 3vw, 32px); }
.bk-head .explore-sub { max-width: 54ch; }
/* ---- made for tiles ---- */
.bk-tiles { display: grid; gap: 16px; grid-template-columns: 1fr; }
.bk-tile { position: relative; display: flex; flex-direction: column; overflow: hidden; border-radius: 14px; background: #F4F2EE; color: var(--ink); aspect-ratio: 4 / 4.6; box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 12px 30px -20px rgba(26,27,29,.2); transition: transform .4s var(--ease-out), box-shadow .4s ease; }
.bk-tile:hover { transform: translateY(-3px); box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 26px 44px -22px rgba(26,27,29,.28); }
.bk-tile-copy { padding: clamp(18px, 2.2vw, 24px) clamp(20px, 2.4vw, 26px) 16px; }
.bk-tile h3 { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.5rem, 1.1rem + 1.2vw, 2rem); line-height: 1.06; letter-spacing: -.012em; }
.bk-tile p { margin-top: 6px; font-size: .9375rem; line-height: 1.45; color: var(--fg-2); }
.bk-tile-pic { position: relative; flex: 1; min-height: 0; overflow: hidden; }
.bk-tile-pic img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transform: scale(1.02); transition: transform 1.1s var(--ease-out); }
.bk-tile:hover img { transform: scale(1.06); }
@media (min-width: 768px) { .bk-tiles { grid-template-columns: repeat(3, minmax(0, 1fr)); } .bk-tile { aspect-ratio: 4 / 5; } }
/* ---- the range ---- */
.bk-range { display: grid; gap: 16px; grid-template-columns: 1fr; }
.bk-range-card { position: relative; display: block; aspect-ratio: 4 / 3; border-radius: 14px; overflow: hidden; background: var(--ink); color: var(--bone); }
.bk-range-card img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transform: scale(1.02); transition: transform .9s var(--ease-out); }
.bk-range-card:hover img { transform: scale(1.07); }
.bk-range-card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(26,27,29,0) 40%, rgba(26,27,29,.78) 100%); }
.bk-range-card span { position: absolute; left: 20px; right: 20px; bottom: 18px; z-index: 2; display: grid; gap: 3px; }
.bk-range-card b { font-family: var(--font-display); font-weight: 300; font-size: 1.7rem; line-height: 1.05; }
.bk-range-card em { font-style: normal; font-size: .8125rem; color: rgba(239,237,230,.85); }
@media (min-width: 768px) { .bk-range { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
/* ---- how it works ---- */
.bk-steps { display: grid; gap: 22px; grid-template-columns: 1fr; }
.bk-step { border-top: 1px solid var(--line-strong); padding-top: 16px; }
.bk-step em { font-family: var(--font-display); font-style: normal; font-weight: 300; font-size: 1.9rem; line-height: 1; color: var(--accent-deep); }
.bk-step b { display: block; margin-top: 10px; font-weight: 600; font-size: 1rem; }
.bk-step p { margin-top: 6px; font-size: .9375rem; line-height: 1.5; color: var(--fg-2); }
@media (min-width: 640px) { .bk-steps { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1024px) { .bk-steps { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 28px; } }
/* ---- personalisation / packaging cards ---- */
.bk-card { display: grid; gap: 24px; background: #F4F2EE; border-radius: 18px; padding: clamp(22px, 3vw, 44px); }
.bk-card + .bk-card { margin-top: 16px; }
.bk-card .explore-title { font-size: clamp(1.7rem, 1.2rem + 1.6vw, 2.6rem); }
.bk-card .explore-sub { max-width: 54ch; font-size: 1rem; }
.bk-card .spec { margin-top: 22px; }
.bk-card .spec dd { font-weight: 500; max-width: 60%; }
.bk-photo { border-radius: 12px; overflow: hidden; aspect-ratio: 4 / 3; background: var(--ink); }
.bk-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
@media (min-width: 1024px) { .bk-card { grid-template-columns: 1fr 1fr; gap: clamp(28px, 4vw, 56px); align-items: center; } .bk-card--flip .bk-photo { order: -1; } }
/* ---- enquiry ---- */
.bk-enquire { padding: clamp(48px, 7vw, 96px) 0 0; }
.bk-form-card { display: grid; gap: 28px; background: #fff; border-radius: 18px; padding: clamp(22px, 3vw, 44px); box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 10px 30px -18px rgba(26,27,29,.18); }
.bk-form-intro .explore-title { font-size: clamp(1.7rem, 1.2rem + 1.6vw, 2.6rem); }
.bk-form-intro .explore-sub { font-size: 1rem; max-width: 40ch; }
.bk-form-intro ul { margin-top: 22px; display: grid; gap: 10px; font-size: .9375rem; }
.bk-form-intro li { display: flex; gap: 10px; align-items: flex-start; }
.bk-form-intro li::before { content: ""; flex: none; width: 6px; height: 6px; margin-top: 8px; background: var(--accent); }
.bk-form-intro .bk-alt { margin-top: 24px; font-size: .9375rem; color: var(--fg-2); }
.bk-form-intro .bk-alt a { color: var(--accent-deep); text-decoration: underline; text-underline-offset: 3px; }
.bk-form { display: grid; gap: 14px; grid-template-columns: 1fr; }
.bk-field { display: grid; gap: 6px; }
.bk-field label { font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; color: var(--fg-2); font-weight: 500; }
.bk-field input, .bk-field select, .bk-field textarea { width: 100%; min-height: 46px; padding: 10px 14px; border: 1px solid var(--line-strong); border-radius: 10px; background: #FBFAF7; color: var(--ink); font: inherit; font-size: .9375rem; transition: border-color .25s ease, box-shadow .25s ease; }
.bk-field textarea { min-height: 110px; resize: vertical; }
.bk-field input:focus, .bk-field select:focus, .bk-field textarea:focus { outline: none; border-color: var(--accent-deep); box-shadow: 0 0 0 3px rgba(139,74,31,.14); }
.bk-form-foot { display: grid; gap: 12px; margin-top: 6px; }
.bk-form-foot .btn { justify-self: start; }
.bk-form-foot p { font-size: .8125rem; color: var(--fg-2); }
.bk-form-foot [data-bk-status] { color: var(--success); font-weight: 500; min-height: 1.4em; }
@media (min-width: 640px) { .bk-form { grid-template-columns: 1fr 1fr; } .bk-field--wide { grid-column: 1 / -1; } .bk-form-foot { grid-column: 1 / -1; } }
@media (min-width: 1024px) { .bk-form-card { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: clamp(32px, 4vw, 64px); align-items: start; } }
@media (max-width: 767px) {
  .chero { height: 72svh; min-height: 500px; max-height: 660px; }
  .chero img { object-position: 50% 45%; }
  .chero::after { background: linear-gradient(180deg, rgba(26,27,29,.6) 0%, rgba(26,27,29,.05) 30%, rgba(26,27,29,.15) 48%, rgba(26,27,29,.86) 100%); }
  .chero-copy { padding-bottom: 56px; }
  .hero-ctas .btn { flex: 1 1 auto; justify-content: center; }
  .bk-head { flex-direction: column; align-items: flex-start; }
}
'''

    body = f'''
<section class="chero" aria-label="Bulk orders">
  <picture><source media="(max-width: 767px)" srcset="assets/bulk/hero-portrait.jpg"><img data-hero-img src="assets/bulk/hero-1600.jpg" srcset="assets/bulk/hero-1000.jpg 1000w, assets/bulk/hero-1600.jpg 1600w, assets/bulk/hero-2400.jpg 2400w" sizes="100vw" alt="Three Stagr belts, tan, black and brown, laid side by side on walnut" width="2400" height="1600" fetchpriority="high" decoding="async"></picture>
  <div class="wrap chero-copy">
    <p class="hero-kicker" data-hero-item>Bulk orders · 10 pieces or more</p>
    <h1 class="hero-h1" data-hero-item>One price,<br>any quantity.</h1>
    <p class="hero-sub" data-hero-item>{G["body"]} Embossed with your logo, boxed with a handwritten card.</p>
    <div class="hero-ctas" data-hero-item><a class="btn btn--tan" href="#enquire">Get a quote {I["arrow"]}</a><a class="btn btn--ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp us</a></div>
  </div>
</section>

<section class="bk-points on-bone" aria-label="What a bulk order includes">
  <div class="wrap"><ul role="list">{points}</ul></div>
</section>

<section class="bk-sec on-bone" aria-labelledby="bk-for-title">
  <div class="wrap">
    <div class="bk-head"><div><p class="label" data-reveal>Made for</p><h2 class="explore-title" id="bk-for-title" data-reveal data-delay=".05">Gifts people keep on them.</h2><p class="explore-sub" data-reveal data-delay=".1">A leather piece is used every day, so your mark is seen every day. That is the whole idea.</p></div></div>
    <div class="bk-tiles">{tiles}</div>
  </div>
</section>

<section class="bk-sec on-bone" aria-labelledby="bk-range-title">
  <div class="wrap">
    <div class="bk-head"><div><p class="label" data-reveal>What you can order</p><h2 class="explore-title" id="bk-range-title" data-reveal data-delay=".05">The whole range, at the shop price.</h2><p class="explore-sub" data-reveal data-delay=".1">{fmt(lo)} to {fmt(hi)} per piece. That is the whole range, and it is the same for a gift of one or an order of a hundred.</p></div><a class="btn btn--ghost" href="shop.html" data-reveal data-delay=".15">Browse everything {I["arrow"]}</a></div>
    <div class="bk-range">{range_cards}</div>
  </div>
</section>

<section class="bk-sec on-bone" aria-labelledby="bk-how-title">
  <div class="wrap">
    <div class="bk-head"><div><p class="label" data-reveal>How it works</p><h2 class="explore-title" id="bk-how-title" data-reveal data-delay=".05">Four steps, one consignment.</h2></div></div>
    <ol class="bk-steps" role="list">{steps_html}</ol>
  </div>
</section>

<section class="bk-sec on-bone" aria-labelledby="bk-mark-title">
  <div class="wrap">
    <div class="bk-card">
      <div>
        <p class="label" data-reveal>Personalisation</p>
        <h2 class="explore-title" id="bk-mark-title" data-reveal data-delay=".05">Your mark, pressed into the leather.</h2>
        <p class="explore-sub" data-reveal data-delay=".1">{B["customisation"]} A logo sits best on the tail of a belt or the front of a wallet, pressed without foil so it ages with the hide.</p>
        <dl class="spec" data-reveal data-delay=".15"><div><dt>Embossing</dt><dd>Your logo or initials</dd></div><div><dt>Placement</dt><dd>Belt tail or wallet front</dd></div><div><dt>Colours</dt><dd>Brown, Black, Tan</dd></div><div><dt>Minimum</dt><dd>10 pieces, belts, wallets or a mix</dd></div></dl>
      </div>
      <figure class="bk-photo" data-reveal data-delay=".1"><img src="assets/bulk/mark-800.jpg" srcset="assets/bulk/mark-800.jpg 800w, assets/bulk/mark-1600.jpg 1600w" sizes="(min-width: 1024px) 45vw, 100vw" alt="The Stagr stag pressed into the tail of a tan belt" width="1600" height="1200" loading="lazy"></figure>
    </div>
    <div class="bk-card bk-card--flip">
      <div>
        <p class="label" data-reveal>Packaging</p>
        <h2 class="explore-title" data-reveal data-delay=".05">Gift-ready, every box.</h2>
        <p class="explore-sub" data-reveal data-delay=".1">{B["handwrittenNote"]["body"]} For a bulk order we can write one message for every box or a different one for each name.</p>
        <dl class="spec" data-reveal data-delay=".15"><div><dt>Box</dt><dd>Each piece boxed</dd></div><div><dt>Note</dt><dd>Handwritten or printed</dd></div><div><dt>Delivery</dt><dd>One office or several addresses</dd></div><div><dt>Invoice</dt><dd>One consignment, one invoice</dd></div></dl>
      </div>
      <figure class="bk-photo" data-reveal data-delay=".1"><img src="assets/bulk/boxed-800.jpg" srcset="assets/bulk/boxed-800.jpg 800w, assets/bulk/boxed-1600.jpg 1600w" sizes="(min-width: 1024px) 45vw, 100vw" alt="A Stagr wallet on its box" width="1600" height="1200" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="bk-enquire on-bone" id="enquire" aria-labelledby="bk-enquire-title">
  <div class="wrap">
    <div class="bk-form-card">
      <div class="bk-form-intro">
        <p class="label" data-reveal>Get a quote</p>
        <h2 class="explore-title" id="bk-enquire-title" data-reveal data-delay=".05">Tell us what you need.</h2>
        <p class="explore-sub" data-reveal data-delay=".1">We reply within one working day with a price per piece and a date.</p>
        <ul data-reveal data-delay=".15"><li>Belts, wallets or a mix, ten pieces or more</li><li>Embossing with your logo or initials</li><li>Boxed, with a handwritten or printed note</li><li>Delivered across Pakistan, cash on delivery</li></ul>
        <p class="bk-alt" data-reveal data-delay=".2">Prefer to talk? <a href="{wa}" target="_blank" rel="noopener">Message us on WhatsApp</a> or call {B["contact"]["phone"]["value"]}.</p>
      </div>
      <form class="bk-form" data-bk-form novalidate>
        {fields}
        <div class="bk-form-foot">
          <button type="submit" class="btn btn--tan">Send the request {I["arrow"]}</button>
          <p>This opens WhatsApp with your request filled in. Nothing is sent until you press send there.</p>
          <p data-bk-status aria-live="polite"></p>
        </div>
      </form>
    </div>
  </div>
</section>

{ctx["why"](ctx)}
'''

    js = r'''
function initBulk() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, reduced = S.reduced;
  const img = $("[data-hero-img]"), items = $$("[data-hero-item]");
  if (G && !reduced) G.set(items, { y: 18, opacity: 0 });
  S.onLoaderDone.push(() => { if (!G || reduced) return; G.fromTo(img, { scale: 1.14 }, { scale: 1.04, duration: 2.6, ease: "power2.out", clearProps: "transform" }); G.to(items, { y: 0, opacity: 1, duration: .7, ease: "power3.out", stagger: .08, delay: .2, clearProps: "transform" }); });
  $$(".bk-points, .bk-sec, .bk-enquire, #why, footer").forEach((el) => S.initReveals(el));
  $$('a[href^="#"]').forEach((a) => a.addEventListener("click", (e) => { const el = $(a.getAttribute("href")); if (!el) return; e.preventDefault(); S.scrollTo(el, 1.1); }));
  const form = $("[data-bk-form]"), status = $("[data-bk-status]");
  if (form) form.addEventListener("submit", (e) => {
    e.preventDefault();
    const v = (n) => (form.elements[n].value || "").trim();
    const missing = ["name", "phone", "quantity"].filter((n) => !v(n));
    if (missing.length) { status.style.color = "var(--error)"; status.textContent = "Please add your name, phone and quantity."; form.elements[missing[0]].focus(); return; }
    const lines = ["Hello Stagr, I would like a quote for a bulk order.", "Name: " + v("name"), v("company") ? "Company: " + v("company") : "", "Phone: " + v("phone"), v("email") ? "Email: " + v("email") : "", "Products: " + v("products"), "Quantity: " + v("quantity"), v("date") ? "Needed by: " + v("date") : "", v("notes") ? "Notes: " + v("notes") : ""].filter(Boolean);
    window.open(S.data.brand.whatsapp + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    status.style.color = ""; status.textContent = "Your request is ready in WhatsApp. Press send there and we reply within one working day.";
  });
  window.addEventListener("load", () => ST && ST.refresh());
}
STAGR.onReady.push(initBulk);
'''

    return {
        "file": "bulk.html",
        "key": "bulk",
        "title": "Bulk orders — STAGR.",
        "description": "Bulk and corporate orders of Stagr belts and wallets. Ten pieces or more, embossed with your logo, boxed with a handwritten card, delivered across Pakistan.",
        "css": css,
        "body": body,
        "js": js,
        "header_dark": True,
        "shop_href": "shop.html",
    }
