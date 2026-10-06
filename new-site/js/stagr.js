/* ==========================================================================
   STAGR — shared runtime (header, split menu, cart drawer, cursor, theme,
   Lenis smooth scroll, page transitions, loader, reveal primitives).
   GSAP 3.13 + ScrollTrigger + SplitText + Flip + Observer are loaded from
   cdnjs by each page; Lenis from unpkg. Everything degrades: if GSAP is
   missing the page is fully readable, just without motion.
   ========================================================================== */
(function () {
  "use strict";
  const html = document.documentElement;
  html.classList.remove("no-js");
  html.classList.add("js");

  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const FINE = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const G = window.gsap || null;
  const ST = window.ScrollTrigger || null;
  const DATA = window.STAGR_DATA || { products: [], brand: {} };
  const EASE = { in: "power3.out", io: "power2.inOut", big: "expo.out" };
  const q = (s, r) => (r || document).querySelector(s);
  const qa = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));

  if (G) {
    const plugins = [ST, window.SplitText, window.Flip, window.Observer].filter(Boolean);
    if (plugins.length) G.registerPlugin.apply(G, plugins);
    G.defaults({ ease: EASE.in, duration: 1 });
  }

  const S = (window.STAGR = {
    reduced: REDUCED, fine: FINE, gsap: G, data: DATA, ease: EASE,
    fmt: (n) => "Rs " + Number(n).toLocaleString("en-PK"),
    product: (id) => DATA.products.find((p) => p.id === id),
    onReady: [], onLoaderDone: [],
  });

  /* ---------------- theme ---------------- */
  const THEME_KEY = "stagr-theme";
  function setTheme(t, store) {
    if (t) html.setAttribute("data-theme", t); else html.removeAttribute("data-theme");
    if (store) { try { t ? localStorage.setItem(THEME_KEY, t) : localStorage.removeItem(THEME_KEY); } catch (e) {} }
    qa(".theme-toggle").forEach((b) => b.setAttribute("aria-pressed", String(isDark())));
  }
  function isDark() {
    const t = html.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  S.toggleTheme = () => setTheme(isDark() ? "light" : "dark", true);
  S.isDark = isDark;
  qa(".theme-toggle").forEach((b) => { b.setAttribute("aria-pressed", String(isDark())); b.addEventListener("click", S.toggleTheme); });

  /* ---------------- smooth scroll ---------------- */
  let lenis = null;
  if (window.Lenis && !REDUCED) {
    lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true, syncTouch: false });
    if (G) {
      if (ST) lenis.on("scroll", ST.update);
      G.ticker.add((t) => lenis.raf(t * 1000));
      G.ticker.lagSmoothing(0);
    } else {
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }
  S.lenis = lenis;
  S.scrollTo = (target, opts) => {
    if (lenis) lenis.scrollTo(target, Object.assign({ offset: -72, duration: 1.2 }, opts || {}));
    else {
      const el = typeof target === "string" ? q(target) : target;
      const y = typeof target === "number" ? target : el ? el.getBoundingClientRect().top + window.scrollY - 72 : 0;
      window.scrollTo({ top: y, behavior: REDUCED ? "auto" : "smooth" });
    }
  };
  S.lock = (on) => { if (lenis) on ? lenis.stop() : lenis.start(); html.style.overflow = on ? "hidden" : ""; };
  qa("[data-scroll-to]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); S.scrollTo(a.getAttribute("data-scroll-to")); }));

  /* ---------------- header ---------------- */
  const header = q(".header");
  if (header) {
    let last = 0;
    const onScroll = () => {
      const y = window.scrollY || 0;
      header.classList.toggle("is-solid", y > 24);
      // hide on fast downward scroll past the hero, show on upward
      if (y > 600 && y - last > 6) header.classList.add("is-hidden");
      else if (last - y > 4 || y < 600) header.classList.remove("is-hidden");
      last = y;
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------- fullscreen split menu ---------------- */
  const menu = q(".menu");
  const menuBtn = q("[data-menu-open]");
  let menuOpen = false, menuTl = null, lastFocus = null;
  function buildMenuTl() {
    if (!G) return null;
    const panels = [q(".menu-panel.l", menu), q(".menu-panel.r", menu)];
    const links = qa(".menu-link", menu);
    const tl = G.timeline({ paused: true, defaults: { ease: EASE.io } });
    tl.set(menu, { visibility: "visible" })
      .to(panels, { y: 0, duration: 0.8, ease: "power3.inOut" }, 0)
      .fromTo(q(".menu-top", menu), { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.5, ease: EASE.in }, 0.5)
      .fromTo(links, { opacity: 0, yPercent: 60 }, { opacity: 1, yPercent: 0, duration: 0.9, stagger: 0.08, ease: EASE.in }, 0.45)
      .fromTo(q(".menu-foot", menu), { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.6, ease: EASE.in }, 0.8)
      .fromTo(q(".menu-art", menu), { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: 1, ease: EASE.in }, 0.7);
    return tl;
  }
  function openMenu() {
    if (!menu || menuOpen) return;
    menuOpen = true; lastFocus = document.activeElement;
    menu.classList.add("is-open");
    menu.setAttribute("aria-hidden", "false");
    menuBtn && menuBtn.setAttribute("aria-expanded", "true");
    S.lock(true);
    if (G && !REDUCED) { menuTl = menuTl || buildMenuTl(); menuTl.timeScale(1).play(0); }
    else { qa(".menu-link, .menu-foot, .menu-art, .menu-top", menu).forEach((el) => (el.style.opacity = 1)); qa(".menu-panel", menu).forEach((p) => (p.style.transform = "none")); }
    setTimeout(() => { const f = q(".menu-close", menu); f && f.focus(); }, 300);
  }
  function closeMenu() {
    if (!menu || !menuOpen) return;
    menuOpen = false;
    menu.setAttribute("aria-hidden", "true");
    menuBtn && menuBtn.setAttribute("aria-expanded", "false");
    const done = () => { menu.classList.remove("is-open"); S.lock(false); lastFocus && lastFocus.focus && lastFocus.focus(); };
    if (G && !REDUCED && menuTl) { menuTl.timeScale(1.6).reverse(); menuTl.eventCallback("onReverseComplete", done); }
    else { qa(".menu-panel", menu).forEach((p) => (p.style.transform = "")); done(); }
  }
  S.openMenu = openMenu; S.closeMenu = closeMenu;
  if (menu) {
    menuBtn && menuBtn.addEventListener("click", openMenu);
    qa("[data-menu-close]", menu).forEach((b) => b.addEventListener("click", closeMenu));
    // menu art swaps on link hover
    const art = q(".menu-art img", menu);
    qa(".menu-link[data-art]", menu).forEach((a) => a.addEventListener("mouseenter", () => {
      if (!art || art.getAttribute("src") === a.dataset.art) return;
      if (G && !REDUCED) G.fromTo(art, { opacity: 0.4, scale: 1.04 }, { opacity: 1, scale: 1, duration: 0.6, onStart: () => art.setAttribute("src", a.dataset.art) });
      else art.setAttribute("src", a.dataset.art);
    }));
  }

  /* ---------------- cart ---------------- */
  const CART_KEY = "stagr-cart";
  const FREE = (DATA.brand && DATA.brand.freeDeliveryThreshold) || 5000;
  function loadCart() { try { return JSON.parse(localStorage.getItem(CART_KEY) || "[]"); } catch (e) { return []; } }
  function saveCart(c) { try { localStorage.setItem(CART_KEY, JSON.stringify(c)); } catch (e) {} }
  let cart = loadCart();
  const drawer = q(".drawer"), backdrop = q(".drawer-backdrop");
  let drawerOpen = false, drawerLastFocus = null;

  function cartCount() { return cart.reduce((n, l) => n + l.qty, 0); }
  function subtotal() { return cart.reduce((n, l) => { const p = S.product(l.id); return n + (p ? p.price * l.qty : 0); }, 0); }
  function renderCart() {
    const n = cartCount();
    qa(".cart-count").forEach((el) => { el.textContent = n; el.classList.toggle("is-on", n > 0); });
    if (!drawer) return;
    const body = q(".drawer-body", drawer), foot = q(".drawer-foot", drawer);
    const brand = DATA.brand || {};
    if (!cart.length) {
      body.innerHTML = '<div class="drawer-empty"><p class="h4">' + (brand.cartEmpty || "Your bag is empty. Start with a belt.") + '</p><p><a class="btn btn--ghost btn--sm" href="belts.html">Shop belts</a> &nbsp; <a class="btn btn--ghost btn--sm" href="wallets.html">Shop wallets</a></p></div>';
      foot.hidden = true; return;
    }
    foot.hidden = false;
    body.innerHTML = cart.map((l, i) => {
      const p = S.product(l.id); if (!p) return "";
      const img = (p.images.find((im) => im.colour.toLowerCase() === (l.colour || "").toLowerCase()) || p.images[0]);
      return '<div class="line-item" data-i="' + i + '">' +
        '<div class="media media--studio"><img src="' + img.src + '" alt="' + img.alt + '" width="' + img.width + '" height="' + img.height + '" loading="lazy"></div>' +
        '<div><div class="li-name">' + p.name + '</div><div class="li-meta">' + [l.colour, l.size ? "Size " + l.size : ""].filter(Boolean).join(" · ") + '</div>' +
        '<div class="qty" style="margin-top:12px;height:40px"><button type="button" data-dec aria-label="Decrease quantity">−</button><span>' + l.qty + '</span><button type="button" data-inc aria-label="Increase quantity">+</button></div>' +
        '<button type="button" class="li-remove" data-remove>Remove</button></div>' +
        '<div class="price">' + S.fmt(p.price * l.qty) + '</div></div>';
    }).join("");
    const sub = subtotal();
    q("[data-subtotal]", drawer).textContent = S.fmt(sub);
    const note = q("[data-delivery-note]", drawer), prog = q("[data-delivery-progress]", drawer);
    if (note) note.textContent = sub >= FREE ? (brand.freeDeliveryCopy || "Delivery is on us.") : "You are " + S.fmt(FREE - sub) + " from free delivery.";
    if (prog) prog.style.setProperty("--p", Math.min(1, sub / FREE));
  }
  function addToCart(id, colour, size, qty) {
    const p = S.product(id); if (!p) return;
    qty = qty || 1;
    const found = cart.find((l) => l.id === id && l.colour === colour && l.size === size);
    if (found) found.qty += qty; else cart.push({ id, colour: colour || p.defaultColour, size: size || null, qty });
    saveCart(cart); renderCart(); openCart();
    pulse(qa(".cart-count"));
  }
  function pulse(els) { if (G && !REDUCED) G.fromTo(els, { scale: 1.5 }, { scale: 1, duration: 0.5, ease: "power3.out" }); }
  function openCart() {
    if (!drawer || drawerOpen) return;
    drawerOpen = true; drawerLastFocus = document.activeElement;
    drawer.classList.add("is-open"); backdrop && backdrop.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false"); S.lock(true);
    setTimeout(() => { const f = q("[data-cart-close]", drawer); f && f.focus(); }, 200);
  }
  function closeCart() {
    if (!drawer || !drawerOpen) return;
    drawerOpen = false;
    drawer.classList.remove("is-open"); backdrop && backdrop.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true"); S.lock(false);
    drawerLastFocus && drawerLastFocus.focus && drawerLastFocus.focus();
  }
  S.addToCart = addToCart; S.openCart = openCart; S.closeCart = closeCart; S.cart = () => cart;
  if (drawer) {
    renderCart();
    qa("[data-cart-open]").forEach((b) => b.addEventListener("click", openCart));
    qa("[data-cart-close]", drawer).forEach((b) => b.addEventListener("click", closeCart));
    backdrop && backdrop.addEventListener("click", closeCart);
    drawer.addEventListener("click", (e) => {
      const li = e.target.closest(".line-item"); if (!li) return;
      const i = +li.dataset.i;
      if (e.target.closest("[data-inc]")) cart[i].qty += 1;
      else if (e.target.closest("[data-dec]")) { cart[i].qty -= 1; if (cart[i].qty <= 0) cart.splice(i, 1); }
      else if (e.target.closest("[data-remove]")) cart.splice(i, 1);
      else return;
      saveCart(cart); renderCart();
    });
    const co = q("[data-checkout]", drawer);
    co && co.addEventListener("click", () => toast("Checkout is not wired yet. Orders are cash on delivery; connect this button to your order form."));
  }
  // generic add buttons anywhere: data-add="product-id" [data-colour] [data-size]
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-add]"); if (!b) return;
    e.preventDefault();
    addToCart(b.dataset.add, b.dataset.colour, b.dataset.size, +(b.dataset.qty || 1));
  });

  /* ---------------- toast ---------------- */
  let toastEl = q(".toast"), toastT = null;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("is-on");
    clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove("is-on"), 3200);
  }
  S.toast = toast;

  /* ---------------- escape closes overlays ---------------- */
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    if (menuOpen) closeMenu();
    if (drawerOpen) closeCart();
    if (S.closeLightbox) S.closeLightbox();
  });

  /* ---------------- custom cursor + magnetic ---------------- */
  const cursor = q(".cursor");
  if (cursor && FINE && !REDUCED && G) {
    html.classList.add("has-cursor");
    const dot = q(".dot", cursor), ring = q(".ring", cursor), label = q(".ring span", cursor);
    const dx = G.quickTo(dot, "x", { duration: 0.08, ease: "none" }), dy = G.quickTo(dot, "y", { duration: 0.08, ease: "none" });
    const rx = G.quickTo(ring, "x", { duration: 0.35, ease: "power3" }), ry = G.quickTo(ring, "y", { duration: 0.35, ease: "power3" });
    let shown = false;
    window.addEventListener("mousemove", (e) => {
      if (!shown) { G.set([dot, ring], { x: e.clientX, y: e.clientY }); cursor.classList.add("is-on"); shown = true; }
      dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY);
    }, { passive: true });
    document.addEventListener("mouseover", (e) => {
      const lab = e.target.closest("[data-cursor]");
      const hot = lab || e.target.closest("a, button, [role=button], input, select, textarea, summary, label");
      if (lab) { label.textContent = lab.dataset.cursor; cursor.classList.add("is-label"); G.to(ring, { scale: 2.4, duration: 0.35 }); }
      else if (hot) { cursor.classList.remove("is-label"); G.to(ring, { scale: 1.6, duration: 0.3 }); }
      else { cursor.classList.remove("is-label"); G.to(ring, { scale: 1, duration: 0.3 }); }
    });
    document.addEventListener("mouseleave", () => G.to([dot, ring], { opacity: 0, duration: 0.2 }));
    document.addEventListener("mouseenter", () => G.to([dot, ring], { opacity: 1, duration: 0.2 }));
  }
  function magnetic(root) {
    if (!G || !FINE || REDUCED) return;
    qa("[data-magnetic]", root).forEach((el) => {
      if (el._mag) return; el._mag = true;
      const R = +(el.dataset.magnetic || 40);
      const xTo = G.quickTo(el, "x", { duration: 0.5, ease: "power3" }), yTo = G.quickTo(el, "y", { duration: 0.5, ease: "power3" });
      const inner = q(".btn-label", el);
      const ixTo = inner && G.quickTo(inner, "x", { duration: 0.5, ease: "power3" }), iyTo = inner && G.quickTo(inner, "y", { duration: 0.5, ease: "power3" });
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const mx = e.clientX - (r.left + r.width / 2), my = e.clientY - (r.top + r.height / 2);
        const d = Math.hypot(mx, my), lim = Math.max(r.width, r.height) / 2 + R;
        if (d > lim) return;
        xTo(mx * 0.35); yTo(my * 0.35); ixTo && ixTo(mx * 0.15); iyTo && iyTo(my * 0.15);
      });
      el.addEventListener("mouseleave", () => { xTo(0); yTo(0); ixTo && ixTo(0); iyTo && iyTo(0); });
    });
  }
  S.magnetic = magnetic;

  /* ---------------- reveal primitives ---------------- */
  function trig(el, extra) {
    return Object.assign({ trigger: el, start: "top 80%", once: true }, extra || {});
  }
  function revealLines(root) {
    const els = qa("[data-lines]", root);
    if (!els.length) return;
    if (!G || !window.SplitText || REDUCED) { els.forEach((el) => el.classList.add("is-split")); return; }
    els.forEach((el) => {
      if (el._split) return; el._split = true;
      const now = el.dataset.lines === "now", delay = +(el.dataset.delay || 0);
      window.SplitText.create(el, {
        type: "lines", mask: "lines", linesClass: "line", autoSplit: true,
        onSplit(self) {
          el.classList.add("is-split");
          const vars = { yPercent: 105, duration: 1.2, ease: EASE.in, stagger: 0.09, delay, overwrite: true };
          if (now) { if (el.dataset.wait === "loader") { return G.from(self.lines, Object.assign(vars, { paused: true })); } return G.from(self.lines, vars); }
          return G.from(self.lines, Object.assign(vars, { scrollTrigger: trig(el) }));
        },
      });
    });
  }
  function revealImages(root) {
    const els = qa(".reveal-img", root);
    if (!els.length) return;
    if (!G || REDUCED) { els.forEach((el) => { el.classList.add("is-revealed"); qa("img", el).forEach((i) => { i.style.clipPath = "none"; i.style.transform = "none"; }); }); return; }
    els.forEach((el) => {
      if (el._rev) return; el._rev = true;
      const img = q("img, picture", el); if (!img) return;
      const from = el.dataset.from || "bottom";
      const start = { bottom: "inset(0 0 100% 0)", top: "inset(100% 0 0 0)", left: "inset(0 100% 0 0)", right: "inset(0 0 0 100%)" }[from];
      const tw = G.fromTo(img, { clipPath: start, scale: 1.15 }, { clipPath: "inset(0 0 0 0)", scale: 1, duration: 1.4, ease: EASE.big, delay: +(el.dataset.delay || 0), paused: el.dataset.wait === "loader", scrollTrigger: el.dataset.wait === "loader" ? null : trig(el), onComplete: () => { el.classList.add("is-revealed"); img.style.clipPath = ""; } });
      if (el.dataset.wait === "loader") S.onLoaderDone.push(() => tw.play());
    });
  }
  function revealBlocks(root) {
    const els = qa("[data-reveal]", root);
    if (!els.length) return;
    if (!G || REDUCED) { els.forEach((el) => el.classList.add("is-revealed")); return; }
    els.forEach((el) => {
      if (el._rev) return; el._rev = true;
      const kind = el.dataset.reveal, delay = +(el.dataset.delay || 0);
      const from = kind === "up" ? { opacity: 0, y: 32 } : { opacity: 0 };
      const tw = G.fromTo(el, from, { opacity: 1, y: 0, duration: 1, ease: EASE.in, delay, paused: el.dataset.wait === "loader", scrollTrigger: el.dataset.wait === "loader" ? null : trig(el), onComplete: () => el.classList.add("is-revealed") });
      if (el.dataset.wait === "loader") S.onLoaderDone.push(() => tw.play());
    });
    // staggered groups
    qa("[data-stagger]", root).forEach((grp) => {
      if (grp._rev) return; grp._rev = true;
      const kids = Array.prototype.slice.call(grp.children);
      G.fromTo(kids, { opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 1, stagger: +(grp.dataset.stagger || 0.1), ease: EASE.in, scrollTrigger: trig(grp) });
    });
  }
  function parallax(root) {
    const els = qa("[data-parallax]", root);
    if (!els.length || !G || !ST || REDUCED) return;
    els.forEach((el) => {
      if (el._px) return; el._px = true;
      const speed = +(el.dataset.parallax || 0.2);
      const target = q("img, video, .px-inner", el) || el;
      G.fromTo(target, { yPercent: -10 * speed * 2 }, { yPercent: 10 * speed * 2, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: 0.8 } });
    });
  }
  function marquee(root) {
    qa("[data-marquee]", root).forEach((el) => {
      if (el._mq) return; el._mq = true;
      const track = q(".track", el); if (!track) return;
      // duplicate until it spans at least 2x the viewport
      const clone = track.cloneNode(true); clone.setAttribute("aria-hidden", "true"); el.appendChild(clone);
      if (!G || REDUCED) return;
      const dir = el.dataset.marquee === "reverse" ? 1 : -1;
      const speed = +(el.dataset.speed || 60); // px / s
      let tw;
      const build = () => {
        const w = track.offsetWidth; if (!w) return;
        tw && tw.kill();
        tw = G.fromTo([track, clone], { xPercent: dir < 0 ? 0 : -100 }, { xPercent: dir < 0 ? -100 : 0, duration: w / speed, ease: "none", repeat: -1 });
        if (ST) ST.create({ trigger: el, start: "top bottom", end: "bottom top", onToggle: (s) => (s.isActive ? tw.play() : tw.pause()) });
      };
      build();
      let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(build, 200); });
      if (el.dataset.scrub !== undefined && ST) {
        // speed up with scroll velocity
        ST.create({ trigger: document.body, start: 0, end: "max", onUpdate: (self) => { if (!tw) return; const v = Math.min(4, 1 + Math.abs(self.getVelocity()) / 800); G.to(tw, { timeScale: v * (self.direction || 1), duration: 0.4, overwrite: true }); } });
      }
    });
  }
  function initReveals(root) { revealLines(root); revealImages(root); revealBlocks(root); parallax(root); marquee(root); magnetic(root); }
  S.initReveals = initReveals;

  /* ---------------- segmented tabs helper ---------------- */
  S.segmented = (seg, onChange) => {
    const btns = qa("button", seg); const thumb = q(".seg-thumb", seg);
    const move = (b) => { if (!thumb) return; thumb.style.width = b.offsetWidth + "px"; thumb.style.transform = "translateX(" + (b.offsetLeft - 4) + "px)"; };
    btns.forEach((b) => b.addEventListener("click", () => { btns.forEach((x) => x.setAttribute("aria-selected", "false")); b.setAttribute("aria-selected", "true"); move(b); onChange && onChange(b.dataset.tab, b); }));
    const cur = btns.find((b) => b.getAttribute("aria-selected") === "true") || btns[0];
    if (cur) { cur.setAttribute("aria-selected", "true"); requestAnimationFrame(() => move(cur)); }
    window.addEventListener("resize", () => { const c = btns.find((b) => b.getAttribute("aria-selected") === "true"); c && move(c); });
  };

  /* ---------------- page transitions ---------------- */
  const curtain = q(".curtain");
  const T_KEY = "stagr-transition";
  function internal(a) {
    const href = a.getAttribute("href"); if (!href) return false;
    if (a.target === "_blank" || a.hasAttribute("download") || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:")) return false;
    try { const u = new URL(href, location.href); if (u.origin !== location.origin) return false; if (u.pathname === location.pathname && u.hash) return false; return /\.html?$|\/$/.test(u.pathname) || !/\.[a-z0-9]+$/i.test(u.pathname); } catch (e) { return false; }
  }
  document.addEventListener("click", (e) => {
    if (e.defaultPrevented || e.target.closest("button, [data-add], [data-quick]")) return;
    const a = e.target.closest("a[href]"); if (!a || !internal(a)) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    if (!curtain || !G || REDUCED) return; // native navigation
    e.preventDefault();
    const href = a.href;
    try { sessionStorage.setItem(T_KEY, "1"); } catch (x) {}
    S.lock(true);
    G.timeline({ onComplete: () => { location.href = href; } })
      .to(curtain, { y: "0%", duration: 0.7, ease: "power2.inOut" })
      .fromTo(q("svg", curtain), { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3 }, "-=0.2");
  });
  window.addEventListener("pageshow", (e) => { if (e.persisted && curtain && G) G.set(curtain, { y: "101%" }); });
  function curtainIn() {
    if (!curtain) return Promise.resolve();
    let entering = false; try { entering = sessionStorage.getItem(T_KEY) === "1"; sessionStorage.removeItem(T_KEY); } catch (e) {}
    if (!entering || !G || REDUCED) { html.classList.remove("is-entering"); if (G && curtain) G.set(curtain, { y: "101%" }); return Promise.resolve(); }
    return new Promise((res) => {
      G.set(curtain, { y: "0%" });
      G.timeline({ onComplete: () => { html.classList.remove("is-entering"); G.set(curtain, { y: "101%" }); res(); } })
        .to(q("svg", curtain), { opacity: 0, duration: 0.2 }, 0.05)
        .to(curtain, { y: "-101%", duration: 0.8, ease: "power2.inOut" }, 0.05);
    });
  }

  /* ---------------- loader (index only) ---------------- */
  function runLoader() {
    const loader = q("#loader");
    if (!loader || loader.hidden || html.classList.contains("no-loader")) { if (loader) loader.hidden = true; return Promise.resolve(); }
    try { sessionStorage.setItem("stagr-loaded", "1"); } catch (e) {}
    if (!G || REDUCED) { loader.hidden = true; return Promise.resolve(); }
    S.lock(true);
    return new Promise((res) => {
      let done = false;
      const count = q(".count", loader), bar = q(".bar", loader), grain = q(".grain", loader), mark = q(".mark", loader), word = q(".word", loader);
      const n = { v: 0 };
      const finish = () => {
        if (done) return; done = true;
        G.timeline({ onComplete: () => { loader.hidden = true; S.lock(false); res(); } })
          .to([count, word, mark], { opacity: 0, y: -16, duration: 0.35, stagger: 0.04, ease: "power2.in" })
          .to(loader, { yPercent: -100, duration: 0.9, ease: "power3.inOut" }, "-=0.1");
      };
      const tl = G.timeline({ onComplete: finish });
      tl.fromTo(grain, { xPercent: -4, yPercent: -2 }, { xPercent: 4, yPercent: 2, duration: 1.8, ease: "none" }, 0)
        .fromTo(mark, { opacity: 0, scale: 0.92, filter: "blur(6px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.9, ease: EASE.big }, 0.05)
        .fromTo(word, { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.3)
        .to(n, { v: 100, duration: 1.3, ease: "power2.inOut", onUpdate: () => { if (count) count.textContent = String(Math.round(n.v)).padStart(3, "0"); } }, 0.1)
        .to(bar, { scaleX: 1, duration: 1.3, ease: "power2.inOut" }, 0.1);
      const skip = () => { tl.kill(); finish(); };
      qa(".skip-btn", loader).forEach((b) => b.addEventListener("click", skip));
      document.addEventListener("keydown", function k(e) { if (e.key === "Escape" || e.key === "Enter") { skip(); document.removeEventListener("keydown", k); } });
    });
  }

  /* ---------------- boot ---------------- */
  function boot() {
    initReveals(document);
    const start = () => { S.onLoaderDone.forEach((f) => { try { f(); } catch (e) { console.error(e); } }); S.onLoaderDone.length = 0; ST && ST.refresh(); };
    curtainIn().then(runLoader).then(start);
    S.onReady.forEach((f) => { try { f(); } catch (e) { console.error(e); } });
    if (ST) { window.addEventListener("load", () => ST.refresh()); if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => ST.refresh()); }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
  window.addEventListener("pagehide", () => { ST && ST.getAll().forEach((t) => t.kill()); });
})();
