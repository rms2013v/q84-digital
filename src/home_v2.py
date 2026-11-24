"""New homepage for the redesign preview (sections A-F from the reference), built from the real homepage's content."""
import re

PERSON = ('<svg class="rd-ph-person" viewBox="0 0 120 140" aria-hidden="true"><circle cx="60" cy="46" r="26"/>'
          '<path d="M12 140c4-34 24-52 48-52s44 18 48 52z"/></svg>')
LOGO_SHAPES = ['<circle cx="12" cy="12" r="9"/>', '<rect x="3" y="3" width="18" height="18" rx="4"/>', '<path d="M12 2l10 18H2z"/>',
               '<path d="M3 12h18M12 3v18"/>', '<path d="M4 18l8-14 8 14"/>', '<rect x="3" y="7" width="18" height="10" rx="5"/>',
               '<path d="M12 3a9 9 0 100 18 6 6 0 010-18z"/>', '<path d="M3 6h18M3 12h12M3 18h6"/>', '<path d="M5 5l14 14M19 5L5 19"/>', '<circle cx="8" cy="12" r="5"/><circle cx="16" cy="12" r="5"/>']
# Real client logos for the featured-client card: (file in redesign/clients/, name, width, height, industry tag).
# "-light" versions: trimmed, own colours, transparent background, for a white card.
CLIENT_LOGOS = [('tyc-americas-light.webp', 'TYC Americas', 427, 160, 'Automotive parts'),
                ('hana-group-light.webp', 'Hana Group', 153, 60, 'Food service'),
                ('maple-lodge-light.webp', 'Maple Lodge Farms', 480, 275, 'Food processing'),
                ('reliance-steel-light.webp', 'Reliance Steel & Aluminum Co.', 480, 206, 'Metals distribution'),
                ('statco-dsi-light.webp', 'Statco-DSI', 480, 67, 'Manufacturing'),
                ('pokemon-company-light.webp', 'The Pokémon Company International', 480, 87, 'Consumer products'),
                ('nova-medical-light.webp', 'Nova Medical Hair Transplant Clinics', 480, 121, 'Healthcare'),
                ('easy-renovation-light.webp', 'EasyRenovation', 306, 90, 'Home services')]
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'


