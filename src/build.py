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
LIVE_HOST = re.sub(r'^https?://|/.*$', '', URL)
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

_digits = re.sub(r'\D', '', CFG.get('phone') or '')
PHONE_TEL = ('+1' + _digits if len(_digits) == 10 else '+' + _digits) if _digits else ''  # e.g. +12532949237 for tel: links and schema

def icon(name):
    return f'<span class="icon"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg></span>'

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- shared parts

NAV = [
    ('business-central', 'Business Central', '@/business-central/', None),
    ('services', 'Services', None, [
        ('implementation', 'Implementation', '@/implementation/'),
        ('rescue', 'Rescue & recovery', '@/rescue/'),
        ('development', 'Development & AL extensions', '@/development/'),
        ('support', 'Support', '@/support/'),
        ('licensing', 'Licensing & pricing', '@/licensing/'),
    ]),
    ('migration', 'Migration', None, [
        ('migration', 'All migrations', '@/migration/'),
        ('mig-quickbooks', 'From QuickBooks', '@/migration/quickbooks/'),
        ('mig-gp', 'From Dynamics GP', '@/migration/dynamics-gp/'),
        ('mig-nav', 'From Dynamics NAV', '@/migration/dynamics-nav/'),
        ('mig-sage', 'From Sage 50 / Sage 100', '@/migration/sage/'),
        ('mig-sheets', 'From spreadsheets', '@/migration/spreadsheets/'),
    ]),
    ('industries', 'Industries', None, [
        ('distribution', 'Wholesale distribution', '@/industries/distribution/'),
        ('manufacturing', 'Manufacturing', '@/industries/manufacturing/'),
        ('ecommerce', 'E-commerce', '@/industries/ecommerce/'),
        ('service-industries', 'Professional services', '@/industries/professional-services/'),
    ]),
    ('integrations', 'Integrations', None, [
        ('integrations', 'All integrations', '@/integrations/'),
        ('int-shopify', 'Shopify', '@/integrations/shopify/'),
        ('int-edi', 'EDI', '@/integrations/edi/'),
        ('int-powerbi', 'Power BI reporting', '@/integrations/power-bi/'),
        ('int-wi', 'Warehouse Insight mobile WMS', '@/integrations/warehouse-insight/'),
    ]),
    ('guides', 'Guides', None, [
        ('guides', 'All guides', '@/guides/'),
        ('guide-cost', 'Implementation cost', '@/guides/implementation-cost/'),
        ('guide-timeline', 'Implementation timeline', '@/guides/implementation-timeline/'),
        ('cmp-netsuite', 'Business Central vs NetSuite', '@/compare/netsuite/'),
        ('cmp-intacct', 'Business Central vs Sage Intacct', '@/compare/sage-intacct/'),
        ('cmp-odoo', 'Business Central vs Odoo', '@/compare/odoo/'),
        ('checklist', 'ERP readiness checklist', '@/guides/erp-readiness-checklist/'),
        ('blog', 'Blog', '@/blog/'),
    ]),
    ('about', 'About', '@/about/', None),
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
        if not url: continue  # only show icons that have a profile to link to
        href = f'href="{esc(url)}" target="_blank" rel="noopener"'
        out.append(f'<a class="social" {href} aria-label="Q84 Digital on {label}"><svg viewBox="0 0 24 24" aria-hidden="true">{SOCIAL_SVG[key]}</svg></a>')
    return '<div class="socials">' + ''.join(out) + '</div>'

def footer():
    legal = f'Q84 Digital is operated by {esc(CFG["legal_name"])}. ' if CFG.get('legal_name') else ''
    phone = f'<li><a href="tel:{PHONE_TEL}">{esc(CFG["phone"])}</a></li>' if CFG.get('phone') else ''
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div class="stack" style="gap:12px">
        <a class="logo" href="@/"><span class="logo-mark">Q84</span>Q84 Digital</a>
        <p>Microsoft Dynamics 365 Business Central partner with offices in Vancouver, BC and Tacoma, WA, for distributors, manufacturers and service businesses, led by a senior supply chain consultant.</p>
        <ul style="list-style:none;padding:0;margin:0;display:grid;gap:4px"><li style="user-select:all">{esc(EMAIL)}</li>{phone}<li>Vancouver, British Columbia</li><li>Tacoma, Washington</li></ul>
        {social_links()}
      </div>
      <div><h4>Services</h4><ul><li><a href="@/implementation/">Implementation</a></li><li><a href="@/rescue/">Rescue &amp; recovery</a></li><li><a href="@/development/">Development</a></li><li><a href="@/support/">Support</a></li><li><a href="@/licensing/">Licensing &amp; pricing</a></li><li><a href="@/integrations/">Integrations</a></li></ul></div>
      <div><h4>Migration</h4><ul><li><a href="@/migration/quickbooks/">From QuickBooks</a></li><li><a href="@/migration/dynamics-gp/">From Dynamics GP</a></li><li><a href="@/migration/dynamics-nav/">From Dynamics NAV</a></li><li><a href="@/migration/sage/">From Sage</a></li><li><a href="@/migration/spreadsheets/">From spreadsheets</a></li></ul></div>
      <div><h4>Industries</h4><ul><li><a href="@/industries/distribution/">Distribution</a></li><li><a href="@/industries/manufacturing/">Manufacturing</a></li><li><a href="@/industries/ecommerce/">E-commerce</a></li><li><a href="@/industries/professional-services/">Professional services</a></li><li><a href="@/business-central-partner-tacoma/">Tacoma &amp; Seattle</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="@/about/">About</a></li><li><a href="@/guides/">Guides</a></li><li><a href="@/blog/">Blog</a></li><li><a href="@/contact/">Contact</a></li><li><a href="@/privacy/">Privacy</a></li></ul></div>
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

def page_head(title, crumb, h1, lede, button=True, art=None):
    btn = f'<div class="hero-actions"><a class="btn btn-primary" {CTA_ATTR}>{CTA_LABEL}</a></div>' if button else ''
    if art:
        # art = (file in images/, alt text); keep '</div></div>\n' only at the very end, with_subnav looks for it
        src, alt = art
        return f'''<div class="page-head"><div class="wrap page-head-grid"><div class="stack">
<nav class="crumb" aria-label="Breadcrumb"><a href="@/">Home</a> / {crumb}</nav>
<h1>{h1}</h1>
<p class="lede">{lede}</p>{btn}
</div><figure class="page-head-art"><img src="@/images/{src}" alt="{esc(alt)}" width="800" height="595" fetchpriority="high"></figure></div></div>'''
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
  <p class="shot-note" id="shotNote" style="margin-top:20px">Screens show Business Central with example data from Microsoft’s demo company.</p>
</div>
</section>'''

FAQ_HOME = [
    ('What is Microsoft Dynamics 365 Business Central?', 'It’s Microsoft’s cloud ERP for small and midsize businesses. It brings accounting, inventory, sales, purchasing, warehousing and reporting into one system that works with Microsoft 365.', None),
    ('Is Business Central right for a distribution or inventory-heavy business?', 'For most small and midsize distributors, yes. It handles multi-location stock, purchasing, bins, picking and shipping. If your warehouse is very high-volume or complex, we’ll tell you whether an extension or Dynamics 365 Supply Chain Management fits better.', ('@/business-central/#fit', 'Is Business Central enough?')),
    ('How much does Business Central cost?', 'Licenses are a monthly per-user subscription from Microsoft. Implementation is a one-time project quoted after a free discovery call. Our calculator estimates your license cost in a minute.', ('@/licensing/', 'Estimate your costs')),
    ('How long does implementation take?', 'A focused finance and inventory rollout usually takes a few months. Projects with manufacturing, advanced warehousing or several integrations take longer. You get a timeline after discovery.', ('@/implementation/', 'How implementation works')),
    ('Can Business Central replace QuickBooks?', 'Yes. Companies usually move when they need proper inventory, multiple companies or better reporting. We handle the data migration.', ('@/migration/quickbooks/', 'QuickBooks to Business Central')),
    ('Can Business Central integrate with Shopify?', 'Yes. Business Central has a Shopify connector, and we build other integrations through its APIs.', ('@/integrations/shopify/', 'Shopify integration')),
    ('Are you a Microsoft partner?', CFG.get('partner_statement') or 'Q84 Digital is an independent Business Central consultancy. Microsoft licenses are billed by Microsoft or a Microsoft licensing partner. We help you choose the right plan, set it up and keep it right-sized as you grow.', ('@/licensing/', 'Licensing & pricing')),
    ('Do you only work with companies in Tacoma?', 'No. We have offices in Vancouver, BC and Tacoma, WA, work on site across the Vancouver and Seattle–Tacoma areas, and work remotely with companies anywhere in the US and Canada. Business Central is a cloud system, so most project work happens online either way.', ('@/business-central-partner-tacoma/', 'Business Central in Tacoma & Seattle')),
    ('Who will I actually work with?', 'Oleh Karnaukhov, the founder. Q84 Digital is senior-led, so the person who scopes your project is the person who delivers it.', ('@/about/', 'About Q84 Digital')),
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
    "address": [{"@type": "PostalAddress", "addressLocality": "Vancouver", "addressRegion": "BC", "addressCountry": "CA"},
                {"@type": "PostalAddress", "addressLocality": "Tacoma", "addressRegion": "WA", "addressCountry": "US"}],
    "@id": URL + "#organization",
    "logo": URL + "images/logo.png", "image": URL + "images/og-default.jpg",
    "founder": {"@id": URL + "#oleh-karnaukhov"},
    "knowsAbout": ["Microsoft Dynamics 365 Business Central", "Dynamics 365 Supply Chain Management", "ERP implementation", "Warehouse management", "ERP integration"],
}
if CFG.get('phone'):
    ORG_SCHEMA['telephone'] = PHONE_TEL
if CFG.get('social_linkedin_url'):
    ORG_SCHEMA['sameAs'] = [u for u in (CFG.get('social_linkedin_url'), CFG.get('social_youtube_url')) if u]

WEBSITE_SCHEMA = {
    "@context": "https://schema.org", "@type": "WebSite", "@id": URL + "#website",
    "url": URL, "name": "Q84 Digital", "inLanguage": "en-US",
    "publisher": {"@id": URL + "#organization"},
}

PERSON_SCHEMA = {
    "@context": "https://schema.org", "@type": "Person", "@id": URL + "#oleh-karnaukhov",
    "name": "Oleh Karnaukhov", "jobTitle": "Founder and lead consultant",
    "description": "Senior Microsoft Dynamics consultant with more than 15 years of ERP and supply chain experience.",
    "url": URL + "about/", "worksFor": {"@id": URL + "#organization"},
    "knowsAbout": ["Microsoft Dynamics 365 Business Central", "Dynamics 365 Supply Chain Management", "Warehouse management", "Transportation management", "Dynamics 365 Customer Engagement", "Dynamics 365 Field Service", "ERP integration"],
}
if LINKEDIN:
    PERSON_SCHEMA["sameAs"] = [LINKEDIN]
if CFG.get('consultant_photo'):
    PERSON_SCHEMA["image"] = URL + "images/" + CFG['consultant_photo']

# ---------------------------------------------------------------- pages

PAGES = []

CHECKLIST_URL = '@/guides/erp-readiness-checklist/'
CHECKLIST_PDF = '@/downloads/q84-erp-readiness-checklist.pdf'
DL_ATTR = f'href="{CHECKLIST_PDF}" download data-download="erp-readiness-checklist"'
def checklist_promo(heading='Is your business ready for a new ERP?', text='Our free ERP Readiness Checklist covers 52 questions across 9 areas, from inventory and warehouse to data and budget. Fill it in with your team, then bring it to your assessment.'):
    return f'''<section class="promo-section"><div class="wrap"><div class="promo">
  <a class="promo-cover" href="{CHECKLIST_URL}" tabindex="-1" aria-hidden="true"><img src="@/images/erp-checklist-cover.webp" alt="" width="640" height="828" loading="lazy"></a>
  <div class="promo-copy"><span class="eyebrow">Free download</span><h2>{heading}</h2><p>{text}</p>
    <div class="hero-actions"><a class="btn btn-primary" {DL_ATTR}>Download the checklist (PDF)</a><a class="btn btn-ghost" href="{CHECKLIST_URL}">See what’s inside</a></div>
    <p class="hint">Free fillable PDF, 6 pages. Enter your email to download.</p></div>
</div></div></section>'''
def add(path, nav, title, desc, body, schema=None, image=None, subnav=False):
    PAGES.append(dict(path=path, nav=nav, title=title, desc=desc, body=body, schema=schema or [], image=image, subnav=subnav))

def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(t).lower()).strip('-')

NAV_SHORT = {'What clients say': 'Reviews', 'Watch the overview': 'Overview', 'Choosing the right ERP': 'Is it enough?', 'Moving from QuickBooks?': 'From QuickBooks', 'Where you\u2019re coming from': 'Source systems', 'How Business Central helps': 'Features', 'Is it the right fit?': 'Fit', 'Marketing agencies': 'Agencies', 'Medical and aesthetic clinics': 'Clinics', 'Who we work with': 'Clients', 'Construction and restoration': 'Construction', 'Step by step': 'Steps',
             'What moves where': 'Mapping', 'What changes': 'Mapping', 'Why companies move': 'Why move', 'Why now': 'Why now', 'Our process': 'Process', 'Two paths': 'Paths',
             'Warning signs': 'Signs', 'How we fix it': 'How we fix it', 'Root causes': 'Causes', 'Local partner': 'Local', 'Who we help': 'Industries', 'Service area': 'Service area',
             'What we do': 'Services', 'What we build': 'What we build', 'Our approach': 'Approach', 'What syncs': 'What syncs', 'Beyond the basics': 'More',
             'Common documents': 'Documents', 'Why it matters': 'Why it matters', 'Two options': 'Options', 'What gets scanned': 'Processes', 'Before scanning': 'Prerequisites',
             'What we set up': 'Setup', 'Good reports start in Business Central': 'Setup tips', 'Typical ranges': 'Ranges', 'Cost drivers': 'Drivers', 'Keeping costs down': 'Saving money',
             'Phase by phase': 'Phases', 'Parcel shipping': 'Shipping', 'What we help with': 'Services', 'Ways to work with us': 'Plans', 'What slows projects down': 'Delays', 'Choosing a go-live date': 'Go-live date', 'Worked example': 'Example'}
def with_subnav(body):
    # Give each labelled section an id and build a floating in-page menu from the labels
    items, used = [], set()
    def fix(m):
        attrs, inner = m.group(1), m.group(2)
        if 'promo-section' in attrs or 'cta-section' in attrs or 'data-nosubnav' in attrs: return m.group(0)
        e = re.search(r'class="eyebrow">(.*?)<', inner)
        if not e: return m.group(0)
        idm = re.search(r'id="([^"]+)"', attrs)
        sid = idm.group(1) if idm else slug(e.group(1))
        while sid in used: sid += '-2'
        used.add(sid)
        items.append((sid, NAV_SHORT.get(html.unescape(e.group(1)), e.group(1))))
        if not idm: attrs = attrs + f' id="{sid}"'
        return f'<section{attrs}>{inner}'
    body = re.sub(r'<section([^>]*)>((?:(?!<section).){0,600})', fix, body, flags=re.S)  # look ahead only within this section
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
HERO_ART = (f'''<figure class="hero-art"><img id="heroImg" src="@/images/{HERO_SET[0][0]}" alt="{esc(HERO_SET[0][1])}" width="1024" height="1024" fetchpriority="high"><script>(function(){{var l={_hero_list},k='q84hero',p=-1;try{{var v=sessionStorage.getItem(k);if(v!==null)p=+v}}catch(e){{}}if(p<0){{try{{sessionStorage.setItem(k,0)}}catch(e){{}}return}}var i=(p+1)%l.length;try{{sessionStorage.setItem(k,i)}}catch(e){{}}var m=document.getElementById('heroImg');m.alt=l[i][1];m.src=l[i][0];}})();</script></figure>''' if HERO_IMG else '')

# HOME

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
    TESTIMONIALS = f'''<section><div class="wrap"><div class="section-head"><span class="eyebrow">What clients say</span><h2>In their words</h2></div><div class="grid {'g2' if len(testimonials) == 2 else 'g3'}">{q}</div></div></section>'''

impl_range = CFG.get('implementation_range')
impl_text = (f'Most implementations fall between {esc(impl_range)}, depending on scope. You get a fixed quote after discovery.'
             if impl_range else 'Quoted as a fixed scope after discovery, based on modules, data, integrations and companies.')

add('', 'home',
    'Business Central Partner | Vancouver & Tacoma | Q84 Digital',
    'Senior-led Microsoft Business Central partner for distributors and manufacturers: implementation, migration from QuickBooks, GP and NAV, and support.',
    f'''<section class="hero"><div class="wrap">
  <div class="{HERO_CLASS}"><div class="hero-center">
    <a class="announce" href="{CHECKLIST_URL}"><span class="announce-tag">New</span><span>Free ERP Readiness Checklist for Business Central projects</span><span class="announce-link">Download \u2192</span></a>
    <h1>Take control of your inventory, operations and finances <span class="h1-accent">with Microsoft Business Central</span></h1>
    <p class="lede lede-strong">Replace disconnected accounting, inventory and warehouse systems with one connected ERP platform.</p>
    <p class="lede">Q84 Digital is a Business Central partner with offices in Vancouver, BC and Tacoma, WA. We help distributors, manufacturers and service businesses across the Pacific Northwest, the US and Canada implement Microsoft Dynamics 365 Business Central, migrate their data and connect the systems they rely on.</p>
    <div class="hero-actions"><a class="btn btn-primary" {CTA_ATTR}>{CTA_LABEL}</a><a class="btn btn-ghost" href="#tour">See how it works</a></div>
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
    <button class="chip" role="tab" id="itab-ecom" aria-controls="ipanel-ecom" aria-selected="false" tabindex="-1">E-commerce</button>
    <button class="chip" role="tab" id="itab-svc" aria-controls="ipanel-svc" aria-selected="false" tabindex="-1">Professional services</button>
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
  <div class="ind-panel" role="tabpanel" id="ipanel-ecom" aria-labelledby="itab-ecom" hidden>
    <figure class="ind-photo"><img src="@/images/hero-packing-station.webp" alt="Packing station with boxes, tape and a shipping label printer" width="1024" height="1024" loading="lazy"></figure>
    <div class="stack"><h3>Sell on every channel from one stock position</h3>
      <p>Shopify and marketplace orders flow into Business Central, stock syncs back to every store, and payouts reconcile without a spreadsheet. Fulfill from your own warehouse or a 3PL and see true margin after fees, shipping and returns.</p>
      <div class="hero-actions"><a class="btn btn-primary" href="@/industries/ecommerce/">See e-commerce features</a></div></div>
  </div>
  <div class="ind-panel" role="tabpanel" id="ipanel-svc" aria-labelledby="itab-svc" hidden>
    <figure class="ind-photo"><img src="@/images/industry-services.webp" alt="Laptop with a project chart, an alarm clock, a hard hat and a clipboard with an invoice" width="1184" height="880" loading="lazy"></figure>
    <div class="stack"><h3>Bill every hour and know which jobs make money</h3>
      <p>For marketing agencies, medical and aesthetic clinics, and construction and restoration companies. Track time, projects, deposits and job costs in the same system as your books, invoice faster, and see profit by client, job and contract.</p>
      <div class="hero-actions"><a class="btn btn-primary" href="@/industries/professional-services/">See professional services features</a></div></div>
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
    <a class="fitem" href="@/migration/">{icon('migrate')}<h3>Migration</h3><p>Clean, verified data moved from QuickBooks, Dynamics GP, Dynamics NAV, Sage or spreadsheets.</p><span class="more">Migration \u2192</span></a>
    <a class="fitem" href="@/rescue/">{icon('support')}<h3>Rescue &amp; recovery</h3><p>Stalled or struggling Business Central project? We find what\u2019s wrong and get it back on track.</p><span class="more">Rescue &amp; recovery \u2192</span></a>
    <a class="fitem" href="@/integrations/">{icon('link')}<h3>Integrations &amp; development</h3><p>Shopify, EDI, Power BI, warehouse scanning and custom AL extensions.</p><span class="more">Integrations \u2192</span></a>
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
{cta('Find out if Business Central fits your business')}''', [WEBSITE_SCHEMA, ORG_SCHEMA, PERSON_SCHEMA, faq_schema(FAQ_HOME)])

# BUSINESS CENTRAL
add('business-central/', 'business-central',
    'What Is Business Central? Features & Fit | Q84 Digital',
    'What Business Central does, its core features for finance, inventory, sales, purchasing and warehousing, and how to tell whether it fits your operations.',
    page_head('Business Central', 'Business Central', 'Microsoft Dynamics 365 Business Central',
              'One cloud ERP for finance, inventory, sales, purchasing and warehousing, built for small and midsize companies and connected to Microsoft 365.', art=('page-business-central.webp', 'Illustration of a cloud connected to a ledger, a box, a shopping cart and a bar chart')) + f'''
<section id="overview-video"><div class="wrap split video-split">
  <div class="stack"><span class="eyebrow">Watch the overview</span><h2>See Business Central in three minutes</h2>
  <p class="lede">Microsoft\u2019s official overview of Business Central: how finance, sales, inventory and operations come together in one system.</p>
  {checks(['Connected finance, sales and operations', 'Built-in Microsoft 365 and Copilot features', 'Runs in the cloud, accessible anywhere'])}</div>
  <figure class="yt" style="margin:0">
    <button class="video-poster" type="button" data-youtube="X7B99e3mNfI" data-title="Microsoft Dynamics 365 Business Central Overview" aria-label="Play video: Microsoft Dynamics 365 Business Central Overview, 3 minutes 13 seconds">
      <img src="https://i.ytimg.com/vi/X7B99e3mNfI/hqdefault.jpg" alt="Microsoft Dynamics 365 Business Central overview video" loading="lazy" width="480" height="360">
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
    'Business Central Implementation Partner | Q84 Digital',
    'A senior-led Business Central implementation partner: discovery, design, build, data migration, testing and go-live, delivered by the consultant who scopes it.',
    page_head('Implementation', 'Services / Implementation', 'Business Central implementation partner',
              'A structured rollout that gets your team working in Business Central with clean data, tested processes and support after go-live.', art=('page-implementation.webp', 'Illustration of a laptop with a project plan, steps leading to a flag, a blueprint and a gear')) + f'''
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
  <div class="stack"><span class="eyebrow">Timeline &amp; cost</span><h2>What drives the size of a project</h2><p class="lede">You get a fixed scope and estimate after discovery, based on your business rather than a guess. Read our guides to <a href="@/guides/implementation-cost/">implementation cost</a> and <a href="@/guides/implementation-timeline/">how long it takes</a>, or <a href="@/licensing/#calculator">try the cost estimator</a>.</p></div>
  {checks(['<strong>Modules in scope.</strong> Finance only, or also inventory, warehousing and manufacturing.', '<strong>Companies and locations.</strong> Multi-entity and multi-warehouse setups take more work.', '<strong>Data volume and quality.</strong> Clean data loads faster than messy data.', '<strong>Integrations.</strong> Each connected system adds design and testing time.', '<strong>Custom development.</strong> Extensions are scoped and estimated separately.'])}
</div></section>
{checklist_promo('Prepare your team for implementation', 'Use our free ERP Readiness Checklist to find gaps in goals, processes, data and ownership before the project starts. It makes discovery faster and scope clearer.')}
{cta('Planning a Business Central project?')}''')

