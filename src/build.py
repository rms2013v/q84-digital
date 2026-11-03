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

MS_PRICING = 'https://www.microsoft.com/en-us/dynamics-365/products/business-central/pricing'
_pc = date.fromisoformat(CFG.get('prices_checked') or TODAY)
PRICES_CHECKED = f'<time datetime="{_pc.isoformat()}">{_pc.strftime("%B")} {_pc.day}, {_pc.year}</time>'
PRICE_SOURCE = f'Source: <a href="{MS_PRICING}" target="_blank" rel="noopener">Microsoft Business Central pricing</a>. Last updated {PRICES_CHECKED}.'
LINKEDIN = CFG.get('linkedin_url', '')

CTA_LABEL = 'Book a free ERP assessment'
if CFG.get('booking_url'):
    CTA_ATTR = f'href="{html.escape(CFG["booking_url"], quote=True)}" data-booking target="_blank" rel="noopener"'
else:
    CTA_ATTR = 'href="@/contact/#schedule"'

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
    ('blog', 'Blog', '@/blog/', None),
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
      <a class="btn btn-primary" {CTA_ATTR}>Book a free assessment</a>
    </nav>
  </div>
</header>'''

SOCIAL_SVG = {
    'linkedin': '<path d="M4.98 3.5a2.5 2.5 0 11-.01 5 2.5 2.5 0 01.01-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.5c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9z"/>',
    'youtube': '<path d="M23 7.2a3 3 0 00-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 001 7.2 31 31 0 00.5 12a31 31 0 00.5 4.8 3 3 0 002.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 002.1-2.1 31 31 0 00.5-4.8 31 31 0 00-.5-4.8zM9.8 15.1V8.9l5.8 3.1z"/>',
}

def social_links():
    out = []
    for key, label in (('linkedin', 'LinkedIn'), ('youtube', 'YouTube')):
        url = CFG.get(f'social_{key}_url') or ''
        href = f'href="{esc(url)}" target="_blank" rel="noopener"' if url else 'href="#" data-placeholder'
        out.append(f'<a class="social" {href} aria-label="Q84 Digital on {label}"><svg viewBox="0 0 24 24" aria-hidden="true">{SOCIAL_SVG[key]}</svg></a>')
    return '<div class="socials">' + ''.join(out) + '</div>'

def footer():
    legal = f'Q84 Digital is operated by {esc(CFG["legal_name"])}. ' if CFG.get('legal_name') else ''
    phone = f'<li>{esc(CFG["phone"])}</li>' if CFG.get('phone') else ''
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div class="stack" style="gap:12px">
        <a class="logo" href="@/"><span class="logo-mark">Q84</span>Q84 Digital</a>
        <p>Business Central implementation for distribution and manufacturing businesses, led by a senior supply chain consultant.</p>
        <ul style="list-style:none;padding:0;margin:0;display:grid;gap:4px"><li style="user-select:all">{esc(EMAIL)}</li>{phone}<li>Vancouver, British Columbia</li></ul>
        {social_links()}
      </div>
      <div><h4>Business Central</h4><ul><li><a href="@/business-central/">Overview &amp; features</a></li><li><a href="@/licensing/">Licensing &amp; pricing</a></li><li><a href="@/business-central/#fit">Is Business Central enough?</a></li><li><a href="@/resources/erp-readiness-checklist/">ERP readiness checklist</a></li></ul></div>
      <div><h4>Services</h4><ul><li><a href="@/implementation/">Implementation</a></li><li><a href="@/data-migration/">Data migration</a></li><li><a href="@/integrations/">Integrations</a></li><li><a href="@/support/">Support</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="@/industries/distribution/">Distribution</a></li><li><a href="@/industries/manufacturing/">Manufacturing</a></li><li><a href="@/blog/">Blog</a></li><li><a href="@/resources/">Resources</a></li><li><a href="@/contact/">Contact</a></li><li><a href="@/privacy/">Privacy</a></li></ul></div>
    </div>
    <div class="legal"><span>© {date.today().year} Q84 Digital. {legal}All rights reserved.</span><span>Microsoft, Dynamics 365 and Business Central are trademarks of the Microsoft group of companies.</span></div>
  </div>
</footer>'''

def cta(title='Find out if Business Central fits your business', text='Pick a time for your free 30-minute ERP assessment with the consultant who would deliver your project.'):
    if CFG.get('booking_url'):
        right = f'''<div class="next"><a class="btn btn-primary" {CTA_ATTR}>{CTA_LABEL}</a></div>'''
    else:
        right = f'''<div class="next">
      <span class="next-label">Next available</span>
      <div class="next-slots" id="nextSlots" data-contact="@/contact/"><a class="next-slot next-fallback" href="@/contact/#schedule"><span>Free 30-minute call</span><strong>Pick a time</strong></a></div>
      <a class="more" href="@/contact/#schedule">See all times \u2192</a>
    </div>'''
    return f'''<section class="cta-section"><div class="wrap"><div class="cta-next">
    <div class="cta-copy"><h2>{title}</h2><p>{text}</p></div>
    {right}
  </div></div></section>'''

def page_head(title, crumb, h1, lede, button=True):
    btn = f'<div class="hero-actions"><a class="btn btn-primary" {CTA_ATTR}>{CTA_LABEL}</a></div>' if button else ''
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

HAS_VIDEO = os.path.exists(os.path.join(ROOT, 'images', 'demo.mp4'))
HAS_POSTER = os.path.exists(os.path.join(ROOT, 'images', 'demo-poster.jpg'))
VIDEO = ''
if HAS_VIDEO:
    poster = '<img src="@/images/demo-poster.jpg" alt="" loading="lazy">' if HAS_POSTER else ''
    VIDEO = f'''<div class="demo-video" id="demo">
    <h3>Watch a 90-second walkthrough</h3>
    <button class="video-poster" type="button" data-video="@/images/demo.mp4" aria-label="Play the 90-second Business Central walkthrough">{poster}<span class="play" aria-hidden="true"></span><span class="video-label">Play walkthrough · 1:30</span></button>
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

''' + VIDEO + '''
  <p class="shot-note" id="shotNote" style="margin-top:20px">Screens shown with example data.</p>
</div>
</section>'''

FAQ_HOME = [
    ('What is Microsoft Dynamics 365 Business Central?', 'It’s Microsoft’s cloud ERP for small and midsize businesses. It brings accounting, inventory, sales, purchasing, warehousing and reporting into one system that works with Microsoft 365.', None),
    ('Is Business Central right for a distribution or inventory-heavy business?', 'For most small and midsize distributors, yes. It handles multi-location stock, purchasing, bins, picking and shipping. If your warehouse is very high-volume or complex, we’ll tell you whether an extension or Dynamics 365 Supply Chain Management fits better.', ('@/business-central/#fit', 'Is Business Central enough?')),
    ('How much does Business Central cost?', 'Licenses are a monthly per-user subscription from Microsoft. Implementation is a one-time project quoted after a free discovery call. Our calculator estimates your license cost in a minute.', ('@/licensing/', 'Estimate your costs')),
    ('How long does implementation take?', 'A focused finance and inventory rollout usually takes a few months. Projects with manufacturing, advanced warehousing or several integrations take longer. You get a timeline after discovery.', ('@/implementation/', 'How implementation works')),
    ('Can Business Central replace QuickBooks?', 'Yes. Companies usually move when they need proper inventory, multiple companies or better reporting. We handle the data migration.', ('@/data-migration/', 'Data migration')),
    ('Can Business Central integrate with Shopify?', 'Yes. Business Central has a Shopify connector, and we build other integrations through its APIs.', ('@/integrations/', 'Integrations')),
    ('Are you a Microsoft partner?', CFG.get('partner_statement') or 'Q84 Digital is an independent Business Central consultancy. Microsoft licenses are billed by Microsoft or a Microsoft licensing partner. We help you choose the right plan, set it up and keep it right-sized as you grow.', ('@/licensing/', 'Licensing & pricing')),
    ('Who will I actually work with?', 'Oleh Karnaukhov, the founder. Q84 Digital is senior-led, so the person who scopes your project is the person who delivers it.', None),
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
    "areaServed": [{"@type": "Country", "name": "United States"}, {"@type": "Country", "name": "Canada"}],
    "address": {"@type": "PostalAddress", "addressLocality": "Vancouver", "addressRegion": "BC", "addressCountry": "CA"},
    "@id": URL + "#organization",
    "founder": {"@id": URL + "#oleh-karnaukhov"},
    "knowsAbout": ["Microsoft Dynamics 365 Business Central", "Dynamics 365 Supply Chain Management", "ERP implementation", "Warehouse management", "ERP integration"],
}
if CFG.get('phone'):
    ORG_SCHEMA['telephone'] = CFG['phone']

PERSON_SCHEMA = {
    "@context": "https://schema.org", "@type": "Person", "@id": URL + "#oleh-karnaukhov",
    "name": "Oleh Karnaukhov", "jobTitle": "Founder and lead consultant",
    "description": "Senior Microsoft Dynamics consultant with more than 15 years of ERP and supply chain experience.",
    "url": URL, "worksFor": {"@id": URL + "#organization"},
    "knowsAbout": ["Microsoft Dynamics 365 Business Central", "Dynamics 365 Supply Chain Management", "Warehouse management", "Transportation management", "Dynamics 365 Customer Engagement", "Dynamics 365 Field Service", "ERP integration"],
}
if LINKEDIN:
    PERSON_SCHEMA["sameAs"] = [LINKEDIN]
if CFG.get('consultant_photo'):
    PERSON_SCHEMA["image"] = URL + "images/" + CFG['consultant_photo']

# ---------------------------------------------------------------- pages

PAGES = []

