/* Portfolio effects — written from scratch for Md. Anisur Rahman's site.
   - Loader timecode, then the ID card drops in on its rope.
   - ID card: Verlet rope, 12 segments. Gravity 0.55, damping 0.982,
     max speed 16 px/frame. Constraint pulls only when stretched.
   - Mask reveal: a lens follows the cursor over the About photo,
     showing the masked version (Spider-Man by default) underneath.
   - Cursor follower ring + halo. Nav hides on scroll down, with a
     scroll-progress line. Copy-email button. */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var isTouch = window.matchMedia("(hover: none)").matches;

  /* ---------- Loader + timecode ---------- */
  var loader = document.querySelector(".loader");
  var tcSpan = document.querySelector(".loader .tc span");
  var frames = 0, loaderDone = false;
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function tickTC() {
    if (loaderDone) return;
    frames++;
    var f = frames % 24, s = Math.floor(frames / 24) % 60,
        m = Math.floor(frames / 1440) % 60, h = Math.floor(frames / 86400);
    if (tcSpan) tcSpan.textContent = pad(h) + ":" + pad(m) + ":" + pad(s) + ":" + pad(f);
  }
  var tcTimer = setInterval(tickTC, 1000 / 24);
  setTimeout(function () {
    loaderDone = true; clearInterval(tcTimer);
    if (loader) loader.classList.add("done");
    startCard();
  }, 750);

  /* ---------- ID card rope (Verlet, 12 segments) ---------- */
  var wrap = document.querySelector(".idwrap");
  var card = document.querySelector(".idcard");
  var strapPath = document.querySelector(".idstrap path");
  var SEG = 12, GRAV = 0.55, DAMP = 0.982, MAXV = 16;
  var pts = [], segLen = 0, ropeLen = 0, anchor = { x: 0, y: 0 };
  var raf = null, dragging = false;

  function cardRest() {
    if (!wrap || !card) return;
    var r = wrap.getBoundingClientRect();
    anchor.x = r.width / 2; anchor.y = -8;
    ropeLen = 130; segLen = ropeLen / SEG;
    pts = [];
    for (var i = 0; i <= SEG; i++) {
      pts.push({ x: anchor.x, y: anchor.y + segLen * i, px: anchor.x, py: anchor.y + segLen * i });
    }
    drawCard();
  }
  function drawCard() {
    if (!pts.length || !card) return;
    var last = pts[SEG], prev = pts[SEG - 1];
    var ang = Math.atan2(last.y - prev.y, last.x - prev.x) - Math.PI / 2;
    var w = card.offsetWidth;
    card.style.transform = "translate(" + (last.x - w / 2).toFixed(1) + "px," + last.y.toFixed(1) + "px) rotate(" + ang.toFixed(3) + "rad)";
    if (strapPath) {
      var d = "M " + pts[0].x.toFixed(1) + " " + pts[0].y.toFixed(1);
      for (var i = 1; i <= SEG; i++) d += " L " + pts[i].x.toFixed(1) + " " + pts[i].y.toFixed(1);
      strapPath.setAttribute("d", d);
    }
  }
  function step() {
    var i, j, p, vx, vy, sp;
    for (i = 1; i <= SEG; i++) {
      if (dragging && i === SEG) continue;
      p = pts[i];
      vx = (p.x - p.px) * DAMP; vy = (p.y - p.py) * DAMP;
      sp = Math.hypot(vx, vy);
      if (sp > MAXV) { vx *= MAXV / sp; vy *= MAXV / sp; }
      p.px = p.x; p.py = p.y;
      p.x += vx; p.y += vy + GRAV;
    }
    for (var k = 0; k < 2; k++) {
      pts[0].x = anchor.x; pts[0].y = anchor.y;
      for (j = 0; j < SEG; j++) {
        var a = pts[j], b = pts[j + 1];
        var dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy);
        if (d > segLen) {
          var diff = (d - segLen) / d;
          if (j === 0) { b.x -= dx * diff; b.y -= dy * diff; }
          else { a.x += dx * diff * 0.5; a.y += dy * diff * 0.5; b.x -= dx * diff * 0.5; b.y -= dy * diff * 0.5; }
        }
      }
    }
    drawCard();
    var moving = false;
    for (var m = 1; m <= SEG; m++) {
      if (Math.abs(pts[m].x - pts[m].px) > 0.05 || Math.abs(pts[m].y - pts[m].py) > 0.05) { moving = true; break; }
    }
    if (moving || dragging) { raf = requestAnimationFrame(step); } else { raf = null; }
  }
  function startCard() {
    if (!card) return;
    if (reduceMotion) { cardRest(); return; }
    cardRest();
    var drop = ropeLen + card.offsetHeight + 60;
    for (var i = 0; i <= SEG; i++) { pts[i].y -= drop; pts[i].py -= drop; }
    pts[SEG].x += 30; pts[SEG].px += 30;
    if (!raf) raf = requestAnimationFrame(step);
  }
  function moveDrag(e) {
    if (!wrap || !pts.length) return;
    var r = wrap.getBoundingClientRect();
    var x = e.clientX - r.left, y = e.clientY - r.top;
    var last = pts[SEG];
    last.px = last.x; last.py = last.y;
    last.x = x; last.y = y;
  }
  function endDrag() {
    if (!dragging) return;
    dragging = false;
    var last = pts[SEG];
    var vx = last.x - last.px, vy = last.y - last.py;
    var sp = Math.hypot(vx, vy);
    if (sp > 10) { last.px = last.x - vx * 10 / sp; last.py = last.y - vy * 10 / sp; }
  }
  if (card) {
    cardRest();
    if (!reduceMotion) {
      card.addEventListener("pointerdown", function (e) {
        dragging = true;
        try { card.setPointerCapture(e.pointerId); } catch (err) {}
        moveDrag(e);
        if (!raf) raf = requestAnimationFrame(step);
        e.preventDefault();
      });
      card.addEventListener("pointermove", function (e) { if (dragging) moveDrag(e); });
      card.addEventListener("pointerup", endDrag);
      card.addEventListener("pointercancel", endDrag);
    }
  }
  window.addEventListener("resize", function () { if (!raf) cardRest(); });

  /* ---------- Cursor follower ---------- */
  var dot = document.querySelector(".cur-dot");
  var ring = document.querySelector(".cur-ring");
  var halo = document.querySelector(".cur-halo");
  var mx = window.innerWidth / 2, my = window.innerHeight / 2, rx = mx, ry = my, hx = mx, hy = my;
  if (!isTouch && !reduceMotion && dot && ring && halo) {
    document.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.left = mx + "px"; dot.style.top = my + "px";
    });
    (function loop() {
      rx += (mx - rx) * 0.12; ry += (my - ry) * 0.12;
      hx += (mx - hx) * 0.08; hy += (my - hy) * 0.08;
      ring.style.left = rx + "px"; ring.style.top = ry + "px";
      halo.style.left = hx + "px"; halo.style.top = hy + "px";
      requestAnimationFrame(loop);
    })();
    document.querySelectorAll("a, button, .idcard, .reveal, .goo").forEach(function (el) {
      el.addEventListener("mouseenter", function () { ring.classList.add("big"); });
      el.addEventListener("mouseleave", function () { ring.classList.remove("big"); });
    });
  }

  /* ---------- Mask reveal ---------- */
  var rev = document.querySelector(".reveal");
  if (rev) {
    var top = rev.querySelector(".top");
    var lens = rev.querySelector(".lens-ring");
    var tx = 50, ty = 40, tr = 0, cx = 50, cy = 40, cr = 0, lensRaf = null;
    function setLens() {
      cx += (tx - cx) * 0.18; cy += (ty - cy) * 0.18; cr += (tr - cr) * 0.18;
      if (top) {
        var px = cr / 100 * rev.offsetWidth;
        top.style.setProperty("--mx", cx.toFixed(1) + "%");
        top.style.setProperty("--my", cy.toFixed(1) + "%");
        top.style.setProperty("--r", px.toFixed(1) + "px");
      }
      if (lens) {
        var d = cr * 2 / 100 * rev.offsetWidth;
        lens.style.width = d.toFixed(1) + "px";
        lens.style.height = d.toFixed(1) + "px";
        lens.style.left = cx.toFixed(1) + "%";
        lens.style.top = cy.toFixed(1) + "%";
        lens.style.opacity = cr > 1 ? "1" : "0";
      }
      if (Math.abs(tx - cx) > 0.1 || Math.abs(ty - cy) > 0.1 || Math.abs(tr - cr) > 0.1) {
        lensRaf = requestAnimationFrame(setLens);
      } else { lensRaf = null; }
    }
    function kick() { if (!lensRaf) lensRaf = requestAnimationFrame(setLens); }
    rev.addEventListener("pointermove", function (e) {
      var r = rev.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width * 100;
      ty = (e.clientY - r.top) / r.height * 100;
      tr = e.buttons ? 32 : 20;
      kick();
    });
    rev.addEventListener("pointerdown", function () { tr = 32; kick(); });
    rev.addEventListener("pointerup", function () { tr = 20; kick(); });
    rev.addEventListener("pointerleave", function () { tr = 0; kick(); });
    rev.addEventListener("mouseenter", function () { document.body.classList.add("no-cur"); });
    rev.addEventListener("mouseleave", function () { document.body.classList.remove("no-cur"); });
  }

  /* ---------- Nav hide + progress ---------- */
  var nav = document.querySelector(".navpill");
  var prog = document.querySelector(".progress");
  var lastY = 0;
  window.addEventListener("scroll", function () {
    var y = window.scrollY || window.pageYOffset;
    if (prog) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.width = (h > 0 ? y / h * 100 : 0) + "%";
    }
    if (nav) {
      if (y > 140 && y > lastY) nav.classList.add("hidden");
      else nav.classList.remove("hidden");
    }
    lastY = y;
  }, { passive: true });

  /* ---------- Copy email ---------- */
  var copyBtn = document.querySelector(".copybtn");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var em = copyBtn.getAttribute("data-email") || "anisuranik6@gmail.com";
      function done() {
        copyBtn.textContent = "Copied ✓";
        setTimeout(function () { copyBtn.textContent = "Copy"; }, 1500);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(em).then(done, done);
      } else { done(); }
    });
  }
})();
