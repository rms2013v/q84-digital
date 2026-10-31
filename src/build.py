#!/usr/bin/env python3
"""Builds the Q84 Digital static site from src/site.json and the page content below.

Run from the repository root:  python3 src/build.py
In page content, "@/" means the site's base path (set "base" in site.json).
"""
import json, html, os, re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, 'src', 'site.json')))
BASE = CFG['base']
URL = CFG['site_url']
EMAIL = CFG['email']
TODAY = date.today().isoformat()
import hashlib
def ver(f):
    return hashlib.md5(open(os.path.join(ROOT, f), 'rb').read()).hexdigest()[:8]
CSS_V, JS_V = ver('assets/site.css'), ver('assets/site.js')

ICON = {
    'chart': '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    'box': '<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>',
    'link': '<path d="M10 13a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1"/><path d="M14 11a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/>',
    'ledger': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M8 15h3"/>',
    'receipt': '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    'cart': '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h12L22 7H6"/>',
    'warehouse': '<path d="M3 21V9l9-6 9 6v12"/><path d="M7 21v-8h10v8M7 17h10"/>',
    'pie': '<path d="M21 12A9 9 0 1112 3v9z"/><path d="M15 3.5A9 9 0 0120.5 9H15z"/>',
    'factory': '<path d="M3 21V10l6 4V10l6 4V6h6v15z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
    'truck': '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    'shop': '<path d="M4 9l1-5h14l1 5"/><path d="M4 9v11h16V9"/><path d="M4 9a2.7 2.7 0 005.3 0 2.7 2.7 0 005.4 0 2.7 2.7 0 005.3 0"/>',
    'tools': '<path d="M14.7 6.3a4 4 0 00-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 005.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    'migrate': '<path d="M4 7h12l-3-3M20 17H8l3 3"/>',
    'support': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M5.6 5.6l3.6 3.6M14.8 14.8l3.6 3.6M18.4 5.6l-3.6 3.6M9.2 14.8l-3.6 3.6"/>',
    'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
}

def icon(name):
    return f'<span class="icon"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg></span>'

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- shared parts

NAV = [
    ('business-central', 'Business Central', '@/business-central/', None),
    ('services', 'Services', None, [
        ('implementation', 'Implementation', '@/implementation/'),
        ('licensing', 'Licensing & pricing', '@/licensing/'),
        ('data-migration', 'Data migration', '@/data-migration/'),
        ('integrations', 'Integrations & customization', '@/integrations/'),
        ('support', 'Support', '@/support/'),
    ]),
    ('industries', 'Industries', None, [
        ('distribution', 'Wholesale distribution', '@/industries/distribution/'),
        ('manufacturing', 'Manufacturing', '@/industries/manufacturing/'),
    ]),
    ('about', 'About', '@/#consultant', None),
]

