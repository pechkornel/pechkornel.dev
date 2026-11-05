# pechkornel.dev

Source of my personal site: project case studies and my CV in English and Hungarian.

```
cv/build.py              CV content (HU + EN) -> cv/out/*.pdf and *.html (one-page A4)
site_src/build_site.py   site content and templates -> site/
site/                    the generated static site, deployed as is
```

## Edit and rebuild

```sh
pip install playwright && python -m playwright install chromium   # only needed for the PDFs
python cv/build.py          # 1. CV PDFs
python site_src/build_site.py   # 2. site (copies the PDFs into site/cv/)
python -m http.server -d site 8000   # preview at http://localhost:8000
```

Project texts live in the `PROJECTS` list in `site_src/build_site.py`, CV texts in the `CV`
dictionary in `cv/build.py`. Images and fonts are in `site/assets/`.

## Deploy (Cloudflare Pages)

Workers & Pages, Create, Pages, Connect to Git, pick this repository, then:

- Framework preset: None
- Build command: (empty)
- Build output directory: `site`

Then add `pechkornel.dev` under Custom domains. Every push to `main` redeploys the site.
