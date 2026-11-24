/* Q84 redesign layer: scroll progress, scroll reveals, hero tilt and the license estimator. */
(function () {
  var root = document.documentElement;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.add('rd-js');

  // Reveal blocks as they scroll into view, staggered within each group
  var sel = ['main .section-head', 'main .fitem', 'main .card', 'main .example', 'main .quote', 'main .steps li', 'main .faq details',
    'main .who', 'main .outcomes li', 'main .checks li', 'main .rd-ops', 'main .rd-est-card', 'main .fpanel', 'main .split > .stack',
    'main .post-card', 'main .bc-shot', 'main .promo', 'main .cta-next', 'main .table-wrap', 'main .rd-why-col', 'main .rd-stat', 'main .rd-job', 'main .rd-person', 'main .rd-side', 'main .rd-n2-stat', 'main .rd-n2'].join(',');
  var els = [].slice.call(document.querySelectorAll(sel)).filter(function (e) {
    return !e.closest('.hero, .page-head, .dd-menu, [hidden]');
  });
  els.forEach(function (e) {
    var sibs = [].filter.call(e.parentElement.children, function (s) { return s.matches(sel); });
    e.style.setProperty('--d', Math.min(sibs.indexOf(e), 6) * 0.08 + 's');
    e.classList.add('rd-reveal');
  });
  if (still || !('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (e) { io.observe(e); });
    // anything already on screen (or skipped past by a jump link) shows at once
    setTimeout(function () { els.forEach(function (e) { if (e.getBoundingClientRect().top < innerHeight) e.classList.add('is-visible'); }); }, 60);
  }

  // Step line draws across when the steps scroll into view
  var jobs = document.querySelector('.rd-jobs');
  if (jobs) {
    if (still || !('IntersectionObserver' in window)) jobs.classList.add('is-visible');
    else new IntersectionObserver(function (en, o) { if (en[0].isIntersecting) { jobs.classList.add('is-visible'); o.disconnect(); } }, { threshold: 0.3 }).observe(jobs);
  }

  // Numbers count up once when they come into view
  var nums = [].slice.call(document.querySelectorAll('[data-count]'));
  if (nums.length && !still && 'IntersectionObserver' in window) {
    var run = function (el) {
      var end = +el.dataset.count, t0 = null;
      var step = function (t) {
        if (!t0) t0 = t;
        var k = Math.min(1, (t - t0) / 1400), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
        el.textContent = v.toLocaleString('en-US');
        if (k < 1) requestAnimationFrame(step);
      };
      el.textContent = '0'; requestAnimationFrame(step);
    };
    var no = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { run(e.target); no.unobserve(e.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { no.observe(n); });
  }

  // Client carousel: arrow buttons, and drag to scroll with a mouse
  var car = document.querySelector('.rd-car');
  if (car) {
    [].forEach.call(document.querySelectorAll('.rd-car-btn'), function (b) {
      b.addEventListener('click', function () { car.scrollBy({ left: +b.dataset.dir * Math.min(car.clientWidth * 0.8, 640), behavior: still ? 'auto' : 'smooth' }); });
    });
    var down = false, sx = 0, sl = 0;
    car.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = car.scrollLeft; car.style.scrollSnapType = 'none'; car.style.cursor = 'grabbing'; });
    addEventListener('pointerup', function () { if (!down) return; down = false; car.style.scrollSnapType = ''; car.style.cursor = ''; });
    car.addEventListener('pointermove', function (e) { if (down) car.scrollLeft = sl - (e.clientX - sx); });
    car.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); car.scrollBy({ left: (e.key === 'ArrowRight' ? 1 : -1) * 320, behavior: 'smooth' }); } });
  }

  // Hero card tilts toward the mouse
  var card = document.querySelector('.rd-card');
  var vis = document.querySelector('.rd-visual');
  if (card && vis && !still && window.matchMedia('(hover: hover)').matches) {
    vis.addEventListener('mousemove', function (ev) {
      var r = vis.getBoundingClientRect();
      var x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
      card.style.setProperty('--tilt-y', (x * 8).toFixed(2) + 'deg');
      card.style.setProperty('--tilt-x', (-y * 8).toFixed(2) + 'deg');
    });
    vis.addEventListener('mouseleave', function () { card.style.setProperty('--tilt-x', '0deg'); card.style.setProperty('--tilt-y', '0deg'); });
  }

  // License estimator: Microsoft list prices per full user per month, in the visitor's currency
  var est = document.querySelector('[data-rd-est]');
  if (est) {
    var LIST = { usd: { essentials: 80, premium: 110, sym: '$', code: 'USD' }, cad: { essentials: 108.5, premium: 149.2, sym: 'CA$', code: 'CAD' } };
    var plan = 'essentials';
    var range = est.querySelector('input[type=range]'), out = est.querySelector('output');
    var total = est.querySelector('.rd-est-total'), line = est.querySelector('.rd-est-line');
    var money = function (n, c) { return c.sym + n.toLocaleString('en-US', { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 }); };
    var render = function () {
      var c = LIST[root.classList.contains('cad') ? 'cad' : 'usd'], users = +range.value, each = c[plan];
      out.textContent = users;
      total.innerHTML = money(users * each, c) + '<em>' + c.code + ' / month</em>';
      line.innerHTML = '<span>' + users + ' × ' + (plan === 'essentials' ? 'Essentials' : 'Premium') + ' at ' + money(each, c) + '</span><b>' + money(users * each, c) + '</b>';
      [].forEach.call(est.querySelectorAll('[data-plan] span'), function (s) { s.textContent = money(c[s.parentNode.dataset.plan], c) + '/user'; });
      total.classList.remove('bump'); void total.offsetWidth; total.classList.add('bump');
      setTimeout(function () { total.classList.remove('bump'); }, 250);
    };
    [].forEach.call(est.querySelectorAll('[data-plan]'), function (b) {
      b.addEventListener('click', function () {
        plan = b.dataset.plan;
        [].forEach.call(est.querySelectorAll('[data-plan]'), function (x) { x.setAttribute('aria-pressed', x === b); });
        render();
      });
    });
    range.addEventListener('input', render);
    document.addEventListener('q84:currency', render);
    render();
  }
})();

