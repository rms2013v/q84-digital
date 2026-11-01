(function () {
  var CFG = window.Q84 || {};

  // Mobile menu
  var menu = document.getElementById('navLinks');
  var btn = document.getElementById('menuBtn');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  }

  // Dropdowns: one open at a time, close on outside click or Escape
  var dds = [].slice.call(document.querySelectorAll('.dd'));
  dds.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) dds.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });
  document.addEventListener('click', function (e) {
    dds.forEach(function (d) { if (!d.contains(e.target)) d.open = false; });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    dds.forEach(function (d) {
      if (d.open) { d.open = false; d.querySelector('summary').focus(); }
    });
  });

  // Product tour tabs
  var tabs = [].slice.call(document.querySelectorAll('.tour-tab'));
  function selectTab(t, focus) {
    tabs.forEach(function (x) {
      var on = x === t;
      x.setAttribute('aria-selected', on);
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) t.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { selectTab(t); });
    t.addEventListener('keydown', function (e) {
      var j = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : null;
      if (j === null) return;
      e.preventDefault();
      selectTab(tabs[(j + tabs.length) % tabs.length], true);
    });
  });

  // Real screenshots replace the example screens once the files exist in /images
  var shots = document.querySelectorAll('[data-shot]');
  [].forEach.call(shots, function (fig) {
    var img = new Image();
    img.onload = function () {
      img.alt = fig.getAttribute('data-alt') || '';
      img.loading = 'lazy';
      fig.querySelector('.shot-body').replaceWith(img);
      var tag = fig.querySelector('.shot-bar span');
      if (tag) tag.textContent = '';
      var n = document.getElementById('shotNote');
      if (n) n.hidden = true;
    };
    img.src = fig.getAttribute('data-shot');
  });
  // Click-to-play video: the player loads only when the visitor asks for it
  [].forEach.call(document.querySelectorAll('.video-poster'), function (b) {
    b.addEventListener('click', function () {
      var v = document.createElement('video');
      v.src = b.getAttribute('data-video');
      v.controls = true; v.autoplay = true; v.playsInline = true;
      v.style.cssText = 'width:100%;aspect-ratio:16/9;border-radius:16px;background:#000';
      b.replaceWith(v);
      if (window.gtag) gtag('event', 'video_start', { video: 'walkthrough' });
    });
  });

  // Consultation form
  var form = document.getElementById('contactForm');
  if (form) {
    var rules = {
      name: function (v) { return v.length > 0; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); },
      company: function (v) { return v.length > 0; }
    };
    function check(id) {
      var v = document.getElementById('f-' + id).value.trim();
      var ok = rules[id](v);
      document.getElementById('e-' + id).hidden = ok;
      return ok;
    }
    Object.keys(rules).forEach(function (id) {
      var el = document.getElementById('f-' + id);
      el.addEventListener('blur', function () { if (el.value) check(id); });
      el.addEventListener('input', function () { document.getElementById('e-' + id).hidden = true; });
    });
    var status = document.getElementById('formStatus');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = Object.keys(rules).filter(function (id) { return !check(id); });
      if (bad.length) { document.getElementById('f-' + bad[0]).focus(); return; }
      if (form.querySelector('[name="_gotcha"]').value) return; // spam trap

      var data = {
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        company: form.company.value.trim(),
        topic: form.topic.value,
        message: form.message.value.trim()
      };
      var submit = form.querySelector('button[type="submit"]');

      if (CFG.formEndpoint) {
        submit.disabled = true;
        submit.textContent = 'Sending…';
        fetch(CFG.formEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(data)
        }).then(function (r) {
          if (!r.ok) throw new Error();
          form.hidden = true;
          document.getElementById('sent').hidden = false;
          if (window.gtag) gtag('event', 'generate_lead', { form: 'consultation' });
        }).catch(function () {
          submit.disabled = false;
          submit.textContent = 'Request my assessment';
          status.hidden = false;
          status.textContent = 'Your request didn’t go through. Try again, or email ' + CFG.email + ' directly.';
        });
      } else {
        // No form service connected yet: hand the message to the visitor's email app
        var body = 'Name: ' + data.name + '\nCompany: ' + data.company + '\nEmail: ' + data.email +
          '\nLooking for: ' + data.topic + '\n\n' + data.message;
        location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent('Consultation request: ' + data.company) +
          '&body=' + encodeURIComponent(body);
        status.hidden = false;
        status.textContent = 'Your email app should open with the message ready to send. If it doesn’t, email ' + CFG.email + '.';
        if (window.gtag) gtag('event', 'generate_lead', { form: 'consultation_email' });
      }
    });
  }

  // Placeholder social links: do nothing until real URLs are set
  [].forEach.call(document.querySelectorAll('[data-placeholder]'), function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); });
  });

  // Booking link clicks count as conversions
  [].forEach.call(document.querySelectorAll('[data-booking]'), function (a) {
    a.addEventListener('click', function () {
      if (window.gtag) gtag('event', 'generate_lead', { form: 'calendar_booking' });
    });
  });

  // License cost calculator (Microsoft US list prices, per user per month)
  var calc = document.getElementById('calc');
  if (calc) {
    var PRICES = { essentials: 80, premium: 110, team: 8 };
    var fmt = function (n) { return '$' + n.toLocaleString('en-US'); };
    function num(id) { var v = parseInt(document.getElementById(id).value, 10); return isNaN(v) || v < 0 ? 0 : Math.min(v, 999); }
    function update() {
      var plan = calc.querySelector('[name="plan"]:checked').value;
      var full = num('c-full'), team = num('c-team');
      var monthly = full * PRICES[plan] + team * PRICES.team;
      document.getElementById('o-monthly').textContent = fmt(monthly);
      document.getElementById('o-annual').textContent = fmt(monthly * 12);
      document.getElementById('o-full').textContent = full + ' × ' + fmt(PRICES[plan]) + ' = ' + fmt(full * PRICES[plan]);
      document.getElementById('o-team').textContent = team + ' × ' + fmt(PRICES.team) + ' = ' + fmt(team * PRICES.team);

      // Project size from scope drivers
      var score = 0, drivers = [];
      var companies = num('c-companies');
      if (full > 15) { score += 2; drivers.push('More than 15 full users'); } else if (full > 5) { score += 1; }
      if (companies > 1) { score += companies > 3 ? 2 : 1; drivers.push(companies + ' companies to set up'); }
      [].forEach.call(calc.querySelectorAll('[name="mod"]:checked'), function (m) {
        score += +m.getAttribute('data-w'); drivers.push(m.getAttribute('data-label'));
      });
      var src = calc.querySelector('[name="from"]').value;
      if (src === 'other-erp' || src === 'nav') { score += 2; drivers.push('Migration from ' + calc.querySelector('[name="from"] option:checked').textContent); }
      else if (src !== 'none') { score += 1; }
      var ints = num('c-int');
      if (ints) { score += ints > 2 ? 3 : ints; drivers.push(ints + ' integration' + (ints > 1 ? 's' : '')); }
      var size = score <= 3 ? 'Focused' : score <= 7 ? 'Standard' : 'Complex';
      var desc = {
        Focused: 'Mostly standard setup with a straightforward data move. Typically 2 to 3 months.',
        Standard: 'Several areas to configure plus migration or an integration. Typically 3 to 6 months.',
        Complex: 'Multiple companies, operations modules or integrations. Typically 6 months or more, often phased.'
      };
      document.getElementById('o-size').textContent = size;
      document.getElementById('o-size-desc').textContent = desc[size];
      var ul = document.getElementById('o-drivers');
      ul.innerHTML = '';
      (drivers.length ? drivers : ['Standard finance and sales setup']).forEach(function (d) {
        var li = document.createElement('li'); li.textContent = d; ul.appendChild(li);
      });
      if (plan === 'essentials' && calc.querySelector('[data-premium]:checked')) {
        document.getElementById('o-hint').hidden = false;
      } else {
        document.getElementById('o-hint').hidden = true;
      }
    }
    calc.addEventListener('input', update);
    calc.addEventListener('change', update);
    update();
  }
})();
