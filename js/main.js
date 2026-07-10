/* ==========================================================================
   LYDIA PEDERSEN — Portfolio
   Chip (bottom-right, facing upper-left)
     → dense cloud of 1s/0s (big→small, no lines)
       → 3D hex node (isometric, same plane as chip)
         → tokens emitted at constant rate, closely spaced, no lines
   ========================================================================== */

(function () {
  'use strict';

  /* ==== NAV / FADE / FILTER / ACCORDION / SMOOTH SCROLL ==== */
  var nav = document.getElementById('navbar');
  var navToggle = document.getElementById('nav-toggle');
  var navLinks = document.getElementById('nav-links');
  var allNavLinks = document.querySelectorAll('.nav__link');
  function handleScroll() {
    nav.classList.toggle('scrolled', window.scrollY > 50);
    var sections = document.querySelectorAll('section[id]'), cur = '';
    sections.forEach(function (s) { if (window.scrollY >= s.offsetTop - 100) cur = s.getAttribute('id'); });
    allNavLinks.forEach(function (l) { l.classList.remove('active'); if (l.getAttribute('href') === '#' + cur) l.classList.add('active'); });
  }
  window.addEventListener('scroll', handleScroll, { passive: true }); handleScroll();
  if (navToggle) {
    navToggle.addEventListener('click', function () { var o = navLinks.classList.toggle('open'); navToggle.setAttribute('aria-expanded', o); });
    allNavLinks.forEach(function (l) { l.addEventListener('click', function () { navLinks.classList.remove('open'); navToggle.setAttribute('aria-expanded', 'false'); }); });
  }
  var fadeObs = new IntersectionObserver(function (entries) { entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); fadeObs.unobserve(e.target); } }); }, { rootMargin: '0px 0px -60px 0px', threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(function (el) { fadeObs.observe(el); });
  document.querySelectorAll('.filter-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.filter-btn').forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
      btn.classList.add('active'); btn.setAttribute('aria-selected', 'true');
      var f = btn.getAttribute('data-filter');
      document.querySelectorAll('.sample-card').forEach(function (c) {
        if (f === 'all' || c.getAttribute('data-company') === f) { c.style.display = ''; c.classList.remove('visible'); requestAnimationFrame(function () { c.classList.add('visible'); }); }
        else { c.style.display = 'none'; }
      });
    });
  });
  document.querySelectorAll('.case-study').forEach(function (cs) {
    var h = cs.querySelector('.case-study__header');
    function toggle() { var o = cs.classList.toggle('open'); h.setAttribute('aria-expanded', o); }
    h.addEventListener('click', toggle);
    h.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
  });
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) { var id = this.getAttribute('href'); if (id === '#') return; var t = document.querySelector(id); if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); } });
  });

  /* ==================================================================
     CANVAS SETUP
     ================================================================== */

  var canvas = document.getElementById('chip-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W, H;

  function resize() {
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();
  window.addEventListener('resize', resize);

  // Colors
  var RG  = 'rgba(185, 115, 130, ';
  var RGD = 'rgba(160, 90, 110, ';
  var GD  = 'rgba(195, 165, 95, ';
  var GDD = 'rgba(160, 130, 60, ';
  var WH  = 'rgba(255, 230, 220, ';

  /* ==================================================================
     KEY POSITIONS
     Chip: bottom-right (flipped to face upper-left)
     Hex: upper-left, well out of the way
     ================================================================== */

  // Chip center (the image is at bottom:-60, right:-60, 580x580)
  function chipX() { return W - 90; }
  function chipY() { return H - 230; }

  // Hex node: upper-left corner area
  function hexX() { return W * 0.20; }
  function hexY() { return H * 0.35; }

  // Diagonal direction from chip to hex (normalized)
  var diagDx, diagDy, diagLen;
  function calcDiag() {
    var dx = hexX() - chipX();
    var dy = hexY() - chipY();
    diagLen = Math.sqrt(dx * dx + dy * dy);
    diagDx = dx / diagLen;
    diagDy = dy / diagLen;
  }
  calcDiag();
  window.addEventListener('resize', calcDiag);

  /* ==================================================================
     TOKENS — pre-split sentence into ~3-4 char chunks
     ================================================================== */

  var sentence = 'using agentic AI to transform raw code into polished developer documentation and fully automate the developer experience';
  var tokens = [];
  (function buildTokens() {
    var ws = sentence.split(' ');
    for (var i = 0; i < ws.length; i++) {
      var w = ws[i];
      // Split words > 4 chars into chunks
      while (w.length > 4) {
        tokens.push(w.slice(0, 3));
        w = w.slice(3);
      }
      if (w.length > 0) tokens.push(w);
    }
  })();

  /* ==================================================================
     DENSE BINARY CLOUD
     A swath of 1s and 0s filling a cone from chip → hex.
     Big near chip, small near hex. No visible lines.
     ================================================================== */

  var cloudParticles = [];
  var MAX_CLOUD = 120;

  function spawnCloudParticle() {
    // t=0 is at the chip, t=1 is at the hex
    // Spawn near the chip end
    var t = Math.random() * 0.15; // start near chip

    // Perpendicular spread: wide near chip, narrow near hex
    var perpDx = -diagDy; // perpendicular to diagonal
    var perpDy = diagDx;
    var spread = (1 - t) * 80 + 10; // wider near chip
    var offset = (Math.random() - 0.5) * spread;

    var baseX = chipX() + diagDx * diagLen * t;
    var baseY = chipY() + diagDy * diagLen * t;

    return {
      t: t,
      offset: offset,
      x: baseX + perpDx * offset,
      y: baseY + perpDy * offset,
      speed: 0.001 + Math.random() * 0.002,
      char: Math.random() > 0.5 ? '1' : '0',
      isGold: Math.random() > 0.5,
      alpha: 0.2 + Math.random() * 0.4
    };
  }

  function updateCloud() {
    // Spawn to maintain density
    while (cloudParticles.length < MAX_CLOUD) {
      cloudParticles.push(spawnCloudParticle());
    }

    var perpDx = -diagDy;
    var perpDy = diagDx;

    var alive = [];
    for (var i = 0; i < cloudParticles.length; i++) {
      var p = cloudParticles[i];
      p.t += p.speed;

      // Narrow the spread as t increases (cone shape)
      var spread = (1 - p.t) * 80 + 10;
      var clampedOffset = Math.max(-spread, Math.min(spread, p.offset));

      var baseX = chipX() + diagDx * diagLen * p.t;
      var baseY = chipY() + diagDy * diagLen * p.t;
      p.x = baseX + perpDx * clampedOffset;
      p.y = baseY + perpDy * clampedOffset;

      if (p.t < 1.0) alive.push(p);
    }
    cloudParticles = alive;
  }

  function drawCloud() {
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (var i = 0; i < cloudParticles.length; i++) {
      var p = cloudParticles[i];

      // Size: big near chip (t≈0), small near hex (t≈1)
      var size = Math.round(22 - p.t * 14); // 22px → 8px
      ctx.font = '700 ' + size + 'px "JetBrains Mono", monospace';

      // Fade: visible in middle, fade at edges
      var alpha = p.alpha * 0.8 * (p.t < 0.1 ? p.t / 0.1 : (p.t > 0.85 ? (1 - p.t) / 0.15 : 1));
      var color = p.isGold ? GD : RG;

      ctx.shadowColor = p.isGold ? 'rgba(195, 165, 95, 0.3)' : 'rgba(185, 115, 130, 0.3)';
      ctx.shadowBlur = 6;
      ctx.fillStyle = color + alpha + ')';
      ctx.fillText(p.char, p.x, p.y);
      ctx.shadowBlur = 0;
    }
  }

  /* ==================================================================
     3D ISOMETRIC HEXAGON NODE
     Drawn as a hexagonal prism on the same plane as the chip.
     Top face lighter, side faces darker for depth.
     ================================================================== */

  var nodePulse = 0;
  var nodeRot = 0;

  function drawHexNode() {
    var nx = hexX(), ny = hexY();
    nodePulse += 0.025;
    nodeRot += 0.0015;
    var pulse = 0.85 + Math.sin(nodePulse) * 0.15;

    // Glow (subtle, matching bits)
    var g1 = ctx.createRadialGradient(nx, ny, 0, nx, ny, 70);
    g1.addColorStop(0, 'rgba(185, 115, 130, ' + (0.07 * pulse) + ')');
    g1.addColorStop(0.4, 'rgba(195, 165, 95, ' + (0.03 * pulse) + ')');
    g1.addColorStop(1, 'rgba(185, 115, 130, 0)');
    ctx.fillStyle = g1;
    ctx.beginPath();
    ctx.arc(nx, ny, 70, 0, Math.PI * 2);
    ctx.fill();

    // Outer ring
    ctx.strokeStyle = RG + (0.15 * pulse) + ')';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(nx, ny, 50, 0, Math.PI * 2);
    ctx.stroke();

    // Main hexagon (45px)
    var HR = 55;
    ctx.save();
    ctx.translate(nx, ny);
    ctx.rotate(nodeRot);
    ctx.beginPath();
    for (var i = 0; i < 6; i++) {
      var a = (Math.PI / 3) * i - Math.PI / 6;
      var hx2 = Math.cos(a) * HR, hy2 = Math.sin(a) * HR;
      i === 0 ? ctx.moveTo(hx2, hy2) : ctx.lineTo(hx2, hy2);
    }
    ctx.closePath();
    ctx.fillStyle = RG + '0.08)';
    ctx.fill();
    ctx.shadowColor = 'rgba(185, 115, 130, 0.2)';
    ctx.shadowBlur = 6;
    ctx.strokeStyle = RGD + (0.3 * pulse) + ')';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Inner hex
    var IR = 35;
    ctx.beginPath();
    for (var i = 0; i < 6; i++) {
      var a = (Math.PI / 3) * i;
      var hx2 = Math.cos(a) * IR, hy2 = Math.sin(a) * IR;
      i === 0 ? ctx.moveTo(hx2, hy2) : ctx.lineTo(hx2, hy2);
    }
    ctx.closePath();
    ctx.strokeStyle = GD + (0.2 * pulse) + ')';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.restore();

    // Labels
    ctx.font = '700 14px "JetBrains Mono", monospace';
    ctx.fillStyle = WH + (0.45 * pulse) + ')';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.shadowColor = 'rgba(185, 115, 130, 0.2)';
    ctx.shadowBlur = 5;
    ctx.fillText('PIPELINE', nx, ny - 6);
    ctx.font = '500 10px "JetBrains Mono", monospace';
    ctx.fillStyle = GD + (0.4 * pulse) + ')';
    ctx.fillText('ORCHESTRATOR', nx, ny + 11);
    ctx.shadowBlur = 0;

    // Stage nodes
    var stages = [
      { label: 'DOC WRITER', angle: -2.4 },
      { label: 'QA ENGINE',  angle: -0.8 },
      { label: 'LINK GOV',   angle: 0.7 },
      { label: 'ANALYTICS',  angle: 2.2 }
    ];
    for (var i = 0; i < stages.length; i++) {
      var st = stages[i];
      var sa = st.angle + nodeRot * 0.4;
      var sx = nx + Math.cos(sa) * 90;
      var sy = ny + Math.sin(sa) * 90;

      ctx.strokeStyle = RG + '0.18)';
      ctx.lineWidth = 0.8;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(nx + Math.cos(sa) * HR, ny + Math.sin(sa) * HR);
      ctx.lineTo(sx, sy);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = GD + (0.1 * pulse) + ')';
      ctx.beginPath();
      ctx.arc(sx, sy, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = GD + (0.3 * pulse) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.font = '600 8px "JetBrains Mono", monospace';
      ctx.fillStyle = RG + (0.35 * pulse) + ')';
      ctx.textAlign = 'center';
      ctx.fillText(st.label, sx, sy + 16);
    }
  }

  /* ==================================================================
     TOKEN EMISSION
     Tokens emerge from hex, flow upper-left at constant rate.
     Closely spaced, no overlap, no visible path line.
     ================================================================== */

  var activeTokens = [];
  var tokenIdx = 0;
  var tokenTimer = 0;
  var TOKEN_INTERVAL = 50;  // frames between tokens (slower, more spaced)
  var TOKEN_SPEED = 0.6;    // px per frame

  // Direction: continue upper-left from hex (same diagonal as chip→hex)
  var tokDx, tokDy;
  function calcTokDir() {
    tokDx = diagDx * TOKEN_SPEED;
    tokDy = diagDy * TOKEN_SPEED;
  }
  calcTokDir();
  window.addEventListener('resize', calcTokDir);

  function updateTokens() {
    tokenTimer++;
    if (tokenTimer >= TOKEN_INTERVAL) {
      var tok = tokens[tokenIdx % tokens.length];
      activeTokens.push({
        text: tok,
        x: hexX() - 65,              // start at left side of hex
        y: hexY(),
        alpha: 0,
        age: 0
      });
      tokenIdx++;
      tokenTimer = 0;
    }

    var alive = [];
    for (var i = 0; i < activeTokens.length; i++) {
      var t = activeTokens[i];
      t.age++;
      // Continue along the diagonal (upper-left)
      t.x += tokDx;
      t.y += tokDy;

      // Fade in quickly
      if (t.age < 15) {
        t.alpha = (t.age / 15) * 0.45;
      } else {
        var dist = Math.sqrt(
          Math.pow(t.x - hexX(), 2) + Math.pow(t.y - hexY(), 2)
        );
        t.alpha = Math.max(0, 0.45 * (1 - dist / 350));
      }

      if (t.alpha > 0.01 && t.x > -150 && t.y > -50) alive.push(t);
    }
    activeTokens = alive;
  }

  function drawTokens() {
    ctx.font = '500 17px "Outfit", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (var i = 0; i < activeTokens.length; i++) {
      var t = activeTokens[i];

      if (t.alpha > 0.25) {
        ctx.shadowColor = 'rgba(185, 115, 130, 0.15)';
        ctx.shadowBlur = 4;
      }

      ctx.fillStyle = (i % 2 === 0 ? RG : GD) + t.alpha + ')';
      ctx.fillText(t.text, t.x, t.y);
      ctx.shadowBlur = 0;
    }
  }

  /* ==================================================================
     SPARKLES
     ================================================================== */

  var sparkles = [];
  function initSparkles() {
    sparkles = [];
    for (var i = 0; i < 25; i++) {
      var t = Math.random();
      sparkles.push({
        x: W * 0.05 + t * W * 0.85 + (Math.random() - 0.5) * 100,
        y: H * 0.05 + t * H * 0.85 + (Math.random() - 0.5) * 100,
        size: 0.6 + Math.random() * 1.5,
        maxAlpha: 0.18 + Math.random() * 0.3,
        phase: Math.random() * Math.PI * 2,
        speed: 0.012 + Math.random() * 0.02,
        isGold: Math.random() > 0.45
      });
    }
  }
  initSparkles();

  function drawSparkles() {
    for (var i = 0; i < sparkles.length; i++) {
      var s = sparkles[i];
      s.phase += s.speed;
      var alpha = s.maxAlpha * Math.max(0, Math.sin(s.phase));
      if (alpha < 0.04) continue;
      var color = s.isGold ? GD : RG;
      ctx.fillStyle = color + alpha + ')';
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
      ctx.fill();
      if (alpha > 0.15) {
        ctx.strokeStyle = color + (alpha * 0.35) + ')';
        ctx.lineWidth = 0.4;
        var r = s.size * 2.5;
        ctx.beginPath();
        ctx.moveTo(s.x - r, s.y); ctx.lineTo(s.x + r, s.y);
        ctx.moveTo(s.x, s.y - r); ctx.lineTo(s.x, s.y + r);
        ctx.stroke();
      }
    }
  }

  /* ==================================================================
     ANIMATION LOOP
     ================================================================== */

  function draw() {
    ctx.clearRect(0, 0, W, H);
    drawSparkles();
    updateCloud();
    drawCloud();
    drawHexNode();
    updateTokens();
    drawTokens();
    requestAnimationFrame(draw);
  }

  draw();
})();
