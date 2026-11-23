# In-depth sections added to pages by build.py: path -> (h2, prose html).
# Links use @/ like the rest of the site. Keep each section specific to its page.

DEEP = {}

DEEP['implementation/'] = ('What a well-run Business Central implementation looks like', '''
<p>Most Business Central projects don’t fail because of the software. They fail because of decisions that were made too late, data that was never cleaned, or a team that was never really involved. A good implementation partner spends as much time on those risks as on configuration.</p>
<h3>Decisions to make before configuration starts</h3>
<p>A handful of early design choices shape everything that follows, and they are expensive to change after go-live:</p>
<ul>
<li><strong>Chart of accounts and dimensions.</strong> Which reporting lives in the account number and which lives in dimensions such as department, location or channel. Getting this right is what makes Power BI and financial reports simple later.</li>
<li><strong>Posting groups.</strong> How customers, vendors and items post to the general ledger. Most “the numbers don’t match” problems trace back here.</li>
<li><strong>Inventory costing method.</strong> FIFO, average or standard cost. It can’t be changed casually once items have transactions.</li>
<li><strong>Warehouse setup per location.</strong> Simple shipping from a single location, bins, or full directed put-away and pick. More control means more steps for the warehouse team.</li>
<li><strong>Number series and document flow.</strong> Quote to order to shipment to invoice, and who approves what along the way.</li>
</ul>
<h3>Who you need on your side</h3>
<p>Business Central is implemented with your team, not for it. You need a <strong>project owner</strong> who can make decisions within a day or two, and a <strong>key user</strong> for each area: finance, sales, purchasing and warehouse. Key users join the workshops, test their own processes and train their colleagues. Budget around a day a week from each of them during the build and testing phases, and more in the final weeks before go-live.</p>
<h3>Testing that actually finds problems</h3>
<p>Testing a few screens is not enough. Before go-live your team should run complete business scenarios end to end: a customer order from quote to cash, a purchase from requisition to vendor payment, a stock count, a return, and a month-end close. Each scenario uses migrated data, not demo data, so data problems surface while there is still time to fix them.</p>
<h3>Cutover and the first month</h3>
<p>Go-live is usually timed for the start of a month. The final data load happens over a weekend: closing balances, open documents and a physical stock count. The first two weeks are the most intensive; we stay close to the team while they post real transactions, then support the first month-end close in Business Central. After that, the project moves into ongoing <a href="@/support/">support</a> at whatever level you need.</p>
<h3>Signs a partner is a good fit</h3>
<ul>
<li>They ask about your processes before they talk about features.</li>
<li>They tell you which requests to handle with standard features instead of custom code.</li>
<li>They put scope, assumptions and exclusions in writing.</li>
<li>The person who scopes the project is involved in delivering it.</li>
</ul>
''')

DEEP['business-central/'] = ('How Business Central works day to day', '''
<p>Microsoft Dynamics 365 Business Central is a cloud ERP for small and midsize companies. It replaces separate accounting, inventory and order systems with one database, so a sales order, the stock it reserves, the shipment and the invoice are all the same record moving through stages.</p>
<h3>Who Business Central is built for</h3>
<p>It typically suits companies with roughly 10 to a few hundred employees, from distributors and manufacturers to professional services firms. Companies usually move to it from QuickBooks, Sage or older Microsoft products such as Dynamics GP and Dynamics NAV, when spreadsheets and disconnected tools start costing more than they save.</p>
<h3>Role centers instead of menus</h3>
<p>Each user opens Business Central to a role center: a home page built for their job. An accountant sees cash, receivables and payables; a warehouse manager sees open picks and shipments; a buyer sees items below their reorder point. Every number can be drilled into to see the entries behind it.</p>
<h3>Microsoft 365 built in</h3>
<p>Business Central is designed to work with the tools most companies already use. Sales staff can work with customers and quotes from Outlook, finance can open almost any list in Excel and publish changes back, and colleagues can share a live record in a Teams conversation. Reports can be built in Power BI on live data.</p>
<h3>Updates without upgrade projects</h3>
<p>In the cloud version, Microsoft releases two major updates a year plus monthly updates. Custom features are built as extensions that sit beside Microsoft’s code rather than changing it, which is why updates no longer mean the costly upgrade projects that older ERPs required.</p>
<h3>Essentials or Premium?</h3>
<p>Essentials covers finance, sales, purchasing, inventory, warehousing and projects. Premium adds manufacturing and service management. Light users who mainly view data and approve documents can use the low-cost Team Members license. See <a href="@/licensing/">Essentials vs Premium pricing</a> for current prices and a calculator.</p>
<h3>Where it reaches its limits</h3>
<p>Very high-volume warehouses, complex multi-site manufacturing, or global groups with heavy consolidation needs may be better served by Dynamics 365 Supply Chain Management, Finance, or a specialist add-on. An honest partner will tell you which side of that line you are on before you commit.</p>
''')

DEEP['licensing/'] = ('How to choose the right Business Central licenses', '''
<p>Licensing mistakes are usually small but recurring: paying for full users who only look at data, or choosing Essentials and discovering later that you need manufacturing. A short review before you buy avoids both.</p>
<h3>Full users or Team Members?</h3>
<p>Anyone who creates and posts transactions, such as sales orders, purchase orders, invoices, journals or warehouse documents, needs a full user license. People who mostly look things up, approve documents, update simple records or fill in time sheets can usually use a Team Members license at a fraction of the price. In a typical distributor, roughly half the people who touch the system qualify as Team Members.</p>
<h3>When you need Premium</h3>
<ul>
<li><strong>Manufacturing:</strong> production orders, routings, work and machine centers, and capacity planning.</li>
<li><strong>Service management:</strong> service orders, service items, contracts and dispatching.</li>
</ul>
<p>Assembly orders for simple kitting are available in Essentials. All full users in the same environment must be on the same plan, so if one person needs Premium features, every full user moves to Premium.</p>
<h3>Other costs to plan for</h3>
<ul>
<li><strong>Additional environments and storage</strong> if you need more sandboxes or a large database.</li>
<li><strong>AppSource apps</strong> for EDI, shipping, scanning or sales tax, priced monthly by their publishers.</li>
<li><strong>Power BI Pro</strong> licenses for people who build or share reports, if your Microsoft 365 plan doesn’t include them.</li>
</ul>
<h3>Monthly or annual commitment</h3>
<p>Microsoft’s list prices assume an annual commitment billed monthly. Your licensing partner can explain the commitment terms and how adding or removing users works during the year. Plan to review your license mix after the first few months live, once you know who actually uses what.</p>
''')

DEEP['support/'] = ('What good Business Central support covers', '''
<p>After go-live, most of the value from Business Central comes from small improvements: a report that saves an hour each week, an approval that stops a recurring mistake, a setup change that makes month-end shorter. Good support makes those happen, not just fixes errors.</p>
<h3>Typical support requests</h3>
<ul>
<li>A document won’t post, or a posting went to the wrong account.</li>
<li>Inventory value doesn’t match the general ledger.</li>
<li>A new employee, location, warehouse process or product line needs setting up.</li>
<li>A report or Excel export needs changing for a new requirement.</li>
<li>An integration stopped syncing after a change in another system.</li>
<li>Preparing for Microsoft’s twice-yearly updates and new features.</li>
</ul>
<h3>Twice-yearly updates</h3>
<p>Microsoft publishes two major Business Central releases a year. Each one brings new features and occasionally changes how something works. Part of support is reviewing release notes, testing extensions in a sandbox before your production environment updates, and pointing out new features worth switching on.</p>
''')

DEEP['rescue/'] = ('Rescue: what to gather before your first call', '''
<p>A recovery moves faster when we can see the system and the history quickly. If you can, collect the following before the health check starts:</p>
<ul>
<li>Admin access to your Business Central environments (production and any sandboxes).</li>
<li>The original scope, solution design or statement of work, even if it’s out of date.</li>
<li>A list of installed extensions and apps, and who built each custom one.</li>
<li>Your top five problems in your team’s own words, with an example document for each.</li>
<li>The last two month-end close checklists or reconciliations.</li>
</ul>
<p>None of this has to be perfect. Missing documentation is common in rescue projects, and rebuilding it is part of the work.</p>
''')

