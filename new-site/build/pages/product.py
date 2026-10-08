"""product-<id>.html for every product, plus product.html (resolves ?id=).

Item detail page in the home-page language: breadcrumb, a gallery card (cutouts of
the chosen colour, then real frames from the shoot) with thumbnails, a sticky buy
column (price, colour, size, quantity, add to cart, WhatsApp, perks, accordions),
a "What you are holding" spec card, the four making steps, a rail of other pieces
and the "Why people choose Stagr" block.
"""
import json
import os

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CSS = r'''
/* ---- top: gallery + buy column ---- */
.pd-top { padding: calc(var(--nav-top) + 18px) 0 clamp(40px, 6vw, 72px); background: var(--bone); color: var(--ink); }
.pd-crumbs { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; font-size: .8125rem; color: var(--fg-2); margin-bottom: 18px; }
.pd-crumbs a:hover { color: var(--accent-deep); }
.pd-crumbs i { font-style: normal; opacity: .5; }
.pd-grid { display: grid; gap: 28px; }
@media (min-width: 1024px) { .pd-grid { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: clamp(32px, 4vw, 64px); align-items: start; } }
/* gallery */
.pd-gallery { display: grid; gap: 10px; }
.pd-stage { position: relative; aspect-ratio: 1; border-radius: 16px; overflow: hidden; background: #F3F1EC; touch-action: pan-y; user-select: none; box-shadow: 0 1px 2px rgba(26,27,29,.04), 0 10px 30px -18px rgba(26,27,29,.18); }
.pd-slide { position: absolute; inset: 0; margin: 0; display: grid; place-items: center; opacity: 0; visibility: hidden; transition: opacity .45s ease, visibility 0s linear .45s; }
.pd-slide.is-on { opacity: 1; visibility: visible; transition-delay: 0s; }
.pd-slide.is-off { display: none; }
.pd-slide--cut img { width: 78%; height: auto; max-height: 84%; object-fit: contain; filter: drop-shadow(0 22px 26px rgba(26,27,29,.18)); }
.pd-slide--photo img { width: 100%; height: 100%; object-fit: cover; }
.pd-slide--photo { cursor: zoom-in; }
.pd-stage .cc-badges { left: 14px; top: 14px; }
.pd-stage .cc-wish { position: absolute; right: 14px; top: 14px; z-index: 3; width: 40px; height: 40px; }
.pd-arrow { position: absolute; top: 50%; z-index: 3; width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,.88); color: var(--ink); display: grid; place-items: center; transform: translateY(-50%); box-shadow: 0 6px 16px -8px rgba(26,27,29,.4); transition: background-color .3s ease, color .3s ease, opacity .3s ease; }
.pd-arrow:hover { background: var(--ink); color: var(--bone); }
.pd-arrow svg { width: 16px; height: 16px; }
.pd-arrow--prev { left: 12px; } .pd-arrow--prev svg { transform: scaleX(-1); }
.pd-arrow--next { right: 12px; }
.pd-zoom { position: absolute; right: 14px; bottom: 14px; z-index: 3; width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,.88); color: var(--ink); display: grid; place-items: center; transition: background-color .3s ease, color .3s ease; }
.pd-zoom:hover { background: var(--ink); color: var(--bone); }
.pd-zoom svg { width: 18px; height: 18px; }
.pd-count { position: absolute; left: 14px; bottom: 16px; z-index: 3; font-size: .6875rem; font-weight: 600; letter-spacing: .08em; padding: 5px 9px; border-radius: 999px; background: rgba(255,255,255,.88); color: var(--ink); font-variant-numeric: tabular-nums; }
.pd-thumbs { display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none; padding: 2px; order: 1; }
.pd-thumbs::-webkit-scrollbar { display: none; }
.pd-thumb { flex: 0 0 64px; width: 64px; height: 64px; border-radius: 10px; overflow: hidden; background: #F3F1EC; border: 1px solid transparent; display: grid; place-items: center; opacity: .72; transition: opacity .3s ease, border-color .3s ease; }
.pd-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.pd-thumb--cut img { width: 80%; height: 80%; object-fit: contain; }
.pd-thumb:hover { opacity: 1; }
.pd-thumb.is-on { border-color: var(--ink); opacity: 1; }
.pd-thumb.is-off { display: none; }
@media (min-width: 1024px) { .pd-gallery { grid-template-columns: 72px minmax(0, 1fr); align-items: start; } .pd-thumbs { order: -1; flex-direction: column; overflow: visible; } .pd-thumb { flex-basis: auto; width: 68px; height: 68px; } }
/* buy column */
.pd-buy { display: grid; gap: 18px; align-content: start; }
@media (min-width: 1024px) { .pd-gallery { position: sticky; top: calc(var(--nav-h) + 20px); } }
.pd-kicker { font-size: .75rem; letter-spacing: .2em; text-transform: uppercase; color: var(--fg-2); }
.pd-name { font-family: var(--font-display); font-weight: 300; font-size: clamp(1.9rem, 1.3rem + 1.8vw, 2.9rem); line-height: 1.08; letter-spacing: -.012em; text-wrap: balance; margin-top: -6px; }
.pd-price { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.pd-price b { font-size: 1.6rem; font-weight: 700; color: var(--accent-deep); font-variant-numeric: tabular-nums; }
.pd-price s { color: var(--fg-2); font-size: .9375rem; }
.pd-save { font-size: .6875rem; font-weight: 600; line-height: 1; padding: 5px 8px; border-radius: 4px; background: #5A1E1A; color: var(--bone); }
.pd-tag { font-family: var(--font-serif); font-style: italic; font-size: 1.05rem; color: var(--fg-2); margin-top: -6px; }
.pd-opt { display: grid; gap: 10px; }
.pd-opt-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; font-size: .8125rem; }
.pd-opt-head b { font-weight: 600; }
.pd-opt-head b span { font-weight: 400; color: var(--fg-2); }
.pd-opt-head button { font-size: .8125rem; color: var(--accent-deep); text-decoration: underline; text-underline-offset: 3px; }
.pd-sw { width: 34px; height: 34px; }
.pd-sw i { width: 24px; height: 24px; }
.pd-sizes { display: flex; flex-wrap: wrap; gap: 8px; }
.pd-size { position: relative; min-width: 50px; height: 40px; padding: 0 12px; border: 1px solid var(--line-strong); border-radius: 10px; display: grid; place-items: center; font-size: .875rem; font-weight: 500; cursor: pointer; transition: background-color .25s ease, color .25s ease, border-color .25s ease; }
.pd-size input { position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer; }
.pd-size:hover { border-color: var(--ink); }
.pd-size:has(input:checked) { background: var(--ink); color: var(--bone); border-color: var(--ink); }
.pd-size:has(input:focus-visible) { outline: 2px solid var(--focus); outline-offset: 3px; }
.pd-hint { font-size: .8125rem; color: var(--fg-2); }
.pd-actions { display: flex; gap: 10px; align-items: center; }
.pd-actions .qty { height: 52px; flex: none; }
.pd-actions .qty button { width: 40px; }
.pd-add { flex: 1; min-height: 52px; padding: 0 20px; border-radius: 999px; background: var(--accent-deep); color: var(--bone); font-size: .9375rem; font-weight: 600; display: inline-flex; align-items: center; justify-content: center; gap: 8px; white-space: nowrap; transition: background-color .3s ease, color .3s ease, transform .3s var(--ease-out); }
.pd-add:hover { background: var(--ink); }
.pd-add:active { transform: scale(.985); }
.pd-add.is-added { background: var(--success); }
.pd-buy .cc-wish { width: 52px; height: 52px; flex: none; }
.pd-buy .cc-wish svg { width: 20px; height: 20px; }
.pd-wa.btn { width: 100%; min-height: 48px; white-space: normal; text-align: center; line-height: 1.3; padding: 10px 20px; }
.pd-wa svg { width: 16px; height: 16px; }
.pd-stock { display: block; font-size: .8125rem; line-height: 1.5; }
.pd-stock i { display: inline-block; vertical-align: middle; margin: -2px 6px 0 0; }
.pd-stock span { color: var(--fg-2); font-weight: 400; }
.pd-perks { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 16px; padding: 18px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.pd-perks li { display: flex; gap: 10px; align-items: flex-start; font-size: .8125rem; line-height: 1.35; }
.pd-perks svg { flex: none; width: 22px; height: 22px; color: var(--accent-deep); }
.pd-perks b { display: block; font-weight: 600; }
.pd-perks span { color: var(--fg-2); }
.pd-buy .acc summary { padding: 16px 0; font-size: .9375rem; font-weight: 500; }
.pd-buy .acc .acc-body { font-size: .9375rem; line-height: 1.55; }
/* ---- what you are holding ---- */
.pd-inside { padding: clamp(8px, 2vw, 16px) 0 0; }
.pd-card { display: grid; gap: 24px; background: #F4F2EE; border-radius: 18px; padding: clamp(22px, 3vw, 44px); }
.pd-card .explore-title { font-size: clamp(1.7rem, 1.2rem + 1.6vw, 2.6rem); }
.pd-card .explore-sub { max-width: 54ch; font-size: 1rem; }
.pd-card .spec { margin-top: 22px; }
.pd-card .spec dd { font-weight: 500; }
.pd-photo { border-radius: 12px; overflow: hidden; aspect-ratio: 4 / 3; background: var(--ink); }
.pd-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
@media (min-width: 1024px) { .pd-card { grid-template-columns: 1fr 1fr; gap: clamp(28px, 4vw, 56px); align-items: center; } .pd-card--flip .pd-photo { order: -1; } }
/* ---- how it is made ---- */
.pd-made { padding: clamp(48px, 7vw, 96px) 0 clamp(8px, 2vw, 16px); }
.pd-made-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: clamp(24px, 3vw, 36px); }
.pd-made-head .explore-sub { max-width: 52ch; }
.pd-steps { display: grid; gap: 22px; grid-template-columns: 1fr; }
.pd-step { border-top: 1px solid var(--line-strong); padding-top: 16px; }
.pd-step em { font-family: var(--font-display); font-style: normal; font-weight: 300; font-size: 1.9rem; line-height: 1; color: var(--accent-deep); }
.pd-step b { display: block; margin-top: 10px; font-weight: 600; font-size: 1rem; }
.pd-step p { margin-top: 6px; font-size: .9375rem; line-height: 1.5; color: var(--fg-2); }
@media (min-width: 640px) { .pd-steps { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1024px) { .pd-steps { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 28px; } }
/* ---- you may also like ---- */
.pd-more { padding: clamp(48px, 7vw, 96px) 0 0; }
.pd-more-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; margin-bottom: clamp(20px, 3vw, 28px); }
.pd-more .cc-track { --rail-w: calc((100% - 12px) / 2); }
.pd-more .wrap:not(.has-overflow) .rail-nav { visibility: hidden; }
@media (min-width: 1024px) { .pd-more .cc-track { --rail-w: calc((100% - 60px) / 4); gap: 20px; } }
@media (min-width: 640px) and (max-width: 1023px) { .pd-more .cc-track { --rail-w: calc((100% - 32px) / 3); gap: 16px; } }
/* ---- sticky bar (phones) ---- */
.pd-bar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 40; display: flex; gap: 12px; align-items: center; padding: 10px var(--gutter) calc(10px + env(safe-area-inset-bottom)); background: rgba(239,237,230,.94); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-top: 1px solid var(--line); transform: translateY(110%); transition: transform .4s var(--ease-out); }
.pd-bar.is-on { transform: none; }
.pd-bar-info { flex: 1; min-width: 0; display: grid; }
.pd-bar-name { font-size: .875rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pd-bar-price { font-size: .875rem; font-weight: 700; color: var(--accent-deep); }
.pd-bar .pd-add { flex: none; min-height: 46px; padding: 0 22px; }
@media (min-width: 1024px) { .pd-bar { display: none; } }
/* ---- lightbox ---- */
.pd-lb { position: fixed; inset: 0; z-index: 90; background: rgba(26,27,29,.96); color: var(--bone); display: grid; place-items: center; opacity: 0; visibility: hidden; transition: opacity .35s ease, visibility 0s linear .35s; }
.pd-lb.is-open { opacity: 1; visibility: visible; transition-delay: 0s; }
.pd-lb img { max-width: 92vw; max-height: 84svh; width: auto; height: auto; object-fit: contain; border-radius: 8px; }
.pd-lb .icon-btn { position: absolute; top: 14px; right: 14px; color: var(--bone); }
.pd-lb .rail-btn { position: absolute; top: 50%; transform: translateY(-50%); color: var(--bone); border-color: rgba(239,237,230,.4); }
.pd-lb .rail-btn:hover { background: var(--bone); color: var(--ink); }
.pd-lb .lb-prev { left: 14px; } .pd-lb .lb-prev svg { transform: scaleX(-1); }
.pd-lb .lb-next { right: 14px; }
.pd-lb .lb-count { position: absolute; bottom: 18px; left: 0; right: 0; text-align: center; font-size: .75rem; letter-spacing: .14em; color: rgba(239,237,230,.7); font-variant-numeric: tabular-nums; }
/* ---- size guide dialog ---- */
.pd-dlg-backdrop { position: fixed; inset: 0; z-index: 95; background: rgba(26,27,29,.55); opacity: 0; visibility: hidden; transition: opacity .35s ease, visibility 0s linear .35s; }
.pd-dlg-backdrop.is-open { opacity: 1; visibility: visible; transition-delay: 0s; }
.pd-dlg { position: fixed; z-index: 96; left: 50%; top: 50%; width: min(520px, 92vw); max-height: 86svh; overflow: auto; background: var(--bone); color: var(--ink); border-radius: 18px; padding: clamp(24px, 4vw, 40px); transform: translate(-50%, -50%) scale(.96); opacity: 0; visibility: hidden; transition: transform .45s var(--ease-out), opacity .35s ease, visibility 0s linear .45s; }
.pd-dlg.is-open { transform: translate(-50%, -50%) scale(1); opacity: 1; visibility: visible; transition-delay: 0s; }
.pd-dlg .icon-btn { position: absolute; top: 10px; right: 10px; }
.pd-dlg h2 { font-family: var(--font-display); font-weight: 300; font-size: 1.8rem; line-height: 1.1; margin-top: 8px; }
.pd-dlg ol { counter-reset: s; display: grid; gap: 14px; margin-top: 20px; }
.pd-dlg ol li { display: grid; grid-template-columns: 2.4em 1fr; gap: 10px; counter-increment: s; font-size: .9375rem; line-height: 1.5; }
.pd-dlg ol li::before { content: "0" counter(s); font-family: var(--font-display); font-size: 1.4rem; line-height: 1.1; color: var(--accent-deep); }
.pd-dlg .pd-sizes { margin-top: 18px; }
.pd-dlg .pd-sizes span { min-width: 44px; height: 36px; border: 1px solid var(--line-strong); border-radius: 8px; display: grid; place-items: center; font-size: .8125rem; font-weight: 500; }
@media (max-width: 767px) {
  .pd-top { padding-top: calc(var(--nav-top) + 10px); }
  .pd-stage { border-radius: 12px; }
  .pd-perks { grid-template-columns: 1fr 1fr; }
  .pd-made-head, .pd-more-head { flex-direction: column; align-items: flex-start; }
  .pd-buy .cc-wish { display: none; }
}
'''