def header(current):
    items = []
    for key, label, href, children in NAV:
        if children:
            is_cur = any(c[0] == current for c in children)
            cur_attr = ' aria-current="page"'
            links = ''.join(
                f'<a href="{h}"{cur_attr if k == current else ""}>{esc(l)}</a>' for k, l, h in children)
            items.append(f'<details class="dd{" current" if is_cur else ""}"><summary>{label}</summary><div class="dd-menu">{links}</div></details>')
        else:
            cur = ' aria-current="page"' if key == current else ''
            items.append(f'<a href="{href}"{cur}>{label}</a>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap nav">
    <a class="logo" href="@/" aria-label="Q84 Digital home"><span class="logo-mark">Q84</span>Q84 Digital</a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="navLinks">Menu</button>
    <nav class="nav-links" id="navLinks" aria-label="Main">
      {''.join(items)}
      <a class="btn btn-primary" href="@/contact/">Book a consultation</a>
    </nav>
  </div>
</header>'''

def footer():
    legal = f'Q84 Digital is operated by {esc(CFG["legal_name"])}. ' if CFG.get('legal_name') else ''
    phone = f'<li>{esc(CFG["phone"])}</li>' if CFG.get('phone') else ''
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div class="stack" style="gap:12px">
        <a class="logo" href="@/"><span class="logo-mark">Q84</span>Q84 Digital</a>
        <p>Business Central implementation and ERP consulting for distributors, manufacturers and inventory-driven businesses.</p>
        <ul style="list-style:none;padding:0;margin:0;display:grid;gap:4px"><li style="user-select:all">{esc(EMAIL)}</li>{phone}<li>Vancouver, British Columbia</li></ul>
      </div>
      <div><h4>Business Central</h4><ul><li><a href="@/business-central/">Overview &amp; features</a></li><li><a href="@/licensing/">Licensing &amp; pricing</a></li><li><a href="@/business-central/#fit">Is Business Central enough?</a></li></ul></div>
      <div><h4>Services</h4><ul><li><a href="@/implementation/">Implementation</a></li><li><a href="@/data-migration/">Data migration</a></li><li><a href="@/integrations/">Integrations</a></li><li><a href="@/support/">Support</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="@/#consultant">About</a></li><li><a href="@/industries/distribution/">Distribution</a></li><li><a href="@/industries/manufacturing/">Manufacturing</a></li><li><a href="@/contact/">Contact</a></li><li><a href="@/privacy/">Privacy</a></li></ul></div>
    </div>
    <div class="legal"><span>© {date.today().year} Q84 Digital. {legal}All rights reserved.</span><span>Microsoft, Dynamics 365 and Business Central are trademarks of the Microsoft group of companies. Q84 Digital is an independent consultancy.</span></div>
  </div>
</footer>'''

def cta(title='Let’s talk about your ERP project', text='Book a free, no-obligation consultation. You’ll speak directly with the consultant who would deliver your project.'):
    booking = ''
    if CFG.get('booking_url'):
        booking = f'<a class="btn btn-ghost" href="{esc(CFG["booking_url"])}" data-booking target="_blank" rel="noopener">Pick a time on my calendar</a>'
    return f'''<section><div class="wrap"><div class="cta"><div><h2>{title}</h2><p>{text}</p></div>
<div class="hero-actions"><a class="btn btn-primary" href="@/contact/">Book a consultation</a>{booking}</div></div></div></section>'''

def page_head(title, crumb, h1, lede, button=True):
    btn = '<div class="hero-actions"><a class="btn btn-primary" href="@/contact/">Book a consultation</a></div>' if button else ''
    return f'''<div class="page-head"><div class="wrap stack">
<nav class="crumb" aria-label="Breadcrumb"><a href="@/">Home</a> / {crumb}</nav>
<h1>{h1}</h1>
<p class="lede">{lede}</p>{btn}
</div></div>'''

def checks(items):
    return '<ul class="checks">' + ''.join(f'<li><div>{i}</div></li>' for i in items) + '</ul>'

EXAMPLES = '''<div class="grid g3">
  <article class="example"><span class="label">Illustrative scenario</span><h3>Wholesale distributor</h3>
    <dl><div><dt>Challenge</dt><dd>Inventory kept in spreadsheets, accounting in a separate system and purchase orders written by hand.</dd></div>
    <div><dt>Approach</dt><dd>Business Central with inventory, purchasing and warehouse receiving, picking and shipping.</dd></div>
    <div><dt>Intended outcome</dt><dd>One view of stock across locations and purchasing driven by reorder points.</dd></div></dl></article>
  <article class="example"><span class="label">Illustrative scenario</span><h3>E-commerce business</h3>
    <dl><div><dt>Challenge</dt><dd>Shopify orders, stock levels and accounting handled in three places and reconciled by hand.</dd></div>
    <div><dt>Approach</dt><dd>Business Central connected to Shopify for orders, items, stock and payments.</dd></div>
    <div><dt>Intended outcome</dt><dd>Less manual order entry and stock levels that stay in step with the online store.</dd></div></dl></article>
  <article class="example"><span class="label">Illustrative scenario</span><h3>Manufacturing company</h3>
    <dl><div><dt>Challenge</dt><dd>Little visibility into production and product costs worked out in spreadsheets.</dd></div>
    <div><dt>Approach</dt><dd>Business Central Premium with bills of materials, production orders and cost reporting.</dd></div>
    <div><dt>Intended outcome</dt><dd>Planned production and product costs that come straight from the system.</dd></div></dl></article>
</div>
<p class="shot-note" style="margin-top:16px">These scenarios show how we approach typical projects. They are not client case studies.</p>'''

FIT = '''<div class="fit">
  <div class="card"><span class="tag">Often the right fit</span><h3>Business Central</h3><p>Standard inventory and warehouse processes: receiving, put-away, picking, shipping and bin-level stock for small and midsize operations.</p></div>
  <div class="card"><span class="tag">When you need more</span><h3>Business Central plus a warehouse extension</h3><p>Barcode scanning, handheld devices or more advanced picking, added through a specialist app from Microsoft AppSource.</p></div>
  <div class="card"><span class="tag">For complex operations</span><h3>Dynamics 365 Supply Chain Management</h3><p>High-volume or multi-site warehousing, advanced wave picking, transportation management and complex supply chains.</p></div>
</div>'''

TOUR = '''<section id="tour" style="border-top:1px solid var(--line)">
<div class="wrap">
  <div class="section-head">
    <span class="eyebrow">See it in action</span>
    <h2>What your team will work in every day</h2>
    <p class="lede">Business Central puts finance, stock, orders and the warehouse on the same screens. Here's what each area looks like.</p>
  </div>
  <div class="tour-tabs" role="tablist" aria-label="Business Central areas">
    <button class="tour-tab" role="tab" id="tab-dash" aria-controls="panel-dash" aria-selected="true">Dashboard</button>
    <button class="tour-tab" role="tab" id="tab-inv" aria-controls="panel-inv" aria-selected="false" tabindex="-1">Inventory</button>
    <button class="tour-tab" role="tab" id="tab-sales" aria-controls="panel-sales" aria-selected="false" tabindex="-1">Sales orders</button>
    <button class="tour-tab" role="tab" id="tab-wh" aria-controls="panel-wh" aria-selected="false" tabindex="-1">Warehouse</button>
  </div>

  <div class="tour-panel" role="tabpanel" id="panel-dash" aria-labelledby="tab-dash">
    <figure class="shot" style="margin:0" data-shot="@/images/dashboard.png" data-alt="Business Central role center dashboard showing sales, receivables and inventory figures">
      <div class="shot-bar"><b>Role Center · Business Manager</b><span>Example data</span></div>
      <div class="shot-body">
        <div class="kpis">
          <div class="kpi"><span>Sales this month</span><strong>$184,250</strong></div>
          <div class="kpi"><span>Overdue receivables</span><strong>$12,480</strong></div>
          <div class="kpi"><span>Inventory value</span><strong>$612,900</strong></div>
          <div class="kpi warn"><span>Items below reorder</span><strong>7</strong></div>
        </div>
        <div>
          <div style="font-weight:600;margin-bottom:6px">Sales by month</div>
          <div class="bars" aria-hidden="true"><div style="height:48%"></div><div style="height:56%"></div><div style="height:52%"></div><div style="height:64%"></div><div style="height:71%"></div><div style="height:83%"></div></div>
          <div class="bar-labels" aria-hidden="true"><span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span></div>
        </div>
      </div>
    </figure>
    <div class="tour-copy"><h3>Financial and operational visibility</h3><p>Each person opens Business Central to a home page built for their role, with the numbers they need first.</p>
    <ul class="checks"><li><div>Cash, receivables and sales at a glance</div></li><li><div>Drill into any figure to see the entries behind it</div></li><li><div>Power BI reports on live data</div></li></ul></div>
  </div>

  <div class="tour-panel" role="tabpanel" id="panel-inv" aria-labelledby="tab-inv" hidden>
    <figure class="shot" style="margin:0" data-shot="@/images/inventory.png" data-alt="Business Central item list showing stock by location and reorder points">
      <div class="shot-bar"><b>Items</b><span>Example data</span></div>
      <div class="shot-body"><table class="mini">
        <thead><tr><th>No.</th><th>Description</th><th>Location</th><th class="n">On hand</th><th class="n">Reorder point</th><th class="n">Unit cost</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>1000</td><td>Steel shelf bracket</td><td>MAIN</td><td class="n">1,240</td><td class="n">400</td><td class="n">3.85</td><td><span class="pill">OK</span></td></tr>
          <tr><td>1010</td><td>Pallet wrap, 18 in</td><td>MAIN</td><td class="n">86</td><td class="n">120</td><td class="n">24.10</td><td><span class="pill low">Reorder</span></td></tr>
          <tr><td>1020</td><td>Hex bolt M10 (box)</td><td>EAST</td><td class="n">530</td><td class="n">200</td><td class="n">11.40</td><td><span class="pill">OK</span></td></tr>
          <tr><td>1030</td><td>Shipping carton, large</td><td>MAIN</td><td class="n">2,015</td><td class="n">800</td><td class="n">1.12</td><td><span class="pill">OK</span></td></tr>
          <tr><td>1040</td><td>Label roll, 4x6</td><td>EAST</td><td class="n">34</td><td class="n">60</td><td class="n">18.75</td><td><span class="pill low">Reorder</span></td></tr>
        </tbody></table></div>
    </figure>
    <div class="tour-copy"><h3>Stock, locations and item tracking</h3><p>See what you have, where it is and what it cost, across every warehouse and location.</p>
    <ul class="checks"><li><div>Stock by location and bin</div></li><li><div>Reorder points and planning suggestions</div></li><li><div>Lot and serial number tracking</div></li></ul></div>
  </div>

  <div class="tour-panel" role="tabpanel" id="panel-sales" aria-labelledby="tab-sales" hidden>
    <figure class="shot" style="margin:0" data-shot="@/images/sales-order.png" data-alt="Business Central sales order with customer details, order lines and totals">
      <div class="shot-bar"><b>Sales Order · SO-101009</b><span>Example data</span></div>
      <div class="shot-body">
        <div class="fields"><div><span>Customer</span><b>Northshore Supply</b></div><div><span>Order date</span><b>Oct 28, 2026</b></div><div><span>Ship from</span><b>MAIN</b></div><div><span>Status</span><b><span class="pill">Released</span></b></div></div>
        <table class="mini"><thead><tr><th>Item</th><th>Description</th><th class="n">Qty</th><th class="n">Unit price</th><th class="n">Line amount</th></tr></thead>
        <tbody><tr><td>1000</td><td>Steel shelf bracket</td><td class="n">400</td><td class="n">7.50</td><td class="n">3,000.00</td></tr>
        <tr><td>1020</td><td>Hex bolt M10 (box)</td><td class="n">120</td><td class="n">22.00</td><td class="n">2,640.00</td></tr>
        <tr><td>1030</td><td>Shipping carton, large</td><td class="n">1,000</td><td class="n">2.40</td><td class="n">2,400.00</td></tr></tbody></table>
        <div class="totals"><span>Subtotal <strong>8,040.00</strong></span><span>Tax <strong>965.00</strong></span><span>Total <strong>9,005.00</strong></span></div>
      </div>
    </figure>
    <div class="tour-copy"><h3>Customer orders and invoicing</h3><p>Go from quote to order to shipment to invoice without retyping anything.</p>
    <ul class="checks"><li><div>Prices, discounts and credit limits applied automatically</div></li><li><div>Stock checked as you enter lines</div></li><li><div>Post the invoice and the ledger updates</div></li></ul></div>
  </div>

  <div class="tour-panel" role="tabpanel" id="panel-wh" aria-labelledby="tab-wh" hidden>
    <figure class="shot" style="margin:0" data-shot="@/images/warehouse-pick.png" data-alt="Business Central warehouse pick with take and place lines by bin">
      <div class="shot-bar"><b>Warehouse Pick · PI-000142</b><span>Example data</span></div>
      <div class="shot-body">
        <div class="fields"><div><span>Source</span><b>SO-101009</b></div><div><span>Location</span><b>MAIN</b></div><div><span>Assigned to</span><b>Picker 2</b></div><div><span>Lines</span><b>6</b></div></div>
        <table class="mini"><thead><tr><th>Action</th><th>Item</th><th>Bin</th><th class="n">Qty to handle</th><th class="n">Qty handled</th></tr></thead>
        <tbody><tr><td>Take</td><td>1000 Steel shelf bracket</td><td>A-03-02</td><td class="n">400</td><td class="n">400</td></tr>
        <tr><td>Place</td><td>1000 Steel shelf bracket</td><td>SHIP-01</td><td class="n">400</td><td class="n">400</td></tr>
        <tr><td>Take</td><td>1020 Hex bolt M10 (box)</td><td>B-11-04</td><td class="n">120</td><td class="n">0</td></tr>
        <tr><td>Place</td><td>1020 Hex bolt M10 (box)</td><td>SHIP-01</td><td class="n">120</td><td class="n">0</td></tr></tbody></table>
      </div>
    </figure>
    <div class="tour-copy"><h3>Picking, shipping and inventory movements</h3><p>Warehouse staff get clear take-and-place instructions by bin, on a desktop or a handheld device.</p>
    <ul class="checks"><li><div>Receive, put away, pick and ship</div></li><li><div>Bin-level stock that stays accurate</div></li><li><div>Shipments post straight to the sales order</div></li></ul></div>
  </div>

  <div class="demo-video" id="demoVideo" data-src="@/images/demo.mp4" hidden>
    <h3>Watch a 90-second walkthrough</h3>
    <video controls preload="none" poster="@/images/demo-poster.jpg"><source src="@/images/demo.mp4" type="video/mp4">Your browser doesn't play this video.</video>
  </div>
  <p class="shot-note" id="shotNote" style="margin-top:20px">Screens shown with example data.</p>
</div>
</section>'''

FAQ_HOME = [
    ('What is Microsoft Dynamics 365 Business Central?', 'It’s Microsoft’s cloud ERP for small and midsize businesses. It brings accounting, inventory, sales, purchasing, warehousing and reporting into one system that works with Microsoft 365.', None),
    ('Is Business Central right for a distribution or inventory-heavy business?', 'For most small and midsize distributors, yes. It handles multi-location stock, purchasing, bins, picking and shipping. If your warehouse is very high-volume or complex, we’ll tell you whether an extension or Dynamics 365 Supply Chain Management fits better.', ('@/business-central/#fit', 'Is Business Central enough?')),
    ('How much does Business Central cost?', 'Licences are a monthly per-user subscription from Microsoft. Implementation is a one-time project quoted after a free discovery call. Our calculator estimates your licence cost in a minute.', ('@/licensing/', 'Estimate your costs')),
    ('How long does implementation take?', 'A focused finance and inventory rollout usually takes a few months. Projects with manufacturing, advanced warehousing or several integrations take longer. You get a timeline after discovery.', ('@/implementation/', 'How implementation works')),
    ('Can Business Central replace QuickBooks?', 'Yes. Companies usually move when they need proper inventory, multiple companies or better reporting. We handle the data migration.', ('@/data-migration/', 'Data migration')),
    ('Can Business Central integrate with Shopify?', 'Yes. Business Central has a Shopify connector, and we build other integrations through its APIs.', ('@/integrations/', 'Integrations')),
    ('Who will I actually work with?', 'Oleh Karnaukhov, the founder. Q84 Digital is senior-led, so the person who scopes your project is the person who delivers it.', ('@/#consultant', 'Meet the consultant')),
]

def faq_html(items):
    out = []
    for q, a, link in items:
        more = f' <a href="{link[0]}">{link[1]} →</a>' if link else ''
        out.append(f'<details><summary>{esc(q)}</summary><p>{esc(a)}{more}</p></details>')
    return '<div class="faq">' + ''.join(out) + '</div>'

def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in items]}

