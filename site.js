/* Loveiko Labs — site behaviour. No dependencies. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* scroll reveal + staggered groups */
  var els = [].slice.call(document.querySelectorAll('.ll-reveal, .ll-stagger'));
  if (!('IntersectionObserver' in window) || reduce) {
    els.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e) { io.observe(e); });
  }

  /* mobile nav */
  var nav = document.querySelector('.ll-nav');
  var toggle = document.querySelector('.ll-nav__toggle');
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('.ll-nav__menu a')) {
        nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); document.body.style.overflow = '';
      }
    });
  }

  /* categories dropdown: hover-intent on desktop, click/tap everywhere, Esc and outside click close */
  var desk = window.matchMedia ? matchMedia('(min-width: 801px)') : { matches: true };
  var canHover = window.matchMedia && matchMedia('(hover: hover)').matches;
  [].slice.call(document.querySelectorAll('.ll-drop')).forEach(function (d) {
    var btn = d.querySelector('.ll-drop__btn'), timer = 0, viaHover = false;
    function set(open) {
      d.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (!open) viaHover = false;
    }
    btn.addEventListener('click', function () {
      if (d.classList.contains('is-open') && viaHover) { viaHover = false; return; }
      set(!d.classList.contains('is-open'));
    });
    if (canHover) {
      d.addEventListener('mouseenter', function () {
        if (!desk.matches) return;
        clearTimeout(timer);
        if (!d.classList.contains('is-open')) { viaHover = true; set(true); }
      });
      d.addEventListener('mouseleave', function () {
        if (!desk.matches) return;
        timer = setTimeout(function () { set(false); }, 160);
      });
    }
    document.addEventListener('click', function (e) { if (!d.contains(e.target)) set(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.classList.contains('is-open')) { set(false); btn.focus(); } });
    d.addEventListener('focusout', function (e) { if (desk.matches && !d.contains(e.relatedTarget)) set(false); });
  });

  /* jump-nav scroll-spy */
  var links = [].slice.call(document.querySelectorAll('.ll-jump a'));
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (l) { var id = l.getAttribute('href').slice(1); if (id) map[id] = l; });
    var spy = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove('is-active'); });
        var a = map[en.target.id];
        if (a) { a.classList.add('is-active'); a.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduce ? 'auto' : 'smooth' }); }
      });
    }, { rootMargin: '-140px 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) spy.observe(s); });
  }

  /* app filter chips */
  var chips = [].slice.call(document.querySelectorAll('.ll-chip[data-filter]'));
  if (chips.length) {
    var cards = [].slice.call(document.querySelectorAll('.ll-apps [data-hub]'));
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        var f = c.getAttribute('data-filter');
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        cards.forEach(function (card) {
          card.classList.toggle('is-hidden', f !== 'all' && card.getAttribute('data-hub') !== f);
        });
      });
    });
  }

  /* hero poster carousel */
  var stage = document.querySelector('.ll-stage');
  if (stage) {
    var posters = [].slice.call(stage.querySelectorAll('.ll-poster'));
    var dotsWrap = stage.querySelector('.ll-stage__dots');
    var n = posters.length, cur = 0, timer = null;
    var dots = posters.map(function (p, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Show ' + (p.getAttribute('data-name') || 'app ' + (i + 1)));
      b.addEventListener('click', function () { go(i); restart(); });
      dotsWrap && dotsWrap.appendChild(b);
      return b;
    });
    function layout() {
      posters.forEach(function (p, i) {
        var d = (i - cur + n) % n; if (d > n / 2) d -= n;
        p.setAttribute('data-pos', Math.abs(d) <= 2 ? String(d) : 'hide');
        p.classList.toggle('is-front', d === 0);
        p.setAttribute('aria-hidden', d === 0 ? 'false' : 'true');
      });
      dots.forEach(function (b, i) { b.setAttribute('aria-current', i === cur ? 'true' : 'false'); });
    }
    function go(i) { cur = (i + n) % n; layout(); }
    function restart() {
      clearInterval(timer);
      if (!reduce) timer = setInterval(function () { if (!document.hidden) go(cur + 1); }, 3400);
    }
    posters.forEach(function (p, i) {
      p.addEventListener('click', function () { if (i !== cur) { go(i); restart(); } });
    });
    stage.addEventListener('mouseenter', function () { clearInterval(timer); });
    stage.addEventListener('mouseleave', restart);
    layout(); restart();

    /* pointer parallax on the floating icons */
    var orbit = [].slice.call(stage.querySelectorAll('.ll-orbit img'));
    if (!reduce && orbit.length && matchMedia('(pointer:fine)').matches) {
      var raf = 0, tx = 0, ty = 0;
      window.addEventListener('pointermove', function (e) {
        tx = (e.clientX / innerWidth - 0.5); ty = (e.clientY / innerHeight - 0.5);
        if (!raf) raf = requestAnimationFrame(function () {
          raf = 0;
          orbit.forEach(function (img, i) {
            var depth = 10 + (i % 3) * 9;
            img.style.translate = (tx * depth * -1).toFixed(1) + 'px ' + (ty * depth * -1).toFixed(1) + 'px';
          });
        });
      }, { passive: true });
    }
  }
})();