CHECKLIST_URL = '@/resources/erp-readiness-checklist/'
CHECKLIST_PDF = '@/downloads/q84-erp-readiness-checklist.pdf'
DL_ATTR = f'href="{CHECKLIST_PDF}" download data-download="erp-readiness-checklist"'
def checklist_promo(heading='Is your business ready for a new ERP?', text='Our free ERP Readiness Checklist covers 52 questions across 9 areas, from inventory and warehouse to data and budget. Fill it in with your team, then bring it to your assessment.'):
    return f'''<section class="promo-section"><div class="wrap"><div class="promo">
  <a class="promo-cover" href="{CHECKLIST_URL}" tabindex="-1" aria-hidden="true"><img src="@/images/erp-checklist-cover.webp" alt="" width="640" height="828" loading="lazy"></a>
  <div class="promo-copy"><span class="eyebrow">Free download</span><h2>{heading}</h2><p>{text}</p>
    <div class="hero-actions"><a class="btn btn-primary" {DL_ATTR}>Download the checklist (PDF)</a><a class="btn btn-ghost" href="{CHECKLIST_URL}">See what’s inside</a></div>
    <p class="hint">Fillable PDF, 6 pages. No email required.</p></div>
</div></div></section>'''
def add(path, nav, title, desc, body, schema=None, image=None, subnav=False):
    PAGES.append(dict(path=path, nav=nav, title=title, desc=desc, body=body, schema=schema or [], image=image, subnav=subnav))

def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(t).lower()).strip('-')

NAV_SHORT = {'Watch the overview': 'Overview', 'Choosing the right ERP': 'Is it enough?', 'Moving from QuickBooks?': 'From QuickBooks', 'Where you\u2019re coming from': 'Source systems', 'How Business Central helps': 'Features', 'Is it the right fit?': 'Fit'}
def with_subnav(body):
    # Give each labelled section an id and build a floating in-page menu from the labels
    items, used = [], set()
    def fix(m):
        attrs, inner = m.group(1), m.group(2)
        if 'promo-section' in attrs or 'cta-section' in attrs: return m.group(0)
        e = re.search(r'class="eyebrow">(.*?)<', inner)
        if not e: return m.group(0)
        idm = re.search(r'id="([^"]+)"', attrs)
        sid = idm.group(1) if idm else slug(e.group(1))
        while sid in used: sid += '-2'
        used.add(sid)
        items.append((sid, NAV_SHORT.get(html.unescape(e.group(1)), e.group(1))))
        if not idm: attrs = attrs + f' id="{sid}"'
        return f'<section{attrs}>{inner}'
    body = re.sub(r'<section([^>]*)>(.{0,600})', fix, body, flags=re.S)
    if len(items) < 3: return body
    nav = ('<nav class="subnav" aria-label="On this page"><div class="wrap"><div class="subnav-bar"><div class="subnav-links">'
           + ''.join(f'<a href="#{i}">{t}</a>' for i, t in items)
           + f'</div><a class="btn btn-primary btn-sm" {CTA_ATTR}>{CTA_LABEL}</a></div></div></nav>')
    # the menu has its own booking button, so drop the duplicate one in the page header
    btn = f'<div class="hero-actions"><a class="btn btn-primary" {CTA_ATTR}>{CTA_LABEL}</a></div>'
    if body.startswith('<div class="page-head">'):
        head_end = body.index('</div></div>\n')
        body = body[:head_end].replace(btn, '', 1) + body[head_end:]
    # place the menu straight after the page header
    return body.replace('</div></div>\n', '</div></div>\n' + nav + '\n', 1) if body.startswith('<div class="page-head">') else nav + body

photo = f'<img src="@/images/{esc(CFG["consultant_photo"])}" alt="Oleh Karnaukhov, founder of Q84 Digital" width="480" height="480">' if CFG.get('consultant_photo') else 'OK'

HERO_SET = [
    ('hero-flow.webp', 'Illustration of an order moving from sales order to warehouse, shipment, invoice and reporting'),
    ('hero-warehouse-cutaway.webp', 'Illustration of a warehouse with racks, pallets and a dashboard showing operations'),
    ('hero-operations-desk.webp', 'Illustration of a desk with a laptop showing an inventory dashboard, a barcode scanner and boxes'),
    ('hero-connected-business.webp', 'Illustration of an office, warehouse and delivery van connected to one dashboard'),
    ('hero-manufacturing-line.webp', 'Illustration of a production line with a robotic arm, conveyor, boxes and a monitoring screen'),
    ('hero-loading-dock.webp', 'Illustration of delivery trucks at a loading dock with pallets of boxes and a checklist'),
    ('hero-warehouse-aisle.webp', 'Illustration of a warehouse aisle with stocked racks, a forklift and a stock dashboard'),
    ('hero-packing-station.webp', 'Illustration of a packing station with a monitor, barcode scanner, tape dispenser and boxes'),
]
HERO_SET = [h for h in HERO_SET if os.path.exists(os.path.join(ROOT, 'images', h[0]))]
HERO_IMG = HERO_SET[0][0] if HERO_SET else None
HERO_CLASS = 'hero-split' if HERO_IMG else ''
_hero_list = json.dumps([['@/images/' + f, alt] for f, alt in HERO_SET]).replace('</', '<\\/')
HERO_ART = (f'''<figure class="hero-art"><img id="heroImg" alt="{esc(HERO_SET[0][1])}" width="1024" height="1024" fetchpriority="high"><script>(function(){{var l={_hero_list},k='q84hero',p=-1;try{{var v=sessionStorage.getItem(k);if(v!==null)p=+v}}catch(e){{}}var i=Math.floor(Math.random()*l.length);if(l.length>1&&i===p)i=(i+1)%l.length;try{{sessionStorage.setItem(k,i)}}catch(e){{}}var m=document.getElementById('heroImg');m.alt=l[i][1];m.src=l[i][0];}})();</script><noscript><img src="@/images/{HERO_SET[0][0]}" alt="{esc(HERO_SET[0][1])}" width="1024" height="1024"></noscript></figure>''' if HERO_IMG else '')

# HOME
AVATAR_ATTR = '' if CFG.get('consultant_photo') else ' aria-hidden="true"'
avatar_small = (f'<img src="@/images/{esc(CFG["consultant_photo"])}" alt="" width="96" height="96">' if CFG.get('consultant_photo') else '<span>OK</span>')

case_studies = CFG.get('case_studies') or []
testimonials = CFG.get('testimonials') or []

if case_studies:
    cards = []
    for c in case_studies:
        res = ''.join(f'<li>{esc(r)}</li>' for r in c.get('results', []))
        cards.append(f'''<article class="example"><span class="label">{esc(c.get("industry",""))}{(" \u00b7 " + esc(c["size"])) if c.get("size") else ""}</span><h3>{esc(c.get("title",""))}</h3>
<dl><div><dt>Challenge</dt><dd>{esc(c.get("challenge",""))}</dd></div><div><dt>What we did</dt><dd>{esc(c.get("solution",""))}</dd></div>
<div><dt>Results</dt><dd><ul class="results">{res}</ul></dd></div></dl></article>''')
    PROOF = f'''<div class="section-head"><span class="eyebrow">Project experience</span><h2>Real projects, real results</h2><p class="lede">Client names are withheld at their request. Projects and results are real.</p></div>
<div class="grid g3">{''.join(cards)}</div>'''
else:
    PROOF = f'''<div class="section-head"><span class="eyebrow">How we approach projects</span><h2>Three common starting points</h2><p class="lede">Typical situations our clients come to us with, and how we\u2019d tackle each one.</p></div>
{EXAMPLES}'''

TESTIMONIALS = ''
if testimonials:
    q = ''.join(f'''<figure class="quote"><blockquote>\u201c{esc(t["quote"])}\u201d</blockquote><figcaption><strong>{esc(t.get("name",""))}</strong>{(", " + esc(t["role"])) if t.get("role") else ""}{(", " + esc(t["company"])) if t.get("company") else ""}</figcaption></figure>''' for t in testimonials)
    TESTIMONIALS = f'''<section><div class="wrap"><div class="section-head"><span class="eyebrow">What clients say</span><h2>In their words</h2></div><div class="grid g3">{q}</div></div></section>'''

impl_range = CFG.get('implementation_range')
impl_text = (f'Most implementations fall between {esc(impl_range)}, depending on scope. You get a fixed quote after discovery.'
             if impl_range else 'Quoted as a fixed scope after discovery, based on modules, data, integrations and companies.')

