"""product-<id>.html for every product, plus product.html (resolves ?id=)."""
import importlib.util, json, os

_spec = importlib.util.spec_from_file_location("collection_mod", os.path.join(os.path.dirname(__file__), "collection.py"))
_col = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_col)
card = _col.card
SWATCH = _col.SWATCH

CSS = r'''
.pdp { padding-top: calc(var(--header-h) + 16px); }
.crumbs { display: flex; flex-wrap: wrap; gap: 8px; padding: 12px 0 20px; }
.crumbs a:hover { color: var(--accent); }
.pdp-grid { display: grid; gap: 28px; }
@media (min-width: 1024px) { .pdp-grid { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: clamp(32px, 5vw, 96px); align-items: start; } }

/* gallery: horizontal snap on phones, tall stack on desktop */
.gallery-track { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; margin-inline: calc(var(--gutter) * -1); padding-inline: var(--gutter); }
.gallery-track::-webkit-scrollbar { display: none; }
.gallery-item { flex: 0 0 86%; scroll-snap-align: center; position: relative; margin: 0; }
.gallery-item .media { --ar: 4 / 5; }
.gallery-item.is-wide .media { --ar: 3 / 2; }
.gallery-item.is-off { display: none; }
.gallery-item .zoom-btn { position: absolute; right: 12px; bottom: 12px; z-index: 2; width: 44px; height: 44px; border-radius: 50%; background: var(--bg); color: var(--ink); display: grid; place-items: center; box-shadow: var(--shadow); opacity: .9; }
.gallery-item .zoom-btn svg { width: 20px; height: 20px; }
.gallery-dots { display: flex; gap: 6px; justify-content: center; padding-top: 14px; }
.gallery-dots i { width: 6px; height: 6px; border-radius: 50%; background: var(--line-strong); transition: transform .3s var(--ease-out), background-color .3s ease; }
.gallery-dots i.is-on { background: var(--ink); transform: scale(1.4); }
@media (min-width: 1024px) {
  .gallery-track { display: grid; grid-template-columns: 1fr 1fr; gap: var(--gap); overflow: visible; scroll-snap-type: none; margin-inline: 0; padding-inline: 0; }
  .gallery-item { flex: none; }
  .gallery-item:first-child, .gallery-item.is-wide { grid-column: 1 / -1; }
  .gallery-item .media { cursor: zoom-in; }
  .gallery-item .media img { transition: transform .25s ease; transform-origin: var(--ox, 50%) var(--oy, 50%); }
  .gallery-item .media.is-zoom img { transform: scale(1.8); }
  .gallery-dots { display: none; }
}

/* summary */
.pdp-summary { display: grid; gap: 22px; align-content: start; }
@media (min-width: 1024px) { .pdp-summary { position: sticky; top: calc(var(--header-h) + 16px); } }
.pdp-summary .h2 { max-width: 12ch; }
.pdp-price { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }
.pdp-price .badge { align-self: center; }
.opt { display: grid; gap: 12px; }
.opt-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.opt-head .label span { text-transform: none; letter-spacing: 0; font-weight: 500; color: var(--ink-2); }
.pdp-actions { display: grid; gap: 12px; }
.pdp-actions .row-qty { display: flex; gap: 12px; align-items: center; }
.pdp-actions .row-qty .btn { flex: 1; --h: 52px; }
.stock { display: flex; align-items: center; gap: 10px; font-size: var(--fs-small); color: var(--ink-2); }
.stock::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--success); }
.perks { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; padding: 18px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.perk { display: grid; gap: 2px; }
.perk b { font-weight: 600; font-size: var(--fs-small); }
.perk span { font-size: var(--fs-small); color: var(--ink-3); }

/* details tabs */
.details { padding-block: var(--section-sm); }
.details-head { display: grid; gap: 20px; margin-bottom: 32px; }
@media (min-width: 1024px) { .details-head { grid-template-columns: 1fr auto; align-items: end; } }
.tab-panel { display: none; }
.tab-panel.is-on { display: block; }
.spec { display: grid; gap: 0; max-width: 60ch; }
.spec div { display: grid; grid-template-columns: 9em 1fr; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: var(--fs-body); }
.spec dt { color: var(--ink-3); font-size: var(--fs-small); font-weight: 600; letter-spacing: .04em; text-transform: uppercase; padding-top: 3px; }
.size-row { display: flex; flex-wrap: wrap; gap: 8px; }

/* craft block */
.pdp-craft { position: relative; overflow: hidden; }
.pdp-craft .grid { align-items: center; }
.pdp-craft .media { --ar: 4 / 5; }
.pdp-craft .media img { transform: scale(1.2); }

/* reviews placeholder */
.reviews-empty { border: 1px dashed var(--line-strong); border-radius: var(--radius); padding: clamp(24px, 4vw, 48px); display: grid; gap: 14px; justify-items: start; max-width: 60ch; }
.stars { display: flex; gap: 4px; color: var(--line-strong); }
.stars svg { width: 18px; height: 18px; }

/* sticky mobile bar */
.sticky-bar .sb-info { display: grid; min-width: 0; flex: 1; }
.sticky-bar .sb-name { font-family: var(--font-display); font-size: 1.1rem; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sticky-bar .btn { --h: 48px; padding: 0 22px; }
@media (min-width: 1024px) { .sticky-bar { display: none; } }

/* dialogs */
.dialog-backdrop { position: fixed; inset: 0; z-index: 100; background: var(--overlay); opacity: 0; visibility: hidden; transition: opacity .4s ease, visibility 0s linear .4s; }
.dialog-backdrop.is-open { opacity: 1; visibility: visible; transition-delay: 0s; }
.dialog { position: fixed; z-index: 101; left: 50%; top: 50%; width: min(560px, 92vw); max-height: 86svh; overflow: auto; background: var(--bg); color: var(--ink); padding: clamp(24px, 4vw, 40px); transform: translate(-50%, -50%) scale(.96); opacity: 0; visibility: hidden; transition: transform .5s var(--ease-out), opacity .4s ease, visibility 0s linear .5s; border-radius: 4px; }
.dialog.is-open { transform: translate(-50%, -50%) scale(1); opacity: 1; visibility: visible; transition-delay: 0s; }
.dialog .dlg-close { position: absolute; top: 12px; right: 12px; }
.dialog ol { counter-reset: s; display: grid; gap: 14px; margin-top: 20px; }
.dialog ol li { display: grid; grid-template-columns: 2.2em 1fr; gap: 10px; counter-increment: s; }
.dialog ol li::before { content: "0" counter(s); font-family: var(--font-display); font-size: var(--fs-h4); color: var(--accent-soft); line-height: 1.2; }
'''

