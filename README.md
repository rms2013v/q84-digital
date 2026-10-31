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
| `booking_url` | Calendar link (Calendly, Microsoft Bookings). Adds "Book a 30-minute call" buttons. |
| `phone` | Business phone. Shown in the footer and contact page when set. |
| `ga_id` | Google Analytics 4 measurement ID (`G-XXXXXXX`). Adds analytics and lead-event tracking. |
| `gsc_verification` | Google Search Console HTML-tag verification code. |
| `legal_name` | Legal company name for the footer and privacy page. |
| `consultant_photo` | File name of a headshot in `images/` (for example `oleh.jpg`). |
| `site_url`, `base` | Change to `https://q84digital.com/` and `/` when the custom domain is connected. |

## Screenshots and demo video

See `images/README.md`. Real screenshots replace the example screens automatically.

## Custom domain

1. Set `site_url` to `https://q84digital.com/` and `base` to `/` in `src/site.json`, then rebuild.
2. Add a `CNAME` file containing `q84digital.com` and push.
3. At your domain registrar, point the domain to GitHub Pages (four A records for the apex domain, or a CNAME record for `www` to `rms2013v.github.io`).
4. In the repository's Settings → Pages, enter the domain and tick Enforce HTTPS.