DEEP['development/'] = ('How we decide whether something needs custom code', '''
<p>Every customization has a cost beyond the build: it must be tested with each Microsoft update, documented and maintained. Before writing code we work through a simple order of preference.</p>
<ol>
<li><strong>Standard setup.</strong> Many requests are solved by settings, workflows, approval rules, report layouts or personalization that already exist in Business Central.</li>
<li><strong>Power Platform.</strong> Notifications, approvals and simple automations often fit Power Automate without touching Business Central’s code.</li>
<li><strong>An AppSource app.</strong> For common needs such as EDI, shipping, scanning or sales tax, a maintained app from a specialist publisher is usually cheaper over time than custom code.</li>
<li><strong>A custom AL extension.</strong> For processes that are genuinely specific to your business and worth automating.</li>
</ol>
<h3>What a good extension project includes</h3>
<p>A short written specification you approve, a fixed price for that scope, development in a sandbox, testing with your real data, a deployment plan, and documentation your team can read. Source code should live in a repository your company controls, so future developers can pick it up.</p>
''')

DEEP['business-central-partner-tacoma/'] = ('Why work with a local Business Central consultant', '''
<p>Most of a Business Central project can be delivered remotely, and much of ours is. But a few moments are worth being in the same room for: the first discovery workshops, walking the warehouse floor to see how goods actually move, training sessions, and go-live day. A consultant based in Tacoma can be there for those without travel costs on your invoice.</p>
<h3>Puget Sound businesses we know well</h3>
<p>The region’s economy leans heavily on trade, logistics and manufacturing. Importers bringing goods through the Port of Tacoma and the Port of Seattle need landed costs on every container. Warehouses in the Kent Valley and Fife need accurate bins and fast picking. Manufacturers across Pierce and King counties need production planning and real product costs. Professional services firms in Seattle and Bellevue need project accounting and time tracking. Business Central handles all of these, and we tailor the setup to which one you are.</p>
<h3>Washington-specific setup</h3>
<p>Washington uses destination-based sales tax, so the rate depends on where goods are delivered. Business Central handles this with tax areas and jurisdictions, and companies shipping to many locations often connect a tax engine. Washington’s business and occupation (B&amp;O) tax is calculated on gross receipts, so we set up your chart of accounts and dimensions to make B&amp;O reporting by classification straightforward.</p>
''')

DEEP['about/'] = ('Why Q84 Digital exists', '''
<p>Many small and midsize companies end up with an ERP partner that is either too big to give them senior attention or too small to know supply chain well. Q84 Digital was set up to fill that gap: a senior consultant with deep Dynamics 365 and supply chain experience who stays with each client from the first conversation to everyday support.</p>
<p>We keep the client list deliberately small so every project gets that attention. If a project needs more hands, we bring in trusted specialists for specific pieces such as EDI or custom development, and we stay accountable for the result.</p>
''')

DEEP['integrations/'] = ('Planning an integration that keeps working', '''
<p>Most integration problems aren’t technical. They come from unclear ownership of data and no plan for what happens when something fails. Before building any connection we agree a few basics with you:</p>
<ul>
<li><strong>System of record:</strong> which system owns each piece of data, such as items, prices, customers, orders and stock.</li>
<li><strong>Timing:</strong> real time, every few minutes, or nightly, based on what the business actually needs.</li>
<li><strong>Error handling:</strong> where failed records go, who reviews them and how quickly.</li>
<li><strong>Monitoring:</strong> how you’ll know if a sync stops, before a customer notices.</li>
</ul>
<p>We then choose the simplest reliable option: Microsoft’s own connectors first, then proven AppSource apps, then custom API work for what’s left.</p>
''')

DEEP['migration/'] = ('Common data problems we find, and how we fix them', '''
<p>Almost every migration turns up the same kinds of data issues. Finding them in a trial load, rather than on go-live day, is the whole point of the process.</p>
<ul>
<li><strong>Duplicate customers and vendors</strong> created under slightly different names over the years. We match on tax IDs, addresses and emails, and you decide which record survives.</li>
<li><strong>Inconsistent units of measure</strong>, such as “EA”, “each” and “pcs” for the same thing. We standardize them before items load.</li>
<li><strong>Items without costs or with negative stock.</strong> These distort inventory value and must be corrected before opening balances are posted.</li>
<li><strong>Open documents that are really closed:</strong> invoices paid outside the system, or orders that will never ship.</li>
<li><strong>Balances that don’t tie out</strong> between subledgers and the general ledger. We reconcile these in the old system first, so you don’t carry the gap into Business Central.</li>
</ul>
''')

DEEP['migration/quickbooks/'] = ('Planning a QuickBooks to Business Central move', '''
<h3>QuickBooks Online vs QuickBooks Desktop</h3>
<p>The destination is the same, but the starting point differs. QuickBooks Online data is extracted through exports and its reports; QuickBooks Desktop data comes from exports and the company file’s reports, and older Desktop files often carry more years of inactive records. Either way, we work from reports you can reconcile against: the trial balance, A/R and A/P aging, and an inventory valuation if you track stock in QuickBooks.</p>
<h3>Things QuickBooks users notice first in Business Central</h3>
<ul>
<li><strong>Posting groups.</strong> Instead of choosing an account on every transaction, customers, vendors and items carry posting groups that decide the accounts automatically. This is what keeps the books consistent as volume grows.</li>
<li><strong>Documents, then posting.</strong> Orders and invoices are created, reviewed and then posted. Posted entries can’t be edited, only reversed, which gives you a real audit trail.</li>
<li><strong>Dimensions instead of classes.</strong> Department, location or channel tags work across every report and Power BI.</li>
<li><strong>Real inventory.</strong> Stock by location and bin, reservations against orders, and costs that flow to the general ledger.</li>
</ul>
<h3>A realistic timeline</h3>
<p>For a small distributor, the QuickBooks data migration typically runs over four to six weeks alongside the wider implementation, with two trial loads before the final cutover. Most companies go live at the start of a month so the opening balances line up with a clean period end. Keep QuickBooks available in read-only mode, or keep an export, so you can look up historical transactions after go-live.</p>
<h3>What to do in QuickBooks before you start</h3>
<ul>
<li>Make customers, vendors and items you no longer use inactive.</li>
<li>Reconcile bank accounts and clear old uncleared items.</li>
<li>Void or close invoices and bills that will never be paid.</li>
<li>Agree a cutover date with your accountant, ideally a month or quarter end.</li>
</ul>
''')

DEEP['migration/dynamics-gp/'] = ('Planning a Dynamics GP to Business Central migration', '''
<h3>Use Microsoft’s migration tools, but don’t stop there</h3>
<p>Business Central includes a cloud migration path built specifically for Dynamics GP. It brings over master data, open transactions and summary account history, and can add a read-only snapshot of detailed history. What it doesn’t do is redesign anything: GP’s account structure, item classes and posting setup come across largely as they were. A GP migration is the right moment to simplify, so we design the Business Central setup first and then map GP data into it.</p>
<h3>Account segments and dimensions</h3>
<p>GP stores department, location or division in account segments, which often leads to thousands of accounts. In Business Central, those segments usually become dimensions on a much shorter chart of accounts. The migration tools support this mapping, but the decision about which segments to keep as accounts and which become dimensions is a business decision to make early.</p>
<h3>Reports and add-ons</h3>
<p>Long-running GP systems typically carry dozens of SmartLists, Management Reporter reports and third-party add-ons. We list them all, find out which are still used, and replace only those: with standard Business Central lists and financial reports, Excel and Power BI, or an AppSource app. Many turn out to be unused.</p>
<h3>Timing your move</h3>
<p>Because Microsoft has announced an end date for GP support, many GP customers will move over the next few years, and experienced consultants will get busier. Starting the assessment early lets you pick a cutover at a fiscal year or quarter end that suits your business, rather than one forced by the support deadline.</p>
''')

