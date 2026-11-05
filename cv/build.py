"""Build the HU and EN CV as one-page A4 HTML + PDF from a single data source."""
import html
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

# Anything in [square brackets] is a missing detail and gets highlighted.
CV = {
    "hu": {
        "lang": "hu",
        "file": "Pech_Kornel_oneletrajz",
        "name": "Péch Kornél",
        "title": "Data science hallgató",
        "contact": ["Budapest", "pechkornel01@gmail.com", "+36 30 200 1692",
                    "github.com/pechkornel", "pechkornel.dev"],
        "h": {"profile": "Bemutatkozás", "exp": "Szakmai tapasztalat", "proj": "Projektek",
              "edu": "Tanulmányok", "skills": "Készségek", "lang": "Nyelvek", "sport": "Sport"},
        "profile": "A Budapesti Corvinus Egyetem Data Science in Business BSc szakos hallgatója vagyok. "
                   "A Python, a gépi tanulás és a nagy nyelvi modellek érdekelnek, ezekkel saját "
                   "projektekben és a szakdolgozatomban is dolgozom: építettem egy adatgyűjtő rendszert "
                   "helyben futó nyelvi modellel, a szakdolgozatomban pedig szövegből nyerek ki strukturált "
                   "tudást. Vállalati környezetben controlling gyakornokként szereztem tapasztalatot.",
        "exp": [
            {"role": "Controlling gyakornok", "org": "Dometic", "when": "2025. augusztus",
             "items": [
                 "Excel-alapú folyamatok automatizálása",
             ]},
            {"role": "Webfejlesztés és AI-megoldások", "org": "egyéni vállalkozó", "when": "",
             "items": [
                 "Ügyfélkereső eszköz Google Places adatokkal és a potenciális ügyfelek pontozásával",
                 "Élesben futó Google-értékeléskérő automatizáció egy budapesti virágboltnak "
                 "(WooCommerce webhook, saját küldő domain SPF/DKIM/DMARC beállítással)",
                 "AI-chatbotok és automatizációk, valamint weboldalak és webshopok (WordPress, WooCommerce) "
                 "kis- és középvállalkozásoknak",
             ]},
        ],
        "proj": [
            {"name": "Credit Risk Early Warning System", "desc": "kurzusprojekt, mélytanulási rész",
             "stack": "Python, PyTorch, pandas, scikit-learn",
             "text": "LSTM és MLP kódolóból álló fúziós modell napi piaci adatokon (CDS, hozam, "
                     "devizavolatilitás) és havi makroadatokon, amely 30-90 napra előre jelzi az országok "
                     "S&P minősítésének változását. Időrendi validáció, osztálysúlyozás a ritka események miatt."},
            {"name": "The Sentiment Gap", "desc": "szövegelemzési csapatprojekt",
             "stack": "Python, NLTK, scikit-learn, SciPy",
             "text": "100 000 Amazon-értékelésen kimutattuk, hogy a csillagszám és a szöveg hangulata az esetek "
                     "44,5%-ában eltér (khi-négyzet, Cramér V = 0,32). VADER, TF-IDF és logisztikus regresszió "
                     "(macro F1 0,655), LDA témamodellezés."},
            {"name": "apro-tracker", "desc": "adatgyűjtő és árfigyelő rendszer használt hardverhirdetésekre",
             "stack": "Python, Scrapling, Ollama, SQLAlchemy, Docker",
             "text": "Három magyar használtpiac hirdetéseit gyűjti, megőrzi a teljes ártörténetet, és a zajos "
                     "címeket szabályalapú parserrel és helyben futó nyelvi modellel strukturált termékekké alakítja."},
            {"name": "Fare Dodger", "desc": "szimuláció és játék a budapesti tömegközlekedésen",
             "stack": "Python, BKK GTFS, saját RAPTOR útvonaltervező",
             "text": "Botok közötti szimulációk (200 játék párosításonként, Wilson-intervallumokkal) a "
                     "játékszabályok kiegyensúlyozására a BKK valós menetrendjén."},
        ],
        "edu": [{"school": "Budapesti Corvinus Egyetem", "degree": "Data Science in Business BSc",
                 "when": "2023 - 2027 (várható)",
                 "items": ["Szakdolgozat (folyamatban): nagy nyelvi modellek alkalmazása szövegből "
                           "történő tudáskinyerésre és strukturálásra"]},
                {"school": "Budapesti Piarista Gimnázium", "degree": "Érettségi",
                 "when": "2023", "items": []}],
        "skills": [("Adat és ML", "Python (pandas, scikit-learn, PyTorch, NLTK), gépi tanulás, mélytanulás, NLP, hálózatelemzés (networkx), operációkutatás és LP modellezés (PuLP), "
                                  "LLM-ek (promptolás, strukturált adatkinyerés, Ollama), web scraping, Excel-automatizálás"),
                   ("Fejlesztés és infrastruktúra", "Git, GitHub, Docker, Linux, Cloudflare"),
                   ("Web", "WordPress, HTML/CSS")],
        "langs": [("Magyar", "anyanyelv"), ("Angol", "folyékony")],
        "sport": "Európa-bajnok kardvívó",
    },
    "en": {
        "lang": "en",
        "file": "Kornel_Pech_CV",
        "name": "Kornél Péch",
        "title": "Data Science student",
        "contact": ["Budapest, Hungary", "pechkornel01@gmail.com", "+36 30 200 1692",
                    "github.com/pechkornel", "pechkornel.dev"],
        "h": {"profile": "Profile", "exp": "Experience", "proj": "Projects",
              "edu": "Education", "skills": "Skills", "lang": "Languages", "sport": "Sport"},
        "profile": "Data Science in Business BSc student at Corvinus University of Budapest. I am interested "
                   "in Python, machine learning and large language models, and work with them in personal "
                   "projects and in my thesis: I built a data collection system with a locally hosted "
                   "language model, and my thesis extracts structured knowledge from text. I gained "
                   "corporate experience as a controlling intern.",
        "exp": [
            {"role": "Controlling Intern", "org": "Dometic", "when": "August 2025",
             "items": [
                 "Automating Excel-based workflows",
             ]},
            {"role": "Web Development and AI Solutions", "org": "self-employed", "when": "",
             "items": [
                 "Lead finder tool using Google Places data with prospect scoring",
                 "Live Google review request automation for a Budapest flower shop (WooCommerce webhook, "
                 "dedicated sending domain with SPF/DKIM/DMARC)",
                 "AI chatbots and automations, plus websites and webshops (WordPress, WooCommerce) "
                 "for small and medium-sized businesses",
             ]},
        ],
        "proj": [
            {"name": "Credit Risk Early Warning System", "desc": "course project, deep learning part",
             "stack": "Python, PyTorch, pandas, scikit-learn",
             "text": "Late-fusion model of an LSTM and an MLP encoder over daily market data (CDS, yields, "
                     "FX volatility) and monthly macro data, predicting S&P sovereign rating changes 30-90 "
                     "days ahead. Chronological validation and class weighting for rare events."},
            {"name": "The Sentiment Gap", "desc": "text analytics team project",
             "stack": "Python, NLTK, scikit-learn, SciPy",
             "text": "On 100,000 Amazon reviews, star rating and text sentiment disagree in 44.5% of cases "
                     "(chi-square, Cramér's V = 0.32). VADER, TF-IDF with logistic regression (macro F1 0.655), "
                     "LDA topic modelling."},
            {"name": "apro-tracker", "desc": "data collection and price tracking for used hardware listings",
             "stack": "Python, Scrapling, Ollama, SQLAlchemy, Docker",
             "text": "Collects listings from three Hungarian second-hand marketplaces, keeps full price "
                     "history, and turns messy titles into structured products with a rule parser and a "
                     "locally hosted language model."},
            {"name": "Fare Dodger", "desc": "simulation and game on Budapest public transport",
             "stack": "Python, BKK GTFS, self-written RAPTOR router",
             "text": "Bot-vs-bot simulations (200 games per matchup, Wilson intervals) to balance the game "
                     "rules on the real BKK timetable."},
        ],
        "edu": [{"school": "Corvinus University of Budapest", "degree": "Data Science in Business BSc",
                 "when": "2023 - 2027 (expected)",
                 "items": ["Thesis (in progress): using large language models to extract and structure "
                           "knowledge from text"]},
                {"school": "Budapest Piarist High School", "degree": "Secondary school leaving exam (érettségi)",
                 "when": "2023", "items": []}],
        "skills": [("Data and ML", "Python (pandas, scikit-learn, PyTorch, NLTK), machine learning, deep learning, NLP, network analysis (networkx), operational research and LP modelling (PuLP), "
                                   "LLMs (prompting, structured information extraction, Ollama), web scraping, Excel automation"),
                   ("Development and infrastructure", "Git, GitHub, Docker, Linux, Cloudflare"),
                   ("Web", "WordPress, HTML/CSS")],
        "langs": [("Hungarian", "native"), ("English", "fluent")],
        "sport": "European Champion sabre fencer",
    },
}

