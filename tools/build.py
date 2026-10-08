#!/usr/bin/env python3
"""Build loveikolabs.com.

  python3 tools/build.py            # regenerate pages + patch app pages / guides
  python3 tools/build.py --refresh  # also pull ratings + screenshots from the iTunes lookup API

Generated:  /, /health/, /pregnancy-baby/, /resale/, /home-style/, /apps/, /guides/,
            /about/, /editorial-policy/, sitemap.xml, llms.txt (app list section)
Patched in place (content untouched): /apps/<slug>/ and /best-*/ — nav, footer,
            breadcrumb + BreadcrumbList, hub accent, scripts, App Store ratings.
"""
import datetime, html, json, re, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from site_data import HUBS, APPS, HERO_POSTERS, SITE, EMAIL, FOUNDER  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STORE = Path(__file__).parent / "store.json"
TODAY = datetime.date.today()
TODAY_ISO = TODAY.isoformat()
TODAY_H = TODAY.strftime("%B %Y")
DEV_URL = "https://apps.apple.com/us/developer/valeriy-loveyko/id1478618306"

HUB = {h["key"]: h for h in HUBS}
APP = {a["slug"]: a for a in APPS}
e = html.escape


# ───────────────────────────── store data ─────────────────────────────
def refresh_store():
    ids = ",".join(str(a["store_id"]) for a in APPS)
    url = f"https://itunes.apple.com/lookup?id={ids}&country=us"
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    out = {}
    for r in data["results"]:
        out[str(r["trackId"])] = {
            "trackName": r["trackName"],
            "url": r["trackViewUrl"].split("?")[0],
            "rating": round(r.get("averageUserRating") or 0, 2),
            "count": r.get("userRatingCount") or 0,
            "version": r.get("version"),
            "minOS": r.get("minimumOsVersion"),
            "released": (r.get("releaseDate") or "")[:10],
            "updated": (r.get("currentVersionReleaseDate") or "")[:10],
            "screenshots": [re.sub(r"/[^/]+$", "/460x0w.webp", u) for u in r.get("screenshotUrls", [])],
        }
    out["_fetched"] = TODAY_ISO
    STORE.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"store.json refreshed: {len(out) - 1} apps")


def store():
    return json.loads(STORE.read_text())


def S(app):
    return store_data[str(app["store_id"])]


def store_url(app, campaign="site"):
    return f'{S(app)["url"]}?utm_source=loveikolabs&utm_medium=web&utm_campaign={campaign}-{app["slug"]}'


def rating_str(app):
    s = S(app)
    return f'{s["rating"]:.1f}' if s["count"] else None


def totals():
    rated = [S(a) for a in APPS if S(a)["count"]]
    n = sum(s["count"] for s in rated)
    avg = sum(s["rating"] * s["count"] for s in rated) / n if n else 0
    return n, avg


# ───────────────────────────── shared chrome ─────────────────────────────
def logo_svg(uid):
    return (f'<svg viewBox="0 0 32 32" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#14b8a6"/><stop offset=".38" stop-color="#3b82f6"/><stop offset=".7" stop-color="#8b5cf6"/>'
            '<stop offset="1" stop-color="#fb7185"/></linearGradient></defs>'
            '<rect width="32" height="32" rx="9" fill="#0e1116"/><rect x=".5" y=".5" width="31" height="31" rx="8.5" fill="none" stroke="#fff" stroke-opacity=".12"/>'
            '<path d="M9.5 9v13.5h5.5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M18.5 9v13.5H24" fill="none" stroke="url(#{uid})" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')


NAV_LABEL = {"health": "Health", "baby": "Pregnancy &amp; Baby", "resale": "Resale", "home": "Home &amp; Style"}


def nav(active=None):
    cur = ' aria-current="page"'
    items = "".join(
        f'<li><a href="/{h["slug"]}/"{cur if active == h["key"] else ""}><i style="background:var(--{h["key"]})"></i>{NAV_LABEL[h["key"]]}</a></li>'
        for h in HUBS)
    items += f'<li><a href="/guides/"{cur if active == "guides" else ""}>Guides</a></li>'
    items += f'<li><a href="/about/"{cur if active == "about" else ""}>About</a></li>'
    return f'''<a class="ll-skip" href="#main">Skip to content</a>
<header class="ll-nav">
  <div class="ll-nav__inner">
    <a class="ll-logo" href="/" aria-label="Loveiko Labs home">{logo_svg("llg-nav")}<span class="ll-logo__text">Loveiko <span>Labs</span></span></a>
    <button class="ll-nav__toggle" type="button" aria-expanded="false" aria-controls="ll-menu" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <div class="ll-nav__menu" id="ll-menu">
      <ul class="ll-nav__links">{items}</ul>
      <a class="ll-nav__cta" href="/apps/">All {len(APPS)} apps</a>
    </div>
  </div>
</header>'''


