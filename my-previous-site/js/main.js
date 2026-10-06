/* STILL. static build: page behaviour and animation.
   Depends on (loaded before this file): gsap, ScrollTrigger, SplitText,
   DrawSVGPlugin and Lenis, all in js/vendor. */
(function () {
  "use strict";

  gsap.registerPlugin(ScrollTrigger, SplitText, DrawSVGPlugin);

  // URL that accepts POST { email, source } as JSON. While this is empty the
  // sign-up forms only show their confirmation state and send nothing.
  const CONFIG = { notifyEndpoint: "" };

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const pad2 = (n) => String(n).padStart(2, "0");
  const isRendered = (el) => el.getClientRects().length > 0;

  const mobileQuery = window.matchMedia("(max-width: 767px)");
  const isMobile = mobileQuery.matches;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(pointer: fine)").matches;

  // Desktop and mobile run different scroll choreography, so crossing the
  // breakpoint starts over rather than trying to unpick pinned sections.
  mobileQuery.addEventListener("change", () => window.location.reload());

  /* ------------------------------------------------------------------ */
  /* Smooth scroll (Lenis) and scroll locking                            */
  /* ------------------------------------------------------------------ */

  let lenis = null;
  const scrollLocks = new Set();

  function initSmoothScroll() {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
    if (scrollLocks.size) lenis.stop();
  }

  function lockScroll(reason) {
    scrollLocks.add(reason);
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    if (lenis) lenis.stop();
  }

  function unlockScroll(reason) {
    scrollLocks.delete(reason);
    if (scrollLocks.size) return;
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
    if (lenis) lenis.start();
  }

  function scrollToTarget(target, duration = 1.2) {
    if (lenis) {
      lenis.scrollTo(target, { duration });
    } else if (typeof target === "number") {
      window.scrollTo({ top: target, behavior: "smooth" });
    } else {
      const el = $(target);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }

  // Scrolls to a fraction of a pinned ScrollTrigger's range.
  function scrollToProgress(trigger, progress, duration) {
    if (!trigger) return;
    scrollToTarget(trigger.start + (trigger.end - trigger.start) * progress, duration);
  }

  /* ------------------------------------------------------------------ */
  /* Shared reveal helpers                                               */
  /* ------------------------------------------------------------------ */

  // Fade-and-rise on scroll.
  function scrollReveal(el) {
    const delay = parseFloat(el.dataset.delay || "0");
    gsap.fromTo(
      el,
      { opacity: 0, y: 12 },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        ease: "power2.out",
        delay,
        scrollTrigger: { trigger: el, start: "top 85%", toggleActions: "play none none none" },
      },
    );
  }

  // Masked line / word / character rise.
  function textReveal(el) {
    if (reducedMotion) {
      gsap.set(el, { opacity: 1 });
      return;
    }
    const split = el.dataset.textReveal || "lines";
    const stagger = split === "chars" ? 0.02 : 0.09;
    const duration = split === "chars" ? 0.8 : 0.9;
    SplitText.create(el, {
      type: split,
      mask: split,
      autoSplit: split === "lines",
      onSplit: (self) =>
        gsap.fromTo(
          self[split],
          { yPercent: 115 },
          {
            yPercent: 0,
            duration,
            ease: "power2.out",
            stagger,
            scrollTrigger: { trigger: el, start: "top 85%", once: true },
          },
        ),
    });
    gsap.set(el, { opacity: 1 });
  }

  // Words brighten one by one as the paragraph scrolls through the viewport.
  function scrollIlluminate(el) {
    if (reducedMotion) {
      gsap.set(el, { opacity: 1 });
      return;
    }
    const dim = parseFloat(el.dataset.dim || "0.24");
    SplitText.create(el, {
      type: "words",
      aria: "none",
      onSplit: (self) => {
        gsap.set(self.words, { opacity: dim });
        gsap.set(el, { opacity: 1 });
        return gsap.to(self.words, {
          opacity: 1,
          ease: "none",
          duration: 1,
          stagger: 0.35,
          scrollTrigger: {
            trigger: el,
            start: el.dataset.start || "top 82%",
            end: el.dataset.end || "top 34%",
            scrub: true,
          },
        });
      },
    });
  }

  function initReveals(root) {
    if (!root) return;
    $$("[data-reveal]", root).filter(isRendered).forEach(scrollReveal);
    $$("[data-text-reveal]", root).filter(isRendered).forEach(textReveal);
    $$("[data-illuminate]", root).filter(isRendered).forEach(scrollIlluminate);
  }

  function initBlooms() {
    $$("[data-bloom]").forEach((el) => {
      gsap.to(el, { scale: 1.05, opacity: 1, duration: 2, yoyo: true, repeat: -1, ease: "sine.inOut" });
    });
  }

  // Title that rises character by character behind a word mask.
  function charRise(el, vars) {
    return SplitText.create(el, {
      type: "words,chars",
      mask: "words",
      onSplit: (self) => gsap.fromTo(self.chars, { yPercent: vars.from || 115 }, { yPercent: 0, ease: "power2.out", ...vars.to }),
    });
  }

  // Tracks which card of a horizontal snap carousel sits in the middle.
  function watchCarousel(track, onChange) {
    let frame = 0;
    let active = 0;
    track.addEventListener(
      "scroll",
      () => {
        if (frame) return;
        frame = requestAnimationFrame(() => {
          frame = 0;
          const cards = Array.from(track.children);
          if (!cards.length) return;
          const middle = track.scrollLeft + track.clientWidth / 2;
          let nearest = 0;
          let best = Infinity;
          cards.forEach((card, i) => {
            const distance = Math.abs(card.offsetLeft + card.offsetWidth / 2 - middle);
            if (distance < best) {
              best = distance;
              nearest = i;
            }
          });
          if (nearest !== active) {
            const previous = active;
            active = nearest;
            onChange(nearest, previous);
          }
        });
      },
      { passive: true },
    );
  }

  function scrollCarouselTo(track, index) {
    const card = track.children[index];
    if (!card) return;
    track.scrollTo({ left: card.offsetLeft - (track.clientWidth - card.offsetWidth) / 2, behavior: "smooth" });
  }

  /* ------------------------------------------------------------------ */
  /* Navigation, menu, cursor                                            */
  /* ------------------------------------------------------------------ */

  let closeMenu = () => {};

  function initNav() {
    const nav = $("[data-nav]");
    if (!nav) return;
    const hero = $("#hero");
    const menu = $("[data-menu]");
    let menuOpen = false;

    const update = () => {
      const scrolled = window.scrollY > 80;
      const overHero = !!hero && hero.getBoundingClientRect().bottom > 100;
      const solid = scrolled || isMobile;
      nav.style.transform = !overHero || menuOpen || isMobile ? "translateY(0)" : "translateY(-100%)";
      nav.style.backgroundColor = solid ? "rgba(239, 237, 230, 0.92)" : "transparent";
      nav.style.backdropFilter = solid ? "blur(20px)" : "none";
      nav.style.webkitBackdropFilter = scrolled ? "blur(20px)" : "none";
      nav.style.borderBottom = scrolled ? "1px solid rgba(140, 139, 134, 0.4)" : "1px solid transparent";
    };
    update();
    window.addEventListener("scroll", update, { passive: true });

    const setMenu = (open) => {
      if (!menu || open === menuOpen) return;
      menuOpen = open;
      menu.classList.toggle("is-open", open);
      menu.setAttribute("aria-hidden", String(!open));
      if (open) lockScroll("menu");
      else unlockScroll("menu");
      update();
    };
    closeMenu = () => setMenu(false);
    const openButton = $("[data-menu-open]");
    const closeButton = $("[data-menu-close]");
    if (openButton) openButton.addEventListener("click", () => setMenu(true));
    if (closeButton) closeButton.addEventListener("click", closeMenu);

    // In-page links glide with Lenis; links to another page behave normally.
    document.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const hash = link.getAttribute("href");
      event.preventDefault();
      closeMenu();
      scrollToTarget(hash === "#top" ? 0 : hash);
    });

    if (finePointer && !reducedMotion) {
      $$("[data-magnetic]").forEach((el) => {
        const strength = parseFloat(el.dataset.magnetic) || 0.35;
        const moveX = gsap.quickTo(el, "x", { duration: 0.4, ease: "power2.out" });
        const moveY = gsap.quickTo(el, "y", { duration: 0.4, ease: "power2.out" });
        el.addEventListener(
          "pointermove",
          (event) => {
            const rect = el.getBoundingClientRect();
            moveX((event.clientX - (rect.left + rect.width / 2)) * strength);
            moveY((event.clientY - (rect.top + rect.height / 2)) * strength);
          },
          { passive: true },
        );
        el.addEventListener(
          "pointerleave",
          () => {
            moveX(0);
            moveY(0);
          },
          { passive: true },
        );
      });
    }
  }

  function initCursor() {
    const root = $("[data-cursor]");
    if (!root || !finePointer || reducedMotion) return;
    const ring = $("[data-cursor-ring]", root);
    const dot = $("[data-cursor-dot]", root);
    const label = $("[data-cursor-text]", root);
    root.hidden = false;
    document.documentElement.classList.add("has-custom-cursor");

    const dotX = gsap.quickTo(dot, "x", { duration: 0.08, ease: "power2.out" });
    const dotY = gsap.quickTo(dot, "y", { duration: 0.08, ease: "power2.out" });
    const ringX = gsap.quickTo(ring, "x", { duration: 0.45, ease: "power2.out" });
    const ringY = gsap.quickTo(ring, "y", { duration: 0.45, ease: "power2.out" });

    let visible = false;
    const show = (state) => {
      if (state === visible) return;
      visible = state;
      gsap.to([dot, ring], { opacity: state ? 1 : 0, duration: 0.25, ease: "power2.out", overwrite: "auto" });
    };

    let mode = "default";
    const setMode = (next, text) => {
      if (text) label.textContent = text;
      if (next === mode) return;
      mode = next;
      const labeled = next === "labeled";
      const size = labeled ? 76 : next === "interactive" ? 56 : 36;
      gsap.set(ring, { mixBlendMode: labeled ? "normal" : "difference" });
      gsap.to(ring, {
        width: size,
        height: size,
        marginLeft: -size / 2,
        marginTop: -size / 2,
        backgroundColor: labeled ? "rgba(26,27,29,0.92)" : "rgba(255,255,255,0)",
        borderColor: labeled ? "rgba(26,27,29,0)" : "rgba(255,255,255,0.55)",
        duration: 0.35,
        ease: "power2.out",
        overwrite: "auto",
      });
      gsap.to(label, { opacity: labeled ? 1 : 0, duration: 0.25, ease: "power2.out", overwrite: "auto" });
      gsap.to(dot, {
        scale: labeled ? 0 : next === "interactive" ? 0.5 : 1,
        duration: 0.25,
        ease: "power2.out",
        overwrite: "auto",
      });
    };

    window.addEventListener(
      "pointermove",
      (event) => {
        dotX(event.clientX);
        dotY(event.clientY);
        ringX(event.clientX);
        ringY(event.clientY);
        show(true);
      },
      { passive: true },
    );
    window.addEventListener(
      "pointerover",
      (event) => {
        const target = event.target;
        if (!target || !target.closest) return;
        const labeled = target.closest("[data-cursor-label]");
        if (labeled) setMode("labeled", labeled.dataset.cursorLabel);
        else if (target.closest("a, button, input, textarea, select, [role='button']")) setMode("interactive");
        else setMode("default");
      },
      { passive: true },
    );
    document.documentElement.addEventListener("pointerleave", () => show(false));
  }

  /* ------------------------------------------------------------------ */
  /* Loader                                                              */
  /* ------------------------------------------------------------------ */

  function initLoader(onReveal) {
    const loader = $("[data-loader]");
    if (!loader) {
      onReveal();
      return;
    }
    const INK = "#1a1b1d";
    const TRACK = "rgba(26, 27, 29, 0.12)";
    const mark = $("[data-loader-mark]", loader);
    const word = $("[data-loader-word]", loader);
    const dot = $("[data-loader-dot]", loader);
    const count = $("[data-loader-count]", loader);
    const pills = $$("[data-pop]", loader);

    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    window.scrollTo(0, 0);
    lockScroll("loader");

    let pillLoop = null;
    if (reducedMotion) {
      word.style.backgroundImage = `linear-gradient(90deg, ${INK} 0%, ${INK} 100%)`;
      gsap.set(dot, { opacity: 1, y: 0 });
    } else {
      gsap.set(pills, { opacity: 0, scale: 0.55 });
      pillLoop = gsap.timeline({ repeat: -1, repeatDelay: 0.3, delay: 0.5 });
      pills.forEach((pill, i) => {
        const at = 0.42 * i;
        pillLoop
          .fromTo(
            pill,
            { opacity: 0, scale: 0.55, y: 10, rotation: i % 2 === 0 ? -3.5 : 3.5, filter: "blur(8px)" },
            { opacity: 1, scale: 1, y: 0, rotation: 0, filter: "blur(0px)", duration: 0.45, ease: "back.out(1.6)", force3D: true },
            at,
          )
          .to(pill, { y: -6, duration: 0.95, ease: "sine.inOut", force3D: true }, at + 0.45)
          .to(pill, { opacity: 0, y: -18, scale: 0.94, filter: "blur(5px)", duration: 0.32, ease: "power2.in", force3D: true }, at + 1.4);
      });
    }

    // Progress follows the page's images and fonts.
    const shown = { val: 0 };
    let target = 0;
    const setProgress = (value) => {
      if (value <= target) return;
      target = value;
      gsap.to(shown, {
        val: value,
        duration: 0.4 + ((value - shown.val) / 100) * 1.2,
        ease: "power2.out",
        overwrite: true,
        onUpdate: () => {
          if (!reducedMotion) {
            word.style.backgroundImage = `linear-gradient(90deg, ${INK} 0%, ${INK} ${shown.val}%, ${TRACK} ${shown.val}%)`;
          }
          count.textContent = String(Math.round(shown.val)).padStart(3, "0");
        },
      });
    };

    let minimumElapsed = false;
    let assetsReady = false;
    let revealed = false;

    const reveal = () => {
      if (revealed) return;
      revealed = true;
      const finish = () => {
        if (pillLoop) pillLoop.kill();
        loader.remove();
      };
      const release = () => {
        unlockScroll("loader");
        onReveal();
      };
      if (reducedMotion) {
        release();
        gsap.to(loader, { opacity: 0, duration: 0.6, ease: "power2.out", onComplete: finish });
        return;
      }
      const timeline = gsap.timeline({ onComplete: finish });
      timeline.fromTo(dot, { y: "-0.6em", opacity: 0 }, { y: "0em", opacity: 1, duration: 0.45, ease: "power2.out" });
      timeline.to({}, { duration: 0.4 });
      timeline.call(release);
      const title = $("[data-hero-title]");
      if (title && !isMobile) {
        // The loader wordmark flies into the exact footprint of the hero title.
        timeline.call(() => {
          const from = mark.getBoundingClientRect();
          const to = title.getBoundingClientRect();
          gsap.set(mark, { transformOrigin: "50% 50%" });
          gsap.to(mark, {
            x: to.left + to.width / 2 - (from.left + from.width / 2),
            y: to.top + to.height / 2 - (from.top + from.height / 2),
            scale: to.width / from.width,
            duration: 0.9,
            ease: "power3.inOut",
          });
        });
        timeline.to({}, { duration: 0.9 });
        timeline.to(loader, { opacity: 0, duration: 0.35, ease: "power1.out" }, "-=0.35");
      } else {
        timeline.to(mark, { scale: 1.6, duration: 0.55, ease: "power2.in" });
        timeline.to(loader, { opacity: 0, duration: 0.5, ease: "power1.inOut" }, "<");
      }
    };
    const maybeReveal = () => {
      if (minimumElapsed && assetsReady) reveal();
    };

    const sources = [...new Set($$("img").map((img) => img.getAttribute("src")).filter(Boolean))];
    const total = sources.length + 1;
    let loaded = 0;
    const assetDone = () => {
      loaded += 1;
      setProgress((loaded / total) * 100);
      if (loaded >= total) {
        assetsReady = true;
        maybeReveal();
      }
    };
    sources.forEach((src) => {
      const image = new Image();
      image.onload = image.onerror = assetDone;
      image.src = src;
    });
    const fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    fontsReady.then(assetDone, assetDone);

    window.setTimeout(
      () => {
        minimumElapsed = true;
        maybeReveal();
      },
      reducedMotion ? 400 : 2200,
    );
    window.setTimeout(reveal, 9000);
  }

  /* ------------------------------------------------------------------ */
  /* 01 Hero                                                             */
  /* ------------------------------------------------------------------ */

  function initScrollHint() {
    const dot = $("[data-scroll-dot]");
    if (!dot || !isRendered(dot)) return;
    if (reducedMotion) {
      gsap.set(dot, { opacity: 1, y: 9 });
      return;
    }
    gsap
      .timeline({ repeat: -1, repeatDelay: 0.5 })
      .set(dot, { y: 0, opacity: 0 })
      .to(dot, { opacity: 1, duration: 0.25, ease: "power1.out" })
      .to(dot, { y: 19, duration: 1, ease: "power2.inOut" }, 0.1)
      .to(dot, { opacity: 0, duration: 0.3, ease: "power1.in" }, 0.85);
  }

  // Desktop: the page opens on a bone-coloured wordmark. A circular window
  // follows the pointer and shows the dark stage (and the can) underneath;
  // scrolling grows that window until the stage fills the screen.
  function initHeroDesktop() {
    const hero = $("#hero");
    const clip = $("[data-hero-clip]");
    const ring = $("[data-hero-ring]");
    const dolly = $("[data-hero-dolly]");
    const parallax = $("[data-hero-parallax]");
    const overlay = $("[data-hero-overlay]");
    const hint = $("[data-hero-scrollhint]");
    const support = $("[data-hero-support]");
    const canWrap = $("[data-hero-can]");
    const canImage = $("img", canWrap);
    const canShadow = $(".can2d-shadow", canWrap);
    const BASE_RADIUS = 170;
    // The original camera saw about 4.54 world units of height; the can's
    // motion is kept in those units and converted to pixels here.
    const unit = () => window.innerHeight / 4.54;

    const windowState = {
      x: window.innerWidth / 2,
      y: 0.48 * window.innerHeight,
      entrance: 0,
      swell: 0,
      breath: 0,
      scrollBoost: 0,
      hasPointer: false,
    };
    const lock = { value: 0 }; // 0 = can follows the pointer, 1 = can rests in the centre
    const zoom = { value: 0 };
    const entrance = { value: 0 };
    const follow = { x: 0, y: 0, active: false };
    const bloomOffset = { x: 0, y: 0 };
    const canState = { x: 0, y: 0, lean: 0 };
    let pointerActive = false;
    let released = false;
    let startedAt = 0;

    gsap.set(canWrap, { opacity: 0 });

    const moveX = gsap.quickTo(windowState, "x", { duration: 0.62, ease: "power2.out" });
    const moveY = gsap.quickTo(windowState, "y", { duration: 0.62, ease: "power2.out" });

    if (!reducedMotion) {
      gsap.to(windowState, { breath: 9, duration: 2.2, yoyo: true, repeat: -1, ease: "sine.inOut" });
    }

    if (finePointer) {
      let lastX = 0;
      let lastY = 0;
      let lastTime = 0;
      const settle = gsap
        .delayedCall(0.3, () => {
          gsap.to(windowState, { swell: 0, duration: 1.1, ease: "power2.out", overwrite: "auto" });
        })
        .pause();
      window.addEventListener(
        "pointermove",
        (event) => {
          const now = performance.now();
          if (!windowState.hasPointer) {
            windowState.hasPointer = true;
            lastX = event.clientX;
            lastY = event.clientY;
            lastTime = now;
          }
          moveX(event.clientX);
          moveY(event.clientY);
          // Fast pointer travel makes the window swell, then relax.
          const elapsed = Math.max(now - lastTime, 1);
          const speed = (Math.hypot(event.clientX - lastX, event.clientY - lastY) / elapsed) * 1000;
          const swell = Math.min(130, (speed / 2200) * 130);
          if (swell > windowState.swell + 1) {
            gsap.to(windowState, { swell, duration: 0.3, ease: "power2.out", overwrite: "auto" });
          }
          settle.restart(true);
          lastX = event.clientX;
          lastY = event.clientY;
          lastTime = now;
          if (!reducedMotion) {
            pointerActive = true;
            released = false;
          }
        },
        { passive: true },
      );
    }

    const render = (time, deltaMs) => {
      const dt = Math.max(deltaMs / 1000, 0.001);
      const locked = lock.value;

      if (locked > 0.98 && !released) {
        released = true;
        pointerActive = false;
        windowState.hasPointer = false;
        moveX(window.innerWidth / 2);
        moveY(0.48 * window.innerHeight);
      }

      const falloff = Math.pow(1 - Math.min(locked / 0.6, 1), 3);
      if (pointerActive && locked < 0.999) {
        follow.x = clamp((windowState.x / window.innerWidth) * 2 - 1, -1, 1) * falloff;
        follow.y = clamp(-((windowState.y / window.innerHeight) * 2 - 1), -1, 1) * falloff;
        follow.active = true;
      } else {
        follow.active = false;
      }

      bloomOffset.x += ((windowState.x - window.innerWidth / 2) * 0.85 * falloff - bloomOffset.x) * 0.06;
      bloomOffset.y += ((windowState.y - window.innerHeight / 2) * 0.85 * falloff - bloomOffset.y) * 0.06;
      parallax.style.transform = `translate3d(${bloomOffset.x}px, ${bloomOffset.y}px, 0)`;

      const radius = Math.max(
        0,
        BASE_RADIUS * windowState.entrance + windowState.swell + windowState.breath * windowState.entrance + windowState.scrollBoost,
      );
      clip.style.clipPath = `circle(${radius.toFixed(1)}px at ${windowState.x.toFixed(1)}px ${windowState.y.toFixed(1)}px)`;
      ring.style.transform = `translate3d(${windowState.x}px, ${windowState.y}px, 0) translate(-50%, -50%) scale(${(radius / BASE_RADIUS).toFixed(3)})`;
      ring.style.opacity = (windowState.entrance * clamp(1 - windowState.scrollBoost / 240, 0, 1)).toFixed(3);

      // Can: eases toward the pointer, leans into its own motion, bobs gently.
      const targetX = follow.active ? 2.5 * follow.x : 0;
      const targetY = follow.active ? 1.6 * follow.y : 0;
      const ease = 0.09 + locked * 0.09;
      const previousX = canState.x;
      canState.x += (targetX - canState.x) * ease;
      canState.y += (targetY - canState.y) * ease;
      const lean = clamp(-(0.016 * ((1 / dt) * 1.4 * (canState.x - previousX))), -0.22, 0.22) * (follow.active ? 1 - locked : 0);
      canState.lean += (lean - canState.lean) * 0.075;

      const u = unit();
      const settled = entrance.value;
      const bob = startedAt && !reducedMotion ? 0.06 * Math.sin(((2 * Math.PI) / 6) * (time - startedAt)) : 0;
      const x = canState.x * u;
      const y = -(canState.y + bob) * u - 4 * u * (1 - settled);
      const scale = (0.8 + 0.2 * settled) * (1 + zoom.value);
      const rotation = (-canState.lean * 180) / Math.PI - 14 * (1 - settled);
      canWrap.style.opacity = settled.toFixed(3);
      canWrap.style.transform = `translate3d(${x.toFixed(2)}px, 0, 0)`;
      canImage.style.transform = `translate3d(0, ${y.toFixed(2)}px, 0) rotate(${rotation.toFixed(2)}deg) scale(${scale.toFixed(4)})`;
      if (canShadow) canShadow.style.opacity = clamp(1 - Math.abs(canState.y) * 1.4, 0, 1).toFixed(3);
    };
    gsap.ticker.add(render);

    if (!reducedMotion) {
      const items = $$("[data-support-item]", support);
      const rule = $("[data-support-rule]", support);
      gsap.set(items, { y: 26, opacity: 0 });
      gsap.set(rule, { scaleX: 0, transformOrigin: "left center" });

      const timeline = gsap.timeline({
        defaults: { ease: "power2.inOut" },
        scrollTrigger: {
          trigger: hero,
          start: "top top",
          end: "+=120%",
          pin: true,
          pinSpacing: true,
          scrub: true,
          invalidateOnRefresh: true,
          refreshPriority: 3,
        },
      });
      timeline
        .to(windowState, { scrollBoost: () => 1.2 * Math.hypot(window.innerWidth, window.innerHeight), ease: "power2.in", duration: 0.55 }, 0)
        .to(lock, { value: 1, ease: "power1.inOut", duration: 0.6 }, 0)
        .to(overlay, { opacity: 0, ease: "none", duration: 0.15 }, 0.48)
        .to(dolly, { scale: 1.09, duration: 1, ease: "none" }, 0)
        .to(zoom, { value: 0.09, duration: 1, ease: "none" }, 0)
        .to(hint, { opacity: 0, duration: 0.15, ease: "power1.out" }, 0);

      const supportIn = gsap.timeline({ paused: true });
      supportIn.to(items, { y: 0, opacity: 1, duration: 0.55, stagger: 0.08, ease: "power2.out" });
      supportIn.to(rule, { scaleX: 1, duration: 0.5 }, 0.2);
      let supportShown = false;
      timeline.eventCallback("onUpdate", () => {
        const progress = timeline.progress();
        if (!supportShown && progress > 0.58) {
          supportShown = true;
          supportIn.restart();
        } else if (supportShown && progress < 0.35) {
          supportShown = false;
          gsap.to(support, {
            opacity: 0,
            duration: 0.25,
            ease: "power1.out",
            overwrite: "auto",
            onComplete: () => {
              supportIn.pause(0);
              gsap.set(items, { y: 26, opacity: 0 });
              gsap.set(rule, { scaleX: 0 });
              gsap.set(support, { opacity: 1 });
            },
          });
        }
      });
    } else {
      // No pinned scrub: show the stage as a plain full-screen panel.
      windowState.scrollBoost = 1.2 * Math.hypot(window.innerWidth, window.innerHeight);
      gsap.set(overlay, { opacity: 0 });
    }

    return function start() {
      gsap.set($$("[data-letter]", overlay), { opacity: 1, y: 0 });
      startedAt = gsap.ticker.time;
      gsap.to(windowState, { entrance: 1, duration: 1.2, delay: 0.15, ease: "power2.inOut" });
      gsap.to(entrance, { value: 1, duration: 1.6, ease: "power4.out" });
    };
  }

  function initHeroMobile() {
    const canWrap = $("[data-hero-can-mobile]");
    const canImage = $("img", canWrap);
    const title = $("[data-hero-title-mobile]");
    gsap.set(canWrap, { opacity: 0 });

    return function start() {
      const letters = $$("[data-letter]", title);
      if (reducedMotion) {
        gsap.set(letters, { opacity: 1, y: 0 });
        gsap.set(canWrap, { opacity: 1 });
        return;
      }
      gsap.fromTo(letters, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.9, ease: "power2.out", stagger: 0.05 });
      gsap.to(canWrap, { opacity: 1, duration: 1.2, ease: "power2.out" });
      gsap.fromTo(
        canImage,
        { yPercent: -60, scale: 0.8, rotation: -14 },
        {
          yPercent: 0,
          scale: 1,
          rotation: 0,
          duration: 1.6,
          ease: "power4.out",
          onComplete: () => {
            gsap.to(canImage, { y: -8, duration: 3, yoyo: true, repeat: -1, ease: "sine.inOut" });
          },
        },
      );
      ScrollTrigger.refresh();
    };
  }

  /* ------------------------------------------------------------------ */
  /* 02 Flavors                                                          */
  /* ------------------------------------------------------------------ */

  function initFlavorsDesktop() {
    const section = $("#flavors");
    const pin = $("[data-flavors-pin]");
    const label = $("[data-flavor-label]");
    const title = $("[data-flavor-title]");
    const count = $("[data-flavor-count]");
    const panels = $$("[data-flavor-panel]");
    const backgrounds = $$("[data-flavor-bg]");
    const ghosts = $$("[data-flavor-ghost]");
    const blooms = $$("[data-flavor-bloom]");
    const cans = $$("[data-flavor-can]");
    const stage = $("[data-flavor-stage]");
    const dots = $$("[data-flavor-dot]");
    const SIDE = [1, -1, 1]; // which side each can arrives from
    // The stage camera saw about 3.51 world units of height.
    const unit = () => stage.clientHeight / 3.509;
    const degrees = (radians) => (radians * 180) / Math.PI;

    cans.forEach((can, i) => {
      gsap.set(can, i === 0 ? { x: 0, scale: 1, opacity: 1 } : { x: () => 3 * SIDE[i] * unit(), scale: 0.94, opacity: 0 });
    });

    gsap.fromTo(
      label,
      { y: 14, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.6,
        ease: "power2.out",
        immediateRender: true,
        scrollTrigger: { trigger: section, start: "top 80%", toggleActions: "play none none none" },
      },
    );
    charRise(title, { to: { duration: 0.8, stagger: 0.022, scrollTrigger: { trigger: section, start: "top 80%", once: true } } });
    gsap.set(title, { opacity: 1 });
    gsap.fromTo(
      [panels[0].parentElement, stage],
      { y: 70, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: "power2.out", stagger: 0.12, scrollTrigger: { trigger: section, start: "top 55%", once: true } },
    );

    let active = 0; // flavour the scroll position asks for
    let shown = 0; // flavour whose text is currently on screen
    let swapping = false;

    const showPanel = (panel) => {
      gsap.fromTo(panel, { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out" });
      gsap.fromTo(
        $$("[data-stage-item]", panel),
        { y: 18, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.45, ease: "power2.out", stagger: 0.05, delay: 0.05 },
      );
    };
    const swapText = () => {
      if (shown === active || swapping) return;
      swapping = true;
      gsap.to(panels[shown], {
        y: -26,
        opacity: 0,
        duration: 0.25,
        ease: "power3.in",
        onComplete: () => {
          panels[shown].hidden = true;
          shown = active;
          panels[shown].hidden = false;
          showPanel(panels[shown]);
          swapping = false;
          swapText();
        },
      });
    };

    const setActive = (next) => {
      if (next === active) return;
      const forward = next > active;
      active = next;
      const side = SIDE[next];
      const u = unit();
      cans.forEach((can, i) => {
        if (i === next) {
          gsap.fromTo(
            can,
            { x: 3 * side * u, y: -0.12 * u, rotation: degrees(0.16 * side), scale: 0.94, opacity: 0 },
            { x: 0, y: 0, rotation: 0, scale: 1, opacity: 1, duration: 0.85, ease: "power2.out", delay: 0.1, overwrite: "auto" },
          );
        } else {
          gsap.to(can, {
            x: -2.2 * side * u,
            y: 0.1 * u,
            rotation: degrees(-0.14 * side),
            scale: 0.94,
            opacity: 0,
            duration: 0.45,
            ease: "power2.in",
            overwrite: "auto",
          });
        }
      });
      blooms.forEach((el, i) => gsap.to(el, { opacity: i === next ? 1 : 0, duration: 0.7, ease: "power2.inOut", overwrite: "auto" }));
      backgrounds.forEach((el, i) => gsap.to(el, { opacity: i === next ? 1 : 0, duration: 0.8, ease: "power2.inOut", overwrite: "auto" }));
      ghosts.forEach((el, i) =>
        gsap.to(el, {
          opacity: i === next ? 1 : 0,
          y: i === next ? 0 : forward ? -40 : 40,
          duration: 0.8,
          ease: "power2.inOut",
          overwrite: "auto",
          force3D: true,
        }),
      );
      count.textContent = `${next + 1} / 3`;
      dots.forEach((dot, i) => {
        dot.style.color = i === next ? "var(--color-ink)" : "var(--color-mist)";
      });
      swapText();
    };

    const trigger = ScrollTrigger.create({
      trigger: pin,
      start: "top top",
      end: () => `+=${3 * window.innerHeight}`,
      pin: true,
      pinSpacing: true,
      scrub: 1,
      snap: { snapTo: [0, 1 / 3, 2 / 3, 1], duration: { min: 0.25, max: 0.55 }, ease: "power2.inOut", directional: false, delay: 0.1 },
      invalidateOnRefresh: true,
      refreshPriority: 1,
      onUpdate: (self) => {
        // Thresholds differ by direction so the flavour does not flicker
        // when the scroll position rests near a boundary.
        const p = self.progress;
        const first = 1 / 6;
        let next;
        if (active === 0) next = p > 0.55 ? 2 : p > first + 0.05 ? 1 : 0;
        else if (active === 1) next = p < first - 0.05 ? 0 : p > 0.55 ? 2 : 1;
        else next = p < first - 0.05 ? 0 : p < 0.45 ? 1 : 2;
        setActive(next);
      },
    });

    dots.forEach((dot, i) => dot.addEventListener("click", () => scrollToProgress(trigger, i / 3, 1)));
  }

  function initFlavorsMobile() {
    const track = $("[data-mflavor-track]");
    if (!track) return;
    const backgrounds = $$("[data-mflavor-bg]");
    const dots = $$("[data-mflavor-dot]");
    const titles = $$("[data-card-title]", track);
    let split = null;
    let started = false;

    const revealCard = (index) => {
      const title = titles[index];
      const items = $$("[data-card-item]", title.closest("article"));
      if (reducedMotion) {
        gsap.set([title, ...items], { opacity: 1 });
        return;
      }
      if (split) split.revert();
      split = SplitText.create(title, {
        type: "words,chars",
        mask: "words",
        onSplit: (self) => {
          gsap.set(title, { opacity: 1 });
          return gsap.fromTo(self.chars, { yPercent: 108 }, { yPercent: 0, duration: 0.55, ease: "power2.out", stagger: 0.03, overwrite: "auto" });
        },
      });
      gsap.fromTo(items, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out", stagger: 0.05, delay: 0.1, overwrite: "auto" });
    };

    ScrollTrigger.create({
      trigger: track,
      start: "top 85%",
      once: true,
      onEnter: () => {
        if (started) return;
        started = true;
        revealCard(0);
      },
    });

    watchCarousel(track, (next, previous) => {
      started = true;
      backgrounds.forEach((el, i) => gsap.to(el, { opacity: i === next ? 1 : 0, duration: 0.8, ease: "power2.inOut", overwrite: "auto" }));
      dots.forEach((dot, i) => {
        dot.style.color = i === next ? "var(--color-ink)" : "var(--color-mist)";
      });
      const oldTitle = titles[previous];
      gsap.to([oldTitle, ...$$("[data-card-item]", oldTitle.closest("article"))], { opacity: 0, duration: 0.12, ease: "power1.out", overwrite: "auto" });
      revealCard(next);
    });
    dots.forEach((dot, i) => dot.addEventListener("click", () => scrollCarouselTo(track, i)));
  }

  /* ------------------------------------------------------------------ */
  /* 03 Inside (ingredients)                                             */
  /* ------------------------------------------------------------------ */

  // Stand-in for the 3D can's quarter turn between ingredients.
  function turnCan(image) {
    if (reducedMotion) return;
    gsap
      .timeline({ overwrite: true })
      .to(image, { scaleX: 0.8, rotation: -3, duration: 0.22, ease: "power2.in" })
      .to(image, { scaleX: 1, rotation: 0, duration: 0.6, ease: "power3.out" });
  }

  function initInside() {
    const section = $("#inside");
    if (!section) return;
    const title = $("[data-inside-title]");
    const halo = $("[data-inside-halo]");
    const canImage = $("[data-inside-can] img");
    const colors = $$("[data-deck-track] article").map((el) => el.dataset.halo);

    if (reducedMotion) {
      gsap.set(title, { opacity: 1 });
    } else if (isMobile) {
      gsap.fromTo(title, { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9, ease: "power2.out", scrollTrigger: { trigger: section, start: "top 75%", once: true } });
    } else {
      SplitText.create(title, {
        type: "chars",
        onSplit: (self) =>
          gsap.fromTo(
            self.chars,
            { yPercent: 22, opacity: 0 },
            { yPercent: 0, opacity: 1, duration: 0.8, ease: "power2.out", stagger: 0.022, scrollTrigger: { trigger: section, start: "top 75%", once: true } },
          ),
      });
      gsap.set(title, { opacity: 1 });
    }

    const tintHalo = (index) => gsap.to(halo, { backgroundColor: colors[index], duration: 0.5, ease: "power2.inOut", overwrite: "auto" });

    if (isMobile) {
      initInsideMobile(tintHalo, canImage);
      return;
    }

    const pills = $$("[data-inside-pill]");
    const lefts = $$("[data-inside-left]");
    const rights = $$("[data-inside-right]");
    let active = 0;
    let shown = 0;
    let swapping = false;
    let nameSplit = null;

    const parts = (index) => [$("[data-inside-name]", lefts[index]), $("[data-inside-sci]", lefts[index]), rights[index]];

    const stylePills = () => {
      pills.forEach((pill, i) => {
        const on = i === active;
        pill.style.border = `1px solid ${on ? "var(--color-bone)" : "rgba(239,237,230,0.35)"}`;
        pill.style.backgroundColor = on ? "var(--color-bone)" : "transparent";
        pill.style.color = on ? "var(--color-ink)" : "var(--color-bone)";
        pill.style.opacity = on ? "1" : "0.65";
      });
    };

    const showIngredient = (index) => {
      const [name, , right] = parts(index);
      gsap.fromTo(parts(index), { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.45, delay: 0.1, ease: "power3.out", stagger: 0.05, overwrite: "auto" });
      if (nameSplit) nameSplit.revert();
      nameSplit = null;
      if (!reducedMotion) {
        nameSplit = SplitText.create(name, {
          type: "chars",
          onSplit: (self) =>
            gsap.fromTo(
              self.chars,
              { yPercent: 60, opacity: 0 },
              { yPercent: 0, opacity: 1, duration: 0.55, ease: "power2.out", stagger: 0.028, delay: 0.12, overwrite: "auto" },
            ),
        });
      }
      gsap.fromTo(halo, { scale: 1.45 }, { scale: 1.6, duration: 0.9, ease: "power2.out", overwrite: "auto" });
      gsap.fromTo(
        $$("[data-bot]", lefts[index]),
        { drawSVG: "0%" },
        { drawSVG: "100%", duration: 0.9, ease: "power1.inOut", stagger: 0.08, delay: 0.15, overwrite: "auto" },
      );
      const bar = $("[data-inside-bar]", right);
      const dose = $("[data-inside-dose]", right);
      gsap.fromTo(bar, { scaleX: 0 }, { scaleX: parseFloat(bar.dataset.insideBar), duration: 0.8, delay: 0.25, ease: "power2.inOut", overwrite: "auto" });
      const counter = { val: 0 };
      gsap.to(counter, {
        val: parseFloat(dose.dataset.insideDose),
        duration: 0.8,
        delay: 0.25,
        ease: "power2.out",
        onUpdate: () => {
          dose.textContent = String(Math.round(counter.val));
        },
      });
    };

    const swap = () => {
      if (shown === active || swapping) return;
      swapping = true;
      gsap.to(parts(shown), {
        opacity: 0,
        y: -26,
        duration: 0.22,
        ease: "power3.in",
        overwrite: "auto",
        onComplete: () => {
          lefts[shown].hidden = true;
          rights[shown].hidden = true;
          shown = active;
          lefts[shown].hidden = false;
          rights[shown].hidden = false;
          showIngredient(shown);
          swapping = false;
          swap();
        },
      });
    };

    const setActive = (next) => {
      if (next === active) return;
      active = next;
      stylePills();
      tintHalo(next);
      turnCan(canImage);
      swap();
    };

    const trigger = ScrollTrigger.create({
      trigger: section,
      start: "top top",
      end: () => `+=${4 * window.innerHeight}`,
      pin: true,
      pinSpacing: true,
      scrub: 1,
      snap: { snapTo: [0, 0.25, 0.5, 0.75, 1], duration: { min: 0.2, max: 0.5 }, ease: "power2.inOut", directional: false, delay: 0.1 },
      invalidateOnRefresh: true,
      onUpdate: (self) => setActive(clamp(Math.floor(4 * self.progress - 1e-4), 0, 3)),
    });
    pills.forEach((pill, i) => pill.addEventListener("click", () => scrollToProgress(trigger, 0.25 * i, 1)));

    // First ingredient plays in when the section arrives.
    gsap.set(parts(0), { opacity: 0 });
    ScrollTrigger.create({ trigger: section, start: "top 60%", once: true, onEnter: () => showIngredient(0) });

    lefts.forEach((left) => {
      const hover = $("[data-inside-hover]", left);
      hover.addEventListener("pointerenter", () => {
        gsap.to(halo, { opacity: 0.7, scale: 1.75, duration: 0.6, ease: "power2.out", overwrite: "auto" });
        gsap.fromTo($$("[data-bot]", left), { drawSVG: "0%" }, { drawSVG: "100%", duration: 0.7, ease: "power1.inOut", stagger: 0.06, overwrite: "auto" });
      });
      hover.addEventListener("pointerleave", () => {
        gsap.to(halo, { opacity: 0.5, scale: 1.6, duration: 0.7, ease: "power2.inOut", overwrite: "auto" });
      });
      if (!reducedMotion) {
        gsap.fromTo(
          $("[data-inside-svg]", left),
          { rotation: -3.5, transformOrigin: "50% 50%" },
          { rotation: 3.5, duration: 5, yoyo: true, repeat: -1, ease: "sine.inOut" },
        );
      }
    });

    // Light pointer parallax on the can.
    if (finePointer && !reducedMotion) {
      const canWrap = $("[data-inside-can]");
      const shiftX = gsap.quickTo(canWrap, "x", { duration: 0.9, ease: "power2.out" });
      const shiftY = gsap.quickTo(canWrap, "y", { duration: 0.9, ease: "power2.out" });
      section.addEventListener(
        "pointermove",
        (event) => {
          shiftX((event.clientX / window.innerWidth - 0.5) * 22);
          shiftY((event.clientY / window.innerHeight - 0.5) * 12);
        },
        { passive: true },
      );
    }
  }

  function initInsideMobile(tintHalo, canImage) {
    const track = $("[data-deck-track]");
    const dots = $$("[data-deck-dot]");
    const titles = $$("[data-deck-title]", track);
    let split = null;
    let pending = true;

    const revealCard = (index) => {
      const title = titles[index];
      const items = $$("[data-deck-item]", title.closest("article"));
      if (reducedMotion) {
        gsap.set([title, ...items], { opacity: 1 });
        return;
      }
      if (split) split.revert();
      split = SplitText.create(title, {
        type: "words,chars",
        mask: "words",
        onSplit: (self) => {
          gsap.set(title, { opacity: 1 });
          return gsap.fromTo(self.chars, { yPercent: 108 }, { yPercent: 0, duration: 0.5, ease: "power2.out", stagger: 0.02, overwrite: "auto" });
        },
      });
      gsap.fromTo(items, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out", stagger: 0.07, delay: 0.08, overwrite: "auto" });
    };

    ScrollTrigger.create({
      trigger: track,
      start: "top 85%",
      once: true,
      onEnter: () => {
        if (!pending) return;
        pending = false;
        revealCard(0);
      },
    });

    watchCarousel(track, (next, previous) => {
      pending = false;
      dots.forEach((dot, i) => {
        dot.style.color = i === next ? "var(--color-bone)" : "rgba(239,237,230,0.35)";
      });
      tintHalo(next);
      turnCan(canImage);
      const oldTitle = titles[previous];
      gsap.to([oldTitle, ...$$("[data-deck-item]", oldTitle.closest("article"))], { opacity: 0, duration: 0.12, ease: "power1.out", overwrite: "auto" });
      revealCard(next);
    });
    dots.forEach((dot, i) => dot.addEventListener("click", () => scrollCarouselTo(track, i)));
  }

  /* ------------------------------------------------------------------ */
  /* 04 Story                                                            */
  /* ------------------------------------------------------------------ */

  function initStory() {
    const section = $("#story");
    if (!section) return;
    if (isMobile) initStoryMobile(section);
    else initStoryDesktop();
  }

  function initStoryDesktop() {
    const pin = $("[data-story-pin]");
    const intro = $("[data-story-intro]");
    const stage = $("[data-story-stage]");
    const ghosts = $$("[data-story-ghost]");
    const figures = $$("[data-story-figure]");
    const panels = $$("[data-story-panel]");
    const progressBar = $("[data-story-progress]");
    const years = $$("[data-story-year]");
    const total = panels.length;
    const step = 1 / (total - 1);
    let active = 0;
    let shown = 0;
    let swapping = false;

    const showPanel = (panel) => {
      gsap.fromTo(panel, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out", overwrite: "auto" });
      gsap.fromTo(
        $$("[data-story-item]", panel),
        { y: 16, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.45, ease: "power2.out", stagger: 0.05, delay: 0.05, overwrite: "auto" },
      );
    };
    const swap = () => {
      if (shown === active || swapping) return;
      swapping = true;
      gsap.to(panels[shown], {
        y: -24,
        opacity: 0,
        duration: 0.22,
        ease: "power3.in",
        overwrite: "auto",
        onComplete: () => {
          panels[shown].hidden = true;
          shown = active;
          panels[shown].hidden = false;
          showPanel(panels[shown]);
          swapping = false;
          swap();
        },
      });
    };

    const setActive = (next) => {
      if (next === active) return;
      const forward = next > active;
      active = next;
      figures.forEach((figure, i) => {
        if (i === next) {
          gsap.fromTo(
            figure,
            { scale: forward ? 0.86 : 1.14, opacity: 0, y: forward ? 46 : -46 },
            { scale: 1, opacity: 1, y: 0, duration: 0.9, ease: "power2.out", delay: 0.08, overwrite: "auto", force3D: true },
          );
        } else {
          gsap.to(figure, {
            scale: i < next ? 1.14 : 0.86,
            opacity: 0,
            y: i < next ? -46 : 46,
            duration: 0.6,
            ease: "power2.in",
            overwrite: "auto",
            force3D: true,
          });
        }
      });
      ghosts.forEach((ghost, i) =>
        gsap.to(ghost, {
          opacity: i === next ? 1 : 0,
          y: i === next ? 0 : forward ? -60 : 60,
          duration: 0.9,
          ease: "power2.inOut",
          overwrite: "auto",
          force3D: true,
        }),
      );
      years.forEach((year, i) => {
        year.style.color = i === next ? "var(--color-ink)" : "var(--color-mist)";
      });
      swap();
    };

    const stops = panels.map((_, i) => 0.1 + (i / (total - 1)) * 0.9);
    const trigger = ScrollTrigger.create({
      trigger: pin,
      start: "top top",
      end: () => `+=${window.innerHeight * (total - 0.4)}`,
      pin: true,
      pinSpacing: true,
      scrub: 1,
      snap: { snapTo: [0, ...stops], duration: { min: 0.25, max: 0.55 }, ease: "power2.inOut" },
      invalidateOnRefresh: true,
      onUpdate: (self) => {
        const p = self.progress;
        // First tenth: the headline lifts away and the timeline fades in.
        const out = clamp(p / 0.08, 0, 1);
        intro.style.opacity = String(1 - out);
        intro.style.transform = `translateY(${-40 * out}px)`;
        stage.style.opacity = String(clamp((p - 0.04) / 0.08, 0, 1));
        const travel = clamp((p - 0.1) / 0.9, 0, 1);
        progressBar.style.transform = `scaleY(${travel})`;
        let next = active;
        while (next < total - 1 && travel > (next + 0.5) * step + 0.05) next += 1;
        while (next > 0 && travel < (next - 0.5) * step - 0.05) next -= 1;
        setActive(next);
      },
    });
    years.forEach((year, i) => year.addEventListener("click", () => scrollToProgress(trigger, stops[i], 1.2)));
  }

  function initStoryMobile(section) {
    const label = $("[data-story-mlabel]");
    const heading = $("[data-story-mtitle]");
    gsap.fromTo(
      label,
      { y: 32, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.9, ease: "power3.out", scrollTrigger: { trigger: section, start: "top 75%", toggleActions: "play none none none" } },
    );
    charRise(heading, { to: { duration: 0.8, stagger: 0.016, scrollTrigger: { trigger: section, start: "top 75%", once: true } } });
    gsap.set(heading, { opacity: 1 });

    const runway = $("[data-mstory]");
    const ghosts = $$("[data-mstory-ghost]");
    const figures = $$("[data-mstory-figure]");
    const panels = $$("[data-mstory-panel]");
    const years = $$("[data-mstory-year]");
    let active = 0;
    let within = 0; // progress through the current chapter, 0 to 1
    let words = [];
    let wordSplit = null;
    let titleSplit = null;

    // Each chapter: the photo wipes open, then the paragraph lights up word by word.
    const paint = () => {
      const figure = figures[active];
      const open = Math.min(1, within / 0.42);
      figure.style.clipPath = `inset(0% 0% ${(1 - open) * 92}% 0%)`;
      figure.style.opacity = String(0.4 + 0.6 * open);
      $("img", figure).style.transform = `scale(${1.12 - 0.12 * Math.min(1, within / 0.55)})`;
      const lit = clamp((within - 0.3) / 0.55, 0, 1);
      words.forEach((word, i) => {
        word.style.opacity = String(clamp(lit * (words.length + 3) - i, 0.24, 1));
      });
    };

    const prepareText = (index) => {
      const title = $("[data-mstory-title]", panels[index]);
      const text = $("[data-mstory-text]", panels[index]);
      gsap.set([title, text], { opacity: 1, y: 0 });
      if (wordSplit) wordSplit.revert();
      wordSplit = SplitText.create(text, { type: "words", aria: "none" });
      words = wordSplit.words || [];
      words.forEach((word) => {
        word.style.opacity = "0.24";
      });
      if (!reducedMotion) {
        if (titleSplit) titleSplit.revert();
        titleSplit = charRise(title, { from: 105, to: { duration: 0.5, stagger: 0.013, overwrite: "auto" } });
      }
      paint();
    };

    const setActive = (next) => {
      if (next === active) return;
      const previous = active;
      const direction = next > previous ? 1 : -1;
      active = next;
      ghosts.forEach((ghost, i) => {
        if (i === next) {
          gsap.fromTo(ghost, { opacity: 0, yPercent: 7 * direction }, { opacity: 1, yPercent: 0, duration: 0.6, ease: "power2.out", overwrite: "auto" });
        } else {
          gsap.to(ghost, { opacity: 0, duration: 0.4, ease: "power2.in", overwrite: "auto" });
        }
      });
      figures.forEach((figure, i) => {
        if (i !== next) gsap.to(figure, { opacity: 0, duration: 0.3, ease: "power2.in", overwrite: "auto" });
      });
      years.forEach((year, i) => {
        year.style.color = i === next ? "var(--color-ink)" : "var(--color-mist)";
      });
      const leaving = panels[previous];
      gsap.to([$("[data-mstory-title]", leaving), $("[data-mstory-text]", leaving)], {
        opacity: 0,
        y: -12,
        duration: 0.16,
        ease: "power2.in",
        overwrite: "auto",
        onComplete: () => {
          panels.forEach((panel, i) => {
            panel.hidden = i !== active;
          });
          prepareText(active);
        },
      });
    };

    const trigger = ScrollTrigger.create({
      trigger: runway,
      start: "top top",
      end: "bottom bottom",
      onUpdate: (self) => {
        const next = Math.min(4, Math.floor(5 * self.progress));
        within = clamp(5 * self.progress - next, 0, 1);
        setActive(next);
        paint();
      },
    });
    prepareText(0);
    years.forEach((year, i) => year.addEventListener("click", () => scrollToProgress(trigger, (i + 0.72) / 5, 0.9)));
  }

  /* ------------------------------------------------------------------ */
  /* 05 Press                                                            */
  /* ------------------------------------------------------------------ */

  function initPress() {
    const section = $("#press");
    if (!section) return;
    const marquee = $("[data-press-marquee]");
    const solid = $('[data-press-row="solid"]');
    const outline = $('[data-press-row="outline"]');

    $$("[data-press-quote]").forEach((figure, i) => {
      gsap.set(figure, { opacity: 1 });
      const quote = $("[data-quote-visual]", figure);
      const caption = $("figcaption", figure);
      if (!reducedMotion) {
        SplitText.create(quote, {
          type: "lines",
          mask: "lines",
          autoSplit: true,
          aria: "none",
          onSplit: (self) =>
            gsap.fromTo(
              self.lines,
              { yPercent: 115 },
              { yPercent: 0, duration: 0.85, ease: "power2.out", stagger: 0.09, delay: 0.12 * i, scrollTrigger: { trigger: figure, start: "top 85%", once: true } },
            ),
        });
      }
      gsap.fromTo(
        caption,
        { opacity: 0, y: 12 },
        { opacity: 1, y: 0, duration: 0.6, ease: "power2.out", delay: 0.45 + 0.12 * i, scrollTrigger: { trigger: figure, start: "top 85%", once: true } },
      );
    });

    if (reducedMotion) return;

    // Two rows drift in opposite directions; fast scrolling skews and speeds them up.
    const rows = [
      gsap.to(solid, { xPercent: -50, duration: 38, ease: "none", repeat: -1 }),
      gsap.fromTo(outline, { xPercent: -50 }, { xPercent: 0, duration: 52, ease: "none", repeat: -1 }),
    ];
    const state = { skew: 0 };
    const setSkew = gsap.quickSetter(marquee, "skewX", "deg");
    const limit = gsap.utils.clamp(-6, 6);
    ScrollTrigger.create({
      trigger: section,
      start: "top bottom",
      end: "bottom top",
      onUpdate: (self) => {
        const velocity = self.getVelocity();
        const skew = limit(-(velocity / 420));
        if (Math.abs(skew) > Math.abs(state.skew)) {
          state.skew = skew;
          gsap.to(state, { skew: 0, duration: 0.9, ease: "power2.out", overwrite: true, onUpdate: () => setSkew(state.skew) });
        }
        const speed = gsap.utils.clamp(1, 4, 1 + Math.abs(velocity) / 1200);
        rows.forEach((row) => {
          gsap.to(row, { timeScale: speed, duration: 0.4, ease: "power1.out", overwrite: "auto" });
          gsap.to(row, { timeScale: 1, duration: 1.4, delay: 0.4, ease: "power2.out", overwrite: false });
        });
      },
    });
  }

  /* ------------------------------------------------------------------ */
  /* 06 Shop and stockists                                               */
  /* ------------------------------------------------------------------ */

  function initShop() {
    const section = $("#shop");
    if (!section) return;
    const pace = isMobile ? 0.7 : 1;
    const label = $("[data-shop-label]");
    const title = $("[data-shop-title]");
    const stockists = $("#stockists");
    const columns = $$("[data-stockist-col]");
    const soon = $("[data-shop-soon]");
    const rules = $$("[data-shop-rule]");
    const or = $("[data-shop-or]");

    gsap.fromTo(
      label,
      { y: 40, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: "power3.out", scrollTrigger: { trigger: section, start: "top 80%", toggleActions: "play none none none" } },
    );
    SplitText.create(title, {
      type: "lines",
      mask: "lines",
      autoSplit: true,
      onSplit: (self) =>
        gsap.fromTo(
          self.lines,
          { yPercent: 115 },
          { yPercent: 0, duration: 0.9, ease: "power2.out", stagger: 0.09, scrollTrigger: { trigger: section, start: "top 80%", once: true } },
        ),
    });
    gsap.set(title, { opacity: 1 });

    columns.forEach((column, i) => {
      const scrollTrigger = { trigger: column, start: "top 85%", toggleActions: "play none none none" };
      gsap.fromTo(column, { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: "power3.out", delay: 0.15 * i * pace, scrollTrigger });
      gsap.fromTo(
        $$("[data-stockist-item]", column),
        { y: 12, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: "power2.out", stagger: 0.06 * pace, delay: 0.15 * i * pace + 0.25, scrollTrigger: { ...scrollTrigger } },
      );
      // Accordion on small screens (one city open at a time).
      $("[data-stockist-toggle]", column).addEventListener("click", () => {
        if (!isMobile) return;
        const open = !column.classList.contains("is-open");
        columns.forEach((other) => other.classList.toggle("is-open", open && other === column));
        requestAnimationFrame(() => requestAnimationFrame(() => ScrollTrigger.refresh()));
      });
    });

    gsap.fromTo(
      soon,
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: "power3.out", delay: 0.45 * pace, scrollTrigger: { trigger: soon, start: "top 90%", toggleActions: "play none none none" } },
    );
    gsap.fromTo(
      rules,
      { scaleX: 0 },
      { scaleX: 1, duration: 0.6, ease: "power3.out", scrollTrigger: { trigger: rules[0], start: "top 88%", toggleActions: "play none none none" } },
    );
    gsap.fromTo(
      or,
      { opacity: 0 },
      { opacity: 1, duration: 0.6, ease: "power3.out", delay: 0.15, scrollTrigger: { trigger: or, start: "top 88%", toggleActions: "play none none none" } },
    );
    $$("[data-product-wrap]")
      .filter(isRendered)
      .forEach((wrap, i) => {
        gsap.fromTo(
          wrap,
          { y: 80, opacity: 0, scale: 0.96 },
          { y: 0, opacity: 1, scale: 1, duration: 1, ease: "power3.out", delay: 0.2 * i * pace, scrollTrigger: { trigger: wrap, start: "top 85%", toggleActions: "play none none none" } },
        );
      });

    // A small can follows the pointer over the stockist lists.
    const preview = $("[data-stockist-preview]");
    if (preview && finePointer && !isMobile) {
      const layers = $$("[data-preview-layer]", preview);
      const moveX = gsap.quickTo(preview, "x", { duration: 0.5, ease: "power2.out" });
      const moveY = gsap.quickTo(preview, "y", { duration: 0.5, ease: "power2.out" });
      const showCity = (index) => {
        const visible = index !== null;
        if (visible) {
          layers.forEach((layer, i) => {
            layer.style.opacity = i === index ? "1" : "0";
          });
        }
        gsap.to(preview, { opacity: visible ? 1 : 0, scale: visible ? 1 : 0.92, duration: 0.4, ease: "power2.out", overwrite: "auto" });
      };
      stockists.addEventListener(
        "pointermove",
        (event) => {
          moveX(event.clientX + 26);
          moveY(event.clientY - 200);
        },
        { passive: true },
      );
      columns.forEach((column, i) => column.addEventListener("pointerenter", () => showCity(i)));
      stockists.addEventListener("pointerleave", () => showCity(null));
    }
  }

  /* ------------------------------------------------------------------ */
  /* Products, cart, checkout, sign-up forms                             */
  /* ------------------------------------------------------------------ */

  const FREE_SHIPPING_THRESHOLD = 50;
  const formatPrice = (value) => (value % 1 === 0 ? String(value) : value.toFixed(2));
  const escapeHtml = (text) =>
    String(text).replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch]);

  const cart = {
    items: [],
    get count() {
      return this.items.reduce((sum, item) => sum + item.qty, 0);
    },
    get subtotal() {
      return this.items.reduce((sum, item) => sum + item.unitPrice * item.qty, 0);
    },
  };
  let openCart = () => {};
  let renderCart = () => {};

  function addToCart(item) {
    const key = `${item.sku}-${item.packSize}-${item.subscription ? "sub" : "once"}`;
    const existing = cart.items.find((entry) => entry.key === key);
    if (existing) existing.qty += 1;
    else cart.items.push({ ...item, key, qty: 1 });
    renderCart(true);
  }

  function initProducts() {
    const packOf = (card) => card.dataset.pack || "4-pack";
    const priceOf = (card) => Number(packOf(card) === "4-pack" ? card.dataset.four : card.dataset.twelve);
    const describe = (card) => ({
      sku: card.dataset.product,
      number: card.dataset.number,
      name: card.dataset.name,
      flavor: card.dataset.flavor,
      accent: card.dataset.accent,
      packSize: packOf(card),
    });

    // Delegated so the cloned card inside the mobile product sheet works too.
    document.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      const card = button.closest("[data-product]");
      if (!card) return;

      if (button.hasAttribute("data-pack") && button.dataset.pack) {
        card.dataset.pack = button.dataset.pack;
        $$("button[data-pack]", card).forEach((option) => {
          const on = option === button;
          option.style.backgroundColor = on ? "var(--color-ink)" : "transparent";
          option.style.color = on ? "var(--color-bone)" : "var(--color-ink)";
        });
        $("[data-price]", card).textContent = `$${priceOf(card)}`;
      } else if (button.hasAttribute("data-add")) {
        addToCart({ ...describe(card), unitPrice: priceOf(card), subscription: false });
        openCart();
        button.classList.add("is-added");
        button.setAttribute("aria-label", "Added to cart");
        button.innerHTML =
          '<span class="inline-flex items-center justify-center" style="gap:10px"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 7 L5.5 10.5 L12 3.5"></path></svg>ADDED</span>';
        window.clearTimeout(button._addedTimer);
        button._addedTimer = window.setTimeout(() => {
          button.classList.remove("is-added");
          button.setAttribute("aria-label", "Add to cart");
          button.textContent = "ADD TO CART";
        }, 1500);
      } else if (button.hasAttribute("data-subscribe")) {
        addToCart({ ...describe(card), unitPrice: Number((0.85 * priceOf(card)).toFixed(2)), subscription: true });
        openCart();
      }
    });

    // Small screens: tapping a can opens that product as a full-screen sheet.
    const modal = $("[data-product-modal]");
    if (!modal) return;
    const body = $("[data-product-modal-body]", modal);
    body.setAttribute("data-lenis-prevent", "");
    const close = () => {
      if (modal.hidden) return;
      modal.hidden = true;
      body.innerHTML = "";
      unlockScroll("product");
    };
    $$("[data-product-view]").forEach((button) => {
      button.addEventListener("click", () => {
        const source = $(`[data-product="${button.dataset.productView}"]`);
        if (!source) return;
        const card = source.cloneNode(true);
        card.classList.remove("h-full");
        const media = $("[data-product-media]", card);
        media.style.aspectRatio = "auto";
        media.style.height = "min(36vh, 280px)";
        const spacer = $("[data-product-spacer]", card);
        spacer.className = "h-5";
        spacer.removeAttribute("style");
        body.replaceChildren(card);
        modal.setAttribute("aria-label", `${card.dataset.number} ${card.dataset.name}`);
        modal.hidden = false;
        lockScroll("product");
      });
    });
    $("[data-product-modal-close]", modal).addEventListener("click", close);
  }

  async function sendNotify(email, source) {
    if (!CONFIG.notifyEndpoint) {
      await new Promise((resolve) => window.setTimeout(resolve, 400));
      return;
    }
    const response = await fetch(CONFIG.notifyEndpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, source }),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => null);
      throw new Error((data && data.error) || "Could not send. Try again.");
    }
  }

  function initCart() {
    const drawer = $("[data-cart]");
    if (!drawer) return;
    const backdrop = $("[data-cart-backdrop]");
    const countLabel = $("[data-cart-count]", drawer);
    const emptyState = $("[data-cart-empty]", drawer);
    const filled = $$("[data-cart-filled]", drawer);
    const list = $("[data-cart-items]", drawer);
    const shippingText = $("[data-cart-shipping]", drawer);
    const shippingBar = $("[data-cart-shipping-bar]", drawer);
    const subtotal = $("[data-cart-subtotal]", drawer);
    const navButton = $("[data-cart-open]");
    const checkout = $("[data-checkout]");
    const checkoutPanel = $("[data-checkout-panel]");
    let cartOpen = false;
    let checkoutOpen = false;
    list.setAttribute("data-lenis-prevent", "");

    const setCart = (open) => {
      if (open === cartOpen) return;
      cartOpen = open;
      drawer.style.transform = open ? "translateX(0)" : "translateX(100%)";
      drawer.setAttribute("aria-hidden", String(!open));
      backdrop.style.opacity = open ? "1" : "0";
      backdrop.style.pointerEvents = open ? "auto" : "none";
      backdrop.setAttribute("aria-hidden", String(!open));
      if (open) lockScroll("cart");
      else unlockScroll("cart");
    };
    const setCheckout = (open) => {
      if (open === checkoutOpen) return;
      checkoutOpen = open;
      checkout.style.opacity = open ? "1" : "0";
      checkout.style.pointerEvents = open ? "auto" : "none";
      checkout.setAttribute("aria-hidden", String(!open));
      checkoutPanel.style.transform = open ? "translateY(0)" : "translateY(12px)";
      if (open) lockScroll("checkout");
      else unlockScroll("checkout");
    };
    openCart = () => setCart(true);

    renderCart = (added) => {
      const count = cart.count;
      countLabel.textContent = String(count);
      emptyState.hidden = cart.items.length > 0;
      filled.forEach((el) => {
        el.hidden = cart.items.length === 0;
      });

      const remaining = Math.max(0, FREE_SHIPPING_THRESHOLD - cart.subtotal);
      shippingText.textContent =
        remaining <= 0 ? "You have free shipping within New Zealand." : `You are $${formatPrice(remaining)} from free NZ shipping.`;
      shippingBar.style.transform = `scaleX(${Math.min(1, cart.subtotal / FREE_SHIPPING_THRESHOLD)})`;
      subtotal.textContent = `$${cart.subtotal.toFixed(2)} NZD`;

      list.innerHTML = cart.items
        .map(
          (item) => `<li class="flex gap-4 py-5 border-b border-ink/10" data-key="${escapeHtml(item.key)}">
            <div class="relative shrink-0 overflow-hidden" style="width:56px;height:70px;background-color:rgba(26,27,29,0.03);border:1px solid rgba(26,27,29,0.1)">
              <div class="absolute inset-0" style="background:radial-gradient(60% 50% at 50% 45%, ${escapeHtml(item.accent)} 0%, transparent 70%);opacity:0.9"></div>
              <img src="images/cans/still-${escapeHtml(item.sku)}.png" alt="" class="absolute inset-0 h-full w-full object-contain" style="transform:scale(1.16)" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-baseline justify-between gap-3">
                <p class="font-display text-ink truncate" style="font-size:16px;font-weight:300"><span class="font-wordmark" style="font-weight:900">${escapeHtml(item.number)}</span> ${escapeHtml(item.name)}</p>
                <button type="button" data-cart-remove class="shrink-0 text-mist hover:text-ink transition-colors" style="font-size:12px" aria-label="Remove ${escapeHtml(item.number)} ${escapeHtml(item.name)}">Remove</button>
              </div>
              <p class="mt-0.5 font-sans uppercase text-mist" style="font-size:10px;letter-spacing:0.18em">${escapeHtml(item.packSize)} · ${item.subscription ? "Subscription" : "One-time"}</p>
              <div class="mt-3 flex items-center justify-between">
                <div class="inline-flex items-center" style="border:1px solid rgba(26,27,29,0.2);border-radius:18px">
                  <button type="button" data-cart-step="-1" class="flex items-center justify-center text-ink hover:text-mist transition-colors" style="width:32px;height:30px" aria-label="Decrease quantity">−</button>
                  <span class="font-sans tabular-nums text-ink text-center" style="width:24px;font-size:13px">${item.qty}</span>
                  <button type="button" data-cart-step="1" class="flex items-center justify-center text-ink hover:text-mist transition-colors" style="width:32px;height:30px" aria-label="Increase quantity">+</button>
                </div>
                <p class="font-sans tabular-nums text-ink" style="font-size:14px">$${formatPrice(Number((item.unitPrice * item.qty).toFixed(2)))} NZD</p>
              </div>
            </div>
          </li>`,
        )
        .join("");

      // Count badge on the nav bag icon.
      if (navButton) {
        navButton.setAttribute("aria-label", `Open cart, ${count} ${count === 1 ? "item" : "items"}`);
        let badge = $("[data-cart-badge]", navButton);
        if (count > 0 && !badge) {
          badge = document.createElement("span");
          badge.setAttribute("data-cart-badge", "");
          badge.className = "absolute font-sans tabular-nums flex items-center justify-center text-bone";
          badge.style.cssText =
            "top:-3px;right:-4px;min-width:16px;height:16px;padding:0 4px;border-radius:8px;background-color:var(--color-ink);font-size:10px;font-weight:500;line-height:1";
          navButton.appendChild(badge);
        }
        if (badge) {
          if (count === 0) badge.remove();
          else {
            badge.textContent = String(count);
            if (added) gsap.fromTo(badge, { scale: 1.4 }, { scale: 1, duration: 0.35, ease: "power2.out" });
          }
        }
      }
    };

    list.addEventListener("click", (event) => {
      const row = event.target.closest("[data-key]");
      if (!row) return;
      const item = cart.items.find((entry) => entry.key === row.dataset.key);
      if (!item) return;
      const step = event.target.closest("[data-cart-step]");
      if (event.target.closest("[data-cart-remove]")) item.qty = 0;
      else if (step) item.qty += Number(step.dataset.cartStep);
      else return;
      cart.items = cart.items.filter((entry) => entry.qty > 0);
      renderCart(false);
    });

    if (navButton) navButton.addEventListener("click", openCart);
    backdrop.addEventListener("click", () => setCart(false));
    $$("[data-cart-close]").forEach((button) => button.addEventListener("click", () => setCart(false)));
    $("[data-checkout-open]", drawer).addEventListener("click", () => setCheckout(true));
    checkout.addEventListener("click", () => setCheckout(false));
    checkoutPanel.addEventListener("click", (event) => event.stopPropagation());
    $("[data-checkout-close]").addEventListener("click", () => setCheckout(false));
    $("[data-checkout-stockist]").addEventListener("click", () => {
      setCheckout(false);
      setCart(false);
      if ($("#stockists")) scrollToTarget("#stockists");
      else window.location.href = "index.html#stockists";
    });
    window.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      if (checkoutOpen) setCheckout(false);
      else if (cartOpen) setCart(false);
    });

    // "Notify me" form inside the checkout dialog.
    const form = $("[data-notify-form]", checkoutPanel);
    const submit = $('button[type="submit"]', form);
    const error = $("[data-notify-error]", checkoutPanel);
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = $("input", form).value.trim();
      if (!email || submit.disabled) return;
      submit.disabled = true;
      submit.textContent = "Sending";
      error.hidden = true;
      try {
        await sendNotify(email, form.dataset.source);
        form.hidden = true;
        $("[data-checkout-copy]", checkoutPanel).hidden = true;
        $("[data-checkout-done]", checkoutPanel).hidden = false;
      } catch (err) {
        error.textContent = err instanceof Error ? err.message : "Something went wrong.";
        error.hidden = false;
      } finally {
        submit.disabled = false;
        submit.textContent = "Notify me";
      }
    });

    renderCart(false);
  }

  function initNewsletter() {
    const form = $("footer [data-notify-form]");
    if (!form) return;
    const input = $("input", form);
    const submit = $('button[type="submit"]', form);
    const status = $("[data-notify-status]");
    let state = "idle";
    input.addEventListener("input", () => {
      if (state !== "idle") state = "idle";
    });
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (state === "sending") return;
      state = "sending";
      status.textContent = "";
      submit.disabled = true;
      submit.textContent = "Sending";
      try {
        await sendNotify(input.value, form.dataset.source);
        state = "done";
        status.textContent = "You're on the list.";
        input.value = "";
      } catch (err) {
        state = "error";
        status.textContent = "Could not send. Try again.";
      } finally {
        submit.disabled = false;
        submit.textContent = "Sign up";
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* Boot                                                                */
  /* ------------------------------------------------------------------ */

  function boot() {
    const isHome = document.body.dataset.page === "index";

    initSmoothScroll();
    initNav();
    initCursor();
    initCart();
    initProducts();
    initNewsletter();
    initBlooms();

    if (!isHome) return;

    // Sections are set up top to bottom so each pinned block is measured
    // after the ones above it.
    const startHero = isMobile ? initHeroMobile() : initHeroDesktop();
    initScrollHint();
    initReveals($("#hero"));

    if (isMobile) initFlavorsMobile();
    else initFlavorsDesktop();
    initReveals($("#flavors"));

    initInside();
    initStory();
    initReveals($("#story"));
    initPress();
    initReveals($("#press"));
    initShop();
    initReveals($("#shop"));
    initReveals($("footer"));

    ScrollTrigger.sort();
    ScrollTrigger.refresh();
    window.addEventListener("load", () => ScrollTrigger.refresh());

    initLoader(() => {
      startHero();
      ScrollTrigger.refresh();
      // Arriving from another page with a section in the URL.
      const hash = window.location.hash;
      if (hash && hash !== "#top" && $(hash)) window.setTimeout(() => scrollToTarget(hash), 900);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
