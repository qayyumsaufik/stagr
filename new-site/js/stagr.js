/* ==========================================================================
   STAGR — shared runtime v2 (ported from the STILL reference choreography)
   Lenis smooth scroll, nav, fullscreen menu, custom cursor, loader with
   popping pills + wordmark fly-in, reveal helpers, blooms, carousel helper,
   cart drawer with cash-on-delivery checkout via WhatsApp, magnetic buttons.
   GSAP 3.13 (ScrollTrigger, SplitText, DrawSVG, Flip, Observer) from cdnjs.
   ========================================================================== */
(function () {
  "use strict";
  const html = document.documentElement;
  html.classList.remove("no-js"); html.classList.add("js");

  const G = window.gsap || null, ST = window.ScrollTrigger || null;
  if (G) { const p = [ST, window.SplitText, window.DrawSVGPlugin, window.Flip, window.Observer].filter(Boolean); if (p.length) G.registerPlugin.apply(G, p); }
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const isRendered = (el) => el.getClientRects().length > 0;
  const mobileQuery = window.matchMedia("(max-width: 767px)");
  const isMobile = mobileQuery.matches;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = window.matchMedia("(pointer: fine)").matches;
  const DATA = window.STAGR_DATA || { products: [], brand: {} };
  // Desktop and mobile run different scroll choreography; crossing the breakpoint restarts.
  mobileQuery.addEventListener("change", () => window.location.reload());

  const S = (window.STAGR = { gsap: G, isMobile, reduced, fine, data: DATA, $, $$, clamp, isRendered,
    fmt: (n) => "Rs " + Number(n).toLocaleString("en-PK"), product: (id) => DATA.products.find((p) => p.id === id), onReady: [], onLoaderDone: [] });

  /* ---------------- theme ---------------- */
  const THEME_KEY = "stagr-theme";
  S.isDark = () => { const t = html.getAttribute("data-theme"); return t ? t === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches; };
  S.toggleTheme = () => { const t = S.isDark() ? "light" : "dark"; html.setAttribute("data-theme", t); try { localStorage.setItem(THEME_KEY, t); } catch (e) {} $$(".theme-toggle").forEach((b) => b.setAttribute("aria-pressed", String(t === "dark"))); };
  $$(".theme-toggle").forEach((b) => { b.setAttribute("aria-pressed", String(S.isDark())); b.addEventListener("click", S.toggleTheme); });

  /* ---------------- smooth scroll + locks ---------------- */
  let lenis = null; const locks = new Set();
  if (window.Lenis && !reduced) {
    lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true });
    if (G) { if (ST) lenis.on("scroll", ST.update); G.ticker.add((t) => lenis.raf(t * 1000)); G.ticker.lagSmoothing(0); }
    else { const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  S.lenis = lenis;
  S.lock = (reason) => { locks.add(reason); html.style.overflow = "hidden"; document.body.style.overflow = "hidden"; if (lenis) lenis.stop(); };
  S.unlock = (reason) => { locks.delete(reason); if (locks.size) return; html.style.overflow = ""; document.body.style.overflow = ""; if (lenis) lenis.start(); };
  S.scrollTo = (target, duration) => {
    if (lenis) lenis.scrollTo(target, { duration: duration || 1.2, offset: typeof target === "number" ? 0 : -8 });
    else if (typeof target === "number") window.scrollTo({ top: target, behavior: "smooth" });
    else { const el = typeof target === "string" ? $(target) : target; el && el.scrollIntoView({ behavior: "smooth" }); }
  };
  S.scrollToProgress = (trigger, p, d) => { if (trigger) S.scrollTo(trigger.start + (trigger.end - trigger.start) * p, d); };

  /* ---------------- reveal helpers ---------------- */
  function scrollReveal(el) {
    const delay = parseFloat(el.dataset.delay || "0");
    if (!G || reduced) { el.classList.add("is-revealed"); return; }
    G.fromTo(el, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out", delay, scrollTrigger: { trigger: el, start: "top 85%", toggleActions: "play none none none" }, onComplete: () => el.classList.add("is-revealed") });
  }
  function textReveal(el) {
    if (!G || !window.SplitText || reduced) { el.classList.add("is-revealed"); return; }
    const split = el.dataset.textReveal || "lines";
    const stagger = split === "chars" ? 0.02 : 0.09, duration = split === "chars" ? 0.8 : 0.9;
    window.SplitText.create(el, { type: split, mask: split, autoSplit: split === "lines", onSplit: (self) => G.fromTo(self[split], { yPercent: 115 }, { yPercent: 0, duration, ease: "power2.out", stagger, scrollTrigger: { trigger: el, start: el.dataset.start || "top 85%", once: true } }) });
    G.set(el, { opacity: 1 });
  }
  function illuminate(el) {
    if (!G || !window.SplitText || reduced) { el.classList.add("is-revealed"); return; }
    const dim = parseFloat(el.dataset.dim || "0.24");
    window.SplitText.create(el, { type: "words", aria: "none", onSplit: (self) => { G.set(self.words, { opacity: dim }); G.set(el, { opacity: 1 }); return G.to(self.words, { opacity: 1, ease: "none", duration: 1, stagger: 0.35, scrollTrigger: { trigger: el, start: el.dataset.start || "top 82%", end: el.dataset.end || "top 34%", scrub: true } }); } });
  }
  S.initReveals = (root) => { if (!root) return; $$("[data-reveal]", root).filter(isRendered).forEach(scrollReveal); $$("[data-text-reveal]", root).filter(isRendered).forEach(textReveal); $$("[data-illuminate]", root).filter(isRendered).forEach(illuminate); };
  S.initBlooms = () => { if (!G || reduced) return; $$("[data-bloom]").forEach((el) => G.to(el, { scale: 1.05, duration: 2, yoyo: true, repeat: -1, ease: "sine.inOut" })); };
  S.charRise = (el, vars) => window.SplitText.create(el, { type: "words,chars", mask: "words", onSplit: (self) => G.fromTo(self.chars, { yPercent: vars.from || 115 }, Object.assign({ yPercent: 0, ease: "power2.out" }, vars.to)) });
  // Tracks which card of a horizontal snap carousel sits in the middle.
  S.watchCarousel = (track, onChange) => {
    let frame = 0, active = 0;
    track.addEventListener("scroll", () => { if (frame) return; frame = requestAnimationFrame(() => { frame = 0; const cards = Array.from(track.children); if (!cards.length) return; const middle = track.scrollLeft + track.clientWidth / 2; let nearest = 0, best = Infinity; cards.forEach((c, i) => { const d = Math.abs(c.offsetLeft + c.offsetWidth / 2 - middle); if (d < best) { best = d; nearest = i; } }); if (nearest !== active) { const prev = active; active = nearest; onChange(nearest, prev); } }); }, { passive: true });
  };
  S.scrollCarouselTo = (track, i) => { const c = track.children[i]; if (c) track.scrollTo({ left: c.offsetLeft - (track.clientWidth - c.offsetWidth) / 2, behavior: "smooth" }); };
  S.magnetic = (root) => { if (!G || !fine || reduced) return; $$("[data-magnetic]", root).forEach((el) => { if (el._mag) return; el._mag = true; const k = parseFloat(el.dataset.magnetic) || 0.35; const mx = G.quickTo(el, "x", { duration: 0.4, ease: "power2.out" }), my = G.quickTo(el, "y", { duration: 0.4, ease: "power2.out" }); el.addEventListener("pointermove", (e) => { const r = el.getBoundingClientRect(); mx((e.clientX - (r.left + r.width / 2)) * k); my((e.clientY - (r.top + r.height / 2)) * k); }, { passive: true }); el.addEventListener("pointerleave", () => { mx(0); my(0); }, { passive: true }); }); };

  /* ---------------- nav + menu ---------------- */
  let menuOpen = false;
  function initNav() {
    const nav = $(".nav"); if (!nav) return;
    const menu = $(".menu");
    // The bar never hides: it only turns solid once the page has scrolled.
    const topbar = $("[data-topbar]");
    // the top bar scrolls away; the fixed nav starts beneath it and slides up to the edge as it goes
    const update = () => { const y = window.scrollY || 0; nav.classList.toggle("is-solid", y > 40); if (topbar) nav.style.top = Math.max(0, topbar.offsetHeight - y) + "px"; };
    window.addEventListener("resize", update);
    update(); window.addEventListener("scroll", update, { passive: true });
    const setMenu = (open) => { if (!menu || open === menuOpen) return; menuOpen = open; menu.classList.toggle("is-open", open); menu.setAttribute("aria-hidden", String(!open)); $$("[data-menu-open]").forEach((b) => b.setAttribute("aria-expanded", String(open))); open ? S.lock("menu") : S.unlock("menu"); update(); if (open) setTimeout(() => { const f = $("[data-menu-close]", menu); f && f.focus(); }, 300); };
    S.openMenu = () => setMenu(true); S.closeMenu = () => setMenu(false);
    // mega panels: open on hover/focus with a short delay, close on leave or Escape
    let megaTimer = null, openPanel = null;
    const panels = $$("[data-mega-panel]", nav);
    const closeMega = () => { clearTimeout(megaTimer); if (!openPanel) return; openPanel.classList.remove("is-open"); openPanel.setAttribute("aria-hidden", "true"); $$("[data-mega]", nav).forEach((li) => li.classList.remove("is-open")); openPanel = null; nav.classList.remove("is-mega"); };
    const openMega = (key) => { clearTimeout(megaTimer); const p = panels.find((x) => x.dataset.megaPanel === key); if (!p || p === openPanel) return; if (openPanel) { openPanel.classList.remove("is-open"); openPanel.setAttribute("aria-hidden", "true"); } openPanel = p; p.classList.add("is-open"); p.setAttribute("aria-hidden", "false"); $$("[data-mega]", nav).forEach((li) => li.classList.toggle("is-open", li.dataset.mega === key)); nav.classList.add("is-mega"); if (G && !reduced) G.fromTo($$(".mega-item, .mega-links a", p).filter((el) => el.offsetParent), { y: 10, opacity: 0 }, { y: 0, opacity: 1, duration: .45, stagger: .04, ease: "power2.out", overwrite: true }); };
    $$("[data-mega]", nav).forEach((li) => { li.addEventListener("pointerenter", () => { clearTimeout(megaTimer); megaTimer = setTimeout(() => openMega(li.dataset.mega), 120); }); li.addEventListener("focusin", () => openMega(li.dataset.mega)); });
    $$(".nav-main > li:not([data-mega])", nav).forEach((li) => li.addEventListener("pointerenter", () => { clearTimeout(megaTimer); megaTimer = setTimeout(closeMega, 150); }));
    nav.addEventListener("pointerleave", () => { clearTimeout(megaTimer); megaTimer = setTimeout(closeMega, 200); });
    panels.forEach((p) => { p.addEventListener("pointerenter", () => clearTimeout(megaTimer)); $$("[data-mega-tab-btn]", p).forEach((b) => b.addEventListener("click", () => { $$("[data-mega-tab-btn]", p).forEach((x) => x.setAttribute("aria-selected", String(x === b))); $$("[data-mega-tab]", p).forEach((r) => r.hidden = r.dataset.megaTab !== b.dataset.megaTabBtn); const row = $('[data-mega-tab="' + b.dataset.megaTabBtn + '"]', p); if (G && !reduced) G.fromTo($$(".mega-item, a", row), { y: 10, opacity: 0 }, { y: 0, opacity: 1, duration: .4, stagger: .04, ease: "power2.out", overwrite: true }); })); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMega(); });
    document.addEventListener("focusin", (e) => { if (!nav.contains(e.target)) closeMega(); });
    S.closeMega = closeMega;
    $$("[data-menu-open]").forEach((b) => b.addEventListener("click", () => setMenu(true)));
    $$("[data-menu-close]").forEach((b) => b.addEventListener("click", () => setMenu(false)));
    // in-page links glide with Lenis
    document.addEventListener("click", (e) => { const a = e.target.closest('a[href^="#"]'); if (!a) return; const hash = a.getAttribute("href"); if (hash === "#") return; e.preventDefault(); setMenu(false); S.scrollTo(hash === "#top" ? 0 : hash); });
  }

  /* ---------------- cursor ---------------- */
  function initCursor() {
    const root = $(".cursor"); if (!root || !fine || reduced || !G) return;
    const ring = $(".ring", root), dot = $(".dot", root), label = $(".ring span", root);
    html.classList.add("has-cursor");
    const dx = G.quickTo(dot, "x", { duration: 0.08, ease: "power2.out" }), dy = G.quickTo(dot, "y", { duration: 0.08, ease: "power2.out" });
    const rx = G.quickTo(ring, "x", { duration: 0.45, ease: "power2.out" }), ry = G.quickTo(ring, "y", { duration: 0.45, ease: "power2.out" });
    let visible = false, mode = "default";
    const show = (s) => { if (s === visible) return; visible = s; G.to([dot, ring], { opacity: s ? 1 : 0, duration: 0.25, overwrite: "auto" }); };
    const setMode = (next, text) => {
      if (text) label.textContent = text; if (next === mode) return; mode = next;
      const labeled = next === "labeled", size = labeled ? 76 : next === "interactive" ? 56 : 36;
      G.set(ring, { mixBlendMode: labeled ? "normal" : "difference" });
      G.to(ring, { width: size, height: size, marginLeft: -size / 2, marginTop: -size / 2, backgroundColor: labeled ? "rgba(26,27,29,0.92)" : "rgba(255,255,255,0)", borderColor: labeled ? "rgba(26,27,29,0)" : "rgba(255,255,255,0.55)", duration: 0.35, ease: "power2.out", overwrite: "auto" });
      G.to(label, { opacity: labeled ? 1 : 0, duration: 0.25, overwrite: "auto" });
      G.to(dot, { scale: labeled ? 0 : next === "interactive" ? 0.5 : 1, duration: 0.25, overwrite: "auto" });
    };
    window.addEventListener("pointermove", (e) => { dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY); show(true); }, { passive: true });
    window.addEventListener("pointerover", (e) => { const t = e.target; if (!t || !t.closest) return; const l = t.closest("[data-cursor-label]"); if (l) setMode("labeled", l.dataset.cursorLabel); else if (t.closest("a, button, input, textarea, select, summary, label, [role='button']")) setMode("interactive"); else setMode("default"); }, { passive: true });
    html.addEventListener("pointerleave", () => show(false));
  }

  /* ---------------- loader ---------------- */
  function initLoader(onReveal) {
    const loader = $(".loader");
    if (!loader || html.classList.contains("no-loader")) { if (loader) loader.remove(); onReveal(); return; }
    try { sessionStorage.setItem("stagr-loaded", "1"); } catch (e) {}
    const INK = "#1a1b1d", TRACK = "rgba(26,27,29,0.12)";
    const mark = $(".mark", loader), word = $(".word", loader), ldot = $(".ldot", loader), count = $(".count", loader), pills = $$(".pop", loader);
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    window.scrollTo(0, 0); S.lock("loader");
    let pillLoop = null;
    if (!G || reduced) { if (word) word.style.backgroundImage = "linear-gradient(90deg," + INK + " 0%," + INK + " 100%)"; if (ldot) ldot.style.opacity = 1; }
    else {
      G.set(pills, { opacity: 0, scale: 0.55 });
      pillLoop = G.timeline({ repeat: -1, repeatDelay: 0.3, delay: 0.4 });
      pills.forEach((pill, i) => { const at = 0.4 * i; pillLoop.fromTo(pill, { opacity: 0, scale: 0.55, y: 10, rotation: i % 2 ? 3.5 : -3.5, filter: "blur(8px)" }, { opacity: 1, scale: 1, y: 0, rotation: 0, filter: "blur(0px)", duration: 0.45, ease: "back.out(1.6)", force3D: true }, at).to(pill, { y: -6, duration: 0.95, ease: "sine.inOut" }, at + 0.45).to(pill, { opacity: 0, y: -18, scale: 0.94, filter: "blur(5px)", duration: 0.32, ease: "power2.in" }, at + 1.4); });
    }
    const shown = { v: 0 }; let target = 0;
    const setProgress = (v) => { if (v <= target) return; target = v; if (!G) { count.textContent = String(Math.round(v)).padStart(3, "0"); return; } G.to(shown, { v, duration: 0.4 + ((v - shown.v) / 100) * 1.2, ease: "power2.out", overwrite: true, onUpdate: () => { if (word && !reduced) word.style.backgroundImage = "linear-gradient(90deg," + INK + " 0%," + INK + " " + shown.v + "%," + TRACK + " " + shown.v + "%)"; count.textContent = String(Math.round(shown.v)).padStart(3, "0"); } }); };
    let minElapsed = false, assetsReady = false, revealed = false;
    const reveal = () => {
      if (revealed) return; revealed = true;
      const finish = () => { pillLoop && pillLoop.kill(); loader.remove(); };
      const release = () => { S.unlock("loader"); onReveal(); };
      if (!G || reduced) { release(); if (G) G.to(loader, { opacity: 0, duration: 0.5, onComplete: finish }); else finish(); return; }
      const tl = G.timeline({ onComplete: finish });
      tl.fromTo(ldot, { y: "-0.6em", opacity: 0 }, { y: "0em", opacity: 1, duration: 0.45, ease: "power2.out" }).to({}, { duration: 0.35 }).call(release);
      const title = $("[data-hero-title]");
      if (title && !isMobile && isRendered(title)) {
        tl.call(() => { const from = mark.getBoundingClientRect(), to = title.getBoundingClientRect(); G.set(mark, { transformOrigin: "50% 50%" }); G.to(mark, { x: to.left + to.width / 2 - (from.left + from.width / 2), y: to.top + to.height / 2 - (from.top + from.height / 2), scale: to.width / from.width, duration: 0.9, ease: "power3.inOut" }); });
        tl.to({}, { duration: 0.9 }).to(loader, { opacity: 0, duration: 0.35, ease: "power1.out" }, "-=0.35");
      } else { tl.to(mark, { scale: 1.6, duration: 0.55, ease: "power2.in" }).to(loader, { opacity: 0, duration: 0.5, ease: "power1.inOut" }, "<"); }
    };
    const maybe = () => { if (minElapsed && assetsReady) reveal(); };
    const sources = [...new Set($$("img").filter((i) => i.getAttribute("loading") !== "lazy" && isRendered(i)).map((i) => i.getAttribute("src")).filter(Boolean))].slice(0, 16);
    const total = sources.length + 1; let loaded = 0;
    const done = () => { loaded += 1; setProgress((loaded / total) * 100); if (loaded >= total) { assetsReady = true; maybe(); } };
    sources.forEach((src) => { const im = new Image(); im.onload = im.onerror = done; im.src = src; });
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(done, done);
    window.setTimeout(() => { minElapsed = true; maybe(); }, reduced ? 300 : 1800);
    window.setTimeout(reveal, 4000);
    $$(".skip-btn", loader).forEach((b) => b.addEventListener("click", reveal));
    document.addEventListener("keydown", function k(e) { if (e.key === "Escape") { reveal(); document.removeEventListener("keydown", k); } });
  }

  /* ---------------- cart + cash-on-delivery checkout ---------------- */
  const CART_KEY = "stagr-cart";
  const FREE = (DATA.brand && DATA.brand.freeDeliveryThreshold) || 5000;
  const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  let cart = []; try { cart = JSON.parse(localStorage.getItem(CART_KEY) || "[]"); } catch (e) {}
  const save = () => { try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) {} };
  const count = () => cart.reduce((n, l) => n + l.qty, 0);
  const subtotal = () => cart.reduce((n, l) => { const p = S.product(l.id); return n + (p ? p.price * l.qty : 0); }, 0);
  let openCart = () => {}, renderCart = () => {};
  function initCart() {
    const drawer = $(".cart"); if (!drawer) return;
    const backdrop = $(".cart-backdrop"), list = $(".cart-body", drawer), foot = $(".cart-foot", drawer), empty = $(".cart-empty", drawer);
    const shipText = $("[data-ship-text]", drawer), shipBar = $("[data-ship-bar]", drawer), sub = $("[data-subtotal]", drawer);
    const checkout = $(".checkout"), panel = $(".checkout-panel");
    let cartOpen = false, coOpen = false, lastFocus = null;
    list.setAttribute("data-lenis-prevent", "");
    const setCart = (open) => { if (open === cartOpen) return; cartOpen = open; drawer.classList.toggle("is-open", open); drawer.setAttribute("aria-hidden", String(!open)); backdrop.classList.toggle("is-open", open); if (open) { lastFocus = document.activeElement; S.lock("cart"); setTimeout(() => { const f = $("[data-cart-close]", drawer); f && f.focus(); }, 200); } else { S.unlock("cart"); lastFocus && lastFocus.focus && lastFocus.focus(); } };
    const setCheckout = (open) => { if (!checkout || open === coOpen) return; coOpen = open; checkout.classList.toggle("is-open", open); checkout.setAttribute("aria-hidden", String(!open)); open ? S.lock("checkout") : S.unlock("checkout"); if (open) renderCheckout(); };
    openCart = () => setCart(true); S.openCart = openCart; S.closeCart = () => setCart(false);
    const renderCheckout = () => {
      const order = $("[data-order]", panel), wa = $("[data-wa]", panel); if (!order) return;
      const fee = subtotal() >= FREE ? 0 : (DATA.brand.deliveryFee || 0);
      order.innerHTML = cart.map((l) => { const p = S.product(l.id); return p ? "<div><span>" + esc(p.name) + " · " + esc(l.colour) + (l.size ? " · " + esc(l.size) : "") + " × " + l.qty + "</span><span>" + S.fmt(p.price * l.qty) + "</span></div>" : ""; }).join("") + "<div><span>Delivery</span><span>" + (fee ? S.fmt(fee) : "Free") + "</span></div><div><b>Total, cash on delivery</b><b>" + S.fmt(subtotal() + fee) + "</b></div>";
      const lines = cart.map((l) => { const p = S.product(l.id); return p ? "• " + p.name + " (" + l.colour + (l.size ? ", size " + l.size : "") + ") × " + l.qty + " — " + S.fmt(p.price * l.qty) : ""; });
      const msg = "Hello Stagr, I would like to order (cash on delivery):\n" + lines.join("\n") + "\nTotal: " + S.fmt(subtotal() + fee) + "\n\nName:\nAddress:\nCity:\nPhone:";
      if (wa) wa.href = (DATA.brand.whatsapp || "https://wa.me/920000000000") + "?text=" + encodeURIComponent(msg);
    };
    renderCart = (added) => {
      const n = count();
      $$(".cart-count").forEach((el) => { el.textContent = n; el.classList.toggle("is-on", n > 0); if (added && G && !reduced) G.fromTo(el, { scale: 1.4 }, { scale: 1, duration: 0.35, ease: "power2.out" }); });
      empty.hidden = cart.length > 0; foot.hidden = cart.length === 0;
      const remaining = Math.max(0, FREE - subtotal());
      if (shipText) shipText.textContent = remaining <= 0 ? "Delivery is on us." : "You are " + S.fmt(remaining) + " from free delivery.";
      if (shipBar) shipBar.style.setProperty("--p", Math.min(1, subtotal() / FREE));
      if (sub) sub.textContent = S.fmt(subtotal());
      $$(".cart-item", list).forEach((el) => el.remove());
      cart.forEach((l, i) => {
        const p = S.product(l.id); if (!p) return;
        const im = p.cutouts && (p.cutouts.find((c) => c.colour.toLowerCase() === (l.colour || "").toLowerCase()) || p.cutouts[0]);
        const li = document.createElement("div"); li.className = "cart-item"; li.dataset.i = i;
        li.innerHTML = '<div class="thumb"><span class="bloom" style="--bloom:' + (p.bloom || "#D9B07A") + '"></span>' + (im ? '<img src="' + im.small + '" alt="" width="200" height="200">' : "") + '</div><div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;gap:10px"><p class="ci-name">' + esc(p.name) + '</p><button type="button" class="ci-remove" data-remove>Remove</button></div><p class="ci-meta">' + esc(l.colour) + (l.size ? " · Size " + esc(l.size) : "") + '</p><div class="ci-row"><div class="qty"><button type="button" data-dec aria-label="Decrease">−</button><span>' + l.qty + '</span><button type="button" data-inc aria-label="Increase">+</button></div><p class="price">' + S.fmt(p.price * l.qty) + "</p></div></div>";
        list.appendChild(li);
      });
    };
    list.addEventListener("click", (e) => { const row = e.target.closest(".cart-item"); if (!row) return; const i = +row.dataset.i; if (e.target.closest("[data-remove]")) cart[i].qty = 0; else if (e.target.closest("[data-inc]")) cart[i].qty++; else if (e.target.closest("[data-dec]")) cart[i].qty--; else return; cart = cart.filter((l) => l.qty > 0); save(); renderCart(false); });
    $$("[data-cart-open]").forEach((b) => b.addEventListener("click", openCart));
    $$("[data-cart-close]").forEach((b) => b.addEventListener("click", () => setCart(false)));
    backdrop && backdrop.addEventListener("click", () => setCart(false));
    const co = $("[data-checkout-open]", drawer); co && co.addEventListener("click", () => setCheckout(true));
    if (checkout) { checkout.addEventListener("click", () => setCheckout(false)); panel.addEventListener("click", (e) => e.stopPropagation()); $$("[data-checkout-close]").forEach((b) => b.addEventListener("click", () => setCheckout(false))); }
    window.addEventListener("keydown", (e) => { if (e.key !== "Escape") return; if (coOpen) setCheckout(false); else if (cartOpen) setCart(false); else if (menuOpen) S.closeMenu(); else if (S.closeOverlay) S.closeOverlay(); });
    renderCart(false);
  }
  S.addToCart = (id, colour, size, qty) => { const p = S.product(id); if (!p) return; qty = qty || 1; colour = colour || p.defaultColour; size = size || null; const f = cart.find((l) => l.id === id && l.colour === colour && l.size === size); if (f) f.qty += qty; else cart.push({ id, colour, size, qty }); save(); renderCart(true); openCart(); };
  S.cart = () => cart;
  // delegated add buttons: [data-add="id"] [data-colour] [data-size]
  document.addEventListener("click", (e) => { const b = e.target.closest("[data-add]"); if (!b) return; e.preventDefault(); S.addToCart(b.dataset.add, b.dataset.colour, b.dataset.size, +(b.dataset.qty || 1)); if (!b.classList.contains("is-added")) { const old = b.innerHTML; b.classList.add("is-added"); b.innerHTML = "Added"; clearTimeout(b._t); b._t = setTimeout(() => { b.classList.remove("is-added"); b.innerHTML = old; }, 1500); } });

  /* ---------------- toast ---------------- */
  let toastEl = $(".toast"), toastT = null;
  S.toast = (msg) => { if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); } toastEl.textContent = msg; toastEl.classList.add("is-on"); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove("is-on"), 3200); };

  /* ---------------- newsletter forms ---------------- */
  function initForms() { $$("form[data-notify]").forEach((f) => f.addEventListener("submit", (e) => { e.preventDefault(); const st = $("[data-notify-status]", f.parentElement) || $("[data-notify-status]"); if (st) st.textContent = "You are on the list."; else S.toast("You are on the list."); f.reset(); })); }

  /* ---------------- cross-page fade ---------------- */
  function initFade() {
    const fade = $(".fade");
    if (fade && G && !reduced) { if (html.classList.contains("is-entering")) { G.set(fade, { opacity: 1 }); G.to(fade, { opacity: 0, duration: 0.6, ease: "power2.out", delay: 0.05, onComplete: () => html.classList.remove("is-entering") }); } else html.classList.remove("is-entering"); }
    else html.classList.remove("is-entering");
    document.addEventListener("click", (e) => {
      if (e.defaultPrevented || e.target.closest("button, [data-add]")) return;
      const a = e.target.closest("a[href]"); if (!a) return;
      const href = a.getAttribute("href"); if (!href || href.startsWith("#") || a.target === "_blank" || /^(mailto|tel|https?):/.test(href) || e.metaKey || e.ctrlKey || e.shiftKey) return;
      if (!fade || !G || reduced) return;
      e.preventDefault(); try { sessionStorage.setItem("stagr-transition", "1"); } catch (x) {}
      G.to(fade, { opacity: 1, duration: 0.35, ease: "power2.in", onComplete: () => { location.href = a.href; } });
    });
    window.addEventListener("pageshow", (e) => { if (e.persisted && fade && G) G.set(fade, { opacity: 0 }); });
  }

  /* ---------------- boot ---------------- */
  function boot() {

  /* ---------------- shop cards: colour radio swaps the cutout ---------------- */
  S.initCards = (root) => { $$("[data-product]", root || document).forEach((card) => { if (card._cards) return; card._cards = true; const btn = $("[data-add]", card); $$("[data-colour-opts] input", card).forEach((r) => r.addEventListener("change", () => {
    if (btn) btn.dataset.colour = r.value;
    const p = S.product(card.dataset.product); if (!p) return;
    const same = p.cutouts.filter((c) => c.colour.toLowerCase() === r.value.toLowerCase()); if (!same.length) return;
    const main = $("img.main", card), alt = $("img.alt", card);
    card.classList.toggle("has-alt", same.length > 1);
    if (alt) alt.src = (same[1] || same[0]).small;
    if (main.getAttribute("src") === same[0].small) return;
    const swap = () => { main.src = same[0].small; };
    if (!G || reduced) { swap(); return; }
    // fade the old view out, swap the file, fade the new one in; leave no inline styles behind so hover keeps working
    G.to(main, { opacity: 0, scale: .96, duration: .18, ease: "power2.in", overwrite: true, onComplete: () => { swap(); const show = () => G.fromTo(main, { opacity: 0, scale: .96 }, { opacity: 1, scale: 1, duration: .35, ease: "power2.out", overwrite: true, clearProps: "opacity,transform,scale" }); if (main.complete && main.naturalWidth) show(); else { main.onload = () => { main.onload = null; show(); }; } } });
  })); }); };

  /* ---------------- wishlist hearts (kept in this browser) ---------------- */
  function initWish() {
    const KEY = "stagr-wishlist"; let wish = []; try { wish = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) {}
    const paint = () => $$("[data-wish]").forEach((b) => b.setAttribute("aria-pressed", String(wish.indexOf(b.dataset.wish) >= 0)));
    document.addEventListener("click", (e) => { const b = e.target.closest("[data-wish]"); if (!b) return; e.preventDefault(); const id = b.dataset.wish, i = wish.indexOf(id); if (i >= 0) wish.splice(i, 1); else wish.push(id); try { localStorage.setItem(KEY, JSON.stringify(wish)); } catch (x) {} paint(); if (G && !reduced) G.fromTo(b, { scale: .8 }, { scale: 1, duration: .45, ease: "back.out(3)", clearProps: "transform" }); S.toast && S.toast(i >= 0 ? "Removed from saved" : "Saved for later"); });
    paint();
  }

  /* ---------------- grid filter swap: fade out, reorder, fade in (no layout tricks) ---------------- */
  S.swapGrid = (grid, mutate) => {
    const visible = $$("[data-product]", grid).filter((c) => !c.classList.contains("is-hidden"));
    const finish = () => { const now = $$("[data-product]", grid).filter((c) => !c.classList.contains("is-hidden")); if (G && !reduced) G.fromTo(now, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .45, ease: "power3.out", stagger: .04, overwrite: true, clearProps: "opacity,transform", onComplete: () => { grid.style.minHeight = ""; } }); else grid.style.minHeight = ""; if (window.ScrollTrigger) window.ScrollTrigger.refresh(); S.repaintRails && S.repaintRails(); };
    if (!G || reduced || !visible.length) { mutate(); finish(); return; }
    grid.style.minHeight = grid.offsetHeight + "px";   // keep the page from jumping while cards are out
    G.to(visible, { opacity: 0, y: -8, duration: .2, ease: "power2.in", stagger: .012, overwrite: true, onComplete: () => { G.set(visible, { clearProps: "opacity,transform" }); mutate(); finish(); } });
  };

  /* ---------------- rail: horizontal card carousel with arrows and dots ---------------- */
  S.initRails = (root) => { $$("[data-rail]", root || document).forEach((rail) => {
    if (rail._rail) return; rail._rail = true;
    const track = $("[data-rail-track]", rail), prev = $("[data-rail-prev]", rail), next = $("[data-rail-next]", rail), dots = $("[data-rail-dots]", rail);
    const items = () => [...track.children];
    const step = () => { const c = [...track.children].find((el) => el.offsetParent !== null); return c ? c.offsetWidth + parseFloat(getComputedStyle(track).gap || 0) : track.clientWidth; };
    const pages = () => Math.max(1, Math.ceil((track.scrollWidth - track.clientWidth) / step()) + 1);
    const page = () => Math.round(track.scrollLeft / step());
    const paint = () => { const n = pages(), i = Math.min(page(), n - 1), overflow = track.scrollWidth > track.clientWidth + 4; rail.classList.toggle("has-overflow", overflow); if (prev) prev.disabled = i <= 0; if (next) next.disabled = i >= n - 1; if (dots) { if (dots.children.length !== n) dots.innerHTML = n > 1 ? Array.from({ length: n }, () => "<i></i>").join("") : ""; [...dots.children].forEach((d, k) => d.classList.toggle("is-on", k === i)); } };
    const go = (d) => track.scrollBy({ left: d * step(), behavior: reduced ? "auto" : "smooth" });
    prev && prev.addEventListener("click", () => go(-1)); next && next.addEventListener("click", () => go(1));
    track.addEventListener("scroll", paint, { passive: true }); window.addEventListener("resize", paint);
    paint(); setTimeout(paint, 400); items(); rail._paint = paint;
  }); };
  S.repaintRails = () => $$("[data-rail]").forEach((r) => r._paint && r._paint());


  /* ---------------- quick view (dialog lives in the shared chrome) ---------------- */
  function initQuickView() {
    const qv = $(".qv"), qvb = $(".qv-backdrop"); if (!qv) return;
    let open = false, last = null, cur = null, colour = "", size = null;
    const SW = { Brown: "#6E4328", Black: "#1A1512", Tan: "#B0773F", Coffee: "#4A3024" };
    const fade = (el) => { if (G) G.fromTo(el, { opacity: 0 }, { opacity: 1, duration: .4 }); };
    const render = () => {
      const p = cur, imgs = p.cutouts.filter((c) => c.colour.toLowerCase() === colour.toLowerCase());
      const main = $("[data-qv-img]", qv); main.src = imgs[0].src; main.alt = p.name + " in " + colour;
      $("[data-qv-thumbs]", qv).innerHTML = imgs.map((im, i) => '<button type="button" aria-pressed="' + (i === 0) + '" aria-label="View ' + (i + 1) + '"><img src="' + im.small + '" alt="" width="100" height="100"></button>').join("");
      $$("[data-qv-thumbs] button", qv).forEach((b, i) => b.addEventListener("click", () => { $$("[data-qv-thumbs] button", qv).forEach((x) => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); fade(main); main.src = imgs[i].src; }));
      $("[data-qv-colour]", qv).textContent = colour;
      $("[data-qv-opts]", qv).innerHTML = p.colours.map((c) => '<label class="opt"><input type="radio" name="qv-colour" value="' + c + '"' + (c === colour ? " checked" : "") + '><span class="sw" style="--sw:' + (SW[c] || "#6E4328") + '"></span>' + c + "</label>").join("");
      $$("[data-qv-opts] input", qv).forEach((r) => r.addEventListener("change", () => { colour = r.value; render(); }));
      const sz = $("[data-qv-sizes]", qv);
      if (p.sizes) { sz.hidden = false; $("[data-qv-size]", qv).textContent = size; $("[data-qv-size-opts]", qv).innerHTML = p.sizes.options.map((s) => '<label class="opt"><input type="radio" name="qv-size" value="' + s + '"' + (s === size ? " checked" : "") + ">" + s + "</label>").join(""); $$("[data-qv-size-opts] input", qv).forEach((r) => r.addEventListener("change", () => { size = +r.value; $("[data-qv-size]", qv).textContent = size; })); } else sz.hidden = true;
      $("[data-qv-add]", qv).onclick = () => { S.addToCart(p.id, colour, size, 1); closeQv(); };
    };
    const openQv = (id) => {
      cur = S.product(id); if (!cur) return; colour = cur.defaultColour; size = cur.sizes ? (cur.sizes.options[2] || cur.sizes.options[0]) : null; last = document.activeElement;
      $("[data-qv-num]", qv).textContent = "STAGR." + String(DATA.products.indexOf(cur) + 1).padStart(2, "0");
      $("[data-qv-meta]", qv).textContent = cur.style || "Belt";
      $("[data-qv-name]", qv).innerHTML = esc(cur.name.split(" ")[0]) + '<span class="dotc">.</span>';
      $("[data-qv-sub]", qv).textContent = cur.name; $("[data-qv-tagline]", qv).textContent = cur.tagline;
      $("[data-qv-price]", qv).innerHTML = S.fmt(cur.price) + (cur.compareAtPrice ? '<s class="small muted" style="margin-left:.5em">' + S.fmt(cur.compareAtPrice) + "</s>" : "");
      $("[data-qv-link]", qv).href = "product-" + cur.id + ".html";
      render(); qv.classList.add("is-open"); qvb.classList.add("is-open"); qv.setAttribute("aria-hidden", "false"); open = true; S.lock("qv");
      setTimeout(() => $(".qv-close", qv).focus(), 300);
    };
    const closeQv = () => { if (!open) return; qv.classList.remove("is-open"); qvb.classList.remove("is-open"); qv.setAttribute("aria-hidden", "true"); open = false; S.unlock("qv"); last && last.focus && last.focus(); };
    S.closeOverlay = closeQv; S.openQuickView = openQv;
    document.addEventListener("click", (e) => { const b = e.target.closest("[data-quick]"); if (b) { e.preventDefault(); openQv(b.dataset.quick); } });
    $$("[data-qv-close]").forEach((b) => b.addEventListener("click", closeQv));
  }

    initNav(); initQuickView(); initWish(); S.initCards(document); S.initRails(document); initCart(); initForms(); initFade(); S.initBlooms(); S.magnetic(document);
    S.onReady.forEach((f) => { try { f(); } catch (e) { console.error(e); } });
    if (ST) { ST.sort(); ST.refresh(); window.addEventListener("load", () => ST.refresh()); }
    initLoader(() => { S.onLoaderDone.forEach((f) => { try { f(); } catch (e) { console.error(e); } }); ST && ST.refresh(); const h = location.hash; if (h && h !== "#top" && $(h)) setTimeout(() => S.scrollTo(h), 900); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
