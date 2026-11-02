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

  // Tab groups (product tour, industries): each tablist works on its own
  [].forEach.call(document.querySelectorAll('[role="tablist"]'), function (list) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
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
  });

  // In-page section menu: highlight the section in view
  var sub = document.querySelector('.subnav');
  if (sub && 'IntersectionObserver' in window) {
    var links = [].slice.call(sub.querySelectorAll('a[href^="#"]'));
    var map = {};
    links.forEach(function (a) { var el = document.getElementById(a.getAttribute('href').slice(1)); if (el) map[el.id] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute('aria-current'); });
        var a = map[en.target.id]; if (a) { a.setAttribute('aria-current', 'true'); if (a.scrollIntoView && sub.scrollWidth > sub.clientWidth) sub.querySelector('.subnav-links').scrollLeft = a.offsetLeft - 16; }
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

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
      var yt = b.getAttribute('data-youtube');
      if (yt) {
        var f = document.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + yt + '?autoplay=1&rel=0&modestbranding=1';
        f.title = b.getAttribute('data-title') || 'Video';
        f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        f.allowFullscreen = true;
        f.referrerPolicy = 'strict-origin-when-cross-origin';
        f.className = 'yt-frame';
        b.replaceWith(f);
        if (window.gtag) gtag('event', 'video_start', { video: yt });
        return;
      }
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
  if (CFG.scheduler && CFG.scheduler.start) {
    var S = CFG.scheduler;
    var BTZ = S.timezone || 'America/Los_Angeles';
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
    var MONTHS = Math.max(1, S.months_ahead || 3);
    var avail = {};
    var lastMonth = new Date(Date.UTC(today.year, today.month + MONTHS, 1));
    for (var i = 0; i < 400; i++) {
      var dUTC = new Date(Date.UTC(today.year, today.month - 1, today.day + i, 12));
      if (dUTC >= lastMonth) break;
      var y = dUTC.getUTCFullYear(), m = dUTC.getUTCMonth() + 1, d = dUTC.getUTCDate();
      if ((S.weekdays || [1, 2, 3, 4, 5]).indexOf(dUTC.getUTCDay()) === -1) continue;
      if ((S.blocked_dates || []).indexOf(dUTC.toISOString().slice(0, 10)) !== -1) continue;
      var slots = [];
      for (var t = start[0] * 60 + start[1]; t + SLOT <= end[0] * 60 + end[1]; t += SLOT) {
        var at = zoned(y, m, d, Math.floor(t / 60), t % 60, BTZ);
        if (at.getTime() >= earliest) slots.push(at);
      }
      if (slots.length) avail[y + '-' + m + '-' + d] = { label: dUTC, slots: slots };
    }
    var keys = Object.keys(avail);
    var firstKey = keys.length ? keys[0].split('-') : [today.year, today.month];
    var monthList = [];
    for (var k = 0; k < MONTHS; k++) {
      var md = new Date(Date.UTC(+firstKey[0], +firstKey[1] - 1 + k, 1, 12));
      monthList.push({ y: md.getUTCFullYear(), m: md.getUTCMonth() + 1, label: md });
    }
    var endKey = new Date(Date.UTC(monthList[MONTHS - 1].y, monthList[MONTHS - 1].m, 1));
    keys.forEach(function (key) { if (avail[key].label >= endKey) delete avail[key]; });

    // Closing section: show the next few open times on every page
    var nextEl = document.getElementById('nextSlots');
    if (nextEl) {
      var upcoming = [];
      Object.keys(avail).some(function (key) {
        var sl = avail[key].slots;
        upcoming.push(sl[Math.min(2, sl.length - 1)]);
        return upcoming.length >= 3;
      });
      if (upcoming.length) {
        nextEl.innerHTML = '';
        upcoming.forEach(function (at) {
          var a = document.createElement('a');
          a.className = 'next-slot';
          a.href = nextEl.getAttribute('data-contact') + '?slot=' + encodeURIComponent(at.toISOString()) + '#schedule';
          var day = document.createElement('span');
          day.textContent = at.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
          var time = document.createElement('strong');
          time.textContent = at.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
          a.appendChild(day); a.appendChild(time);
          a.setAttribute('aria-label', 'Request ' + at.toLocaleString([], { weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit' }));
          nextEl.appendChild(a);
        });
      }
    }

    var schedEl = document.getElementById('days');
    if (schedEl) {

    var tzNote = document.getElementById('tzNote');
    if (tzNote) tzNote.textContent = 'Times are shown in your time zone (' + visitorTZ.replace(/_/g, ' ') + ').';

    var slotsEl = document.getElementById('slots');
    var bookForm = document.getElementById('bookForm');
    var picked = document.getElementById('picked');
    var chosen = null;
    var timeFmt = { hour: 'numeric', minute: '2-digit' };
    var longFmt = { weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit' };

    function pressed(group, btn) {
      [].forEach.call(group.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b === btn); });
    }
    function pick(at, btn) {
      chosen = at;
      pressed(slotsEl, btn);
      var biz = at.toLocaleString('en-US', { timeZone: BTZ, hour: 'numeric', minute: '2-digit', timeZoneName: 'short' });
      picked.innerHTML = '';
      var strong = document.createElement('strong');
      strong.textContent = at.toLocaleString([], longFmt);
      picked.appendChild(document.createTextNode('Requested time: '));
      picked.appendChild(strong);
      picked.appendChild(document.createTextNode(' (' + SLOT + ' minutes, ' + biz + ')'));
      bookForm.hidden = false;
      document.getElementById('b-name').focus({ preventScroll: true });
      bookForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    var grid = document.getElementById('calGrid');
    var monthSel = document.getElementById('calMonth');
    var prevBtn = document.getElementById('calPrev'), nextBtn = document.getElementById('calNext');
    var slotsTitle = document.getElementById('slotsTitle');
    var monthIdx = 0, selectedKey = null;

    monthList.forEach(function (mo, i) {
      var o = document.createElement('option');
      o.value = i;
      o.textContent = mo.label.toLocaleDateString([], { month: 'long', year: 'numeric', timeZone: 'UTC' });
      monthSel.appendChild(o);
    });

    function noTimes(msg) {
      slotsEl.innerHTML = '';
      var p = document.createElement('p'); p.className = 'hint'; p.textContent = msg;
      slotsEl.appendChild(p);
      slotsTitle.textContent = 'Choose a time';
    }
    function selectDay(key) {
      selectedKey = key;
      var day = avail[key];
      [].forEach.call(grid.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-key') === key); });
      bookForm.hidden = true; chosen = null;
      slotsTitle.textContent = day.label.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric', timeZone: 'UTC' });
      slotsEl.innerHTML = '';
      day.slots.forEach(function (at) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'slot'; b.setAttribute('aria-pressed', 'false');
        b.textContent = at.toLocaleTimeString([], timeFmt);
        b.addEventListener('click', function () { pick(at, b); });
        slotsEl.appendChild(b);
      });
    }
    function renderMonth(idx) {
      monthIdx = idx;
      monthSel.value = idx;
      prevBtn.classList.toggle('is-off', idx === 0);
      nextBtn.classList.toggle('is-off', idx === monthList.length - 1);
      prevBtn.tabIndex = idx === 0 ? -1 : 0;
      nextBtn.tabIndex = idx === monthList.length - 1 ? -1 : 0;
      var mo = monthList[idx];
      var first = new Date(Date.UTC(mo.y, mo.m - 1, 1)).getUTCDay();
      var count = new Date(Date.UTC(mo.y, mo.m, 0)).getUTCDate();
      grid.innerHTML = '';
      for (var e = 0; e < first; e++) { var sp = document.createElement('span'); sp.className = 'cal-blank'; grid.appendChild(sp); }
      var firstAvail = null;
      for (var dd = 1; dd <= count; dd++) {
        var key = mo.y + '-' + mo.m + '-' + dd;
        if (avail[key]) {
          var b = document.createElement('button');
          b.type = 'button'; b.className = 'cal-day'; b.textContent = dd;
          b.setAttribute('data-key', key);
          b.setAttribute('aria-pressed', 'false');
          b.setAttribute('aria-label', avail[key].label.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric', timeZone: 'UTC' }) + ', ' + avail[key].slots.length + ' times available');
          (function (k2) { b.addEventListener('click', function () { selectDay(k2); }); })(key);
          grid.appendChild(b);
          if (!firstAvail) firstAvail = key;
        } else {
          var off = document.createElement('span'); off.className = 'cal-off'; off.textContent = dd;
          off.setAttribute('aria-hidden', 'true');
          grid.appendChild(off);
        }
      }
      if (selectedKey && grid.querySelector('[data-key="' + selectedKey + '"]')) selectDay(selectedKey);
      else if (firstAvail) selectDay(firstAvail);
      else noTimes('No open times this month. Try the next month, or send a message below.');
    }
    prevBtn.addEventListener('click', function () { if (monthIdx > 0) renderMonth(monthIdx - 1); });
    nextBtn.addEventListener('click', function () { if (monthIdx < monthList.length - 1) renderMonth(monthIdx + 1); });
    monthSel.addEventListener('change', function () { renderMonth(+monthSel.value); });

    var startIdx = 0;
    for (var q = 0; q < monthList.length; q++) {
      var mq = monthList[q], has = false;
      for (var key2 in avail) { if (key2.indexOf(mq.y + '-' + mq.m + '-') === 0) { has = true; break; } }
      if (has) { startIdx = q; break; }
    }
    if (Object.keys(avail).length) renderMonth(startIdx);
    else { renderMonth(0); noTimes('No times are open right now. Send a message below and we’ll find a time.'); }

    // A time chosen in the closing section arrives as ?slot=ISO: open that day and time
    var wanted = new URLSearchParams(location.search).get('slot');
    if (wanted) {
      var wt = Date.parse(wanted);
      Object.keys(avail).some(function (key) {
        var idx = -1;
        avail[key].slots.some(function (at, n) { if (at.getTime() === wt) { idx = n; return true; } return false; });
        if (idx === -1) return false;
        var parts = key.split('-');
        for (var mi = 0; mi < monthList.length; mi++) {
          if (monthList[mi].y === +parts[0] && monthList[mi].m === +parts[1]) { selectedKey = key; renderMonth(mi); break; }
        }
        var btn = slotsEl.querySelectorAll('button')[idx];
        if (btn) btn.click();
        return true;
      });
    }

    document.getElementById('changeTime').addEventListener('click', function () {
      bookForm.hidden = true; chosen = null;
      [].forEach.call(slotsEl.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', 'false'); });
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
      document.getElementById('schedPick').hidden = true;
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
      var pacific = chosen.toLocaleString('en-US', { timeZone: BTZ, weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' });
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
        var body = 'Requested time: ' + pacific + ' (' + when + ' in ' + visitorTZ + ')\nName: ' + data.name +
          '\nCompany: ' + data.company + '\nEmail: ' + data.email + '\n\n' + data.notes;
        location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent('ERP assessment request: ' + data.company) + '&body=' + encodeURIComponent(body);
        done('Your email app should open with your request for ' + when + ' ready to send. Once it’s sent, Oleh will confirm with a calendar invite. If your email app didn’t open, email ' + CFG.email + '.');
        if (window.gtag) gtag('event', 'generate_lead', { form: 'scheduler_email' });
      }
    });
  }

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

/* Track checklist downloads */
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('[data-download]');
  if (a && window.gtag) gtag('event', 'file_download', { file_name: a.getAttribute('data-download'), link_url: a.href });
});
