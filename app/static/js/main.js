/**
 * StockIQ Frontend JavaScript
 * Autocomplete search, card animations, UI interactions
 */

(function () {
  "use strict";

  /* ── Autocomplete ─────────────────────────────────────────────────────── */

  function setupAutocomplete(inputId, dropdownId) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    if (!input || !dropdown) return;

    let debounceTimer;
    let currentResults = [];

    input.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      const q = input.value.trim();
      if (q.length < 1) {
        hideDropdown(dropdown);
        return;
      }
      debounceTimer = setTimeout(() => fetchSuggestions(q, dropdown, currentResults), 160);
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Escape") hideDropdown(dropdown);
    });

    document.addEventListener("click", (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        hideDropdown(dropdown);
      }
    });
  }

  async function fetchSuggestions(q, dropdown, cache) {
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      if (!res.ok) return;
      const data = await res.json();
      renderSuggestions(data, dropdown);
    } catch (err) {
      console.warn("Autocomplete error:", err);
    }
  }

  function renderSuggestions(results, dropdown) {
    if (!results.length) {
      hideDropdown(dropdown);
      return;
    }

    dropdown.innerHTML = results
      .map(
        (r) => `
      <div class="autocomplete-item" onclick="window.location.href='/stock/${encodeURIComponent(r.ticker)}'">
        <span class="ac-ticker">${escHtml(r.ticker)}</span>
        <span class="ac-name">${escHtml(r.name)}</span>
        <span class="ac-sector">${escHtml(r.sector || "")}</span>
      </div>`
      )
      .join("");

    dropdown.style.display = "block";
  }

  function hideDropdown(dropdown) {
    if (dropdown) dropdown.style.display = "none";
  }

  function escHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  /* ── Card Visibility Observer ─────────────────────────────────────────── */

  function setupCardObserver() {
    const cards = document.querySelectorAll(".siq-card");
    if (!cards.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 }
    );

    cards.forEach((card, i) => {
      card.style.transitionDelay = `${i * 40}ms`;
      observer.observe(card);
    });
  }

  /* ── Range Bar Animation ──────────────────────────────────────────────── */
  function animateRangeBars() {
    // Shareholding bars start at 0 and animate on load
    const fills = document.querySelectorAll(".sh-fill");
    fills.forEach((el) => {
      const w = el.style.width;
      el.style.width = "0%";
      setTimeout(() => { el.style.width = w; }, 300);
    });

    const rangeFill = document.querySelector(".range-fill");
    if (rangeFill) {
      const w = rangeFill.style.width;
      rangeFill.style.width = "0%";
      setTimeout(() => { rangeFill.style.width = w; }, 400);
    }
  }

  /* ── Q&A Chevron Update ───────────────────────────────────────────────── */
  function setupQAChevrons() {
    document.querySelectorAll(".qa-question").forEach((btn) => {
      btn.addEventListener("click", () => {
        const isExpanded = btn.getAttribute("aria-expanded") === "true";
        // Bootstrap collapse toggles aria-expanded automatically
        // We just animate the chevron via CSS on [aria-expanded="true"]
      });
    });
  }

  /* ── Stock Card Hover Glow ────────────────────────────────────────────── */
  function setupCardGlow() {
    document.querySelectorAll(".stock-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.background = `radial-gradient(circle at ${x}% ${y}%, rgba(212,168,83,0.04) 0%, white 60%)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.background = "";
      });
    });
  }

  /* ── Init ─────────────────────────────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", () => {
    setupAutocomplete("navSearchInput", "navAutocomplete");
    setupAutocomplete("heroSearchInput", "heroAutocomplete");
    setupCardObserver();
    animateRangeBars();
    setupQAChevrons();
    setupCardGlow();
  });
})();