def footer(extra_col="", legal=None):
    def col(key):
        h = HUB[key]
        lis = "".join(f'<li><a href="/apps/{a["slug"]}/">{e(a["name"])}</a></li>' for a in APPS if a["hub"] == key)
        return f'<div><strong><a href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")}</a></strong><ul>{lis}</ul></div>'
    legal = legal or "App Store and iPhone are trademarks of Apple Inc. Brand names are used for identification only."
    return f'''<footer class="ll-footer">
  <div class="ll-footer__grid">
    <div>
      <a class="ll-logo" href="/" aria-label="Loveiko Labs home">{logo_svg("llg-foot")}<span class="ll-logo__text ll-footer__brand">Loveiko <span>Labs</span></span></a>
      <p>Independent iOS studio making focused apps for health, family, resale and the home. Pattaya, Thailand.</p>
    </div>
    {col("health")}
    {col("resale")}
    <div>{col("baby")[5:-6]}<strong style="margin-top:22px"><a href="/home-style/">Home &amp; Style</a></strong><ul>{"".join(f'<li><a href="/apps/{a["slug"]}/">{e(a["name"])}</a></li>' for a in APPS if a["hub"] == "home")}</ul></div>
    {extra_col or '<div><strong><a href="/guides/">Guides</a></strong><ul>' + "".join(f'<li><a href="/guides/#{h["slug"]}">{h["name"].replace("&", "&amp;")} guides</a></li>' for h in HUBS) + '</ul></div>'}
    <div>
      <strong>Studio</strong>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/editorial-policy/">Editorial policy</a></li>
        <li><a href="/apps/">All apps</a></li>
        <li><a href="{DEV_URL}" rel="noopener">App Store page</a></li>
        <li><a href="mailto:{EMAIL}">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="ll-footer__legal"><p>{legal}</p><p>© {TODAY.year} Loveiko Labs</p></div>
</footer>'''


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">')
HEAD_COMMON = ('<meta name="theme-color" content="#fafaf7" media="(prefers-color-scheme: light)">\n'
               '<meta name="theme-color" content="#0b0c0f" media="(prefers-color-scheme: dark)">\n'
               '<meta name="color-scheme" content="light dark">\n'
               '<script>document.documentElement.classList.add(\'js\')</script>')
FAVICON = ('<link rel="icon" href="/icons/favicon.svg" type="image/svg+xml">\n'
           '<link rel="icon" href="/icons/favicons/favicon-32x32.png?v=6" sizes="32x32" type="image/png">\n'
           '<link rel="apple-touch-icon" href="/icons/favicons/apple-touch-icon.png?v=6">')


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + "\n</script>"