DEEP['migration/dynamics-nav/'] = ('How NAV and Business Central differ', '''
<p>Business Central grew out of Dynamics NAV, so finance and operations users will recognize much of it: the same document flow, posting groups and journals. The bigger differences are underneath.</p>
<ul>
<li><strong>Cloud first.</strong> Business Central online is hosted and updated by Microsoft. No servers, SQL maintenance or upgrade projects every few years.</li>
<li><strong>Extensions instead of modified code.</strong> NAV customizations changed Microsoft’s code directly, which made every upgrade a project. Business Central customizations are extensions written in AL that sit beside the standard code.</li>
<li><strong>Web and mobile clients.</strong> Business Central runs in a browser and on phones and tablets, with no Windows client to install.</li>
<li><strong>Microsoft 365 integration</strong> with Outlook, Excel, Teams and Power BI.</li>
</ul>
<h3>Which NAV version you’re on matters</h3>
<p>Recent NAV versions can usually be upgraded with their data and setup, through a Business Central on-premises version and then Microsoft’s cloud migration. Older versions, or systems with heavy customization, often move faster and cleaner with a fresh implementation that brings over master data, open items and summary history. We recommend a path after looking at your version, objects and add-ons.</p>
<h3>Before you start</h3>
<p>List every customization and add-on, note which department relies on each one, and identify the reports people actually run. That list drives most of the cost and is the first thing we review in an assessment.</p>
''')

DEEP['migration/sage/'] = ('Planning a Sage to Business Central migration', '''
<h3>Sage 50 or Sage 100 makes a difference</h3>
<p><strong>Sage 50</strong> companies are usually moving because they’ve outgrown a small-business accounting system: they need proper inventory, more users, multiple locations or better reporting. The migration looks much like a <a href="@/migration/quickbooks/">QuickBooks move</a>: master data, open items and balances, with stock coming from a count.</p>
<p><strong>Sage 100</strong> companies often run a full ERP already, with sales orders, purchasing, inventory and sometimes bills of materials and work orders, on their own servers with add-ons. Their move is closer to an ERP replacement: each module is mapped to Business Central, add-ons are reviewed, and open orders are migrated as well as balances.</p>
<h3>How we get data out of Sage</h3>
<p>There’s no Microsoft migration tool for Sage, so we extract data through Sage’s own reports and exports and, where available, its database connection. Everything is staged in templates, cleaned, and loaded into a Business Central test company with configuration packages. Trial loads are reconciled against Sage’s trial balance and aging reports before the final cutover.</p>
<h3>Common differences to plan for</h3>
<ul>
<li><strong>Sub-accounts and departments</strong> in the Sage chart of accounts usually become dimensions.</li>
<li><strong>Price levels and customer-specific pricing</strong> move to Business Central price lists, which are more flexible.</li>
<li><strong>Costing methods</strong> must be confirmed per item before stock is loaded.</li>
<li><strong>Custom reports and Crystal reports</strong> are rebuilt only where people still use them.</li>
</ul>
''')

DEEP['migration/spreadsheets/'] = ('What changes when you stop running on spreadsheets', '''
<p>Moving off spreadsheets isn’t only a data load. It changes who owns each piece of information and how changes are controlled.</p>
<h3>One owner per record</h3>
<p>In Business Central, each item, customer, vendor and price has a single record. Instead of several people keeping their own copies, specific roles are allowed to create and change each type of record, and every change is logged. That alone removes most of the “which version is right?” arguments.</p>
<h3>Item data that works for everyone</h3>
<p>The item list is usually the hardest part. A clean item record needs a consistent number, a clear description, a base unit of measure plus purchase and sales units, a category, a costing method, and the posting group that sends it to the right accounts. Getting those right once means sales, purchasing, warehouse and finance all work from the same data.</p>
<h3>Excel stays, in a better role</h3>
<p>Your team doesn’t have to give up Excel. Business Central opens almost any list in Excel, and many lists can be edited there and published back. The difference is that Excel becomes a view of the real data rather than the place the data lives.</p>
<h3>Start small</h3>
<p>If the spreadsheets are very messy, it can help to go live with finance, customers, vendors and items first, and bring in warehouse bins and detailed pricing in a second phase once the basics are stable.</p>
''')

DEEP['industries/distribution/'] = ('Running a distribution business on Business Central', '''
<figure class="bc-shot"><img src="@/images/shot-purchase-orders.webp" alt="Business Central purchase orders list showing vendors, locations, status and amounts, with vendor details" width="1600" height="359" loading="lazy"><figcaption>Open and released purchase orders by vendor and location in Business Central. Example data from Microsoft’s demo company.</figcaption></figure>
<p>Distributors live on thin margins and fast turns. The system has to tell you what you have, where it is, what it really cost, and what to buy next, without anyone rebuilding a spreadsheet.</p>
<h3>Inventory you can trust</h3>
<p>Business Central tracks stock by location and, where you use them, by bin. Every receipt, shipment, transfer and adjustment is a posted entry, so you can see exactly why a quantity changed. Cycle counting lets you count a few items or bins each day instead of shutting down for an annual count, and variances post straight to the general ledger.</p>
<h3>Purchasing driven by demand</h3>
<p>Each item can carry a reorder point, a safety stock, a lead time and a preferred vendor. The requisition worksheet looks at stock on hand, open sales orders and open purchase orders, then suggests what to order and when. Buyers review the suggestions and turn them into purchase orders in a few clicks, instead of guessing from memory.</p>
<h3>Landed cost and true margin</h3>
<p>For importers and anyone paying freight, duty or brokerage, item charges assign those costs to the items they belong to, by quantity, weight, volume or value. The item’s cost, and therefore your margin, then reflects what the goods actually cost to land in your warehouse.</p>
<h3>Picking and shipping</h3>
<p>Warehouse setup scales with your operation. A small team can ship straight from the sales order. A busier warehouse uses warehouse shipments and pick documents grouped by bin. High-volume operations add directed put-away and pick, and handheld scanning with a warehouse app such as <a href="@/integrations/warehouse-insight/">Warehouse Insight</a>.</p>
<h3>Customer-specific pricing</h3>
<p>Price lists handle customer-specific prices, price groups, quantity breaks and date ranges, and line discounts can be set by customer and item group. Sales staff see the right price as they enter the order, with stock availability and the customer’s credit limit checked on the same screen.</p>
<h3>Selling online and through EDI</h3>
<p>Many distributors sell through several channels at once: sales reps, a web store and large retail customers on EDI. Business Central can take orders from <a href="@/integrations/shopify/">Shopify</a> and <a href="@/integrations/edi/">EDI trading partners</a> into the same order flow, so stock and margin are always measured across all channels.</p>
''')

DEEP['industries/manufacturing/'] = ('Choosing the right manufacturing setup', '''
<figure class="bc-shot"><img src="@/images/shot-production-order.webp" alt="Business Central released production order for 700 ATHENS desks, showing quantity, dates, unit cost and cost amount" width="1600" height="918" loading="lazy"><figcaption>A released production order in Business Central, with planned quantity, schedule and cost. Example data from Microsoft’s demo company.</figcaption></figure>
<p>Not every manufacturer needs every feature. Business Central offers a range, and starting with the simplest setup that fits usually gives the fastest return.</p>
<ul>
<li><strong>Assembly orders</strong> (Essentials) suit kitting and light assembly: combine components into a finished item without routings or capacity planning.</li>
<li><strong>Production orders with BOMs</strong> (Premium) track material consumption and output for real production runs.</li>
<li><strong>Routings and work centers</strong> add labor and machine time, so costs include conversion and you can see load on each work center.</li>
<li><strong>Planning worksheets</strong> pull it together, suggesting what to make and buy from demand, stock and lead times.</li>
</ul>
<p>Many companies start with BOMs and production orders, then add routings once the shop floor is used to recording output.</p>
''')

