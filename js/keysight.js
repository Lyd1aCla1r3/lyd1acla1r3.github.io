/* ==========================================================================
   KEYSIGHT v2 — Shared Interactions
   IntersectionObserver reveals, animated counters, keyboard navigation.
   No external dependencies. GPU-composited animations only.
   ========================================================================== */

(function () {
  'use strict';

  /* ------------------------------------------------------------------
     IntersectionObserver — Scroll-triggered reveals
     Observes all elements with class "ks-reveal" and adds "ks-visible"
     when they enter the viewport.
     ------------------------------------------------------------------ */

  var revealObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('ks-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '0px 0px -40px 0px', threshold: 0.1 }
  );

  document.querySelectorAll('.ks-reveal').forEach(function (el) {
    revealObserver.observe(el);
  });


  /* ------------------------------------------------------------------
     Animated Counter
     Counts from 0 to a target value using requestAnimationFrame.
     Uses cubic ease-out for a fast start and smooth deceleration.

     Usage:
       <span class="ks-counter" data-target="150" data-suffix=" pages"></span>

     Options (data attributes):
       data-target   — target number (integer)
       data-suffix   — text appended after the number (e.g., " pages", "+")
       data-prefix   — text prepended before the number (e.g., "$")
       data-duration — animation duration in ms (default: 1200)
     ------------------------------------------------------------------ */

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function animateCounter(element, target, duration, prefix, suffix) {
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var elapsed = timestamp - startTime;
      var progress = Math.min(elapsed / duration, 1);
      var easedProgress = easeOutCubic(progress);
      var currentValue = Math.round(easedProgress * target);

      element.textContent = (prefix || '') + currentValue + (suffix || '');

      if (progress < 1) {
        requestAnimationFrame(step);
      }
    }

    requestAnimationFrame(step);
  }

  /* Observe counter elements and trigger animation on viewport entry */
  var counterObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var target = parseInt(el.getAttribute('data-target'), 10);
          var suffix = el.getAttribute('data-suffix') || '';
          var prefix = el.getAttribute('data-prefix') || '';
          var duration = parseInt(el.getAttribute('data-duration'), 10) || 1200;

          /* Respect prefers-reduced-motion */
          var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          if (prefersReduced) {
            el.textContent = (prefix || '') + target + (suffix || '');
          } else {
            animateCounter(el, target, duration, prefix, suffix);
          }

          counterObserver.unobserve(el);
        }
      });
    },
    { threshold: 0.3 }
  );

  document.querySelectorAll('.ks-counter').forEach(function (el) {
    counterObserver.observe(el);
  });


  /* ------------------------------------------------------------------
     Keyboard Navigation
     Escape or H — navigate to hub page
     Keys 1-6   — navigate to section pages
     ------------------------------------------------------------------ */

  var sectionPaths = {
    '1': 'convergence.html',
    '2': 'customer.html',
    '3': 'architecture.html',
    '4': 'translation.html',
    '5': 'value.html',
    '6': 'close.html'
  };

  /* ------------------------------------------------------------------
     Standards Page - Detail Overlay State Management
     ------------------------------------------------------------------ */

  var standardRows = document.querySelectorAll('.standard-row');
  var closeButtons = document.querySelectorAll('.ks-overlay-close');

  if (standardRows.length > 0) {
    standardRows.forEach(function (row) {
      row.addEventListener('click', function () {
        var targetId = row.getAttribute('data-target');
        var targetOverlay = document.getElementById(targetId);
        if (targetOverlay) {
          /* Close any currently open overlays first */
          document.querySelectorAll('.standard-detail-overlay.is-expanded').forEach(function (overlay) {
            overlay.classList.remove('is-expanded');
          });
          
          targetOverlay.classList.add('is-expanded');
          
          var closeBtn = targetOverlay.querySelector('.ks-overlay-close');
          if (closeBtn) {
            setTimeout(function () { closeBtn.focus(); }, 100);
          }
        }
      });
      
      row.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          row.click();
        }
      });
    });

    closeButtons.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var overlay = btn.closest('.standard-detail-overlay');
        if (overlay) {
          overlay.classList.remove('is-expanded');
          
          /* Find the row that opened it and focus back */
          var targetId = overlay.id;
          var openingRow = document.querySelector('.standard-row[data-target="' + targetId + '"]');
          if (openingRow) {
            openingRow.focus();
          }
        }
      });
    });
  }

  /* Determine the base path for navigation.
     If we are on the hub (keysight.html at root), child pages are in keysight/.
     If we are on a child page (inside keysight/), navigate relative to current dir. */
  function getBasePath() {
    var path = window.location.pathname;
    if (path.indexOf('/keysight/') !== -1) {
      /* We are in a child page — siblings are in the same directory */
      return '';
    }
    /* We are on the hub page — children are in keysight/ */
    return 'keysight/';
  }

  function getHubPath() {
    var path = window.location.pathname;
    if (path.indexOf('/keysight/') !== -1) {
      return '../keysight.html';
    }
    return 'keysight.html';
  }

  document.addEventListener('keydown', function (e) {
    /* Do not intercept when user is typing in an input/textarea */
    var tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    var key = e.key;

    /* Escape or H — handle overlays or return to hub */
    if (key === 'Escape' || key === 'h' || key === 'H') {
      e.preventDefault();

      var expandedOverlay = document.querySelector('.standard-detail-overlay.is-expanded');
      if (expandedOverlay) {
        expandedOverlay.classList.remove('is-expanded');
        
        /* Focus back on the row */
        var targetId = expandedOverlay.id;
        var openingRow = document.querySelector('.standard-row[data-target="' + targetId + '"]');
        if (openingRow) {
          openingRow.focus();
        }
        return;
      }

      window.location.href = getHubPath();
      return;
    }

    /* Number keys 1-6 — jump to section */
    if (sectionPaths[key]) {
      e.preventDefault();
      window.location.href = getBasePath() + sectionPaths[key];
    }
  });

})();