def page(path, title, desc, body, schema=(), theme="", active=None, og_title=None):
    url = SITE + path
    og = SITE + "/icons/og-image.jpg"
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{HEAD_COMMON}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Loveiko Labs">
<meta property="og:title" content="{e(og_title or title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_title or title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
{FAVICON}
{FONTS}
<link rel="stylesheet" href="/styles.css?v=3">
{chr(10).join(ld(s) for s in schema)}
</head>
<body class="{theme}">
{nav(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/site.js?v=3" defer></script>
</body>
</html>
'''
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head)
    print("wrote", out.relative_to(ROOT))


# ───────────────────────────── components ─────────────────────────────
def icon(app, size=64, cls=""):
    return f'<img src="/icons/sm/{app["slug"]}.jpg" alt="{e(app["name"])} app icon" width="{size}" height="{size}" loading="lazy" decoding="async"{f" class={cls}" if cls else ""}>'


def stars_meta(app):
    r = rating_str(app)
    if not r:
        return '<span>New on the App Store</span>'
    return f'<span class="stars">★</span><span>{r}</span><span>· {S(app)["count"]} ratings</span>'


def app_card(app, large=False):
    h = HUB[app["hub"]]
    if large:
        return f'''<article class="ll-app ll-app--lg t-{h["key"]}" data-hub="{h["key"]}">
  {icon(app, 80)}
  <div class="ll-app__body">
    <h3 class="ll-app__name">{e(app["name"])} <span class="ll-app__tag">{e(app["tag"])}</span></h3>
    <p>{e(app["tagline"])}</p>
    <div class="ll-app__meta">{stars_meta(app)}</div>
    <div class="ll-app__links">
      <a class="is-primary" href="/apps/{app["slug"]}/">About {e(app["name"])}</a>
      <a href="/{app["guide"]}/">Compare alternatives</a>
      <a href="{store_url(app, "hub")}" rel="noopener" target="_blank">App Store ↗</a>
    </div>
  </div>
</article>'''
    return f'''<a class="ll-app t-{h["key"]}" data-hub="{h["key"]}" href="/apps/{app["slug"]}/">
  {icon(app)}
  <div class="ll-app__body">
    <span class="ll-app__name">{e(app["name"])} <span class="ll-app__tag">{e(app["tag"])}</span></span>
    <p>{e(app["tagline"])}</p>
    <div class="ll-app__meta">{stars_meta(app)}</div>
  </div>
</a>'''


def hub_apps(key):
    return [a for a in APPS if a["hub"] == key]


def guides_block(keys=None, heading=True):
    keys = keys or [h["key"] for h in HUBS]
    cols = []
    for k in keys:
        h = HUB[k]
        lis = "".join(f'<li><a href="/{a["guide"]}/">{e(a["guide_title"])}</a></li>' for a in hub_apps(k))
        cols.append(f'<div class="t-{k}" id="{h["slug"]}"><h3><i></i>{h["name"].replace("&", "&amp;")}</h3><ul>{lis}</ul></div>')
    return f'<div class="ll-guides ll-stagger">{"".join(cols)}</div>'


def faq_html(items):
    return '<div class="ll-faq">' + "".join(
        f'<details><summary>{e(q)}</summary><div class="ll-faq__a"><p>{e(a)}</p></div></details>' for q, a in items) + "</div>"


def faq_ld(items, url):
    return {"@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#faq",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}


def crumbs_html(trail):
    parts = [f'<a href="{p}">{n.replace("&", "&amp;")}</a>' for n, p in trail[:-1]] + [trail[-1][0].replace("&", "&amp;")]
    return '<nav class="ll-breadcrumb" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def app_ld(app):
    s = S(app)
    o = {"@type": "MobileApplication", "@id": f"{SITE}/apps/{app['slug']}/#app", "name": s["trackName"], "alternateName": app["name"],
         "operatingSystem": f"iOS {s['minOS']}+", "url": f"{SITE}/apps/{app['slug']}/", "downloadUrl": s["url"],
         "description": app["tagline"], "image": f"{SITE}/icons/{app['slug']}.jpeg",
         "applicationCategory": "HealthApplication" if app["hub"] == "health" else "LifestyleApplication",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "author": {"@id": SITE + "/#organization"}}
    if s["count"]:
        o["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": rating_str(app), "ratingCount": s["count"], "bestRating": 5, "worstRating": 1}
    return o


ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#organization", "name": "Loveiko Labs",
       "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/icons/logo-mark.png", "width": 512, "height": 512},
       "description": "Independent iOS app studio in Pattaya, Thailand, making focused apps for health tracking, pregnancy and baby, resale valuation and the home.",
       "foundingDate": "2024", "founder": {"@type": "Person", "@id": SITE + "/about/#founder", "name": FOUNDER, "jobTitle": "Founder"},
       "address": {"@type": "PostalAddress", "addressLocality": "Pattaya", "addressCountry": "TH"},
       "email": EMAIL, "sameAs": [DEV_URL]}


# ───────────────────────────── homepage ─────────────────────────────
def build_home():
    n_ratings, avg = totals()
    posters = []
    for i, (slug, idx) in enumerate(HERO_POSTERS):
        a = APP[slug]; h = HUB[a["hub"]]
        shots = S(a)["screenshots"]
        src = shots[min(idx, len(shots) - 1)]
        posters.append(f'''<figure class="ll-poster t-{h["key"]}" data-name="{e(a["name"])}" data-pos="{"0" if i == 0 else "hide"}">
          <img src="{src}" alt="{e(a["name"])} App Store screenshot" width="460" height="1000" {"fetchpriority=high" if i == 0 else 'loading="lazy"'} decoding="async">
          <figcaption>{icon(a, 24)}{e(a["name"])}<small style="color:var(--accent-ink);background:var(--accent-soft)">{h["name"].split(" ")[0]}</small></figcaption>
        </figure>''')
    orbit_slugs = ["folik", "pestsnap", "bumpcheck", "snapflip", "hepatica", "calibrum"]
    orbit = "".join(f'<img src="/icons/sm/{s}.jpg" alt="" width="64" height="64" decoding="async">' for s in orbit_slugs)

    tiles = []
    for h in HUBS:
        apps = hub_apps(h["key"])
        tiles.append(f'''<a class="ll-hub-tile t-{h["key"]}" href="/{h["slug"]}/">
        <div>
          <div class="ll-hub-tile__top"><span class="ll-hub-tile__count">{len(apps)} app{"s" if len(apps) > 1 else ""}</span>
          <span class="ll-hub-tile__arrow" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
          <h3>{h["name"].replace("&", "&amp;")}</h3>
          <p>{e(h["short"])}</p>
        </div>
        <div class="ll-icons">{"".join(icon(a, 52) for a in apps)}</div>
      </a>''')

    chips = '<button class="ll-chip" type="button" data-filter="all" aria-pressed="true">All apps</button>' + "".join(
        f'<button class="ll-chip" type="button" data-filter="{h["key"]}" aria-pressed="false"><i style="background:var(--{h["key"]})"></i>{h["name"].replace("&", "&amp;")}</button>' for h in HUBS)

    body = f'''
<section class="ll-home-hero">
  <div class="ll-aura" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="ll-wrap ll-home-hero__grid">
    <div class="ll-enter">
      <a class="ll-badge" href="/about/"><b>Independent</b> iOS studio · Pattaya, Thailand</a>
      <h1>{len(APPS)} focused iPhone apps for health, family, resale <em>and home.</em></h1>
      <p class="ll-home-hero__sub">Loveiko Labs is an independent iOS studio. Each of our apps solves one specific problem, like tracking a condition, checking an ingredient or valuing a watch, and says plainly what it can't do.</p>
      <div class="ll-home-hero__cta">
        <a class="ll-btn" href="#hubs">Explore the apps <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>
        <a class="ll-btn ll-btn--ghost" href="/about/">How we build</a>
      </div>
      <div class="ll-trust">
        <div><strong>{avg:.1f}★</strong><span>average across {n_ratings} App Store ratings</span></div>
        <div><strong>{len(APPS)}</strong><span>apps in {len(HUBS)} categories</span></div>
        <div><strong>168</strong><span>App Store countries</span></div>
      </div>
    </div>
    <div class="ll-stage" aria-roledescription="carousel" aria-label="App Store screenshots">
      <div class="ll-orbit" aria-hidden="true">{orbit}</div>
      <div class="ll-stage__ring">{"".join(posters)}</div>
      <div class="ll-stage__dots"></div>
    </div>
  </div>
</section>

<section class="ll-band" id="hubs">
  <div class="ll-wrap">
    <div class="ll-head ll-reveal">
      <div><p class="ll-kicker">Four categories</p><h2 class="ll-h2">Find the app for <em>your</em> problem.</h2></div>
      <p>Every category has its own page with the apps, honest comparisons with alternatives and answers to the questions people ask most.</p>
    </div>
    <div class="ll-hubs ll-stagger">{"".join(tiles)}</div>
  </div>
</section>

<section class="ll-band ll-band--alt" id="apps">
  <div class="ll-wrap">
    <div class="ll-head ll-reveal">
      <div><p class="ll-kicker">The catalogue</p><h2 class="ll-h2">All {len(APPS)} apps</h2></div>
      <p>Free to download on iPhone. Each app page covers what it does, who it is for, pricing and what it does not do.</p>
    </div>
    <div class="ll-chips" role="group" aria-label="Filter apps by category">{chips}</div>
    <div class="ll-apps">{"".join(app_card(a) for a in APPS)}</div>
  </div>
</section>

<section class="ll-band" id="guides">
  <div class="ll-wrap">
    <div class="ll-head ll-reveal">
      <div><p class="ll-kicker">Buyer's guides</p><h2 class="ll-h2">Compare before you <em>download</em>.</h2></div>
      <p>Side-by-side rankings of the best iOS apps in each category, competitors included. We make one app in every list, and each guide says so up front.</p>
    </div>
    {guides_block()}
  </div>
</section>

<section class="ll-band ll-band--alt" id="principles">
  <div class="ll-wrap">
    <div class="ll-head ll-reveal">
      <div><p class="ll-kicker">How we build</p><h2 class="ll-h2">Four rules every app follows.</h2></div>
    </div>
    <div class="ll-principles ll-stagger">
      <div class="ll-principle"><h3>One job, done well</h3><p>Each app answers one specific question. If a feature does not help answer it, it does not ship.</p></div>
      <div class="ll-principle"><h3>Honest about limits</h3><p>Every app page says what the app is not: not a diagnosis, not a certified appraisal, not a guarantee.</p></div>
      <div class="ll-principle"><h3>Grounded in sources</h3><p>Health and reference answers lean on published guidance such as NIH, FDA and clinical societies, and documented brand references.</p></div>
      <div class="ll-principle"><h3>Private by default</h3><p>Most apps need no account, and records stay on your iPhone wherever the feature allows it.</p></div>
    </div>
  </div>
</section>

<section class="ll-band" id="studio">
  <div class="ll-wrap ll-split">
    <div class="ll-reveal">
      <p class="ll-kicker">The studio</p>
      <h2 class="ll-h2">Small, independent and <em>focused</em>.</h2>
      <div class="ll-prose">
        <p>Loveiko Labs was founded in 2024 by {FOUNDER}. It is self-funded, with no agency work and no investor roadmap: just apps, shipped and refined in public on the App Store.</p>
        <p>Read about <a href="/about/">how the studio works</a> and the <a href="/editorial-policy/">editorial policy</a> behind our guides and health pages.</p>
      </div>
    </div>
    <dl class="ll-facts ll-reveal">
      <div><dt>Founder</dt><dd>{FOUNDER}</dd></div>
      <div><dt>Based in</dt><dd>Pattaya, Thailand</dd></div>
      <div><dt>Apps live</dt><dd>{len(APPS)} on iOS</dd></div>
      <div><dt>Contact</dt><dd><a href="mailto:{EMAIL}" style="text-decoration:none">Email us</a></dd></div>
    </dl>
  </div>
</section>

<section class="ll-wrap">
  <div class="ll-cta-band ll-reveal">
    <h2>Have a question, a partnership or <em>an idea?</em></h2>
    <p style="margin:-10px auto 26px;max-width:52ch">Email is the fastest way to reach the studio. We usually reply within a day.</p>
    <div class="ll-hero__cta" style="margin:0">
      <a class="ll-btn" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="ll-btn ll-btn--ghost" href="{DEV_URL}" rel="noopener" target="_blank">See us on the App Store ↗</a>
    </div>
  </div>
</section>
'''
    schema = [
        ORG,
        {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Loveiko Labs",
         "publisher": {"@id": SITE + "/#organization"}, "inLanguage": "en"},
        {"@context": "https://schema.org", "@type": "ItemList", "name": "Loveiko Labs iOS apps", "numberOfItems": len(APPS),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": app_ld(a)} for i, a in enumerate(APPS)]},
    ]
    page("/", "Loveiko Labs — focused iPhone apps for health, family, resale and home",
         f"Independent iOS studio with {len(APPS)} focused apps: health trackers for GLP-1, TRT, PCOS, eczema and more; pregnancy and baby tools; watch, jewelry and handbag valuation; and home and style helpers.",
         body, schema, og_title="Loveiko Labs — focused iPhone apps")


# ───────────────────────────── hub pages ─────────────────────────────
def build_hub(h):
    apps = hub_apps(h["key"])
    url = f'{SITE}/{h["slug"]}/'
    trail = [("Loveiko Labs", "/"), (h["name"], f'/{h["slug"]}/')]
    others = "".join(f'<a class="t-{o["key"]}" href="/{o["slug"]}/">{o["name"].replace("&", "&amp;")}<span>{len(hub_apps(o["key"]))} apps →</span></a>' for o in HUBS if o["key"] != h["key"])
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <div class="ll-icons">{"".join(icon(a, 60) for a in apps)}</div>
    <p class="ll-eyebrow">{h["eyebrow"].replace("&", "&amp;")}</p>
    <h1>{h["h1"]}</h1>
    <div class="ll-prose">{"".join(f"<p>{e(p)}</p>" for p in h["intro"])}</div>
    <p class="ll-updated">Last reviewed {TODAY_H} · <a href="/editorial-policy/" style="color:inherit">Editorial policy</a></p>
  </section>

  <section class="ll-section" id="apps">
    <p class="ll-kicker">The apps</p>
    <h2>{h["title"]} by Loveiko Labs</h2>
    <div class="ll-apps ll-stagger" style="margin-top:28px">{"".join(app_card(a, large=True) for a in apps)}</div>
  </section>

  <section class="ll-section ll-reveal" id="guides">
    <p class="ll-kicker">Compare</p>
    <h2>Independent comparisons, <em>competitors included</em></h2>
    <p>Each guide ranks the best iOS apps for one need, explains where competitors are the better pick, and discloses that we make one of the apps on the list.</p>
    <div class="ll-related">{"".join(f'<a class="ll-related-card" href="/{a["guide"]}/"><h3>{e(a["guide_title"])} →</h3><p>How {e(a["name"])} compares with the alternatives on features, price and limits.</p></a>' for a in apps)}</div>
  </section>

  <section class="ll-section ll-reveal" id="faq">
    <p class="ll-kicker">Questions</p>
    <h2>Frequently asked questions</h2>
    {faq_html(h["faq"])}
  </section>

  <section class="ll-section ll-reveal">
    <p class="ll-kicker">More from the studio</p>
    <h2>Other categories</h2>
    <div class="ll-hub-links" style="margin-top:24px">{others}</div>
  </section>
</div>
'''
    schema = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url, "url": url, "name": f'{h["title"]} — Loveiko Labs',
         "description": h["meta"], "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"},
         "dateModified": TODAY_ISO, "inLanguage": "en",
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(apps),
                        "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": app_ld(a)} for i, a in enumerate(apps)]}},
        crumbs_ld(trail),
        faq_ld(h["faq"], url),
    ]
    page(f'/{h["slug"]}/', f'{h["title"]} for iPhone — {", ".join(a["name"] for a in apps)} | Loveiko Labs' if len(apps) <= 4 else f'{h["title"]} for iPhone — {len(apps)} focused trackers | Loveiko Labs',
         h["meta"], body, schema, theme=f't-{h["key"]}', active=h["key"])


