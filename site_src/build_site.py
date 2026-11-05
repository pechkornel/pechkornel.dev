"""Static site generator for pechkornel.dev.

Run:  python build_site.py   ->  writes ../site/ (deploy that folder to Cloudflare Pages)
All content lives in the PROJECTS list and the page functions below.
"""
import html
import importlib.util
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "site"
GH = "https://github.com/pechkornel"

# ---------------------------------------------------------------- content
PROJECTS = [
    {
        "slug": "credit-risk-ews",
        "title": "Credit Risk Early Warning System",
        "kicker": "Deep learning, time series",
        "summary": "Predicting sovereign rating changes 30 to 90 days ahead from daily market data "
                   "with an LSTM and MLP fusion model.",
        "tags": ["PyTorch", "LSTM", "Imbalanced classification"],
        "meta": [("Context", "Course project, Machine Learning in Practice II"), ("When", "Spring 2026"),
                 ("Stack", "Python, pandas, PyTorch, scikit-learn")],
        "repo": f"{GH}/credit-risk-ews",
        "image": ("credit-confusion.webp", "Confusion matrix on the test period"),
        "body": [
            ("The question",
             "<p>Can market signals that move every day, such as CDS spreads, bond yields and FX "
             "volatility, warn a bank that a country's S&amp;P credit rating is about to change? The "
             "model looks at a 60-day window and predicts an upgrade, a downgrade or no change in the "
             "30 to 90 days after it.</p>"),
            ("Data",
             "<p>Daily CDS, 10-year yield and FX volatility per country from 2010, exported from "
             "Bloomberg, plus monthly inflation, FX reserves and the policy rate forward-filled onto "
             "the daily grid. Targets come from the S&amp;P rating history. About 96% of the training "
             "windows are \"no change\", which is the real difficulty of the task.</p>"),
            ("Approach",
             "<ul><li>Custom parsers for the Bloomberg wide export, resampling and gap filling within "
             "each country so nothing leaks across countries.</li>"
             "<li>A chronological split: train up to October 2022, test on everything after.</li>"
             "<li>A late-fusion network: a 2-layer LSTM encodes the daily sequence, an MLP encodes the "
             "macro snapshot, and both feed one classification head.</li>"
             "<li>Weighted cross-entropy against the class imbalance, and early stopping.</li></ul>"),
            ("Result",
             "<p>The weighted model catches about half of the real upgrades and downgrades in the test "
             "period, but only by raising far too many false alarms, so in this form it is not a usable "
             "early warning system. I keep it in the portfolio as an honest negative result: with a "
             "handful of rating actions per country the event classes are too small for a sequence "
             "model, and a ranking formulation (flag the riskiest country-days) on engineered features "
             "is the better next step.</p>"),
        ],
    },
    {
        "slug": "sentiment-gap",
        "title": "The Sentiment Gap",
        "kicker": "NLP, statistics",
        "summary": "Star ratings and review text disagree in 44.5% of 100,000 Amazon reviews. "
                   "What drives the gap?",
        "tags": ["NLTK", "TF-IDF", "LDA", "Hypothesis testing"],
        "meta": [("Context", "Team project, Text Analytics"), ("When", "Spring 2026"),
                 ("Team", "Németh Mariann, Péch Kornél, Somlai Dóra, Tulit Zsolt"),
                 ("Stack", "Python, NLTK, scikit-learn, SciPy")],
        "repo": f"{GH}/sentiment-gap",
        "extra_links": [("Paper (PDF)", f"{GH}/sentiment-gap/blob/main/sentiment_gap_paper.pdf"),
                        ("Slides (PDF)", f"{GH}/sentiment-gap/blob/main/sentiment_gap_slides.pdf")],
        "image": ("sentiment-heatmap.webp", "VADER sentiment labels against labels derived from the stars"),
        "body": [
            ("The question",
             "<p>Shoppers lean on star ratings, but the text of a review often tells a different "
             "story. We measured how often the sentiment of the text and the star rating disagree, and "
             "tested two explanations: delivery problems, and how much people write.</p>"),
            ("Data and methods",
             "<p>A balanced sample of 100,000 verified Amazon Electronics reviews, 20,000 per star "
             "level. NLTK preprocessing, VADER sentiment, a TF-IDF and logistic regression classifier, "
             "LDA topics and a keyword-based logistics proxy checked with keyword-in-context reading. "
             "Every claim is backed by a significance test and an effect size, with robustness checks "
             "across thresholds, review length and time.</p>"),
            ("Findings",
             "<table><tr><th>Question</th><th>Result</th></tr>"
             "<tr><td>How big is the gap?</td><td><b>44.5%</b> of reviews mismatch, Cramér's V = 0.32, "
             "stable across thresholds and periods</td></tr>"
             "<tr><td>Do logistics complaints matter?</td><td>They cost <b>0.60 stars</b> on average, "
             "Cohen's d = 0.43</td></tr>"
             "<tr><td>Does length matter?</td><td>Long reviews mismatch more: <b>50.2% vs 40.2%</b></td></tr>"
             "<tr><td>Can text alone predict the rating?</td><td>Partly: macro F1 = <b>0.655</b></td></tr>"
             "</table>"
             "<p>Negative reviews are often written in a factual tone with few evaluative words, which "
             "a lexicon model reads as neutral. Part of the gap is therefore a limit of VADER, and a "
             "transformer model fine-tuned on reviews is the next step.</p>"),
        ],
        "gallery": [("sentiment-vader.webp", "VADER compound score by star rating"),
                    ("sentiment-logistics.webp", "Share of logistics mentions by star rating")],
    },
    {
        "slug": "apro-tracker",
        "title": "apro-tracker",
        "kicker": "Data pipeline, web scraping, local LLM",
        "summary": "A price tracker for used PC parts that crawls three Hungarian marketplaces, keeps "
                   "the full history of every listing and turns messy titles into structured products.",
        "tags": ["Scraping", "SQLAlchemy", "Ollama", "FastAPI"],
        "meta": [("Context", "Personal project"), ("When", "2026, ongoing"),
                 ("Stack", "Python, Scrapling, SQLAlchemy, Alembic, FastAPI, HTMX, Ollama, Docker")],
        "repo": None,
        "repo_note": "Private repository, happy to walk through the code on request.",
        "image": ("apro-model.webp", "Price history page for one GPU model"),
        "body": [
            ("What it does",
             "<p>Every 30 minutes it crawls the GPU, CPU, motherboard, memory, PSU, storage and case "
             "categories of HardverApró, and Jófogás and Vatera every two hours. It records every price "
             "change, title edit, reservation and disappearance, so it knows what a part usually sells "
             "for and how fast it goes.</p>"),
            ("The data problem",
             "<p>Listing titles are written by hand, for example <code>Gigabyte RTX 3070 Gaming OC 8GB "
             "garis</code>. A rule parser turns most of them into structured products (brand, model, "
             "memory, maker), and a small local language model running on my own server handles the "
             "cases the rules are unsure about.</p>"),
            ("Engineering",
             "<ul><li>Typed Python (mypy strict), tests and CI, database migrations with Alembic.</li>"
             "<li>26 written architecture decision records.</li>"
             "<li>A server-rendered web UI with deals, price history and watchlists, published behind "
             "an invite-only Cloudflare Access gate.</li>"
             "<li>Runs in Docker on my homelab server, with backups and one-click updates.</li></ul>"),
        ],
        "gallery": [("apro-buys.webp", "Deals page: best used parts right now, against their usual price")],
    },
    {
        "slug": "fare-dodger",
        "title": "Fare Dodger",
        "kicker": "Algorithms, simulation",
        "summary": "A hidden-movement chase game on the real Budapest timetable, balanced with "
                   "thousands of bot-vs-bot simulations.",
        "tags": ["GTFS", "RAPTOR routing", "Simulation"],
        "meta": [("Context", "Personal project"), ("When", "2026, ongoing"),
                 ("Stack", "Python, BKK GTFS, Docker")],
        "repo": f"{GH}/fare-dodger",
        "body": [
            ("The game",
             "<p>One hidden Fare Dodger tries to stay ahead of three Inspectors for 12 rounds. Every "
             "round is 10 minutes of real weekday service on the Budapest metro, tram, trolleybus and "
             "main bus lines, and every move is validated against the timetable.</p>"),
            ("Under the hood",
             "<ul><li>GTFS ingestion of the BKK feed into a playable network of 421 stations.</li>"
             "<li>A self-written RAPTOR router for fast earliest-arrival journeys.</li>"
             "<li>Bots: a greedy Dodger that maximises distance to the Inspectors, and Inspectors that "
             "track every station the Dodger could be at and spread to cover it (also a k-means "
             "variant).</li>"
             "<li>A deterministic simulation runner, and a real-time 3D browser version for team play.</li></ul>"),
            ("Balancing with data",
             "<p>The target is a Dodger win rate of about 45% against the best Inspectors. I ran 200 "
             "games per matchup and report Wilson 95% intervals.</p>"
             "<table><tr><th>Rule set</th><th>Dodger wins</th></tr>"
             "<tr><td>Original rules</td><td>76.0% [70-81%]</td></tr>"
             "<tr><td>Four Inspectors</td><td>71.0% [64-77%]</td></tr>"
             "<tr><td>Reveal transport modes</td><td>57.0% [50-64%]</td></tr>"
             "<tr><td>Reveal modes, position every 2nd round</td><td><b>46.5% [40-53%]</b></td></tr></table>"
             "<p>The lesson: <b>information is the bottleneck, not manpower</b>. A fourth Inspector "
             "barely helps, while revealing more information shrinks the set of possible positions "
             "and brings the game into balance.</p>"),
        ],
    },
    {
        "slug": "trading-bot",
        "title": "Paper-trading portfolio bot",
        "kicker": "Machine learning, systems",
        "summary": "XGBoost and LSTM trend models, a score-based ETF allocation and a news sentiment "
                   "sleeve, running on paper money with a web dashboard.",
        "tags": ["XGBoost", "LSTM", "FastAPI", "Docker"],
        "meta": [("Context", "Personal project"), ("When", "2025 to 2026"),
                 ("Stack", "Python, scikit-learn, XGBoost, TensorFlow, FastAPI, HTMX, SQLite, Docker")],
        "repo": f"{GH}/trading-bot",
        "body": [
            ("From experiments to one system",
             "<p>It started as four separate scripts: an XGBoost trend classifier, an LSTM, a test bot "
             "and a backtester. I consolidated them into one codebase with a model registry, so the "
             "live runner always loads a model together with the features and scaler it was trained "
             "with.</p>"),
            ("Strategy",
             "<ul><li><b>Core sleeve (70%):</b> weekly scores for 10 ETFs from momentum, macro "
             "alignment and trend, holding the top 4, with a risk-off switch to bonds.</li>"
             "<li><b>Sentiment sleeve (20%):</b> long positions on strong bullish news spikes from the "
             "Alpha Vantage sentiment API, with a time exit and a stop.</li>"
             "<li><b>Tactical models:</b> technical indicators as features, XGBoost (class weights or "
             "SMOTE) and a 2-layer LSTM, fused 70/30 with sentiment and sized by volatility "
             "targeting.</li></ul>"),
            ("Safety first",
             "<p>The bot refuses to start unless it is pointed at a paper account, runs as a dry run "
             "by default, and keeps every decision and order in SQLite for the FastAPI and HTMX "
             "dashboard.</p>"),
        ],
    },
]