ORG_SCHEMA = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Q84 Digital",
    "url": URL, "email": EMAIL,
    "description": "Microsoft Dynamics 365 Business Central implementation, integration and support for distributors, manufacturers and inventory-driven businesses.",
    "areaServed": [{"@type": "Country", "name": "Canada"}, {"@type": "Country", "name": "United States"}],
    "address": {"@type": "PostalAddress", "addressLocality": "Vancouver", "addressRegion": "BC", "addressCountry": "CA"},
    "founder": {"@type": "Person", "name": "Oleh Karnaukhov", "jobTitle": "Founder and lead consultant"},
    "knowsAbout": ["Microsoft Dynamics 365 Business Central", "Dynamics 365 Supply Chain Management", "ERP implementation", "Warehouse management", "ERP integration"],
}
if CFG.get('phone'):
    ORG_SCHEMA['telephone'] = CFG['phone']

# ---------------------------------------------------------------- pages

PAGES = []
def add(path, nav, title, desc, body, schema=None):
    PAGES.append(dict(path=path, nav=nav, title=title, desc=desc, body=body, schema=schema or []))

photo = f'<img src="@/images/{esc(CFG["consultant_photo"])}" alt="Oleh Karnaukhov">' if CFG.get('consultant_photo') else 'OK'

HERO_IMG = next((f for f in ('hero-flow.webp', 'hero-flow.png', 'hero-flow.jpg') if os.path.exists(os.path.join(ROOT, 'images', f))), None)
HERO_CLASS = 'hero-split' if HERO_IMG else ''
HERO_ART = (f'<figure class="hero-art"><img src="@/images/{HERO_IMG}" alt="Illustration of an order moving from sales order to warehouse, shipment, invoice and reporting" width="1024" height="1024" fetchpriority="high"></figure>' if HERO_IMG else '')