# ───────────────────────────── apps index / guides index ─────────────────────────────
def build_apps_index():
    trail = [("Loveiko Labs", "/"), ("Apps", "/apps/")]
    sections = "".join(f'''
  <section class="ll-section t-{h["key"]}" id="{h["slug"]}">
    <p class="ll-kicker">{h["name"].replace("&", "&amp;")}</p>
    <h2><a href="/{h["slug"]}/" style="text-decoration:none;color:inherit">{h["title"]} →</a></h2>
    <div class="ll-apps ll-stagger" style="margin-top:24px">{"".join(app_card(a) for a in hub_apps(h["key"]))}</div>
  </section>''' for h in HUBS)
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <p class="ll-eyebrow">The catalogue · {len(APPS)} apps</p>
    <h1>Every Loveiko Labs app, <em>by category</em>.</h1>
    <div class="ll-prose"><p>{len(APPS)} focused iPhone apps across health, pregnancy and baby, resale and valuation, and home and style. All are free to download and each page lists what the app does not do.</p></div>
  </section>
  {sections}
</div>'''
    schema = [crumbs_ld(trail), {"@context": "https://schema.org", "@type": "ItemList", "name": "All Loveiko Labs apps", "numberOfItems": len(APPS),
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE}/apps/{a["slug"]}/', "name": a["name"]} for i, a in enumerate(APPS)]}]
    page("/apps/", f"All {len(APPS)} Loveiko Labs iPhone apps by category | Loveiko Labs",
         f"The full Loveiko Labs catalogue: {len(APPS)} focused iPhone apps for health tracking, pregnancy and baby, resale and valuation, and home and style.", body, schema)


def build_guides_index():
    trail = [("Loveiko Labs", "/"), ("Guides", "/guides/")]
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <p class="ll-eyebrow">Buyer's guides · {len(APPS)} comparisons</p>
    <h1>The best iOS apps for each need, <em>ranked honestly</em>.</h1>
    <div class="ll-prose">
      <p>Every guide compares the leading iPhone apps for one specific need on features, price, privacy and limits. We make one app in each list; it is disclosed at the top of every guide, along with the places where a competitor is the better choice.</p>
      <p>How we research and update these pages is described in our <a href="/editorial-policy/">editorial policy</a>.</p>
    </div>
  </section>
  <section class="ll-section">{guides_block()}</section>
</div>'''
    schema = [crumbs_ld(trail), {"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE + "/guides/", "name": "Loveiko Labs buyer's guides",
              "hasPart": [{"@type": "Article", "headline": a["guide_title"], "url": f'{SITE}/{a["guide"]}/'} for a in APPS]}]
    page("/guides/", "Best iPhone app guides 2026 — honest comparisons | Loveiko Labs",
         "Side-by-side comparisons of the best iOS apps for GLP-1, TRT, PCOS, eczema, pregnancy, baby cry, watch, jewelry and handbag checks, pests, roofing and colour analysis.",
         body, schema, active="guides")