MORE = [
    ("Solar Performance & Weather Analytics", "AWS Lambda pulls weather data into an S3 data lake, "
     "Glue and Athena join it with inverter telemetry to measure heat-related energy loss.",
     ["AWS", "SQL", "Data engineering"], f"{GH}/solar_analytics"),
    ("AWS Data Engineering Capstone", "CSV to Parquet conversion, Glue crawlers, Athena views and "
     "analysis on 70 years of global fisheries data.", ["AWS Glue", "Athena", "Parquet"], f"{GH}/capstone"),
]

# ---------------------------------------------------------------- layout
CSS = """
@font-face{font-family:Inter;src:url(/assets/fonts/Inter-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Inter;src:url(/assets/fonts/Inter-Medium.woff2) format('woff2');font-weight:500;font-display:swap}
@font-face{font-family:Inter;src:url(/assets/fonts/Inter-SemiBold.woff2) format('woff2');font-weight:600;font-display:swap}
@font-face{font-family:'Inter Display';src:url(/assets/fonts/InterDisplay-SemiBold.woff2) format('woff2');font-weight:600;font-display:swap}
:root{--ink:#16181d;--muted:#5d6470;--line:#e4e6ea;--soft:#f5f6f8;--accent:#1f4e79;--accent-soft:#e8eef5}
*{box-sizing:border-box;margin:0;padding:0}
html{font-family:Inter,system-ui,sans-serif;color:var(--ink);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;background:#fff}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:860px;margin:0 auto;padding:0 24px}
nav{border-bottom:1px solid var(--line)}
nav .wrap{display:flex;justify-content:space-between;align-items:center;height:64px}
nav .brand{font-weight:600;color:var(--ink)}
nav .links a{color:var(--muted);margin-left:22px;font-size:.92rem}nav .links a:hover{color:var(--ink);text-decoration:none}
h1,h2,h3{font-family:'Inter Display',Inter,sans-serif;font-weight:600;letter-spacing:-.015em;line-height:1.2}
.hero{padding:88px 0 56px}
.hero h1{font-size:2.9rem}
.hero p{font-size:1.18rem;color:var(--muted);max-width:620px;margin-top:18px}
.hero .cta{margin-top:28px;display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;padding:9px 16px;border-radius:8px;border:1px solid var(--line);color:var(--ink);font-weight:500;font-size:.92rem}
.btn:hover{background:var(--soft);text-decoration:none}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}.btn.primary:hover{background:#18405f}
section{padding:40px 0}
.eyebrow{font-size:.75rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:18px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.card{border:1px solid var(--line);border-radius:12px;padding:22px;display:flex;flex-direction:column;transition:border-color .15s,box-shadow .15s;color:var(--ink)}
a.card:hover{border-color:#c9d3df;box-shadow:0 4px 18px rgba(20,30,50,.06);text-decoration:none}
.card .k{font-size:.78rem;color:var(--muted);margin-bottom:6px}
.card h3{font-size:1.15rem;margin-bottom:8px}
.card p{color:#3a3f47;font-size:.94rem;flex:1}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.tag{font-size:.74rem;background:var(--accent-soft);color:var(--accent);padding:2px 9px;border-radius:99px;font-weight:500}
.card.wide{grid-column:span 2}
.about p{max-width:640px;color:#3a3f47;margin-bottom:12px}
footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:.86rem}
footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.proj-head{padding:64px 0 26px}
.proj-head .back{font-size:.88rem;color:var(--muted)}
.proj-head h1{font-size:2.4rem;margin-top:18px}
.proj-head p.lead{font-size:1.15rem;color:var(--muted);margin-top:14px;max-width:660px}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px 26px;margin:28px 0;padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.meta dt{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:600}
.meta dd{font-size:.92rem;margin-top:3px}
figure{margin:28px 0}figure img{width:auto;max-width:100%;height:auto;margin:0 auto;border:1px solid var(--line);border-radius:10px;display:block;background:#fff}
figcaption{font-size:.84rem;color:var(--muted);margin-top:8px;text-align:center}
.gallery{display:grid;grid-template-columns:1fr 1fr;gap:16px}.gallery.one{grid-template-columns:1fr}
article h2{font-size:1.35rem;margin:36px 0 12px}
article p,article li{color:#2c3038}
article ul{padding-left:20px}article li{margin-bottom:8px}
article p+p{margin-top:12px}
article table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.93rem}
article th,article td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
article th{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:600}
code{font-size:.88em;background:var(--soft);padding:1px 5px;border-radius:4px}
.links-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.note{font-size:.9rem;color:var(--muted);margin-top:16px}
@media (max-width:700px){html{font-size:16px}.cards,.gallery{grid-template-columns:1fr}.card.wide{grid-column:auto}.hero{padding:56px 0 36px}.hero h1{font-size:2.2rem}nav .links a{margin-left:14px}}
"""

