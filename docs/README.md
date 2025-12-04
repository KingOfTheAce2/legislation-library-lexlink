# LexLink Static Site

This folder contains the generated static HTML site for GitHub Pages.

**Do not edit files in this folder directly!**

Files are auto-generated from:
- `data/dictionaries/` - Term dictionaries
- `data/examples/` - Article examples
- `scripts/generate_static_site.py` - Site generator

## Regenerating the Site

```bash
cd scripts
python create_css.py
python generate_static_site.py
```

## GitHub Pages Setup

1. Push this repository to GitHub
2. Go to repository Settings > Pages
3. Set source to: **Deploy from branch**
4. Set branch to: **main** and folder to: **/docs**
5. Save and wait for deployment

Your site will be live at:
`https://yourusername.github.io/legislation-library-lexlink/`

## Custom Domain (Optional)

Edit `docs/CNAME` and add your domain name, then configure DNS:
```
CNAME record: www.yourdomain.com -> yourusername.github.io
A record: yourdomain.com -> GitHub Pages IPs
```