# LICENSING
add('licensing/', 'licensing',
    'Business Central Essentials vs Premium Pricing | Q84 Digital',
    'Business Central Essentials vs Premium: license prices, what each plan includes, Team Members licenses, and a cost calculator for your own users.',
    page_head('Licensing', 'Services / Licensing &amp; pricing', 'Business Central pricing: Essentials vs Premium',
              'What you’ll pay Microsoft for licenses, what drives implementation cost, and a quick calculator for your own numbers.', button=False, art=('page-licensing.webp', 'Illustration of three license cards of increasing size, a key and a stack of coins')) + '''
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
  <div class="section-head"><span class="eyebrow">License types</span><h2>Business Central Essentials vs Premium</h2><p class="lede">Essentials covers finance, sales, purchasing, inventory, warehousing and projects, which is enough for most distributors and service businesses. Premium adds manufacturing and service management. Most companies combine a few full users with lower-cost Team Members licenses for people who only view data or do light tasks. All full users in a company must be on the same plan.</p></div>
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
<section><div class="wrap"><div class="note">Licenses are only part of the budget. See our guide to <a href="@/guides/implementation-cost/">Business Central implementation cost</a> for the full picture.</div></div></section>
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

def related(title, items, band=False):
    # items: (href, heading, text) — a row of link cards to sibling pages
    cards = ''.join(f'<a class="fitem" href="{h}"><h3>{t}</h3><p>{d}</p><span class="more">Read more →</span></a>' for h, t, d in items)
    return f'''<section data-nosubnav{' class="band"' if band else ''}><div class="wrap">
  <div class="section-head"><span class="eyebrow">Related</span><h2>{title}</h2></div>
  <div class="fgrid">{cards}</div>
</div></section>'''

# DATA MIGRATION
FAQ_MIG = [
    ('How long does a data migration take?', 'For most small and midsize businesses the migration runs alongside the implementation over three to six weeks, with at least two trial loads before the final cutover. The final load itself usually happens over a weekend or at a month-end.', None),
    ('Do we have to bring over all our historical transactions?', 'Usually not. Most companies bring over open items, balances and a summary of past results, and keep the old system or an export for reference. Detailed history can be migrated, but it adds cost and rarely pays off.', None),
    ('Who cleans up the data?', 'We do the heavy lifting: finding duplicates, gaps and inconsistent codes, and fixing what can be fixed automatically. Your team makes the business decisions, such as which customers are inactive and which item numbers to keep.', None),
    ('Can we keep using our old system during the project?', 'Yes. You keep working as normal until cutover. We take a final extract at an agreed point, load it, reconcile it and then you switch to Business Central.', None),
]
add('migration/', 'migration',
    'Business Central Data Migration Services | Q84 Digital',
    'Move to Business Central with clean, reconciled data. Migration from QuickBooks, Dynamics GP, Dynamics NAV, Sage, other ERPs and spreadsheets.',
    page_head('Migration', 'Migration', 'Business Central data migration',
              'Move customers, vendors, items, open documents and balances into Business Central, then reconcile everything so your numbers match on day one.', art=('page-migration.webp', 'Illustration of boxes and folders moving from an old computer to a laptop and the cloud')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where you're coming from</span><h2>Systems we migrate from</h2>
  <p class="lede">Every source system has its own quirks. QuickBooks stores items and customers differently from Business Central, Dynamics GP has its own migration tools, and Dynamics NAV often carries years of custom code. We plan the move around the system you actually have.</p></div>
  <div class="fgrid">
    <a class="fitem" href="@/migration/quickbooks/">{icon('migrate')}<h3>QuickBooks</h3><p>QuickBooks Online and Desktop: customers, vendors, items, open items and balances.</p><span class="more">QuickBooks to Business Central \u2192</span></a>
    <a class="fitem" href="@/migration/dynamics-gp/">{icon('migrate')}<h3>Dynamics GP</h3><p>Microsoft’s GP-to-Business Central migration tools, plus the cleanup they don’t do.</p><span class="more">GP to Business Central \u2192</span></a>
    <a class="fitem" href="@/migration/dynamics-nav/">{icon('migrate')}<h3>Dynamics NAV</h3><p>Upgrade or re-implement, depending on your version and custom code.</p><span class="more">NAV to Business Central \u2192</span></a>
    <a class="fitem" href="@/migration/sage/">{icon('migrate')}<h3>Sage 50 &amp; Sage 100</h3><p>Master data, open transactions and balances, mapped to Business Central.</p><span class="more">Sage to Business Central \u2192</span></a>
    <a class="fitem" href="@/migration/spreadsheets/">{icon('migrate')}<h3>Spreadsheets</h3><p>Item lists, stock and customer data pulled out of Excel and cleaned up.</p><span class="more">Spreadsheets to Business Central \u2192</span></a>
    <div class="fitem">{icon('migrate')}<h3>Other ERPs</h3><p>Acumatica, Epicor, homegrown systems and more, using structured templates and validation.</p></div>
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
<section id="history"><div class="wrap split">
  <div class="stack"><span class="eyebrow">How much history?</span><h2>Choose what to bring over</h2><p class="lede">Bringing everything over sounds safe but often means moving years of messy data. Most companies choose the middle option.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Option</th><th>What moves</th><th>Best for</th></tr></thead>
    <tbody>
      <tr><td>Open items only</td><td>Master data, open orders, open receivables and payables, stock and opening balances</td><td>Fast, clean starts</td></tr>
      <tr><td>Plus summary history</td><td>The above, plus monthly general ledger balances for one or two prior years</td><td>Year-over-year reporting in Business Central</td></tr>
      <tr><td>Detailed history</td><td>Individual historical transactions</td><td>Specific audit or reporting needs. Quoted separately.</td></tr>
    </tbody></table></div>
</div></section>
{faq_section(FAQ_MIG)}
{cta('Planning your move to Business Central?')}''', [faq_schema(FAQ_MIG)])

# MIGRATION PAGES
MIG_RELATED = lambda skip, band=False: related('Other migrations', band=band, items=[x for x in [
    ('@/migration/quickbooks/', 'From QuickBooks', 'QuickBooks Online and Desktop to Business Central.'),
    ('@/migration/dynamics-gp/', 'From Dynamics GP', 'Microsoft’s GP migration tools, plus the cleanup they don’t do.'),
    ('@/migration/dynamics-nav/', 'From Dynamics NAV', 'Upgrade or re-implement, depending on version and code.'),
    ('@/migration/sage/', 'From Sage 50 &amp; Sage 100', 'Mapping Sage data and modules to Business Central.'),
    ('@/migration/spreadsheets/', 'From spreadsheets', 'Turning Excel lists into clean master data.')] if x[0] != skip][:3])