DESC = ("Kornél Péch, data science student at Corvinus University of Budapest. "
        "Machine learning, NLP and data pipeline projects.")


def page(title, body, desc=DESC, path="/"):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="https://pechkornel.dev{path}">
<link rel="canonical" href="https://pechkornel.dev{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
</head><body>
<nav><div class="wrap"><a class="brand" href="/">Kornél Péch</a>
<div class="links"><a href="/#projects">Projects</a><a href="/cv/">CV</a><a href="{GH}">GitHub</a></div></div></nav>
{body}
<footer><div class="wrap"><span>Kornél Péch, Budapest</span>
<span><a href="mailto:pechkornel01@gmail.com">pechkornel01@gmail.com</a> · <a href="{GH}">github.com/pechkornel</a></span></div></footer>
</body></html>"""


def tags(ts):
    return '<div class="tags">' + "".join(f'<span class="tag">{html.escape(t)}</span>' for t in ts) + "</div>"


def index():
    cards = "".join(
        f'<a class="card{" wide" if i == len(PROJECTS) - 1 and len(PROJECTS) % 2 else ""}" href="/projects/{p["slug"]}/"><div class="k">{html.escape(p["kicker"])}</div>'
        f'<h3>{html.escape(p["title"])}</h3><p>{html.escape(p["summary"])}</p>{tags(p["tags"])}</a>'
        for i, p in enumerate(PROJECTS))
    more = "".join(
        f'<a class="card" href="{url}"><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p>{tags(ts)}</a>'
        for t, d, ts, url in MORE)
    body = f"""