DEEP['industries/ecommerce/'] = ('What e-commerce brands get from moving to an ERP', '''
<figure class="bc-shot bc-shot-narrow"><img src="@/images/shot-item-card.webp" alt="Business Central item card for a yellow guest chair with product picture, inventory, unit cost and a Draft with Copilot button for marketing text" width="1600" height="1785" loading="lazy"><figcaption>An item card with product picture, stock and cost, plus Copilot-drafted marketing text for your web store. Example data from Microsoft’s demo company.</figcaption></figure>
<p>Most online brands start with their store platform plus accounting software, and add tools as they grow: an inventory app, a shipping tool, spreadsheets for purchasing. Somewhere past a few thousand orders a month, the gaps between those tools become the biggest cost in the business.</p>
<h3>One stock position across every channel</h3>
<p>Business Central becomes the single place that knows what’s in each warehouse or 3PL and what’s already promised to open orders. It tells each channel what is available to sell, so a busy weekend on one channel doesn’t oversell stock another channel already sold.</p>
<h3>Purchasing for seasonal demand</h3>
<p>Online sales are often seasonal and promotion-driven. Reorder points, lead times and the planning worksheet help buyers order ahead of peaks rather than reacting to stockouts, using actual sales history from every channel rather than one platform’s report.</p>
<h3>Reconciling payouts</h3>
<p>Marketplace and payment payouts net together sales, refunds, fees and reserves. Bringing those transactions into Business Central with the orders lets finance match each payout to the bank and post fees to the right accounts, instead of reconciling in a spreadsheet each week.</p>
<h3>Returns that update stock and finance together</h3>
<p>Return orders receive goods back into stock (or into a quarantine location), credit the customer and adjust revenue and cost in one flow. You can see return rates by product and channel, which often explains margin problems that sales reports hide.</p>
<h3>Bundles, kits and B2B</h3>
<p>Bundles can be sold as one product and shipped as their components using assembly items. Brands that also sell wholesale can run B2B orders with customer price lists and payment terms in the same system as their online sales.</p>
''')

DEEP['integrations/shopify/'] = ('Setting up the Shopify connector well', '''
<h3>Decisions to make first</h3>
<ul>
<li><strong>Which locations feed Shopify stock.</strong> You may not want every warehouse, or stock reserved for wholesale customers, to show as available online.</li>
<li><strong>How orders import.</strong> Automatically as sales orders, as invoices for prepaid orders, or into a review step first.</li>
<li><strong>Customer handling.</strong> One generic web customer or a Business Central customer per buyer. Individual customers give better reporting; a generic customer keeps the customer list small.</li>
<li><strong>Taxes and shipping charges.</strong> How Shopify’s tax and shipping lines map to Business Central accounts.</li>
</ul>
<h3>Payouts and fees</h3>
<p>Shopify payouts combine sales, refunds and fees. Importing payout transactions lets finance match each payout to the bank deposit and post fees to their own account, so gross sales and fees are visible separately.</p>
<h3>Living with it day to day</h3>
<p>Once set up, the connector runs on a schedule. The daily routine is short: check the exceptions list for orders that couldn’t be created, usually because of a new product or an unusual address, and fix them at the source so they don’t repeat.</p>
''')

DEEP['integrations/edi/'] = ('What an EDI setup involves', '''
<h3>Choosing an EDI provider</h3>
<p>Most small and midsize companies use an EDI provider rather than building EDI themselves. The provider connects to your trading partners, translates their documents, keeps up with each retailer’s rules and supplies a connector app for Business Central. When comparing providers, ask whether they already work with your trading partners, how they price per partner and per document, and how their Business Central connector handles errors.</p>
<h3>Trading partner requirements</h3>
<p>Each retailer publishes its own EDI guide: which documents it requires, the fields it expects, how ship notices must describe cartons and pallets, and which label formats it accepts. These guides drive the setup. Missing a requirement usually shows up as a chargeback rather than an error message, so we go through them line by line before go-live.</p>
<h3>Item and customer cross-references</h3>
<p>Retailers order using their own item numbers, UPCs and store or distribution center codes. Business Central’s item references and ship-to addresses map those to your items and locations, so incoming orders land on the right products and the right destination without manual lookups.</p>
<h3>Carton and pallet labels</h3>
<p>Many retailers require GS1-128 shipping labels with a serial shipping container code (SSCC) that matches the ship notice. That means capturing which items went into which carton during packing, which is usually done with a warehouse scanning app or a small extension.</p>
<h3>Costs to expect</h3>
<p>EDI costs usually include a one-time setup fee per trading partner, a monthly subscription, and sometimes per-document or per-kilocharacter charges from the provider. Implementation work on the Business Central side is quoted separately.</p>
''')

DEEP['integrations/power-bi/'] = ('Building a Business Central reporting setup that lasts', '''
<h3>Start with five numbers</h3>
<p>The most useful reporting projects start small. Ask the leadership team which five numbers they look at every week, how they want them sliced and how often they need them. Build those first, get them trusted, then expand. A dashboard with forty charts that nobody trusts is worse than five numbers everyone believes.</p>
<h3>Where reports should live</h3>
<ul>
<li><strong>Business Central pages and lists</strong> for operational, always-current views such as open orders, stock or overdue invoices.</li>
<li><strong>Excel</strong> for ad hoc analysis, using Business Central’s built-in Excel views and financial reports.</li>
<li><strong>Power BI</strong> for trends, comparisons across companies or periods, and dashboards for leadership.</li>
</ul>
<h3>Data refresh and access</h3>
<p>Power BI reports usually refresh on a schedule, several times a day. Access is controlled in Power BI by workspace and report, and can follow Business Central permissions where needed. People who build or share reports typically need a Power BI Pro license, which some Microsoft 365 plans include.</p>
<h3>Keeping definitions consistent</h3>
<p>Agree one definition for each key measure, such as revenue (gross or net of returns), margin (with or without landed cost and freight) and on-time delivery. Write them down and build them once in the data model, so every report uses the same numbers.</p>
''')

DEEP['integrations/warehouse-mobile/'] = ('Rolling out scanning in your warehouse', '''
<h3>Barcodes first</h3>
<p>Scanning only works if what you scan is labeled. Check which items already carry supplier barcodes (UPC or EAN), which need your own labels, and whether pallets, cartons and bins need labels too. Business Central item references store supplier barcodes against your items and units of measure, so a scan of a case barcode adds the right quantity.</p>
<h3>Choosing devices</h3>
<p>Rugged Android handhelds with built-in scanners are the most common choice: they survive drops, scan quickly at a distance and last a full shift. Phones with camera scanning can work for low volumes. Test devices against your chosen app and your Wi-Fi before buying a fleet, and check coverage in every aisle, including cold rooms and mezzanines.</p>
<h3>Rolling out in stages</h3>
<p>Start with one process, usually receiving or picking, in one area of the warehouse. Run it for a couple of weeks, fix what’s awkward, then add the next process. Staff accept scanning faster when it makes their day easier from the start rather than arriving everywhere at once.</p>
''')

DEEP['guides/implementation-cost/'] = ('Budgeting beyond year one', '''
<h3>Year one vs the years after</h3>
<p>The first year carries the one-time implementation, data migration and integration costs on top of licenses. From year two, the budget is mostly licenses, app subscriptions and support. When comparing Business Central with other systems, compare three to five years of total cost rather than the first invoice.</p>
<h3>Hidden costs to ask about</h3>
<ul>
<li><strong>Your team’s time.</strong> Key users spend real hours in workshops, testing and training. Plan for backfill in busy periods.</li>
<li><strong>Data cleanup.</strong> If the data is in poor shape, someone has to clean it, either your team or the consultant.</li>
<li><strong>Reports.</strong> Custom invoice, packing slip and label layouts are often forgotten in early estimates.</li>
<li><strong>Hardware.</strong> Scanners, label printers and Wi-Fi upgrades for warehouse scanning.</li>
<li><strong>Change orders.</strong> Requirements added after the scope is signed.</li>
</ul>
<h3>Fixed price or time and materials?</h3>
<p>A fixed price after discovery gives budget certainty for a clearly defined scope, and is the norm for well-scoped small and midsize projects. Time and materials suits work where the scope genuinely can’t be known yet, such as a rescue or a complex integration. Many projects combine both: fixed price for the core implementation, time and materials for later improvements.</p>
<h3>Questions to ask any implementation partner</h3>
<ul>
<li>What exactly is included, and what is excluded?</li>
<li>How many trial data loads are included?</li>
<li>Who on their team will do the work, and how senior are they?</li>
<li>How are changes to scope priced and approved?</li>
<li>What support is included after go-live, and for how long?</li>
</ul>
''')