JS = r'''
const PRODUCT = __PRODUCT__;
const SWATCH = { Brown: "#7B4A2B", Black: "#1A1512", Tan: "#B0773F", Coffee: "#4A3024" };
function initAnimations() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger;
  const q = (s, r) => (r || document).querySelector(s), qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches, desktop = () => window.matchMedia("(min-width: 1024px)").matches;
  let colour = PRODUCT.defaultColour, size = PRODUCT.sizes ? PRODUCT.sizes.options[2] || PRODUCT.sizes.options[0] : null, qty = 1;

  /* ---- gallery ---- */
  const track = q("[data-gallery]"), items = qa(".gallery-item", track), dots = q(".gallery-dots");
  const visible = () => items.filter(i => !i.classList.contains("is-off"));
  const applyColour = () => {
    items.forEach(it => { const c = it.dataset.colour; it.classList.toggle("is-off", !!c && c.toLowerCase() !== colour.toLowerCase()); });
    const vis = visible();
    if (dots) { dots.innerHTML = vis.map((_, i) => '<i' + (i === 0 ? ' class="is-on"' : '') + '></i>').join(""); }
    if (G && !S.reduced) G.fromTo(vis.map(v => v.querySelector("img")), { opacity: 0 }, { opacity: 1, duration: .6, stagger: .05, ease: "power2.out", clearProps: "opacity" });
    qa("[data-colour-label]").forEach(el => el.textContent = colour);
    qa("[data-add-main]").forEach(b => { b.dataset.colour = colour; });
    if (track && !desktop()) track.scrollTo({ left: 0, behavior: "auto" });
    ST && ST.refresh();
  };
  if (track && dots) track.addEventListener("scroll", () => { const vis = visible(); const i = Math.round(track.scrollLeft / (vis[0].offsetWidth + 12)); qa("i", dots).forEach((d, k) => d.classList.toggle("is-on", k === i)); }, { passive: true });
  // hover zoom (desktop)
  if (fine) items.forEach(it => { const m = q(".media", it); m.addEventListener("mousemove", e => { if (!desktop()) return; const r = m.getBoundingClientRect(); m.style.setProperty("--ox", ((e.clientX - r.left) / r.width * 100) + "%"); m.style.setProperty("--oy", ((e.clientY - r.top) / r.height * 100) + "%"); m.classList.add("is-zoom"); }); m.addEventListener("mouseleave", () => m.classList.remove("is-zoom")); });

  /* ---- lightbox ---- */
  const lb = q(".lightbox"); let lbOpen = false, lbIndex = 0, lbLast = null;
  const lbImg = q("img", lb), lbCount = q(".lb-count", lb);
  const showLb = i => { const vis = visible(); lbIndex = (i + vis.length) % vis.length; const src = vis[lbIndex].querySelector("img"); lbImg.src = src.currentSrc || src.src; lbImg.alt = src.alt; lbCount.textContent = (lbIndex + 1) + " / " + vis.length; if (G && !S.reduced) G.fromTo(lbImg, { opacity: 0, scale: .98 }, { opacity: 1, scale: 1, duration: .5, ease: "power3.out" }); };
  const openLb = i => { lbLast = document.activeElement; lb.classList.add("is-open"); lb.setAttribute("aria-hidden", "false"); lbOpen = true; S.lock(true); showLb(i); setTimeout(() => q(".lb-close", lb).focus(), 300); };
  const closeLb = () => { if (!lbOpen) return; lb.classList.remove("is-open"); lb.setAttribute("aria-hidden", "true"); lbOpen = false; S.lock(false); lbLast && lbLast.focus && lbLast.focus(); };
  items.forEach(it => { const open = () => openLb(visible().indexOf(it)); q(".zoom-btn", it).addEventListener("click", open); q(".media", it).addEventListener("click", e => { if (desktop()) open(); }); });
  q(".lb-close", lb).addEventListener("click", closeLb); q(".lb-nav.prev", lb).addEventListener("click", () => showLb(lbIndex - 1)); q(".lb-nav.next", lb).addEventListener("click", () => showLb(lbIndex + 1));
  lb.addEventListener("click", e => { if (e.target === lb) closeLb(); });
  document.addEventListener("keydown", e => { if (!lbOpen) return; if (e.key === "ArrowRight") showLb(lbIndex + 1); if (e.key === "ArrowLeft") showLb(lbIndex - 1); });

  /* ---- options ---- */
  qa('input[name="colour"]').forEach(r => r.addEventListener("change", () => { colour = r.value; applyColour(); }));
  qa('input[name="size"]').forEach(r => r.addEventListener("change", () => { size = r.value; qa("[data-size-label]").forEach(el => el.textContent = size); }));
  const qtyOut = q("[data-qty]");
  qa("[data-qty-inc]").forEach(b => b.addEventListener("click", () => { qty++; qtyOut.textContent = qty; }));
  qa("[data-qty-dec]").forEach(b => b.addEventListener("click", () => { qty = Math.max(1, qty - 1); qtyOut.textContent = qty; }));
  const add = () => S.addToCart(PRODUCT.id, colour, size, qty);
  qa("[data-add-main]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); add(); }));
  qa("[data-buy-now]").forEach(b => b.addEventListener("click", e => { e.preventDefault(); add(); }));
  applyColour();

  /* ---- sticky mobile bar: shows once the summary add button scrolls out ---- */
  const bar = q(".sticky-bar"), mainBtn = q("[data-add-main]");
  if (bar && mainBtn) { const check = () => { const r = mainBtn.getBoundingClientRect(); bar.classList.toggle("is-on", r.bottom < 0 && !desktop()); }; window.addEventListener("scroll", check, { passive: true }); window.addEventListener("resize", check); check(); }

  /* ---- details tabs ---- */
  const seg = q("[data-seg]"); if (seg) S.segmented(seg, tab => { qa(".tab-panel").forEach(p => p.classList.toggle("is-on", p.dataset.panel === tab)); ST && ST.refresh(); });

  /* ---- dialogs (size guide) ---- */
  qa("[data-dialog-open]").forEach(b => b.addEventListener("click", () => { const d = q(b.dataset.dialogOpen), bd = q(".dialog-backdrop"); d.classList.add("is-open"); bd.classList.add("is-open"); d.setAttribute("aria-hidden", "false"); S.lock(true); setTimeout(() => q(".dlg-close", d).focus(), 300); }));
  const closeDialogs = () => { qa(".dialog.is-open").forEach(d => { d.classList.remove("is-open"); d.setAttribute("aria-hidden", "true"); }); const bd = q(".dialog-backdrop"); if (bd && bd.classList.contains("is-open")) { bd.classList.remove("is-open"); S.lock(false); } };
  qa("[data-dialog-close]").forEach(b => b.addEventListener("click", closeDialogs));
  S.closeLightbox = () => { closeLb(); closeDialogs(); };
  qa("[data-review]").forEach(b => b.addEventListener("click", () => S.toast("Reviews are coming soon. For now, tell us on WhatsApp.")));
}
STAGR.onReady.push(initAnimations);
'''