<header class="hero"><div class="wrap">
<h1>Kornél Péch</h1>
<p>Data science student at Corvinus University of Budapest. I build machine learning models, data
pipelines and the tools around them, from scraping the data to shipping the dashboard.</p>
<div class="cta"><a class="btn primary" href="/cv/">View CV</a><a class="btn" href="{GH}">GitHub</a>
<a class="btn" href="mailto:pechkornel01@gmail.com">Email me</a></div>
</div></header>
<section id="projects"><div class="wrap"><div class="eyebrow">Selected projects</div>
<div class="cards">{cards}</div></div></section>
<section><div class="wrap"><div class="eyebrow">More projects</div><div class="cards">{more}</div></div></section>
<section class="about"><div class="wrap"><div class="eyebrow">About</div>
<p>I study Data Science in Business at Corvinus University of Budapest (2023 to 2027). My thesis
uses large language models to extract structured knowledge from text. I like projects where data
meets a real system: collecting it, modelling it and building the tool people actually use.</p>
<p>I worked as a controlling intern at Dometic, and I build websites and AI automations for small
businesses on the side. Outside of code I am a European Champion sabre fencer.</p>
</div></section>"""
    return page("Kornél Péch, data science", body)


def project(p):
    meta = "".join(f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in p["meta"])
    links = ""
    if p.get("repo"):
        links += f'<a class="btn primary" href="{p["repo"]}">View on GitHub</a>'
    for label, url in p.get("extra_links", []):
        links += f'<a class="btn" href="{url}">{html.escape(label)}</a>'
    note = f'<p class="note">{html.escape(p["repo_note"])}</p>' if p.get("repo_note") else ""
    fig = ""
    if p.get("image"):
        src, cap = p["image"]
        fig = (f'<figure><img src="/assets/img/{src}" alt="{html.escape(cap)}" loading="lazy">'
               f'<figcaption>{html.escape(cap)}</figcaption></figure>')
    sections = "".join(f"<h2>{html.escape(h)}</h2>{b}" for h, b in p["body"])
    gal = ""
    if p.get("gallery"):
        cls = "gallery one" if len(p["gallery"]) == 1 else "gallery"
        gal = f'<div class="{cls}">' + "".join(
            f'<figure><img src="/assets/img/{s}" alt="{html.escape(c)}" loading="lazy">'
            f"<figcaption>{html.escape(c)}</figcaption></figure>" for s, c in p["gallery"]) + "</div>"
    body = f"""
