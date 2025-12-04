# GitHub Pages Setup Guide

This guide explains how to deploy your LexLink legal dictionary as a public website on GitHub Pages.

## 📊 What's Been Generated

**Total Pages Created:** 5,083 HTML pages
- 821 individual term pages (each term has its own URL)
- 4,252 article example pages
- 10+ index and navigation pages

**Features:**
- ✅ SEO-optimized (each page has unique title, meta description, keywords)
- ✅ Parallel language layout (left: source language, right: target language)
- ✅ Responsive design (works on mobile, tablet, desktop)
- ✅ Searchable dictionary indexes
- ✅ Breadcrumb navigation
- ✅ Print-friendly styling
- ✅ Dark mode support
- ✅ Accessibility features

## 🚀 Deployment Steps

### Step 1: Commit the Files

```bash
# Add all generated files
git add docs/
git add .nojekyll
git add scripts/generate_static_site.py
git add scripts/create_css.py

# Commit
git commit -m "Add static site for GitHub Pages

- Generated 5,083 HTML pages (821 terms + 4,252 examples)
- Parallel language layout (Dutch/German/English)
- SEO-optimized individual pages for each term
- Responsive design with search functionality"

# Push to GitHub
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/legislation-library-lexlink`
2. Click **Settings** (top right)
3. In the left sidebar, click **Pages**
4. Under "Build and deployment":
   - **Source:** Select "Deploy from a branch"
   - **Branch:** Select `main` and folder `/docs`
   - Click **Save**
5. Wait 1-2 minutes for deployment

### Step 3: Access Your Site

Your site will be live at:
```
https://YOUR_USERNAME.github.io/legislation-library-lexlink/
```

Example URLs:
- Homepage: `https://YOUR_USERNAME.github.io/legislation-library-lexlink/`
- NL-EN Dictionary: `https://YOUR_USERNAME.github.io/legislation-library-lexlink/dictionaries/nl-nl_en-gb/index.html`
- Individual term: `https://YOUR_USERNAME.github.io/legislation-library-lexlink/dictionaries/nl-nl_en-gb/aanhangig.html`

## 🔍 SEO Benefits

Each term has its own page with:
- **Unique URL:** `aanhangig.html`, `rechtspersoon.html`, etc.
- **Page title:** "aanhangig → pending - LexLink Legal Dictionary"
- **Meta description:** Optimized for search engines
- **OpenGraph tags:** Social media sharing support

This makes each term:
- ✅ Indexable by Google/Bing/DuckDuckGo
- ✅ Shareable with unique links
- ✅ Bookmarkable
- ✅ Linkable from external sites

## 📱 Responsive Layout

The parallel language view adapts to screen size:

**Desktop (>768px):**
```
┌────────────────────────────────────────┐
│  Dutch (nl-nl)    →    English (en-gb) │
│  aanhangig               pending        │
└────────────────────────────────────────┘
```

**Mobile (<768px):**
```
┌──────────────────┐
│  Dutch (nl-nl)   │
│  aanhangig       │
├──────────────────┤
│  English (en-gb) │
│  pending         │
└──────────────────┘
```

## 🎨 Customization

### Change Colors

Edit `docs/css/style.css` line 5-12:
```css
:root {
    --primary-color: #2c3e50;      /* Header/titles */
    --secondary-color: #3498db;    /* Links/buttons */
    --accent-color: #e74c3c;       /* Highlights */
}
```

### Add Custom Domain

1. Buy a domain (e.g., `lexlink.law`)
2. Edit `docs/CNAME`:
   ```
   lexlink.law
   ```
3. Configure DNS at your domain registrar:
   ```
   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io

   Type: A
   Name: @
   Values: 185.199.108.153
           185.199.109.153
           185.199.110.153
           185.199.111.153
   ```
4. Wait for DNS propagation (1-24 hours)

### Update GitHub Link

Edit `scripts/generate_static_site.py` line 86:
```python
<a href="https://github.com/YOUR_USERNAME/legislation-library-lexlink">
```

Then regenerate:
```bash
cd scripts
python generate_static_site.py
```

## 🔄 Updating Content

When you add new terms or update translations:

```bash
# 1. Update CSV files in data/dictionaries/ or data/examples/

# 2. Regenerate site
cd scripts
python create_css.py      # Only if CSS changed
python generate_static_site.py

# 3. Commit and push
git add docs/
git commit -m "Update dictionary with new terms"
git push origin main
```

GitHub Pages will automatically rebuild in 1-2 minutes.

## 📊 Site Statistics

**File Structure:**
```
docs/
├── index.html                          # Landing page
├── about.html                          # About page
├── css/style.css                       # Stylesheet
├── favicon.svg                         # Site icon
├── dictionaries/
│   ├── nl-nl_en-gb/
│   │   ├── index.html                  # Dictionary index with search
│   │   ├── aanhangig.html             # Individual term pages (619 total)
│   │   └── ...
│   └── nl-nl_de-de/
│       ├── index.html
│       ├── rechtspersoon.html         # Individual term pages (202 total)
│       └── ...
└── articles/
    ├── index.html                      # Articles overview
    ├── book-1/
    │   ├── index.html
    │   └── [4252 example pages]
    ├── book-2-3/
    └── book-4/
```

**Storage:**
- Total size: ~25-30 MB (uncompressed)
- GitHub Pages limit: 1 GB (plenty of room)
- Bandwidth limit: 100 GB/month (soft limit)

## 🔐 Privacy & Licensing

The site is **public** by default. To add licensing:

1. Create `docs/license.html`
2. Add copyright notice
3. Specify usage terms (e.g., CC BY-NC-SA 4.0)

Example:
```html
<p>© 2025 LexLink. All translations © respective translators.</p>
<p>Usage: Attribution-NonCommercial-ShareAlike 4.0 International</p>
```

## 🐛 Troubleshooting

**Site not deploying?**
- Check Settings > Pages shows "Your site is live"
- Verify `/docs` folder is in `main` branch
- Check Actions tab for build errors

**CSS not loading?**
- Verify `docs/css/style.css` exists
- Check browser console (F12) for 404 errors
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

**Search not working?**
- JavaScript is inline in HTML, should work automatically
- Check browser console for errors
- Ensure you're viewing over HTTPS (not file://)

## 📈 Analytics (Optional)

Add Google Analytics by editing `scripts/generate_static_site.py` line 18, add before `</head>`:

```python
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Then regenerate the site.

## ✅ Next Steps

1. ✅ Commit and push to GitHub
2. ✅ Enable GitHub Pages in repository settings
3. ⬜ Share your site URL
4. ⬜ (Optional) Add custom domain
5. ⬜ (Optional) Add Google Analytics
6. ⬜ (Optional) Submit sitemap to Google Search Console

Your professional legal dictionary is now live and searchable! 🎉

---

**Generated:** 2025-11-26
**Pages:** 5,083 HTML files
**Languages:** Dutch, English, German
**Domains:** Civil Procedure, Tax Law
