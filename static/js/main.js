/* ═══════════════════════════════════════════════════════════════════════════
   GLOW & GRACE — MAIN.JS
   ───────────────────────────────────────────────────────────────────────────
   Three small enhancements:
     1. Navbar shadow on scroll
     2. Fade-in animation for [data-animate] elements
     3. Scroll-to-top button visibility

   Everything degrades gracefully if JavaScript is disabled:
     • Navbar just loses its shadow
     • Content is visible immediately (CSS-only fallback for reduced motion)
     • To-top button never appears — but users can still scroll normally
   ═══════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────────────
     1. NAVBAR — add .is-scrolled once the user has scrolled past 20px
     ───────────────────────────────────────────────────────────────────── */
  const navbar = document.querySelector('.gg-navbar');
  const toTop  = document.getElementById('toTop');

  function handleScroll() {
    const y = window.scrollY || window.pageYOffset;

    if (navbar) {
      if (y > 20) {
        navbar.classList.add('is-scrolled');
      } else {
        navbar.classList.remove('is-scrolled');
      }
    }

    if (toTop) {
      if (y > 400) {
        toTop.classList.add('is-visible');
      } else {
        toTop.classList.remove('is-visible');
      }
    }
  }

  // Use requestAnimationFrame to avoid hammering the scroll handler
  let ticking = false;
  window.addEventListener(
    'scroll',
    function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          handleScroll();
          ticking = false;
        });
        ticking = true;
      }
    },
    { passive: true }
  );

  // Run once on load in case the page opens already scrolled (refresh mid-page)
  handleScroll();


  /* ─────────────────────────────────────────────────────────────────────
     2. SCROLL-TO-TOP BUTTON
     ───────────────────────────────────────────────────────────────────── */
  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }


  /* ─────────────────────────────────────────────────────────────────────
     3. INTERSECTION OBSERVER — reveal [data-animate] elements on scroll
     ───────────────────────────────────────────────────────────────────── */
  const animatedElements = document.querySelectorAll('[data-animate]');

  if (animatedElements.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target); // animate only once
          }
        });
      },
      {
        threshold: 0.12,          // fire when 12% of element is visible
        rootMargin: '0px 0px -60px 0px', // slight offset so it feels early
      }
    );

    animatedElements.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // No IntersectionObserver support — just show everything
    animatedElements.forEach(function (el) {
      el.classList.add('is-visible');
    });
  }


  /* ─────────────────────────────────────────────────────────────────────
     4. FORM ENHANCEMENT — disable submit button while posting
        Prevents double-submits when the user clicks twice
     ───────────────────────────────────────────────────────────────────── */
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('button[type="submit"]');
      if (btn && !btn.disabled) {
        // Small delay so the browser can register the click and begin the POST
        setTimeout(function () {
          btn.disabled = true;
          btn.dataset.originalText = btn.innerHTML;
          btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Sending…';
        }, 10);
      }
    });
  });

})();