JS = r'''
function initProduct() {
  const S = window.STAGR, G = S.gsap, ST = window.ScrollTrigger, $ = S.$, $$ = S.$$, reduced = S.reduced;
  const P = __PRODUCT__;
  const desktop = () => window.matchMedia("(min-width: 1024px)").matches;
  let colour = P.defaultColour, size = P.size, qty = 1, idx = 0;

  /* ---- gallery ---- */
  const stage = $("[data-stage]"), slides = $$("[data-slide]"), thumbsEl = $("[data-thumbs]"), thumbs = $$("[data-thumb]"), count = $("[data-count]");
  const vis = () => slides.filter((s) => !s.classList.contains("is-off"));
  function show(i, animate) {
    const v = vis(); if (!v.length) return;
    idx = (i + v.length) % v.length;
    const s = v[idx];
    slides.forEach((x) => x.classList.toggle("is-on", x === s));
    thumbs.forEach((t) => t.classList.toggle("is-on", t.dataset.thumb === s.dataset.slide));
    if (count) count.textContent = (idx + 1) + " / " + v.length;
    const t = thumbs.find((x) => x.dataset.thumb === s.dataset.slide);
    if (t && thumbsEl) { const r = t.getBoundingClientRect(), b = thumbsEl.getBoundingClientRect(); if (desktop()) { if (r.top < b.top || r.bottom > b.bottom) t.scrollIntoView({ block: "nearest" }); } else if (r.left < b.left || r.right > b.right) thumbsEl.scrollTo({ left: t.offsetLeft - 8, behavior: "smooth" }); }
    if (animate !== false && G && !reduced) G.fromTo(s.querySelector("img"), { scale: 1.04, opacity: .5 }, { scale: 1, opacity: 1, duration: .6, ease: "power2.out", clearProps: "transform,opacity" });
  }
  function applyColour() {
    slides.forEach((s) => { const c = s.dataset.colour; s.classList.toggle("is-off", !!c && c !== colour); });
    thumbs.forEach((t) => { const c = t.dataset.colour; t.classList.toggle("is-off", !!c && c !== colour); });
    $$("[data-colour-label]").forEach((e) => e.textContent = colour);
    sync(); show(0);
  }
  function sync() { $$("[data-add-main]").forEach((b) => { b.dataset.colour = colour; if (size) b.dataset.size = size; b.dataset.qty = qty; }); }
  thumbs.forEach((t) => t.addEventListener("click", () => { const v = vis(); const i = v.findIndex((s) => s.dataset.slide === t.dataset.thumb); if (i >= 0) show(i); }));
  $$("[data-prev]").forEach((b) => b.addEventListener("click", () => show(idx - 1)));
  $$("[data-next]").forEach((b) => b.addEventListener("click", () => show(idx + 1)));
  // swipe on the stage
  let sx = null, sy = null;
  stage.addEventListener("pointerdown", (e) => { if (e.target.closest("button")) return; sx = e.clientX; sy = e.clientY; }, { passive: true });
  stage.addEventListener("pointerup", (e) => { if (sx === null) return; const dx = e.clientX - sx, dy = e.clientY - sy; sx = sy = null; if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) show(dx < 0 ? idx + 1 : idx - 1); }, { passive: true });
  stage.addEventListener("pointercancel", () => { sx = sy = null; });

  /* ---- lightbox ---- */
  const lb = $("[data-lb]"), lbImg = $("img", lb), lbCount = $("[data-lb-count]"); let lbOpen = false, lbLast = null;
  const lbShow = () => { const v = vis(); const img = v[idx].querySelector("img"); lbImg.src = img.dataset.full || img.currentSrc || img.src; lbImg.alt = img.alt; lbCount.textContent = (idx + 1) + " / " + v.length; if (G && !reduced) G.fromTo(lbImg, { opacity: 0, scale: .985 }, { opacity: 1, scale: 1, duration: .45, ease: "power3.out", clearProps: "transform,opacity" }); };
  const openLb = () => { lbLast = document.activeElement; lb.classList.add("is-open"); lb.setAttribute("aria-hidden", "false"); lbOpen = true; S.lock("lightbox"); lbShow(); setTimeout(() => $("[data-lb-close]", lb).focus(), 300); };
  const closeLb = () => { if (!lbOpen) return; lb.classList.remove("is-open"); lb.setAttribute("aria-hidden", "true"); lbOpen = false; S.unlock("lightbox"); lbLast && lbLast.focus && lbLast.focus(); };
  $("[data-zoom]").addEventListener("click", openLb);
  slides.forEach((s) => s.addEventListener("click", (e) => { if (s.classList.contains("pd-slide--photo") && desktop() && !e.target.closest("button")) openLb(); }));
  $("[data-lb-close]", lb).addEventListener("click", closeLb);
  $("[data-lb-prev]", lb).addEventListener("click", () => { show(idx - 1, false); lbShow(); });
  $("[data-lb-next]", lb).addEventListener("click", () => { show(idx + 1, false); lbShow(); });
  lb.addEventListener("click", (e) => { if (e.target === lb) closeLb(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeLb(); closeDlg(); } if (!lbOpen) return; if (e.key === "ArrowRight") { show(idx + 1, false); lbShow(); } if (e.key === "ArrowLeft") { show(idx - 1, false); lbShow(); } });

  /* ---- options ---- */
  $$('input[name="pd-colour"]').forEach((r) => r.addEventListener("change", () => { colour = r.value; applyColour(); }));
  $$('input[name="pd-size"]').forEach((r) => r.addEventListener("change", () => { size = r.value; $$("[data-size-label]").forEach((e) => e.textContent = size); sync(); }));
  const qtyOut = $("[data-qty-out]");
  $$("[data-qty-inc]").forEach((b) => b.addEventListener("click", () => { qty = Math.min(99, qty + 1); qtyOut.textContent = qty; sync(); }));
  $$("[data-qty-dec]").forEach((b) => b.addEventListener("click", () => { qty = Math.max(1, qty - 1); qtyOut.textContent = qty; sync(); }));
  applyColour(); show(0, false);

  /* ---- size guide ---- */
  const dlg = $("[data-dlg]"), bd = $("[data-dlg-backdrop]"); let dlgOpen = false;
  const openDlg = () => { if (!dlg) return; dlgOpen = true; dlg.classList.add("is-open"); bd.classList.add("is-open"); dlg.setAttribute("aria-hidden", "false"); S.lock("dialog"); setTimeout(() => $("[data-dlg-close]", dlg).focus(), 300); };
  const closeDlg = () => { if (!dlgOpen) return; dlgOpen = false; dlg.classList.remove("is-open"); bd.classList.remove("is-open"); dlg.setAttribute("aria-hidden", "true"); S.unlock("dialog"); };
  $$("[data-dlg-open]").forEach((b) => b.addEventListener("click", openDlg));
  $$("[data-dlg-close], [data-dlg-backdrop]").forEach((b) => b.addEventListener("click", closeDlg));

  /* ---- sticky bar on phones ---- */
  const bar = $("[data-bar]"), mainBtn = $(".pd-buy [data-add-main]");
  if (bar && mainBtn) { const check = () => { const r = mainBtn.getBoundingClientRect(); bar.classList.toggle("is-on", r.bottom < 0 && !desktop()); }; window.addEventListener("scroll", check, { passive: true }); window.addEventListener("resize", check); check(); }

  /* ---- motion ---- */
  const top = [stage, thumbsEl].filter(Boolean), buy = $$(".pd-buy > *");
  if (G && !reduced) { G.set(top, { opacity: 0, y: 18 }); G.set(buy, { opacity: 0, y: 14 }); }
  S.onLoaderDone.push(() => { if (!G || reduced) return; G.to(top, { opacity: 1, y: 0, duration: .8, ease: "power3.out", stagger: .08, clearProps: "transform,opacity" }); G.to(buy, { opacity: 1, y: 0, duration: .7, ease: "power3.out", stagger: .05, delay: .15, clearProps: "transform,opacity" }); });
  $$(".pd-inside, .pd-made, .pd-more, #why, footer").forEach((el) => S.initReveals(el));
  S.initRails(document);
  window.addEventListener("load", () => ST && ST.refresh());
}
STAGR.onReady.push(initProduct);
'''