/* Home page motion: word-by-word slogan, stat tilt, steps lighting up, portrait parallax */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // Slogan: wrap each word so it can rise in on its own
  var slogan = document.querySelector('.rd-slogan');
  if (slogan) {
    var i = 0;
    [].forEach.call(slogan.children, function (line) {
      var words = line.textContent.trim().split(/\s+/);
      line.textContent = '';
      words.forEach(function (w, k) {
        var s = document.createElement('span');
        s.className = 'rd-w'; s.style.setProperty('--i', i++); s.textContent = w;
        line.appendChild(s);
        if (k < words.length - 1) line.appendChild(document.createTextNode(' '));
      });
    });
    slogan.setAttribute('aria-label', slogan.textContent.replace(/\s+/g, ' ').trim());
    slogan.classList.add('rd-split');
  }

  // Stat cards tilt toward the cursor (mouse only)
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    [].forEach.call(document.querySelectorAll('.rd-stat'), function (c) {
      c.addEventListener('mousemove', function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.setProperty('--ry', ((x - 0.5) * 10).toFixed(2) + 'deg');
        c.style.setProperty('--rx', ((0.5 - y) * 10).toFixed(2) + 'deg');
        c.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
        c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
        c.classList.add('is-tilt');
      });
      c.addEventListener('mouseleave', function () { c.classList.remove('is-tilt'); });
    });
  }

  // Steps light up one after another once the row is in view
  var jobs = document.querySelector('.rd-jobs');
  if (jobs && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en, o) {
      if (!en[0].isIntersecting) return;
      o.disconnect();
      [].forEach.call(jobs.querySelectorAll('.rd-job'), function (j, k) {
        setTimeout(function () { j.classList.add('is-lit'); }, 500 + k * 650);
      });
    }, { threshold: 0.35 }).observe(jobs);
  }

  // Portrait drifts slightly slower than the page
  var fig = document.querySelector('.rd-person-cut');
  if (fig) {
    var ticking = false;
    var move = function () {
      ticking = false;
      var r = fig.getBoundingClientRect(), mid = r.top + r.height / 2 - innerHeight / 2;
      if (r.bottom < -200 || r.top > innerHeight + 200) return;
      fig.style.setProperty('--px', (mid * -0.06).toFixed(1) + 'px');
      fig.style.setProperty('--pg', (mid * 0.05).toFixed(1) + 'px');
    };
    addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(move); } }, { passive: true });
    move();
  }
})();

/* Featured-client card: rotate the featured client, its industry tag and the four logos below */
(function () {
  var card = document.querySelector('[data-rd-cc]');
  if (!card) return;
  var feat = [].slice.call(card.querySelectorAll('.rd-cc-feat img'));
  var cells = [].slice.call(card.querySelectorAll('.rd-cc-cell'));
  var dots = [].slice.call(card.querySelectorAll('.rd-cc-dots span'));
  var tag = card.querySelector('.rd-cc-tag'), ind = card.dataset.ind.split('|'), n = feat.length, cur = 0, timer;
  var show = function (i) {
    cur = (i + n) % n;
    feat.forEach(function (im, k) { im.classList.toggle('is-on', k === cur); });
    dots.forEach(function (d, k) { d.classList.toggle('is-on', k === cur); });
    tag.classList.add('is-swap');
    setTimeout(function () { tag.textContent = ind[cur]; tag.classList.remove('is-swap'); }, 250);
    cells.forEach(function (c, k) {
      var j = (cur + k + 1) % n;
      setTimeout(function () {
        c.classList.add('is-swap');
        setTimeout(function () {
          var src = feat[j].getAttribute('src'), im = c.querySelector('img');
          im.setAttribute('src', src); im.width = feat[j].width; im.height = feat[j].height; c.dataset.i = j;
          c.classList.remove('is-swap');
        }, 300);
      }, k * 70);
    });
  };
  cells.forEach(function (c) { c.addEventListener('click', function () { show(+c.dataset.i); restart(); }); });
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var restart = function () { clearInterval(timer); if (!still) timer = setInterval(function () { show(cur + 1); }, 3800); };
  card.addEventListener('mouseenter', function () { clearInterval(timer); });
  card.addEventListener('mouseleave', restart);
  restart();
})();