# ───────────────────────────── about / editorial ─────────────────────────────
def build_about():
    trail = [("Loveiko Labs", "/"), ("About", "/about/")]
    hubs = "".join(f'''<div class="t-{h["key"]}"><h3 style="display:flex;align-items:center;gap:8px;margin-bottom:12px"><i style="width:8px;height:8px;border-radius:50%;background:var(--accent)"></i><a href="/{h["slug"]}/" style="text-decoration:none;color:inherit">{h["name"].replace("&", "&amp;")}</a></h3>
      <div class="ll-apps" style="grid-template-columns:1fr">{"".join(app_card(a) for a in hub_apps(h["key"]))}</div></div>''' for h in HUBS)
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <p class="ll-eyebrow">Independent iOS studio · since 2024</p>
    <h1>One problem, one app, <em>one honest answer</em>.</h1>
    <div class="ll-prose"><p>Loveiko Labs is an independent iOS studio building focused, single-purpose apps. Each one answers one specific, real-world question and ends when that question is answered clearly, with the next step you can actually take. {len(APPS)} apps are live on the App Store in 168 countries.</p></div>
  </section>

  <section class="ll-section ll-split" id="studio">
    <div class="ll-reveal">
      <p class="ll-kicker">The studio</p>
      <h2 class="ll-h2">A small studio with a <em>narrow</em> definition of done.</h2>
      <div class="ll-prose">
        <p>Loveiko Labs was founded in 2024 by {FOUNDER}. It is independent and self-funded: no agency work, no investor roadmap, no feature padding.</p>
        <p>Most apps try to do everything. We do the opposite. Every app starts with a single question (is this gold real, is this ingredient okay in pregnancy, why is the baby crying, what do these liver numbers mean) and a feature ships only if it helps answer it.</p>
      </div>
    </div>
    <dl class="ll-facts ll-reveal" id="founder">
      <div><dt>Founder</dt><dd>{FOUNDER}</dd></div>
      <div><dt>Founded</dt><dd>2024</dd></div>
      <div><dt>Based in</dt><dd>Pattaya, Thailand</dd></div>
      <div><dt>Platform</dt><dd>iPhone · iOS 17+</dd></div>
    </dl>
  </section>

  <section class="ll-section" id="principles">
    <p class="ll-kicker">How we build</p>
    <h2>Principles we don't break</h2>
    <div class="ll-principles ll-stagger" style="margin-top:28px">
      <div class="ll-principle"><h3>One job, done well</h3><p>Snap, scan, log or record, and get a structured answer fast. No dashboards to learn.</p></div>
      <div class="ll-principle"><h3>Honest about limits</h3><p>No app here claims a certification, guarantee or affiliation it does not have. Every product page carries scope and limitation notes.</p></div>
      <div class="ll-principle"><h3>Grounded in sources</h3><p>Where an app touches health or authentication, its AI leans on public reference material (NIH, FDA, RxNav, clinical society guidance, documented brand references) and says so.</p></div>
      <div class="ll-principle"><h3>Private by default</h3><p>Camera and audio processing stays on-device or in a private request wherever possible. We collect only what an app needs to work.</p></div>
    </div>
  </section>

  <section class="ll-section" id="apps">
    <p class="ll-kicker">The portfolio</p>
    <h2>{len(APPS)} apps, {len(APPS)} specific problems</h2>
    <div class="ll-guides" style="margin-top:28px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">{hubs}</div>
  </section>

  <section class="ll-section" id="contact">
    <p class="ll-kicker">Contact</p>
    <h2>Get in touch</h2>
    <p>Press, partnerships, corrections or a question about one of the apps: email is the fastest way to reach the studio.</p>
    <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a><br><strong>App Store:</strong> <a href="{DEV_URL}" rel="noopener">{FOUNDER} developer page</a></p>
  </section>