LINKS = {"pechkornel01@gmail.com": "mailto:pechkornel01@gmail.com",
         "+36 30 200 1692": "tel:+36302001692",
         "github.com/pechkornel": "https://github.com/pechkornel",
         "pechkornel.dev": "https://pechkornel.dev"}


def t(s):
    """Escape and highlight [missing] placeholders."""
    s = html.escape(s)
    return re.sub(r"\[([^\]]+)\]", r'<mark>\1</mark>', s)


def contact(c):
    out = []
    for item in c:
        if item in LINKS:
            out.append(f'<a href="{LINKS[item]}">{t(item)}</a>')
        else:
            out.append(f"<span>{t(item)}</span>")
    return '<span class="dot"></span>'.join(out)


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --ink:#1b1d21; --muted:#5d6470; --line:#e3e5e8; --accent:#1f4e79; }
html { font-family: Inter, sans-serif; color: var(--ink); font-size: 9pt; line-height: 1.42;
       -webkit-font-smoothing: antialiased; }
body { width: 210mm; height: 297mm; overflow: hidden; padding: 14mm 14mm 11mm; }
a { color: inherit; text-decoration: none; }
mark { background: #fff1c2; color: #7a5a00; padding: 0 2px; border-radius: 2px; }
header { padding-bottom: 5.5mm; border-bottom: 1px solid var(--line); margin-bottom: 5.5mm; }
h1 { font-family: 'Inter Display', Inter, sans-serif; font-weight: 600; font-size: 25pt;
     letter-spacing: -0.02em; line-height: 1.1; }
.title { color: var(--accent); font-weight: 500; font-size: 11pt; margin-top: 1.5mm; }
.contact { color: var(--muted); margin-top: 3mm; display: flex; flex-wrap: wrap; align-items: center; }
.dot { width: 3px; height: 3px; background: #b5bac2; border-radius: 50%; margin: 0 2.4mm; display: inline-block; }
.grid { display: grid; grid-template-columns: 1fr 58mm; gap: 9mm; }
h2 { font-size: 7.6pt; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
     color: var(--accent); margin-bottom: 2.6mm; }
section { margin-bottom: 5.2mm; }
section:last-child { margin-bottom: 0; }
.entry { margin-bottom: 3.6mm; }
.entry:last-child { margin-bottom: 0; }
.row { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }
.role { font-weight: 600; font-size: 10pt; }
.org { color: var(--muted); }
.when { color: var(--muted); font-size: 8.4pt; white-space: nowrap; font-variant-numeric: tabular-nums; }
ul { list-style: none; margin-top: 1.3mm; }
li { position: relative; padding-left: 3.6mm; margin-bottom: 0.9mm; }
li::before { content: ""; position: absolute; left: 0.4mm; top: 0.62em; width: 3.5px; height: 3.5px;
             background: var(--accent); border-radius: 50%; }
.pname { font-weight: 600; }
.pdesc { color: var(--muted); }
.stack { font-size: 8.2pt; color: var(--accent); margin: 0.6mm 0 0.6mm; }
aside .entry { margin-bottom: 3mm; }
.school { font-weight: 600; }
.skill { margin-bottom: 2.4mm; }
.skill b { display: block; font-weight: 600; font-size: 8.6pt; }
.skill span { color: #3a3f47; }
.lang { display: flex; justify-content: space-between; margin-bottom: 1mm; }
.lang span:last-child { color: var(--muted); }
.sport { font-weight: 500; }
aside li { font-size: 8.8pt; }
"""


def render(d):
    exp = "".join(
        f'<div class="entry"><div class="row"><div><span class="role">{t(e["role"])}</span>'
        f'<span class="org">, {t(e["org"])}</span></div><div class="when">{t(e["when"])}</div></div>'
        f'<ul>{"".join(f"<li>{t(i)}</li>" for i in e["items"])}</ul></div>'
        for e in d["exp"])
    proj = "".join(
        f'<div class="entry"><div><span class="pname">{t(p["name"])}</span>'
        f'<span class="pdesc">: {t(p["desc"])}</span></div>'
        f'<div class="stack">{t(p["stack"])}</div><div>{t(p["text"])}</div></div>'
        for p in d["proj"])
    edu = "".join(
        f'<div class="entry"><div class="school">{t(e["school"])}</div><div>{t(e["degree"])}</div>'
        f'<div class="when">{t(e["when"])}</div>'
        + (f'<ul>{"".join(f"<li>{t(i)}</li>" for i in e["items"])}</ul>' if e["items"] else "")
        + '</div>'
        for e in d["edu"])
    skills = "".join(f'<div class="skill"><b>{t(k)}</b><span>{t(v)}</span></div>' for k, v in d["skills"])
    langs = "".join(f'<div class="lang"><span>{t(k)}</span><span>{t(v)}</span></div>' for k, v in d["langs"])
    h = d["h"]
    return f"""<!DOCTYPE html>
<html lang="{d['lang']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t(d['name'])}, CV</title><style>{CSS}</style></head>
<body>
<header><h1>{t(d['name'])}</h1><div class="title">{t(d['title'])}</div>
<div class="contact">{contact(d['contact'])}</div></header>
<div class="grid">
<main>
<section><h2>{h['profile']}</h2><p>{t(d['profile'])}</p></section>
<section><h2>{h['exp']}</h2>{exp}</section>
<section><h2>{h['proj']}</h2>{proj}</section>
</main>
<aside>
<section><h2>{h['edu']}</h2>{edu}</section>
<section><h2>{h['skills']}</h2>{skills}</section>
<section><h2>{h['lang']}</h2>{langs}</section>
<section><h2>{h['sport']}</h2><div class="sport">{t(d['sport'])}</div></section>
</aside>
</div>
</body></html>"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for key, d in CV.items():
            html_path = OUT / f"{d['file']}.html"
            html_path.write_text(render(d), encoding="utf-8")
            page.goto(html_path.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            height = page.evaluate("Math.max(...[...document.querySelectorAll('main,aside')].map(e=>e.getBoundingClientRect().bottom))")
            page.pdf(path=str(OUT / f"{d['file']}.pdf"), format="A4", print_background=True,
                     prefer_css_page_size=True)
            print(key, "body height px:", height, "content bottom, limit ~1081")
        browser.close()


if __name__ == "__main__":
    sys.exit(main())