add('', 'home',
    'Business Central for Distribution & Manufacturing | Q84 Digital',
    'Take control of your inventory, operations and finances with Microsoft Dynamics 365 Business Central. Senior-led implementation for distributors and manufacturers, with 15+ years of Dynamics experience.',
    f'''<section class="hero"><div class="wrap">
  <div class="{HERO_CLASS}"><div class="hero-center">
    <a class="announce" href="{CHECKLIST_URL}"><span class="announce-tag">New</span><span>Free ERP Readiness Checklist for Business Central projects</span><span class="announce-link">Download \u2192</span></a>
    <h1>Take control of your inventory, operations and finances <span class="h1-accent">with Microsoft Business Central</span></h1>
    <p class="lede lede-strong">Replace disconnected accounting, inventory and warehouse systems with one connected ERP platform.</p>
    <p class="lede">Q84 Digital helps distributors and manufacturers implement Microsoft Dynamics 365 Business Central, migrate their data and connect the systems they rely on.</p>
    <div class="hero-actions"><a class="btn btn-primary" {CTA_ATTR}>{CTA_LABEL}</a><a class="btn btn-ghost" href="#tour">See how it works</a></div>
    <div class="founder"><span class="founder-photo">{avatar_small}</span><span><strong>Led by Oleh Karnaukhov</strong><span>15+ years of Microsoft Dynamics and supply chain experience</span></span>{f'<a class="li" href="{esc(LINKEDIN)}" target="_blank" rel="noopener me" aria-label="Oleh Karnaukhov on LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 11-.01 5 2.5 2.5 0 01.01-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.5c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9z"/></svg></a>' if LINKEDIN else ''}</div>
  </div>{HERO_ART}</div>
</div></section>

<section class="band" id="problems"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Problems we solve</span><h2>You\u2019re not shopping for software. You\u2019re fixing these.</h2></div>
  <div class="fgrid">
    <div class="fitem">{icon('box')}<h3>Inventory you can\u2019t trust</h3><p>Counts drift from what\u2019s on the shelf.</p><p class="fix"><strong>Fix:</strong> stock by location and bin, cycle counts and item tracking in one system.</p></div>
    <div class="fitem">{icon('link')}<h3>Accounting and warehouse don\u2019t talk</h3><p>Shipments, invoices and the ledger are reconciled by hand.</p><p class="fix"><strong>Fix:</strong> every shipment and receipt posts straight to the books.</p></div>
    <div class="fitem">{icon('receipt')}<h3>Orders processed manually</h3><p>Orders are retyped between email, spreadsheets and systems.</p><p class="fix"><strong>Fix:</strong> one quote-to-cash flow, connected to your online store and carriers.</p></div>
    <div class="fitem">{icon('migrate')}<h3>Outgrown QuickBooks</h3><p>No real inventory, multiple companies or reporting you can rely on.</p><p class="fix"><strong>Fix:</strong> a clean, reconciled move to Business Central.</p></div>
    <div class="fitem">{icon('warehouse')}<h3>A warehouse that can\u2019t keep up</h3><p>Picking errors, slow shipping and no visibility on the floor.</p><p class="fix"><strong>Fix:</strong> bin-based receiving, picking and shipping that staff can follow.</p></div>
    <div class="fitem">{icon('chart')}<h3>Can\u2019t scale or see margins</h3><p>Growth adds more spreadsheets instead of better answers.</p><p class="fix"><strong>Fix:</strong> planning, landed costs and margin reporting on live data.</p></div>
  </div>
</div></section>

{TOUR}

<section class="wash wash-warm" id="industries"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">Industries</span><h2>Built around the way you operate</h2></div>
  <div class="chips" role="tablist" aria-label="Industries">
    <button class="chip" role="tab" id="itab-dist" aria-controls="ipanel-dist" aria-selected="true">Wholesale distribution</button>
    <button class="chip" role="tab" id="itab-mfg" aria-controls="ipanel-mfg" aria-selected="false" tabindex="-1">Manufacturing</button>
  </div>
  <div class="ind-panel" role="tabpanel" id="ipanel-dist" aria-labelledby="itab-dist">
    <figure class="ind-photo"><img src="@/images/industry-distribution.webp" alt="Delivery truck, pallet jack and pallets of boxes with an order list on a tablet" width="1200" height="900" loading="lazy"></figure>
    <div class="stack"><h3>Run a responsive, profitable distribution business</h3>
      <p>Connect purchasing, inventory, warehousing and finance so you always know what you have, where it is and what it earns. Plan replenishment from real demand, pick and ship faster with bins and scanners, and see margins by customer and item.</p>
      <div class="hero-actions"><a class="btn btn-primary" href="@/industries/distribution/">See distribution features</a></div></div>
  </div>
  <div class="ind-panel" role="tabpanel" id="ipanel-mfg" aria-labelledby="itab-mfg" hidden>
    <figure class="ind-photo"><img src="@/images/industry-manufacturing.webp" alt="Production machine and conveyors moving finished products to packing, with a production chart on screen" width="1200" height="900" loading="lazy"></figure>
    <div class="stack"><h3>Plan production and know what each product costs</h3>
      <p>Manage bills of materials, production orders and material planning in the same system as your stock and books. See shortages before they stop the floor and compare actual costs with standard on every order.</p>
      <div class="hero-actions"><a class="btn btn-primary" href="@/industries/manufacturing/">See manufacturing features</a></div></div>
  </div>
</div></section>

<section class="band"><div class="wrap">
  {PROOF}
</div></section>
{TESTIMONIALS}

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we deliver</span><h2>From assessment to everyday support</h2></div>
  <div class="fgrid">
    <a class="fitem" href="@/implementation/">{icon('tools')}<h3>Implementation</h3><p>Business Central set up around your processes, from chart of accounts to go-live.</p><span class="more">Implementation \u2192</span></a>
    <a class="fitem" href="@/data-migration/">{icon('migrate')}<h3>Data migration</h3><p>Clean, verified data moved from QuickBooks, Sage, Dynamics NAV or spreadsheets.</p><span class="more">Data migration \u2192</span></a>
    <a class="fitem" href="@/integrations/">{icon('link')}<h3>Integrations &amp; automation</h3><p>Business Central connected to e-commerce, shipping, CRM and Power BI.</p><span class="more">Integrations \u2192</span></a>
    <a class="fitem" href="@/licensing/">{icon('receipt')}<h3>Licensing &amp; advice</h3><p>The right license mix and a clear view of total cost before you commit.</p><span class="more">Licensing &amp; pricing \u2192</span></a>
    <a class="fitem" href="@/support/">{icon('chart')}<h3>Ongoing support</h3><p>Fixes, improvements and training once you\u2019re live, hourly or monthly.</p><span class="more">Support \u2192</span></a>
  </div>
</div></section>

<section class="band" id="why"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Why Q84 Digital</span><h2>A different way to implement Business Central</h2><p class="lede">Larger Microsoft partners bring big teams and broad portfolios. Q84 Digital is built for companies that want an experienced operations consultant to own their project personally.</p></div>
  <div class="table-wrap"><table class="compare">
    <thead><tr><th></th><th>Many larger ERP firms</th><th>Q84 Digital</th></tr></thead>
    <tbody>
      <tr><td>Who you work with</td><td>Account managers, project managers and a delivery team</td><td>The lead consultant, directly</td></tr>
      <tr><td>Continuity</td><td>Work can be handed between sales, design and delivery teams</td><td>The person who scopes your project delivers it</td></tr>
      <tr><td>Approach</td><td>A standard methodology across many industries</td><td>Built around your warehouse, inventory and order flow</td></tr>
      <tr><td>Depth</td><td>Broad ERP coverage</td><td>Deep supply chain and warehouse background</td></tr>
      <tr><td>Product advice</td><td>Usually focused on the products they sell</td><td>Honest fit advice, including when you need Dynamics 365 Supply Chain Management instead</td></tr>
    </tbody></table></div>
  <p class="shot-note" style="margin-top:14px">A general comparison. Every firm works differently, and larger teams suit some projects better.</p>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Process &amp; pricing</span><h2>Clear steps, clear costs</h2></div>
  <ol class="steps">
    <li><h3>Free assessment</h3><p>30 minutes on your systems, goals and fit.</p></li>
    <li><h3>Discovery</h3><p>Requirements, scope and a fixed quote.</p></li>
    <li><h3>Build</h3><p>Configure, migrate data, build approved extensions.</p></li>
    <li><h3>Testing</h3><p>Run real processes end to end and train your team.</p></li>
    <li><h3>Go-live</h3><p>Switch over with hands-on help afterwards.</p></li>
  </ol>
  <div class="grid g3" style="margin-top:24px">
    <div class="card"><span class="tag">Monthly, from Microsoft</span><h3>Licenses</h3><p>Essentials is $80 and Premium is $110 USD per full user per month at Microsoft\u2019s US list prices.</p><p class="hint">{PRICE_SOURCE}</p></div>
    <div class="card"><span class="tag">One-time</span><h3>Implementation</h3><p>{impl_text}</p></div>
    <div class="card"><span class="tag">Ongoing</span><h3>Support</h3><p>Pay as you go, or a monthly plan with included hours.</p></div>
  </div>
  <p style="margin-top:24px;display:flex;flex-wrap:wrap;gap:12px"><a class="btn btn-primary" href="@/licensing/#calculator">Estimate your costs</a><a class="btn btn-ghost" href="@/licensing/#included">What\u2019s included</a></p>
</div></section>

<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">FAQ</span><h2>Common questions</h2><p class="lede">Don\u2019t see yours? <a href="@/contact/">Ask directly.</a></p></div>
  {faq_html(FAQ_HOME)}
</div></section>
{checklist_promo()}
{cta('Find out if Business Central fits your business')}''', [ORG_SCHEMA, PERSON_SCHEMA, faq_schema(FAQ_HOME)])