</div>'''
    schema = [ORG, crumbs_ld(trail), {"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/about/", "name": "About Loveiko Labs",
              "mainEntity": {"@id": SITE + "/#organization"}},
              {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "/about/#founder", "name": FOUNDER, "jobTitle": "Founder, Loveiko Labs",
               "worksFor": {"@id": SITE + "/#organization"}, "sameAs": [DEV_URL]}]
    page("/about/", "About Loveiko Labs — independent iOS studio | Loveiko Labs",
         f"Loveiko Labs is an independent iOS studio founded in 2024 by {FOUNDER} in Pattaya, Thailand, building {len(APPS)} focused apps for health, family, resale and home.",
         body, schema, active="about")


def build_editorial():
    trail = [("Loveiko Labs", "/"), ("Editorial policy", "/editorial-policy/")]
    sections = [
        ("Who writes these pages", f"App pages, hub pages and buyer's guides are written and maintained by the Loveiko Labs studio, led by founder {FOUNDER}. We are app developers, not clinicians, appraisers or authenticators, and we write from that position."),
        ("Disclosure", "We make one app in every buyer's guide. Each guide says so at the top. Where a competitor is cheaper, more established or better suited to a specific need, the guide says that too. We do not accept payment for placement and we do not use affiliate links."),
        ("Sources", "Health pages rely on published guidance from public bodies and clinical societies, such as the FDA, NIH, CDC, ACOG, Mayo Clinic and specialty society guidelines, and on each app's own documented behaviour. Valuation and authentication pages rely on documented brand references and public market data. Competitor details come from their App Store listings at the time of writing."),
        ("Health information", "Nothing on this site is medical advice. Our health apps organise your own records, explain terms and numbers on your own reports and help you prepare for appointments. They do not diagnose or treat any condition. Talk to your clinician before changing medication, supplements or diet."),
        ("Authenticity and valuation", "Photo-based checks are a screening step, not certified authentication or a formal appraisal. For high-value purchases, insurance or sale, use a qualified professional who can inspect the item in person."),
        ("Ratings and numbers", "App Store ratings shown on this site are taken from Apple's public data and refreshed when pages are rebuilt. Prices are in US dollars as listed on the US App Store and may differ by country."),
        ("Updates and corrections", f"We review hub pages and guides when apps or competitors change, and the review date is shown on each hub page. If you spot an error, email {EMAIL} and we will correct it."),
    ]
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <p class="ll-eyebrow">Editorial policy</p>
    <h1>How we write about <em>our apps</em> and the alternatives.</h1>
    <div class="ll-prose"><p>This page explains who writes the content on loveikolabs.com, where the information comes from, and how we handle disclosure, health topics and corrections.</p></div>
    <p class="ll-updated">Last updated {TODAY_H}</p>
  </section>
  {"".join(f'<section class="ll-section"><h2>{e(t)}</h2><p>{e(p)}</p></section>' for t, p in sections)}
</div>'''
    page("/editorial-policy/", "Editorial policy | Loveiko Labs",
         "How Loveiko Labs writes its app pages and buyer's guides: authorship, disclosure, sources, health information, ratings and corrections.",
         body, [crumbs_ld(trail)])