DEEP['guides/implementation-timeline/'] = ('Example timeline: a 20-person distributor', '''
<p>Here’s how a standard project typically unfolds for a distributor moving from QuickBooks to Business Central with warehouse processes and one Shopify integration. Every project is different, but the shape is common.</p>
<table>
<thead><tr><th>Weeks</th><th>What happens</th></tr></thead>
<tbody>
<tr><td>1–3</td><td>Discovery workshops for finance, sales, purchasing and warehouse. Data extracts start.</td></tr>
<tr><td>4–5</td><td>Solution design signed off: chart of accounts, dimensions, posting groups, warehouse setup, integration design.</td></tr>
<tr><td>6–11</td><td>Configuration, Shopify connector setup, document layouts, first trial data load.</td></tr>
<tr><td>12–15</td><td>End-to-end testing by key users with migrated data, second trial load, training.</td></tr>
<tr><td>16</td><td>Go-live at a month start: final data load and physical count over a weekend.</td></tr>
<tr><td>17–20</td><td>Hands-on support and the first month-end close in Business Central.</td></tr>
</tbody>
</table>
<h3>What shortens a project</h3>
<ul>
<li>Clean data and inactive records removed before the project starts.</li>
<li>A decision-maker available for quick answers.</li>
<li>Accepting standard Business Central processes where they work.</li>
<li>Phasing: going live with the core first and adding extras later.</li>
</ul>
<h3>What usually needs more time</h3>
<ul>
<li>Manufacturing with routings and capacity planning.</li>
<li>Several companies with inter-company transactions and consolidation.</li>
<li>EDI with large retailers, because each trading partner tests and certifies separately.</li>
<li>Heavily customized source systems, such as older Dynamics NAV.</li>
</ul>
<h3>How to keep your project on schedule</h3>
<p>Agree the go-live date at the start and work backwards. Book key users’ time for testing weeks in advance. Hold a short weekly status meeting with an open-issues list, and make sure every issue has an owner and a date. Most delays come from questions waiting for answers, not from the work itself.</p>
''')

DEEP['guides/erp-readiness-checklist/'] = ('How to run an ERP readiness review with your team', '''
<p>The checklist works best as a team exercise rather than something one person fills in alone. A simple way to run it:</p>
<ol>
<li><strong>Assign sections.</strong> Give each area of the checklist to the person who runs it: finance, sales, purchasing, warehouse, IT.</li>
<li><strong>Answer honestly.</strong> Mark each question Yes, Partly or No. “Partly” is the most useful answer; it shows where decisions are still open.</li>
<li><strong>Meet for an hour.</strong> Go through the No and Partly answers together and agree an owner for each.</li>
<li><strong>Pick your top five.</strong> Write down the five questions that matter most to your business and bring them to your first conversation with any ERP partner.</li>
</ol>
<p>Teams that do this before talking to vendors get better proposals, because partners can quote against real requirements instead of guesses. It also surfaces disagreements inside the business early, when they’re cheap to resolve.</p>
''')

DEEP['compare/netsuite/'] = ('Questions to settle before choosing between Business Central and NetSuite', '''
<h3>How many entities, and where?</h3>
<p>For one company or a few US entities, both systems handle consolidation well. For many subsidiaries across countries and currencies, look closely at how each handles inter-company transactions, local tax and statutory reporting, and whether your partner has done it before.</p>
<h3>How much of the day happens in Microsoft 365?</h3>
<p>If your team lives in Outlook, Excel and Teams, Business Central’s built-in integration saves time every day. If you use Google Workspace or other tools, that advantage matters less.</p>
<h3>Who will support you after go-live?</h3>
<p>Ask both vendors who handles day-to-day support, what it costs, and how quickly typical requests are resolved. The quality of your support partner often matters more to long-term satisfaction than the product itself.</p>
<h3>What does the five-year cost look like?</h3>
<p>Ask for a five-year view that includes licenses, renewals, apps, implementation and support for the same scope. Year-one quotes can look similar while year-five costs differ a lot.</p>
<h3>Can you see your own processes in a demo?</h3>
<p>Ask each vendor to demo three of your real processes, such as a customer order with a backorder, a purchase with landed cost, and month-end, rather than a standard script. How each system handles your actual work is the best comparison you can get.</p>
''')

DEEP['compare/sage-intacct/'] = ('Questions to settle before choosing between Business Central and Sage Intacct', '''
<h3>Which teams must the system serve?</h3>
<p>List every team that will use the new system daily. If it’s mainly finance and leadership, a finance-first system can be the cleaner choice. If purchasing, warehouse, production or project teams also need it, a full ERP avoids building and maintaining integrations between separate tools.</p>
<h3>How do you report today, and how do you want to?</h3>
<p>Both systems support dimensional reporting. Write down the reports your CFO and board actually use and ask each vendor to show how they’re produced, including how much setup they need and whether they can be changed without a consultant.</p>
<h3>What will you integrate?</h3>
<p>Count the systems that would need to connect: CRM, e-commerce, warehouse, payroll, banking. Each integration has a build cost and an upkeep cost. A system that covers more of the business natively needs fewer of them.</p>
<h3>Five-year cost for the same scope</h3>
<p>Compare licenses, implementation, integrations and support over five years, for the same users and processes. A finance-first system plus separate operational tools can cost more in total than one ERP, or less, depending on how much of your business is operational.</p>
<h3>Growth over the next five years</h3>
<p>Consider where the business is heading. Adding inventory, a warehouse or light manufacturing later is straightforward in a full ERP; in a finance-first system it usually means adding and integrating another product.</p>
''')

DEEP['compare/odoo/'] = ('Questions to settle before choosing between Business Central and Odoo', '''
<h3>How important are accounting controls?</h3>
<p>If you have outside investors, a lender or an annual audit, ask your accountant or auditor which system they’re comfortable with. Posting controls, audit trails and standard US financial reporting matter more as the company grows.</p>
<h3>Who will implement and support it locally?</h3>
<p>Both products are implemented through partners. Check how many experienced partners work in your area and industry, how long they’ve been doing it, and what happens if your partner moves on.</p>
<h3>How much will you customize?</h3>
<p>Odoo’s flexibility is a strength, but heavy customization means more work at every major version upgrade. Business Central’s extension model is more constrained but designed to survive Microsoft’s twice-yearly updates. Estimate how much custom work you’ll really need and who will maintain it.</p>
<h3>What will you use beyond ERP?</h3>
<p>If you want website, point of sale, CRM and helpdesk in one suite, Odoo covers more ground natively. If you already use Microsoft 365, Dynamics 365 Sales or other best-of-breed tools, Business Central fits into that landscape more naturally.</p>
<h3>Total cost over five years</h3>
<p>Compare licenses or subscriptions, hosting, implementation, custom development and upgrades over five years for the same scope. Lower license costs can be offset by more custom work, or not, depending on your requirements.</p>
''')

DEEP['guides/'] = ('How to use these guides', '''
<p>These guides are written for owners, CFOs and operations leaders at small and midsize companies who are considering Microsoft Dynamics 365 Business Central, or already use it and want to get more from it. Each one answers a question we hear in almost every first conversation.</p>
<ul>
<li><strong>Just starting to look?</strong> Begin with the <a href="@/guides/erp-readiness-checklist/">ERP readiness checklist</a> to get your team aligned, then read <a href="@/business-central/">what Business Central does</a>.</li>
<li><strong>Comparing systems?</strong> Our comparisons with <a href="@/compare/netsuite/">NetSuite</a>, <a href="@/compare/sage-intacct/">Sage Intacct</a> and <a href="@/compare/odoo/">Odoo</a> explain where each one fits better.</li>
<li><strong>Building a budget?</strong> The <a href="@/guides/implementation-cost/">cost guide</a>, <a href="@/guides/implementation-timeline/">timeline guide</a> and <a href="@/licensing/#calculator">license calculator</a> give you realistic numbers to plan with.</li>
<li><strong>Replacing an older system?</strong> See our <a href="@/migration/">migration guides</a> for QuickBooks, Dynamics GP, Dynamics NAV, Sage and spreadsheets.</li>
</ul>
<p>All guides are free and need no email address. They’re written by <a href="@/about/">our senior consultants</a> and updated when Microsoft’s products or prices change.</p>
''')