def home(s):
    main = re.search(r'<main id="main">(.*)</main>', s, re.S).group(1)
    S = re.findall(r'<section[^>]*>.*?</section>', main, re.S)
    hero, problems, tour, industries, scen, quotes, deliver, why, process, faq, promo, cta = S
    quote_list = re.findall(r'<blockquote>(.*?)</blockquote><figcaption><strong>(.*?)</strong>, (.*?)</figcaption>', quotes, re.S)

    # A + B: slogan and featured-client card. One client is featured at a time (logo + industry),
    # the next four sit in the grid below; rd.js rotates through them. No quotes or results are invented.
    img = lambda f, n, w, h, cls='': f'<img class="{cls}" src="/images/clients/{f}" alt="" width="{w}" height="{h}" loading="eager" decoding="async">'
    feat = ''.join(img(f, n, w, h, 'is-on' if k == 0 else '') for k, (f, n, w, h, ind) in enumerate(CLIENT_LOGOS))
    grid = ''.join(f'<button type="button" class="rd-cc-cell" data-i="{k}" tabindex="-1">{img(f, n, w, h)}</button>' for k, (f, n, w, h, ind) in enumerate(CLIENT_LOGOS[1:5], 1))
    names = ''.join(f'<li>{n}</li>' for f, n, w, h, ind in CLIENT_LOGOS)
    data = '|'.join(ind for *_, ind in CLIENT_LOGOS)
    dots = ''.join(f'<span class="{"is-on" if k == 0 else ""}"></span>' for k in range(len(CLIENT_LOGOS)))
    card = (f'<div class="rd-cc rd-enter rd-enter-2" data-rd-cc data-ind="{data}">'
            f'<h2 class="visually-hidden">Our clients</h2><ul class="visually-hidden">{names}</ul>'
            f'<div class="rd-cc-top" aria-hidden="true"><div class="rd-cc-feat">{feat}</div><span class="rd-cc-tag">{CLIENT_LOGOS[0][4]}</span></div>'
            '<p class="rd-cc-line">Trusted by distributors, manufacturers and service businesses across the US and Canada.</p>'
            '<div class="rd-cc-stats"><div><b>30+</b><span>projects delivered</span></div><div><b>100%</b><span>senior-led projects</span></div></div>'
            f'<div class="rd-cc-grid" aria-hidden="true">{grid}</div><div class="rd-cc-dots" aria-hidden="true">{dots}</div></div>')
    a = f'''<section class="hero rd-hero2"><span class="rd-glow rd-glow-1" aria-hidden="true"></span><span class="rd-glow rd-glow-2" aria-hidden="true"></span><div class="wrap rd-hero2-grid">
  <div class="rd-hero2-copy rd-enter">
    <span class="eyebrow">Microsoft Dynamics 365 Business Central partner · Vancouver &amp; Tacoma</span>
    <h1 class="rd-slogan"><span>Connected,</span><span>Reliable ERP</span><span class="h1-accent">For Your Business</span></h1>
    <p class="lede">Replace disconnected accounting, inventory and warehouse systems with one connected ERP platform, implemented and supported by senior consultants.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="/contact/#schedule">Book a free ERP assessment</a><a class="btn btn-ghost" href="#steps">See how we work</a></div>
  </div>
  {card}
</div></section>'''

    # C: SEO copy - why Q84 Digital
    c = '''<section id="why-q84"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Why Q84 Digital</span><h2>A Business Central partner that knows how your business runs</h2>
    <p class="lede">Q84 Digital implements Microsoft Dynamics 365 Business Central for distributors, manufacturers and service businesses across the US and Canada. Here’s when it’s time for a new ERP, and why companies choose us to deliver it.</p></div>
  <div class="rd-why">
    <article class="rd-why-col"><span class="rd-why-n">01</span><h3>Common signs you need a new ERP</h3>
      <ul class="rd-ticks">
        <li>Inventory counts drift from what’s on the shelf.</li>
        <li>Shipments, invoices and the ledger are reconciled by hand.</li>
        <li>Orders are retyped between email, spreadsheets and systems.</li>
        <li>You’ve outgrown QuickBooks, Sage, Dynamics GP or NAV.</li>
        <li>The warehouse can’t keep up with picking and shipping.</li>
        <li>Growth adds spreadsheets instead of clear margins.</li></ul></article>
    <article class="rd-why-col"><span class="rd-why-n">02</span><h3>A senior team, on site when it matters</h3>
      <p>Every Q84 Digital consultant has more than 10 years of Microsoft Dynamics and ERP experience. The people who scope your project are the people who deliver it, with no hand-off to a junior team.</p>
      <p>With offices in <a href="/business-central-partner-vancouver/">Vancouver, BC</a> and <a href="/business-central-partner-tacoma/">Tacoma, WA</a>, we run discovery workshops, warehouse walkthroughs, training and go-live support at your site, and the rest of the project remotely to keep costs down.</p></article>
    <article class="rd-why-col"><span class="rd-why-n">03</span><h3>Deep industry expertise</h3>
      <ul class="rd-inds">
        <li><a href="/industries/distribution/"><strong>Wholesale distribution</strong><span>Multi-location stock, landed costs, bins and scanning.</span></a></li>
        <li><a href="/industries/manufacturing/"><strong>Manufacturing</strong><span>Bills of materials, production orders and product costing.</span></a></li>
        <li><a href="/industries/ecommerce/"><strong>E-commerce</strong><span>Shopify and marketplace orders, stock and fulfillment in one system.</span></a></li>
        <li><a href="/industries/professional-services/"><strong>Professional services</strong><span>Projects, jobs and contracts billed from one ledger.</span></a></li></ul></article>
  </div>
</div></section>'''

    # D: client photo cards (two real quotes with placeholder photos, plus placeholder slots)
    cards = ''
    for q, name, role in quote_list:
        short = re.sub(r'\s+', ' ', q).strip()
        cards += (f'<figure class="rd-client"><div class="rd-client-ph">{PERSON}<span class="rd-ph-tag">Placeholder photo</span></div>'
                  f'<figcaption><blockquote>{short}</blockquote><strong>{name}</strong><span>{role}</span></figcaption></figure>')
    for _ in range(3):
        cards += (f'<figure class="rd-client rd-client-empty"><div class="rd-client-ph">{PERSON}<span class="rd-ph-tag">Placeholder photo</span></div>'
                  '<figcaption><strong class="rd-client-result">Client result goes here</strong><span>Client name, company</span></figcaption></figure>')
    d = f'''<section class="rd-clients"><div class="wrap">
  <div class="rd-clients-head"><div><span class="eyebrow">Client stories</span><h2>We deliver.<br>Just ask our clients.</h2></div>
    <p>Business Central projects succeed when the system fits how the business really works. Here’s what clients say about working with us.</p>
    <div class="rd-car-btns"><button type="button" class="rd-car-btn" data-dir="-1" aria-label="Previous client stories">←</button><button type="button" class="rd-car-btn" data-dir="1" aria-label="Next client stories">→</button></div></div>
</div><div class="rd-car" tabindex="0" aria-label="Client stories">{cards}</div></section>'''

    # E: numbers - split card: copy and three stats on the left, consultant photo on the right
    stats = [('30', '+', 'Projects delivered', 'Implementations, migrations and rescues.'),
             ('10', 'k+', 'Parcels shipped', 'Through systems designed and delivered by us.'),
             ('100', '%', 'Senior-led', 'The people who scope your project deliver it.')]
    tiles = ''.join(f'<div class="rd-n2-stat"><small>0{k}</small><strong><span data-count="{n}">{n}</span>{u}</strong><b>{t}</b><p>{x}</p></div>'
                    for k, (n, u, t, x) in enumerate(stats, 1))
    e = f'''<section class="rd-numbers2"><div class="wrap"><div class="rd-n2">
  <div class="rd-n2-copy">
    <span class="eyebrow rd-eyebrow-line">By the numbers</span>
    <h2>Experience you can put a face to.</h2>
    <p class="lede">No junior hand-offs. The people you meet on day one stay accountable through go-live.</p>
    <div class="rd-n2-stats">{tiles}</div>
  </div>
  <figure class="rd-n2-photo"><span class="rd-n2-circle" aria-hidden="true"></span><img src="/images/clients/headshot-2-cutout.webp" alt="Q84 Digital senior consultant" width="720" height="720" loading="lazy">
    <figcaption><i aria-hidden="true"></i><span><small>Your project lead</small>Senior-led from first call to go-live</span></figcaption></figure>
</div></div></section>'''

    # F: a true partnership - your side + our side
    def side(cls, k, label, h, items):
        lis = ''.join(f'<li><span class="rd-side-tick">{CHECK}</span>{i}</li>' for i in items)
        return f'<article class="rd-side {cls}"><div class="rd-side-k"><span>{k}</span>{label}</div><h3>{h}</h3><ul>{lis}</ul></article>'
    f = f'''<section id="steps"><div class="wrap">
  <div class="rd-sides-head"><span class="eyebrow rd-eyebrow-line">A true partnership</span><h2>You know the business.<br>We know the build.</h2></div>
  <div class="rd-sides">
    {side('rd-side-dark', '01', 'Your side', 'Keep the business moving.', ['Share how work really gets done', 'Make the key decisions', 'Test real processes'])}
    <span class="rd-sides-plus" aria-hidden="true">+</span>
    {side('', '02', 'Our side', 'Own the implementation.', ['Configure Business Central', 'Migrate and check your data', 'Train and support your team'])}
  </div>
</div></section>'''

    # keep the product tour, industries, process + costs (dark), FAQ, checklist and booking
    proc = process.replace('<section>', '<section class="rd-dark" id="process">', 1)
    est = """
<section class="band" id="estimate"><div class="wrap rd-est">
  <div class="stack"><span class="eyebrow">Transparent starting point</span><h2>Estimate your Business Central licenses</h2>
    <p class="lede">Choose a license and team size for a quick monthly estimate. Implementation is quoted separately, as a fixed scope after discovery.</p>
    <ul class="checks"><li><div><strong>Microsoft list prices</strong>, in US or Canadian dollars.</div></li><li><div><strong>No hidden packages.</strong> Licenses come from Microsoft at list price.</div></li><li><div><strong>Right-sized advice</strong> on which users need which license.</div></li></ul></div>
  <div class="rd-est-card" data-rd-est>
    <div class="rd-est-top"><div><small>Monthly estimate</small><div class="rd-est-total" aria-live="polite"></div></div><span class="rd-spark" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2z"/></svg></span></div>
    <div><p class="rd-range-head" style="margin:0 0 8px">License type</p><div class="rd-seg" role="group" aria-label="License type"><button type="button" data-plan="essentials" aria-pressed="true">Essentials <span></span></button><button type="button" data-plan="premium" aria-pressed="false">Premium <span></span></button></div></div>
    <div><label class="rd-range-head" for="rdUsers">Full users <output for="rdUsers">8</output></label><input id="rdUsers" type="range" min="1" max="50" value="8"></div>
    <div class="rd-est-line"></div>
    <a class="btn btn-primary" href="/licensing/#calculator">Get a complete estimate</a>
    <p class="rd-est-note">Based on Microsoft list prices per full user per month. Taxes and implementation not included.</p>
  </div>
</div></section>"""
    # the industries tabs section was removed at the owner's request
    # client stories carousel (d) removed at the owner's request
    new = '\n'.join([a, c, e, f, tour, proc, est, faq, promo, cta])
    return s.replace(main, '\n' + new + '\n', 1)