# BUSINESS CENTRAL
add('business-central/', 'business-central',
    'What Is Business Central? Features & Fit | Q84 Digital',
    'What Business Central does, its core features for finance, inventory, sales, purchasing and warehousing, and how to tell whether it fits your operations.',
    page_head('Business Central', 'Business Central', 'Microsoft Dynamics 365 Business Central',
              'One cloud ERP for finance, inventory, sales, purchasing and warehousing, built for small and midsize companies and connected to Microsoft 365.') + f'''
<section id="overview-video"><div class="wrap split video-split">
  <div class="stack"><span class="eyebrow">Watch the overview</span><h2>See Business Central in three minutes</h2>
  <p class="lede">Microsoft\u2019s official overview of Business Central: how finance, sales, inventory and operations come together in one system.</p>
  {checks(['Connected finance, sales and operations', 'Built-in Microsoft 365 and Copilot features', 'Runs in the cloud, accessible anywhere'])}</div>
  <figure class="yt" style="margin:0">
    <button class="video-poster" type="button" data-youtube="X7B99e3mNfI" data-title="Microsoft Dynamics 365 Business Central Overview" aria-label="Play video: Microsoft Dynamics 365 Business Central Overview, 3 minutes 13 seconds">
      <img src="https://i.ytimg.com/vi/X7B99e3mNfI/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">
      <span class="play" aria-hidden="true"></span><span class="video-label">Business Central overview \u00b7 3:13</span>
    </button>
    <figcaption class="shot-note">Video by Microsoft. Plays from YouTube when you press play.</figcaption>
  </figure>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Core features</span><h2>One system for the whole business</h2></div>
  <div class="fgrid">
    <div class="fitem">{icon('ledger')}<h3>Financial management</h3><p>General ledger, payables, receivables, bank reconciliation, dimensions and financial reporting.</p></div>
    <div class="fitem">{icon('box')}<h3>Inventory management</h3><p>Items, variants, locations, costing methods, reorder points and planning suggestions.</p></div>
    <div class="fitem">{icon('receipt')}<h3>Sales</h3><p>Quotes, orders, invoicing, pricing, discounts, credit limits and customer management.</p></div>
    <div class="fitem">{icon('cart')}<h3>Purchasing</h3><p>Purchase orders, vendor management, receiving, approvals and drop shipments.</p></div>
    <div class="fitem">{icon('warehouse')}<h3>Warehouse operations</h3><p>Receipts, put-away, picking, shipping, bins and inventory movements.</p></div>
    <div class="fitem">{icon('factory')}<h3>Manufacturing (Premium)</h3><p>Bills of materials, routings, production orders and capacity planning.</p></div>
    <div class="fitem">{icon('pie')}<h3>Reporting &amp; analytics</h3><p>Role-based home pages, Excel analysis and Power BI on live data.</p></div>
    <div class="fitem">{icon('link')}<h3>Integrations</h3><p>A Shopify connector, Microsoft 365 and Dataverse links, and open APIs.</p></div>
    <div class="fitem">{icon('tools')}<h3>Extensions</h3><p>Apps from Microsoft AppSource and custom AL extensions for specific needs.</p></div>
  </div>
</div></section>
<section id="fit"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Choosing the right ERP</span><h2>Is Business Central enough for your operations?</h2>
  <p class="lede">For most small and midsize distributors it is. For very high-volume or complex warehousing, an extension or Dynamics 365 Supply Chain Management may be a better fit. Because we've worked hands-on with both, we can give you a straight answer.</p></div>
  {FIT}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Moving from QuickBooks?</span><h2>Signs you've outgrown entry-level accounting</h2></div>
  {checks(['<strong>Inventory lives in spreadsheets.</strong> Stock counts and costs are tracked outside your accounting system.', '<strong>Several companies or locations.</strong> Consolidation and inter-company work take days.', '<strong>Reporting is manual.</strong> Month-end means exporting and rebuilding reports in Excel.', '<strong>Too many disconnected tools.</strong> Orders, stock and accounting are reconciled by hand.'])}
</div></section>
{checklist_promo('Check your readiness before you choose')}
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
{checklist_promo('Prepare your team for implementation', 'Use our free ERP Readiness Checklist to find gaps in goals, processes, data and ownership before the project starts. It makes discovery faster and scope clearer.')}
{cta('Planning a Business Central project?')}''')

# LICENSING
add('licensing/', 'licensing',
    'Business Central Pricing & Cost Calculator | Q84 Digital',
    'Business Central license prices for Essentials, Premium and Team Members, a cost calculator for your users, and what drives implementation and support costs.',
    page_head('Licensing', 'Services / Licensing &amp; pricing', 'Business Central licensing and pricing',
              'What you’ll pay Microsoft for licenses, what drives implementation cost, and a quick calculator for your own numbers.', button=False) + '''
<section style="padding-top:32px" id="calculator"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Cost estimator</span><h2>Estimate your Business Central costs</h2></div>
  <form class="calc" id="calc" onsubmit="return false">
    <div class="stack" style="gap:22px">
      <fieldset><legend>License plan</legend><div class="choice">
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
      <div><div class="sub">Microsoft licenses per month (USD)</div><div class="big" id="o-monthly">$0</div><div class="sub"><span id="o-annual">$0</span> USD per year</div></div>
      <div class="line"><span>Full users</span><span id="o-full"></span></div>
      <div class="line"><span>Team Members</span><span id="o-team"></span></div>
      <p class="sub" id="o-hint" hidden style="color:inherit">Manufacturing and service management need the Premium plan.</p>
      <div class="line" style="display:block"><div class="sub">Likely implementation size</div><div style="font:600 1.4rem var(--display)" id="o-size"></div><p class="sub" id="o-size-desc"></p></div>
      <div><div class="sub" style="margin-bottom:6px">What drives your scope</div><ul id="o-drivers"></ul></div>
      <a class="btn btn-primary" href="@/contact/">Get a quote for implementation</a>
      <p class="sub">All figures are in US dollars, using Microsoft's US list prices (per user per month, annual commitment) effective November 2025. ''' + PRICE_SOURCE.replace('<a ', '<a style="color:inherit" ') + ''' Implementation is quoted after a free discovery call. <a href="#included" style="color:inherit">What’s included</a></p>
    </div>
  </form>
</div></section>
<section class="band" id="included"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Implementation scope</span><h2>What an implementation includes</h2><p class="lede">Every project gets a written, fixed scope after discovery. This is what a standard implementation covers, and what is quoted separately.</p></div>
  <div class="grid g2">
    <div class="card"><span class="tag">Included</span><h3>In a standard implementation</h3>
      <ul class="checks"><li><div>Discovery workshops and a written solution design</div></li><li><div>Setup of finance, sales, purchasing and inventory</div></li><li><div>Warehouse setup for locations and bins in scope</div></li><li><div>Migration of master data, open items and opening balances</div></li><li><div>Testing with your team and role-based training</div></li><li><div>Go-live support and the first month-end close</div></li></ul></div>
    <div class="card"><span class="tag">Quoted separately</span><h3>Not included by default</h3>
      <ul class="checks"><li><div>Microsoft licenses and paid AppSource apps</div></li><li><div>Custom AL extensions and reports</div></li><li><div>Integrations with other systems</div></li><li><div>Migration of detailed transaction history</div></li><li><div>Ongoing support after the go-live period</div></li></ul></div>
  </div>
  <div class="section-head" style="margin-top:48px"><h2>Typical timelines</h2><p class="lede">Typical ranges for small and midsize businesses. Your actual timeline is set after discovery.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Project size</th><th>Typical scope</th><th>Typical timeline</th></tr></thead>
    <tbody>
      <tr><td>Focused</td><td>Finance, sales, purchasing and basic inventory, one company, straightforward data move</td><td>2 to 3 months</td></tr>
      <tr><td>Standard</td><td>Adds warehouse processes, migration from another ERP, or one or two integrations</td><td>3 to 6 months</td></tr>
      <tr><td>Complex</td><td>Several companies, manufacturing, advanced warehousing or multiple integrations</td><td>6 months or more, often phased</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">License types</span><h2>Choosing the right licenses</h2><p class="lede">Most companies combine a few full users with lower-cost Team Members licenses for people who only view data or do light tasks. All full users in a company must be on the same plan.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>License</th><th>Price (USD)</th><th>Who it's for</th><th>Typical use</th></tr></thead>
    <tbody>
      <tr><td>Essentials</td><td>$80 / user / month</td><td>Full users</td><td>Finance, sales, purchasing, inventory, warehousing, projects</td></tr>
      <tr><td>Premium</td><td>$110 / user / month</td><td>Full users who need more</td><td>Everything in Essentials, plus manufacturing and service management</td></tr>
      <tr><td>Team Members</td><td>$8 / user / month</td><td>Light users</td><td>View data, approve documents, update basic records</td></tr>
    </tbody></table></div>
  <p class="note" style="margin-top:20px">Prices are Microsoft's US list prices in US dollars, effective November 1, 2025, and may change. We confirm current pricing in every estimate. Microsoft license fees are separate from our consulting fees.<br>''' + PRICE_SOURCE + '''</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Total cost</span><h2>The parts of a Business Central budget</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Cost</th><th>Type</th><th>What it depends on</th></tr></thead>
    <tbody>
      <tr><td>Licenses</td><td>Monthly</td><td>Plan and number of full and light users</td></tr>
      <tr><td>Implementation</td><td>One-time</td><td>Modules, companies, processes and custom work</td></tr>
      <tr><td>Data migration</td><td>One-time</td><td>Source systems, data volume and data quality</td></tr>
      <tr><td>Integrations</td><td>One-time plus upkeep</td><td>Number of systems and how complex the data flow is</td></tr>
      <tr><td>Add-on apps</td><td>Monthly</td><td>AppSource apps you choose, priced by their publishers</td></tr>
      <tr><td>Support</td><td>Hourly or monthly</td><td>How much help you want after go-live</td></tr>
    </tbody></table></div>
</div></section>
''' + cta('Get a cost estimate for your business', 'Share a few details and we’ll come back with licensing and implementation ranges.'))

def worked(title, setup, rows, outcome):
    trs = ''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in rows)
    return f'''<div class="worked">
  <span class="label">Worked example · Illustrative scenario</span>
  <h3>{esc(title)}</h3>
  <p>{esc(setup)}</p>
  <div class="table-wrap"><table><thead><tr><th>Stage</th><th>What happens</th></tr></thead><tbody>{trs}</tbody></table></div>
  <p><strong>Outcome:</strong> {esc(outcome)}</p>
  <p class="shot-note">This example shows how we approach this kind of project. It is not a client case study.</p>
</div>'''

def faq_section(items, title='Frequently asked questions'):
    return f'''<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">FAQ</span><h2>{title}</h2><p class="lede">Have a different question? <a href="@/contact/">Ask directly.</a></p></div>
  {faq_html(items)}
</div></section>'''