# HOME
add('', 'home',
    'Business Central for Distributors & Manufacturers | Q84 Digital',
    'Senior-led Microsoft Dynamics 365 Business Central implementation, integration and support for growing distributors, manufacturers and inventory-driven businesses.',
    f'''<section class="hero"><div class="wrap">
  <div class="{HERO_CLASS}"><div class="hero-center">
    <span class="eyebrow">Microsoft Dynamics 365 Business Central consulting</span>
    <h1>Business Central implementation for businesses that move products</h1>
    <p class="lede">We help growing distributors, manufacturers and inventory-driven businesses implement Business Central, connect their operations and replace disconnected systems.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="@/contact/">Book a free consultation</a><a class="btn btn-ghost" href="@/business-central/">Explore Business Central</a></div>
  </div>{HERO_ART}</div>
  <div class="trust"><span><strong>10+ years</strong> of Microsoft Dynamics experience</span><span><strong>Senior-led:</strong> you work with the consultant who delivers</span><span><strong>Supply chain</strong> and warehouse background</span></div>
  <div class="grid g3 hero-cards">
    <a class="card" href="@/implementation/">{icon('ledger')}<h3>ERP implementation</h3><p>Finance, inventory and sales set up around how your business runs.</p><span class="more">How it works →</span></a>
    <a class="card" href="@/industries/distribution/">{icon('warehouse')}<h3>Inventory &amp; warehouse</h3><p>Accurate stock, purchasing, picking and shipping across locations.</p><span class="more">For distributors →</span></a>
    <a class="card" href="@/integrations/">{icon('link')}<h3>Integrations</h3><p>Shopify, shipping, CRM and Power BI connected to Business Central.</p><span class="more">See integrations →</span></a>
  </div>
</div></section>

<section class="band" id="consultant"><div class="wrap profile">
  <div class="profile-card">
    <div class="avatar" aria-hidden="true">{photo}</div>
    <div><h3 style="font-size:1.25rem">Oleh Karnaukhov</h3><p class="role">Founder and lead consultant</p></div>
    <div class="stat"><strong>10+ years</strong><span>Microsoft Dynamics consulting</span></div>
    <div class="stat"><strong>Senior-led</strong><span>No hand-off to junior staff</span></div>
    <a class="btn btn-primary" href="@/contact/" style="width:100%">Talk to Oleh</a>
  </div>
  <div class="stack" style="gap:20px">
    <span class="eyebrow">Meet the consultant behind Q84 Digital</span>
    <h2>ERP expertise that goes beyond setup screens</h2>
    <p class="lede">Oleh Karnaukhov is a senior Microsoft Dynamics consultant with more than 10 years of experience delivering ERP and supply chain projects, working with Microsoft partners and consulting firms on implementations for their clients.</p>
    <p class="lede">Q84 Digital brings that operations experience to Business Central projects for growing businesses, with one difference: you work directly with him from first call to go-live.</p>
    <div><h3 style="margin-bottom:12px">Experience across</h3>
    <ul class="tags"><li>Dynamics 365 Supply Chain Management</li><li>Warehouse management</li><li>Transportation management</li><li>Inventory and distribution processes</li><li>Dynamics 365 Customer Engagement (CRM)</li><li>Dynamics 365 Field Service</li><li>ERP integrations and automation</li><li>Business process design</li></ul></div>
  </div>
</div></section>

{TOUR}

<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Who we help</span><h2>Built for businesses where inventory is the business</h2></div>
  <div class="grid g3">
    <a class="card" href="@/industries/distribution/">{icon('truck')}<span class="tag">Wholesale distribution</span><h3>Stock you can trust</h3><p>Counts that drift, purchasing done by hand and systems that don't talk to each other.</p><span class="more">Distribution →</span></a>
    <a class="card" href="@/industries/manufacturing/">{icon('factory')}<span class="tag">Manufacturing</span><h3>See production clearly</h3><p>Little visibility into production, hard-to-trace costs and planning that lives in someone's head.</p><span class="more">Manufacturing →</span></a>
    <a class="card" href="@/integrations/">{icon('shop')}<span class="tag">E-commerce &amp; retail</span><h3>One view of every order</h3><p>Online orders, stock and accounting kept in separate places and reconciled by hand.</p><span class="more">Shopify and integrations →</span></a>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we deliver</span><h2>From first conversation to everyday support</h2></div>
  <div class="svc">
    <a href="@/implementation/"><h3>Implementation</h3><p>Business Central set up around your processes, from chart of accounts to go-live.</p><span class="more">Implementation →</span></a>
    <a href="@/data-migration/"><h3>Data migration</h3><p>Clean, verified data moved from QuickBooks, Sage, Dynamics NAV or spreadsheets.</p><span class="more">Data migration →</span></a>
    <a href="@/integrations/"><h3>Integrations &amp; automation</h3><p>Business Central connected to e-commerce, shipping, CRM and Power BI.</p><span class="more">Integrations →</span></a>
    <a href="@/licensing/"><h3>Licensing &amp; advice</h3><p>The right licence mix and a clear view of total cost before you commit.</p><span class="more">Licensing &amp; pricing →</span></a>
    <a href="@/support/"><h3>Ongoing support</h3><p>Fixes, improvements and training once you're live, hourly or monthly.</p><span class="more">Support →</span></a>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Implementation examples</span><h2>What a project looks like</h2><p class="lede">Three typical starting points and how we'd approach each one.</p></div>
  {EXAMPLES}
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">How we work</span><h2>A structured path to go-live</h2></div>
  <ol class="steps">
    <li><h3>Discovery</h3><p>Review your systems, processes and goals.</p></li>
    <li><h3>Design</h3><p>Agree scope, setup, integrations and plan.</p></li>
    <li><h3>Build</h3><p>Configure, migrate data, build approved extensions.</p></li>
    <li><h3>Testing</h3><p>Run real processes end to end and train your team.</p></li>
    <li><h3>Go-live</h3><p>Switch over with hands-on help afterwards.</p></li>
  </ol>
  <p style="margin-top:28px"><a class="more" href="@/implementation/">See each phase and what you receive →</a></p>
</div></section>

<section class="band" id="fit"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Choosing the right ERP</span><h2>Not sure Business Central is enough for your operations?</h2>
  <p class="lede">Business Central has solid warehouse features, but it isn't the same as the advanced warehouse management in Dynamics 365 Supply Chain Management. With hands-on experience in both, we'll help you pick the right fit instead of selling you one product.</p></div>
  {FIT}
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Pricing</span><h2>Know what Business Central will cost</h2><p class="lede">Licences are a monthly Microsoft subscription. Implementation is a one-time project. Support is hourly or monthly.</p></div>
  <div class="grid g3">
    <div class="card"><span class="tag">From Microsoft</span><h3>Licences</h3><p>Essentials is US$80 and Premium US$110 per full user per month at Microsoft's US list prices.</p></div>
    <div class="card"><span class="tag">One-time</span><h3>Implementation</h3><p>Quoted after discovery, based on modules, data, integrations and companies.</p></div>
    <div class="card"><span class="tag">Ongoing</span><h3>Support</h3><p>Pay as you go, or a monthly plan with included hours.</p></div>
  </div>
  <p style="margin-top:28px"><a class="btn btn-primary" href="@/licensing/#calculator">Estimate your costs</a></p>
</div></section>

<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">FAQ</span><h2>Common questions</h2><p class="lede">Don't see yours? <a href="@/contact/">Ask directly.</a></p></div>
  {faq_html(FAQ_HOME)}
</div></section>
{cta()}''', [ORG_SCHEMA, faq_schema(FAQ_HOME)])

