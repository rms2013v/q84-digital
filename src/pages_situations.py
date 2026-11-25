# Situation guides. Executed inside build.py (exec), so it uses build.py's helpers:
# add, page_head, guide_head, checks, cur, faq_section, faq_schema, related, worked, cta, icon, esc,
# article_schema, CAD_RANGES, CUR_SWITCH, CHECKLIST_URL, GUIDE_LIST, URL.
# Dates checked against Microsoft's lifecycle pages in November 2026.

GP_LIFECYCLE = 'https://learn.microsoft.com/dynamics-gp/terms/lifecycle'

# ------------------------------------------------------------------ Dynamics GP end of support
GP_EOS_PATH = 'guides/dynamics-gp-end-of-support/'
GP_EOS_DESC = 'Dynamics GP support ends December 31, 2029, with security patches to April 2031. What stops, what keeps working, and how to plan your move.'
FAQ_GP_EOS = [
    ('Will Dynamics GP stop working after December 31, 2029?', 'No. GP keeps running after support ends. What stops is Microsoft’s help: product updates, tax and regulatory updates and technical support. Security patches, if needed, continue until April 30, 2031. After that, you run GP with no fixes of any kind.', None),
    ('Can we still buy Dynamics GP licenses?', 'Microsoft has stopped selling Dynamics GP to new customers. Existing customers can keep using and paying for their current GP licenses and enhancement plan until support ends.', None),
    ('What happens to GP payroll?', 'Payroll is often the first thing to hurt, because payroll tax updates stop with product support. Business Central doesn’t include payroll, so GP payroll users move payroll to a payroll provider that connects to Business Central. Plan this early: payroll changes are easiest at the start of a calendar year.', None),
    ('Is Business Central the only option?', 'No, but it’s the one Microsoft built a migration path for. Business Central includes tools that bring GP master data, open transactions and history across. Other ERPs such as NetSuite or Sage Intacct mean a fresh data migration without those tools.', ('@/compare/netsuite/', 'Business Central vs NetSuite')),
    ('When should we start?', 'Most GP moves take three to six months once the project starts, and you’ll want a buffer for testing, year-end and payroll timing. Starting the assessment one to two years before the support end date lets you pick a calm go-live date instead of a rushed one.', ('@/guides/implementation-timeline/', 'Implementation timeline guide')),
]
add(GP_EOS_PATH, 'guide-gp-eos',
    'Dynamics GP End of Support: Dates & Options | Q84 Digital',
    GP_EOS_DESC,
    guide_head('Dynamics GP end of support', 'Dynamics GP end of support: dates and your options',
               'Microsoft is retiring Dynamics GP. Here’s exactly what ends and when, what keeps working, and how to plan a move on your own timetable.',
               photo=('guide-gp-diorama', 'Miniature model scene of workers moving servers and boxes by truck from an old office building to a modern building with a cloud-shaped roof', '60% 55%', '30% 60%')) + f'''
<section style="padding-top:32px"><div class="wrap prose">
<p><strong>The short answer:</strong> Microsoft ends product support for Dynamics GP on <strong>December 31, 2029</strong>. That’s the last day for product updates, tax and regulatory updates and technical support. Security patches, if needed, continue until <strong>April 30, 2031</strong>. Older GP versions lose support sooner: GP 2018 on January 11, 2028, and GP 2016 already lost support on July 14, 2026. Microsoft has also stopped selling GP to new customers and points existing customers to <a href="@/business-central/">Dynamics 365 Business Central</a>.</p>
<p>GP won’t switch off on those dates. But every month you run it past them, you carry more risk: tax changes you have to handle yourself, no help when something breaks, and fewer people who know the product.</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Key dates</span><h2>Dynamics GP support dates by version</h2><p class="lede">Find your version in GP under Help, About Microsoft Dynamics GP.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Version</th><th>Status</th><th>Support ends</th></tr></thead>
    <tbody>
      <tr><td>Dynamics GP (version 18.x, kept current)</td><td>Supported</td><td>Product, tax and technical support until December 31, 2029. Security patches until April 30, 2031.</td></tr>
      <tr><td>Dynamics GP 2018 and GP 2018 R2</td><td>Extended support</td><td>January 11, 2028</td></tr>
      <tr><td>Dynamics GP 2016 and GP 2016 R2</td><td>Out of support</td><td>Ended July 14, 2026</td></tr>
      <tr><td>Dynamics GP 2015 and earlier</td><td>Out of support</td><td>Already ended</td></tr>
    </tbody></table></div>
  <p class="shot-note" style="margin-top:12px">Source: <a href="{GP_LIFECYCLE}" target="_blank" rel="noopener">Microsoft Dynamics GP lifecycle policy</a>, checked November 2026. Microsoft has moved these dates before, so check the page for the latest.</p>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">What stops</span><h2>What stops, and what keeps working</h2><p class="lede">Support ending is a gradual risk, not a cliff. These are the parts of GP that feel it first.</p></div>
  {checks(['<strong>Tax and year-end updates stop.</strong> Changes to payroll tax tables, 1099 and T4 forms and sales tax rules are no longer delivered after 2029.', '<strong>No technical support.</strong> If an update to Windows, SQL Server or an add-on breaks GP, Microsoft won’t help fix it.', '<strong>Add-on vendors move on.</strong> Many ISVs that extend GP are already moving their products and people to Business Central.', '<strong>Fewer GP specialists.</strong> Consultants who know GP well are retiring or retraining, and their rates rise as they get scarce.', '<strong>Security patches end in 2031.</strong> After April 30, 2031, newly found vulnerabilities in GP stay open.', '<strong>Your data stays yours.</strong> GP keeps running and your history stays readable for as long as you keep the system.'])}
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Your options</span><h2>Three ways to respond</h2><p class="lede">There’s no single right answer, but there is a wrong one: waiting until 2029 and choosing in a hurry.</p></div>
  <div class="grid g3">
    <div class="card"><span class="tag">Option 1</span><h3>Stay on GP for now</h3><p>Reasonable for a year or two if GP still fits and you have a plan. Keep GP current, keep your enhancement plan, and set a decision date well before the end of 2029.</p></div>
    <div class="card"><span class="tag">Option 2 · Microsoft’s path</span><h3>Move to Business Central</h3><p>The closest fit for most GP users. Microsoft’s migration tools bring master data, open transactions and history across, and the finance concepts will feel familiar. <a href="@/migration/dynamics-gp/">See our GP migration approach</a>.</p></div>
    <div class="card"><span class="tag">Option 3</span><h3>Choose another ERP</h3><p>Worth a look if your business has changed a lot. Compare honestly: <a href="@/compare/netsuite/">NetSuite</a>, <a href="@/compare/sage-intacct/">Sage Intacct</a> and <a href="@/compare/odoo/">Odoo</a> all mean a fresh migration without GP-specific tools.</p></div>
  </div>
</div></section>
<section><div class="wrap split">
  <div class="stack"><span class="eyebrow">Plan backwards</span><h2>A calm timeline to leave GP</h2><p class="lede">Work back from the date you want to be live, not from Microsoft’s deadline. Most companies aim to go live at the start of a fiscal year, with payroll moving on January 1.</p></div>
  {checks(['<strong>Now: take stock.</strong> List your GP modules, add-ons, customizations, reports, integrations and who uses what. Our <a href="' + CHECKLIST_URL + '">ERP readiness checklist</a> helps.', '<strong>12 to 18 months before go-live: choose.</strong> Decide on Business Central or another ERP, and get a written scope and quote.', '<strong>6 to 9 months before: build.</strong> Design, set up, migrate data into a test company and replace add-ons.', '<strong>2 to 3 months before: test.</strong> Your team runs real processes and signs off balances against GP.', '<strong>Go-live: cut over.</strong> Final data load at a period end, with support for the first month-end close. Keep GP read-only for lookups.'])}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">What it costs</span><h2>Budgeting the move off GP</h2><p class="lede">Implementation services for a move off GP typically start at {cur('$35,000 to $50,000', 'CA$35,000 to CA$50,000')}, plus monthly Business Central licenses. Your <a href="@/guides/implementation-cost/">full budget</a> depends on modules, add-ons and integrations.</p></div>
  {checks(['<strong>Smaller and simpler:</strong> finance-only GP with few add-ons can come in lower.', '<strong>Bigger:</strong> manufacturing, several companies or many integrations push it higher.', '<strong>Licenses change shape:</strong> GP’s yearly enhancement plan is replaced by a monthly per-user subscription. Try our <a href="@/licensing/#calculator">license calculator</a>.', '<strong>Fixed scope:</strong> we quote a written, fixed scope after a short discovery, so the number doesn’t move.'])}
</div></section>
{faq_section(FAQ_GP_EOS, 'Dynamics GP end of support questions')}
{related('Keep reading', [('@/migration/dynamics-gp/', 'GP to Business Central migration', 'How the move works, what maps where, and our five-step process.'), ('@/guides/implementation-timeline/', 'How long implementation takes', 'Timelines by project size and phase.'), ('@/guides/implementation-cost/', 'Implementation cost', 'What a Business Central project really costs.')])}
{cta('Plan your move off Dynamics GP', 'Book a free 30-minute call. We’ll look at your GP version, add-ons and payroll, and suggest a realistic timeline.')}''',
    [article_schema(GP_EOS_PATH, 'Dynamics GP end of support: dates and your options', GP_EOS_DESC), faq_schema(FAQ_GP_EOS)])