# ───────────────────────────── patch existing pages ─────────────────────────────
NAV_RE = re.compile(r'(?:<a class="ll-skip"[^>]*>[^<]*</a>\s*)?<header class="ll-nav">.*?</header>', re.S)
FOOT_RE = re.compile(r'<footer class="ll-footer">.*?</footer>', re.S)
CURSOR_RE = re.compile(r'\s*<div class="ll-cursor(?:-ring)?" aria-hidden="true"></div>')
SCRIPT_RE = re.compile(r'<script>\s*/\* scroll reveal \*/.*?</script>|<script src="/site\.js[^"]*" defer></script>', re.S)
CRUMB_RE = re.compile(r'<nav class="ll-breadcrumb" aria-label="Breadcrumb">.*?</nav>', re.S)
CRUMB_LD_RE = re.compile(r'\n?<script type="application/ld\+json" id="ll-crumbs">.*?</script>', re.S)
FONTS_RE = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">', re.S)
THEME_RE = re.compile(r'<meta name="theme-color"[^>]*>\s*(?:<meta name="theme-color"[^>]*>\s*)?(?:<meta name="color-scheme"[^>]*>\s*)?(?:<script>document\.documentElement\.classList\.add\(\'js\'\)</script>\s*)?')
CSS_RE = re.compile(r'<link rel="stylesheet" href="/styles\.css[^"]*">')
BODY_RE = re.compile(r'<body[^>]*>')
FAKE_QUOTES_RE = re.compile(r'\s*<p><strong>What users praise(?: in reviews)?:</strong>.*?</p>', re.S)


def legal_from(old_footer):
    m = re.search(r'<p class="ll-footer__legal">(.*?)</p>', old_footer, re.S)
    if not m:
        return None
    t = re.sub(r"©\s*\d{4}\s*Loveiko Labs\.?\s*", "", m.group(1)).strip()
    return t or None


def app_col(old_footer, fallback_title, links):
    """Keep the page-specific column (e.g. 'WatchSnap' anchors + guide link)."""
    m = re.findall(r'<div>\s*<strong>([^<]*)</strong>\s*(<ul>.*?</ul>)\s*</div>', old_footer, re.S)
    for title, ul in m:
        if title.strip() not in ("Studio", "Loveiko Labs"):
            return f'<div><strong>{title.strip()}</strong>{ul}</div>'
    return f'<div><strong>{fallback_title}</strong><ul>{links}</ul></div>'


def patch_common(s, theme, trail, extra_col, legal_default=None):
    old_footer = (FOOT_RE.search(s) or [""])[0] if FOOT_RE.search(s) else ""
    legal = legal_from(old_footer) if old_footer else legal_default
    s = CURSOR_RE.sub("", s)
    s = NAV_RE.sub(lambda _: nav(None), s, count=1)
    s = FOOT_RE.sub(lambda _: footer(extra_col, legal), s, count=1)
    s = SCRIPT_RE.sub('<script src="/site.js?v=3" defer></script>', s)
    s = FONTS_RE.sub(FONTS, s, count=1)
    s = THEME_RE.sub(HEAD_COMMON + "\n", s, count=1)
    s = CSS_RE.sub('<link rel="stylesheet" href="/styles.css?v=3">', s, count=1)
    s = BODY_RE.sub(f'<body class="{theme}">', s, count=1)
    s = CRUMB_RE.sub(lambda _: crumbs_html(trail), s, count=1)
    s = CRUMB_LD_RE.sub("", s)
    crumb_ld = '\n<script type="application/ld+json" id="ll-crumbs">\n' + json.dumps(crumbs_ld(trail), ensure_ascii=False) + "\n</script>"
    s = s.replace("</head>", crumb_ld + "\n</head>", 1)
    if '<main class="ll-page">' in s:
        s = s.replace('<main class="ll-page">', '<main class="ll-page" id="main">', 1)
    return s


def patch_ratings(s, app):
    st = S(app)
    r = rating_str(app)
    # schema: the page's own MobileApplication rating (first aggregateRating in the file)
    agg = re.compile(r'("aggregateRating"\s*:\s*\{[^}]*?"ratingValue"\s*:\s*)"?[\d.]+"?([^}]*?"ratingCount"\s*:\s*)"?\d+"?', re.S)
    if r:
        s = agg.sub(lambda m: f'{m.group(1)}"{r}"{m.group(2)}"{st["count"]}"', s, count=1)
        s = re.sub(r'(<div class="ll-hero__rating">).*?(</div>)',
                   lambda m: f'{m.group(1)}\n      <span class="stars">★★★★★</span> <span>{r}</span> <span class="muted">· {st["count"]} ratings on the App Store</span>\n    {m.group(2)}', s, count=1, flags=re.S)
        old_counts = set()

        def td(m):
            old_counts.add(m.group(2))
            return f'{m.group(1)}{r}★ ({st["count"]} ratings){m.group(3)}'
        s = re.sub(r'(<td class="is-us">)~?\d\.\d+★\s*(?:\(|·)\s*(\d+)(?: ratings)?\)?(</td>)', td, s)

        def prose(m):
            old_counts.add(m.group(4))
            return f'{m.group(1)}{r}{m.group(3)}{st["count"]}{m.group(5)}'
        name = re.escape(app["name"])
        s = re.sub(rf'((?:{name}[^.<"]{{0,40}}?|Current App Store rating:\s*))(\d\.\d+)([- ]stars?(?: rating)? from )(\d+)( ratings)', prose, s)
        for c in old_counts - {str(st["count"])}:
            s = s.replace(f" vs {c} ratings", f' vs {st["count"]} ratings')
    return s