DEEP['blog/'] = ('What we write about', '''
<p>The Q84 Digital blog covers the practical side of running a growing business on Microsoft Dynamics 365 Business Central: choosing an ERP, moving off QuickBooks and older systems, inventory and warehouse operations, and getting more from Business Central once you’re live. Articles draw on <a href="@/about/">our team’s</a> more than 15 years of Microsoft Dynamics and supply chain work.</p>
<p>Looking for something more structured? Our <a href="@/guides/">guides</a> cover implementation cost and timeline, honest comparisons with NetSuite, Sage Intacct and Odoo, and a free ERP readiness checklist.</p>
''')

# Second round: more depth appended to the same in-depth sections
MORE = {}

MORE['blog/'] = '''<h3>Topics we cover</h3>
<ul>
<li><strong>ERP selection:</strong> when to move off entry-level accounting, how to compare systems and how to run a fair evaluation.</li>
<li><strong>Migration:</strong> moving from QuickBooks, Sage, Dynamics GP, Dynamics NAV and spreadsheets without losing control of your numbers.</li>
<li><strong>Inventory and warehouse:</strong> costing, replenishment, landed cost, bins, picking and scanning.</li>
<li><strong>Getting more from Business Central:</strong> reporting, automation, Microsoft’s twice-yearly updates and features worth switching on.</li>
</ul>'''

MORE['business-central/'] = '''<h3>What it connects to</h3>
<p>Business Central has a built-in Shopify connector, standard integration with Dynamics 365 Sales through Dataverse, and open APIs for other systems. Thousands of apps on Microsoft AppSource add specialist features such as EDI, shipping, sales tax, scanning and payroll connections. See <a href="@/integrations/">integrations</a> for the most common ones.</p>'''

MORE['compare/netsuite/'] = '''<h3>Migration and switching costs</h3>
<p>Whichever system you choose, plan the move from your current one carefully. The data migration, the processes your team has to relearn and the integrations you rebuild usually cost more than the difference in license prices. Choosing the system your team can adopt quickly, with a partner who has done your kind of migration before, matters more than small differences in features.</p>
<h3>The honest summary</h3>
<p>For a US company with one or a few entities, inventory to manage and a team that works in Microsoft 365, Business Central is usually the more cost-effective choice. For a fast-growing company with many international subsidiaries that wants one vendor for software and services, NetSuite is often worth its higher price.</p>'''

MORE['compare/sage-intacct/'] = '''<h3>The honest summary</h3>
<p>For services, nonprofit or software companies with little inventory and a strong focus on multi-entity accounting, Sage Intacct is a strong, focused choice. For companies that buy, stock, make or ship physical goods, or expect to soon, Business Central covers operations and finance in one system and is usually the better long-term fit.</p>
<p>Whichever you lean towards, ask for a demo of your own month-end and one operational process, and talk to a reference customer of a similar size in your industry.</p>'''

MORE['compare/odoo/'] = '''<h3>The honest summary</h3>
<p>For very small companies on a tight budget, or businesses that want one suite for website, point of sale and operations, Odoo can be a good fit, especially with in-house technical skills. For growing companies that need strong accounting controls, reliable upgrades, Microsoft 365 integration and a large US partner network, Business Central is usually the safer long-term choice.</p>
<p>Either way, insist on a demo of your own processes and a written scope before signing, and check how much custom development each proposal assumes.</p>'''

MORE['development/'] = '''<h3>Common extension requests</h3>
<ul>
<li>Extra fields on customers, items or orders, shown where your team needs them.</li>
<li>Custom document layouts: invoices, packing slips, pallet and shelf labels.</li>
<li>Validation rules that stop common mistakes before a document posts.</li>
<li>Automated jobs, such as nightly price updates or stock exports to a partner.</li>
<li>API endpoints for an integration that has no ready-made connector.</li>
</ul>'''

MORE['guides/erp-readiness-checklist/'] = '''<h3>Who should fill in each section</h3>
<p>Finance and reporting goes to your controller or bookkeeper. Inventory, purchasing and sales go to the people who run purchasing and order entry. Warehouse and fulfillment goes to your warehouse lead. Data, integrations and technology goes to whoever manages IT or your current systems. The owner or general manager should answer the goals, budget and timeline sections, because those are the decisions that shape everything else.</p>'''

MORE['guides/implementation-cost/'] = '''<h3>How to compare two quotes</h3>
<p>Implementation quotes are only comparable when the scope is the same. Line them up against the same list: modules, companies, locations, number of trial data loads, integrations, custom reports, training sessions and post-go-live support. A cheaper quote often leaves out items the other includes, which come back later as change orders.</p>'''

MORE['guides/implementation-timeline/'] = '''<h3>Phasing a larger project</h3>
<p>For bigger scopes, splitting the project into phases reduces risk and gets value sooner. A common pattern is:</p>
<ul>
<li><strong>Phase 1:</strong> finance, sales, purchasing and basic inventory for the main company.</li>
<li><strong>Phase 2:</strong> warehouse processes and scanning, once the basics are stable.</li>
<li><strong>Phase 3:</strong> integrations such as EDI or a web store, then additional companies or locations.</li>
</ul>
<p>Each phase has its own go-live and a few weeks of settling in before the next starts. The total time is a little longer than one big-bang project, but the risk on any single weekend is much lower and your team learns the system in stages.</p>
<h3>Questions to ask about any proposed timeline</h3>
<ul>
<li>How many hours a week does the plan assume from our key users?</li>
<li>When are the trial data loads, and who reconciles them?</li>
<li>What has to be true before go-live is approved?</li>
<li>What happens to the timeline if a decision takes a week instead of a day?</li>
</ul>'''

MORE['industries/distribution/'] = '''<h3>Reporting distributors rely on</h3>
<p>Margin by customer, item and salesperson; inventory turns and days on hand by location; slow-moving and dead stock; fill rate and backorders; and vendor performance on lead times. Most are available in Business Central and Excel from day one, and <a href="@/integrations/power-bi/">Power BI</a> adds trend dashboards for leadership.</p>'''

MORE['industries/ecommerce/'] = '''<h3>When to make the move</h3>
<p>Common triggers are a second sales channel or warehouse, a 3PL, wholesale customers alongside online sales, or finance spending days each month reconciling payouts. If two or more of those apply, an ERP usually pays for itself in time saved and stock mistakes avoided.</p>'''

MORE['integrations/'] = '''<h3>Integration or AppSource app?</h3>
<p>Before commissioning a custom integration, check Microsoft AppSource. Many common connections, including shipping carriers, EDI networks, sales tax engines, payment providers and marketplaces, already have maintained apps. A subscription to a proven app is usually cheaper over five years than building and maintaining the same connection yourself.</p>'''

MORE['integrations/edi/'] = '''<h3>Testing with trading partners</h3>
<p>Most large retailers require a test phase before they accept live documents. You exchange test purchase orders, ship notices and invoices, and the retailer checks each one against its rules. Plan a few weeks for this per trading partner, and start with the partner that matters most to your business.</p>'''