# QUICKBOOKS
FAQ_QB = [
    ('Can we migrate from both QuickBooks Online and QuickBooks Desktop?', 'Yes. The data we bring over is the same: chart of accounts, customers, vendors, items, open invoices and bills, and balances. Only the way we extract it differs.', None),
    ('What happens to payroll?', 'Business Central doesn’t include US payroll. Most companies keep a payroll provider such as ADP or Gusto and post payroll to Business Central as a journal, or connect it with an app.', None),
    ('Do QuickBooks classes and locations carry over?', 'Yes, as dimensions in Business Central. Dimensions do the same job with more flexibility, so you can report profit by department, location or project.', None),
    ('Should we bring our transaction history?', 'Usually just open items, balances and monthly totals for one or two prior years. Keep QuickBooks or an export for looking up old invoices.', ('@/migration/#history', 'Choosing how much history')),
]
add('migration/quickbooks/', 'mig-quickbooks',
    'QuickBooks to Business Central Migration | Q84 Digital',
    'Move from QuickBooks Online or Desktop to Microsoft Dynamics 365 Business Central with clean data, real inventory and balances that reconcile to the cent.',
    page_head('Migration', '<a href="@/migration/">Migration</a> / QuickBooks', 'QuickBooks to Business Central migration',
              'You’ve outgrown QuickBooks. We move your accounts, customers, vendors, items and balances into Business Central, then prove the numbers match.', art=('page-mig-quickbooks.webp', 'Illustration of an accounting ledger and calculator, boxes on a pallet and a laptop with an inventory list')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Why companies move</span><h2>Signs you’ve outgrown QuickBooks</h2><p class="lede">QuickBooks is a good accounting system for a small company. It wasn’t built to run inventory, warehouses and several entities. For a closer look, read <a href="@/blog/signs-you-have-outgrown-quickbooks/">seven signs your distribution business has outgrown QuickBooks</a>.</p></div>
  {checks(['<strong>Inventory lives in spreadsheets.</strong> Stock and costs are tracked outside your books. <a href="@/migration/spreadsheets/">We move those too.</a>', '<strong>More than one location or company.</strong> Consolidation and inter-company work take days.', '<strong>Month-end takes a week.</strong> Reports are rebuilt in Excel every month.', '<strong>File size and speed.</strong> QuickBooks Desktop slows down or hits its limits.', '<strong>No real controls.</strong> Approvals, user permissions and audit trails are thin.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What moves where</span><h2>How QuickBooks maps to Business Central</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>In QuickBooks</th><th>In Business Central</th><th>What to watch</th></tr></thead>
    <tbody>
      <tr><td>Chart of accounts</td><td>General ledger accounts</td><td>A good time to simplify. Many QuickBooks accounts become dimensions instead.</td></tr>
      <tr><td>Classes and locations</td><td>Dimensions</td><td>Agree the reporting you want before mapping.</td></tr>
      <tr><td>Customers and vendors</td><td>Customers and vendors with posting groups</td><td>Duplicates and inactive records cleaned up first.</td></tr>
      <tr><td>Items (inventory, non-inventory, service)</td><td>Items, with costing method and units of measure</td><td>Stock by location usually comes from spreadsheets and a physical count.</td></tr>
      <tr><td>Sales tax items</td><td>Tax areas, groups and jurisdictions</td><td>Set up per state; consider a tax engine if you ship to many states.</td></tr>
      <tr><td>Open invoices and bills</td><td>Open customer and vendor ledger entries</td><td>Reconciled to QuickBooks aging reports.</td></tr>
      <tr><td>Trial balance</td><td>Opening balances</td><td>Matched to the cent at cutover.</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap">
  {worked('Moving a 25-person distributor off QuickBooks Desktop',
          'A distributor runs accounting in QuickBooks Desktop with around 1,800 customers. Its 4,000 items and stock levels for two warehouses live in spreadsheets, and month-end takes a week of reconciling.',
          [('Weeks 1 to 2', 'Map QuickBooks customers, vendors and accounts to Business Central. Merge the item spreadsheets into one list and agree cleansing rules with the owner.'),
           ('Week 3', 'First trial load into a test company. Duplicate customers and inconsistent unit-of-measure codes are found and fixed.'),
           ('Week 4', 'Finance posts test invoices and payments. The warehouse lead checks stock by location and bin.'),
           ('Week 5', 'Second trial load. Receivables, payables and the trial balance reconcile to QuickBooks.'),
           ('Cutover weekend', 'Physical stock count, final load of open items and opening balances, and sign-off before Monday trading.')],
          'The company starts in Business Central with balances that match QuickBooks to the cent, one item list and stock it can trust, with no gap in trading.')}
</div></section>
{faq_section(FAQ_QB, 'QuickBooks migration questions')}
{MIG_RELATED('@/migration/quickbooks/')}
{cta('Ready to move off QuickBooks?', 'Book a free 30-minute call. We’ll look at your QuickBooks setup and tell you what the move involves.')}''', [faq_schema(FAQ_QB)])

# DYNAMICS GP
FAQ_GP = [
    ('When does Microsoft stop supporting Dynamics GP?', 'Microsoft has stopped selling Dynamics GP to new customers and has announced that product support, including tax and regulatory updates and technical support, ends on December 31, 2029. Security patches, if needed, continue until April 30, 2031. Check Microsoft’s Dynamics GP lifecycle page for the latest dates.', None),
    ('Can we bring our GP history?', 'Yes. Microsoft’s migration brings summary account history and can add a read-only snapshot of detailed historical transactions, so you can look up old GP documents inside Business Central.', None),
    ('What happens to our GP add-ons?', 'Each third-party GP product needs a decision: a standard Business Central feature, an AppSource app, or a small extension. We list them all during discovery so nothing is missed.', None),
    ('Is this an upgrade or a new implementation?', 'It’s a new implementation with a guided data migration. Business Central works differently from GP, so we set it up around how you work today rather than copying GP’s structure.', None),
]
add('migration/dynamics-gp/', 'mig-gp',
    'Migrate from Dynamics GP to Business Central | Q84 Digital',
    'Move from Dynamics GP to Business Central before GP support ends: Microsoft’s migration tools, segments to dimensions, history and add-on replacements.',
    page_head('Migration', '<a href="@/migration/">Migration</a> / Dynamics GP', 'Dynamics GP to Business Central migration',
              'Microsoft is retiring Dynamics GP. Business Central is its natural successor, and Microsoft provides tools to move your data. We plan the move and handle what the tools don’t.', art=('page-mig-gp.webp', 'Illustration of an old server and filing cabinet sending folders to the cloud and a laptop')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Why now</span><h2>Why GP customers are moving</h2><p class="lede">Microsoft has stopped selling Dynamics GP to new customers and has announced an end date for product support. Planning a move now means you choose the timing instead of the deadline choosing it for you.</p></div>
  {checks(['<strong>Support has an end date.</strong> Tax updates and technical support stop on December 31, 2029, and security patches stop after April 30, 2031.', '<strong>Fewer GP specialists.</strong> Finding consultants and add-on vendors gets harder each year.', '<strong>Cloud and Microsoft 365.</strong> Business Central runs in the cloud and works with Outlook, Excel and Teams.', '<strong>Microsoft’s migration path.</strong> Business Central includes tools built specifically to bring GP data across.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What changes</span><h2>How GP maps to Business Central</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>In Dynamics GP</th><th>In Business Central</th><th>What to watch</th></tr></thead>
    <tbody>
      <tr><td>Account segments</td><td>G/L accounts plus dimensions</td><td>Decide which segments become dimensions before migrating.</td></tr>
      <tr><td>Customers, vendors, items</td><td>Customers, vendors, items</td><td>Clean up inactive records and item classes first.</td></tr>
      <tr><td>Open receivables and payables</td><td>Open ledger entries</td><td>Reconciled to GP aging reports.</td></tr>
      <tr><td>Checkbooks</td><td>Bank accounts</td><td>Bank reconciliation starts fresh at cutover.</td></tr>
      <tr><td>Historical transactions</td><td>Summary history plus an optional read-only snapshot</td><td>Choose how much detail you really need.</td></tr>
      <tr><td>SmartLists and Management Reporter</td><td>Lists, Excel, financial reports and Power BI</td><td>Rebuild the reports people actually use, not all of them.</td></tr>
      <tr><td>Third-party add-ons</td><td>Standard features, AppSource apps or extensions</td><td>List every add-on early; this drives scope.</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our process</span><h2>A GP migration in five steps</h2></div>
  {checks(['<strong>Inventory your GP.</strong> Modules, add-ons, customizations, reports and integrations in use today.', '<strong>Design Business Central.</strong> Chart of accounts, dimensions, posting groups and processes set up for how you work now.', '<strong>Run Microsoft’s migration.</strong> Master data, open transactions and history brought across into a test company.', '<strong>Test and reconcile.</strong> Your team runs real processes and signs off balances against GP.', '<strong>Cut over.</strong> Final migration at a period end, with hands-on support for the first close.'])}
</div></section>
{faq_section(FAQ_GP, 'Dynamics GP migration questions')}
{MIG_RELATED('@/migration/dynamics-gp/')}
{cta('Planning your move off Dynamics GP?', 'Book a free 30-minute call to talk through your GP setup, add-ons and timing.')}''', [faq_schema(FAQ_GP)])

# DYNAMICS NAV
FAQ_NAV = [
    ('Can we upgrade NAV directly to Business Central online?', 'Not in one step. NAV 2018 and earlier versions first need upgrading to a Business Central on-premises version, then Microsoft’s cloud migration moves the data online. Older NAV versions often get a fresh implementation with data migration instead, which can be quicker and cleaner.', None),
    ('What happens to our NAV customizations?', 'Old C/AL code can’t run in Business Central online. Each customization is either replaced with a standard feature, replaced with an AppSource app, or rewritten as an AL extension. Many turn out to be unnecessary.', ('@/development/', 'AL development')),
    ('Is NAV still supported?', 'Every version of Dynamics NAV is past mainstream support. NAV 2018, the last version, reaches the end of extended support on January 11, 2028. Check Microsoft’s lifecycle pages for your exact version.', None),
    ('Should we move to the cloud or stay on-premises?', 'Most companies choose Business Central online: Microsoft handles hosting, updates and backups. On-premises still exists for specific needs, and we’ll discuss the trade-offs with you.', None),
]
add('migration/dynamics-nav/', 'mig-nav',
    'Dynamics NAV to Business Central Upgrade | Q84 Digital',
    'Upgrade from Microsoft Dynamics NAV to Business Central: upgrade or re-implement, what happens to C/AL customizations, and moving to the cloud.',
    page_head('Migration', '<a href="@/migration/">Migration</a> / Dynamics NAV', 'Dynamics NAV to Business Central upgrade',
              'Business Central is the modern version of NAV. Getting there depends on your NAV version and how much custom code you carry. We’ll help you choose the right path.', art=('page-mig-nav.webp', 'Illustration of steps leading from an old monitor up to a modern laptop')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Two paths</span><h2>Upgrade or re-implement?</h2><p class="lede">There’s no single right answer. The choice depends on your version, your customizations and how well NAV still fits your business.</p></div>
  <div class="grid g2">
    <div class="card"><span class="tag">Technical upgrade</span><h3>Bring your data and setup forward</h3>
      <ul class="checks"><li><div>Best for recent NAV versions with clean data</div></li><li><div>Keeps your history and setup largely as-is</div></li><li><div>Customizations rewritten as AL extensions</div></li><li><div>Several upgrade steps for older versions</div></li></ul></div>
    <div class="card"><span class="tag">Re-implementation</span><h3>Start clean, bring the data you need</h3>
      <ul class="checks"><li><div>Best for older versions or heavy customization</div></li><li><div>Uses standard Business Central features first</div></li><li><div>Open items, balances and summary history migrated</div></li><li><div>Often simpler to maintain afterwards</div></li></ul></div>
  </div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Custom code</span><h2>What happens to your NAV customizations</h2><p class="lede">Years of NAV customizations are often the biggest part of the project. Many are no longer needed because Business Central now does the job as standard.</p></div>
  {checks(['<strong>Replace with standard.</strong> Features that Business Central has added since your NAV version.', '<strong>Replace with an app.</strong> Proven AppSource apps for EDI, warehouse scanning, shipping and more.', '<strong>Rewrite as an extension.</strong> Genuinely unique processes rebuilt in AL, upgrade-safe.', '<strong>Retire.</strong> Reports and fields nobody uses anymore.'])}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our process</span><h2>From NAV to Business Central</h2></div>
  {checks(['<strong>Assess.</strong> NAV version, modules, objects, customizations, add-ons and integrations.', '<strong>Choose the path.</strong> Upgrade or re-implement, with the cost and effort of each laid out.', '<strong>Rework custom code.</strong> Each customization replaced, rebuilt or retired.', '<strong>Migrate and test.</strong> Data moved into a test environment and checked by your team.', '<strong>Go live.</strong> Cutover at a period end with support for the first close.'])}
</div></section>
{faq_section(FAQ_NAV, 'NAV upgrade questions')}
{MIG_RELATED('@/migration/dynamics-nav/')}
{cta('Still running Dynamics NAV?', 'Book a free 30-minute call. We’ll look at your version and customizations and suggest the simplest path.')}''', [faq_schema(FAQ_NAV)])

# SAGE
FAQ_SAGE = [
    ('Does Microsoft provide a migration tool for Sage?', 'Not a dedicated one like it does for Dynamics GP. We extract data from Sage using its reports and, where available, its ODBC connection, then load it with Business Central’s configuration packages.', None),
    ('Can Business Central replace Sage 100 manufacturing?', 'For most discrete manufacturers, yes. Business Central Premium covers bills of materials, production orders, routings and costing. We compare your Sage 100 work order setup with Business Central during discovery.', ('@/industries/manufacturing/', 'Business Central for manufacturing')),
    ('How long does a Sage migration take?', 'The data migration usually runs over three to six weeks alongside the wider implementation, with at least two trial loads before cutover.', ('@/guides/implementation-timeline/', 'Implementation timeline')),
]
add('migration/sage/', 'mig-sage',
    'Sage 50 & Sage 100 to Business Central Migration | Q84 Digital',
    'Move from Sage 50 or Sage 100 to Microsoft Dynamics 365 Business Central: what maps where, how data is extracted, and how balances are reconciled.',
    page_head('Migration', '<a href="@/migration/">Migration</a> / Sage', 'Sage 50 and Sage 100 to Business Central',
              'Moving from Sage 50 or Sage 100? We map your Sage data and modules to Business Central, clean it up and reconcile every balance before you switch.', art=('page-mig-sage.webp', 'Illustration of binders on a conveyor moving into a laptop')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Why companies move</span><h2>When Sage stops keeping up</h2></div>
  {checks(['<strong>Sage 50 limits.</strong> Inventory, multi-location stock and users outgrow a small-business system.', '<strong>Sage 100 on old servers.</strong> On-premises hardware, add-ons and upgrades to maintain.', '<strong>Disconnected tools.</strong> E-commerce, warehouse and reporting running beside Sage, not inside it.', '<strong>Microsoft 365.</strong> Teams wanting Outlook, Excel and Teams to work with their ERP.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What moves where</span><h2>How Sage maps to Business Central</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>In Sage</th><th>In Business Central</th><th>What to watch</th></tr></thead>
    <tbody>
      <tr><td>Chart of accounts and departments</td><td>G/L accounts plus dimensions</td><td>Sub-account structures often become dimensions.</td></tr>
      <tr><td>Customers and vendors</td><td>Customers and vendors with posting groups</td><td>Duplicates and inactive records cleaned up first.</td></tr>
      <tr><td>Inventory items</td><td>Items, units of measure and costing methods</td><td>Confirm costing method; changing it later is hard.</td></tr>
      <tr><td>Sage 100 sales and purchase orders</td><td>Open sales and purchase orders</td><td>Only open documents move.</td></tr>
      <tr><td>Sage 100 bills of materials and work orders</td><td>Production BOMs and production orders (Premium)</td><td>Routings are added if you track operations.</td></tr>
      <tr><td>Open invoices and bills</td><td>Open customer and vendor ledger entries</td><td>Reconciled to Sage aging reports.</td></tr>
    </tbody></table></div>
</div></section>
{faq_section(FAQ_SAGE, 'Sage migration questions').replace('<section class="band">', '<section>', 1)}
{MIG_RELATED('@/migration/sage/', band=True)}
{cta('Thinking about leaving Sage?', 'Book a free 30-minute call to talk through your Sage setup and what the move involves.')}''', [faq_schema(FAQ_SAGE)])

# SPREADSHEETS
FAQ_XLS = [
    ('Do we need to clean our spreadsheets before starting?', 'No. Send them as they are. We find duplicates, gaps and inconsistent codes and give you a short list of business decisions, such as which item numbers to keep.', None),
    ('Can we still use Excel with Business Central?', 'Yes. Business Central opens almost any list in Excel, and many lists can be edited in Excel and published back. Your team keeps the tool they know, with one source of truth behind it.', None),
    ('How do we get accurate opening stock?', 'With a physical count just before go-live. We load item data in advance, then post the counted quantities as opening stock at cutover.', None),
]
add('migration/spreadsheets/', 'mig-sheets',
    'Moving from Spreadsheets to Business Central | Q84 Digital',
    'Replace inventory, customer and order spreadsheets with Microsoft Dynamics 365 Business Central: cleaning Excel data, building master data and opening stock.',
    page_head('Migration', '<a href="@/migration/">Migration</a> / Spreadsheets', 'From spreadsheets to Business Central',
              'When inventory, pricing and orders live in Excel, nobody trusts the numbers. We turn your spreadsheets into clean Business Central data.', art=('page-mig-sheets.webp', 'Illustration of a pile of printed spreadsheets and a calculator turning into a neat database')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">The problem</span><h2>Why spreadsheets stop working</h2></div>
  {checks(['<strong>Several versions of the truth.</strong> Each team keeps its own copy, and they never match.', '<strong>No audit trail.</strong> Nobody knows who changed a price or a stock level, or when.', '<strong>Manual re-entry.</strong> Orders and invoices are typed again into the accounting system.', '<strong>Errors that cost money.</strong> A wrong formula becomes a wrong order or a wrong margin.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Our process</span><h2>From Excel to clean master data</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Step</th><th>What happens</th><th>Your team’s role</th></tr></thead>
    <tbody>
      <tr><td>1. Collect</td><td>Gather every spreadsheet that holds items, prices, customers, vendors or stock.</td><td>Send what you use today.</td></tr>
      <tr><td>2. Combine</td><td>Merge versions into one list per subject and flag conflicts.</td><td>Decide which value wins.</td></tr>
      <tr><td>3. Standardize</td><td>Consistent item numbers, units of measure, categories and pricing.</td><td>Approve naming and numbering rules.</td></tr>
      <tr><td>4. Load</td><td>Templates and configuration packages load the data into a test company.</td><td>Spot-check key records.</td></tr>
      <tr><td>5. Count and go live</td><td>Physical count, opening stock posted, spreadsheets retired.</td><td>Count and sign off.</td></tr>
    </tbody></table></div>
</div></section>
{faq_section(FAQ_XLS, 'Spreadsheet migration questions').replace('<section class="band">', '<section>', 1)}
{MIG_RELATED('@/migration/spreadsheets/', band=True)}
{cta('Ready to retire the spreadsheets?', 'Book a free 30-minute call. Bring one of your spreadsheets and we’ll show you what it looks like in Business Central.')}''', [faq_schema(FAQ_XLS)])


# INTEGRATIONS
FAQ_INT = [
    ('Will integrations break when Business Central updates?', 'Microsoft releases two major updates a year. Integrations built on its standard APIs and extension model are designed to survive them, and we test custom work against each release preview so problems show up before your production system updates.', None),
    ('Do integrations run in real time?', 'It depends on the connection. Some sync within minutes, others run on a schedule such as every 15 minutes or nightly. We pick the timing based on what the business needs, such as near real-time stock for an online store and nightly for reporting.', None),
    ('Do we always need custom code?', 'No. We check for a standard connector or an AppSource app first, such as Microsoft’s Shopify connector. Custom development is only for gaps those options can’t cover.', None),
    ('Are there running costs?', 'Sometimes. Connector apps often have a monthly subscription, and some integrations use Azure services billed by Microsoft. We include these costs in the estimate so there are no surprises.', None),
]
add('integrations/', 'integrations',
    'Business Central Integrations & Customization | Q84 Digital',
    'Connect Business Central to Shopify, EDI partners, carriers, CRM and Power BI, add warehouse scanning, and extend it with AL and Power Automate.',
    page_head('Integrations', 'Integrations', 'Business Central integrations and customization',
              'Connect Business Central to the tools you already use, and extend it where standard features don’t cover your process.', art=('page-integrations.webp', 'Illustration of a central hub connected to a laptop, phone, shopping bag and delivery truck')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we build</span><h2>Connected systems, less manual entry</h2>
  <p class="lede">Every time someone retypes an order, a tracking number or a stock level, you pay for it in time and errors. Integrations remove those steps so data is entered once and flows where it is needed.</p></div>
  <div class="grid g3">
    <a class="card" href="@/integrations/shopify/">{icon('shop')}<span class="tag">Commerce</span><h3>Shopify &amp; e-commerce</h3><p>Orders, items, stock and pricing kept in step with your online store.</p><span class="more">Shopify integration \u2192</span></a>
    <a class="card" href="@/integrations/edi/">{icon('receipt')}<span class="tag">Trading partners</span><h3>EDI</h3><p>Purchase orders, ship notices and invoices exchanged with retailers and suppliers.</p><span class="more">EDI integration \u2192</span></a>
    <a class="card" href="@/integrations/power-bi/">{icon('pie')}<span class="tag">Reporting</span><h3>Power BI</h3><p>Financial and operational dashboards on live Business Central data.</p><span class="more">Power BI reporting \u2192</span></a>
    <a class="card" href="@/integrations/warehouse-insight/">{icon('box')}<span class="tag">Mobile WMS</span><h3>Warehouse Insight</h3><p>A scanner-first warehouse app for receiving, picking, counts and license plates.</p><span class="more">Warehouse Insight \u2192</span></a>
    <a class="card" href="@/development/">{icon('tools')}<span class="tag">Extensions</span><h3>AL development</h3><p>Custom fields, pages, reports and business logic built as extensions.</p><span class="more">Development \u2192</span></a>
    <div class="card">{icon('truck')}<span class="tag">Logistics</span><h3>Shipping &amp; fulfillment</h3><p>Carrier rates, labels and tracking connected to warehouse shipments.</p></div>
    <div class="card">{icon('link')}<span class="tag">APIs</span><h3>System integrations</h3><p>Data sync with CRM and other business systems through Business Central's APIs.</p></div>
    <div class="card">{icon('chart')}<span class="tag">Automation</span><h3>Power Automate</h3><p>Approvals, notifications and routine tasks handled automatically.</p></div>
    <div class="card">{icon('ledger')}<span class="tag">Microsoft 365</span><h3>Outlook, Excel &amp; Teams</h3><p>Business Central data where your team already works.</p></div>
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
<section><div class="wrap"><div class="note">Also running Dynamics 365 Sales, Customer Service or Field Service? We work across the Dynamics 365 family and can connect Business Central with Dataverse and your CRM.</div></div></section>
{faq_section(FAQ_INT)}
{cta('Have a system that needs to connect?', 'Tell us what you use today. We’ll suggest the simplest reliable way to make it work with Business Central.')}''', [faq_schema(FAQ_INT)])

# INTEGRATION PAGES
SHOPIFY_WORKED = f'''<section class="band"><div class="wrap">
  {worked('Connecting a Shopify store to Business Central',
          'An e-commerce distributor sells through Shopify and keeps its accounting in Business Central. Staff re-enter every web order, stock levels are updated by hand twice a day, and the store sometimes sells items that are out of stock.',
          [('Design', 'Agree that Business Central owns items, prices and stock, and Shopify owns web orders. Map product variants to item variants.'),
           ('Setup', 'Configure Microsoft’s Shopify connector: item sync, stock sync by location, and order import with customer matching.'),
           ('Rules', 'Orders with unknown items or failed payments go to a review list instead of creating bad sales orders.'),
           ('Testing', 'Run test orders, refunds and partial shipments through the full flow, from Shopify order to shipment, invoice and payment.'),
           ('Go-live', 'Switch on scheduled sync and train staff to clear the exceptions list each morning.')],
          'Web orders arrive in Business Central without retyping, the store shows stock that matches the warehouse, and staff only touch the orders that genuinely need attention.')}
</div></section>
'''
INT_RELATED = lambda skip: related('Other integrations', [x for x in [
    ('@/integrations/shopify/', 'Shopify', 'Orders, items, stock and payouts synced with your store.'),
    ('@/integrations/edi/', 'EDI', 'Orders, ship notices and invoices with trading partners.'),
    ('@/integrations/power-bi/', 'Power BI', 'Dashboards on live Business Central data.'),
    ('@/integrations/warehouse-insight/', 'Warehouse Insight', 'Mobile WMS app for receiving, picking, counts and license plates.')] if x[0] != skip][:3])

# SHOPIFY
FAQ_SHOP = [
    ('Does the Shopify connector cost extra?', 'No. Microsoft’s Shopify connector is included with Business Central. You pay for your Shopify plan and Business Central licenses as usual.', None),
    ('Can we connect more than one Shopify store?', 'Yes. The connector supports several stores, each with its own settings for items, prices, locations and order handling.', None),
    ('Which system should own prices and stock?', 'Usually Business Central. It knows what’s in every warehouse and what’s already promised to other orders, so it should tell Shopify what’s available to sell.', None),
    ('What about Shopify B2B?', 'The connector supports Shopify’s B2B features on Shopify Plus, including company accounts and their locations. We check which parts you need during setup.', None),
]
add('integrations/shopify/', 'int-shopify',
    'Business Central Shopify Integration | Q84 Digital',
    'Connect Shopify to Business Central with Microsoft’s connector: products, stock, customers, orders, refunds and payouts, set up and tested.',
    page_head('Integrations', '<a href="@/integrations/">Integrations</a> / Shopify', 'Business Central Shopify integration',
              'Web orders flow into Business Central, stock flows back to your store, and nobody retypes anything. We set up Microsoft’s Shopify connector around how you sell.', art=('page-shopify.webp', 'Illustration of a laptop order list and a phone store page syncing, with a shopping cart of boxes')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What syncs</span><h2>What the Shopify connector handles</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Data</th><th>Direction</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>Products and variants</td><td>Business Central to Shopify (or both ways)</td><td>Item variants map to Shopify variants.</td></tr>
      <tr><td>Prices</td><td>Business Central to Shopify</td><td>Including price lists for different customer groups.</td></tr>
      <tr><td>Stock levels</td><td>Business Central to Shopify</td><td>By location, so the store only sells what you can ship.</td></tr>
      <tr><td>Customers</td><td>Both ways</td><td>Matched by email or phone to avoid duplicates.</td></tr>
      <tr><td>Orders</td><td>Shopify to Business Central</td><td>Created as sales orders or invoices, automatically or after review.</td></tr>
      <tr><td>Fulfillments and tracking</td><td>Business Central to Shopify</td><td>Customers get tracking when you ship.</td></tr>
      <tr><td>Refunds, returns and payouts</td><td>Shopify to Business Central</td><td>So finance can reconcile Shopify payouts to the bank.</td></tr>
    </tbody></table></div>
</div></section>
''' + SHOPIFY_WORKED + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Beyond the basics</span><h2>When you need more than the connector</h2></div>
  {checks(['<strong>Bundles and kits.</strong> Sold as one product, shipped as several items.', '<strong>Marketplaces.</strong> Amazon, Walmart and other channels through specialist connector apps.', '<strong>3PL fulfillment.</strong> Orders passed to a third-party warehouse and confirmed back.', '<strong>Custom rules.</strong> Order routing, fraud holds or special pricing logic built as small extensions.'])}
</div></section>
{faq_section(FAQ_SHOP, 'Shopify integration questions')}
{INT_RELATED('@/integrations/shopify/')}
{cta('Connect your Shopify store to Business Central', 'Book a free 30-minute call. We’ll look at how you sell today and how the connector would fit.')}''', [faq_schema(FAQ_SHOP)])

# EDI
FAQ_EDI = [
    ('Does Business Central have EDI built in?', 'No. EDI is handled by a specialist EDI provider, usually through an app from Microsoft AppSource that connects their network to Business Central. We help you choose the provider and set up the connection.', None),
    ('Which EDI documents do we need?', 'It depends on your trading partners. Most retailers require at least purchase orders (850), ship notices (856) and invoices (810), and some add order acknowledgments (855) or inventory updates (846). Each partner has its own rules, so we start from their requirements.', None),
    ('How long does it take to add a trading partner?', 'Usually a few weeks, most of it spent on the partner’s testing and certification. Once the first partner is live, the next ones are faster.', None),
]
add('integrations/edi/', 'int-edi',
    'Business Central EDI Integration | Q84 Digital',
    'Set up EDI with Microsoft Dynamics 365 Business Central: purchase orders, ship notices, invoices and inventory updates with retailers and trading partners.',
    page_head('Integrations', '<a href="@/integrations/">Integrations</a> / EDI', 'Business Central EDI integration',
              'Retailers and large customers expect EDI. We connect Business Central to an EDI provider so orders come in, ship notices go out and invoices are accepted the first time.', art=('page-edi.webp', 'Illustration of documents travelling between a store and a warehouse')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Common documents</span><h2>EDI documents most distributors exchange</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Document</th><th>X12 code</th><th>In Business Central</th></tr></thead>
    <tbody>
      <tr><td>Purchase order (in)</td><td>850</td><td>Creates a sales order</td></tr>
      <tr><td>Order acknowledgment (out)</td><td>855</td><td>Confirms quantities, prices and dates</td></tr>
      <tr><td>Advance ship notice (out)</td><td>856</td><td>Sent from the warehouse shipment, with carton and pallet detail</td></tr>
      <tr><td>Invoice (out)</td><td>810</td><td>Sent when the sales invoice posts</td></tr>
      <tr><td>Inventory advice (out)</td><td>846</td><td>Shares available stock with the trading partner</td></tr>
      <tr><td>Warehouse shipping order and advice</td><td>940 / 945</td><td>Used with third-party warehouses</td></tr>
    </tbody></table></div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Why it matters</span><h2>Getting EDI right saves real money</h2><p class="lede">Retailers charge back for late ship notices, wrong labels and mismatched invoices. Most chargebacks come from data that was right in one system and wrong in another.</p></div>
  {checks(['<strong>Orders without retyping.</strong> EDI orders become sales orders automatically, with exceptions flagged.', '<strong>Ship notices from real data.</strong> Built from what was actually picked and packed.', '<strong>Compliant labels.</strong> Carton and pallet labels with the barcodes partners require.', '<strong>Invoices that match.</strong> Prices and quantities checked against the original order.'])}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our process</span><h2>How we set up EDI</h2></div>
  {checks(['<strong>Collect partner requirements.</strong> Each retailer’s documents, rules and label specs.', '<strong>Choose the provider.</strong> An EDI network with a proven Business Central connector.', '<strong>Map and configure.</strong> EDI fields mapped to Business Central customers, items and units of measure.', '<strong>Test and certify.</strong> Test documents exchanged until the partner signs off.', '<strong>Go live and monitor.</strong> Exceptions reviewed daily until everything runs clean.'])}
</div></section>
{faq_section(FAQ_EDI, 'EDI questions')}
{INT_RELATED('@/integrations/edi/')}
{cta('A retailer asking you for EDI?', 'Book a free 30-minute call. Bring the requirements and we’ll explain what it takes in Business Central.')}''', [faq_schema(FAQ_EDI)])

# POWER BI
FAQ_PBI = [
    ('Do we need Power BI licenses?', 'To build and share reports, people usually need a Power BI Pro license, which some Microsoft 365 plans include. Viewing reports inside Business Central follows the same Power BI licensing rules. We confirm the right setup for your team.', None),
    ('How current is the data?', 'Reports refresh on a schedule, typically several times a day. For truly live numbers, Business Central’s own pages and Excel views are always up to date.', None),
    ('Can we report across several companies?', 'Yes. Power BI can combine data from several Business Central companies into one report, which is often simpler than consolidating in Business Central for management reporting.', None),
]
add('integrations/power-bi/', 'int-powerbi',
    'Business Central Power BI Reporting Setup | Q84 Digital',
    'Power BI reporting for Business Central: Microsoft’s ready-made reports, custom dashboards, dimensions and multi-company reporting, set up properly.',
    page_head('Integrations', '<a href="@/integrations/">Integrations</a> / Power BI', 'Business Central Power BI reporting',
              'Stop rebuilding reports in Excel every month. We set up Power BI on your Business Central data so the numbers your team needs are always one click away.', art=('page-power-bi.webp', 'Illustration of a monitor with a reporting dashboard, a bar chart and a pie chart')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we set up</span><h2>From ready-made reports to custom dashboards</h2></div>
  <div class="grid g3">
    <div class="card">{icon('pie')}<h3>Microsoft’s ready-made reports</h3><p>Finance, sales, purchasing, inventory, projects and manufacturing reports from Microsoft, connected and configured.</p></div>
    <div class="card">{icon('chart')}<h3>Custom dashboards</h3><p>The handful of numbers your leadership team actually runs the business on, on one page.</p></div>
    <div class="card">{icon('ledger')}<h3>Inside Business Central</h3><p>Reports embedded in role centers, so people see them where they already work.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Examples</span><h2>Reports our clients ask for most</h2></div>
  {checks(['<strong>Margin by customer, item and salesperson.</strong> Including landed costs and discounts.', '<strong>Inventory health.</strong> Stock value, slow movers, stockouts and days on hand by location.', '<strong>Cash and receivables.</strong> Aging, collections and cash forecast.', '<strong>Sales trends.</strong> This year against last year, by region, channel and product line.', '<strong>Job and project profitability.</strong> Budget against actual for service businesses.'])}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Good reports start in Business Central</span><h2>Why setup matters</h2><p class="lede">Power BI can only slice data the way Business Central records it. Clean dimensions, item categories and customer groups make reports simple; messy ones make them impossible.</p></div>
  {checks(['<strong>Dimensions.</strong> Department, location, channel or project recorded on every transaction.', '<strong>Categories.</strong> Item categories and customer groups that match how you report.', '<strong>Definitions.</strong> One agreed meaning for margin, revenue and on-time delivery.'])}
</div></section>
{faq_section(FAQ_PBI, 'Power BI questions')}
{INT_RELATED('@/integrations/power-bi/')}
{cta('Want reports you don’t have to rebuild every month?', 'Book a free 30-minute call. Tell us which numbers matter and we’ll show you how to get them.')}''', [faq_schema(FAQ_PBI)])

# WAREHOUSE INSIGHT (mobile WMS app for Business Central)
WI_SHOT = next((f for f in ('shot-warehouse-insight-app.webp', 'shot-warehouse-insight-app.png') if os.path.exists(os.path.join(ROOT, 'images', f))), None)
WI_FIG = (f'<figure class="phone-shot"><img src="@/images/{WI_SHOT}" alt="Warehouse Insight mobile app home screen with item inquiry, bin inquiry, count, receive, put-away, move, pick, ship, consumption, output, assembly order, license plate and scratchpad" width="329" height="664" loading="lazy"><figcaption>The Warehouse Insight home screen on a handheld device.</figcaption></figure>'
          if WI_SHOT else '')
FAQ_WI = [
    ('Does Warehouse Insight replace Business Central’s warehouse features?', 'No. It works on top of them. Receipts, put-aways, picks, shipments and counts are still Business Central documents; Warehouse Insight gives your team a fast, scanner-first way to process them on the floor.', None),
    ('Which devices does it run on?', 'Rugged Android handhelds with built-in barcode scanners are the usual choice for warehouse work. We help you choose and test devices before you buy a fleet.', None),
    ('Does it support manufacturing?', 'Yes. The app includes consumption and output, so shop-floor staff can record materials used and finished goods produced against production orders, and assembly orders for kitting.', ('@/industries/manufacturing/', 'Business Central for manufacturing')),
    ('How is it licensed?', 'Warehouse Insight is an add-on app available through Microsoft AppSource, with its own subscription from the publisher, separate from your Business Central licenses. We include the cost in your estimate.', None),
    ('What does Order Ship Express cost?', 'The app itself is free. You pay the carriers for postage through an EasyPost account, and EasyPost’s discounted rates can lower what you pay today. You need accounts with the carriers you want to use.', None),
    ('Can Order Ship Express handle international or freight shipments?', 'It is designed for domestic parcel shipping with up to three carriers. For international parcels, more carriers or LTL and truckload freight, a more advanced shipping app is the better fit, and we’ll recommend one during discovery.', None),
]
add('integrations/warehouse-insight/', 'int-wi',
    'Warehouse Insight Mobile WMS for Business Central | Q84 Digital',
    'Warehouse Insight mobile WMS and Order Ship Express parcel shipping for Business Central: scan, pick, pack and print carrier labels, set up by Q84 Digital.',
    page_head('Integrations', '<a href="@/integrations/">Integrations</a> / Warehouse Insight', 'Warehouse Insight mobile WMS for Business Central',
              'A scanner-first warehouse app for Business Central. Your team receives, puts away, picks, ships and counts on handheld devices, and every scan updates Business Central straight away.', art=('page-warehouse-insight.webp', 'Illustration of a handheld scanner, a labeled parcel and a label printer printing a shipping label')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">What it is</span><h2>Business Central in your warehouse team’s hands</h2>
    <p class="lede">Warehouse Insight is an advanced warehouse management app for Microsoft Dynamics 365 Business Central. It runs on rugged handhelds and puts every everyday warehouse task on one simple home screen, with large buttons designed for scanning on the move.</p>
    <p>Instead of walking back to a desk to update the system, staff scan the item, the bin and the quantity where the work happens. Business Central stays accurate in real time, and paper pick lists and count sheets disappear.</p></div>
  {WI_FIG}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Functions</span><h2>Every warehouse task on one screen</h2></div>
  <div class="grid g3">
    <div class="card">{icon('box')}<h3>Item and bin inquiry</h3><p>Scan an item to see where it is and how many are available, or scan a bin to see what it holds.</p></div>
    <div class="card">{icon('truck')}<h3>Receive and put-away</h3><p>Receive against purchase orders by scanning, then put goods away into the right bins.</p></div>
    <div class="card">{icon('warehouse')}<h3>Pick and ship</h3><p>Follow picks bin by bin, confirm each item with a scan, and ship from the device.</p></div>
    <div class="card">{icon('migrate')}<h3>Movement and ad-hoc moves</h3><p>Process planned movements, or move stock between bins on the spot when the floor needs it.</p></div>
    <div class="card">{icon('ledger')}<h3>Counts</h3><p>Cycle counts and basic counts by scanning, without printed count sheets.</p></div>
    <div class="card">{icon('factory')}<h3>Consumption, output and assembly</h3><p>Record materials used and finished goods produced, and process assembly orders for kits.</p></div>
    <div class="card">{icon('shop')}<h3>License plates</h3><p>Track pallets and cartons as license plates, so a whole pallet moves or ships with one scan.</p></div>
    <div class="card">{icon('receipt')}<h3>Scratchpad</h3><p>Capture quick scans and notes on the device for tasks that don’t fit a standard document.</p></div>
    <div class="card">{icon('chart')}<h3>Live in Business Central</h3><p>Every scan posts or updates the Business Central document, so stock and orders are always current.</p></div>
  </div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Why it matters</span><h2>What changes on the warehouse floor</h2><p class="lede">Scanning removes the two biggest sources of warehouse errors: picking the wrong item and typing the wrong quantity.</p></div>
  {checks(['<strong>Fewer picking errors.</strong> A scan confirms the right item and bin before anything ships.', '<strong>Inventory you can trust.</strong> Stock moves are recorded as they happen, not at the end of the day.', '<strong>Faster receiving and shipping.</strong> No paperwork to key in afterwards.', '<strong>Counting without shutdowns.</strong> Count a few bins every day instead of closing for a full count.', '<strong>Pallet-level tracking.</strong> License plates keep pallets and cartons together from receipt to shipment.'])}
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Parcel shipping</span><h2>Ship parcels with Order Ship Express</h2>
    <p class="lede">Once an order is picked and packed, it still needs a carrier label. Order Ship Express is a free shipping app for Business Central from Insight Works, the publisher of Warehouse Insight. It connects Business Central to carriers through EasyPost, so your team can compare rates and print labels without leaving the order.</p></div>
  <div class="grid g3">
    <div class="card">{icon('chart')}<h3>Live rate shopping</h3><p>Compare carrier services and prices from the sales order before you choose how to ship.</p></div>
    <div class="card">{icon('truck')}<h3>Multiple carriers</h3><p>Connect up to three carriers through an EasyPost account, such as UPS, USPS, FedEx or DHL, and pick one per shipment.</p></div>
    <div class="card">{icon('receipt')}<h3>Labels from the order</h3><p>Print carrier-approved labels directly from the sales order, using standard or custom package sizes, with no retyping.</p></div>
    <div class="card">{icon('box')}<h3>Tracking back in Business Central</h3><p>Tracking numbers and freight charges are written back to the sales order, so customer service can answer “where is my order?” from Business Central.</p></div>
    <div class="card">{icon('migrate')}<h3>Return labels</h3><p>Create return labels from posted shipments or invoices, something standard Business Central doesn’t offer.</p></div>
    <div class="card">{icon('pie')}<h3>Freight charges and markups</h3><p>Add shipping charges to orders automatically, with optional markup rules per carrier for what you bill customers.</p></div>
  </div>
  <div class="note" style="margin-top:24px">Order Ship Express has no license fee; you pay the carriers for postage through EasyPost. It is built for domestic parcel shipping in North America. For international shipping, more than three carriers, or LTL and full-truckload freight, Insight Works offers a separate, more advanced shipping app, and we can help you choose.</div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our role</span><h2>How we set up Warehouse Insight</h2></div>
  {checks(['<strong>Warehouse review.</strong> We walk your floor and map how goods are received, stored, picked and shipped today.', '<strong>Business Central setup.</strong> Locations, bins, zones and warehouse documents configured for how you work.', '<strong>Barcodes and labels.</strong> Item, bin and license plate labels designed and tested with your printers.', '<strong>Devices and app setup.</strong> Handhelds tested on your Wi-Fi, users and functions configured in Warehouse Insight.', '<strong>Carrier labels.</strong> Order Ship Express connected to your carrier accounts, with package sizes and freight rules set up.', '<strong>Training and go-live.</strong> Hands-on training on the floor, one process at a time, and support through the first weeks.'])}
</div></section>
<section><div class="wrap"><div class="note">Warehouse Insight and Order Ship Express are third-party apps from Insight Works, available through Microsoft AppSource. Their costs are separate from Microsoft’s Business Central licenses.</div></div></section>
{faq_section(FAQ_WI, 'Warehouse Insight questions')}
{INT_RELATED('@/integrations/warehouse-insight/')}
{cta('Want scanning in your warehouse?', 'Book a free 30-minute call. We’ll look at your warehouse processes and show you how Warehouse Insight would fit.')}''', [faq_schema(FAQ_WI)])


# E-COMMERCE INDUSTRY
FAQ_ECOM = [
    ('Is Business Central a good fit for an e-commerce brand?', 'Yes, once you have real inventory, more than one sales channel or a warehouse to run. Smaller stores selling a few products through one channel may be fine with simpler tools for now.', None),
    ('Can Business Central handle Amazon and other marketplaces?', 'Yes, through connector apps from Microsoft AppSource. Shopify has Microsoft’s own connector; other channels use specialist apps.', ('@/integrations/shopify/', 'Shopify integration')),
    ('Can we use a third-party warehouse?', 'Yes. Orders can be passed to a 3PL and shipment confirmations posted back, often over EDI or an API.', ('@/integrations/edi/', 'EDI integration')),
]
add('industries/ecommerce/', 'ecommerce',
    'Business Central for E-commerce Brands | Q84 Digital',
    'Business Central for e-commerce brands: Shopify and marketplace orders, multi-location stock, fulfillment, returns and payout reconciliation.',
    page_head('E-commerce', 'Industries / E-commerce', 'Business Central for e-commerce brands',
              'Orders from every channel in one system, stock you can trust across warehouses and 3PLs, and payouts that reconcile without a spreadsheet.', art=('page-ecommerce.webp', 'Illustration of a phone with an online store, shopping bag, parcels and a delivery scooter')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Common challenges</span><h2>Where growing online brands get stuck</h2></div>
  {checks(['<strong>Overselling.</strong> Stock in the store doesn’t match the warehouse.', '<strong>Orders typed twice.</strong> Web orders re-entered for fulfillment and accounting.', '<strong>Payouts that don’t reconcile.</strong> Fees, refunds and reserves make bank matching painful.', '<strong>Margins you can’t see.</strong> Shipping, returns and channel fees never reach product margin.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How Business Central helps</span><h2>One system behind every channel</h2></div>
  <div class="grid g3">
    <div class="card">{icon('shop')}<h3>Shopify, built in</h3><p>Microsoft’s connector syncs products, stock, orders, refunds and payouts.</p></div>
    <div class="card">{icon('cart')}<h3>Marketplaces</h3><p>Amazon and other channels through specialist connector apps.</p></div>
    <div class="card">{icon('box')}<h3>Multi-location stock</h3><p>Stock by warehouse, 3PL and store, with what’s available to sell on each channel.</p></div>
    <div class="card">{icon('truck')}<h3>Fulfillment</h3><p>Picking, packing and shipping in your warehouse, or orders sent to a 3PL.</p></div>
    <div class="card">{icon('receipt')}<h3>Returns &amp; refunds</h3><p>Returns received into stock and refunds posted to the right customer.</p></div>
    <div class="card">{icon('pie')}<h3>True product margin</h3><p>Landed cost, channel fees and shipping included in margin reporting.</p></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it flows</span><h2>An online order, start to finish</h2></div>
  <ol class="steps">
    <li><h3>Order</h3><p>The order is placed on Shopify or a marketplace.</p></li>
    <li><h3>Import</h3><p>Business Central creates the sales order automatically.</p></li>
    <li><h3>Fulfill</h3><p>Your warehouse or 3PL picks, packs and ships.</p></li>
    <li><h3>Track</h3><p>Tracking goes back to the store and the customer.</p></li>
    <li><h3>Reconcile</h3><p>The payout matches orders, fees and refunds.</p></li>
  </ol>
</div></section>
{faq_section(FAQ_ECOM)}
{related('Related', [('@/integrations/shopify/', 'Shopify integration', 'How the Shopify connector is set up and tested.'), ('@/integrations/warehouse-insight/', 'Warehouse Insight', 'Scanner-first picking, packing and counts.'), ('@/industries/distribution/', 'Wholesale distribution', 'Selling B2B as well as online.')])}
{cta('Running an online brand on too many tools?', 'Book a free 30-minute call. We’ll map your channels, warehouse and finance and show where Business Central fits.')}''', [faq_schema(FAQ_ECOM)])


# SUPPORT
FAQ_SUP = [
    ('Can you support a system another partner implemented?', 'Yes. Many support clients come to us after their original implementation. We usually start with a health check so we understand how your system was set up before changing anything.', None),
    ('Do we have to move our Microsoft licenses?', 'No. Your licenses can stay with your current licensing partner or Microsoft. Support covers the system itself, not where the subscription is billed.', None),
    ('Hourly or monthly: which is better?', 'Hourly suits occasional questions and one-off fixes. A monthly plan suits businesses that want regular improvements, priority response and someone who knows their system well. You can start hourly and move to a plan later.', None),
    ('What if a fix needs development work?', 'Small changes are handled within support time. Larger changes, such as a new integration or extension, are scoped and quoted separately so you approve the cost before work starts.', None),
]
add('support/', 'support',
    'Business Central Support Services | Q84 Digital',
    'Business Central support from a senior consultant: health checks, troubleshooting, setup fixes, training and enhancements, billed hourly or monthly.',
    page_head('Support', 'Services / Support', 'Business Central support',
              'Already using Business Central? Get help fixing issues, improving your setup and training your team, from a consultant who knows the system well.', art=('page-support.webp', 'Illustration of a headset beside a laptop showing a chat bubble and a check mark, with a wrench and a mug')) + f'''
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
    'Business Central for wholesale distributors: multi-location inventory, purchasing, picking, shipping and landed costs, set up by a supply chain specialist.',
    page_head('Distribution', 'Industries / Wholesale distribution', 'Business Central for wholesale distributors',
              'Accurate stock, faster purchasing and a warehouse that ships the right order the first time.',
              art=('page-distribution.webp', 'Illustration of warehouse racking with boxes and a forklift lifting a pallet')) + f'''
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
    'Business Central Premium for small and midsize manufacturers: bills of materials, production orders, material planning and product costing, with examples.',
    page_head('Manufacturing', 'Industries / Manufacturing', 'Business Central for manufacturers',
              'Plan production, control materials and know what each product really costs to make.',
              art=('page-manufacturing.webp', 'Illustration of a machine and conveyor moving metal gears into a box, with a production chart on screen')) + f'''
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

FAQ_SVC = [
    ('Do we need Business Central Premium for a service business?', 'Not always. Projects, resources, time sheets and project invoicing are in Essentials. Service orders, service items, service contracts and dispatching are part of Service Management, which needs the Premium license.', ('@/licensing/#calculator', 'Estimate your license cost')),
    ('Is Business Central a good fit for a marketing agency?', 'Yes, for agencies that want time, retainers, media costs and accounting in one system. Projects track each client and campaign, recurring billing handles retainers, and outside costs are re-billed with a markup. Agencies that need detailed creative workflow or proofing usually keep a separate project tool and connect it.', None),
    ('Can a medical or aesthetic clinic use Business Central?', 'Yes, for finance, deposits, consumables, purchasing and multi-clinic reporting. Patient health records should stay in your clinical or practice management system, which has the privacy controls health data requires. Business Central only needs the patient account and the invoice, and the two systems can be connected.', None),
    ('Does Business Central work for construction and restoration companies?', 'Yes, for job costing, purchasing, subcontractor invoices, change orders and billing by job or insurance claim. Standard Business Central bills by milestone or percentage complete; if you need AIA-style progress billing with retainage, or a direct link to estimating software such as Xactimate, we add a proven extension from Microsoft AppSource or build the integration.', None),
    ('Can staff enter time without a full license?', 'Yes. Employees who only fill in time sheets and expenses can use the lower-cost Team Members license, in the browser or the Business Central mobile app.', None),
    ('How does Business Central handle work in progress on long projects?', 'Projects support several WIP methods, including cost value, sales value, percentage of completion and completed contract. You post WIP at month-end so revenue and costs land in the right period.', None),
    ('When do we need Dynamics 365 Field Service instead?', 'Business Central covers service orders, contracts and basic dispatching. If you schedule dozens of technicians a day, need route optimization or a full mobile technician app, Dynamics 365 Field Service fits better, and it integrates with Business Central for parts, pricing and invoicing.', None),
]
add('industries/professional-services/', 'service-industries',
    'Business Central for Professional Services | Q84 Digital',
    'Business Central for professional services: project accounting, time, retainers and job costing for agencies, clinics, construction and restoration firms.',
    page_head('Professional services', 'Industries / Professional services', 'Business Central for professional services and project-based businesses',
              'From marketing agencies and clinics to construction and restoration crews: track every hour, job and procedure, bill every client and know what actually makes money.',
              art=('page-services.webp', 'Illustration of a laptop with a project chart, an alarm clock, a hard hat and a clipboard with an invoice')) + f'''
<section data-nosubnav><div class="wrap split">
  <div class="stack"><span class="eyebrow">Challenges</span><h2>Where service businesses lose margin</h2><p class="lede">In a service business, what you sell is time, skills and parts. When those are tracked in separate spreadsheets and apps, hours go unbilled and nobody can say which jobs are profitable until it’s too late.</p></div>
  {checks(['<strong>Hours that never get billed.</strong> Time is entered late, on paper or not at all.', '<strong>Budgets tracked in spreadsheets.</strong> Overruns show up after the project is finished.', '<strong>Slow invoicing.</strong> Billing waits for someone to collect time, expenses and parts.', '<strong>Technicians working blind.</strong> No service history, contract terms or parts availability in the field.', '<strong>No profitability view.</strong> Margin by project, customer or contract is a guess.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Who we work with</span><h2>Service businesses we work with</h2></div>
  <div class="grid g3">
    <div class="card">{icon('chart')}<span class="pill">Current client</span><h3>Marketing and creative agencies</h3><p>Agencies that sell retainers, campaigns and projects, and need to see time, media spend and margin by client. We support a marketing agency on Business Central today.</p></div>
    <div class="card">{icon('support')}<span class="pill">Current client</span><h3>Medical and aesthetic clinics</h3><p>Plastic surgery, cosmetic and hair restoration clinics that take deposits, use costly consumables and run more than one location. We support a hair transplant clinic on Business Central today.</p></div>
    <div class="card">{icon('tools')}<span class="pill">Current client</span><h3>Construction and restoration</h3><p>General contractors, trades, and water, fire and mold restoration companies that need job costing, change orders and insurance claim billing. We support a construction and restoration company on Business Central today.</p></div>
    <div class="card">{icon('ledger')}<h3>Project-based firms</h3><p>Engineering, IT services, consulting and installation companies that sell fixed-price or time-and-materials projects.</p></div>
    <div class="card">{icon('truck')}<h3>Field service and maintenance</h3><p>Companies that install, repair and maintain equipment on customer sites, often under service contracts.</p></div>
  </div>
</div></section>
{TESTIMONIALS}
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Marketing agencies</span><h2>Business Central for marketing agencies</h2><p class="lede">An agency’s profit depends on billing every hour and every dollar of media it handles for clients. Business Central ties time, costs and billing to each client and campaign, so you see margin while the work is still running.</p></div>
  {checks(['<strong>Retainers and projects side by side.</strong> Monthly retainers billed on a schedule, with campaigns and one-off projects tracked as their own budgets.', '<strong>Time by client and campaign.</strong> Staff log hours against the right job, and you see who is over-servicing which account.', '<strong>Media and pass-through costs.</strong> Ad spend, printing and freelancer invoices charged to the client’s project and re-billed with your markup.', '<strong>Utilization and capacity.</strong> Billable hours against available hours by person and team.', '<strong>Profit by client.</strong> Revenue, staff cost and outside costs per client, campaign and retainer, not just in total.'])}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Medical and aesthetic clinics</span><h2>Business Central for plastic surgery and hair restoration clinics</h2><p class="lede">Elective clinics run on deposits, expensive consumables and procedures that are booked weeks ahead. Business Central handles the financial and operational side, while patient records stay in your clinical system.</p></div>
  {checks(['<strong>Deposits and payment plans.</strong> Take prepayments when a procedure is booked and apply them to the final invoice, including amounts paid through financing companies.', '<strong>Procedure packages.</strong> Price procedures as packages, such as a hair transplant priced by graft count, with the consumables and staff time behind each one.', '<strong>Consumables and medications.</strong> Track stock by clinic and room, with lot numbers and expiry dates, and reorder before supplies run short.', '<strong>Revenue by procedure, provider and location.</strong> See which treatments and surgeons drive profit across every clinic.', '<strong>Multi-clinic accounting.</strong> Separate locations or companies with consolidated reporting for the owners.'])}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Construction and restoration</span><h2>Business Central for construction and restoration companies</h2><p class="lede">Contractors and restoration firms make or lose money job by job. Business Central gives every job its own budget, costs and billing, so you see the margin on each one while crews are still on site, not months after it closes.</p></div>
  {checks(['<strong>Job costing.</strong> Labor, materials, equipment and subcontractors posted to each job and phase, with budget against actual at any time.', '<strong>Estimates and change orders.</strong> Turn the estimate into the job budget, and add change orders as new budget lines so extra work gets billed.', '<strong>Subcontractors and purchasing.</strong> Purchase orders and subcontractor invoices charged straight to the job, with approval before payment.', '<strong>Insurance restoration claims.</strong> Track water, fire and mold jobs by claim, invoice the insurance carrier and the homeowner’s deductible separately, and follow up on what’s outstanding.', '<strong>Equipment and crews.</strong> Charge drying equipment, machinery and crew hours to jobs at internal rates, so equipment cost shows up in job margin.', '<strong>Progress billing and work in progress.</strong> Bill by milestone or percentage complete, and post WIP at month-end so revenue lands in the right period.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How Business Central helps</span><h2>Projects, people and service in one system</h2></div>
  <div class="grid g3">
    <div class="card">{icon('chart')}<h3>Projects &amp; budgets</h3><p>Tasks, budgets and planning lines for labor, items and expenses, with budget against actual at any time.</p></div>
    <div class="card">{icon('key')}<h3>Time sheets &amp; resources</h3><p>Weekly time sheets with approval, resource capacity and cost and billing rates by person or role.</p></div>
    <div class="card">{icon('receipt')}<h3>Project invoicing</h3><p>Fixed-price, milestone and time-and-materials billing straight from approved time and costs.</p></div>
    <div class="card">{icon('support')}<h3>Service orders (Premium)</h3><p>Service requests, technician assignment, parts used and labor recorded against the customer’s equipment.</p></div>
    <div class="card">{icon('shop')}<h3>Service items &amp; contracts</h3><p>Installed equipment with warranty and service history, and contracts invoiced on a schedule.</p></div>
    <div class="card">{icon('pie')}<h3>Profitability reporting</h3><p>Margin by project, customer and contract, with work in progress posted at month-end.</p></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Step by step</span><h2>A project, start to finish</h2></div>
  <ol class="steps">
    <li><h3>Quote</h3><p>Estimate labor, materials and expenses on the project’s planning lines.</p></li>
    <li><h3>Plan</h3><p>Assign people and dates, and order the parts the job needs.</p></li>
    <li><h3>Deliver</h3><p>Staff record time and expenses; parts are consumed from stock.</p></li>
    <li><h3>Invoice</h3><p>Approved time and costs become an invoice, or a milestone is billed.</p></li>
    <li><h3>Review</h3><p>Compare budget with actual and see the margin on every job.</p></li>
  </ol>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Is it the right fit?</span><h2>Where Business Central works best for services</h2><p class="lede">Business Central suits most small and midsize service companies. Some scheduling-heavy operations need more, and it’s better to know that before you start.</p></div>
  {checks(['<strong>A good fit:</strong> project-based firms that need budgets, time sheets and project billing tied to their accounting.', '<strong>Add Premium Service Management:</strong> companies that repair or maintain equipment and sell service contracts.', '<strong>Consider Dynamics 365 Field Service:</strong> large technician teams that need advanced scheduling, route optimization and a full mobile app, connected to Business Central.'])}
</div></section>
<section><div class="wrap">
  {worked('An equipment service company replacing paper work orders',
          'A 35-person company installs and maintains commercial refrigeration equipment. Technicians fill in paper work orders, parts are taken from the van without being recorded, and contract customers are invoiced from a spreadsheet, often weeks late.',
          [('Design', 'Map installations as projects and repairs as service orders, and define service items for every installed unit with warranty dates.'),
           ('Build', 'Set up Premium Service Management, service contracts with quarterly billing, van stock as locations and time sheets for technicians.'),
           ('Data', 'Load customers, installed equipment and active contracts from the spreadsheets after removing duplicates and filling in serial numbers.'),
           ('Test', 'Run sample jobs end to end, from service request to technician assignment, parts consumption, time entry and invoice.'),
           ('Go-live', 'Start with contract customers first, then move installation projects once the team is comfortable with the new process.')],
          'Every visit is recorded with time and parts, contracts invoice automatically each quarter, and the owner sees margin by customer and contract instead of guessing.')}
</div></section>
<section><div class="wrap"><div class="note">Service orders and contracts need the Business Central Premium license. Projects and time sheets are included in Essentials. <a href="@/licensing/#calculator">Estimate your license cost.</a></div></div></section>
{faq_section(FAQ_SVC)}
{checklist_promo()}
{cta('Talk about your service operations')}''', [faq_schema(FAQ_SVC)])

# COMPANY & SERVICE PAGES
# ABOUT
about_photo = (f'<figure class="page-head-art about-photo"><img src="@/images/{esc(CFG["consultant_photo"])}" alt="Oleh Karnaukhov, founder of Q84 Digital" width="400" height="400"></figure>'
               if CFG.get('consultant_photo') else '')
ABOUT_SCHEMA = dict(PERSON_SCHEMA)
add('about/', 'about',
    'About Q84 Digital | Business Central in Vancouver & Tacoma',
    'Senior-led Business Central consultancy in Vancouver, BC and Tacoma, WA, founded by Oleh Karnaukhov after 15+ years in Dynamics and supply chain.',
    page_head('About', 'About', 'About Q84 Digital',
              'A senior-led Business Central consultancy with offices in Vancouver, BC and Tacoma, WA. The person who scopes your project is the person who delivers it.') + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Who we are</span><h2>Senior Dynamics expertise on every project</h2>
    <p class="lede">Q84 Digital was founded by Oleh Karnaukhov, a Microsoft Dynamics consultant with more than 15 years of ERP and supply chain experience. Before starting Q84 Digital he worked across the Dynamics 365 family, from Business Central to Supply Chain Management, Customer Engagement and Field Service.</p>
    <p>That range matters when you choose an ERP. Because we’ve worked hands-on with both Business Central and the larger Dynamics 365 products, we can tell you honestly when Business Central is enough and when it isn’t.</p>
  </div>
  {about_photo}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Experience</span><h2>Where our experience comes from</h2></div>
  <div class="grid g3">
    <div class="card">{icon('ledger')}<h3>Business Central</h3><p>Implementation, migration, integration and support for small and midsize companies.</p></div>
    <div class="card">{icon('warehouse')}<h3>Supply chain &amp; warehousing</h3><p>Inventory, purchasing, warehouse and transportation processes, from the shop floor up.</p></div>
    <div class="card">{icon('link')}<h3>The wider Dynamics 365 family</h3><p>Supply Chain Management, Customer Engagement and Field Service, and how they connect to Business Central.</p></div>
  </div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">How we work</span><h2>What you can expect from us</h2></div>
  {checks(['<strong>Senior-led from start to finish.</strong> No hand-off from sales to a junior delivery team.', '<strong>Honest fit advice.</strong> If Business Central isn’t right for you, we’ll say so, even if it means no project.', '<strong>Configure first.</strong> Standard features and proven apps before custom code, so your system stays easy to update.', '<strong>Clear scope and cost.</strong> A written, fixed scope after discovery, so you know what you’re paying for.', '<strong>Here after go-live.</strong> The same consultant supports you once you’re live.'])}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Two offices</span><h2>Vancouver and Tacoma, working across the US and Canada</h2><p class="lede">We have offices in Vancouver, British Columbia and Tacoma, Washington. We work on site with companies across the Vancouver and Seattle–Tacoma areas, and remotely with clients anywhere in the US and Canada.</p><p><a class="more" href="@/business-central-partner-tacoma/">Business Central in Tacoma &amp; Seattle →</a></p></div>
  {checks(['<strong>Who we work with today:</strong> distributors, a marketing agency, a hair transplant clinic and a construction and restoration company.', '<strong>Microsoft partner:</strong> ' + esc(CFG.get('partner_statement') or 'We help you choose and manage the right Microsoft licenses.')])}
</div></section>
{cta('Talk to the person who would deliver your project')}''', [ABOUT_SCHEMA])

# TACOMA / SEATTLE
LOCAL_SCHEMA = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": URL + "#organization", "name": "Q84 Digital",
                "areaServed": [{"@type": "City", "name": n} for n in ('Tacoma', 'Seattle', 'Bellevue', 'Kent', 'Auburn', 'Puyallup', 'Federal Way', 'Lakewood', 'Everett', 'Olympia')] + [{"@type": "State", "name": "Washington"}]}
FAQ_LOCAL = [
    ('Do you meet clients in person?', 'Yes, for companies in the Seattle–Tacoma area. Discovery workshops, warehouse walkthroughs, training and go-live support can happen at your office or warehouse. Day-to-day project work happens online.', None),
    ('Can Business Central handle Washington sales tax?', 'Yes. Washington uses destination-based sales tax, so the rate depends on where goods are delivered. Business Central handles this with tax areas and jurisdictions, or you can connect a tax engine such as Avalara if you ship to many locations or several states.', None),
    ('Do you only work with companies in Washington?', 'No. We’re based in Tacoma, but Business Central is a cloud system and we work remotely with companies across the US.', None),
]
add('business-central-partner-tacoma/', 'local',
    'Business Central Consultant in Seattle & Tacoma, WA | Q84 Digital',
    'Business Central consultants in Seattle, Tacoma and across Washington: on-site workshops, implementation and support for Puget Sound businesses.',
    page_head('Seattle & Tacoma', 'Business Central in Seattle &amp; Tacoma', 'Business Central consultant in Seattle, Tacoma &amp; Washington',
              'Senior-led Microsoft Dynamics 365 Business Central implementation and support for companies in Tacoma, Seattle and across the Puget Sound.', art=('page-tacoma.webp', 'Illustration of a port with a container crane, cargo ship, warehouse and a snow-capped mountain')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Local partner</span><h2>A Business Central consultant down the road, not across the country</h2>
    <p class="lede">Q84 Digital is based in Tacoma. For Puget Sound companies that means workshops in your building, a consultant who can walk your warehouse floor, and someone nearby when you go live.</p></div>
  {checks(['<strong>On-site when it matters.</strong> Discovery workshops, warehouse walkthroughs, training and go-live day.', '<strong>Online the rest of the time.</strong> Design, build and testing happen remotely, which keeps costs down.', '<strong>Pacific time, same working day.</strong> Questions get answered while your team is still at work.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Who we help</span><h2>Business Central for Puget Sound businesses</h2>
    <p class="lede">The region runs on distribution, manufacturing and services, from port-linked importers to Kent Valley warehouses and professional firms in Seattle and Bellevue.</p></div>
  <div class="fgrid">
    <a class="fitem" href="@/industries/distribution/">{icon('truck')}<h3>Distributors &amp; importers</h3><p>Multi-location stock, landed costs on imported goods, and warehouse picking and shipping.</p><span class="more">Distribution →</span></a>
    <a class="fitem" href="@/industries/manufacturing/">{icon('factory')}<h3>Manufacturers</h3><p>Bills of materials, production orders, material planning and product costing.</p><span class="more">Manufacturing →</span></a>
    <a class="fitem" href="@/industries/ecommerce/">{icon('shop')}<h3>E-commerce brands</h3><p>Shopify and marketplace orders, stock sync and fulfillment in one system.</p><span class="more">E-commerce →</span></a>
    <a class="fitem" href="@/industries/professional-services/">{icon('ledger')}<h3>Professional services</h3><p>Agencies, clinics, construction and restoration companies that bill by job, project or contract.</p><span class="more">Service businesses →</span></a>
  </div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Service area</span><h2>Where we work on site</h2><p class="lede">We visit clients across the Seattle–Tacoma area and work remotely with companies anywhere in the US.</p></div>
  {checks(['<strong>South Sound:</strong> Tacoma, Fife, Puyallup, Lakewood, University Place, Gig Harbor and Olympia.', '<strong>Kent Valley &amp; South King County:</strong> Kent, Auburn, Federal Way, Renton and Tukwila.', '<strong>Seattle &amp; Eastside:</strong> Seattle, Bellevue, Redmond and Kirkland.', '<strong>North Sound:</strong> Lynnwood, Everett and Marysville.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we do</span><h2>Business Central services</h2></div>
  <div class="fgrid">
    <a class="fitem" href="@/implementation/">{icon('tools')}<h3>Implementation</h3><p>Business Central set up around your processes, from discovery to go-live.</p><span class="more">Implementation →</span></a>
    <a class="fitem" href="@/migration/">{icon('migrate')}<h3>Migration</h3><p>From QuickBooks, Dynamics GP, Dynamics NAV, Sage or spreadsheets.</p><span class="more">Migration →</span></a>
    <a class="fitem" href="@/rescue/">{icon('support')}<h3>Rescue &amp; recovery</h3><p>Stalled projects and systems that never worked properly.</p><span class="more">Rescue &amp; recovery →</span></a>
    <a class="fitem" href="@/support/">{icon('chart')}<h3>Support</h3><p>Fixes, improvements and training once you’re live.</p><span class="more">Support →</span></a>
  </div>
</div></section>
{faq_section(FAQ_LOCAL, 'Questions from Washington businesses').replace('<section class="band">', '<section>', 1)}
{cta('Meet a Business Central consultant in Tacoma', 'Book a free 30-minute call. If you’re in the Puget Sound area, we can follow up with an on-site visit.')}''', [LOCAL_SCHEMA, faq_schema(FAQ_LOCAL)])

# RESCUE
FAQ_RES = [
    ('Can we switch Business Central partners in the middle of a project?', 'Yes. Your Business Central environment and data belong to you, and your licenses can stay where they are or move to a new partner. We’ll help you get admin access, documentation and any custom code handed over cleanly.', None),
    ('Do we have to start over?', 'Rarely. Most struggling systems have a sound foundation with specific problems on top: wrong setup, bad data or unfinished processes. We fix those first. A fresh start is only worth it when the setup is wrong at its core, and we’ll show you why before recommending it.', None),
    ('How quickly can you start?', 'The health check usually starts within one to two weeks of your call. If something is blocking daily work, such as invoices that won’t post, we deal with that first.', None),
    ('What does a health check cost?', 'It’s a fixed-price review agreed up front, sized to your system. You get a written report you can act on with us, on your own or with another partner.', None),
]
add('rescue/', 'rescue',
    'Business Central Rescue & Recovery Partner | Q84 Digital',
    'Business Central project stalled, over budget or live but not working? A senior consultant finds what went wrong and gets your system back on track.',
    page_head('Rescue', 'Services / Rescue &amp; recovery', 'Business Central rescue and recovery',
              'Your Business Central project has stalled, run over budget, or gone live without working properly. We find out why and get it back on track.', art=('page-rescue.webp', 'Illustration of a laptop dashboard with a warning turning green, a life ring, a toolbox and a checklist')) + f'''
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Warning signs</span><h2>Does this sound familiar?</h2><p class="lede">A struggling ERP rarely fails all at once. It shows up as workarounds, spreadsheets coming back and a team that stops trusting the numbers.</p></div>
  {checks(['<strong>The go-live date keeps moving.</strong> Months later, you’re still not live and the budget is gone.', '<strong>Live, but nobody trusts it.</strong> Inventory, receivables or margins don’t match reality.', '<strong>Month-end takes longer than before.</strong> Finance reconciles Business Central against spreadsheets.', '<strong>Your partner has gone quiet.</strong> Tickets sit unanswered, or the consultants you knew have left.', '<strong>Too much custom code.</strong> Every Microsoft update breaks something.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How we fix it</span><h2>From health check to a stable system</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Step</th><th>What happens</th><th>You receive</th></tr></thead>
    <tbody>
      <tr><td>1. Triage</td><td>We deal with anything stopping daily work, such as documents that won’t post or a broken integration.</td><td>Business running again</td></tr>
      <tr><td>2. Health check</td><td>Review of setup, posting groups, data, extensions, integrations and how your team actually uses the system.</td><td>Written findings, ranked by business impact</td></tr>
      <tr><td>3. Recovery plan</td><td>What to fix, in what order, with effort and cost for each item. Some are quick wins, some are projects.</td><td>Fixed-scope plan you approve</td></tr>
      <tr><td>4. Fix</td><td>Correct setups, clean data, replace fragile customizations with standard features, finish missing processes.</td><td>A system that matches how you work</td></tr>
      <tr><td>5. Retrain &amp; hand over</td><td>Role-based training and simple guides, then ongoing support if you want it.</td><td>A team that trusts the system</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Root causes</span><h2>What usually goes wrong</h2><p class="lede">Most rescues trace back to the same handful of causes. Knowing which one you have tells us how big the fix is.</p></div>
  {checks(['<strong>Posting setup.</strong> General and inventory posting groups that don’t match how the business reports.', '<strong>Data loaded as-is.</strong> Duplicates, wrong units of measure and bad opening balances.', '<strong>Processes never finished.</strong> Warehouse, approvals or purchasing set up halfway.', '<strong>Customization instead of configuration.</strong> Code replacing features Business Central already has.', '<strong>No training.</strong> Users never learned the new way, so they kept the old one.'])}
</div></section>
<section class="band"><div class="wrap">
  {worked('Fixing month-end at a distributor whose project stalled',
          'A 30-person distributor went live on Business Central with its first partner a year earlier. Inventory value never matches the balance sheet, month-end takes two weeks, and the original consultants have moved on.',
          [('Week 1', 'Triage: fix the two integrations that stopped syncing orders, so daily trading is back to normal.'),
           ('Weeks 2 to 3', 'Health check finds inventory posting groups mapped to the wrong accounts and item costs never adjusted.'),
           ('Weeks 4 to 6', 'Correct posting setup, run cost adjustment, reconcile inventory to the general ledger and document the month-end routine.'),
           ('Weeks 7 to 8', 'Replace a custom costing report with standard Business Central reports and train the finance team on the new close checklist.')],
          'Inventory reconciles to the balance sheet every month, and month-end drops from two weeks to three days.')}
</div></section>
{faq_section(FAQ_RES) .replace('<section class="band">', '<section>', 1)}
{related('Related services', band=True, items=[('@/support/', 'Business Central support', 'Hourly or monthly help once your system is stable.'), ('@/implementation/', 'Implementation', 'How we run a project so it doesn’t need rescuing.'), ('@/development/', 'Development', 'Replacing fragile customizations with clean extensions.')])}
{cta('Get your Business Central project back on track', 'Tell us what’s happening. We’ll tell you honestly how big the fix is.')}''', [faq_schema(FAQ_RES)])

# DEVELOPMENT
FAQ_DEV = [
    ('Will custom extensions break when Business Central updates?', 'Extensions built on Microsoft’s extension model don’t change Business Central’s own code, which makes updates far safer than old-style customizations. We still test every extension against Microsoft’s release previews before each major update.', None),
    ('Who owns the code?', 'You should. We recommend keeping your extension source code in a repository your company controls, such as Azure DevOps or GitHub, so you’re never locked in to one developer.', None),
    ('Can you take over extensions someone else wrote?', 'Yes. We review the code first, fix anything risky and document what it does before making changes.', None),
    ('Do you build AppSource apps?', 'Our focus is extensions for your company (per-tenant extensions). If your idea would help many Business Central customers, we can talk about what publishing on AppSource involves.', None),
]
add('development/', 'development',
    'Business Central Developer & Custom AL Extensions | Q84 Digital',
    'Hire a Business Central developer for custom AL extensions, reports, APIs and integrations, built on Microsoft’s extension model so updates stay safe.',
    page_head('Development', 'Services / Development', 'Business Central development and AL extensions',
              'Custom fields, pages, reports, business logic and integrations, built as AL extensions that survive Microsoft’s updates.', art=('page-development.webp', 'Illustration of a laptop showing code, puzzle pieces snapping together and a gear')) + f'''
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we build</span><h2>Custom work for Business Central</h2>
  <p class="lede">Every company has a few processes that standard Business Central doesn’t quite cover. We build those as clean extensions, and only after checking that standard features or an existing app can’t do the job.</p></div>
  <div class="grid g3">
    <div class="card">{icon('tools')}<h3>AL extensions</h3><p>New fields, pages, validations and business logic, added without touching Microsoft’s code.</p></div>
    <div class="card">{icon('receipt')}<h3>Reports &amp; documents</h3><p>Invoices, packing slips, labels and management reports in Word, Excel or RDLC layouts.</p></div>
    <div class="card">{icon('link')}<h3>APIs &amp; integrations</h3><p>Custom API pages and connections to the other systems your business runs on.</p></div>
    <div class="card">{icon('chart')}<h3>Automation</h3><p>Job queue tasks, workflows and Power Automate flows for routine work.</p></div>
    <div class="card">{icon('warehouse')}<h3>Warehouse &amp; operations</h3><p>Picking rules, labels and scanning steps tailored to how your floor works.</p></div>
    <div class="card">{icon('migrate')}<h3>NAV code conversion</h3><p>Old C/AL customizations rewritten as AL extensions, or replaced with standard features.</p></div>
  </div>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Our approach</span><h2>Build less, build it right</h2><p class="lede">Every line of custom code is something to test and maintain. The best extension is often the one you don’t need.</p></div>
  {checks(['<strong>Fit check first.</strong> Standard setup, an AppSource app or a custom extension: we compare cost and upkeep with you.', '<strong>Written specification.</strong> You approve what will be built, and the price, before work starts.', '<strong>Built for updates.</strong> Microsoft’s extension model, events and APIs only. No changes to base code.', '<strong>Tested and documented.</strong> Tested against realistic data and Microsoft’s release previews, with notes your team can read.', '<strong>Your code, your repository.</strong> We recommend keeping the source in a repository your company controls.'])}
</div></section>
<section><div class="wrap">
  {worked('A custom pallet label for a distributor',
          'A distributor prints pallet labels from a separate program and types order details into it by hand. Mislabeled pallets cause returns from two large retail customers.',
          [('Spec', 'Agree label content per customer: order number, PO, ship-to, carton count and a scannable code.'),
           ('Build', 'An AL extension adds a label layout and a Print Pallet Label action on warehouse shipments.'),
           ('Test', 'Print labels for real orders and scan them with the customers’ required formats.'),
           ('Deploy', 'Install in production after the test sign-off, with a one-page guide for the shipping team.')],
          'Labels print straight from the shipment with no retyping, and label-related returns stop.')}
</div></section>
{faq_section(FAQ_DEV)}
{related('Related services', [('@/integrations/', 'Integrations', 'Shopify, EDI, Power BI and other systems connected to Business Central.'), ('@/migration/dynamics-nav/', 'NAV to Business Central', 'Moving old NAV customizations to modern extensions.'), ('@/rescue/', 'Rescue &amp; recovery', 'Fixing systems weighed down by risky custom code.')])}
{cta('Need something Business Central doesn’t do out of the box?', 'Describe the process. We’ll tell you whether it needs custom work, an app or just the right setup.')}''', [faq_schema(FAQ_DEV)])


# BLOG
# Each post: slug, title, date (YYYY-MM-DD), summary, tag, body (HTML), placeholder (True = shows a draft notice)
POSTS = [
    dict(slug='signs-you-have-outgrown-quickbooks',
         title='Seven signs your distribution business has outgrown QuickBooks',
         seo_title='7 Signs Your Distribution Business Has Outgrown QuickBooks',
         date='2026-11-16', tag='ERP selection',
         summary='QuickBooks is a great start for a small business. These seven signs mean your distribution company has grown past it, and what to do next.',
         body='''<p>QuickBooks is where most distributors start, and for good reason: it’s affordable, familiar and good at basic accounting. But distribution is an inventory business, and QuickBooks was built for accounting first. Somewhere between a few hundred and a few thousand SKUs, the workarounds start to cost more than the software saves. Here are the seven signs we see most often.</p>
<h2>1. Your real inventory lives in a spreadsheet</h2>
<p>If the stock numbers your team trusts are in Excel rather than QuickBooks, your books are only as accurate as the last time someone copied numbers across. Every manual update is a chance to oversell, under-order or misstate inventory value on the balance sheet. (Here’s <a href="@/migration/spreadsheets/">how spreadsheet data moves into an ERP</a>.)</p>
<h2>2. You stock more than one location</h2>
<p>A second warehouse, a 3PL or even a van stock location changes everything. You need to know what’s where, move stock between locations and pick from the right place. QuickBooks can track locations in its higher editions, but bins, transfers and location-level replenishment quickly push past what it was designed for.</p>
<h2>3. Purchasing runs on memory</h2>
<p>When buyers reorder based on gut feel or a weekly spreadsheet review, you end up with too much of what doesn’t sell and not enough of what does. A distribution ERP suggests purchase orders from reorder points, lead times and actual demand.</p>
<h2>4. You can’t see true margin</h2>
<p>Freight, duty and handling change what a product really costs you. If landed costs never reach the item, your margin reports are optimistic, and some of your best-selling products may be your least profitable.</p>
<h2>5. Month-end takes a week</h2>
<p>If finance spends days exporting, reconciling and rebuilding reports in Excel, the system isn’t doing its job. Inventory value that doesn’t match the general ledger is the classic symptom.</p>
<h2>6. Orders are typed more than once</h2>
<p>A web order retyped for the warehouse, then again for invoicing, costs time and causes errors. When orders come from Shopify, EDI or email, they should flow into one system automatically.</p>
<h2>7. Your team has outgrown the file</h2>
<p>Slow company files, user limits, thin permissions and no approval workflows are signs the business has grown past a small-business tool. Growth should make your systems more useful, not more fragile.</p>
<blockquote>If three or more of these sound familiar, it’s time to look at an ERP, not another spreadsheet.</blockquote>
<h2>Is it QuickBooks, or is it your processes?</h2>
<p>Before blaming the software, it’s worth checking. Some problems follow you to any system: no one owns the item list, receipts aren’t entered on the day goods arrive, or counts are never reconciled. A new ERP won’t fix those on its own, but it does make them visible and gives you the tools to enforce better habits, such as required fields, approval workflows and posted entries that can’t be quietly edited.</p>
<p>A useful test: if your team follows a consistent process and still needs spreadsheets to get answers, the system is the bottleneck. If the process itself varies from person to person, fix that first, ideally as part of the ERP project.</p>
<h2>What about QuickBooks Enterprise or add-on apps?</h2>
<p>Many distributors try to stretch QuickBooks first, with QuickBooks Enterprise’s advanced inventory or a separate inventory app synced to QuickBooks Online. That can buy a year or two. The trade-offs show up as the business grows: two systems to reconcile, sync errors to chase, reporting split across tools, and limits on users, locations or transaction volume. When you find yourself adding a third or fourth app to cover gaps, you’re effectively building an ERP out of parts, without the single database that makes an ERP worth having.</p>
<h2>What moving to an ERP actually involves</h2>
<p>For a small or midsize distributor, a move from QuickBooks to an ERP such as Business Central usually takes two to six months, depending on how many locations, integrations and warehouse processes are in scope. The main steps are:</p>
<ul><li><strong>Discovery:</strong> how you buy, stock, sell, ship and close the month today.</li><li><strong>Design:</strong> chart of accounts, dimensions, item setup and warehouse processes in the new system.</li><li><strong>Data migration:</strong> customers, vendors, items, open invoices and bills, and opening balances, with stock from a physical count.</li><li><strong>Testing and training:</strong> your team runs real orders end to end before go-live.</li><li><strong>Go-live:</strong> usually at the start of a month, with support through the first close.</li></ul>
<p>Most of your QuickBooks history doesn’t need to move. Keep QuickBooks available for lookups, and bring open items, balances and summary history into the new system. See <a href="@/guides/implementation-timeline/">how long implementation takes</a> for a week-by-week example.</p>
<h2>What it costs</h2>
<p>An ERP costs more than QuickBooks, both in monthly licenses and in a one-time implementation. The return comes from the problems above: fewer stockouts and overstock, faster month-end, less retyping and fewer costly mistakes. Our <a href="@/guides/implementation-cost/">implementation cost guide</a> breaks down the budget, and the <a href="@/licensing/#calculator">license calculator</a> estimates your monthly cost from your number of users.</p>
<h2>Questions to ask before choosing a replacement</h2>
<ul><li>Does it track stock by location and bin, with costs that flow to the general ledger?</li><li>Can it suggest purchase orders from reorder points, lead times and open orders?</li><li>How does it handle landed costs such as freight and duty?</li><li>Can it take orders from your web store and EDI customers without retyping?</li><li>Can your team use Excel and Outlook with it?</li><li>Who will implement and support it, and have they moved other distributors off QuickBooks?</li></ul>
<p>A system that answers yes to most of these will remove the workarounds that QuickBooks forces on a growing distributor. A partner who has done the move before will help you avoid the data problems that make migrations painful: duplicate customers, inconsistent units of measure and inventory values that don’t match the books.</p>
<h2>How long can you wait?</h2>
<p>There’s rarely a perfect moment to change systems, but there are bad ones. Avoid starting an ERP project right before your busiest season, and avoid going live in the middle of it. Most distributors plan to go live in a quieter month, which means starting the project three to six months earlier. If you can see the signs above today, the cost of waiting another year is usually more stockouts, more overstock and more hours lost to reconciling, at a time when the business is larger and the move is harder.</p>
<h2>Making the case internally</h2>
<p>Owners and finance leaders usually want the business case in numbers. Estimate the hours spent each month on retyping orders, reconciling inventory and rebuilding reports; the cost of stockouts and emergency freight; and the stock written off or discounted because nobody knew it was there. Even rough figures usually show that the workarounds already cost more than the system would. Pair that with the risks of staying put: key-person dependency on whoever maintains the spreadsheets, and growth that the current setup can’t support.</p>
<h2>Who should be involved</h2>
<p>An ERP decision isn’t only finance’s. Involve whoever runs purchasing, the warehouse and sales from the start; they will use the system every day and know where today’s workarounds are. A small selection team of three or four people, with one clear decision-maker, usually works better than a large committee.</p>
<h2>Common mistakes when leaving QuickBooks</h2>
<ul><li><strong>Bringing all the history.</strong> Years of transactions slow the project and rarely get used. Bring open items, balances and summary history; keep QuickBooks for lookups.</li><li><strong>Copying the old chart of accounts.</strong> A move is the best chance to simplify it and use dimensions instead of dozens of similar accounts.</li><li><strong>Skipping the physical count.</strong> Opening stock should come from a count, not from the spreadsheet everyone already distrusts.</li><li><strong>Training too early.</strong> Train people in the last few weeks before go-live, on their own data, so it sticks.</li></ul>
<h2>What to do next</h2>
<p>Start by writing down what hurts most and what “better” would look like: accurate stock by location, faster month-end, fewer typed orders. Then look at systems built for distribution. Microsoft Dynamics 365 Business Central is a common next step for QuickBooks users because it adds real inventory, warehousing and purchasing while keeping finance familiar and working with Microsoft 365.</p>
<p>Moving is less disruptive than most companies expect. Customers, vendors, items, open invoices and balances come across; the old transaction history usually stays in QuickBooks for reference. See <a href="@/migration/quickbooks/">how a QuickBooks to Business Central migration works</a>, or use our <a href="@/guides/erp-readiness-checklist/">free ERP readiness checklist</a> to get your team on the same page first.</p>'''),
]

def fmt_date(d):
    x = date.fromisoformat(d)
    return f'<time datetime="{d}">{x.strftime("%B")} {x.day}, {x.year}</time>'

def post_card(p):
    draft = '<span class="pill low">Placeholder</span>' if p.get('placeholder') else ''
    return f'''<a class="card post-card" href="@/blog/{p['slug']}/"><span class="tag">{esc(p['tag'])}</span>{draft}<h3>{esc(p['title'])}</h3><p>{esc(p['summary'])}</p><span class="post-meta">{fmt_date(p['date'])}</span></a>'''

add('blog/', 'blog', 'Business Central & ERP Blog | Q84 Digital',
    'Practical articles on Microsoft Dynamics 365 Business Central, ERP selection, inventory and warehouse operations for distributors and manufacturers.',
    page_head('Blog', 'Blog', 'Insights on Business Central and operations',
              'Practical articles on ERP selection, inventory, warehousing and getting the most out of Business Central.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap">
  <h2 class="sr-only">Latest articles</h2>
  <div class="grid g3">{''.join(post_card(p) for p in sorted(POSTS, key=lambda p: p['date'], reverse=True))}</div>
</div></section>
{checklist_promo()}
{cta()}''')

for p in POSTS:
    notice = '<div class="note" style="margin-bottom:24px"><strong>Placeholder article.</strong> This page uses dummy text to show the blog layout. Real content will replace it before launch.</div>' if p.get('placeholder') else ''
    schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'], "datePublished": p['date'], "dateModified": p.get('updated', p['date']), "image": URL + "images/og-default.jpg",
              "author": {"@id": URL + "#organization"}, "publisher": {"@id": URL + "#organization"},
              "mainEntityOfPage": URL + f"blog/{p['slug']}/"}
    add(f"blog/{p['slug']}/", 'blog', p.get('seo_title') or f"{p['title']} | Q84 Digital", p['summary'],
        f'''<article class="post"><div class="wrap post-wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="@/">Home</a> / <a href="@/blog/">Blog</a></nav>
  <span class="tag post-tag">{esc(p['tag'])}</span>
  <h1>{esc(p['title'])}</h1>
  <div class="byline"><span><span>{fmt_date(p['date'])}</span></span></div>
  {notice}
  <div class="post-body">{p['body']}</div>
  <p style="margin-top:32px"><a class="more" href="@/blog/">\u2190 All articles</a></p>
</div></article>
{checklist_promo()}
{cta()}''', [schema])

# CONTACT
phone_card = f'<div class="card"><span class="tag">Phone</span><p class="mono" style="color:var(--ink)"><a href="tel:{PHONE_TEL}" style="color:inherit">{esc(CFG["phone"])}</a></p></div>' if CFG.get('phone') else ''
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
  <div class="sent" id="bookSent" hidden role="status" tabindex="-1"><h3>Thank you, your request has been received</h3><p id="bookSentText"></p></div>
  <noscript><p class="hint">The scheduler needs JavaScript. Email ''' + esc(EMAIL) + ''' with a few times that suit you.</p></noscript>
</div>'''

add('contact/', 'contact',
    'Free ERP Readiness Assessment | Q84 Digital',
    'Book a free 30-minute ERP readiness assessment. Find out whether Business Central fits your business, what it would involve and what it would cost.',
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


# GUIDES: ERP readiness checklist
CL_AREAS = [('Business goals and ownership', 'Why you need to change, the outcomes you expect and who makes decisions.'), ('Current systems and processes', 'What you use today, what stays and where spreadsheets fill the gaps.'), ('Finance and reporting', 'Chart of accounts, approvals, month-end close, tax and historical data.'), ('Inventory, purchasing and sales', 'Item data, costing, replenishment, pricing and traceability.'), ('Warehouse and fulfillment', 'Receiving to shipping, scanning, bins, carriers and 3PLs.'), ('Manufacturing and service', 'BOMs, routings, production, quality and service work.'), ('Data, integrations and technology', 'Data quality, ecommerce, EDI, CRM and security.'), ('People and change', 'Workshops, testing, training and keeping your team informed.'), ('Budget, timeline and scope', 'Costs, realistic dates, priorities and support after go-live.')]
CL_SCHEMA = {"@context": "https://schema.org", "@type": "DigitalDocument", "name": "ERP Readiness Checklist",
             "description": "A free, fillable 52-question checklist to prepare distributors and manufacturers for a Microsoft Dynamics 365 Business Central project.",
             "encodingFormat": "application/pdf", "url": URL + "downloads/q84-erp-readiness-checklist.pdf",
             "author": {"@id": URL + "#organization"}, "inLanguage": "en-US", "isAccessibleForFree": True}
add('guides/erp-readiness-checklist/', 'checklist',
    'Free ERP Readiness Checklist for Business Central | Q84 Digital',
    'Download a free, fillable ERP Readiness Checklist. 52 questions across 9 areas help distributors and manufacturers prepare for a Business Central project.',
    page_head('Guides', '<a href="@/guides/">Guides</a> / ERP readiness checklist', 'Free ERP Readiness Checklist',
              'Find the gaps before you choose an ERP. 52 practical questions across 9 areas, written for distributors and manufacturers considering Microsoft Dynamics 365 Business Central.', button=False) + f'''
<section style="padding-top:32px"><div class="wrap split cl-hero">
  <div class="stack">
    <span class="eyebrow">What it helps you do</span><h2>Get your team aligned before the first workshop</h2>
    {checks(['<strong>Spot gaps early.</strong> Mark each question Yes, Partly or No and see where decisions are missing.', '<strong>Get everyone involved.</strong> Finance, sales, purchasing, warehouse and IT each have their own section.', '<strong>Have a better first conversation.</strong> Bring it to your assessment and spend the time on what matters.'])}
    <div class="hero-actions"><a class="btn btn-primary" {DL_ATTR}>Download the checklist (PDF)</a></div>
    <p class="hint">Fillable PDF, 6 pages, US Letter. Fill it in on screen or print it. Enter your email to download.</p>
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

# GUIDES & COMPARISONS
def guide_head(crumb, h1, lede, updated=TODAY, art=None):
    return page_head('Guides', f'<a href="@/guides/">Guides</a> / {crumb}', h1, lede + f' <span class="hint">Updated {fmt_date(updated)} · <a href="@/about/">Oleh Karnaukhov</a></span>', button=False, art=art)

def article_schema(path, headline, desc):
    return {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc,
            "dateModified": TODAY, "image": URL + "images/og-default.jpg", "author": {"@id": URL + "#oleh-karnaukhov"}, "publisher": {"@id": URL + "#organization"},
            "mainEntityOfPage": URL + path}

GUIDE_LIST = [
    ('@/guides/implementation-cost/', 'Guide', 'Business Central implementation cost', 'What a Business Central project really costs, line by line, with typical ranges.'),
    ('@/guides/implementation-timeline/', 'Guide', 'How long implementation takes', 'Typical timelines by project size, phase by phase, and what slows projects down.'),
    ('@/compare/netsuite/', 'Comparison', 'Business Central vs NetSuite', 'Two leading mid-market cloud ERPs compared honestly.'),
    ('@/compare/sage-intacct/', 'Comparison', 'Business Central vs Sage Intacct', 'Full ERP or finance-first cloud accounting?'),
    ('@/compare/odoo/', 'Comparison', 'Business Central vs Odoo', 'Microsoft’s ERP against the modular, open-source-based alternative.'),
    ('@/licensing/#calculator', 'Tool', 'License cost calculator', 'Estimate your monthly Business Central license cost.'),
]

# COST GUIDE
COST_DESC = 'What a Business Central implementation costs: licenses, implementation, data migration, integrations, apps and support, with typical ranges by project size.'
FAQ_COST = [
    ('Why don’t you publish a fixed price?', 'Because two companies with the same number of users can need very different projects. One may need finance and basic inventory; another needs warehousing, manufacturing and three integrations. We give a fixed quote after discovery, once we know which one you are.', None),
    ('What’s the most common reason budgets grow?', 'Scope that wasn’t written down. Requirements that surface late, such as a forgotten integration or a report finance relies on, are the biggest driver of overruns.', None),
    ('Can we lower the cost by doing some work ourselves?', 'Yes. Teams that clean their own data, write their own test scripts and train their own users after a train-the-trainer session can reduce consulting time noticeably.', None),
]
add('guides/implementation-cost/', 'guide-cost',
    'Business Central Implementation Cost (2026 Guide) | Q84 Digital',
    COST_DESC,
    guide_head('Implementation cost', 'How much does a Business Central implementation cost?',
               'An honest breakdown of what you’ll pay, where the money goes and what makes projects bigger or smaller.', art=('page-guide-cost.webp', 'Illustration of a calculator printing a receipt, a stack of coins and a piggy bank')) + f'''
<section style="padding-top:32px"><div class="wrap prose">
<p><strong>The short answer:</strong> for small and midsize US businesses, a <a href="@/business-central/">Business Central</a> implementation is typically a one-time project in the tens of thousands of dollars, plus monthly Microsoft licenses. A focused finance and inventory rollout sits at the lower end. Multi-company, manufacturing or integration-heavy projects can reach six figures. The rest of this guide explains what drives those numbers.</p>
<h2>The six parts of a Business Central budget</h2>
<p>Every Business Central budget is made of the same parts. Some are one-time, some monthly.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="table-wrap"><table>
    <thead><tr><th>Cost</th><th>Type</th><th>What it depends on</th></tr></thead>
    <tbody>
      <tr><td>Microsoft licenses</td><td>Monthly</td><td>Essentials ($80) or Premium ($110) per full user, plus Team Members ($8) for light users, at Microsoft’s US list prices</td></tr>
      <tr><td>Implementation</td><td>One-time</td><td>Modules, companies, locations and how many processes change</td></tr>
      <tr><td>Data migration</td><td>One-time</td><td>Source system, data volume, data quality and how much history you bring</td></tr>
      <tr><td>Integrations</td><td>One-time plus upkeep</td><td>Number of systems and whether a standard connector exists</td></tr>
      <tr><td>Add-on apps</td><td>Monthly</td><td>AppSource apps for EDI, scanning, shipping or tax, priced by their publishers</td></tr>
      <tr><td>Support</td><td>Hourly or monthly</td><td>How much help you want after go-live</td></tr>
    </tbody></table></div>
  <p class="shot-note" style="margin-top:12px">{PRICE_SOURCE}</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Typical ranges</span><h2>What projects of different sizes usually cost</h2><p class="lede">Typical ranges for implementation services at small and midsize US companies, before licenses and apps. Your quote depends on your scope.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Project size</th><th>Typical scope</th><th>Typical implementation cost</th></tr></thead>
    <tbody>
      <tr><td>Focused</td><td>Finance, sales, purchasing and basic inventory; one company; QuickBooks or spreadsheet migration</td><td>$25,000 to $60,000</td></tr>
      <tr><td>Standard</td><td>Adds warehouse processes, migration from another ERP, or one or two integrations</td><td>$60,000 to $150,000</td></tr>
      <tr><td>Complex</td><td>Several companies, manufacturing, advanced warehousing or many integrations</td><td>$150,000 and up, often phased</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Worked example</span><h2>License cost for a 20-person distributor</h2><p class="lede">Ten people post orders, invoices and journals; ten more mostly look things up and approve.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>License</th><th>Users</th><th>Per month</th></tr></thead>
    <tbody>
      <tr><td>Essentials full users</td><td>10 × $80</td><td>$800</td></tr>
      <tr><td>Team Members</td><td>10 × $8</td><td>$80</td></tr>
      <tr><td><strong>Total</strong></td><td></td><td><strong>$880 per month, about $10,560 per year</strong></td></tr>
    </tbody></table></div>
  <p style="margin-top:16px"><a class="btn btn-ghost" href="@/licensing/#calculator">Try the calculator with your numbers</a></p>
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Cost drivers</span><h2>What makes a project bigger</h2></div>
  {checks(['<strong>Manufacturing.</strong> Bills of materials, routings and costing add design and testing time, and need Premium.', '<strong>Warehousing.</strong> Bins, directed picking and scanning add setup, devices and training.', '<strong>Several companies.</strong> Each entity needs setup; inter-company and consolidation add more.', '<strong>Integrations.</strong> Each connected system adds design, build and testing.', '<strong>Messy data.</strong> Cleaning duplicate customers and inconsistent items takes real time.', '<strong>Custom development.</strong> Every extension must be specified, built, tested and maintained.'])}
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Keeping costs down</span><h2>How to spend less without cutting corners</h2></div>
  {checks(['<strong>Start with standard features.</strong> Adapt processes to Business Central where it costs you nothing to do so.', '<strong>Phase the project.</strong> Go live with finance and inventory first, then add warehousing or integrations.', '<strong>Clean data early.</strong> Start deleting duplicates and inactive records before the project starts.', '<strong>Name an owner.</strong> One person who can make decisions quickly saves weeks.', '<strong>Use the readiness checklist.</strong> <a href="' + CHECKLIST_URL + '">Our free checklist</a> surfaces scope gaps before they become change orders.'])}
</div></section>
{faq_section(FAQ_COST, 'Cost questions')}
{related('Keep reading', [('@/guides/implementation-timeline/', 'How long implementation takes', 'Timelines by project size and phase.'), ('@/licensing/', 'Essentials vs Premium', 'Which license plan you need.'), ('@/implementation/', 'Our implementation method', 'How we scope and deliver a project.')])}
{cta('Get a real number for your project', 'Book a free 30-minute call. We’ll give you a realistic range and tell you what would change it.')}''',
    [article_schema('guides/implementation-cost/', 'How much does a Business Central implementation cost?', COST_DESC), faq_schema(FAQ_COST)])

# TIMELINE GUIDE
TIME_DESC = 'How long a Business Central implementation takes: typical timelines by project size, what happens in each phase, and what slows projects down.'
add('guides/implementation-timeline/', 'guide-timeline',
    'How Long Does Business Central Implementation Take? | Q84 Digital',
    TIME_DESC,
    guide_head('Implementation timeline', 'How long does a Business Central implementation take?',
               'Typical timelines by project size, what happens week by week, and the decisions that keep a project on schedule.', art=('page-guide-timeline.webp', 'Illustration of a calendar, an hourglass and a timeline with milestones')) + f'''
<section style="padding-top:32px"><div class="wrap prose">
<p><strong>The short answer:</strong> a focused Business Central rollout for a small or midsize company usually takes two to three months. Adding warehousing, an ERP migration or integrations stretches it to three to six months. Multi-company or manufacturing projects often run six months or more, usually in phases.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="table-wrap"><table>
    <thead><tr><th>Project size</th><th>Typical scope</th><th>Typical timeline</th></tr></thead>
    <tbody>
      <tr><td>Focused</td><td>Finance, sales, purchasing and basic inventory, one company, straightforward data move</td><td>2 to 3 months</td></tr>
      <tr><td>Standard</td><td>Adds warehouse processes, migration from another ERP, or one or two integrations</td><td>3 to 6 months</td></tr>
      <tr><td>Complex</td><td>Several companies, manufacturing, advanced warehousing or multiple integrations</td><td>6 months or more, often phased</td></tr>
    </tbody></table></div>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Phase by phase</span><h2>Where the time goes in a standard project</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Phase</th><th>Typical length</th><th>What happens</th></tr></thead>
    <tbody>
      <tr><td>Discovery</td><td>2 to 4 weeks</td><td>Workshops by area, current processes and requirements</td></tr>
      <tr><td>Design</td><td>1 to 3 weeks</td><td>Requirements mapped to standard features, apps or extensions; fixed scope agreed</td></tr>
      <tr><td>Build</td><td>4 to 10 weeks</td><td>Configuration, extensions and integrations, with data migration running alongside</td></tr>
      <tr><td>Testing &amp; training</td><td>3 to 6 weeks</td><td>Your team runs real processes end to end; role-based training</td></tr>
      <tr><td>Go-live &amp; first close</td><td>2 to 4 weeks</td><td>Cutover, hands-on support and the first month-end in Business Central</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">What slows projects down</span><h2>The usual causes of delay</h2></div>
  {checks(['<strong>Slow decisions.</strong> Questions waiting a week for an answer add up to months.', '<strong>Team availability.</strong> Key users who can’t step away from daily work for workshops and testing.', '<strong>Data cleanup left late.</strong> Dirty data found during the final load.', '<strong>Scope added mid-project.</strong> New requirements after design is signed off.', '<strong>Third parties.</strong> EDI partners, 3PLs or other vendors with their own schedules.'])}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Choosing a go-live date</span><h2>When to switch over</h2></div>
  {checks(['<strong>Start of a month or quarter.</strong> Opening balances are cleaner and reporting periods line up.', '<strong>Avoid your busy season.</strong> Retailers and distributors usually avoid Q4.', '<strong>Not the start of the year if you can help it.</strong> Year-end close and the go-live in the same weeks overload finance.', '<strong>Leave a buffer.</strong> Two weeks of slack between final testing and go-live.'])}
</div></section>
{related('Keep reading', [('@/guides/implementation-cost/', 'Implementation cost', 'What a Business Central project really costs.'), ('@/implementation/', 'Our implementation method', 'The phases and deliverables of our projects.'), (CHECKLIST_URL, 'ERP readiness checklist', '52 questions to prepare your team.')])}
{cta('Planning a go-live date?', 'Book a free 30-minute call and we’ll sketch a realistic timeline for your project.')}''',
    [article_schema('guides/implementation-timeline/', 'How long does a Business Central implementation take?', TIME_DESC)])

# COMPARISONS
def compare_page(path, nav, other, title, desc, lede, rows, bc_better, other_better, faqs, rel, extra='', art=None):
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    add(path, nav, title, desc,
        guide_head(f'Business Central vs {other}', f'Business Central vs {other}', lede, art=art) + f'''
<section style="padding-top:32px"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Side by side</span><h2>How they compare</h2><p class="lede">A general comparison for small and midsize companies. Both products change often; check current details with each vendor. New to Business Central? Start with <a href="@/business-central/">what Business Central does</a>.</p></div>
  <div class="table-wrap"><table class="compare">
    <thead><tr><th></th><th>Business Central</th><th>{other}</th></tr></thead>
    <tbody>{tr}</tbody></table></div>
  <div class="prose" style="margin-top:40px">{extra}</div>
</div></section>
<section class="band"><div class="wrap">
  <div class="grid g2">
    <div class="card"><span class="tag">Choose Business Central if</span><h3>Business Central fits better when…</h3>{checks(bc_better)}</div>
    <div class="card"><span class="tag">Choose {other} if</span><h3>{other} fits better when…</h3>{checks(other_better)}</div>
  </div>
  <p class="shot-note" style="margin-top:16px">We implement Business Central, so we’re not neutral. We’ve tried to be fair, and we’ll tell you on a call if another system suits you better.</p>
</div></section>
{faq_section(faqs).replace('<section class="band">', '<section>', 1)}
{related('Other comparisons', rel, band=True)}
{cta(f'Deciding between Business Central and {other}?', 'Book a free 30-minute call. We’ll look at your requirements and give you a straight answer.')}''',
        [article_schema(path, f'Business Central vs {other}', desc), faq_schema(faqs)])

CMP_REL = {
    'netsuite': ('@/compare/netsuite/', 'Business Central vs NetSuite', 'Two leading mid-market cloud ERPs.'),
    'intacct': ('@/compare/sage-intacct/', 'Business Central vs Sage Intacct', 'Full ERP or finance-first accounting?'),
    'odoo': ('@/compare/odoo/', 'Business Central vs Odoo', 'Microsoft’s ERP against the modular alternative.'),
    'cost': ('@/guides/implementation-cost/', 'Implementation cost', 'What a Business Central project really costs.'),
}

compare_page('compare/netsuite/', 'cmp-netsuite', 'NetSuite',
    'Business Central vs NetSuite: Honest Comparison | Q84 Digital',
    'Business Central vs Oracle NetSuite for small and midsize companies: pricing model, features, customization, Microsoft 365 and when each one fits.',
    'Both are leading cloud ERPs for growing companies. They differ most in pricing model, ecosystem and how they’re customized.',
    [('Vendor', 'Microsoft', 'Oracle'),
     ('Deployment', 'Cloud (Microsoft-hosted), on-premises still available', 'Cloud only'),
     ('Pricing', 'Published per-user prices: Essentials, Premium and Team Members', 'Quoted per customer: base subscription plus users and modules'),
     ('Implementation', 'Through Microsoft partners', 'Through Oracle NetSuite or its partners'),
     ('Customization', 'AL extensions, Power Platform and AppSource apps', 'SuiteScript (JavaScript), SuiteFlow and SuiteApps'),
     ('Microsoft 365', 'Built in: Outlook, Excel, Teams, Power BI', 'Available through integrations'),
     ('Multi-entity', 'Several companies with consolidation and inter-company', 'Strong multi-subsidiary support in NetSuite OneWorld'),
     ('E-commerce', 'Shopify connector built in; others via apps', 'SuiteCommerce and connectors')],
    ['Your company runs on Microsoft 365 and wants Outlook, Excel and Teams to work with the ERP.', 'You want published per-user pricing and a choice of implementation partners.', 'You’re moving from QuickBooks, Dynamics GP or Dynamics NAV.', 'Inventory, warehousing and light manufacturing are central to the business.'],
    ['You run many subsidiaries across countries and need deep global consolidation from day one.', 'You prefer a single vendor for software and implementation.', 'You already use NetSuite add-ons or SuiteCommerce heavily.'],
    [('Is Business Central cheaper than NetSuite?', 'Often, especially on licenses, because Business Central has published per-user prices and Team Members licenses for light users. Implementation cost depends far more on scope than on the product. Get quotes for the same scope to compare fairly.', ('@/guides/implementation-cost/', 'Implementation cost')),
     ('Can we move from NetSuite to Business Central?', 'Yes. Master data, open items and balances move with the same process we use for other ERPs.', ('@/migration/', 'Data migration'))],
    [CMP_REL['intacct'], CMP_REL['odoo'], CMP_REL['cost']], extra='''<h2>Comparing cost fairly</h2>
<p>Business Central publishes its per-user prices: Essentials and Premium for full users, and low-cost Team Members licenses for people who mostly view and approve. NetSuite is quoted per customer, usually as a base platform fee plus users and add-on modules. That makes a like-for-like comparison harder than it looks.</p>
<p>The fairest way to compare is to price the same scope on both: the same number of full and light users, the same modules, and three to five years of subscription rather than year one. Ask both vendors how renewal pricing works, since multi-year contract terms make a real difference to total cost.</p>
<h2>Who implements it</h2>
<p>Business Central is sold and implemented almost entirely through Microsoft partners, so you can choose a firm by industry, size and location, and change partners later without changing software. NetSuite can be implemented by Oracle NetSuite’s own services team or by partners. Either way, the consultant’s experience in your industry matters more than the product logo.</p>
<h2>Day to day with Microsoft 365</h2>
<p>For teams that live in Outlook, Excel and Teams, Business Central’s Microsoft 365 integration is a practical difference. Sales staff can create quotes from Outlook, finance can open almost any list in Excel and publish changes back, and colleagues can share a live customer or order card in a Teams chat.</p>
<h2>Switching between them</h2>
<p>Companies move in both directions. A move is a new implementation either way: master data, open transactions and balances are migrated, and detailed history usually stays in the old system for reference.</p>''', art=('page-cmp-netsuite.webp', 'Illustration of a balance scale weighing a laptop against a cloud'))

compare_page('compare/sage-intacct/', 'cmp-intacct', 'Sage Intacct',
    'Business Central vs Sage Intacct: Honest Comparison | Q84 Digital',
    'Microsoft Dynamics 365 Business Central vs Sage Intacct: full ERP or finance-first cloud accounting, inventory and operations, multi-entity and when each fits.',
    'Sage Intacct is a finance-first cloud accounting system. Business Central is a full ERP. The right choice depends on how much of your business is inventory and operations.',
    [('Focus', 'Full ERP: finance, inventory, warehousing, manufacturing, projects', 'Financial management first, with optional modules'),
     ('Vendor', 'Microsoft', 'Sage'),
     ('Inventory &amp; warehousing', 'Built in, including bins, picking and shipping', 'Inventory module available; lighter on warehousing'),
     ('Manufacturing', 'Built into Premium', 'Usually through partner solutions'),
     ('Multi-entity', 'Several companies with consolidation', 'A known strength, with dimensions and consolidation'),
     ('Pricing', 'Published per-user prices', 'Quoted per customer'),
     ('Microsoft 365', 'Built in', 'Available through integrations')],
    ['You hold inventory, run a warehouse or manufacture products.', 'You want one system for operations and finance, not finance plus separate tools.', 'Your team lives in Microsoft 365.'],
    ['You’re a services, nonprofit or software company with little or no inventory.', 'Finance is the main buyer and multi-entity accounting is the core need.', 'You already run Sage products and want to stay in that family.'],
    [('Can Sage Intacct handle inventory?', 'It has an inventory module that suits simpler needs. Companies with warehouses, bins, picking or manufacturing usually find a full ERP such as Business Central a better fit.', None),
     ('We use Sage 50 or Sage 100. Is Intacct the natural next step?', 'Not automatically. Sage Intacct is a different product from Sage 50 and Sage 100, so either move is a new implementation. Choose on fit, not on the name.', ('@/migration/sage/', 'Sage to Business Central'))],
    [CMP_REL['netsuite'], CMP_REL['odoo'], CMP_REL['cost']], extra='''<h2>Inventory-heavy or finance-first?</h2>
<p>The most useful question is where your complexity sits. If the hard part of your business is purchasing, stock, warehouse and fulfillment, you need a full ERP, and Business Central handles those processes natively. If the hard part is accounting itself, such as many entities, complex revenue recognition or detailed dimensional reporting with little or no inventory, a finance-first system like Sage Intacct is built for that.</p>
<h2>Multi-entity and consolidation</h2>
<p>Both handle several companies. Sage Intacct is known for multi-entity accounting and dimension-based reporting. Business Central runs each entity as a company with consolidation and inter-company postings, which suits most small and midsize groups, and Power BI can report across companies when you need a combined view.</p>
<h2>What it means for your team</h2>
<p>With a finance-first system, operations teams often keep separate tools for inventory, orders or projects, and those need integrating. With a full ERP, more of the business works in one system, but setup covers more departments. Be clear about which teams the new system has to serve before comparing products.</p>''', art=('page-cmp-intacct.webp', 'Illustration of a balance scale weighing warehouse boxes and a forklift against an accounting ledger'))

compare_page('compare/odoo/', 'cmp-odoo', 'Odoo',
    'Business Central vs Odoo: Honest Comparison | Q84 Digital',
    'Microsoft Dynamics 365 Business Central vs Odoo for small and midsize companies: accounting depth, apps, customization, pricing, partners and when each fits.',
    'Odoo is a modular, open-source-based business suite with apps for almost everything. Business Central is Microsoft’s ERP with deep accounting and operations. They suit different companies.',
    [('Model', 'Commercial cloud ERP from Microsoft', 'Open-source Community edition plus a paid Enterprise edition'),
     ('Scope', 'Finance, inventory, warehousing, manufacturing, projects', 'Very broad: ERP plus CRM, website, POS, e-commerce and more'),
     ('Accounting depth', 'Strong US accounting, controls and audit trail', 'Capable, with depth varying by country and version'),
     ('Customization', 'AL extensions and Power Platform', 'Python modules; very flexible'),
     ('Upgrades', 'Microsoft updates twice a year; extensions stay compatible', 'Version upgrades can require reworking custom modules'),
     ('Ecosystem', 'Microsoft 365, Power BI, AppSource', 'Odoo Apps store and community modules'),
     ('Pricing', 'Published per-user prices', 'Published per-user pricing for Enterprise; Community is free')],
    ['Accounting controls, audit trail and reporting matter to your finance team and auditors.', 'You want Microsoft 365 and Power BI working with your ERP.', 'You’re growing past 20 or 30 users and want a large partner ecosystem in the US.', 'You’re replacing QuickBooks, Dynamics GP or Dynamics NAV.'],
    ['Budget is the deciding factor and your needs are simple.', 'You want one suite for website, POS, CRM and operations.', 'You have in-house Python developers and want full control of the code.'],
    [('Is Odoo cheaper than Business Central?', 'Licenses can be cheaper, especially with the Community edition. Total cost depends on implementation and custom development, which can close the gap. Compare quotes for the same scope.', ('@/guides/implementation-cost/', 'Implementation cost')),
     ('Can Odoo and Business Central work together?', 'Possible, but rarely worth it. Running two systems for the same processes usually means duplicate data and reconciliation work.', None)],
    [CMP_REL['netsuite'], CMP_REL['intacct'], CMP_REL['cost']], extra='''<h2>Community vs Enterprise</h2>
<p>Odoo comes in two editions. Community is free and open source; Enterprise is paid per user and adds apps and features, including full accounting, plus hosting options and upgrade support. When you compare costs, compare Odoo Enterprise with the apps you actually need, not the free edition.</p>
<h2>Breadth vs depth</h2>
<p>Odoo’s strength is breadth: CRM, website, e-commerce, point of sale, HR and operations in one suite. Business Central focuses on finance and operations, and connects to Microsoft’s other products, such as Dynamics 365 Sales, Power BI and Microsoft 365, for the rest. Companies whose finance team and auditors need strong controls and US reporting usually lean towards Business Central; companies wanting one low-cost suite for everything often look at Odoo.</p>
<h2>Customization and upgrades</h2>
<p>Odoo is customized in Python and is very flexible, but custom modules often need rework when you move to a new major version. Business Central extensions are built on Microsoft’s extension model and are designed to keep working through Microsoft’s twice-yearly updates, which keeps long-term maintenance predictable.</p>''', art=('page-cmp-odoo.webp', 'Illustration of a balance scale weighing a single blue cube against many puzzle pieces'))

# GUIDES HUB
add('guides/', 'guides',
    'Business Central Guides, Comparisons & Checklists | Q84 Digital',
    'Free Business Central guides: implementation cost and timeline, comparisons with NetSuite, Sage Intacct and Odoo, and an ERP readiness checklist.',
    page_head('Guides', 'Guides', 'Business Central guides',
              'Practical guides, honest comparisons and free tools to help you plan, choose and implement Business Central.', button=False, art=('page-guides.webp', 'Illustration of an open guidebook, a stack of books and a light bulb')) + f'''
<section style="padding-top:32px"><div class="wrap">
  <h2 class="sr-only">All guides and tools</h2>
  <div class="grid g3">
    <a class="card resource-card" href="{CHECKLIST_URL}">
      <img src="@/images/erp-checklist-cover.webp" alt="" width="640" height="828" loading="lazy">
      <span class="tag">Checklist · PDF</span><h3>ERP Readiness Checklist</h3>
      <p>52 questions across 9 areas to find the gaps before you choose an ERP. Fillable, 6 pages.</p>
      <span class="more">See what’s inside →</span></a>
    {''.join(f'<a class="card resource-card" href="{h}"><span class="resource-art">{icon("chart" if t != "Comparison" else "link")}</span><span class="tag">{t}</span><h3>{n}</h3><p>{d}</p><span class="more">Read →</span></a>' for h, t, n, d in GUIDE_LIST)}
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
analytics_line = ''.join([
    '<p>We use Google Analytics to understand how visitors use this site, such as which pages are viewed. It sets cookies and collects information like your approximate location and device type. It does not tell us who you are.</p>' if CFG.get('ga_id') else '',
    '<p>We use Microsoft Clarity to see how visitors use this site, through heatmaps and session recordings of clicks, scrolling and mouse movement. Clarity sets cookies and collects information like your device, browser and approximate location. Text you type into forms is masked and not recorded. The data is processed by Microsoft under the <a href="https://privacy.microsoft.com/privacystatement">Microsoft Privacy Statement</a>.</p>' if CFG.get('clarity_id') else '',
]) or '<p>This site does not currently use analytics or advertising cookies.</p>'
add('privacy/', 'privacy', 'Privacy Policy | Q84 Digital',
    'How Q84 Digital collects, uses and protects personal information submitted through this website.',
    page_head('Privacy', 'Privacy', 'Privacy policy', f'Last updated {date.today().strftime("%B %-d, %Y")}.', button=False) + f'''
<section style="padding-top:24px"><div class="wrap prose">
<p>This policy explains how Q84 Digital handles personal information you share through this website.{legal_line}</p>
<h2>What we collect</h2><p>When you request a consultation we collect the details you enter: your name, business email, company, the topic you choose and any message you write. When you download the ERP Readiness Checklist we collect your email address and, if you enter them, your first name and company.</p>
<h2>How we use it</h2><p>We use your information only to reply to your request, arrange a consultation and follow up about your project. We don't sell or rent it, and we don't add you to marketing lists without your consent.</p>
<h2>Analytics</h2>{analytics_line}
<h2>Embedded videos</h2><p>Some pages include videos hosted on YouTube. Nothing loads from YouTube until you press play. When you do, the video plays from YouTube’s privacy-enhanced mode and YouTube’s privacy policy applies.</p>
<h2>Sharing</h2><p>We share information only with service providers that help us run this website and handle email, and only as needed to provide those services, or where the law requires it.</p>
<h2>Retention and your rights</h2><p>We keep inquiries for as long as needed to respond and manage any resulting work. You can ask to see, correct or delete your information at any time by emailing <span style="user-select:all">{esc(EMAIL)}</span>. If you have a concern we haven’t resolved, you can also contact the Washington State Attorney General’s Office.</p>
</div></section>''')

# ---------------------------------------------------------------- render

def analytics():
    out = ''
    if CFG.get('ga_id'):
        gid = esc(CFG['ga_id'])
        out += f'''<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{gid}');</script>'''
    if CFG.get('clarity_id'):
        # Microsoft Clarity tag, as given in the Clarity project's setup page
        cid = esc(CFG['clarity_id'])
        # Only record the live site, not local previews
        out += f'''<script>if(location.hostname==="{LIVE_HOST}")(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{cid}");</script>'''
    return out

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
<link rel="preload" href="@/assets/fonts/poppins-600-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="@/assets/fonts/open-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="@/assets/site.css?v={CSS_V}">
{analytics()}{schema}<script>window.Q84={client};</script>
</head>
<body>
{header(p['nav'])}
<main id="main">
{p['body']}
</main>
{footer()}
<dialog class="dl-gate" id="dlGate" aria-labelledby="dlGateTitle">
  <form id="dlForm" novalidate>
    <button class="dl-close" type="button" id="dlClose" aria-label="Close">×</button>
    <h2 id="dlGateTitle">Get the ERP Readiness Checklist</h2>
    <p class="hint">Enter your email and the PDF downloads right away. We may follow up once to see if you have questions. No newsletters.</p>
    <div class="field"><label for="dl-email">Business email</label><input id="dl-email" name="email" type="email" autocomplete="email" required><span class="err" id="dl-e-email" hidden>Enter an email address like name@company.com.</span></div>
    <div class="row">
      <div class="field"><label for="dl-name">First name <span class="hint">(optional)</span></label><input id="dl-name" name="name" autocomplete="given-name"></div>
      <div class="field"><label for="dl-company">Company <span class="hint">(optional)</span></label><input id="dl-company" name="company" autocomplete="organization"></div>
    </div>
    <div style="position:absolute;left:-9999px" aria-hidden="true"><label for="dl-gotcha">Leave this empty</label><input id="dl-gotcha" name="_gotcha" tabindex="-1" autocomplete="off"></div>
    <div><button class="btn btn-primary" type="submit">Download the checklist</button></div>
    <p class="hint">See our <a href="@/privacy/">privacy policy</a>.</p>
  </form>
  <div class="dl-done" id="dlDone" hidden role="status"><h2>Your download has started</h2><p>If it didn’t, <a href="@/downloads/q84-erp-readiness-checklist.pdf" download>download the checklist here</a>.</p><button class="btn btn-ghost" type="button" id="dlDoneClose">Close</button></div>
</dialog>

<script src="@/assets/site.js?v={JS_V}" defer></script>
</body>
</html>
'''
    return doc.replace('@/', BASE)

SUBNAV_PAGES = {'business-central/', 'licensing/', 'implementation/', 'migration/', 'integrations/', 'support/', 'industries/distribution/', 'industries/manufacturing/', 'industries/professional-services/',
                'rescue/', 'development/', 'business-central-partner-tacoma/', 'industries/ecommerce/',
                'migration/quickbooks/', 'migration/dynamics-gp/', 'migration/dynamics-nav/', 'migration/sage/', 'migration/spreadsheets/',
                'integrations/shopify/', 'integrations/edi/', 'integrations/power-bi/', 'integrations/warehouse-insight/',
                'guides/implementation-cost/', 'guides/implementation-timeline/'}
# In-depth sections live in src/content_deep.py: path -> (h2, prose html). Each is placed before the
# page's FAQ (or related links / checklist promo / booking section, whichever comes first).
import sys
sys.path.insert(0, os.path.join(ROOT, 'src'))
from content_deep import DEEP
DEEP_MARKERS = ('<span class="eyebrow">FAQ</span>', '<section data-nosubnav', '<section class="promo-section"', '<section class="cta-section"')
DEEP_NO_SUBNAV = {'industries/professional-services/'}  # menu already full on these pages
def add_deep(body, h2, prose, nosub=False):
    sec = f'''<section{' data-nosubnav' if nosub else ''}><div class="wrap">
  <div class="section-head"><span class="eyebrow">In depth</span><h2>{h2}</h2></div>
  <div class="prose deep">{prose}</div>
</div></section>
'''
    for m in DEEP_MARKERS:
        i = body.find(m)
        if i >= 0:
            i = body.rfind('<section', 0, i) if m.startswith('<span') else i
            return body[:i] + sec + body[i:]
    return body + sec

def alternate_bands(body):
    # re-shade content sections plain/band in turn; sections with padding-top:0 continue the one before
    band = True
    def fix(m):
        nonlocal band
        attrs = m.group(1) or ''
        if re.search(r'class="(?!band")', attrs): return m.group(0)
        if 'padding-top:0' not in attrs: band = not band
        attrs = attrs.replace(' class="band"', '')
        return f'<section{attrs}{" class=\"band\"" if band else ""}>'
    return re.sub(r'<section((?: [^>]*)?)>', fix, body)

for p in PAGES:
    if p['path'] in DEEP:
        p['body'] = alternate_bands(add_deep(p['body'], *DEEP[p['path']], nosub=p['path'] in DEEP_NO_SUBNAV))
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

# Old URLs renamed before launch: GitHub Pages has no server redirects, so leave a small page that forwards
REDIRECTS = {'integrations/warehouse-mobile/': 'integrations/warehouse-insight/', 'industries/services/': 'industries/professional-services/', 'data-migration/': 'migration/', 'resources/': 'guides/', 'resources/erp-readiness-checklist/': 'guides/erp-readiness-checklist/'}
for old, new in REDIRECTS.items():
    os.makedirs(os.path.join(ROOT, old), exist_ok=True)
    open(os.path.join(ROOT, old, 'index.html'), 'w').write(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Moved | Q84 Digital</title>
<link rel="canonical" href="{URL}{new}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={BASE}{new}"></head>
<body><p>This page has moved to <a href="{BASE}{new}">{URL}{new}</a>.</p></body></html>
''')

# sitemap + robots
urls = ''.join(f'<url><loc>{URL}{p["path"]}</loc><lastmod>{TODAY}</lastmod></url>' for p in PAGES)
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
rule = 'Allow: /' if CFG.get('allow_indexing', True) else 'Disallow: /'
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\n{rule}\n\nSitemap: {URL}sitemap.xml\n')
print(f'Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt')
