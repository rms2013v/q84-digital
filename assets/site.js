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
        name: form.elements['name'].value.trim(),
        email: form.elements['email'].value.trim(),
        company: form.elements['company'].value.trim(),
        topic: form.elements['topic'].value,
        message: form.elements['message'].value.trim()
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
          submit.textContent = 'Send message';
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

  // ---- Appointment scheduler (request a time) ----
  var schedEl = document.getElementById('days');
  if (schedEl && CFG.scheduler) {
    var S = CFG.scheduler;
    var BTZ = S.timezone || 'America/Vancouver';
    var SLOT = S.slot_minutes || 30;
    var visitorTZ = (Intl.DateTimeFormat().resolvedOptions().timeZone) || 'your time zone';

    function partsIn(date, tz) {
      var f = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' });
      var o = {};
      f.formatToParts(date).forEach(function (p) { o[p.type] = +p.value; });
      return o;
    }
    function offsetMin(date, tz) {
      var p = partsIn(date, tz);
      return (Date.UTC(p.year, p.month - 1, p.day, p.hour === 24 ? 0 : p.hour, p.minute, p.second) - Math.floor(date.getTime() / 1000) * 1000) / 60000;
    }
    function zoned(y, m, d, h, mi, tz) {
      var guess = Date.UTC(y, m - 1, d, h, mi);
      var off = offsetMin(new Date(guess), tz);
      var t = guess - off * 60000;
      var off2 = offsetMin(new Date(t), tz);
      if (off2 !== off) t = guess - off2 * 60000;
      return new Date(t);
    }
    function hm(str) { var a = str.split(':'); return [+a[0], +a[1]]; }

    var start = hm(S.start || '08:00'), end = hm(S.end || '16:00');
    var earliest = Date.now() + (S.min_notice_hours || 24) * 3600000;
    var today = partsIn(new Date(), BTZ);
    var days = [];
    for (var i = 0; i < 60 && days.length < (S.days_ahead || 10); i++) {
      var dUTC = new Date(Date.UTC(today.year, today.month - 1, today.day + i, 12));
      var y = dUTC.getUTCFullYear(), m = dUTC.getUTCMonth() + 1, d = dUTC.getUTCDate();
      if ((S.weekdays || [1, 2, 3, 4, 5]).indexOf(dUTC.getUTCDay()) === -1) continue;
      var slots = [];
      for (var t = start[0] * 60 + start[1]; t + SLOT <= end[0] * 60 + end[1]; t += SLOT) {
        var at = zoned(y, m, d, Math.floor(t / 60), t % 60, BTZ);
        if (at.getTime() >= earliest) slots.push(at);
      }
      if (slots.length) days.push({ label: dUTC, slots: slots });
    }

    var tzNote = document.getElementById('tzNote');
    if (tzNote) tzNote.textContent = 'Times are shown in your time zone (' + visitorTZ.replace(/_/g, ' ') + ').';

    var slotsEl = document.getElementById('slots');
    var bookForm = document.getElementById('bookForm');
    var picked = document.getElementById('picked');
    var chosen = null;
    var dayFmt = { weekday: 'short', month: 'short', day: 'numeric', timeZone: 'UTC' };
    var timeFmt = { hour: 'numeric', minute: '2-digit' };
    var longFmt = { weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit' };

    function pressed(group, btn) {
      [].forEach.call(group.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b === btn); });
    }
    function showDay(day, btn) {
      pressed(schedEl, btn);
      slotsEl.innerHTML = '';
      day.slots.forEach(function (at) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'slot'; b.setAttribute('aria-pressed', 'false');
        b.textContent = at.toLocaleTimeString([], timeFmt);
        b.addEventListener('click', function () { pick(at, b); });
        slotsEl.appendChild(b);
      });
    }
    function pick(at, btn) {
      chosen = at;
      pressed(slotsEl, btn);
      var biz = at.toLocaleString('en-US', { timeZone: BTZ, hour: 'numeric', minute: '2-digit' });
      picked.innerHTML = '';
      var strong = document.createElement('strong');
      strong.textContent = at.toLocaleString([], longFmt);
      picked.appendChild(document.createTextNode('Requested time: '));
      picked.appendChild(strong);
      picked.appendChild(document.createTextNode(' (' + SLOT + ' minutes, ' + biz + ' Vancouver time)'));
      bookForm.hidden = false;
      document.getElementById('b-name').focus({ preventScroll: true });
      bookForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    if (!days.length) {
      slotsEl.innerHTML = '';
      var p = document.createElement('p'); p.className = 'hint';
      p.textContent = 'No times are open right now. Send a message below and we’ll find a time.';
      slotsEl.appendChild(p);
    }
    days.forEach(function (day, idx) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'day'; b.setAttribute('aria-pressed', 'false');
      var parts = day.label.toLocaleDateString([], dayFmt).split(', ');
      b.innerHTML = '<span></span><strong></strong>';
      b.firstChild.textContent = parts[0];
      b.lastChild.textContent = parts.slice(1).join(', ') || parts[0];
      b.addEventListener('click', function () { showDay(day, b); });
      schedEl.appendChild(b);
      if (idx === 0) showDay(day, b);
    });

    document.getElementById('changeTime').addEventListener('click', function () {
      bookForm.hidden = true; chosen = null;
      pressed(slotsEl, null);
      slotsEl.querySelector('button') && slotsEl.querySelector('button').focus();
    });

    var bRules = {
      name: function (v) { return v.length > 0; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); },
      company: function (v) { return v.length > 0; }
    };
    function bCheck(id) {
      var ok = bRules[id](document.getElementById('b-' + id).value.trim());
      document.getElementById('be-' + id).hidden = ok;
      return ok;
    }
    Object.keys(bRules).forEach(function (id) {
      var el = document.getElementById('b-' + id);
      el.addEventListener('blur', function () { if (el.value) bCheck(id); });
      el.addEventListener('input', function () { document.getElementById('be-' + id).hidden = true; });
    });

    var bStatus = document.getElementById('bookStatus');
    function done(text) {
      bookForm.hidden = true;
      document.getElementById('days').closest('.sched-step').hidden = true;
      slotsEl.closest('.sched-step').hidden = true;
      var sent = document.getElementById('bookSent');
      document.getElementById('bookSentText').textContent = text;
      sent.hidden = false; sent.focus();
    }
    bookForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!chosen) return;
      var bad = Object.keys(bRules).filter(function (id) { return !bCheck(id); });
      if (bad.length) { document.getElementById('b-' + bad[0]).focus(); return; }
      if (bookForm.querySelector('[name="_gotcha"]').value) return;
      var when = chosen.toLocaleString([], longFmt);
      var pacific = chosen.toLocaleString('en-US', { timeZone: BTZ, weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit' });
      var data = {
        type: 'assessment_request',
        name: bookForm.elements['name'].value.trim(), email: bookForm.elements['email'].value.trim(), company: bookForm.elements['company'].value.trim(),
        notes: bookForm.elements['notes'].value.trim(), requested_time_utc: chosen.toISOString(),
        requested_time_pacific: pacific, visitor_time_zone: visitorTZ
      };
      var submit = bookForm.querySelector('button[type="submit"]');
      if (CFG.formEndpoint) {
        submit.disabled = true; submit.textContent = 'Sending…';
        fetch(CFG.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
          .then(function (r) {
            if (!r.ok) throw new Error();
            done('We’ve received your request for ' + when + ' (your time). Oleh will confirm by email with a calendar invite, normally within one business day.');
            if (window.gtag) gtag('event', 'generate_lead', { form: 'scheduler' });
          })
          .catch(function () {
            submit.disabled = false; submit.textContent = 'Request this time';
            bStatus.hidden = false;
            bStatus.textContent = 'Your request didn’t go through. Try again, or email ' + CFG.email + ' with your preferred time.';
          });
      } else {
        var body = 'Requested time: ' + pacific + ' Vancouver time (' + when + ' in ' + visitorTZ + ')\nName: ' + data.name +
          '\nCompany: ' + data.company + '\nEmail: ' + data.email + '\n\n' + data.notes;
        location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent('ERP assessment request: ' + data.company) + '&body=' + encodeURIComponent(body);
        done('Your email app should open with your request for ' + when + ' ready to send. Once it’s sent, Oleh will confirm with a calendar invite. If your email app didn’t open, email ' + CFG.email + '.');
        if (window.gtag) gtag('event', 'generate_lead', { form: 'scheduler_email' });
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