MORE['integrations/power-bi/'] = '''<h3>Common reports by role</h3>
<ul>
<li><strong>Owner or CEO:</strong> revenue, gross margin, cash and receivables trend, compared with last year and budget.</li>
<li><strong>Finance:</strong> aged receivables and payables, cash forecast, expenses by department, and month-end checks.</li>
<li><strong>Sales:</strong> sales by rep, customer and product line, open quotes, and customers buying less than last year.</li>
<li><strong>Operations:</strong> stock value and turns, stockouts, slow movers, on-time shipping and backorders.</li>
</ul>
<h3>Ready-made reports first</h3>
<p>Microsoft provides Power BI reports for Business Central covering finance, sales, purchasing, inventory, projects and manufacturing. Starting from these and adjusting them is usually much faster than building from scratch, and they keep up with Microsoft’s data model as Business Central updates.</p>'''

MORE['integrations/shopify/'] = '''<h3>Multiple stores and markets</h3>
<p>Brands with separate stores for different countries, brands or wholesale can connect each store to the same Business Central company, each with its own settings for prices, stock locations and order handling. Stock and sales from every store then roll up into one set of books and one inventory position.</p>'''

MORE['integrations/warehouse-mobile/'] = '''<h3>Label printing</h3>
<p>Scanning usually goes hand in hand with label printing: item labels at receiving, bin labels for shelving, and shipping labels at packing. Business Central report layouts can print labels to standard label printers, and warehouse and shipping apps add carrier and compliance labels.</p>
<h3>Measuring the result</h3>
<p>Track a few numbers before and after rollout: picking errors, inventory accuracy from cycle counts, time from order release to shipment, and how many documents are still entered at a desk. These show whether scanning is paying off and where to focus next.</p>'''

MORE['migration/'] = '''<h3>Cutover weekend</h3>
<p>Final cutover usually happens over a weekend at a month or quarter end. The old system is closed for new transactions on Friday, final balances and open documents are extracted, a physical stock count is taken, and everything is loaded and reconciled in Business Central. Your finance lead signs off the numbers before trading starts on Monday.</p>'''

MORE['migration/dynamics-gp/'] = '''<h3>What GP users notice first in Business Central</h3>
<p>Business Central runs in a browser instead of a desktop client, uses posting groups to decide accounts automatically, and replaces GP batches with documents and journals that post directly. Finance teams usually adapt quickly; the bigger change is often for operations users, who get more inventory and warehouse capability than GP offered.</p>'''

MORE['migration/dynamics-nav/'] = '''<h3>On-premises or online?</h3>
<p>Business Central online removes servers, backups and upgrade projects, and is the right choice for most companies. On-premises Business Central still exists for specific needs, such as strict data residency or heavy local integrations, but it brings back the upgrade and hosting work that moving off NAV usually aims to remove.</p>'''

MORE['migration/sage/'] = '''<h3>Running Sage and Business Central in parallel</h3>
<p>Most companies don’t run both systems side by side for long; it doubles the data entry. Instead, Sage stays available for lookups after go-live, and the first Business Central month-end is reconciled closely against expected results. If your auditor or lender requires it, a parallel close for one period can be planned into the timeline.</p>'''

MORE['migration/spreadsheets/'] = '''<h3>Typical spreadsheets we replace</h3>
<ul>
<li><strong>Item and price lists</strong> become items, units of measure and price lists.</li>
<li><strong>Stock counts by location</strong> become inventory by location and bin, updated by every transaction.</li>
<li><strong>Purchase trackers</strong> become purchase orders with expected receipt dates.</li>
<li><strong>Order logs</strong> become sales orders linked to shipments and invoices.</li>
<li><strong>Customer lists with credit notes</strong> become customers with credit limits and payment terms.</li>
</ul>'''

for _k, _v in MORE.items():
    DEEP[_k] = (DEEP[_k][0], DEEP[_k][1] + _v)

# Third round: sized to each page's remaining gap
MORE2 = {}

MORE2['blog/'] = '''<h3>Start here</h3>
<p>New to ERP? Read <a href="@/blog/signs-you-have-outgrown-quickbooks/">seven signs your distribution business has outgrown QuickBooks</a>, then use the <a href="@/guides/erp-readiness-checklist/">ERP readiness checklist</a> to see where your team stands. If you already run Business Central and something isn’t working the way it should, our <a href="@/support/">support</a> and <a href="@/rescue/">rescue</a> pages explain how we can help.</p>'''

MORE2['business-central/'] = '''<p>Business Central is sold through Microsoft partners, who also implement and support it. Choosing a partner who knows your industry is as important as choosing the product.</p>'''

MORE2['compare/netsuite/'] = '''<p>If you’re still unsure, list your ten most important requirements and score both systems against them with your team, rather than relying on feature lists.</p>'''

MORE2['compare/sage-intacct/'] = '''<h3>A note on Sage’s other products</h3>
<p>Sage sells several different accounting and ERP products, including Sage 50, Sage 100, Sage 300 and Sage Intacct. They are separate systems rather than editions of one product, so moving between them is a new implementation, just like moving to Business Central. If you’re on Sage 50 or Sage 100 today, compare Sage Intacct and Business Central on equal terms: both mean new software, new processes and a data migration. See <a href="@/migration/sage/">moving from Sage to Business Central</a> for what that involves.</p>'''

MORE2['compare/odoo/'] = '''<h3>Hosting and data ownership</h3>
<p>Odoo can be hosted by Odoo itself, by a partner, or on your own servers, which gives flexibility but also means deciding who is responsible for backups, security and upgrades. Business Central online is hosted, backed up and updated by Microsoft in its cloud, so those responsibilities sit with Microsoft. In both cases, make sure your contract says you can export your data in full if you ever move to another system.</p>'''

MORE2['development/'] = '''<p>We also review extensions written by others before you rely on them, checking for risky code, missing tests and anything that might break with the next Microsoft update.</p>'''

MORE2['guides/erp-readiness-checklist/'] = '''<p>Once the checklist is done, keep it. It becomes a useful reference during discovery workshops and a reminder of what “done” should look like at go-live.</p>'''

MORE2['guides/implementation-cost/'] = '''<p>Finally, keep a contingency of around 10 to 15 percent for genuine surprises, such as a data problem nobody knew about or a new requirement from a key customer.</p>'''

MORE2['guides/implementation-timeline/'] = '''<h3>Timelines for migrations from older systems</h3>
<p>Where you’re coming from changes the shape of the project. Moves from <a href="@/migration/quickbooks/">QuickBooks</a> or <a href="@/migration/spreadsheets/">spreadsheets</a> spend more time on designing item data and inventory processes, because those didn’t really exist before. Moves from <a href="@/migration/dynamics-gp/">Dynamics GP</a> benefit from Microsoft’s migration tools but need time to rethink account segments and replace add-ons. Moves from <a href="@/migration/dynamics-nav/">Dynamics NAV</a> are often driven by how much custom code needs replacing.</p>
<h3>After go-live</h3>
<p>Plan for a settling-in period of one to three months after go-live. Users find faster ways of working, small setup changes are made, and reports are fine-tuned. Many companies then start a second phase for the features they deliberately left out of the first one.</p>'''

MORE2['industries/distribution/'] = '''<h3>Lot, serial and expiration tracking</h3>
<p>Distributors of food, chemicals, medical or electrical products often need to trace what went where. Business Central tracks lot and serial numbers from receipt to shipment, records expiration dates and can enforce first-expired, first-out picking, so a recall can be traced to the customers affected in minutes.</p>'''

MORE2['industries/ecommerce/'] = '''<h3>Working with a 3PL</h3>
<p>Many brands use a third-party logistics provider for some or all fulfillment. Business Central treats the 3PL as a location: stock is transferred to it, orders are sent to it for fulfillment, and shipment confirmations come back to post the shipment and invoice. The connection is usually made through EDI or the 3PL’s own API, and the 3PL’s stock reports are reconciled against Business Central regularly.</p>'''

MORE2['integrations/edi/'] = '''<h3>Before you start</h3>
<p>Gather each trading partner’s EDI guide, label specifications and vendor compliance manual, plus a list of the documents they require. Having these in hand on day one shortens the project considerably.</p>'''

MORE2['integrations/'] = '''<p>Every integration we build or set up comes with notes on how it works, where errors appear and who to contact when something changes.</p>'''

