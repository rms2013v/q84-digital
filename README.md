# Q84 Digital website

Static marketing site for Q84 Digital, hosted on GitHub Pages. Each page has its own URL, title, description and canonical link.

## Editing

Page content lives in `src/build.py`; settings live in `src/site.json`. After any change, rebuild and push:

```
python3 src/build.py
git add -A && git commit -m "Update site" && git push
```

## Settings in `src/site.json`

| Setting | What it does |
|---|---|
| `email` | Contact email shown on the site and used by the form fallback. **Replace the placeholder before launch.** |
| `form_endpoint` | Form service URL (for example Formspree `https://formspree.io/f/xxxx`). Empty = the form opens the visitor's email app instead. |
| `booking_url` | Calendar link (Calendly, Microsoft Bookings). When set, every "Book a free ERP assessment" button opens the calendar directly. |
| `phone` | Business phone. Shown in the footer and contact page when set. |
| `ga_id` | Google Analytics 4 measurement ID (`G-XXXXXXX`). Adds analytics and lead-event tracking. |
| `gsc_verification` | Google Search Console HTML-tag verification code. |
| `legal_name` | Legal company name for the footer and privacy page. |
| `consultant_photo` | File name of a headshot in `images/` (for example `oleh.jpg`). |
| `implementation_range` | Optional typical implementation price range, e.g. `$40,000 and $120,000`. Shown on the homepage when set. |
| `partner_statement` | Optional text for the "Are you a Microsoft partner?" FAQ. |
| `case_studies` | List of real projects. When filled, replaces the example scenarios on the homepage. Each item: `title`, `industry`, `size`, `challenge`, `solution`, `results` (list). |
| `testimonials` | List of real client quotes. Each item: `quote`, `name`, `role`, `company`. Section appears only when filled. |
| `linkedin_url` | Founder's LinkedIn profile. Used in the founder schema (`sameAs`) and shown on the homepage and contact page. |
| `prices_checked` | Date Microsoft prices were last verified (YYYY-MM-DD). Shown as "Last updated" next to prices, with a link to Microsoft's pricing page. Update it whenever you re-check prices. |
| `social_linkedin_url`, `social_youtube_url` | Company LinkedIn and YouTube links for the footer icons. Empty = icons show but do nothing. |
| `scheduler` | Working hours for the contact-page scheduler: `timezone`, `weekdays` (0=Sun to 6=Sat), `start`, `end`, `slot_minutes`, `days_ahead`, `min_notice_hours`. Ignored when `booking_url` is set (the booking page is embedded instead). |
| `allow_indexing` | `false` adds a noindex tag to every page and blocks crawlers in robots.txt. Set to `true` at launch. |
| `site_url`, `base` | Change to `https://q84digital.com/` and `/` when the custom domain is connected. |

## Blog

Posts live in the `POSTS` list in `src/build.py`. Each needs a `slug`, `title`, `date`, `tag`, `summary` and HTML `body`. Set `placeholder` to `False` (or remove it) for real articles so the draft notice disappears.

## Screenshots and demo video

See `images/README.md`. Real screenshots replace the example screens automatically.

## Custom domain

1. Set `site_url` to `https://q84digital.com/` and `base` to `/` in `src/site.json`, then rebuild.
2. Add a `CNAME` file containing `q84digital.com` and push.
3. At your domain registrar, point the domain to GitHub Pages (four A records for the apex domain, or a CNAME record for `www` to `rms2013v.github.io`).
4. In the repository's Settings → Pages, enter the domain and tick Enforce HTTPS.
