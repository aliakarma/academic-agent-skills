/* Interactions for the ASD-STE100 visual explainer. No dependencies, works from file://.
   Every feature checks that its markup exists, so unused components can be deleted from index.html. */
(() => {
  "use strict";
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) { /* private mode: keep the session value only */ } },
  };
  const announcer = Object.assign(document.createElement("div"), { className: "sr-only" });
  announcer.setAttribute("aria-live", "polite");
  document.body.append(announcer);
  const announce = (text) => { announcer.textContent = ""; setTimeout(() => (announcer.textContent = text), 50); };

  /* Theme: the inline script in <head> sets data-theme before the first paint. */
  const root = document.documentElement;
  const themeBtn = $(".theme-toggle");
  if (!root.dataset.theme) root.dataset.theme = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  const syncTheme = () => themeBtn && themeBtn.setAttribute("aria-pressed", String(root.dataset.theme === "dark"));
  syncTheme();
  themeBtn?.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store.set("ste-theme", root.dataset.theme);
    syncTheme();
  });

  /* Table of contents: built from the h2 of each section, so it always agrees with the page. */
  const sections = $$("main > section[id]");
  const tocList = $(".toc ol");
  if (tocList && !tocList.children.length) {
    sections.forEach((sec) => {
      const h = $("h2", sec);
      if (!h) return;
      const a = Object.assign(document.createElement("a"), { href: `#${sec.id}`, textContent: h.textContent.trim() });
      const li = document.createElement("li");
      li.append(a);
      tocList.append(li);
    });
  }
  const tocLinks = new Map($$(".toc a").map((a) => [decodeURIComponent(a.hash.slice(1)), a]));
  if ("IntersectionObserver" in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.filter((e) => e.isIntersecting).forEach((e) => {
        tocLinks.forEach((a) => a.removeAttribute("aria-current"));
        tocLinks.get(e.target.id)?.setAttribute("aria-current", "true");
      });
    }, { rootMargin: "0px 0px -70% 0px" });
    sections.forEach((s) => spy.observe(s));
  }
  const tocDetails = $(".toc details");
  const wide = matchMedia("(min-width: 980px)");
  const syncToc = () => { if (tocDetails) tocDetails.open = wide.matches; };
  syncToc();
  wide.addEventListener?.("change", syncToc);
  tocLinks.forEach((a) => a.addEventListener("click", () => { if (!wide.matches && tocDetails) tocDetails.open = false; }));

  /* Reading progress and the go-to-top control */
  const bar = $(".progress span");
  const toTop = $(".to-top");
  const onScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
    if (toTop) toTop.hidden = scrollY < 600;
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Technical explanations: open or close all of them with one control */
  const levelsBtn = $(".levels-toggle");
  if (levelsBtn && !$("details.technical")) levelsBtn.hidden = true;
  levelsBtn?.addEventListener("click", () => {
    const open = levelsBtn.getAttribute("aria-pressed") !== "true";
    $$("details.technical").forEach((d) => (d.open = open));
    levelsBtn.setAttribute("aria-pressed", String(open));
    levelsBtn.textContent = open ? "Close all technical explanations" : "Show all technical explanations";
  });
  addEventListener("beforeprint", () => $$("details").forEach((d) => (d.open = true)));

  /* Copy buttons for code listings */
  $$("pre > code").forEach((code) => {
    const pre = code.parentElement;
    const wrap = Object.assign(document.createElement("div"), { className: "code-wrap" });
    pre.before(wrap);
    wrap.append(pre);
    const btn = Object.assign(document.createElement("button"), { type: "button", className: "copy", textContent: "Copy" });
    btn.setAttribute("aria-label", "Copy the code");
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(code.innerText);
      } catch (e) {
        const range = document.createRange();
        range.selectNodeContents(code);
        const sel = getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        document.execCommand("copy");
        sel.removeAllRanges();
      }
      btn.textContent = "Copied";
      announce("The code is copied.");
      setTimeout(() => (btn.textContent = "Copy"), 1600);
    });
    wrap.append(btn);
  });

  /* Interactive diagrams: select a node to show its text in the panel.
     Without JavaScript all node texts stay visible as a list. */
  $$("figure.diagram").forEach((fig) => {
    const nodes = $$("[data-node]", fig);
    const infos = $$("[data-node-info]", fig);
    const hint = $(".node-hint", fig);
    if (!nodes.length || !infos.length) return;
    infos.forEach((i) => (i.hidden = true));
    const select = (id) => {
      nodes.forEach((n) => n.setAttribute("aria-pressed", String(n.dataset.node === id)));
      infos.forEach((i) => (i.hidden = i.dataset.nodeInfo !== id));
      if (hint) hint.hidden = true;
    };
    nodes.forEach((n) => {
      n.setAttribute("tabindex", "0");
      n.setAttribute("role", "button");
      n.setAttribute("aria-pressed", "false");
      n.addEventListener("click", () => select(n.dataset.node));
      n.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(n.dataset.node); }
      });
    });
  });

  /* Value bars: the table keeps the exact source numbers. The bar length is
     (value - data-bar-min) / (data-bar-max - data-bar-min). */
  $$("table[data-bar-max]").forEach((t) => {
    const max = parseFloat(t.dataset.barMax);
    const min = parseFloat(t.dataset.barMin || "0");
    $$("td.bar", t).forEach((td) => {
      const m = td.textContent.match(/-?\d+(?:\.\d+)?/);
      if (m && max > min) td.style.setProperty("--bar", Math.max(0, Math.min(1, (parseFloat(m[0]) - min) / (max - min))));
    });
  });

  /* Glossary filter */
  const filter = $("#glossary-filter");
  const terms = $$("dl.glossary .term");
  const empty = $(".glossary-empty");
  filter?.addEventListener("input", () => {
    const q = filter.value.trim().toLowerCase();
    let shown = 0;
    terms.forEach((t) => {
      const hit = !q || t.textContent.toLowerCase().includes(q);
      t.hidden = !hit;
      shown += hit;
    });
    if (empty) empty.hidden = shown > 0;
  });

  /* Term tooltips: a link to a glossary entry shows the first paragraph of its definition.
     The tooltip opens on hover and focus, stays open while the pointer is on it, and Escape closes it. */
  const tip = Object.assign(document.createElement("div"), { className: "tooltip", id: "term-tooltip", hidden: true });
  tip.setAttribute("role", "tooltip");
  document.body.append(tip);
  let current = null;
  let hideTimer = 0;
  const hideTip = () => {
    tip.hidden = true;
    current?.removeAttribute("aria-describedby");
    current = null;
  };
  const showTip = (a) => {
    const entry = document.getElementById(decodeURIComponent(a.hash.slice(1)));
    const def = entry && $("dd p", entry);
    if (!def) return;
    clearTimeout(hideTimer);
    tip.textContent = def.textContent.trim();
    tip.hidden = false;
    const r = a.getBoundingClientRect();
    const w = Math.min(320, innerWidth - 32);
    tip.style.maxWidth = `${w}px`;
    tip.style.left = `${Math.max(16, Math.min(r.left, innerWidth - w - 16)) + scrollX}px`;
    tip.style.top = `${r.bottom + scrollY + 8}px`;
    a.setAttribute("aria-describedby", tip.id);
    current = a;
  };
  $$('a.term-ref[href^="#"]').forEach((a) => {
    a.addEventListener("mouseenter", () => showTip(a));
    a.addEventListener("mouseleave", () => { hideTimer = setTimeout(hideTip, 250); });
    a.addEventListener("focus", () => showTip(a));
    a.addEventListener("blur", hideTip);
  });
  tip.addEventListener("mouseenter", () => clearTimeout(hideTimer));
  tip.addEventListener("mouseleave", hideTip);
  addEventListener("keydown", (e) => { if (e.key === "Escape") hideTip(); });
})();