# BUSINESS CENTRAL
add('business-central/', 'business-central',
    'What Is Business Central? Features & Fit | Q84 Digital',
    'What Business Central does, its core features for finance, inventory, sales, purchasing and warehousing, and how to tell whether it fits your operations.',
    page_head('Business Central', 'Business Central', 'Microsoft Dynamics 365 Business Central',
              'One cloud ERP for finance, inventory, sales, purchasing and warehousing, built for small and midsize companies and connected to Microsoft 365.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Core features</span><h2>One system for the whole business</h2></div>
  <div class="grid g3">
    <div class="plain">{icon('ledger')}<h3>Financial management</h3><p>General ledger, payables, receivables, bank reconciliation, dimensions and financial reporting.</p></div>
    <div class="plain">{icon('box')}<h3>Inventory management</h3><p>Items, variants, locations, costing methods, reorder points and planning suggestions.</p></div>
    <div class="plain">{icon('receipt')}<h3>Sales</h3><p>Quotes, orders, invoicing, pricing, discounts, credit limits and customer management.</p></div>
    <div class="plain">{icon('cart')}<h3>Purchasing</h3><p>Purchase orders, vendor management, receiving, approvals and drop shipments.</p></div>
    <div class="plain">{icon('warehouse')}<h3>Warehouse operations</h3><p>Receipts, put-away, picking, shipping, bins and inventory movements.</p></div>
    <div class="plain">{icon('factory')}<h3>Manufacturing (Premium)</h3><p>Bills of materials, routings, production orders and capacity planning.</p></div>
    <div class="plain">{icon('pie')}<h3>Reporting &amp; analytics</h3><p>Role-based home pages, Excel analysis and Power BI on live data.</p></div>
    <div class="plain">{icon('link')}<h3>Integrations</h3><p>A Shopify connector, Microsoft 365 and Dataverse links, and open APIs.</p></div>
    <div class="plain">{icon('tools')}<h3>Extensions</h3><p>Apps from Microsoft AppSource and custom AL extensions for specific needs.</p></div>
  </div>
</div></section>
<section class="band" id="fit"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Choosing the right ERP</span><h2>Is Business Central enough for your operations?</h2>
  <p class="lede">For most small and midsize distributors it is. For very high-volume or complex warehousing, an extension or Dynamics 365 Supply Chain Management may be a better fit. Because we've worked hands-on with both, we can give you a straight answer.</p></div>
  {FIT}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Moving from QuickBooks?</span><h2>Signs you've outgrown entry-level accounting</h2></div>
  {checks(['<strong>Inventory lives in spreadsheets.</strong> Stock counts and costs are tracked outside your accounting system.', '<strong>Several companies or locations.</strong> Consolidation and inter-company work take days.', '<strong>Reporting is manual.</strong> Month-end means exporting and rebuilding reports in Excel.', '<strong>Too many disconnected tools.</strong> Orders, stock and accounting are reconciled by hand.'])}
</div></section>
{cta('See whether Business Central fits', 'Tell us how your business runs today. We’ll tell you honestly whether Business Central is the right choice.')}''')

# IMPLEMENTATION
add('implementation/', 'implementation',
    'Business Central Implementation Services | Q84 Digital',
    'A structured Business Central implementation: discovery, design, build, data migration, testing, training and go-live support, led by a senior Dynamics consultant.',
    page_head('Implementation', 'Services / Implementation', 'Business Central implementation',
              'A structured rollout that gets your team working in Business Central with clean data, tested processes and support after go-live.') + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Common problems</span><h2>Why ERP projects go sideways</h2><p class="lede">Most failed implementations fail for the same few reasons. Our method is built to prevent each one.</p></div>
  {checks(['<strong>Vague scope.</strong> Nobody agrees on what “done” means, so the budget keeps moving.', '<strong>Dirty data.</strong> Old records are loaded as-is and cause problems from day one.', '<strong>Too much customization.</strong> Custom code replaces standard features and makes upgrades harder.', '<strong>Rushed testing.</strong> Real processes aren’t tested end to end before go-live.', '<strong>Untrained users.</strong> People go back to spreadsheets because nobody showed them how.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Our method</span><h2>Phases and what each one delivers</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Phase</th><th>What happens</th><th>You receive</th></tr></thead>
    <tbody>
      <tr><td>1. Discovery</td><td>Workshops on finance, sales, purchasing, inventory, warehouse and reporting.</td><td>Current-state summary and requirements list</td></tr>
      <tr><td>2. Solution design</td><td>Each requirement mapped to standard features, an AppSource app or an extension.</td><td>Solution design, project plan and fixed scope</td></tr>
      <tr><td>3. Build</td><td>Setups, posting groups and dimensions configured; approved extensions and integrations built.</td><td>Configured test environment</td></tr>
      <tr><td>4. Data migration</td><td>Master data and opening balances mapped, cleaned, loaded and reconciled.</td><td>Signed-off reconciliation</td></tr>
      <tr><td>5. Testing &amp; training</td><td>Your team runs real scenarios end to end. Role-based training.</td><td>Test sign-off and training guides</td></tr>
      <tr><td>6. Go-live &amp; support</td><td>Cutover plan, first period close and hands-on help.</td><td>Live system and support handover</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Examples</span><h2>What an implementation looks like</h2></div>
  {EXAMPLES}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Timeline &amp; cost</span><h2>What drives the size of a project</h2><p class="lede">You get a fixed scope and estimate after discovery, based on your business rather than a guess. <a href="@/licensing/#calculator">Try the cost estimator.</a></p></div>
  {checks(['<strong>Modules in scope.</strong> Finance only, or also inventory, warehousing and manufacturing.', '<strong>Companies and locations.</strong> Multi-entity and multi-warehouse setups take more work.', '<strong>Data volume and quality.</strong> Clean data loads faster than messy data.', '<strong>Integrations.</strong> Each connected system adds design and testing time.', '<strong>Custom development.</strong> Extensions are scoped and estimated separately.'])}
</div></section>
{cta('Planning a Business Central project?')}''')

# LICENSING
add('licensing/', 'licensing',
    'Business Central Pricing & Cost Calculator | Q84 Digital',
    'Business Central licence prices for Essentials, Premium and Team Members, a cost calculator for your users, and what drives implementation and support costs.',
    page_head('Licensing', 'Services / Licensing &amp; pricing', 'Business Central licensing and pricing',
              'What you’ll pay Microsoft for licences, what drives implementation cost, and a quick calculator for your own numbers.', button=False) + '''
<section style="padding-top:32px" id="calculator"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Cost estimator</span><h2>Estimate your Business Central costs</h2></div>
  <form class="calc" id="calc" onsubmit="return false">
    <div class="stack" style="gap:22px">
      <fieldset><legend>Licence plan</legend><div class="choice">
        <label><input type="radio" name="plan" value="essentials" checked> Essentials</label>
        <label><input type="radio" name="plan" value="premium"> Premium</label></div></fieldset>
      <div class="row">
        <div class="field"><label for="c-full">Full users</label><input id="c-full" type="number" min="0" max="999" value="8" inputmode="numeric"><span class="hint">People who post orders, invoices or journals</span></div>
        <div class="field"><label for="c-team">Team Members</label><input id="c-team" type="number" min="0" max="999" value="5" inputmode="numeric"><span class="hint">People who mainly view, approve or update records</span></div>
      </div>
      <div class="row">
        <div class="field"><label for="c-companies">Companies</label><input id="c-companies" type="number" min="1" max="99" value="1" inputmode="numeric"></div>
        <div class="field"><label for="c-int">Integrations needed</label><input id="c-int" type="number" min="0" max="20" value="1" inputmode="numeric"><span class="hint">e.g. Shopify, shipping, CRM</span></div>
      </div>
      <div class="field"><label for="c-from">Moving from</label>
        <select id="c-from" name="from"><option value="qb">QuickBooks</option><option value="sage">Sage</option><option value="nav">Dynamics NAV</option><option value="other-erp">Another ERP</option><option value="sheets">Spreadsheets</option><option value="none">Nothing yet</option></select></div>
      <fieldset><legend>Areas in scope</legend><div class="choice">
        <label><input type="checkbox" name="mod" data-w="1" data-label="Inventory and purchasing" checked> Inventory &amp; purchasing</label>
        <label><input type="checkbox" name="mod" data-w="2" data-label="Warehouse processes"> Warehouse</label>
        <label><input type="checkbox" name="mod" data-w="3" data-label="Manufacturing" data-premium> Manufacturing</label>
        <label><input type="checkbox" name="mod" data-w="2" data-label="Service management" data-premium> Service management</label></div></fieldset>
    </div>
    <div class="calc-out" aria-live="polite">
      <div><div class="sub">Microsoft licences per month</div><div class="big" id="o-monthly">$0</div><div class="sub"><span id="o-annual">$0</span> per year</div></div>
      <div class="line"><span>Full users</span><span id="o-full"></span></div>
      <div class="line"><span>Team Members</span><span id="o-team"></span></div>
      <p class="sub" id="o-hint" hidden style="color:inherit">Manufacturing and service management need the Premium plan.</p>
      <div class="line" style="display:block"><div class="sub">Likely implementation size</div><div style="font:600 1.4rem var(--display)" id="o-size"></div><p class="sub" id="o-size-desc"></p></div>
      <div><div class="sub" style="margin-bottom:6px">What drives your scope</div><ul id="o-drivers"></ul></div>
      <a class="btn btn-primary" href="@/contact/">Get a quote for implementation</a>
      <p class="sub">Licence figures use Microsoft's US list prices (per user per month, annual commitment) effective November 2025. Canadian dollar prices differ. Implementation is quoted after a free discovery call.</p>
    </div>
  </form>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Licence types</span><h2>Choosing the right licences</h2><p class="lede">Most companies combine a few full users with lower-cost Team Members licences for people who only view data or do light tasks. All full users in a company must be on the same plan.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Licence</th><th>US list price</th><th>Who it's for</th><th>Typical use</th></tr></thead>
    <tbody>
      <tr><td>Essentials</td><td>$80 / user / month</td><td>Full users</td><td>Finance, sales, purchasing, inventory, warehousing, projects</td></tr>
      <tr><td>Premium</td><td>$110 / user / month</td><td>Full users who need more</td><td>Everything in Essentials, plus manufacturing and service management</td></tr>
      <tr><td>Team Members</td><td>$8 / user / month</td><td>Light users</td><td>View data, approve documents, update basic records</td></tr>
    </tbody></table></div>
  <p class="note" style="margin-top:20px">Prices are Microsoft's US list prices effective November 1, 2025, and may change. We confirm current pricing in your currency in every estimate. Microsoft licence fees are separate from our consulting fees.</p>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Total cost</span><h2>The parts of a Business Central budget</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Cost</th><th>Type</th><th>What it depends on</th></tr></thead>
    <tbody>
      <tr><td>Licences</td><td>Monthly</td><td>Plan and number of full and light users</td></tr>
      <tr><td>Implementation</td><td>One-time</td><td>Modules, companies, processes and custom work</td></tr>
      <tr><td>Data migration</td><td>One-time</td><td>Source systems, data volume and data quality</td></tr>
      <tr><td>Integrations</td><td>One-time plus upkeep</td><td>Number of systems and how complex the data flow is</td></tr>
      <tr><td>Add-on apps</td><td>Monthly</td><td>AppSource apps you choose, priced by their publishers</td></tr>
      <tr><td>Support</td><td>Hourly or monthly</td><td>How much help you want after go-live</td></tr>
    </tbody></table></div>
</div></section>
''' + cta('Get a cost estimate for your business', 'Share a few details and we’ll come back with licensing and implementation ranges.'))

# DATA MIGRATION
add('data-migration/', 'data-migration',
    'Business Central Data Migration | Q84 Digital',
    'Move to Business Central with clean, reconciled data. Migration from QuickBooks, Sage, Dynamics NAV, other ERPs and spreadsheets.',
    page_head('Data migration', 'Services / Data migration', 'Business Central data migration',
              'Move customers, vendors, items, open documents and balances into Business Central, then reconcile so your numbers match on day one.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where you're coming from</span><h2>Systems we migrate from</h2></div>
  <div class="grid g4">
    <div class="card"><span class="tag">From</span><h3>QuickBooks</h3><p>Customers, vendors, items, open receivables and payables, and trial balance.</p></div>
    <div class="card"><span class="tag">From</span><h3>Sage</h3><p>Master data, open transactions and historical balances.</p></div>
    <div class="card"><span class="tag">From</span><h3>Dynamics NAV</h3><p>Upgrade or re-implement, depending on version and custom code.</p></div>
    <div class="card"><span class="tag">From</span><h3>Spreadsheets &amp; other ERPs</h3><p>Structured templates, cleansing and validation before loading.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Our process</span><h2>Five steps to clean data</h2></div>
  <ol class="steps">
    <li><h3>Map</h3><p>Match old fields and codes to Business Central.</p></li>
    <li><h3>Cleanse</h3><p>Remove duplicates, fix gaps and retire old records.</p></li>
    <li><h3>Load</h3><p>Trial loads into a test company first.</p></li>
    <li><h3>Validate</h3><p>Your team checks records and spot-tests transactions.</p></li>
    <li><h3>Reconcile</h3><p>Balances matched to the old system and signed off.</p></li>
  </ol>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">What moves</span><h2>What we usually migrate</h2><p class="lede">We agree with you how much history to bring over. Often it's open items and balances, with older history kept for reference.</p></div>
  {checks(['Customers, vendors, items and contacts', 'Chart of accounts and opening balances', 'Open sales and purchase orders', 'Open receivables and payables', 'Stock on hand by location, with costs'])}
</div></section>
{cta('Planning your move to Business Central?')}''')

# INTEGRATIONS
add('integrations/', 'integrations',
    'Business Central Integrations & Shopify | Q84 Digital',
    'Connect Business Central to Shopify, shipping, CRM and Power BI, and extend it with AL extensions and Power Automate, built to Microsoft’s extension model.',
    page_head('Integrations', 'Services / Integrations &amp; customization', 'Business Central integrations and customization',
              'Connect Business Central to the tools you already use, and extend it where standard features don’t cover your process.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we build</span><h2>Connected systems, less manual entry</h2></div>
  <div class="grid g3">
    <div class="card">{icon('tools')}<span class="tag">Extensions</span><h3>AL development</h3><p>Custom fields, pages, reports and business logic built as extensions.</p></div>
    <div class="card">{icon('link')}<span class="tag">APIs</span><h3>System integrations</h3><p>Data sync with other business systems through Business Central's APIs.</p></div>
    <div class="card">{icon('shop')}<span class="tag">Commerce</span><h3>Shopify &amp; e-commerce</h3><p>Orders, items, stock and pricing kept in step with your online store.</p></div>
    <div class="card">{icon('truck')}<span class="tag">Logistics</span><h3>Shipping &amp; fulfillment</h3><p>Carrier rates, labels and tracking connected to warehouse shipments.</p></div>
    <div class="card">{icon('chart')}<span class="tag">Automation</span><h3>Power Automate</h3><p>Approvals, notifications and routine tasks handled automatically.</p></div>
    <div class="card">{icon('pie')}<span class="tag">Reporting</span><h3>Power BI</h3><p>Financial and operational dashboards on live Business Central data.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our approach</span><h2>Configure first, customize only when it pays off</h2><p class="lede">Every custom line of code is something to maintain. We check whether standard features or an existing app can do the job before we build anything.</p></div>
  {checks(['<strong>Fit check.</strong> Standard setup, AppSource app or custom extension: we compare the options with you.', '<strong>Built for updates.</strong> Extensions follow Microsoft’s extension model, which keeps Business Central updates much smoother. We still test custom work against each major release.', '<strong>Documented.</strong> You get notes on what was built and how it works.', '<strong>Tested.</strong> Integrations are tested with realistic data volumes and error cases.'])}
</div></section>
<section><div class="wrap"><div class="note">Also running Dynamics 365 Sales, Customer Service or Field Service? We work across the Dynamics 365 family and can connect Business Central with Dataverse and your CRM.</div></div></section>
{cta('Have a system that needs to connect?', 'Tell us what you use today. We’ll suggest the simplest reliable way to make it work with Business Central.')}''')

# SUPPORT
add('support/', 'support',
    'Business Central Support Services | Q84 Digital',
    'Business Central support from a senior consultant: troubleshooting, configuration improvements, training, integration support and enhancements. Hourly or monthly.',
    page_head('Support', 'Services / Support', 'Business Central support',
              'Already using Business Central? Get help fixing issues, improving your setup and training your team, from a consultant who knows the system well.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we help with</span><h2>Support that goes beyond tickets</h2></div>
  <div class="grid g3">
    <div class="plain">{icon('support')}<h3>Troubleshooting</h3><p>Posting errors, setup problems, failed jobs and unexpected results.</p></div>
    <div class="plain">{icon('tools')}<h3>Configuration improvements</h3><p>Cleaner posting groups, dimensions, approvals and number series.</p></div>
    <div class="plain">{icon('receipt')}<h3>User training</h3><p>Role-based sessions for new staff or new processes.</p></div>
    <div class="plain">{icon('chart')}<h3>Process reviews</h3><p>Find manual steps and slow spots, and fix them.</p></div>
    <div class="plain">{icon('link')}<h3>Integration support</h3><p>Monitor and fix connections with other systems.</p></div>
    <div class="plain">{icon('box')}<h3>Enhancements</h3><p>Small extensions, reports and changes as your business grows.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Ways to work with us</span><h2>Choose the support model that fits</h2></div>
  <div class="grid g2">
    <div class="card"><span class="tag">Flexible</span><h3>Hourly consulting</h3><p>Pay only for the time you use. Good for occasional questions and one-off fixes.</p><a class="more" href="@/contact/">Ask about hourly support →</a></div>
    <div class="card"><span class="tag">Predictable</span><h3>Monthly support plan</h3><p>A set number of hours each month, priority response and a regular check-in on your system.</p><a class="more" href="@/contact/">Ask about monthly plans →</a></div>
  </div>
</div></section>
{cta('Need help with Business Central?', 'Describe the issue and we’ll get back to you with next steps within one business day.')}''')

# INDUSTRIES
add('industries/distribution/', 'distribution',
    'Business Central for Wholesale Distributors | Q84 Digital',
    'Business Central for wholesale distribution: accurate multi-location inventory, purchasing, warehouse picking and shipping, and landed costs, from a supply chain specialist.',
    page_head('Distribution', 'Industries / Wholesale distribution', 'Business Central for wholesale distributors',
              'Accurate stock, faster purchasing and a warehouse that ships the right order the first time.') + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Common challenges</span><h2>Where distributors lose time and margin</h2></div>
  {checks(['<strong>Inventory you can’t trust.</strong> System counts drift from what’s on the shelf.', '<strong>Manual purchasing.</strong> Buyers reorder from memory or spreadsheets.', '<strong>Picking errors.</strong> Wrong items or quantities shipped, and costly returns.', '<strong>Hidden costs.</strong> Freight and duty aren’t added to item costs, so margins look better than they are.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How Business Central helps</span><h2>Built around the order-to-cash and procure-to-pay flow</h2></div>
  <div class="grid g3">
    <div class="card">{icon('box')}<h3>Multi-location inventory</h3><p>Stock by location and bin, transfers, cycle counts and item tracking.</p></div>
    <div class="card">{icon('cart')}<h3>Purchasing &amp; replenishment</h3><p>Reorder points, planning suggestions and vendor lead times turned into purchase orders.</p></div>
    <div class="card">{icon('warehouse')}<h3>Warehouse processes</h3><p>Receiving, put-away, picking and shipping documents by bin.</p></div>
    <div class="card">{icon('truck')}<h3>Shipping</h3><p>Shipment documents, carrier integrations and tracking.</p></div>
    <div class="card">{icon('receipt')}<h3>Landed cost</h3><p>Freight, duty and handling charged to the items they belong to.</p></div>
    <div class="card">{icon('pie')}<h3>Margin reporting</h3><p>Profit by item, customer and salesperson on live data.</p></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Example workflow</span><h2>A typical order, start to finish</h2></div>
  <ol class="steps">
    <li><h3>Order</h3><p>Sales order entered with live stock and pricing.</p></li>
    <li><h3>Release</h3><p>Order released to the warehouse.</p></li>
    <li><h3>Pick</h3><p>Pick list created by bin and handled.</p></li>
    <li><h3>Ship</h3><p>Shipment posted, stock reduced.</p></li>
    <li><h3>Invoice</h3><p>Invoice posted, ledger updated.</p></li>
  </ol>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Right-sized</span><h2>Is Business Central enough for your warehouse?</h2></div>
  {FIT}
</div></section>
{cta('Talk to a distribution ERP specialist')}''')

add('industries/manufacturing/', 'manufacturing',
    'Business Central for Manufacturers | Q84 Digital',
    'Business Central Premium for small and midsize manufacturers: bills of materials, production orders, material planning and product costing.',
    page_head('Manufacturing', 'Industries / Manufacturing', 'Business Central for manufacturers',
              'Plan production, control materials and know what each product really costs to make.') + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Common challenges</span><h2>What holds growing manufacturers back</h2></div>
  {checks(['<strong>No production visibility.</strong> Order status lives on the shop floor, not in the system.', '<strong>Costs worked out in spreadsheets.</strong> Material and labour costs are estimates.', '<strong>Material shortages.</strong> Components run out because demand isn’t planned.', '<strong>Disconnected systems.</strong> Production, stock and accounting don’t share data.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How Business Central helps</span><h2>Manufacturing features in Business Central Premium</h2></div>
  <div class="grid g3">
    <div class="card">{icon('ledger')}<h3>Bills of materials</h3><p>Multi-level BOMs with versions and component substitutes.</p></div>
    <div class="card">{icon('factory')}<h3>Production orders</h3><p>Planned, released and finished orders with consumption and output.</p></div>
    <div class="card">{icon('chart')}<h3>Material planning</h3><p>Planning worksheets that suggest what to buy and make, and when.</p></div>
    <div class="card">{icon('tools')}<h3>Routings &amp; capacity</h3><p>Work centres, machine centres and capacity planning.</p></div>
    <div class="card">{icon('receipt')}<h3>Product costing</h3><p>Standard or actual costs with variance reporting.</p></div>
    <div class="card">{icon('box')}<h3>Inventory &amp; tracking</h3><p>Lot and serial tracking from components to finished goods.</p></div>
  </div>
</div></section>
<section><div class="wrap"><div class="note">Manufacturing features need the Business Central Premium licence. <a href="@/licensing/#calculator">Estimate your licence cost.</a></div></div></section>
{cta('Talk about your production processes')}''')

# CONTACT
booking_block = ''
if CFG.get('booking_url'):
    booking_block = f'''<div class="card"><span class="tag">Fastest</span><h3>Book a 30-minute call</h3><p>Pick a time that suits you on my calendar.</p><a class="btn btn-primary" href="{esc(CFG['booking_url'])}" data-booking target="_blank" rel="noopener">Choose a time</a></div>
<p class="or">or send a message</p>'''
phone_card = f'<div class="card"><span class="tag">Phone</span><p class="mono" style="color:var(--ink);user-select:all">{esc(CFG["phone"])}</p></div>' if CFG.get('phone') else ''
add('contact/', 'contact',
    'Book a Free Business Central Consultation | Q84 Digital',
    'Book a free, no-obligation Business Central consultation with Q84 Digital. Talk directly with the senior consultant who would deliver your project.',
    page_head('Contact', 'Book a consultation', 'Book a free consultation',
              'Tell us a little about your business. We’ll reply within one business day to set up a 30-minute call.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap split">
  <div class="stack" style="gap:20px">
    {booking_block}
    <form id="contactForm" novalidate>
      <div class="row">
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required><span class="err" id="e-name" hidden>Enter your name so we know who to reply to.</span></div>
        <div class="field"><label for="f-email">Business email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err" id="e-email" hidden>Enter an email address like name@company.com.</span></div>
      </div>
      <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" autocomplete="organization" required><span class="err" id="e-company" hidden>Enter your company name.</span></div>
      <div class="field"><label for="f-topic">What are you looking for?</label>
        <select id="f-topic" name="topic"><option>A new Business Central implementation</option><option>Pricing or licensing advice</option><option>Data migration</option><option>Integrations or customization</option><option>Support for an existing system</option><option>Help choosing an ERP</option></select></div>
      <div class="field"><label for="f-msg">Brief description <span class="hint">(optional)</span></label><textarea id="f-msg" name="message"></textarea></div>
      <div style="position:absolute;left:-9999px" aria-hidden="true"><label for="f-gotcha">Leave this empty</label><input id="f-gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <div><button class="btn btn-primary" type="submit">Request consultation</button></div>
      <p class="hint" id="formStatus" role="status" hidden></p>
    </form>
    <div class="sent" id="sent" hidden role="status"><h3>Thanks, your request is in</h3><p>We'll reply within one business day to book your consultation.</p></div>
  </div>
  <aside class="contact-side">
    <div class="card"><span class="tag">What to expect</span><h3>A 30-minute call with Oleh</h3><p>We'll talk through your systems, your goals and whether Business Central is a good fit. No obligation and no sales script.</p></div>
    <div class="card"><span class="tag">Email</span><p class="mono" style="color:var(--ink);user-select:all">{esc(EMAIL)}</p></div>
    {phone_card}
    <div class="card"><span class="tag">Location</span><p>Vancouver, British Columbia. Working with clients across Canada and the United States.</p></div>
  </aside>
</div></section>''')

# PRIVACY
legal_line = f' Q84 Digital is operated by {esc(CFG["legal_name"])}.' if CFG.get('legal_name') else ''
analytics_line = ('<p>We use Google Analytics to understand how visitors use this site, such as which pages are viewed. It sets cookies and collects information like your approximate location and device type. It does not tell us who you are.</p>'
                  if CFG.get('ga_id') else '<p>This site does not currently use analytics or advertising cookies.</p>')
add('privacy/', 'privacy', 'Privacy Policy | Q84 Digital',
    'How Q84 Digital collects, uses and protects personal information submitted through this website.',
    page_head('Privacy', 'Privacy', 'Privacy policy', f'Last updated {date.today().strftime("%B %-d, %Y")}.', button=False) + f'''
<section style="padding-top:24px"><div class="wrap prose">
<p>This policy explains how Q84 Digital handles personal information you share through this website.{legal_line}</p>
<h2>What we collect</h2><p>When you request a consultation we collect the details you enter: your name, business email, company, the topic you choose and any message you write.</p>
<h2>How we use it</h2><p>We use your information only to reply to your request, arrange a consultation and follow up about your project. We don't sell or rent it, and we don't add you to marketing lists without your consent.</p>
<h2>Analytics</h2>{analytics_line}
<h2>Sharing</h2><p>We share information only with service providers that help us run this website and handle email, and only as needed to provide those services, or where the law requires it.</p>
<h2>Retention and your rights</h2><p>We keep enquiries for as long as needed to respond and manage any resulting work. You can ask to see, correct or delete your information at any time by emailing <span style="user-select:all">{esc(EMAIL)}</span>. Under Canada's PIPEDA you can also contact the Office of the Privacy Commissioner of Canada.</p>
</div></section>''')

# ---------------------------------------------------------------- render

def analytics():
    if not CFG.get('ga_id'):
        return ''
    gid = esc(CFG['ga_id'])
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{gid}');</script>'''

FAVICON = "data:image/svg+xml," + re.sub(r'\s+', ' ', '''<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%232563EB'/><text x='32' y='41' font-family='Arial,sans-serif' font-size='24' font-weight='700' fill='white' text-anchor='middle'>Q84</text></svg>''')

def render(p):
    canonical = URL + p['path']
    schema = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in p['schema'])
    verify = f'<meta name="google-site-verification" content="{esc(CFG["gsc_verification"])}">\n' if CFG.get('gsc_verification') else ''
    client = json.dumps({'email': EMAIL, 'formEndpoint': CFG.get('form_endpoint', '')})
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Q84 Digital">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
{verify}<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&family=Open+Sans:wght@400;600&display=swap">
<link rel="stylesheet" href="@/assets/site.css?v={CSS_V}">
{analytics()}{schema}<script>window.Q84={client};</script>
</head>
<body>
{header(p['nav'])}
<main id="main">
{p['body']}
</main>
{footer()}
<script src="@/assets/site.js?v={JS_V}" defer></script>
</body>
</html>
'''
    return doc.replace('@/', BASE)

for p in PAGES:
    out = os.path.join(ROOT, p['path'], 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(render(p))

# 404
nf = dict(path='404.html', nav='', title='Page not found | Q84 Digital', desc='This page could not be found.',
          schema=[], body=page_head('', 'Page not found', 'We couldn’t find that page',
                                    'The link may be out of date. Try the homepage or book a consultation.') )
html404 = render(nf).replace(f'<link rel="canonical" href="{URL}404.html">\n', '<meta name="robots" content="noindex">\n')
open(os.path.join(ROOT, '404.html'), 'w').write(html404)

# sitemap + robots
urls = ''.join(f'<url><loc>{URL}{p["path"]}</loc><lastmod>{TODAY}</lastmod></url>' for p in PAGES)
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
rule = 'Allow: /' if CFG.get('allow_indexing', True) else 'Disallow: /'
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\n{rule}\n\nSitemap: {URL}sitemap.xml\n')
print(f'Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt')