PERK_ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><rect x="3" y="7" width="18" height="13" rx="1"/><path d="M3 11h18M8 7V4h8v3"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17" r="1.6"/><circle cx="17" cy="17" r="1.6"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M4 12a8 8 0 1 0 2.3-5.7"/><path d="M4 4v5h5"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M13 8l3 3"/></svg>',
]


def clean(v):
    """Strip the editorial notes carried in the data strings."""
    if not v:
        return ""
    for cut in (" (old page", " — please", " — please", " (assumed"):
        v = v.split(cut)[0]
    return v.strip()


def product_page(ctx, p):
    P = ctx["products"]
    B = ctx["brand"]
    I = ctx["icon"]
    TAGS = ctx["tags"]
    esc = ctx["esc"]
    fmt = lambda n: "Rs " + format(n, ",d")
    is_belt = p["line"] == "belt"
    line_title = "Belts" if is_belt else "Wallets"
    line_url = "belts.html" if is_belt else "wallets.html"
    style = p["style"] or "Belt"
    num = "STAGR." + str(P.index(p) + 1).zfill(2)
    off = round(100 - p["price"] / p["compareAtPrice"] * 100) if p.get("compareAtPrice") else 0
    tags = TAGS.get(p["id"], [])
    badges = (f'<span class="cc-badge cc-sale">Sale -{off}%</span>' if off else "") + ('<span class="cc-badge cc-best">&#9733; Bestseller</span>' if "best" in tags else "") + ('<span class="cc-badge cc-new">New in</span>' if "new" in tags and "best" not in tags else "")
    heart = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 20.5s-7.5-4.6-7.5-10A4.2 4.2 0 0 1 12 8.2a4.2 4.2 0 0 1 7.5 2.3c0 5.4-7.5 10-7.5 10z"/></svg>'
    wa = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4V5z"/></svg>'
    zoom = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M11 8v6M8 11h6"/></svg>'

    # ---- gallery: cutouts (per colour) then real frames from the shoot ----
    cuts = ctx["cutouts"](p)
    photos = [f"assets/pdp/{p['id']}-{n}" for n in (1, 2, 3) if os.path.exists(os.path.join(SITE, f"assets/pdp/{p['id']}-{n}.jpg"))]
    slides, thumbs = [], []
    one_colour = len({c["colour"] for c in cuts}) == 1   # reversible belts share one set of cutouts
    for i, c in enumerate(cuts):
        key = f"cut-{i}"
        slides.append(f'<figure class="pd-slide pd-slide--cut" data-slide="{key}"{"" if one_colour else f" data-colour=\"{c["colour"]}\""}><img src="{c["src"]}" data-full="{c["src"]}" alt="{esc(p["name"])} in {c["colour"].lower()}" width="1200" height="1200" {"fetchpriority=high" if i == 0 else "loading=lazy"} draggable="false"></figure>')
        thumbs.append(f'<button type="button" class="pd-thumb pd-thumb--cut" data-thumb="{key}"{"" if one_colour else f" data-colour=\"{c["colour"]}\""} aria-label="{esc(p["name"])} in {c["colour"].lower()}, view {i + 1}"><img src="{c["small"]}" alt="" width="120" height="120" loading="lazy" draggable="false"></button>')
    photo_alts = ["in the workshop", "open, with cards" if not is_belt else "coiled, from the shoot", "a closer look"]
    for i, ph in enumerate(photos):
        key = f"photo-{i}"
        slides.append(f'<figure class="pd-slide pd-slide--photo" data-slide="{key}"><img src="{ph}-800.jpg" srcset="{ph}-800.jpg 800w, {ph}.jpg 1600w" sizes="(min-width: 1024px) 50vw, 100vw" data-full="{ph}.jpg" alt="{esc(p["name"])}, {photo_alts[i]}" width="1600" height="1200" loading="lazy" draggable="false"></figure>')
        thumbs.append(f'<button type="button" class="pd-thumb" data-thumb="{key}" aria-label="Photograph {i + 1}"><img src="{ph}-800.jpg" alt="" width="120" height="120" loading="lazy" draggable="false"></button>')

    # ---- options ----
    swatches = "".join(f'<label class="cc-sw pd-sw" title="{c}"><input type="radio" name="pd-colour" value="{c}" {"checked" if c == p["defaultColour"] else ""}><i style="--sw:{ctx["swatch"].get(c, "#6E4328")}"></i><span class="sr-only">{c}</span></label>' for c in p["colours"])
    size_default = None
    sizes_html = ""
    if p.get("sizes"):
        opts = p["sizes"]["options"]
        size_default = 34 if 34 in opts else opts[0]
        sizes_html = f'''<div class="pd-opt"><div class="pd-opt-head"><b>{p["sizes"]["label"]} <span>· <span data-size-label>{size_default}</span></span></b><button type="button" data-dlg-open>Size guide</button></div><div class="pd-sizes">{"".join(f'<label class="pd-size"><input type="radio" name="pd-size" value="{s}" {"checked" if s == size_default else ""}>{s}</label>' for s in opts)}</div><p class="pd-hint">Measured from the buckle bar to the hole you use. Between two sizes, take the larger.</p></div>'''
    perks = "".join(f'<li>{PERK_ICONS[i]}<div><b>{t["title"]}</b><span>{t["sub"]}</span></div></li>' for i, t in enumerate(B["trust"]["items"]))
    d = p["details"]
    acc = "".join(f'<details{" open" if i == 0 else ""}><summary>{t}<span class="plus"></span></summary><div class="acc-body"><p>{b}</p></div></details>' for i, (t, b) in enumerate([
        ("Product details", d["productDetails"]), ("Leather", d["leatherSpecification"]), ("Care", d["care"]), ("Delivery and returns", d["deliveryAndReturns"])]))
    wa_link = B["contact"]["whatsapp"]["link"]
    wa_href = wa_link + ("&" if "?" in wa_link else "?") + "text=" + esc(f"Hello Stagr, I have a question about the {p['name']}.").replace(" ", "%20")

    # ---- spec card ----
    m = p["materials"]
    rows = [("Leather", "Crazy horse, full grain cowhide")]
    rows.append(("Hardware", clean(m["hardware"])) if "hardware" in m else ("Lining", clean(m.get("lining"))))
    rows += [("Thickness", clean(m["thickness"])), ("Stitching", "Saddle stitch, by hand"), ("Colours", " / ".join(p["colours"])),
             ("Sizes", f'{p["sizes"]["options"][0]} to {p["sizes"]["options"][-1]}') if is_belt else ("Fit", "One size"), ("Origin", B["origin"])]
    spec = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows if v)
    inside_h = "Cut along the spine, finished by hand" if is_belt else "Folded, skived, stitched by hand"
    inside_body = d["productDetails"] + " " + ("Edges bevelled, sanded and burnished, then sealed with beeswax." if is_belt else "One row of saddle stitch, two needles, waxed linen thread.")
    inside_photo = photos[1] if len(photos) > 1 else (photos[0] if photos else "")

    # ---- making steps ----
    steps = "".join(f'<li class="pd-step" data-reveal data-delay="{i * .08}"><em>{s["n"]}</em><b>{s["title"]}</b><p>{s["body"]}</p></li>' for i, s in enumerate(B["craft"]["steps"]))

    # ---- more pieces: the rest of this line first, then the other line ----
    others = [x for x in P if x["line"] == p["line"] and x["id"] != p["id"]] + [x for x in P if x["line"] != p["line"]]
    more = "".join(ctx["ccard"](ctx, x, P.index(x)) for x in others[:8])

    body = f'''
<section class="pd-top on-bone" aria-labelledby="pd-title">
  <div class="wrap">
    <nav class="pd-crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i><a href="{line_url}">{line_title}</a><i>/</i><span aria-current="page">{esc(p["name"].split(" ")[0])}</span></nav>
    <div class="pd-grid">
      <div class="pd-gallery">
        <div class="pd-thumbs" data-thumbs role="tablist" aria-label="Product images">{"".join(thumbs)}</div>
        <div class="pd-stage" data-stage>
          {"".join(slides)}
          <span class="cc-badges">{badges}</span>
          <button type="button" class="cc-wish" data-wish="{p["id"]}" aria-pressed="false" aria-label="Save {esc(p["name"])}">{heart}</button>
          <button type="button" class="pd-arrow pd-arrow--prev" data-prev aria-label="Previous image">{I["arrow"]}</button>
          <button type="button" class="pd-arrow pd-arrow--next" data-next aria-label="Next image">{I["arrow"]}</button>
          <span class="pd-count" data-count>1 / {len(slides)}</span>
          <button type="button" class="pd-zoom" data-zoom aria-label="Open image full screen">{zoom}</button>
        </div>
      </div>
      <aside class="pd-buy">
        <p class="pd-kicker">{style} · {line_title} · {num}</p>
        <h1 class="pd-name" id="pd-title">{esc(p["name"]).replace("-", "&#8209;")}</h1>
        <p class="pd-price"><b>{fmt(p["price"])}</b>{f'<s>{fmt(p["compareAtPrice"])}</s><span class="pd-save">Save {off}%</span>' if off else ""}</p>
        <p class="pd-tag">{esc(p["tagline"])}</p>
        <div class="pd-opt"><div class="pd-opt-head"><b>Colour <span>· <span data-colour-label>{p["defaultColour"]}</span></span></b><span>{len(p["colours"])} colour{"s" if len(p["colours"]) > 1 else ""}</span></div><div class="opts cc-opts">{swatches}</div></div>
        {sizes_html}
        <div class="pd-actions">
          <div class="qty"><button type="button" data-qty-dec aria-label="Decrease quantity">−</button><span data-qty-out>1</span><button type="button" data-qty-inc aria-label="Increase quantity">+</button></div>
          <button type="button" class="pd-add" data-add="{p["id"]}" data-add-main data-colour="{p["defaultColour"]}" {f'data-size="{size_default}"' if size_default else ""} data-qty="1"><span aria-hidden="true">+</span> Add to cart</button>
          <button type="button" class="cc-wish" data-wish="{p["id"]}" aria-pressed="false" aria-label="Save {esc(p["name"])}">{heart}</button>
        </div>
        <a class="btn btn--ghost pd-wa" href="{wa_href}" target="_blank" rel="noopener">{wa} Ask on WhatsApp</a>
        <p class="cc-stock pd-stock"><i></i>In stock <span>· ships in {B["shipping"]["deliveryTime"]} · cash on delivery</span></p>
        <ul class="pd-perks" role="list">{perks}</ul>
        <div class="acc" id="details">{acc}</div>
      </aside>
    </div>
  </div>
</section>

<section class="pd-inside on-bone" aria-labelledby="pd-inside-title">
  <div class="wrap pd-card">
    <div>
      <p class="label" data-reveal>What you are holding</p>
      <h2 class="explore-title" id="pd-inside-title" data-reveal data-delay=".05">{inside_h}</h2>
      <p class="explore-sub" data-reveal data-delay=".1">{inside_body}</p>
      <dl class="spec" data-reveal data-delay=".15">{spec}</dl>
    </div>
    {f'<figure class="pd-photo" data-reveal data-delay=".1"><img src="{inside_photo}-800.jpg" srcset="{inside_photo}-800.jpg 800w, {inside_photo}.jpg 1600w" sizes="(min-width: 1024px) 45vw, 100vw" alt="{esc(p["name"])}, from the shoot" width="1600" height="1200" loading="lazy"></figure>' if inside_photo else ""}
  </div>
</section>

<section class="pd-made on-bone" aria-labelledby="pd-made-title">
  <div class="wrap">
    <div class="pd-made-head">
      <div><p class="label" data-reveal>How it is made</p><h2 class="explore-title" id="pd-made-title" data-reveal data-delay=".05">{B["craft"]["heading"]}</h2><p class="explore-sub" data-reveal data-delay=".1">{B["craft"]["body"]}</p></div>
      <a class="btn btn--ghost" href="about.html#craft" data-reveal data-delay=".15">The workshop {I["arrow"]}</a>
    </div>
    <ol class="pd-steps" role="list">{steps}</ol>
  </div>
</section>

<section class="pd-more on-bone" aria-labelledby="pd-more-title">
  <div class="wrap" data-rail>
    <div class="pd-more-head">
      <div><p class="label" data-reveal>You may also like</p><h2 class="explore-title" id="pd-more-title" data-reveal data-delay=".05">More from the bench</h2></div>
      <div class="rail-nav" data-reveal data-delay=".1"><button type="button" class="rail-btn" data-rail-prev aria-label="Previous" style="transform:scaleX(-1)">{I["arrow"]}</button><button type="button" class="rail-btn" data-rail-next aria-label="Next">{I["arrow"]}</button></div>
    </div>
    <div class="rail-track cc-track" data-rail-track data-reveal data-delay=".1">{more}</div>
  </div>
</section>

{ctx["why"](ctx)}

<div class="pd-bar" data-bar aria-hidden="true"><div class="pd-bar-info"><span class="pd-bar-name">{esc(p["name"])}</span><span class="pd-bar-price">{fmt(p["price"])}</span></div><button type="button" class="pd-add" data-add="{p["id"]}" data-add-main data-colour="{p["defaultColour"]}" {f'data-size="{size_default}"' if size_default else ""} data-qty="1">Add to cart</button></div>

<div class="pd-lb" data-lb role="dialog" aria-modal="true" aria-label="Image viewer" aria-hidden="true">
  <button type="button" class="icon-btn" data-lb-close aria-label="Close">{I["close"]}</button>
  <button type="button" class="rail-btn lb-prev" data-lb-prev aria-label="Previous image">{I["arrow"]}</button>
  <img src="" alt="" width="1600" height="1200">
  <button type="button" class="rail-btn lb-next" data-lb-next aria-label="Next image">{I["arrow"]}</button>
  <div class="lb-count" data-lb-count></div>
</div>

{f"""<div class="pd-dlg-backdrop" data-dlg-backdrop aria-hidden="true"></div>
<div class="pd-dlg" data-dlg role="dialog" aria-modal="true" aria-labelledby="pd-sg-title" aria-hidden="true" data-lenis-prevent>
  <button type="button" class="icon-btn" data-dlg-close aria-label="Close">{I["close"]}</button>
  <p class="label">Size guide</p>
  <h2 id="pd-sg-title">Measure the belt you wear</h2>
  <ol>{"".join(f"<li>{s}</li>" for s in p["sizes"]["guide"])}</ol>
  <div class="pd-sizes">{"".join(f"<span>{s}</span>" for s in p["sizes"]["options"])}</div>
  <p class="pd-hint" style="margin-top:16px">Still unsure? Message us on WhatsApp with the belt you wear today.</p>
</div>""" if p.get("sizes") else ""}
'''
    data = {"id": p["id"], "defaultColour": p["defaultColour"], "size": size_default}
    return {
        "file": f"product-{p['id']}.html",
        "key": line_title.lower(),
        "title": f'{p["name"]} — STAGR.',
        "description": f'{p["name"]}. {p["tagline"]} {fmt(p["price"])}, cash on delivery across Pakistan.',
        "css": CSS,
        "body": body,
        "js": JS.replace("__PRODUCT__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")),
        "header_dark": False,
        "shop_href": line_url,
    }


def render(ctx):
    pages = [product_page(ctx, p) for p in ctx["products"]]
    ids = [p["id"] for p in ctx["products"]]
    # product.html resolves ?id=<slug> to the static page (falls back to the first product)
    pages.append({
        "file": "product.html",
        "key": "product",
        "title": "Product — STAGR.",
        "css": ".pd-resolve { padding: calc(var(--nav-top) + 48px) 0 96px; }",
        "body": f'<section class="pd-resolve on-bone"><div class="wrap"><p class="label">Product</p><h1 class="explore-title" style="margin-top:14px">Opening the piece…</h1><p class="explore-sub" style="margin-top:14px">If nothing happens, pick one: {" · ".join(f"<a href=product-{i}.html>{i}</a>" for i in ids)}.</p></div></section>',
        "js": f'(function(){{var ids={json.dumps(ids)};var id=new URLSearchParams(location.search).get("id");location.replace("product-"+(ids.indexOf(id)>=0?id:ids[0])+".html"+location.hash);}})();',
        "header_dark": False,
    })
    return pages
