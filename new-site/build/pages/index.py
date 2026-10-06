"""index.html — home."""
import json


def render(ctx):
    P = ctx["products"]
    B = ctx["brand"]
    I = ctx["icon"]
    by = {p["id"]: p for p in P}
    fmt = lambda n: "Rs " + format(n, ",d")

    # ---------- craft story steps (text from brand.json; stand-in imagery flagged) ----------
    step_imgs = [
        ("assets/lifestyle/ranger-flat.jpg", "Crazy horse hide with the embossed stag"),
        ("assets/lifestyle/onyx-flat.jpg", "A cut strap, backlit"),
        ("assets/lifestyle/kingsmen-02.jpg", "Saddle stitching on a wallet edge"),
        ("assets/lifestyle/monarch-01.jpg", "A finished belt and buckle"),
    ]
    steps = B["craft"]["steps"]
    craft_steps = "".join(
        f'<li class="craft-step" data-step="{i}"><span class="num">{s["n"]}</span><div><h3 class="h3">{s["title"]}</h3><p class="muted">{s["body"]}</p></div></li>'
        for i, s in enumerate(steps))
    craft_imgs = "".join(
        f'<div class="craft-img media" data-step-img="{i}"><img src="{src}" alt="{alt}" width="1800" height="1200" loading="lazy"></div>'
        for i, (src, alt) in enumerate(step_imgs))

    # ---------- featured slider ----------
    featured_ids = ["kingsmann", "monarch", "rodeo", "nova", "maverick", "outlaw", "upbuck", "regent", "purefold", "majestic", "regal"]
    def slide(p):
        a = p["images"][0]
        meta = (p["style"] or "Belt") + " · " + " / ".join(p["colours"])
        return (f'<a class="slide" href="product-{p["id"]}.html" draggable="false">'
                f'<div class="media media--studio"><img src="{a["src"]}" srcset="{a["srcSmall"]} 800w, {a["src"]} 1600w" sizes="(min-width: 1024px) 380px, 70vw" alt="{a["alt"]}" width="{a["width"]}" height="{a["height"]}" loading="lazy" draggable="false"></div>'
                f'<div class="slide-body"><span class="card-name">{p["name"]}</span><span class="card-meta">{meta}</span><span class="price">{fmt(p["price"])}</span></div></a>')
    slides = "".join(slide(by[i]) for i in featured_ids)

    trust = "".join(f'<div class="trust-item"><span class="t">{t["title"]}</span><span class="s">{t["sub"]}</span></div>' for t in B["trust"]["items"])
    ticker = "".join(f'<span class="label">{t}</span><span class="label tick-dot">·</span>' for t in B["ticker"])

    wallets_count = sum(1 for p in P if p["line"] == "wallet")
    belts_count = sum(1 for p in P if p["line"] == "belt")

    css = r'''
/* ---- hero ---- */
.hero { position: relative; min-height: 100svh; display: grid; align-items: end; overflow: hidden; background: var(--c-espresso); color: var(--c-offwhite); }
.hero-media { position: absolute; inset: 0; --ar: auto; border-radius: 0; background: var(--c-espresso); }
.hero-media img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%; }
.hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to top, rgba(30,22,18,.88) 0%, rgba(30,22,18,.45) 40%, rgba(30,22,18,.15) 70%, rgba(30,22,18,.35) 100%); pointer-events: none; }
.hero-body { position: relative; z-index: 2; padding-top: calc(var(--header-h) + 48px); padding-bottom: clamp(96px, 14vh, 160px); display: grid; gap: 24px; }
.hero .display { max-width: 11ch; color: var(--c-offwhite); }
.hero .lead { color: rgba(246,242,236,.8); max-width: 30em; }
.hero-eyebrow { color: var(--c-saddle); }
.hero-eyebrow::before { background: var(--c-saddle); }
.hero-ctas { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 8px; }
.hero .btn { --btn-bg: var(--c-offwhite); --btn-ink: var(--c-espresso); }
.hero .btn--ghost { color: var(--c-offwhite); border-color: rgba(246,242,236,.45); }
.hero .btn--ghost::before { background: var(--c-offwhite); }
.hero .btn--ghost:hover { color: var(--c-espresso); }
.hero .scroll-cue { position: absolute; z-index: 2; left: var(--gutter); bottom: 28px; color: rgba(246,242,236,.75); }
.hero .hero-count { position: absolute; z-index: 2; right: var(--gutter); bottom: 28px; font-size: var(--fs-small); letter-spacing: .14em; text-transform: uppercase; color: rgba(246,242,236,.6); display: none; }
@media (min-width: 768px) { .hero .hero-count { display: block; } }
@media (min-width: 1024px) { .hero-body { padding-bottom: clamp(120px, 16vh, 200px); } .hero .scroll-cue { bottom: 40px; } }

/* ---- ticker ---- */
.ticker { background: var(--c-espresso); color: var(--c-offwhite); padding: 18px 0; border-top: 1px solid rgba(246,242,236,.12); }
.ticker .track { --mq-gap: 40px; align-items: center; }
.ticker .tick-dot { color: var(--c-saddle); }

/* ---- two lines ---- */
.lines-head { display: grid; gap: 16px; margin-bottom: clamp(40px, 6vw, 72px); }
.lines-head .h2 { max-width: 16ch; }
@media (min-width: 1024px) { .lines-head { grid-template-columns: 1fr 1fr; align-items: end; } }
.doors { display: grid; gap: var(--gap); perspective: 1400px; }
@media (min-width: 768px) { .doors { grid-template-columns: 1fr 1fr; } .doors .door:nth-child(2) { margin-top: clamp(40px, 8vw, 120px); } }
.door .media { --ar: 3 / 4; }
@media (min-width: 1024px) { .door .media { --ar: 4 / 5; } }
.door .door-count { position: absolute; top: clamp(16px, 2.4vw, 28px); left: clamp(16px, 2.4vw, 28px); z-index: 2; color: var(--c-offwhite); }
.door .door-arrow { display: inline-flex; align-items: center; gap: 10px; color: var(--c-offwhite); }
.door .door-arrow svg { transition: transform var(--t-micro) var(--ease-out); }
.door:hover .door-arrow svg { transform: translateX(6px); }

/* ---- craft story (sticky stage, images swap on scroll) ---- */
.craft { position: relative; background: var(--c-espresso); color: var(--c-offwhite); }
.craft-track { position: relative; height: calc(var(--steps) * 100svh + 40svh); }
.craft-stage { position: sticky; top: 0; height: 100svh; display: grid; grid-template-rows: 46svh 1fr; overflow: hidden; }
.craft-media { position: relative; }
.craft-img { position: absolute; inset: 0; --ar: auto; border-radius: 0; opacity: 0; }
.craft-img:first-child { opacity: 1; }
.craft-img > img { transform: scale(1.06); }
.craft-text { position: relative; padding: 24px var(--gutter) 24px; display: grid; align-content: start; gap: 18px; min-height: 0; }
.craft-text .label { color: var(--c-saddle); }
.craft-steps { position: relative; display: grid; }
.craft-step { grid-area: 1 / 1; display: flex; gap: 20px; opacity: 0; visibility: hidden; transform: translateY(14px); transition: opacity .6s ease, transform .7s var(--ease-out), visibility 0s linear .6s; }
.craft-step.is-active { opacity: 1; visibility: visible; transform: none; transition-delay: 0s; }
.craft-step .num { flex: none; width: 2.2em; }
.craft-step .h3 { margin-bottom: 8px; }
.craft-step .muted { color: rgba(246,242,236,.72); max-width: 40ch; }
.craft-progress { display: flex; gap: 8px; }
.craft-progress i { width: 32px; height: 2px; background: rgba(246,242,236,.2); position: relative; overflow: hidden; }
.craft-progress i::after { content: ""; position: absolute; inset: 0; background: var(--c-saddle); transform: scaleX(0); transform-origin: left; transition: transform .5s var(--ease-out); }
.craft-progress i.is-active::after { transform: scaleX(1); }
@media (min-width: 1024px) {
  .craft-stage { grid-template-rows: none; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); }
  .craft-text { padding: 0 var(--gutter); align-content: center; gap: 28px; }
  .craft-media { order: 2; }
  .craft-step { grid-area: auto; opacity: .38; visibility: visible; transform: none; padding: 22px 0; border-top: 1px solid rgba(246,242,236,.12); transition: opacity .5s ease; }
  .craft-step.is-active { opacity: 1; }
  .craft-step .muted { max-height: 0; overflow: hidden; opacity: 0; transition: max-height .6s var(--ease-out), opacity .4s ease; }
  .craft-step.is-active .muted { max-height: 160px; opacity: 1; }
  .craft-progress { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .craft-track { height: auto; }
  .craft-stage { position: static; height: auto; display: block; padding: var(--section) 0; }
  .craft-media { display: grid; gap: var(--gap); grid-template-columns: repeat(2, 1fr); padding: 0 var(--gutter); margin-top: 32px; }
  .craft-img { position: relative; inset: auto; --ar: 3 / 2; opacity: 1; }
  .craft-step { opacity: 1; visibility: visible; transform: none; grid-area: auto; padding: 18px 0; }
  .craft-step .muted { max-height: none; opacity: 1; }
  .craft-progress { display: none; }
}

/* ---- featured slider ---- */
.featured { overflow: hidden; }
.featured-head { margin-bottom: clamp(32px, 5vw, 56px); }
.featured-head .h2 { max-width: 16ch; }
.slider { position: relative; --w: clamp(230px, 64vw, 360px); --g: 20px; height: calc(var(--w) * 1.25 + 110px); user-select: none; touch-action: pan-y; }
@media (min-width: 1024px) { .slider { --w: 380px; --g: 28px; } }
.slider-track { position: absolute; inset: 0; }
.slide { position: absolute; top: 0; left: 50%; width: var(--w); margin-left: calc(var(--w) / -2); will-change: transform; transform-origin: 50% 40%; }
.slide .media { --ar: 4 / 5; }
.slide .media img { pointer-events: none; }
.slide-body { display: grid; gap: 4px; padding-top: 14px; }
.slide .card-name { font-family: var(--font-display); font-size: var(--fs-h4); line-height: 1.2; }
.slide .card-meta { font-size: var(--fs-small); color: var(--ink-2); }
.slide .price { font-size: var(--fs-small); }
.slider-nav { display: flex; gap: 10px; }
.featured-cta { margin-top: clamp(32px, 5vw, 56px); display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }

/* ---- materials ---- */
.materials-head { display: grid; gap: 20px; margin-bottom: clamp(40px, 6vw, 80px); }
.materials-head .h2 { max-width: 14ch; }
@media (min-width: 1024px) { .materials-head { grid-template-columns: 1fr 1fr; align-items: end; } }
.mat-row { display: grid; gap: var(--gap); grid-template-columns: repeat(3, minmax(0, 1fr)); align-items: start; }
.mat-row .media { --ar: 3 / 4; }
.mat-row .media:nth-child(2) { margin-top: clamp(32px, 8vw, 120px); }
.mat-row .media:nth-child(3) { margin-top: clamp(16px, 4vw, 60px); }
.mat-row .media > img { transform: scale(1.25); }
.mat-facts { display: flex; flex-wrap: wrap; gap: 10px; margin-top: clamp(32px, 5vw, 56px); }

/* ---- note band ---- */
.note-band { padding-block: var(--section); }
.note-band .wrap { display: grid; gap: 20px; }
.note-band .h2 { max-width: 14ch; }
.note-band .lead { color: rgba(246,242,236,.8); }
@media (min-width: 1024px) { .note-band .wrap { grid-template-columns: 1fr 1fr; align-items: center; } }

/* ---- trust ---- */
.trust-section { padding-block: var(--section-sm); }
'''

    body = f'''
<section class="hero" id="hero" aria-label="Introduction">
  <div class="hero-media media reveal-img" data-from="bottom" data-wait="loader">
    <picture>
      <source media="(max-width: 767px)" srcset="assets/hero/hero-belts-portrait.jpg">
      <img src="assets/hero/hero-belts-1600.jpg" srcset="assets/hero/hero-belts-900.jpg 900w, assets/hero/hero-belts-1600.jpg 1600w, assets/hero/hero-belts-2400.jpg 2400w" sizes="100vw" alt="Four Stagr belts in black, brown and tan hanging on a wooden board" width="2400" height="1600" fetchpriority="high">
    </picture>
  </div>
  <div class="wrap hero-body">
    <p class="label label-row hero-eyebrow" data-reveal="up" data-wait="loader" data-delay=".9">{B["hero"]["eyebrow"]}</p>
    <h1 class="display" data-lines="now" data-wait="loader" data-delay=".55">{B["hero"]["headline"][0]}<br>{B["hero"]["headline"][1]}</h1>
    <p class="lead" data-reveal="up" data-wait="loader" data-delay="1.15">{B["hero"]["sub"]}</p>
    <div class="hero-ctas" data-reveal="up" data-wait="loader" data-delay="1.3">
      <a class="btn btn--lg" href="belts.html" data-magnetic><span class="btn-label">{B["hero"]["ctas"][0]}</span>{I["arrow"]}</a>
      <a class="btn btn--lg btn--ghost" href="wallets.html" data-magnetic><span class="btn-label">{B["hero"]["ctas"][1]}</span></a>
    </div>
  </div>
  <a class="scroll-cue" href="#lines" data-scroll-to="#lines" data-reveal data-wait="loader" data-delay="1.6">Scroll <i></i></a>
  <p class="hero-count" data-reveal data-wait="loader" data-delay="1.6">{B["origin"]} · {B["since"]["value"]}</p>
</section>

<div class="ticker marquee" data-marquee data-speed="50" aria-hidden="true"><div class="track">{ticker}</div></div>

<section class="section" id="lines" aria-labelledby="lines-title">
  <div class="wrap">
    <div class="lines-head">
      <div><p class="label label-row" data-reveal="up">Two lines</p><h2 class="h2" id="lines-title" data-lines style="margin-top:20px">Wallets and belts. <em class="i">Nothing else.</em></h2></div>
      <p class="lead" data-reveal="up" data-delay=".2">{B["craft"]["body"]}</p>
    </div>
    <div class="doors">
      <a class="door" href="wallets.html" data-tilt data-cursor="Wallets">
        <span class="label door-count">01 · {wallets_count} styles</span>
        <div class="media reveal-img"><img src="assets/lifestyle/kingsmen-01.jpg" srcset="assets/lifestyle/kingsmen-01-800.jpg 800w, assets/lifestyle/kingsmen-01.jpg 1600w" sizes="(min-width: 768px) 50vw, 100vw" alt="Kingsmann bifold wallet with orange stitching on sherpa" width="1200" height="1500" loading="lazy"></div>
        <div class="door-body"><div class="door-title">Wallets</div><div class="door-rule"></div><p class="small" style="color:rgba(246,242,236,.8);max-width:34ch;margin-bottom:18px">{B["lines"]["wallet"]["homeLine"] if "lines" in B else "Bifolds, trifolds and long wallets that soften and darken with every carry."}</p><span class="label door-arrow">Shop wallets {I["arrow"]}</span></div>
      </a>
      <a class="door" href="belts.html" data-tilt data-cursor="Belts">
        <span class="label door-count">02 · {belts_count} styles</span>
        <div class="media reveal-img"><img src="assets/lifestyle/ranger-open.jpg" srcset="assets/lifestyle/ranger-open-800.jpg 800w, assets/lifestyle/ranger-open.jpg 1600w" sizes="(min-width: 768px) 50vw, 100vw" alt="Tan Stagr belt buckle on wood with coffee beans" width="1800" height="1200" loading="lazy"></div>
        <div class="door-body"><div class="door-title">Belts</div><div class="door-rule"></div><p class="small" style="color:rgba(246,242,236,.8);max-width:34ch;margin-bottom:18px">Cut from full crazy horse hides and stitched by hand. Classic and double-sided styles.</p><span class="label door-arrow">Shop belts {I["arrow"]}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="craft" id="craft" aria-labelledby="craft-title">
  <div class="craft-track" style="--steps:{len(steps)}">
    <div class="craft-stage">
      <div class="craft-media">{craft_imgs}</div>
      <div class="craft-text">
        <p class="label label-row">{B["about"]["howItIsMadeTitle"]}</p>
        <h2 class="h2" id="craft-title">One hide, four hands, no shortcuts.</h2>
        <ol class="craft-steps">{craft_steps}</ol>
        <div class="craft-progress" aria-hidden="true">{"".join('<i></i>' for _ in steps)}</div>
      </div>
    </div>
  </div>
</section>

<section class="section featured" id="featured" aria-labelledby="featured-title">
  <div class="wrap">
    <div class="between featured-head">
      <div><p class="label label-row" data-reveal="up">Featured</p><h2 class="h2" id="featured-title" data-lines style="margin-top:20px">The pieces people come back for</h2></div>
      <div class="slider-nav" data-reveal="up"><button type="button" class="btn btn--icon" data-slide="-1" aria-label="Previous">{I["arrow-l"]}</button><button type="button" class="btn btn--icon" data-slide="1" aria-label="Next">{I["arrow-r"]}</button></div>
    </div>
  </div>
  <div class="slider" data-cursor="Drag" data-reveal><div class="slider-track">{slides}</div></div>
  <div class="wrap featured-cta" data-reveal="up"><a class="btn btn--ghost" href="wallets.html">All wallets</a><a class="btn btn--ghost" href="belts.html">All belts</a></div>
</section>

<section class="section" id="materials" aria-labelledby="materials-title">
  <div class="wrap">
    <div class="materials-head">
      <div><p class="label label-row" data-reveal="up">Materials</p><h2 class="h2" id="materials-title" data-lines style="margin-top:20px">{B["craft"]["heading"]}</h2></div>
      <p class="lead" data-reveal="up" data-delay=".2">{B["faqs"][0]["a"]}</p>
    </div>
    <div class="mat-row">
      <div class="media" data-parallax=".25"><img src="assets/lifestyle/ranger-02.jpg" srcset="assets/lifestyle/ranger-02-800.jpg 800w, assets/lifestyle/ranger-02.jpg 1600w" sizes="33vw" alt="Macro of crazy horse leather grain with the embossed Stagr stag" width="1200" height="1500" loading="lazy"></div>
      <div class="media" data-parallax=".45"><img src="assets/lifestyle/kingsmen-02.jpg" srcset="assets/lifestyle/kingsmen-02-800.jpg 800w, assets/lifestyle/kingsmen-02.jpg 1600w" sizes="33vw" alt="Macro of hand saddle stitching on a dark wallet" width="1200" height="1500" loading="lazy"></div>
      <div class="media" data-parallax=".15"><img src="assets/lifestyle/heritage-flat.jpg" srcset="assets/lifestyle/heritage-flat-800.jpg 800w, assets/lifestyle/heritage-flat.jpg 1600w" sizes="33vw" alt="Macro of a tan belt and buckle on wood" width="1800" height="1200" loading="lazy"></div>
    </div>
    <ul class="mat-facts" data-stagger=".06">
      <li class="badge">100% crazy horse leather</li><li class="badge">Full grain hide</li><li class="badge">Waxed finish</li><li class="badge">Saddle stitched</li><li class="badge">No PU, no rexine</li><li class="badge">Handmade in Pakistan</li>
    </ul>
  </div>
</section>

<section class="note-band theme-oxblood" aria-labelledby="note-title">
  <div class="wrap">
    <div><p class="label label-row" data-reveal="up">{B["handwrittenNote"]["eyebrow"]}</p><h2 class="h2" id="note-title" data-lines style="margin-top:20px">{B["handwrittenNote"]["title"]}</h2></div>
    <p class="lead" data-reveal="up" data-delay=".2">{B["handwrittenNote"]["body"]}</p>
  </div>
</section>

<section class="trust-section" id="trust" aria-label="Delivery, returns and service">
  <div class="wrap"><div class="trust" data-stagger=".08">{trust}</div></div>
</section>
'''

    js = r'''
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger;
  const q = (s, r) => (r || document).querySelector(s), qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---- door tilt (desktop only) ---- */
  if (G && fine && !S.reduced) qa("[data-tilt]").forEach(door => {
    const rx = G.quickTo(door, "rotationX", { duration: .6, ease: "power3" }), ry = G.quickTo(door, "rotationY", { duration: .6, ease: "power3" });
    door.addEventListener("mousemove", e => { const r = door.getBoundingClientRect(); const px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5; rx(-py * 6); ry(px * 6); });
    door.addEventListener("mouseleave", () => { rx(0); ry(0); });
  });

  /* ---- craft story: sticky stage, step driven by scroll progress ---- */
  const craft = q(".craft-track");
  if (craft) {
    const steps = qa(".craft-step"), imgs = qa(".craft-img"), bars = qa(".craft-progress i");
    let cur = -1;
    const setStep = i => {
      if (i === cur) return; cur = i;
      steps.forEach((s, k) => s.classList.toggle("is-active", k === i));
      bars.forEach((b, k) => b.classList.toggle("is-active", k <= i));
      if (G && !S.reduced) {
        imgs.forEach((im, k) => G.to(im, { opacity: k === i ? 1 : 0, duration: .8, ease: "power2.inOut", overwrite: true }));
        G.fromTo(imgs[i].querySelector("img"), { scale: 1.12 }, { scale: 1.04, duration: 1.6, ease: "power3.out", overwrite: true });
      } else imgs.forEach((im, k) => im.style.opacity = k === i ? 1 : 0);
    };
    if (S.reduced || !ST) { steps.forEach(s => s.classList.add("is-active")); imgs.forEach(im => im.style.opacity = 1); }
    else {
      setStep(0);
      ST.create({ trigger: craft, start: "top top", end: "bottom bottom", scrub: true, onUpdate: self => setStep(Math.min(steps.length - 1, Math.floor(self.progress * steps.length))) });
    }
  }

  /* ---- featured: infinite slider with centre scale, drag + wheel ---- */
  const slider = q(".slider");
  if (slider && G) {
    const track = q(".slider-track", slider), items = qa(".slide", slider), n = items.length;
    let W = 0, GAP = 0, STEP = 0, TOTAL = 0, offset = 0, vel = 0, dragging = false, moved = 0, hover = false, lastT = 0;
    const measure = () => { W = items[0].offsetWidth || 300; GAP = parseFloat(getComputedStyle(slider).getPropertyValue("--g")) || 20; STEP = W + GAP; TOTAL = STEP * n; render(); };
    const wrap = G.utils.wrap(-TOTAL / 2, TOTAL / 2);
    const render = () => {
      const half = TOTAL / 2;
      items.forEach((el, i) => {
        let x = i * STEP + offset; x = ((x + half) % TOTAL + TOTAL) % TOTAL - half;
        const d = Math.min(1, Math.abs(x) / STEP);
        const sc = S.reduced ? 1 : 1 + .14 * (1 - d);
        G.set(el, { x, scale: sc, opacity: .55 + .45 * (1 - d), zIndex: Math.round(100 - d * 50) });
      });
    };
    measure(); window.addEventListener("resize", measure);
    // idle drift + inertia
    G.ticker.add(t => {
      if (S.reduced) return;
      const dt = Math.min(.05, t - lastT); lastT = t;
      if (!dragging) {
        if (Math.abs(vel) > .05) { offset += vel * dt; vel *= Math.pow(.08, dt); }
        else if (!hover) offset -= 18 * dt; /* slow auto drift */
        else return;
        render();
      }
    });
    slider.addEventListener("mouseenter", () => hover = true); slider.addEventListener("mouseleave", () => hover = false);
    if (window.Observer && !S.reduced) {
      window.Observer.create({ target: slider, type: "touch,pointer", lockAxis: true, dragMinimum: 3, preventDefault: false,
        onDragStart: () => { dragging = true; moved = 0; vel = 0; slider.classList.add("is-dragging"); },
        onDrag: self => { offset += self.deltaX; moved += Math.abs(self.deltaX); render(); },
        onDragEnd: self => { dragging = false; vel = self.velocityX * .6; slider.classList.remove("is-dragging"); } });
    }
    slider.addEventListener("wheel", e => { if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) { e.preventDefault(); vel = 0; offset -= e.deltaX; render(); } }, { passive: false });
    slider.addEventListener("click", e => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); moved = 0; } }, true);
    const snapTo = dir => { vel = 0; const target = Math.round(offset / STEP) * STEP - dir * STEP; const o = { v: offset }; G.to(o, { v: target, duration: .8, ease: "power3.out", onUpdate: () => { offset = o.v; render(); } }); };
    qa("[data-slide]").forEach(b => b.addEventListener("click", () => snapTo(+b.dataset.slide)));
    slider.addEventListener("keydown", e => { if (e.key === "ArrowRight") snapTo(1); if (e.key === "ArrowLeft") snapTo(-1); });
    slider.tabIndex = 0; slider.setAttribute("aria-roledescription", "carousel"); slider.setAttribute("aria-label", "Featured products");
  }
}
STAGR.onReady.push(initAnimations);
'''

    return {
        "file": "index.html",
        "title": "Handmade crazy horse leather belts and wallets",
        "description": B["descriptor"] + " " + B["origin"] + ". Cash on delivery across Pakistan.",
        "css": css,
        "body": body,
        "js": js,
        "loader": True,
        "header_dark": True,
    }