def product_page(ctx, p):
    P = ctx["products"]
    B = ctx["brand"]
    I = ctx["icon"]
    fmt = lambda n: "Rs " + format(n, ",d")
    line_title = "Wallets" if p["line"] == "wallet" else "Belts"
    line_url = "wallets.html" if p["line"] == "wallet" else "belts.html"
    other = "belt" if p["line"] == "wallet" else "wallet"
    blurb = ctx["products_doc"]["lines"][p["line"]]["blurb"]
    save = round((1 - p["price"] / p["compareAtPrice"]) * 100) if p.get("compareAtPrice") else 0

    # gallery: studio shots (per colour) then lifestyle
    items = []
    for im in p["images"]:
        items.append(f'<figure class="gallery-item" data-colour="{im["colour"]}"><div class="media media--studio reveal-img"><img src="{im["src"]}" srcset="{im["srcSmall"]} 800w, {im["src"]} 1600w" sizes="(min-width: 1024px) 40vw, 86vw" alt="{im["alt"]}" width="{im["width"]}" height="{im["height"]}" {"fetchpriority=high" if not items else "loading=lazy"}></div><button type="button" class="zoom-btn" aria-label="Open image full screen">{I["zoom"]}</button></figure>')
    for im in p["lifestyleImages"]:
        wide = im["width"] > im["height"]
        items.append(f'<figure class="gallery-item{" is-wide" if wide else ""}"><div class="media reveal-img"><img src="{im["src"]}" srcset="{im["srcSmall"]} 800w, {im["src"]} 1600w" sizes="(min-width: 1024px) 50vw, 86vw" alt="{im["alt"]}" width="{im["width"]}" height="{im["height"]}" loading="lazy"></div><button type="button" class="zoom-btn" aria-label="Open image full screen">{I["zoom"]}</button></figure>')
    gallery = "".join(items)

    swatches = "".join(f'<label class="swatch" style="--sw:{SWATCH.get(c, "#7B4A2B")}"><input type="radio" name="colour" value="{c}" {"checked" if c == p["defaultColour"] else ""}><span class="sw"></span><span class="sr-only">{c}</span></label>' for c in p["colours"])
    sizes_html = ""
    if p.get("sizes"):
        opts = p["sizes"]["options"]
        default = opts[2] if len(opts) > 2 else opts[0]
        sizes_html = f'''<div class="opt"><div class="opt-head"><p class="label">{p["sizes"]["label"]} · <span data-size-label>{default}</span></p><button type="button" class="btn btn--flat btn--sm" data-dialog-open="#size-guide">Size guide</button></div><div class="sizes">{"".join(f'<label class="size"><input type="radio" name="size" value="{s}" {"checked" if s == default else ""}>{s}</label>' for s in opts)}</div><p class="small muted">Between two sizes, take the larger. Leather gives, notches do not.</p></div>'''
    perks = "".join(f'<div class="perk"><b>{t["title"]}</b><span>{t["sub"]}</span></div>' for t in B["trust"]["items"])
    acc = "".join(f'<details{" open" if i == 0 else ""}><summary>{t}<span class="plus"></span></summary><div class="acc-body"><p>{b}</p></div></details>' for i, (t, b) in enumerate([
        ("Product details", p["details"]["productDetails"]), ("Leather specification", p["details"]["leatherSpecification"]), ("Care", p["details"]["care"]), ("Delivery and returns", p["details"]["deliveryAndReturns"])]))
    mats = p["materials"]
    mat_rows = "".join(f'<div><dt>{k}</dt><dd>{v.split(" (old page")[0].split(" — ")[0]}</dd></div>' for k, v in [("Leather", mats["leather"]), ("Hardware" if "hardware" in mats else "Lining", mats.get("hardware") or mats.get("lining")), ("Thickness", mats["thickness"]), ("Stitching", mats["stitching"]), ("Colours", " / ".join(p["colours"])), ("Made in", "Pakistan")])
    if p["line"] == "belt":
        dims = f'<p class="body">Sizes {p["sizes"]["options"][0]} to {p["sizes"]["options"][-1]}, measured from the buckle bar to the hole you use. Cut in one piece from the hide.</p><div class="size-row" style="margin-top:16px">{"".join(f"<span class=chip>{s}</span>" for s in p["sizes"]["options"])}</div><p class="small muted" style="margin-top:16px">Belt width is not listed yet. Message us on WhatsApp and we will measure the strap for you.</p>'
    else:
        dims = f'<p class="body">{p["style"]} wallet, one size. Exact dimensions are being measured for this page.</p><p class="small muted" style="margin-top:12px">Message us on <a class="link" href="{B["contact"]["whatsapp"]["link"]}" target="_blank" rel="noopener">WhatsApp</a> for the measurements of this piece in the meantime.</p>'
    cross = [x for x in P if x["line"] == other][:3]
    cross_cards = "".join(card(ctx, x, i) for i, x in enumerate(cross))
    guide_steps = "".join(f"<li>{s}</li>" for s in (p["sizes"]["guide"] if p.get("sizes") else []))
    star = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>'

    body = f'''
<section class="pdp" aria-labelledby="p-title">
  <div class="wrap">
    <nav class="crumbs small muted" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="{line_url}">{line_title}</a><span>/</span><span aria-current="page">{p["name"]}</span></nav>
    <div class="pdp-grid">
      <div class="pdp-gallery">
        <div class="gallery-track" data-gallery aria-label="Product images">{gallery}</div>
        <div class="gallery-dots" aria-hidden="true"></div>
      </div>
      <aside class="pdp-summary">
        <p class="label label-row" data-reveal="up">{p["style"] or "Belt"} · Crazy horse leather</p>
        <h1 class="h2" id="p-title" data-lines="now" data-delay=".15">{p["name"]}</h1>
        <div class="pdp-price" data-reveal="up" data-delay=".35"><span class="price h3">{fmt(p["price"])}</span>{f'<s class="muted">{fmt(p["compareAtPrice"])}</s><span class="badge badge--tint">Save {save}%</span>' if save else ''}</div>
        <p class="lead" data-reveal="up" data-delay=".45">{p["tagline"]}</p>
        <p class="muted body" data-reveal="up" data-delay=".5">{blurb}</p>
        <div class="opt" data-reveal="up" data-delay=".55"><div class="opt-head"><p class="label">Colour · <span data-colour-label>{p["defaultColour"]}</span></p></div><div class="swatches">{swatches}</div></div>
        {sizes_html}
        <div class="pdp-actions" data-reveal="up" data-delay=".65">
          <div class="row-qty"><div class="qty"><button type="button" data-qty-dec aria-label="Decrease quantity">−</button><span data-qty>1</span><button type="button" data-qty-inc aria-label="Increase quantity">+</button></div><button type="button" class="btn" data-add-main data-magnetic><span class="btn-label">Add to cart</span></button></div>
          <button type="button" class="btn btn--ghost btn--wide" data-buy-now>{B["payment"]["ctaCopy"]}</button>
          <p class="stock">Ships in 3 to 5 working days, anywhere in Pakistan</p>
        </div>
        <div class="perks" data-reveal="up" data-delay=".7">{perks}</div>
        <div class="acc" data-reveal="up" data-delay=".75" id="details">{acc}</div>
      </aside>
    </div>
  </div>
</section>

<section class="details" aria-labelledby="details-title">
  <div class="wrap">
    <div class="details-head"><div><p class="label label-row" data-reveal="up">Details</p><h2 class="h2" id="details-title" data-lines style="margin-top:16px">What you are holding</h2></div>
      <div class="seg" data-seg role="tablist"><div class="seg-thumb"></div><button type="button" role="tab" aria-selected="true" data-tab="materials">Materials</button><button type="button" role="tab" aria-selected="false" data-tab="dimensions">Dimensions</button><button type="button" role="tab" aria-selected="false" data-tab="care">Care</button></div></div>
    <div class="tab-panel is-on" data-panel="materials" role="tabpanel"><dl class="spec">{mat_rows}</dl></div>
    <div class="tab-panel" data-panel="dimensions" role="tabpanel">{dims}</div>
    <div class="tab-panel" data-panel="care" role="tabpanel"><p class="body">{B["care"]["short"]}</p><p class="body muted" style="margin-top:12px">{B["care"]["accordion"]}</p></div>
  </div>
</section>

<section class="section-sm theme-dark pdp-craft" aria-labelledby="craft-title">
  <div class="wrap grid">
    <div class="col-12 md:col-6 lg:col-5"><div class="media reveal-img" data-parallax=".25"><img src="assets/lifestyle/{"kingsmen-02" if p["line"] == "wallet" else "ranger-02"}.jpg" alt="{"Hand saddle stitching on a Stagr wallet" if p["line"] == "wallet" else "Crazy horse leather grain with the embossed Stagr stag"}" width="1200" height="1500" loading="lazy"></div></div>
    <div class="col-12 md:col-6 lg:col-5 lg:start-8"><p class="label label-row" data-reveal="up" style="color:var(--c-saddle)">The craft</p><h2 class="h2" id="craft-title" data-lines style="margin-top:16px">{B["craft"]["heading"]}</h2><p class="lead" data-reveal="up" data-delay=".2" style="color:rgba(246,242,236,.78);margin-top:20px">{B["craft"]["body"]}</p><p data-reveal="up" data-delay=".3" style="margin-top:28px"><a class="btn btn--ghost" href="about.html#craft">How it is made {I["arrow"]}</a></p></div>
  </div>
</section>

<section class="section-sm" aria-labelledby="cross-title">
  <div class="wrap">
    <div class="between" style="margin-bottom:clamp(28px,4vw,48px)"><div><p class="label label-row" data-reveal="up">Complete the look</p><h2 class="h2" id="cross-title" data-lines style="margin-top:16px">{"A belt to go with it" if p["line"] == "wallet" else "A wallet to go with it"}</h2></div><a class="btn btn--ghost" href="{other}s.html">All {other}s</a></div>
    <div class="product-grid" style="display:grid;gap:var(--gap);grid-template-columns:repeat(3,minmax(0,1fr))" data-stagger=".08">{cross_cards}</div>
  </div>
</section>

<section class="section-sm" aria-labelledby="reviews-title" style="padding-top:0">
  <div class="wrap">
    <p class="label label-row" data-reveal="up">Reviews</p>
    <h2 class="h2" id="reviews-title" data-lines style="margin-top:16px">What people say</h2>
    <div class="reviews-empty" data-reveal="up" style="margin-top:28px"><div class="stars">{star * 5}</div><p class="h4">No reviews yet.</p><p class="muted">Be the first to write one once your {p["name"].split(" ")[0]} arrives.</p><button type="button" class="btn btn--ghost btn--sm" data-review>Write a review</button></div>
  </div>
</section>

<div class="sticky-bar" aria-hidden="true"><div class="sb-info"><span class="sb-name">{p["name"]}</span><span class="price small">{fmt(p["price"])}</span></div><button type="button" class="btn" data-add-main>Add to cart</button></div>

<div class="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" aria-hidden="true">
  <button type="button" class="lb-close" aria-label="Close">{I["close"]}</button>
  <button type="button" class="lb-nav prev" aria-label="Previous image">{I["arrow-l"]}</button>
  <img src="" alt="" width="1600" height="1200">
  <button type="button" class="lb-nav next" aria-label="Next image">{I["arrow-r"]}</button>
  <div class="lb-count"></div>
</div>

<div class="dialog-backdrop" data-dialog-close aria-hidden="true"></div>
<div class="dialog" id="size-guide" role="dialog" aria-modal="true" aria-labelledby="sg-title" aria-hidden="true" data-lenis-prevent>
  <button type="button" class="btn btn--icon dlg-close" data-dialog-close aria-label="Close">{I["close"]}</button>
  <p class="label">Size guide</p>
  <h2 class="h3" id="sg-title" style="margin-top:10px">Measure the belt you wear</h2>
  <ol>{guide_steps or "<li>Wallets come in one size.</li>"}</ol>
  <p class="small muted" style="margin-top:20px">Sizes {p["sizes"]["options"][0] if p.get("sizes") else ""}{" to " + str(p["sizes"]["options"][-1]) if p.get("sizes") else ""}. Still unsure? Message us on WhatsApp with the belt you wear today.</p>
</div>
'''
    data = {k: p[k] for k in ("id", "name", "line", "style", "price", "colours", "defaultColour", "sizes")}
    return {
        "file": f"product-{p['id']}.html",
        "title": p["name"],
        "description": f'{p["name"]}. {p["tagline"]} {fmt(p["price"])}, cash on delivery across Pakistan.',
        "css": CSS,
        "body": body,
        "js": JS.replace("__PRODUCT__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")),
    }


def render(ctx):
    pages = [product_page(ctx, p) for p in ctx["products"]]
    ids = [p["id"] for p in ctx["products"]]
    # product.html resolves ?id=<slug> to the static page (falls back to the first product)
    pages.append({
        "file": "product.html",
        "title": "Product",
        "css": "",
        "body": f'<section class="section" style="padding-top:calc(var(--header-h) + var(--section-sm))"><div class="wrap"><p class="label label-row">Product</p><h1 class="h2" style="margin-top:20px">Opening the product page…</h1><p class="lead" style="margin-top:20px">If nothing happens, pick a piece: {" · ".join(f"<a class=link href=product-{i}.html>{i}</a>" for i in ids)}.</p></div></section>',
        "js": f'(function(){{var ids={json.dumps(ids)};var id=new URLSearchParams(location.search).get("id");location.replace("product-"+(ids.indexOf(id)>=0?id:ids[0])+".html"+location.hash);}})();',
    })
    return pages