# DATA MIGRATION
FAQ_MIG = [
    ('How long does a data migration take?', 'For most small and midsize businesses the migration runs alongside the implementation over three to six weeks, with at least two trial loads before the final cutover. The final load itself usually happens over a weekend or at a month-end.', None),
    ('Do we have to bring over all our historical transactions?', 'Usually not. Most companies bring over open items, balances and a summary of past results, and keep the old system or an export for reference. Detailed history can be migrated, but it adds cost and rarely pays off.', None),
    ('Who cleans up the data?', 'We do the heavy lifting: finding duplicates, gaps and inconsistent codes, and fixing what can be fixed automatically. Your team makes the business decisions, such as which customers are inactive and which item numbers to keep.', None),
    ('Can we keep using our old system during the project?', 'Yes. You keep working as normal until cutover. We take a final extract at an agreed point, load it, reconcile it and then you switch to Business Central.', None),
]
add('data-migration/', 'data-migration',
    'Business Central Data Migration | Q84 Digital',
    'Move to Business Central with clean, reconciled data. Migration from QuickBooks, Sage, Dynamics NAV, other ERPs and spreadsheets, with a worked example and FAQs.',
    page_head('Data migration', 'Services / Data migration', 'Business Central data migration',
              'Move customers, vendors, items, open documents and balances into Business Central, then reconcile everything so your numbers match on day one.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where you're coming from</span><h2>Systems we migrate from</h2>
  <p class="lede">Every source system has its own quirks. QuickBooks stores items and customers differently from Business Central, and Dynamics NAV often carries years of custom fields. We plan the move around the system you actually have.</p></div>
  <div class="grid g4">
    <div class="card"><span class="tag">From</span><h3>QuickBooks</h3><p>Customers, vendors, items, open receivables and payables, and trial balance.</p></div>
    <div class="card"><span class="tag">From</span><h3>Sage</h3><p>Master data, open transactions and historical balances.</p></div>
    <div class="card"><span class="tag">From</span><h3>Dynamics NAV</h3><p>Upgrade or re-implement, depending on version and custom code.</p></div>
    <div class="card"><span class="tag">From</span><h3>Spreadsheets &amp; other ERPs</h3><p>Structured templates, cleansing and validation before loading.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Our process</span><h2>Five steps to clean, trusted data</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Step</th><th>What happens</th><th>Your team's role</th></tr></thead>
    <tbody>
      <tr><td>1. Map</td><td>Old fields, codes and structures are matched to Business Central, including posting groups and dimensions.</td><td>Confirm how you want customers, items and accounts grouped.</td></tr>
      <tr><td>2. Cleanse</td><td>Duplicates, missing values and inactive records are flagged and fixed.</td><td>Decide which records to retire or merge.</td></tr>
      <tr><td>3. Trial load</td><td>Data is loaded into a test company using Business Central configuration packages.</td><td>None yet. This is our check.</td></tr>
      <tr><td>4. Validate</td><td>Records are spot-checked and real transactions are posted against the migrated data.</td><td>Finance and warehouse leads review and test.</td></tr>
      <tr><td>5. Reconcile</td><td>Balances, open items and stock values are matched to the old system before go-live.</td><td>Sign off the reconciliation.</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">How much history?</span><h2>Choose what to bring over</h2><p class="lede">Bringing everything over sounds safe but often means moving years of messy data. Most companies choose the middle option.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Option</th><th>What moves</th><th>Best for</th></tr></thead>
    <tbody>
      <tr><td>Open items only</td><td>Master data, open orders, open receivables and payables, stock and opening balances</td><td>Fast, clean starts</td></tr>
      <tr><td>Plus summary history</td><td>The above, plus monthly general ledger balances for one or two prior years</td><td>Year-over-year reporting in Business Central</td></tr>
      <tr><td>Detailed history</td><td>Individual historical transactions</td><td>Specific audit or reporting needs. Quoted separately.</td></tr>
    </tbody></table></div>
</div></section>
<section class="band"><div class="wrap">
  {worked('Moving a 25-person distributor off QuickBooks Desktop',
          'A distributor runs accounting in QuickBooks Desktop with around 1,800 customers. Its 4,000 items and stock levels for two warehouses live in spreadsheets, and month-end takes a week of reconciling.',
          [('Weeks 1 to 2', 'Map QuickBooks customers, vendors and accounts to Business Central. Merge the item spreadsheets into one list and agree cleansing rules with the owner.'),
           ('Week 3', 'First trial load into a test company. Duplicate customers and inconsistent unit-of-measure codes are found and fixed.'),
           ('Week 4', 'Finance posts test invoices and payments. The warehouse lead checks stock by location and bin.'),
           ('Week 5', 'Second trial load. Receivables, payables and the trial balance reconcile to QuickBooks.'),
           ('Cutover weekend', 'Physical stock count, final load of open items and opening balances, and sign-off before Monday trading.')],
          'The company starts in Business Central with balances that match QuickBooks to the cent, one item list and stock it can trust, with no gap in trading.')}
</div></section>
{faq_section(FAQ_MIG)}
{cta('Planning your move to Business Central?')}''', [faq_schema(FAQ_MIG)])

# INTEGRATIONS
FAQ_INT = [
    ('Will integrations break when Business Central updates?', 'Microsoft releases two major updates a year. Integrations built on its standard APIs and extension model are designed to survive them, and we test custom work against each release preview so problems show up before your production system updates.', None),
    ('Do integrations run in real time?', 'It depends on the connection. Some sync within minutes, others run on a schedule such as every 15 minutes or nightly. We pick the timing based on what the business needs, such as near real-time stock for an online store and nightly for reporting.', None),
    ('Do we always need custom code?', 'No. We check for a standard connector or an AppSource app first, such as Microsoft’s Shopify connector. Custom development is only for gaps those options can’t cover.', None),
    ('Are there running costs?', 'Sometimes. Connector apps often have a monthly subscription, and some integrations use Azure services billed by Microsoft. We include these costs in the estimate so there are no surprises.', None),
]
add('integrations/', 'integrations',
    'Business Central Integrations & Shopify | Q84 Digital',
    'Connect Business Central to Shopify, shipping carriers, CRM, EDI providers and Power BI, and extend it with AL and Power Automate. Includes a worked example and FAQs.',
    page_head('Integrations', 'Services / Integrations &amp; customization', 'Business Central integrations and customization',
              'Connect Business Central to the tools you already use, and extend it where standard features don’t cover your process.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we build</span><h2>Connected systems, less manual entry</h2>
  <p class="lede">Every time someone retypes an order, a tracking number or a stock level, you pay for it in time and errors. Integrations remove those steps so data is entered once and flows where it is needed.</p></div>
  <div class="grid g3">
    <div class="card">{icon('tools')}<span class="tag">Extensions</span><h3>AL development</h3><p>Custom fields, pages, reports and business logic built as extensions.</p></div>
    <div class="card">{icon('link')}<span class="tag">APIs</span><h3>System integrations</h3><p>Data sync with other business systems through Business Central's APIs.</p></div>
    <div class="card">{icon('shop')}<span class="tag">Commerce</span><h3>Shopify &amp; e-commerce</h3><p>Orders, items, stock and pricing kept in step with your online store.</p></div>
    <div class="card">{icon('truck')}<span class="tag">Logistics</span><h3>Shipping &amp; fulfillment</h3><p>Carrier rates, labels and tracking connected to warehouse shipments.</p></div>
    <div class="card">{icon('chart')}<span class="tag">Automation</span><h3>Power Automate</h3><p>Approvals, notifications and routine tasks handled automatically.</p></div>
    <div class="card">{icon('pie')}<span class="tag">Reporting</span><h3>Power BI</h3><p>Financial and operational dashboards on live Business Central data.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Common integrations</span><h2>What typically connects to Business Central</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>System</th><th>What syncs</th><th>Usual approach</th></tr></thead>
    <tbody>
      <tr><td>Shopify</td><td>Orders, customers, items, stock levels and payments</td><td>Microsoft's built-in Shopify connector</td></tr>
      <tr><td>Shipping carriers</td><td>Rates, labels and tracking numbers</td><td>An AppSource shipping app or an API integration</td></tr>
      <tr><td>EDI trading partners</td><td>Purchase orders, advance ship notices and invoices</td><td>An app from a specialist EDI provider</td></tr>
      <tr><td>Dynamics 365 Sales</td><td>Accounts, contacts, products and orders</td><td>Microsoft's standard Dataverse integration</td></tr>
      <tr><td>Power BI</td><td>Financial and operational data</td><td>Microsoft's Business Central Power BI apps, extended as needed</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our approach</span><h2>Configure first, customize only when it pays off</h2><p class="lede">Every custom line of code is something to maintain. We check whether standard features or an existing app can do the job before we build anything.</p></div>
  {checks(['<strong>Fit check.</strong> Standard setup, AppSource app or custom extension: we compare the options and their running costs with you.', '<strong>Clear data flow.</strong> We agree which system owns each piece of data, how often it syncs and what happens when something fails.', '<strong>Built for updates.</strong> Extensions follow Microsoft’s extension model, which keeps Business Central updates much smoother. We still test custom work against each major release.', '<strong>Tested properly.</strong> Integrations are tested with realistic data volumes, duplicates and error cases, not just the happy path.', '<strong>Documented.</strong> You get notes on what was built, how it works and how to monitor it.'])}
</div></section>
<section class="band"><div class="wrap">
  {worked('Connecting a Shopify store to Business Central',
          'An e-commerce distributor sells through Shopify and keeps its accounting in Business Central. Staff re-enter every web order, stock levels are updated by hand twice a day, and the store sometimes sells items that are out of stock.',
          [('Design', 'Agree that Business Central owns items, prices and stock, and Shopify owns web orders. Map product variants to item variants.'),
           ('Setup', 'Configure Microsoft’s Shopify connector: item sync, stock sync by location, and order import with customer matching.'),
           ('Rules', 'Orders with unknown items or failed payments go to a review list instead of creating bad sales orders.'),
           ('Testing', 'Run test orders, refunds and partial shipments through the full flow, from Shopify order to shipment, invoice and payment.'),
           ('Go-live', 'Switch on scheduled sync and train staff to clear the exceptions list each morning.')],
          'Web orders arrive in Business Central without retyping, the store shows stock that matches the warehouse, and staff only touch the orders that genuinely need attention.')}
</div></section>
<section><div class="wrap"><div class="note">Also running Dynamics 365 Sales, Customer Service or Field Service? We work across the Dynamics 365 family and can connect Business Central with Dataverse and your CRM.</div></div></section>
{faq_section(FAQ_INT)}
{cta('Have a system that needs to connect?', 'Tell us what you use today. We’ll suggest the simplest reliable way to make it work with Business Central.')}''', [faq_schema(FAQ_INT)])

# SUPPORT
FAQ_SUP = [
    ('Can you support a system another partner implemented?', 'Yes. Many support clients come to us after their original implementation. We usually start with a health check so we understand how your system was set up before changing anything.', None),
    ('Do we have to move our Microsoft licenses?', 'No. Your licenses can stay with your current licensing partner or Microsoft. Support covers the system itself, not where the subscription is billed.', None),
    ('Hourly or monthly: which is better?', 'Hourly suits occasional questions and one-off fixes. A monthly plan suits businesses that want regular improvements, priority response and someone who knows their system well. You can start hourly and move to a plan later.', None),
    ('What if a fix needs development work?', 'Small changes are handled within support time. Larger changes, such as a new integration or extension, are scoped and quoted separately so you approve the cost before work starts.', None),
]
add('support/', 'support',
    'Business Central Support Services | Q84 Digital',
    'Business Central support from a senior consultant: health checks, troubleshooting, configuration fixes, training and enhancements. Hourly or monthly, with a worked example and FAQs.',
    page_head('Support', 'Services / Support', 'Business Central support',
              'Already using Business Central? Get help fixing issues, improving your setup and training your team, from a consultant who knows the system well.') + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we help with</span><h2>Support that goes beyond tickets</h2>
  <p class="lede">Most support requests are symptoms of something in the setup: a posting group pointing to the wrong account, a missing batch job or a process people work around. We fix the request and the cause behind it.</p></div>
  <div class="grid g3">
    <div class="plain">{icon('support')}<h3>Troubleshooting</h3><p>Posting errors, setup problems, failed jobs and unexpected results.</p></div>
    <div class="plain">{icon('tools')}<h3>Configuration improvements</h3><p>Cleaner posting groups, dimensions, approvals and number series.</p></div>
    <div class="plain">{icon('receipt')}<h3>User training</h3><p>Role-based sessions for new staff or new processes.</p></div>
    <div class="plain">{icon('chart')}<h3>Process reviews</h3><p>Find manual steps and slow spots, and fix them.</p></div>
    <div class="plain">{icon('link')}<h3>Integration support</h3><p>Monitor and fix connections with other systems.</p></div>
    <div class="plain">{icon('box')}<h3>Enhancements</h3><p>Small extensions, reports and changes as your business grows.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Start here</span><h2>A Business Central health check</h2><p class="lede">New support clients usually start with a health check. It gives you a clear picture of your system and a prioritized list of fixes, whether or not you continue with us.</p></div>
  {checks(['<strong>Setup review.</strong> Posting groups, dimensions, number series, costing and approvals.', '<strong>Data review.</strong> Unposted entries, inventory value against the general ledger, and duplicate records.', '<strong>Jobs and integrations.</strong> Scheduled jobs, connector errors and failed syncs.', '<strong>Security.</strong> User permissions and who can post what.', '<strong>Report.</strong> A plain-language list of findings, ranked by business impact.'])}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">How it works</span><h2>What happens when you ask for help</h2><p class="lede">Simple, predictable and handled by the same consultant each time, so you never have to explain your setup twice.</p></div>
  <ol class="steps" style="grid-template-columns:1fr">
    <li><h3>Tell us what’s wrong</h3><p>Email a short description and, if you can, a screenshot or the document number involved.</p></li>
    <li><h3>We diagnose the cause</h3><p>We reproduce the problem in a sandbox where possible, so your live data stays safe while we investigate.</p></li>
    <li><h3>Fix, test and explain</h3><p>We apply the fix, confirm it with you and explain what caused it in plain language.</p></li>
    <li><h3>Prevent it next time</h3><p>Where it makes sense, we change the setup or add a check so the same issue doesn’t come back.</p></li>
  </ol>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Ways to work with us</span><h2>Choose the support model that fits</h2></div>
  <div class="grid g2">
    <div class="card"><span class="tag">Flexible</span><h3>Hourly consulting</h3><p>Pay only for the time you use. Good for occasional questions and one-off fixes.</p><a class="more" href="@/contact/">Ask about hourly support →</a></div>
    <div class="card"><span class="tag">Predictable</span><h3>Monthly support plan</h3><p>A set number of hours each month, agreed response times and a regular review of your system.</p><a class="more" href="@/contact/">Ask about monthly plans →</a></div>
  </div>
</div></section>
<section><div class="wrap">
  {worked('Fixing month-end at a company that inherited its setup',
          'A wholesaler went live on Business Central two years ago with another partner. Month-end now takes days because inventory value in reports never matches the balance sheet, and posting errors stop invoices going out.',
          [('Health check', 'Review costing setup, inventory posting groups, scheduled jobs and recent posting errors.'),
           ('Findings', 'The Adjust Cost – Item Entries job was not scheduled and two item categories posted to the wrong inventory accounts.'),
           ('Fix', 'Correct the posting setup, run cost adjustment, post inventory cost to the general ledger and reconcile the difference with the accountant.'),
           ('Prevent', 'Schedule nightly cost adjustment and add a simple month-end checklist inside Business Central.'),
           ('Ongoing', 'Move to a small monthly plan covering questions, minor changes and a quarterly review.')],
          'Inventory value in Business Central matches the balance sheet, invoices post without errors, and month-end takes hours instead of days.')}
</div></section>
{faq_section(FAQ_SUP)}
{cta('Need help with Business Central?', 'Describe the issue and we’ll get back to you with next steps within one business day.')}''', [faq_schema(FAQ_SUP)])

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
{checklist_promo()}
{cta('Talk to a distribution ERP specialist')}''')

FAQ_MFG = [
    ('Do we need Business Central Premium for manufacturing?', 'For production orders, routings, work centers and capacity planning, yes. Those features are only in the Premium license. Simple kitting with assembly orders is available in Essentials.', ('@/licensing/#calculator', 'Estimate your license cost')),
    ('Can Business Central handle process manufacturing?', 'Business Central is built for discrete manufacturing: products made from distinct parts. Batch, formula or recipe-based production, such as food or chemicals, usually needs a specialist add-on from Microsoft AppSource. We’ll tell you early if that applies to you.', None),
    ('How do shop-floor workers record production?', 'Through output and consumption journals or the production order pages, on a desktop, tablet or shop-floor terminal. Shared terminals can use a lower-cost device license instead of named user licenses.', None),
    ('Should we use standard or actual costing?', 'Many manufacturers use standard costing so they can see variances between planned and actual costs. Others prefer average or FIFO costing for simplicity. We’ll recommend a method based on how you price and report.', None),
]
add('industries/manufacturing/', 'manufacturing',
    'Business Central for Manufacturers | Q84 Digital',
    'Business Central Premium for small and midsize manufacturers: bills of materials, production orders, material planning and product costing, with a worked example and FAQs.',
    page_head('Manufacturing', 'Industries / Manufacturing', 'Business Central for manufacturers',
              'Plan production, control materials and know what each product really costs to make.') + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Common challenges</span><h2>What holds growing manufacturers back</h2><p class="lede">Most small manufacturers start with accounting software and spreadsheets. That works until order volume grows and nobody can say what’s in production, what’s short or what a product really costs.</p></div>
  {checks(['<strong>No production visibility.</strong> Order status lives on the shop floor, not in the system.', '<strong>Costs worked out in spreadsheets.</strong> Material and labor costs are estimates.', '<strong>Material shortages.</strong> Components run out because demand isn’t planned.', '<strong>Disconnected systems.</strong> Production, stock and accounting don’t share data.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How Business Central helps</span><h2>Manufacturing features in Business Central Premium</h2></div>
  <div class="grid g3">
    <div class="card">{icon('ledger')}<h3>Bills of materials</h3><p>Multi-level BOMs with versions and component substitutes.</p></div>
    <div class="card">{icon('factory')}<h3>Production orders</h3><p>Planned, released and finished orders with consumption and output.</p></div>
    <div class="card">{icon('chart')}<h3>Material planning</h3><p>Planning worksheets that suggest what to buy and make, and when.</p></div>
    <div class="card">{icon('tools')}<h3>Routings &amp; capacity</h3><p>Work centers, machine centers and capacity planning.</p></div>
    <div class="card">{icon('receipt')}<h3>Product costing</h3><p>Standard or actual costs with variance reporting.</p></div>
    <div class="card">{icon('box')}<h3>Inventory &amp; tracking</h3><p>Lot and serial tracking from components to finished goods.</p></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it flows</span><h2>A production order, start to finish</h2></div>
  <ol class="steps">
    <li><h3>Plan</h3><p>The planning worksheet turns sales demand into suggested production and purchase orders.</p></li>
    <li><h3>Release</h3><p>Released production orders reserve components and create pick work for the warehouse.</p></li>
    <li><h3>Produce</h3><p>Consumption and output are recorded against each operation in the routing.</p></li>
    <li><h3>Finish</h3><p>Finished goods move into stock, ready to ship.</p></li>
    <li><h3>Cost</h3><p>Cost adjustment calculates actual costs and variances against standard.</p></li>
  </ol>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Is it the right fit?</span><h2>Where Business Central manufacturing works best</h2><p class="lede">Business Central suits most small and midsize discrete manufacturers. A few situations need an add-on or a different product, and it’s better to know that before you start.</p></div>
  {checks(['<strong>A good fit:</strong> make-to-stock and make-to-order production, assembly and kitting, and light fabrication with defined routings.', '<strong>Needs an add-on:</strong> batch or recipe-based process manufacturing, advanced shop-floor scheduling, or detailed quality management.', '<strong>Consider Dynamics 365 Supply Chain Management:</strong> multi-site, high-volume production with complex planning across plants.'])}
</div></section>
<section><div class="wrap">
  {worked('A fabrication shop moving production off spreadsheets',
          'A 40-person metal fabrication company builds made-to-order products from about 600 components. Production is planned on a whiteboard, costs are estimated in a spreadsheet and the accountant only learns the real margin weeks after shipping.',
          [('Design', 'Model three-level bills of materials, routings across four work centers and standard costs for components and labor.'),
           ('Build', 'Set up Premium manufacturing, production order statuses, and warehouse picks for releasing components to the floor.'),
           ('Data', 'Load items, BOMs and routings from the existing spreadsheets after cleansing duplicates and missing units of measure.'),
           ('Test', 'Run sample orders end to end, from sales order to planning worksheet, production order, output, shipment and invoice.'),
           ('Go-live', 'Start with one product family, then add the rest once the floor team is comfortable recording output.')],
          'The company plans production from real demand, sees shortages before they stop the floor, and gets cost variances for every order instead of guessing at margins.')}
</div></section>
<section><div class="wrap"><div class="note">Manufacturing features need the Business Central Premium license. <a href="@/licensing/#calculator">Estimate your license cost.</a></div></div></section>
{faq_section(FAQ_MFG)}
{checklist_promo()}
{cta('Talk about your production processes')}''', [faq_schema(FAQ_MFG)])

# BLOG
# Each post: slug, title, date (YYYY-MM-DD), summary, tag, body (HTML), placeholder (True = shows a draft notice)
POSTS = [
    dict(slug='signs-you-have-outgrown-quickbooks',
         title='Seven signs your distribution business has outgrown QuickBooks',
         date='2026-10-31', tag='ERP selection', placeholder=True,
         summary='Placeholder summary. A short description of the article will appear here, about two sentences long, to help readers decide whether to read on.',
         body='''<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper.</p>
<h2>1. Placeholder heading</h2>
<p>Sed posuere consectetur est at lobortis. Cras mattis consectetur purus sit amet fermentum. Maecenas faucibus mollis interdum. Nullam quis risus eget urna mollis ornare vel eu leo. Aenean lacinia bibendum nulla sed consectetur.</p>
<h2>2. Placeholder heading</h2>
<p>Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Curabitur blandit tempus porttitor.</p>
<ul><li>Placeholder bullet point one</li><li>Placeholder bullet point two</li><li>Placeholder bullet point three</li></ul>
<h2>3. Placeholder heading</h2>
<p>Etiam porta sem malesuada magna mollis euismod. Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Donec sed odio dui.</p>
<blockquote>Placeholder pull quote. A short, memorable line from the article can go here.</blockquote>
<h2>What to do next</h2>
<p>Nulla vitae elit libero, a pharetra augue. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh.</p>'''),
]

def fmt_date(d):
    x = date.fromisoformat(d)
    return f'<time datetime="{d}">{x.strftime("%B")} {x.day}, {x.year}</time>'

def post_card(p):
    draft = '<span class="pill low">Placeholder</span>' if p.get('placeholder') else ''
    return f'''<a class="card post-card" href="@/blog/{p['slug']}/"><span class="tag">{esc(p['tag'])}</span>{draft}<h3>{esc(p['title'])}</h3><p>{esc(p['summary'])}</p><span class="post-meta">{fmt_date(p['date'])} \u00b7 Oleh Karnaukhov</span></a>'''

add('blog/', 'blog', 'Business Central & ERP Blog | Q84 Digital',
    'Practical articles on Microsoft Dynamics 365 Business Central, ERP selection, inventory and warehouse operations for distributors and manufacturers.',
    page_head('Blog', 'Blog', 'Insights on Business Central and operations',
              'Practical articles on ERP selection, inventory, warehousing and getting the most out of Business Central.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap">
  <div class="grid g3">{''.join(post_card(p) for p in sorted(POSTS, key=lambda p: p['date'], reverse=True))}</div>
</div></section>
{checklist_promo()}
{cta()}''')

for p in POSTS:
    avatar = f'<img src="@/images/{esc(CFG["consultant_photo"])}" alt="" width="48" height="48">' if CFG.get('consultant_photo') else 'OK'
    notice = '<div class="note" style="margin-bottom:24px"><strong>Placeholder article.</strong> This page uses dummy text to show the blog layout. Real content will replace it before launch.</div>' if p.get('placeholder') else ''
    schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'], "datePublished": p['date'],
              "author": {"@id": URL + "#oleh-karnaukhov"}, "publisher": {"@id": URL + "#organization"},
              "mainEntityOfPage": URL + f"blog/{p['slug']}/"}
    add(f"blog/{p['slug']}/", 'blog', f"{p['title']} | Q84 Digital", p['summary'],
        f'''<article class="post"><div class="wrap post-wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="@/">Home</a> / <a href="@/blog/">Blog</a></nav>
  <span class="tag post-tag">{esc(p['tag'])}</span>
  <h1>{esc(p['title'])}</h1>
  <div class="byline"><span class="founder-photo">{avatar}</span><span><strong>Oleh Karnaukhov</strong><span>{fmt_date(p['date'])}</span></span></div>
  {notice}
  <div class="post-body">{p['body']}</div>
  <p style="margin-top:32px"><a class="more" href="@/blog/">\u2190 All articles</a></p>
</div></article>
{checklist_promo()}
{cta()}''', [schema])

# CONTACT
phone_card = f'<div class="card"><span class="tag">Phone</span><p class="mono" style="color:var(--ink);user-select:all">{esc(CFG["phone"])}</p></div>' if CFG.get('phone') else ''
if CFG.get('booking_url'):
    SCHEDULER = f'''<div class="sched" id="schedule">
  <div class="sched-head"><h2>Pick a time</h2><p class="hint">Choose a 30-minute slot. You’ll get a calendar invite straight away.</p></div>
  <iframe class="sched-embed" src="{esc(CFG['booking_url'])}" title="Book a free ERP assessment" loading="lazy"></iframe>
  <p class="hint">Calendar not loading? <a href="{esc(CFG['booking_url'])}" data-booking target="_blank" rel="noopener">Open the booking page</a>.</p>
</div>'''
else:
    SCHEDULER = '''<div class="sched" id="schedule">
  <div class="sched-head"><h2>Pick a time</h2><p class="hint" id="tzNote">Times are shown in your time zone.</p></div>
  <div class="sched-pick" id="schedPick">
    <div class="sched-step"><h3><span class="num">1</span> Choose a day</h3>
      <div class="cal" id="days">
        <div class="cal-head">
          <button type="button" class="cal-nav" id="calPrev" aria-label="Previous month"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
          <label class="sr-only" for="calMonth">Month</label><select id="calMonth"></select>
          <button type="button" class="cal-nav" id="calNext" aria-label="Next month"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
        </div>
        <div class="cal-dow" aria-hidden="true"><span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span></div>
        <div class="cal-grid" id="calGrid" role="group" aria-label="Available days"></div>
      </div>
    </div>
    <div class="sched-step"><h3><span class="num">2</span> <span id="slotsTitle">Choose a time</span></h3><div class="slots" id="slots" role="group" aria-label="Available times" aria-live="polite"><p class="hint">Choose a day to see available times.</p></div></div>
  </div>
  <form class="sched-step" id="bookForm" novalidate hidden>
    <h3><span class="num">3</span> Your details</h3>
    <p class="picked" id="picked"></p>
    <div class="row">
      <div class="field"><label for="b-name">Name</label><input id="b-name" name="name" autocomplete="name" required><span class="err" id="be-name" hidden>Enter your name so we know who to expect.</span></div>
      <div class="field"><label for="b-email">Business email</label><input id="b-email" name="email" type="email" autocomplete="email" required><span class="err" id="be-email" hidden>Enter an email address like name@company.com.</span></div>
    </div>
    <div class="field"><label for="b-company">Company</label><input id="b-company" name="company" autocomplete="organization" required><span class="err" id="be-company" hidden>Enter your company name.</span></div>
    <div class="field"><label for="b-notes">Anything we should know? <span class="hint">(optional)</span></label><textarea id="b-notes" name="notes" placeholder="e.g. We run QuickBooks and two warehouses"></textarea></div>
    <div style="position:absolute;left:-9999px" aria-hidden="true"><label for="b-gotcha">Leave this empty</label><input id="b-gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
    <div class="hero-actions"><button class="btn btn-primary" type="submit">Request this time</button><button class="btn btn-ghost" type="button" id="changeTime">Change time</button></div>
    <p class="hint" id="bookStatus" role="status" hidden></p>
  </form>
  <div class="sent" id="bookSent" hidden role="status" tabindex="-1"><h3>Your time is requested</h3><p id="bookSentText"></p></div>
  <noscript><p class="hint">The scheduler needs JavaScript. Email ''' + esc(EMAIL) + ''' with a few times that suit you.</p></noscript>
</div>'''

add('contact/', 'contact',
    'Free ERP Readiness Assessment | Q84 Digital',
    'Book a free 30-minute ERP readiness assessment. Find out whether Business Central fits your distribution or manufacturing business, what it would involve and what it would cost.',
    page_head('Contact', 'Free ERP assessment', 'Book a free ERP readiness assessment',
              'In 30 minutes with Oleh you’ll get an honest view of whether Business Central fits your business, what the project would involve and a rough idea of cost.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap contact-grid">
  <div class="stack" style="gap:20px">
    {SCHEDULER}
    <details class="alt-contact">
      <summary>Prefer to send a message instead?</summary>
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
        <div><button class="btn btn-primary" type="submit">Send message</button></div>
        <p class="hint" id="formStatus" role="status" hidden></p>
      </form>
      <div class="sent" id="sent" hidden role="status"><h3>Thanks, your message is in</h3><p>We'll reply within one business day.</p></div>
    </details>
  </div>
  <aside class="contact-side">
    <div class="card offer"><span class="tag">What you get</span><h3>Your free assessment</h3><ul class="checks"><li><div>A review of your current systems and pain points</div></li><li><div>An honest view of whether Business Central fits, or what would fit better</div></li><li><div>The likely project size, timeline and license cost</div></li><li><div>Clear next steps, with no obligation</div></li></ul></div>
    <div class="card prep"><span class="tag">Prepare for your call</span><h3>ERP Readiness Checklist</h3><p>Fill it in with your team before the call to get more out of your 30 minutes.</p><a class="btn btn-ghost" {DL_ATTR}>Download the PDF</a></div>
    <div class="card"><span class="tag">Email</span><p class="mono" style="color:var(--ink);user-select:all">{esc(EMAIL)}</p></div>
    {phone_card}
  </aside>
</div></section>''')


# RESOURCES: ERP readiness checklist
CL_AREAS = [('Business goals and ownership', 'Why you need to change, the outcomes you expect and who makes decisions.'), ('Current systems and processes', 'What you use today, what stays and where spreadsheets fill the gaps.'), ('Finance and reporting', 'Chart of accounts, approvals, month-end close, tax and historical data.'), ('Inventory, purchasing and sales', 'Item data, costing, replenishment, pricing and traceability.'), ('Warehouse and fulfillment', 'Receiving to shipping, scanning, bins, carriers and 3PLs.'), ('Manufacturing and service', 'BOMs, routings, production, quality and service work.'), ('Data, integrations and technology', 'Data quality, ecommerce, EDI, CRM and security.'), ('People and change', 'Workshops, testing, training and keeping your team informed.'), ('Budget, timeline and scope', 'Costs, realistic dates, priorities and support after go-live.')]
CL_SCHEMA = {"@context": "https://schema.org", "@type": "DigitalDocument", "name": "ERP Readiness Checklist",
             "description": "A free, fillable 52-question checklist to prepare distributors and manufacturers for a Microsoft Dynamics 365 Business Central project.",
             "encodingFormat": "application/pdf", "url": URL + "downloads/q84-erp-readiness-checklist.pdf",
             "author": {"@id": URL + "#organization"}, "inLanguage": "en-US", "isAccessibleForFree": True}
add('resources/erp-readiness-checklist/', 'resources',
    'Free ERP Readiness Checklist for Business Central | Q84 Digital',
    'Download a free, fillable ERP Readiness Checklist. 52 questions across 9 areas help distributors and manufacturers prepare for a Business Central project.',
    page_head('Resources', '<a href="@/resources/">Resources</a> / ERP readiness checklist', 'Free ERP Readiness Checklist',
              'Find the gaps before you choose an ERP. 52 practical questions across 9 areas, written for distributors and manufacturers considering Microsoft Dynamics 365 Business Central.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap split cl-hero">
  <div class="stack">
    <span class="eyebrow">What it helps you do</span><h2>Get your team aligned before the first workshop</h2>
    {checks(['<strong>Spot gaps early.</strong> Mark each question Yes, Partly or No and see where decisions are missing.', '<strong>Get everyone involved.</strong> Finance, sales, purchasing, warehouse and IT each have their own section.', '<strong>Have a better first conversation.</strong> Bring it to your assessment and spend the time on what matters.'])}
    <div class="hero-actions"><a class="btn btn-primary" {DL_ATTR}>Download the checklist (PDF)</a></div>
    <p class="hint">Fillable PDF, 6 pages, US Letter. Fill it in on screen or print it. No email required.</p>
  </div>
  <a class="cl-cover" {DL_ATTR} aria-label="Download the ERP Readiness Checklist PDF"><img src="@/images/erp-checklist-cover.webp" alt="First page of the Q84 Digital ERP Readiness Checklist" width="640" height="828"></a>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What’s inside</span><h2>Nine areas every ERP project depends on</h2></div>
  <div class="grid g3">{''.join(f'<div class="card"><span class="num-badge">{i:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(CL_AREAS, 1))}</div>
  <p class="shot-note" style="margin-top:16px">It ends with a readiness summary, your top five open questions and what a good assessment should cover.</p>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">How to use it</span><h2>Three steps</h2></div>
  <ol class="steps steps-3">
    <li><h3>Download</h3><p>Save the PDF and share it with the people who run each area.</p></li>
    <li><h3>Fill it in</h3><p>Tick Yes, Partly or No and note owners and open questions.</p></li>
    <li><h3>Talk it through</h3><p>Bring it to a free 30-minute assessment and we’ll go through the gaps together.</p></li>
  </ol>
</div></section>
{cta('Bring your checklist to a free assessment', 'Pick a time for a 30-minute call. We’ll go through your answers and tell you honestly whether Business Central fits.')}''', [CL_SCHEMA],
    image=('og-erp-checklist.jpg', 'Q84 Digital free ERP Readiness Checklist: 52 questions across 9 areas'))

# RESOURCES index
add('resources/', 'resources',
    'Free Business Central & ERP Resources | Q84 Digital',
    'Free guides and checklists from Q84 Digital to help distributors and manufacturers plan, choose and implement Microsoft Dynamics 365 Business Central.',
    page_head('Resources', 'Resources', 'Free ERP resources',
              'Practical guides and checklists to help you plan, choose and implement Business Central. Free to download, no email required.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap">
  <div class="grid g3">
    <a class="card resource-card" href="{CHECKLIST_URL}">
      <img src="@/images/erp-checklist-cover.webp" alt="" width="640" height="828" loading="lazy">
      <span class="tag">Checklist · PDF</span><h3>ERP Readiness Checklist</h3>
      <p>52 questions across 9 areas to find the gaps before you choose an ERP. Fillable, 6 pages.</p>
      <span class="more">See what’s inside →</span></a>
    <a class="card resource-card" href="@/licensing/#calculator">
      <span class="resource-art">{icon('chart')}</span>
      <span class="tag">Tool</span><h3>License cost calculator</h3>
      <p>Estimate your monthly Business Central license cost from your number of users.</p>
      <span class="more">Estimate your costs →</span></a>
    <a class="card resource-card" href="@/blog/">
      <span class="resource-art">{icon('ledger')}</span>
      <span class="tag">Articles</span><h3>Business Central blog</h3>
      <p>Practical articles on ERP selection, inventory, warehousing and Business Central.</p>
      <span class="more">Read the blog →</span></a>
  </div>
</div></section>
{cta()}''')

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
<h2>Embedded videos</h2><p>Some pages include videos hosted on YouTube. Nothing loads from YouTube until you press play. When you do, the video plays from YouTube’s privacy-enhanced mode and YouTube’s privacy policy applies.</p>
<h2>Sharing</h2><p>We share information only with service providers that help us run this website and handle email, and only as needed to provide those services, or where the law requires it.</p>
<h2>Retention and your rights</h2><p>We keep inquiries for as long as needed to respond and manage any resulting work. You can ask to see, correct or delete your information at any time by emailing <span style="user-select:all">{esc(EMAIL)}</span>. Under Canada's PIPEDA you can also contact the Office of the Privacy Commissioner of Canada.</p>
</div></section>''')

# ---------------------------------------------------------------- render

def analytics():
    if not CFG.get('ga_id'):
        return ''
    gid = esc(CFG['ga_id'])
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{gid}');</script>'''

FAVICON = "data:image/svg+xml," + re.sub(r'\s+', ' ', '''<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%232563EB'/><text x='32' y='41' font-family='Arial,sans-serif' font-size='24' font-weight='700' fill='white' text-anchor='middle'>Q84</text></svg>''')

def breadcrumb_schema(p):
    m = re.search(r'<nav class="crumb"[^>]*>(.*?)</nav>', p['body'], re.S)
    if not m: return None
    items = []
    parts = m.group(1).split(' / ')
    for idx, part in enumerate(parts):
        a = re.search(r'<a href="([^"]+)">(.*?)</a>', part)
        if a: items.append((re.sub('<.*?>', '', a.group(2)).strip(), URL + a.group(1).replace('@/', '')))
        else:
            name = re.sub('<.*?>', '', part).strip()
            if name and idx == len(parts) - 1: items.append((name, None))
    if items and items[-1][1] is not None and items[-1][1] != URL + p['path']:
        items.append((p['title'].split(' | ')[0], None))
    if len(items) < 2: return None
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i, "name": html.unescape(n)}, **({"item": u} if u else {}))
        for i, (n, u) in enumerate(items, 1)]}

def render(p):
    canonical = URL + p['path']
    bc = breadcrumb_schema(p)
    if p.get('subnav'): p = dict(p, body=with_subnav(p['body']))
    if bc: p = dict(p, schema=p['schema'] + [bc])
    img, img_alt = p.get('image') or ('og-default.jpg', 'Q84 Digital: Microsoft Business Central for distribution and manufacturing')
    img_url = URL + 'images/' + img
    schema = ''.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in p['schema'])
    noindex = '' if CFG.get('allow_indexing', True) else '<meta name="robots" content="noindex, nofollow">\n'
    verify = noindex + (f'<meta name="google-site-verification" content="{esc(CFG["gsc_verification"])}">\n' if CFG.get('gsc_verification') else '')
    client = json.dumps({'email': EMAIL, 'formEndpoint': CFG.get('form_endpoint', ''), 'scheduler': CFG.get('scheduler', {})})
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
<meta property="og:image" content="{img_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(img_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img_url}">
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

SUBNAV_PAGES = {'business-central/', 'licensing/', 'implementation/', 'data-migration/', 'integrations/', 'support/', 'industries/distribution/', 'industries/manufacturing/'}
for p in PAGES:
    if p['path'] in SUBNAV_PAGES: p['subnav'] = True
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
