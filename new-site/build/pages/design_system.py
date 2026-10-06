"""design-system.html — tokens, type scale, components and animation primitives."""


def render(ctx):
    P = ctx["products"]
    I = ctx["icon"]
    wallet = next(p for p in P if p["id"] == "kingsmann")
    belt = next(p for p in P if p["id"] == "monarch")
    rodeo = next(p for p in P if p["id"] == "rodeo")

    def card(p, badge=None):
        a, b = p["images"][0], p["images"][1]
        return f'''
<a class="card" href="product.html?id={p["id"]}" data-cursor="View">
  <div class="media media--studio">
    <img src="{a["src"]}" alt="{a["alt"]}" width="{a["width"]}" height="{a["height"]}" loading="lazy">
    <img class="alt" src="{b["src"]}" alt="" width="{b["width"]}" height="{b["height"]}" loading="lazy" aria-hidden="true">
    {f'<span class="badge">{badge}</span>' if badge else ''}
    <button type="button" class="btn btn--sm btn--wide quick" data-add="{p["id"]}" data-colour="{p["defaultColour"]}">Add to cart</button>
  </div>
  <div class="card-body">
    <div><div class="card-name">{p["name"]}</div><div class="card-meta">{p["style"] or "Belt"} · {" / ".join(p["colours"])}</div><div class="card-rule"></div></div>
    <div class="price">{ctx["esc"]("Rs " + format(p["price"], ",d"))}<s>{"Rs " + format(p["compareAtPrice"], ",d")}</s></div>
  </div>
</a>'''

    swatch_rows = [
        ("Background", "--c-offwhite", "#F6F2EC"), ("Espresso", "--c-espresso", "#1E1612"),
        ("Cognac", "--c-cognac", "#8B4A1F"), ("Saddle tan", "--c-saddle", "#C58B4A"),
        ("Oxblood", "--c-oxblood", "#5C1F1F"), ("Ink", "--c-ink", "#161311"),
    ]
    swatches = "".join(f'<div class="sw-cell"><div class="sw-chip" style="background:{hx}"></div><div class="small"><strong>{n}</strong><br><code>{v}</code> {hx}</div></div>' for n, v, hx in swatch_rows)
    fn_rows = [("Accent / links", "--accent"), ("Accent soft (rules, cues)", "--accent-soft"), ("Focus ring", "--focus"), ("Success", "--success"), ("Error", "--error"), ("Line", "--line-strong"), ("Surface 2", "--bg-2"), ("Button", "--btn-bg")]
    fn = "".join(f'<div class="sw-cell"><div class="sw-chip" style="background:var({v})"></div><div class="small"><strong>{n}</strong><br><code>{v}</code></div></div>' for n, v in fn_rows)

    css = r'''
.ds-section { padding-block: var(--section-sm); border-top: 1px solid var(--line); }
.ds-head { display: grid; gap: 12px; margin-bottom: 40px; }
.ds-head .h2 { max-width: 20ch; }
.sw-grid { display: grid; gap: 20px; grid-template-columns: repeat(2, minmax(0,1fr)); }
@media (min-width: 768px) { .sw-grid { grid-template-columns: repeat(3, minmax(0,1fr)); } }
@media (min-width: 1024px) { .sw-grid { grid-template-columns: repeat(6, minmax(0,1fr)); } }
.sw-cell { display: grid; gap: 10px; }
.sw-chip { aspect-ratio: 4 / 3; border-radius: var(--radius); border: 1px solid var(--line); }
.ds-panel { padding: clamp(24px, 4vw, 48px); border-radius: var(--radius); }
.type-row { display: grid; gap: 8px; padding: 20px 0; border-bottom: 1px solid var(--line); }
.type-row .small { color: var(--ink-3); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.grid-demo > div { background: var(--bg-2); min-height: 48px; display: grid; place-items: center; font-size: var(--fs-small); color: var(--ink-3); }
.demo-row { display: flex; flex-wrap: wrap; gap: 16px; align-items: center; }
.demo-box { position: relative; border: 1px dashed var(--line-strong); border-radius: var(--radius); padding: clamp(20px, 4vw, 48px); display: grid; gap: 20px; }
.demo-box .replay { justify-self: start; }
.ds-cards { display: grid; gap: var(--gap); grid-template-columns: repeat(2, minmax(0,1fr)); }
@media (min-width: 1024px) { .ds-cards { grid-template-columns: repeat(4, minmax(0,1fr)); } }
.ds-doors { display: grid; gap: var(--gap); grid-template-columns: 1fr; }
@media (min-width: 768px) { .ds-doors { grid-template-columns: 1fr 1fr; } }
.cursor-zone { display: grid; place-items: center; min-height: 180px; background: var(--bg-2); border-radius: var(--radius); font-size: var(--fs-small); color: var(--ink-2); }
.motion-table { width: 100%; border-collapse: collapse; font-size: var(--fs-small); }
.motion-table th, .motion-table td { text-align: left; padding: 12px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
.motion-table th { font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--ink-2); }
.px-demo { display: grid; gap: var(--gap); grid-template-columns: repeat(3, minmax(0,1fr)); }
.px-demo .media { --ar: 3 / 4; }
.px-demo .media:nth-child(2) { margin-top: 48px; }
.loader-demo { position: relative; height: 260px; overflow: hidden; border-radius: var(--radius); }
.loader-demo .loader { position: absolute; }
'''

    body = f'''
<section class="section" style="padding-top:calc(var(--header-h) + var(--section-sm))">
  <div class="wrap">
    <p class="label label-row" data-reveal="up">Stagr · design system v1</p>
    <h1 class="display" data-lines="now" style="margin-top:24px">Quiet surfaces, <em class="i">warm</em> leather, slow reveals.</h1>
    <p class="lead" data-reveal="up" data-delay=".4" style="margin-top:32px">Every page is built from these tokens, components and animation primitives. Toggle the theme in the header to check the dark variant. Resize to check the fluid scale.</p>
  </div>
</section>

<section class="ds-section" id="colour">
  <div class="wrap">
    <div class="ds-head"><p class="label">01 · Colour</p><h2 class="h2">Palette and functional tokens</h2><p class="muted body">Backgrounds and text are fixed by the brief. Links use cognac on light (5.9:1) and a lighter saddle on dark (8.1:1). Saddle tan is never used for body text; it carries rules, cues and hover fills.</p></div>
    <div class="sw-grid">{swatches}</div>
    <div class="sw-grid" style="margin-top:32px">{fn}</div>
    <div class="grid" style="margin-top:40px">
      <div class="col-12 md:col-6 ds-panel theme-light" style="border:1px solid var(--line)"><p class="label">Light surface</p><p class="h3" style="margin-top:12px">Carried daily.</p><p class="muted" style="margin-top:8px">Body text on off-white. <a class="link" href="#">A cognac link.</a></p><p style="margin-top:16px"><button class="btn btn--sm">Add to cart</button> <button class="btn btn--ghost btn--sm">Quick view</button></p></div>
      <div class="col-12 md:col-6 ds-panel theme-dark"><p class="label">Dark surface</p><p class="h3" style="margin-top:12px">Made slowly.</p><p class="muted" style="margin-top:8px">Body text on espresso. <a class="link" href="#">A saddle link.</a></p><p style="margin-top:16px"><button class="btn btn--sm">Add to cart</button> <button class="btn btn--ghost btn--sm">Quick view</button></p></div>
      <div class="col-12 ds-panel theme-oxblood"><p class="label">Oxblood tint — used sparingly as a section accent</p><p class="h3" style="margin-top:12px">A handwritten note, in every order.</p></div>
    </div>
  </div>
</section>

<section class="ds-section" id="type">
  <div class="wrap">
    <div class="ds-head"><p class="label">02 · Typography</p><h2 class="h2">Fraunces for the voice, Manrope for the work</h2><p class="muted body">Display sizes use the 144 optical size with soft serifs. Everything else is Manrope. Minimum size anywhere is 14px; body runs 16 to 18px.</p></div>
    <div class="type-row"><div class="display">Nothing but leather</div><div class="small">.display · clamp(2.75rem, 1.6rem + 5.4vw, 7.5rem) · lh 1.02</div></div>
    <div class="type-row"><div class="h1">We cut leather, not corners</div><div class="small">.h1 · clamp(2.5rem, 1.5rem + 4.2vw, 5.75rem)</div></div>
    <div class="type-row"><div class="h2">Two lines. One workshop.</div><div class="small">.h2 · clamp(2rem, 1.3rem + 2.8vw, 4rem)</div></div>
    <div class="type-row"><div class="h3">Crazy horse leather, stitched by hand</div><div class="small">.h3 · clamp(1.5rem, 1.2rem + 1.3vw, 2.375rem)</div></div>
    <div class="type-row"><div class="h4">Kingsmann Bifold Leather Wallet</div><div class="small">.h4 · card names, drawer items</div></div>
    <div class="type-row"><p class="lead">Belts and wallets cut from full hides by local artisans. Pay cash on delivery, anywhere in Pakistan.</p><div class="small">.lead · clamp(1.125rem, 1rem + .55vw, 1.4rem)</div></div>
    <div class="type-row"><p class="body">Every piece is cut from full hides by local artisans. The waxed surface marks and darkens with use, so no two pieces age the same way. Keep it dry and away from direct heat.</p><div class="small">.body · 16–18px · max 60ch</div></div>
    <div class="type-row"><p class="small">Three to five working days across Pakistan. Cash on delivery available.</p><div class="small">.small · 14px</div></div>
    <div class="type-row"><p class="label">Micro label · 14px uppercase</p><p class="label label-row" style="margin-top:8px">With rule</p><div class="small">.label / .label-row</div></div>
    <div class="type-row"><p class="h3">Regular, <em class="i">italic light</em>, and <span class="price">Rs 2,600<s>Rs 3,999</s></span></p><div class="small">.i · .price with compare-at</div></div>
  </div>
</section>

<section class="ds-section" id="layout">
  <div class="wrap">
    <div class="ds-head"><p class="label">03 · Layout</p><h2 class="h2">Twelve columns, generous air</h2><p class="muted body">Max width 1440px. Gutters 24px on phones growing to 64px on desktop. Section rhythm clamps between 96px and 200px. Images sit in fixed aspect-ratio boxes so nothing shifts while they load.</p></div>
    <div class="grid grid-demo">{"".join('<div>' + str(i + 1) + '</div>' for i in range(12))}</div>
    <div class="grid" style="margin-top:var(--gap)">
      <div class="col-12 md:col-4 media ar-45 reveal-img"><img src="{belt["images"][0]["src"]}" alt="{belt["images"][0]["alt"]}" width="1200" height="896" loading="lazy" style="object-fit:cover"></div>
      <div class="col-12 md:col-8 media ar-169 reveal-img" data-from="left"><img src="assets/lifestyle/belts-lineup.jpg" alt="Four Stagr belts hanging on wood" width="2400" height="1600" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="ds-section" id="buttons">
  <div class="wrap">
    <div class="ds-head"><p class="label">04 · Buttons</p><h2 class="h2">One solid, the rest flat</h2><p class="muted body">Primary is the only filled button. Hover sweeps a cognac fill upward. Magnetic buttons follow the cursor within 40px and snap back.</p></div>
    <div class="demo-row">
      <button class="btn" data-magnetic><span class="btn-label">Add to cart</span></button>
      <button class="btn btn--lg" data-magnetic><span class="btn-label">Shop belts</span>{I["arrow"]}</button>
      <button class="btn btn--sm">Quick view</button>
      <button class="btn btn--ghost" data-magnetic><span class="btn-label">View all</span></button>
      <button class="btn btn--flat">Size guide</button>
      <button class="btn btn--icon" aria-label="Next">{I["arrow-r"]}</button>
      <button class="btn" disabled>Sold out</button>
    </div>
    <div class="demo-row theme-dark ds-panel" style="margin-top:24px">
      <button class="btn" data-magnetic><span class="btn-label">Add to cart</span></button>
      <button class="btn btn--ghost">View all</button>
      <button class="btn btn--flat">Size guide</button>
      <button class="btn btn--icon" aria-label="Next">{I["arrow-r"]}</button>
    </div>
  </div>
</section>

<section class="ds-section" id="forms">
  <div class="wrap">
    <div class="ds-head"><p class="label">05 · Inputs and selection</p><h2 class="h2">Underlines, pills, swatches</h2></div>
    <div class="grid">
      <div class="col-12 md:col-6 stack" style="--stack:24px">
        <div class="field"><label for="f1">Full name</label><input class="input" id="f1" placeholder="Your name"></div>
        <div class="field"><label for="f2">Email</label><input class="input" id="f2" type="email" placeholder="you@example.com" aria-invalid="true" aria-describedby="f2e"><span class="error" id="f2e">Please add a valid email address.</span></div>
        <div class="field"><label for="f3">City</label><select class="select" id="f3"><option>Karachi</option><option>Lahore</option><option>Islamabad</option></select></div>
        <div class="field"><label for="f4">Handwritten note</label><textarea class="textarea" id="f4" placeholder="We write it by hand on a card and pack it with your order."></textarea><span class="hint">0 of 160 characters</span></div>
        <label class="check"><input type="checkbox" checked> Keep me posted on new cuts</label>
      </div>
      <div class="col-12 md:col-6 stack" style="--stack:32px">
        <div><p class="label" style="margin-bottom:12px">Filter pills</p><div class="pills"><button class="pill" aria-pressed="true">All</button><button class="pill" aria-pressed="false"><span class="dot" style="--sw:#7B4A2B"></span>Brown</button><button class="pill" aria-pressed="false"><span class="dot" style="--sw:#14100E"></span>Black</button><button class="pill" aria-pressed="false"><span class="dot" style="--sw:#B0773F"></span>Tan</button><button class="pill" aria-pressed="false">Under Rs 2,000</button></div></div>
        <div><p class="label" style="margin-bottom:12px">Segmented tabs</p><div class="seg" data-seg><div class="seg-thumb"></div><button type="button" role="tab" aria-selected="true" data-tab="materials">Materials</button><button type="button" role="tab" aria-selected="false" data-tab="dimensions">Dimensions</button><button type="button" role="tab" aria-selected="false" data-tab="care">Care</button></div></div>
        <div><p class="label" style="margin-bottom:12px">Colour · <span class="muted" style="text-transform:none;letter-spacing:0">Brown</span></p><div class="swatches"><label class="swatch" style="--sw:#7B4A2B"><input type="radio" name="sw" checked><span class="sw"></span><span class="sr-only">Brown</span></label><label class="swatch" style="--sw:#14100E"><input type="radio" name="sw"><span class="sw"></span><span class="sr-only">Black</span></label><label class="swatch" style="--sw:#B0773F"><input type="radio" name="sw"><span class="sw"></span><span class="sr-only">Tan</span></label></div></div>
        <div><p class="label" style="margin-bottom:12px">Waist size</p><div class="sizes">{"".join(f'<label class="size"><input type="radio" name="sz" {"checked" if s == 34 else ""}>{s}</label>' for s in [30, 32, 34, 36, 38, 40, 42])}<label class="size is-out"><input type="radio" name="sz" disabled>44</label></div></div>
        <div class="demo-row"><div class="qty"><button type="button" aria-label="Decrease">−</button><span>1</span><button type="button" aria-label="Increase">+</button></div><span class="chip">Brown ×</span><span class="badge">New</span><span class="badge badge--solid">Bestseller</span><span class="badge badge--tint">Save 35%</span></div>
      </div>
    </div>
  </div>
</section>

<section class="ds-section" id="cards">
  <div class="wrap">
    <div class="ds-head"><p class="label">06 · Cards</p><h2 class="h2">Let the object speak</h2><p class="muted body">Studio shots sit on a warm grey plate with multiply blending so the white renders sit in the palette. Hover crossfades to the second view and raises the quick-add. Cards reveal with a stagger on scroll.</p></div>
    <div class="ds-cards" data-stagger=".08">{card(wallet, "Bestseller")}{card(belt)}{card(rodeo, "Long wallet")}{card(P[6])}</div>
    <div class="ds-doors" style="margin-top:var(--section-sm)">
      <a class="door" href="wallets.html" data-cursor="Wallets"><div class="media"><img src="assets/lifestyle/kingsmen-01.jpg" alt="Kingsmann bifold on sherpa" width="1200" height="1500" loading="lazy"></div><div class="door-body"><p class="label" style="color:var(--c-saddle)">01 · Seven styles</p><div class="door-title">Wallets</div><div class="door-rule"></div><span class="label">Shop wallets {I["arrow"]}</span></div></a>
      <a class="door" href="belts.html" data-cursor="Belts"><div class="media"><img src="assets/lifestyle/ranger-open.jpg" alt="Tan belt buckle on wood" width="1800" height="1200" loading="lazy"></div><div class="door-body"><p class="label" style="color:var(--c-saddle)">02 · Four styles</p><div class="door-title">Belts</div><div class="door-rule"></div><span class="label">Shop belts {I["arrow"]}</span></div></a>
    </div>
  </div>
</section>

<section class="ds-section" id="content">
  <div class="wrap">
    <div class="ds-head"><p class="label">07 · Content blocks</p><h2 class="h2">Accordion and trust strip</h2></div>
    <div class="grid">
      <div class="col-12 md:col-6">
        <div class="acc">
          <details open><summary>Product details<span class="plus"></span></summary><div class="acc-body"><p>{belt["details"]["productDetails"]}</p></div></details>
          <details><summary>Leather specification<span class="plus"></span></summary><div class="acc-body"><p>{belt["details"]["leatherSpecification"]}</p></div></details>
          <details><summary>Care<span class="plus"></span></summary><div class="acc-body"><p>{belt["details"]["care"]}</p></div></details>
          <details><summary>Delivery and returns<span class="plus"></span></summary><div class="acc-body"><p>{belt["details"]["deliveryAndReturns"]}</p></div></details>
        </div>
      </div>
      <div class="col-12 md:col-6">
        <div class="trust" style="grid-template-columns:repeat(2,minmax(0,1fr))">
          {"".join(f'<div class="trust-item"><span class="t">{t["title"]}</span><span class="s">{t["sub"]}</span></div>' for t in ctx["brand"]["trust"]["items"])}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="ds-section" id="motion">
  <div class="wrap">
    <div class="ds-head"><p class="label">08 · Animation primitives</p><h2 class="h2">Slow, masked, never bouncy</h2><p class="muted body">All motion animates only transform, opacity and clip-path. Entrances fire once at <code>top 80%</code>. Reduced-motion users get plain fades and no pinning, scrubbing or parallax.</p></div>
    <div class="grid">
      <div class="col-12 md:col-6 demo-box" id="demo-lines">
        <p class="label">Text reveal · SplitText lines, yPercent 100 → 0 in a mask</p>
        <h3 class="h2" data-lines>Cut once. Worn for years, then handed down.</h3>
        <button type="button" class="btn btn--sm btn--ghost replay" data-replay="lines">Replay</button>
      </div>
      <div class="col-12 md:col-6 demo-box" id="demo-img">
        <p class="label">Image reveal · clip-path inset from a side + scale 1.15 → 1</p>
        <div class="media ar-32 reveal-img" data-from="left"><img src="assets/lifestyle/onyx-02.jpg" alt="Black belt buckle with coffee beans" width="1200" height="1500" loading="lazy"></div>
        <button type="button" class="btn btn--sm btn--ghost replay" data-replay="img">Replay</button>
      </div>
      <div class="col-12 md:col-6 demo-box" id="demo-fade">
        <p class="label">Block reveal · opacity + 32px rise, staggered 0.08s</p>
        <div data-stagger=".08" class="stack" style="--stack:12px"><p class="h4">One workshop.</p><p class="h4">One price.</p><p class="h4">No filler.</p><p class="h4">Repairs for life.</p></div>
        <button type="button" class="btn btn--sm btn--ghost replay" data-replay="fade">Replay</button>
      </div>
      <div class="col-12 md:col-6 demo-box">
        <p class="label">Cursor labels · hover these zones (desktop)</p>
        <div class="cursor-zone" data-cursor="View">Hover → “View”</div>
        <div class="cursor-zone" data-cursor="Drag">Hover → “Drag”</div>
      </div>
      <div class="col-12 demo-box">
        <p class="label">Parallax · three speeds, scrub 0.8 (scroll to see)</p>
        <div class="px-demo">
          <div class="media" data-parallax=".15"><img src="assets/lifestyle/heritage-01.jpg" alt="Tan belt coiled on wood" width="1200" height="1500" loading="lazy"></div>
          <div class="media" data-parallax=".35"><img src="assets/lifestyle/majestic-02.jpg" alt="Dark wallet on burlap" width="1200" height="1500" loading="lazy"></div>
          <div class="media" data-parallax=".25"><img src="assets/lifestyle/ranger-02.jpg" alt="Tan belt tip with embossed stag" width="1200" height="1500" loading="lazy"></div>
        </div>
      </div>
      <div class="col-12 demo-box" style="padding-inline:0;overflow:hidden">
        <p class="label" style="padding-inline:clamp(20px,4vw,48px)">Marquee · 60px/s, pauses off-screen, speeds up with scroll velocity</p>
        <div class="marquee" data-marquee data-speed="60" data-scrub><div class="track">{"".join(f'<span class="label">{t}</span><span class="label" style="color:var(--accent-soft)">·</span>' for t in ctx["brand"]["ticker"])}</div></div>
      </div>
      <div class="col-12 md:col-6 demo-box">
        <p class="label">Page transition · curtain wipe (≤1.1s)</p>
        <p class="muted small">Every internal link plays a curtain out, navigates, then the next page lifts the curtain on load. Try it:</p>
        <p><a class="btn btn--ghost btn--sm" href="design-system.html">Reload through the curtain</a> <button type="button" class="btn btn--sm" data-replay="curtain">Preview without leaving</button></p>
      </div>
      <div class="col-12 md:col-6 demo-box">
        <p class="label">Intro loader · ≤1.8s, once per session, skippable</p>
        <div class="loader-demo"><div class="loader" id="loader-demo" aria-hidden="true"><div class="grain"></div><div class="mark"><img src="assets/brand/stagr-lockup-brass.png" alt="" width="538" height="392"></div><div class="count">000</div><div class="word">Nothing but leather</div><div class="bar"></div></div></div>
        <button type="button" class="btn btn--sm btn--ghost replay" data-replay="loader">Replay</button>
      </div>
    </div>
    <div class="table-wrap" style="margin-top:48px"><table class="motion-table">
      <thead><tr><th>Use</th><th>Ease</th><th>Duration</th><th>Stagger</th></tr></thead>
      <tbody>
        <tr><td>Micro-interactions (hover fills, pills, swatches)</td><td>power3.out / cubic-bezier(.22,1,.36,1)</td><td>0.3–0.5s</td><td>—</td></tr>
        <tr><td>Entrances (lines, blocks, cards)</td><td>power3.out</td><td>0.9–1.2s</td><td>0.06–0.12s</td></tr>
        <tr><td>Large image reveals</td><td>expo.out</td><td>1.4s</td><td>—</td></tr>
        <tr><td>Menu, drawer, curtain, loader lift</td><td>power2.inOut / power3.inOut</td><td>0.6–1.1s</td><td>0.08s (menu links)</td></tr>
        <tr><td>Scroll-driven (parallax, pinned story, marquee velocity)</td><td>none</td><td>scrub: 0.8</td><td>—</td></tr>
        <tr><td>Hover image zoom</td><td>power3.out</td><td>0.8s · scale 1 → 1.05</td><td>—</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="ds-section" id="chrome">
  <div class="wrap">
    <div class="ds-head"><p class="label">09 · Chrome</p><h2 class="h2">Header, split menu, bag, footer</h2><p class="muted body">All live on this page. The header turns solid after 24px of scroll and hides on fast downward scroll. The menu opens as two half-screen panels sliding from top and bottom, links stagger in, and it closes in reverse at 1.6× speed. The bag slides in from the right; try “Add to cart” on a card above.</p></div>
    <div class="demo-row"><button type="button" class="btn" data-menu-open-demo>Open the menu</button><button type="button" class="btn btn--ghost" data-cart-open>Open the bag</button><button type="button" class="btn btn--ghost theme-toggle">Toggle theme</button></div>
  </div>
</section>
'''

    js = r'''
function initAnimations() {
  const S = window.STAGR, G = S.gsap;
  const seg = document.querySelector("[data-seg]"); if (seg) S.segmented(seg);
  const demoMenu = document.querySelector("[data-menu-open-demo]"); demoMenu && demoMenu.addEventListener("click", S.openMenu);
  document.querySelectorAll("form[data-newsletter]").forEach(f => f.addEventListener("submit", e => { e.preventDefault(); S.toast("You are on the list."); f.reset(); }));
  if (!G || S.reduced) return;

  document.querySelectorAll("[data-replay]").forEach(btn => btn.addEventListener("click", () => {
    const k = btn.dataset.replay;
    if (k === "lines") {
      const el = document.querySelector("#demo-lines [data-lines]");
      G.fromTo(el.querySelectorAll(".line"), { yPercent: 105 }, { yPercent: 0, duration: 1.2, ease: S.ease.in, stagger: .09, overwrite: true });
    }
    if (k === "img") {
      const img = document.querySelector("#demo-img img");
      G.fromTo(img, { clipPath: "inset(0 100% 0 0)", scale: 1.15 }, { clipPath: "inset(0 0% 0 0)", scale: 1, duration: 1.4, ease: S.ease.big, overwrite: true });
    }
    if (k === "fade") {
      G.fromTo("#demo-fade [data-stagger] > *", { opacity: 0, y: 32 }, { opacity: 1, y: 0, duration: 1, stagger: .08, ease: S.ease.in, overwrite: true });
    }
    if (k === "curtain") {
      const c = document.querySelector(".curtain"), svg = c.querySelector("svg");
      G.timeline().to(c, { y: "0%", duration: .7, ease: "power2.inOut" }).fromTo(svg, { opacity: 0, scale: .9 }, { opacity: 1, scale: 1, duration: .3 }, "-=.2").to(svg, { opacity: 0, duration: .2 }, "+=.3").to(c, { y: "-101%", duration: .8, ease: "power2.inOut" }).set(c, { y: "101%" });
    }
    if (k === "loader") {
      const l = document.querySelector("#loader-demo"), n = { v: 0 };
      const count = l.querySelector(".count"), bar = l.querySelector(".bar"), mark = l.querySelector(".mark"), word = l.querySelector(".word"), grain = l.querySelector(".grain");
      l.hidden = false; G.set(l, { yPercent: 0 }); G.set([count, word, mark], { opacity: 1, y: 0 }); G.set(bar, { scaleX: 0 });
      G.timeline()
        .fromTo(grain, { xPercent: -4, yPercent: -2 }, { xPercent: 4, yPercent: 2, duration: 1.8, ease: "none" }, 0)
        .fromTo(mark, { opacity: 0, scale: .92 }, { opacity: 1, scale: 1, duration: .9, ease: S.ease.big }, .05)
        .fromTo(word, { opacity: 0 }, { opacity: 1, duration: .5 }, .3)
        .to(n, { v: 100, duration: 1.3, ease: "power2.inOut", onUpdate: () => count.textContent = String(Math.round(n.v)).padStart(3, "0") }, .1)
        .to(bar, { scaleX: 1, duration: 1.3, ease: "power2.inOut" }, .1)
        .to([count, word, mark], { opacity: 0, y: -16, duration: .35, stagger: .04, ease: "power2.in" })
        .to(l, { yPercent: -100, duration: .9, ease: "power3.inOut" }, "-=.1")
        .set(l, { yPercent: 0, delay: .6 }).set([count, word, mark], { opacity: 1, y: 0 });
    }
  }));
}
STAGR.onReady.push(initAnimations);
'''

    return {
        "file": "design-system.html",
        "title": "Design system",
        "description": "Tokens, type scale, components and animation primitives for the Stagr website.",
        "css": css,
        "body": body,
        "js": js,
    }