# ------------------------------------------------------------------ NAV to Business Central cost
NAV_COST_PATH = 'guides/nav-to-business-central-cost/'
NAV_COST_DESC = 'What moving from Dynamics NAV to Business Central costs: upgrade vs re-implementation, what drives the price, typical ranges and how to keep it down.'
FAQ_NAV_COST = [
    ('Is a technical upgrade cheaper than a re-implementation?', 'Not always. An upgrade keeps your setup and history, but every NAV customization still has to be rewritten as an AL extension, and older versions need several upgrade steps. For older or heavily customized NAV systems, a fresh implementation that migrates master data, open items and summary history is often cheaper and leaves you with a cleaner system.', None),
    ('How many customizations is “a lot”?', 'It depends on what they do more than how many there are. A useful first step is an object analysis: we list every modified or custom object in your NAV database and sort each into keep, replace with standard, replace with an app, or retire. Many customizations turn out to be features Business Central now has as standard.', ('@/development/', 'AL development')),
    ('What do Business Central licenses cost compared to NAV?', 'NAV was usually bought once with a yearly enhancement plan. Business Central online is a monthly subscription per user: Essentials or Premium for full users and low-cost Team Members licenses for people who mostly look things up and approve. Hosting, backups and upgrades are included.', ('@/licensing/', 'Business Central licensing')),
    ('Can we spread the cost?', 'Yes. Many NAV customers go live first with finance, sales, purchasing and inventory, then add warehousing, integrations or reporting in a second phase. Phasing spreads the cost and lowers the risk of each go-live.', None),
    ('How do you quote a NAV move?', 'We start with a short assessment of your NAV version, objects, add-ons and integrations, recommend upgrade or re-implementation in writing, and then give you a fixed scope and price for the path you choose.', None),
]
add(NAV_COST_PATH, 'guide-nav-cost',
    'NAV to Business Central Upgrade Cost | Q84 Digital',
    NAV_COST_DESC,
    guide_head('NAV to Business Central cost', 'How much does moving from NAV to Business Central cost?',
               'An honest look at what drives the price of leaving Dynamics NAV, how the two paths compare, and what most companies end up spending.',
               photo=('guide-nav-diorama', 'Miniature model scene of workers sorting parts from an old building beside coins and a calculator, while a crane builds a modern office from blue blocks', '60% 55%', '45% 60%')) + f'''
<section style="padding-top:32px"><div class="wrap prose">
<p><strong>The short answer:</strong> moving from <a href="@/migration/dynamics-nav/">Dynamics NAV to Business Central</a> typically starts at {cur('$35,000 to $50,000', 'CA$35,000 to CA$50,000')} for implementation services, plus monthly Business Central licenses. A small, lightly customized NAV system sits at that starting point. Heavy customization, several companies or manufacturing push it higher. The single biggest factor is how much custom code your NAV system carries.</p>
<p>Timing matters too. NAV 2016 is already out of support, NAV 2017 loses extended support on January 11, 2027, and NAV 2018, the last version, on January 11, 2028.</p>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Typical ranges</span><h2>What NAV moves usually cost</h2><p class="lede">{cur('Implementation services in US dollars, before licenses and apps.', 'Implementation services in Canadian dollars, before licenses, apps and tax.')}</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Your NAV system</th><th>Typical path</th><th>Typical cost</th></tr></thead>
    <tbody>
      <tr><td>One company, finance and basic inventory, few customizations</td><td>Re-implementation with data migration</td><td>{cur('$35,000 to $50,000', 'CA$35,000 to CA$50,000')}</td></tr>
      <tr><td>Warehousing, a handful of add-ons and integrations, moderate custom code</td><td>Either path, after an object analysis</td><td>{cur('$50,000 to $100,000', 'CA$50,000 to CA$100,000')}</td></tr>
      <tr><td>Several companies, manufacturing, heavy custom code or many integrations</td><td>Usually phased</td><td>{cur('$100,000 and up', 'CA$100,000 and up')}</td></tr>
    </tbody></table></div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Cost drivers</span><h2>What makes a NAV move bigger or smaller</h2></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Driver</th><th>Why it matters</th><th>How to keep it down</th></tr></thead>
    <tbody>
      <tr><td>Custom code</td><td>Old C/AL code can’t run in Business Central online; each customization must be replaced, rebuilt as an AL extension or retired.</td><td>Retire what nobody uses and take standard features where they now exist.</td></tr>
      <tr><td>NAV version</td><td>Older versions need more upgrade steps, which is why they often get a fresh implementation instead.</td><td>Let the version decide the path, not habit.</td></tr>
      <tr><td>Add-ons</td><td>Each third-party NAV add-on needs a Business Central version, an AppSource replacement or a rebuild.</td><td>List them all early; many vendors offer a Business Central app.</td></tr>
      <tr><td>Integrations</td><td>Connections to e-commerce, EDI, shipping or banks need rebuilding on Business Central’s APIs.</td><td>Use standard connectors where they exist.</td></tr>
      <tr><td>Data and history</td><td>Every year of detailed history adds mapping and checking.</td><td>Bring open items, balances and summary history; keep NAV read-only for lookups.</td></tr>
      <tr><td>Companies and users</td><td>Each company needs setup, testing and training.</td><td>Phase companies or processes if needed.</td></tr>
    </tbody></table></div>
</div></section>
<section class="band"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Two paths</span><h2>Upgrade or re-implement: the cost trade-off</h2></div>
  <div class="grid g2">
    <div class="card"><span class="tag">Technical upgrade</span><h3>Pays off when NAV is recent and clean</h3><ul class="checks"><li><div>Keeps setup, history and familiar structure</div></li><li><div>Every customization still rewritten in AL</div></li><li><div>Several steps for older versions add cost</div></li><li><div>Carries old data problems forward</div></li></ul></div>
    <div class="card"><span class="tag">Re-implementation</span><h3>Pays off when NAV is old or heavily modified</h3><ul class="checks"><li><div>Standard features first, less custom code to maintain</div></li><li><div>Master data, open items and summary history migrated</div></li><li><div>A chance to fix processes and data</div></li><li><div>Lower running costs after go-live</div></li></ul></div>
  </div>
</div></section>
<section><div class="wrap">
{worked('A 30-user distributor on NAV 2016', 'One company, two warehouses, about 40 modified objects, an EDI add-on and a web shop integration. NAV 2016 is out of support and the server needs replacing.',
        [('Assessment', 'Object analysis sorts the 40 customizations: 22 replaced by standard Business Central features, 6 by AppSource apps, 8 rebuilt as AL extensions, 4 retired.'),
         ('Path', 'Re-implementation, because two upgrade steps plus rewriting the code would cost more than starting clean.'),
         ('Build', 'Business Central online set up around current processes; EDI and web shop reconnected through supported apps.'),
         ('Data', 'Customers, vendors, items, open entries, balances and two years of summary history, with two trial loads.'),
         ('Go-live', 'Cutover at a month end; NAV kept read-only for lookups.')],
        'A mid-range project, with far less custom code to maintain and no more server or upgrade projects.')}
</div></section>
<section class="band"><div class="wrap split">
  <div class="stack"><span class="eyebrow">Keeping costs down</span><h2>How to spend less on leaving NAV</h2></div>
  {checks(['<strong>Start with an object analysis.</strong> Knowing what each customization does is the cheapest way to cut scope.', '<strong>Retire aggressively.</strong> Reports, fields and code nobody uses shouldn’t move.', '<strong>Prefer apps to custom code.</strong> Proven AppSource apps cost less to maintain than your own extensions.', '<strong>Clean data first.</strong> Delete duplicates and inactive records in NAV before migration starts.', '<strong>Phase it.</strong> Finance and inventory first; warehousing and integrations next.'])}
</div></section>
{faq_section(FAQ_NAV_COST, 'NAV upgrade cost questions')}
{related('Keep reading', [('@/migration/dynamics-nav/', 'NAV to Business Central upgrade', 'Upgrade or re-implement, and what happens to your code.'), ('@/guides/implementation-cost/', 'Implementation cost', 'The full Business Central budget, line by line.'), ('@/development/', 'AL extensions', 'Rebuilding the customizations you keep.')])}
{cta('Get a NAV upgrade estimate', 'Book a free 30-minute call. We’ll look at your NAV version and customizations and tell you which path will cost less.')}''',
    [article_schema(NAV_COST_PATH, 'How much does moving from NAV to Business Central cost?', NAV_COST_DESC), faq_schema(FAQ_NAV_COST)])

GUIDE_LIST[2:2] = [
    ('@/' + GP_EOS_PATH, 'Guide', 'Dynamics GP end of support', 'Support dates by version, what stops in 2029 and how to plan your move.'),
    ('@/' + NAV_COST_PATH, 'Guide', 'NAV to Business Central cost', 'What leaving Dynamics NAV costs, and upgrade vs re-implementation.'),
]