MORE2['integrations/power-bi/'] = '''<h3>Data quality comes first</h3>
<p>Reports only show what Business Central records. If salespeople aren’t assigned to customers, items have no categories, or transactions miss their department dimension, the reports will have gaps. Part of every reporting project is checking those basics and, where needed, making fields mandatory so the data stays clean from then on.</p>'''

MORE2['integrations/shopify/'] = '''<p>Before go-live we test the full flow with real products: orders, partial shipments, refunds, cancellations and a payout, so the first live weekend holds no surprises.</p>'''

MORE2['integrations/warehouse-mobile/'] = '''<h3>Training the warehouse team</h3>
<p>Warehouse staff learn scanning fastest on the floor, not in a meeting room. Short, hands-on sessions on real orders, a one-page guide for each process kept near the packing benches, and a named person to ask for the first few weeks make adoption much smoother. Expect a short dip in speed during the first week, followed by faster and more accurate work than before.</p>
<h3>Common mistakes to avoid</h3>
<ul>
<li>Buying devices before testing them with the chosen app.</li>
<li>Starting scanning before bins and item barcodes are set up and labeled.</li>
<li>Rolling out every process at once instead of one at a time.</li>
</ul>'''

MORE2['migration/dynamics-nav/'] = '''<p>Your NAV data, setup knowledge and process experience aren’t wasted. Most of it carries straight into Business Central; what changes is the technology underneath.</p>'''

MORE2['migration/'] = '''<p>Every migration ends with a signed reconciliation, so you know exactly which numbers came across and that they match.</p>'''

MORE2['migration/sage/'] = '''<h3>Before you start</h3>
<ul>
<li>Run and save your trial balance, A/R and A/P aging, and inventory valuation for the last closed month.</li>
<li>Make customers, vendors and items you no longer use inactive.</li>
<li>List the Sage add-ons, custom reports and integrations you rely on.</li>
<li>Agree a cutover date with your accountant, ideally a month or quarter end.</li>
</ul>
<p>With those in hand, the first trial load can usually happen within a few weeks of the project starting.</p>'''

MORE2['migration/spreadsheets/'] = '''<h3>Signs it’s time to move off spreadsheets</h3>
<ul>
<li>More than one person updates the same spreadsheet each day.</li>
<li>Stock levels in the spreadsheet regularly disagree with the shelf.</li>
<li>Orders, invoices or purchase orders are typed into more than one place.</li>
<li>Month-end depends on someone copying spreadsheet totals into the accounts.</li>
<li>Only one person really understands how the spreadsheets fit together.</li>
</ul>
<p>If two or more apply, the time spent maintaining spreadsheets is likely already more than an ERP would cost.</p>'''

for _k, _v in MORE2.items():
    DEEP[_k] = (DEEP[_k][0], DEEP[_k][1] + _v)

# Final top-up for pages still a little under their target length
MORE3 = {
'blog/': '''<p>New articles are added regularly. Each one links to the guides and service pages where you can go deeper.</p>''',
'compare/netsuite/': '''<p>Both are capable systems; the right one is the one that fits how your business runs.</p>''',
'compare/odoo/': '''<p>Whichever you choose, a clear scope and an experienced partner matter more than the logo on the login screen. Ask for references from companies of your size.</p>''',
'compare/sage-intacct/': '''<p>A short paid discovery with each shortlisted vendor, focused on your hardest processes, is often the best money you spend in the whole selection.</p>''',
'guides/erp-readiness-checklist/': '''<p>If you’d like help working through it, bring your answers to a free assessment and we’ll go through the gaps with you.</p>''',
'guides/implementation-cost/': '''<p>Revisit the budget at each phase gate, so surprises are caught early rather than at go-live.</p>''',
'guides/implementation-timeline/': '''<h3>A note on year-end</h3>
<p>Going live at the start of a fiscal year is tempting because it gives a clean break, but it lands on top of year-end close, audit preparation and tax filings. Many finance teams prefer a go-live a month or two into the new year, once the year-end work is done, with opening balances taken from the closed year. Discuss the timing with your accountant early.</p>''',
'industries/distribution/': '''<h3>Drop shipments and special orders</h3>
<p>For items you don’t stock, Business Central links the sales order to a purchase order so the vendor ships straight to your customer, or orders goods in specifically for one customer. Both keep margin and delivery visible on the original sales order.</p>''',
'industries/ecommerce/': '''<p>Getting the item and stock setup right in Business Central first makes every channel connection simpler afterwards.</p>''',
'integrations/edi/': '''<p>Keep a simple log of chargebacks by reason after go-live; it shows exactly where the EDI or warehouse process needs tightening.</p>''',
'integrations/power-bi/': '''<h3>Sharing reports safely</h3>
<p>Decide early who should see what. Leadership dashboards with margins and salaries shouldn’t be shared as widely as operational reports. Power BI workspaces and row-level security let you show each team only the data it needs, for example restricting sales reps to their own customers.</p>''',
'integrations/shopify/': '''<p>After go-live, review the connector settings when you add a new store, location, product type or payment method, since each can need a small configuration change.</p>''',
'integrations/warehouse-mobile/': '''<p>Once scanning is stable, cycle counting becomes quick enough to do daily, which is usually where inventory accuracy improves the most.</p>''',
'migration/dynamics-nav/': '''<p>We start every NAV project with a short assessment of your version, objects and add-ons, and give you a written recommendation on the path before any larger commitment.</p>''',
'migration/sage/': '''<h3>After go-live</h3>
<p>The first month-end in Business Central is the real test. We reconcile it with your finance team line by line against what Sage would have shown, and adjust any posting setup that doesn’t match how you report. From the second month, the close is usually faster than it was in Sage, because inventory, receivables and payables all post straight to the general ledger.</p>''',
'migration/spreadsheets/': '''<h3>After go-live</h3>
<p>Retire the old spreadsheets deliberately. Archive them read-only on go-live day so nobody keeps updating them by habit, and point every team to the Business Central list or Excel view that replaces each one. In the first weeks, the most common question is “where do I find what I used to look up in the spreadsheet?”, so a short list mapping old files to new screens saves a lot of time.</p>''',
}
for _k, _v in MORE3.items():
    DEEP[_k] = (DEEP[_k][0], DEEP[_k][1] + _v)

DEEP['industries/professional-services/'] = ('Projects in Business Central', '''
<figure class="bc-shot"><img src="@/images/shot-projects.webp" alt="Business Central projects list with project details showing work in progress and budget cost by resource and item" width="1600" height="448" loading="lazy"><figcaption>Projects with budget cost by resource and item, and work-in-progress figures, in Business Central. Example data from Microsoft’s demo company.</figcaption></figure>
<p>Each project carries its own budget, actual cost and billable price, split by resources (people), items and expenses. Project managers see at a glance how much of the budget is used and how much is ready to invoice, and finance posts work in progress at month-end so revenue and cost land in the right period.</p>
''')

DEEP['integrations/warehouse-insight/'] = ('Getting your warehouse ready for Warehouse Insight', '''
<p>A mobile warehouse app works best when the basics in Business Central are already right. Before rollout we check four things:</p>
<ul>
<li><strong>Bins that match the floor.</strong> Every rack position has a bin code in Business Central and a label on the shelf.</li>
<li><strong>Barcodes on items.</strong> Supplier barcodes are recorded as item references, and items without one get your own labels.</li>
<li><strong>Warehouse documents per location.</strong> Receipts, put-aways, picks and shipments are switched on for the locations that will use scanning.</li>
<li><strong>Wi-Fi in every aisle.</strong> Coverage is tested with the actual devices, including cold rooms, mezzanines and the loading dock.</li>
</ul>
<p>We then roll out one process at a time, usually receiving or picking first, and add counting, moves and license plates once the team is comfortable.</p>
''')

# The separate warehouse mobile page was removed; its rollout advice now lives on the Warehouse Insight page
_WM = 'integrations/warehouse-mobile/'
DEEP['integrations/warehouse-insight/'] = (DEEP['integrations/warehouse-insight/'][0], DEEP['integrations/warehouse-insight/'][1] + MORE[_WM] + MORE2[_WM])
DEEP.pop(_WM, None)