def patch_pages():
    for a in APPS:
        h = HUB[a["hub"]]
        # app page
        p = ROOT / "apps" / a["slug"] / "index.html"
        s = p.read_text()
        trail = [("Loveiko Labs", "/"), (h["name"], f'/{h["slug"]}/'), (a["name"], f'/apps/{a["slug"]}/')]
        links = f'<li><a href="/{a["guide"]}/">{e(a["guide_title"])}</a></li><li><a href="/{h["slug"]}/">More {h["name"].replace("&", "&amp;")} apps</a></li>'
        s = patch_common(s, f't-{h["key"]}', trail, app_col(FOOT_RE.search(s).group(0) if FOOT_RE.search(s) else "", e(a["name"]), links))
        s = patch_ratings(s, a)
        p.write_text(s)
        # guide page
        g = ROOT / a["guide"] / "index.html"
        s = g.read_text()
        trail = [("Loveiko Labs", "/"), (h["name"], f'/{h["slug"]}/'), (a["guide_title"], f'/{a["guide"]}/')]
        links = f'<li><a href="/apps/{a["slug"]}/">{e(a["name"])} overview</a></li><li><a href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")} apps</a></li><li><a href="/guides/">All guides</a></li>'
        s = patch_common(s, f't-{h["key"]}', trail, f'<div><strong>Related</strong><ul>{links}</ul></div>')
        s = FAKE_QUOTES_RE.sub("", s)
        g.write_text(s)
    print(f"patched {len(APPS)} app pages + {len(APPS)} guides")


# ───────────────────────────── sitemap / llms.txt ─────────────────────────────
def build_sitemap():
    urls = ["/", "/apps/", "/guides/", "/about/", "/editorial-policy/"] + [f'/{h["slug"]}/' for h in HUBS] + \
           [f'/apps/{a["slug"]}/' for a in APPS] + [f'/{a["guide"]}/' for a in APPS]
    pri = lambda u: "1.0" if u == "/" else "0.9" if u.count("/") == 2 and not u.startswith("/apps/") and not u.startswith("/best-") else "0.8"
    body = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY_ISO}</lastmod><priority>{pri(u)}</priority></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
    print("wrote sitemap.xml:", len(urls), "urls")


def build_llms():
    p = ROOT / "llms.txt"
    s = p.read_text()
    block = ["## Site structure", "",
             f"- Home: {SITE}/", f"- All apps: {SITE}/apps/", f"- Buyer's guides: {SITE}/guides/",
             f"- About: {SITE}/about/", f"- Editorial policy: {SITE}/editorial-policy/", ""]
    for h in HUBS:
        block.append(f'### {h["name"]} — {SITE}/{h["slug"]}/')
        for a in hub_apps(h["key"]):
            r = rating_str(a)
            rt = f' · {r}★ from {S(a)["count"]} App Store ratings' if r else ""
            block.append(f'- {a["name"]}: {a["tagline"]} App page: {SITE}/apps/{a["slug"]}/ · Guide: {SITE}/{a["guide"]}/{rt}')
        block.append("")
    block_s = "\n".join(block).rstrip() + "\n"
    start, end = "<!-- site-structure:start -->", "<!-- site-structure:end -->"
    if start in s:
        s = re.sub(re.escape(start) + r".*?" + re.escape(end), start + "\n" + block_s + end, s, flags=re.S)
    else:
        s = s.replace("\n## About", f"\n{start}\n{block_s}{end}\n\n## About", 1)
    p.write_text(s)
    print("updated llms.txt")


def build_404():
    tiles = "".join(f'<a class="t-{h["key"]}" href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")}<span>{len(hub_apps(h["key"]))} apps →</span></a>' for h in HUBS)
    body = f'''
<div class="ll-wrap">
  <section class="ll-hub-hero" style="padding-top:96px">
    <p class="ll-eyebrow">404</p>
    <h1>This page <em>doesn't exist</em>.</h1>
    <div class="ll-prose"><p>The link may be old or mistyped. Pick a category below or go back to the <a href="/">home page</a>.</p></div>
  </section>
  <section class="ll-section"><div class="ll-hub-links" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{tiles}</div></section>
</div>'''
    page("/404/", "Page not found | Loveiko Labs", "This page does not exist on loveikolabs.com.", body)
    src = ROOT / "404" / "index.html"
    (ROOT / "404.html").write_text(src.read_text().replace('<link rel="canonical" href="https://loveikolabs.com/404/">', '<meta name="robots" content="noindex">'))
    src.unlink(); src.parent.rmdir()
    print("wrote 404.html")


if __name__ == "__main__":
    if "--refresh" in sys.argv or not STORE.exists():
        refresh_store()
    store_data = store()
    build_home()
    for h in HUBS:
        build_hub(h)
    build_apps_index()
    build_guides_index()
    build_about()
    build_editorial()
    build_404()
    patch_pages()
    build_sitemap()
    build_llms()