<header class="proj-head"><div class="wrap"><a class="back" href="/#projects">← All projects</a>
<h1>{html.escape(p["title"])}</h1><p class="lead">{html.escape(p["summary"])}</p>
<div class="links-row">{links}</div>{note}</div></header>
<div class="wrap"><dl class="meta">{meta}</dl>
<article>{fig}{sections}{gal}</article></div>"""
    return page(f'{p["title"]}, Kornél Péch', body, p["summary"], f'/projects/{p["slug"]}/')


# ---------------------------------------------------------------- CV pages from the CV generator
def cv_pages():
    spec = importlib.util.spec_from_file_location("cvbuild", ROOT.parent / "cv" / "build.py")
    cv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cv)
    web_css = cv.CSS.replace("@page { size: A4; margin: 0; }", "") \
        .replace("body { width: 210mm; height: 297mm; overflow: hidden; padding: 14mm 14mm 11mm; }",
                 "body { max-width: 210mm; margin: 0 auto; padding: 28px 24px 48px; }") \
        .replace("mark {", "mark { background:none; color:inherit; } .x {")
    web_css += """
.bar{display:flex;padding:0 0 22px;justify-content:space-between;
 font-family:Inter,sans-serif;font-size:9.5pt}
.bar a{color:#1f4e79;text-decoration:none;margin-left:14px}
@media (max-width:720px){.grid{grid-template-columns:1fr !important}.row{flex-direction:column}}
"""
    cv.CSS = web_css
    out = {}
    for key, d in cv.CV.items():
        # the phone number stays in the PDF only, not on the public web page
        d = dict(d, contact=[c for c in d["contact"] if not c.startswith("+")])
        doc = cv.render(d)
        other = ("/cv/hu/", "Magyar") if key == "en" else ("/cv/", "English")
        pdf = f'/cv/{d["file"]}.pdf'
        dl = "Download PDF" if key == "en" else "PDF letöltése"
        back = "pechkornel.dev" if key == "en" else "pechkornel.dev"
        bar = (f'<div class="bar"><a href="/" style="margin-left:0">← {back}</a><span>'
               f'<a href="{other[0]}">{other[1]}</a><a href="{pdf}">{dl}</a></span></div>')
        doc = doc.replace("<body>", "<body>\n" + bar, 1)
        doc = doc.replace("</title>", '</title>\n<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">'
                          '\n<style>@font-face{font-family:Inter;src:url(/assets/fonts/Inter-Regular.woff2) format("woff2");font-weight:400}'
                          '@font-face{font-family:Inter;src:url(/assets/fonts/Inter-Medium.woff2) format("woff2");font-weight:500}'
                          '@font-face{font-family:Inter;src:url(/assets/fonts/Inter-SemiBold.woff2) format("woff2");font-weight:600}'
                          '@font-face{font-family:"Inter Display";src:url(/assets/fonts/InterDisplay-SemiBold.woff2) format("woff2");font-weight:600}</style>', 1)
        out[key] = doc
    return out, cv


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1f4e79"/>
<text x="32" y="42" font-family="Inter,Arial,sans-serif" font-size="28" font-weight="600" fill="#fff" text-anchor="middle">KP</text></svg>"""


def build():
    if OUT.exists():
        for child in OUT.iterdir():
            if child.name != "assets":
                shutil.rmtree(child) if child.is_dir() else child.unlink()
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "site.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (OUT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    for p in PROJECTS:
        d = OUT / "projects" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(project(p), encoding="utf-8")
    pages, cv = cv_pages()
    (OUT / "cv" / "hu").mkdir(parents=True, exist_ok=True)
    (OUT / "cv" / "index.html").write_text(pages["en"], encoding="utf-8")
    (OUT / "cv" / "hu" / "index.html").write_text(pages["hu"], encoding="utf-8")
    for d in cv.CV.values():
        shutil.copy(ROOT.parent / "cv" / "out" / f'{d["file"]}.pdf', OUT / "cv" / f'{d["file"]}.pdf')
    (OUT / "404.html").write_text(page("Not found, Kornél Péch",
        '<header class="hero"><div class="wrap"><h1>Page not found</h1><p>'
        '<a href="/">Back to the start page</a></p></div></header>'), encoding="utf-8")
    urls = ["/", "/cv/", "/cv/hu/"] + [f'/projects/{p["slug"]}/' for p in PROJECTS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>https://pechkornel.dev{u}</loc></url>" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://pechkornel.dev/sitemap.xml\n")
    print("built", sum(1 for _ in OUT.rglob("*") if _.is_file()), "files")


if __name__ == "__main__":
    build()
