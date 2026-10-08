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
from site_data import HUBS, APPS, HERO_POSTERS, SITE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STORE = Path(__file__).parent / "store.json"
TODAY = datetime.date.today()
TODAY_ISO = TODAY.isoformat()
TODAY_H = TODAY.strftime("%B %Y")
DEV_URL = "https://apps.apple.com/us/developer/id1478618306"
ASSET_V = "5"  # bump when styles.css / site.js change (browsers cache them for a day)

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
def logo_svg(uid=None):
    return '<img class="ll-logo__mark" src="/icons/logo-96.png" width="30" height="30" alt="">'



NAV_LABEL = {"health": "Health", "baby": "Pregnancy &amp; Baby", "resale": "Resale", "home": "Home &amp; Style", "mind": "Mind &amp; Faith"}


def nav(active=None):
    cur = ' aria-current="page"'
    hub_on = active in HUB
    cats = "".join(
        f'<a class="t-{h["key"]}" href="/{h["slug"]}/"{cur if active == h["key"] else ""}><i></i><span>{NAV_LABEL[h["key"]]}</span><small>{len(hub_apps(h["key"]))}</small></a>'
        for h in HUBS)
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    items = (f'<li class="ll-drop"><button class="ll-drop__btn{" is-current" if hub_on else ""}" type="button" aria-expanded="false" aria-controls="ll-cats">Categories{chev}</button>'
             f'<div class="ll-drop__panel" id="ll-cats"><p class="ll-drop__label">Categories</p>{cats}</div></li>')
    items += f'<li><a href="/guides/"{cur if active == "guides" else ""}>Guides</a></li>'
    items += f'<li><a href="/about/"{cur if active == "about" else ""}>About</a></li>'
    return f'''<a class="ll-skip" href="#main">Skip to content</a>
<header class="ll-nav">
  <div class="ll-nav__inner">
    <a class="ll-logo" href="/" aria-label="Loveiko Labs home">{logo_svg("llg-nav")}<span class="ll-logo__text">Loveiko <span>Labs</span></span></a>
    <button class="ll-nav__toggle" type="button" aria-expanded="false" aria-controls="ll-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
    <div class="ll-nav__menu" id="ll-menu">
      <ul class="ll-nav__links">{items}</ul>
      <a class="ll-nav__cta" href="/apps/"{cur if active == "apps" else ""}>All {len(APPS)} apps</a>
    </div>
  </div>
</header>'''


def footer(extra_col="", legal=None):
    legal = legal or "App Store and iPhone are trademarks of Apple Inc. Brand names are used for identification only."
    cats = "".join(f'<li><a href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")}</a></li>' for h in HUBS)
    return f'''<footer class="ll-footer">
  <div class="ll-footer__grid">
    <div class="ll-footer__about">
      <a class="ll-logo" href="/" aria-label="Loveiko Labs home">{logo_svg()}<span class="ll-logo__text ll-footer__brand">Loveiko <span>Labs</span></span></a>
      <p>Focused iPhone apps, each built to solve one problem.</p>
    </div>
    <div><strong>Categories</strong><ul>{cats}</ul></div>
    {extra_col}
    <div>
      <strong>Studio</strong>
      <ul>
        <li><a href="/apps/">All apps</a></li>
        <li><a href="/guides/">Buyer's guides</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/editorial-policy/">Editorial policy</a></li>
        <li><a href="{DEV_URL}" rel="noopener">App Store ↗</a></li>
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
FAVICON = ('<link rel="icon" href="/icons/favicons/favicon.ico?v=5" sizes="any">\n'
           '<link rel="icon" href="/icons/favicons/favicon-32x32.png?v=5" sizes="32x32" type="image/png">\n'
           '<link rel="apple-touch-icon" href="/icons/favicons/apple-touch-icon.png?v=5">')


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + "\n</script>"


def page(path, title, desc, body, schema=(), theme="", active=None, og_title=None):
    url = SITE + path
    og = SITE + "/icons/og-image.jpg?v=2"
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
<link rel="stylesheet" href="/styles.css?v={ASSET_V}">
{chr(10).join(ld(s) for s in schema)}
</head>
<body class="{theme}">
{nav(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/site.js?v={ASSET_V}" defer></script>
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
    return f'<span class="stars">★</span><span>{r}</span>'


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


def short_guide(app):
    """Guide title without the trailing year, for compact lists."""
    return re.sub(r"\s+20\d\d$", "", app["guide_title"])


def guides_block(keys=None, heading=True):
    keys = keys or [h["key"] for h in HUBS]
    groups = []
    for k in keys:
        h = HUB[k]
        apps = hub_apps(k)
        lis = "".join(f'<li><a href="/{a["guide"]}/">{icon(a, 28)}<span>{e(short_guide(a))}</span></a></li>' for a in apps)
        groups.append(f'<div class="ll-guides__group t-{k}" id="{h["slug"]}"><h3><i></i>{h["name"].replace("&", "&amp;")}<span>{len(apps)} guide{"s" if len(apps) > 1 else ""}</span></h3><ul>{lis}</ul></div>')
    return f'<div class="ll-guides">{"".join(groups)}</div>'


def featured_guides(n=6):
    """One guide per category (the app with most ratings), topped up by overall rating count."""
    by_count = sorted(APPS, key=lambda a: -S(a)["count"])
    picks = []
    for h in HUBS:
        top = next((a for a in by_count if a["hub"] == h["key"]), None)
        if top:
            picks.append(top)
    picks += [a for a in by_count if a not in picks][:max(0, n - len(picks))]
    cards = "".join(f'''<a class="ll-gcard t-{a["hub"]}" href="/{a["guide"]}/">
        <span class="ll-gcard__cat"><i></i>{HUB[a["hub"]]["name"].replace("&", "&amp;")}</span>
        <span class="ll-gcard__title">{e(short_guide(a))}</span>
        <span class="ll-gcard__foot">{icon(a, 28)}<span>Includes {e(a["name"])}</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
      </a>''' for a in picks[:n])
    return f'<div class="ll-gcards ll-stagger">{cards}</div>'


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
       "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/icons/logo-512.png", "width": 512, "height": 512},
       "description": "iOS app studio making focused iPhone apps for health tracking, pregnancy and baby, resale valuation, the home, prayer and Scripture.",
       "foundingDate": "2024", "sameAs": [DEV_URL]}


# ───────────────────────────── homepage ─────────────────────────────
def build_home():
    _, avg = totals()
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

    newest = sorted(APPS, key=lambda a: S(a).get("released") or "", reverse=True)[:6]

    body = f'''
<section class="ll-home-hero">
  <div class="ll-aura" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="ll-wrap ll-home-hero__grid">
    <div class="ll-enter">
      <h1>{len(APPS)} iPhone apps, each built to solve <em>one problem.</em></h1>
      <p class="ll-home-hero__sub">Track a health condition, check an ingredient in pregnancy, value a watch, keep a Bible verse on your Lock Screen. Each Loveiko Labs app does one job well and says plainly what it can't do.</p>
      <div class="ll-home-hero__cta">
        <a class="ll-btn" href="#hubs">Explore the apps <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>
        <a class="ll-btn ll-btn--ghost" href="/about/">How we build</a>
      </div>
      <div class="ll-trust">
        <div><strong>{avg:.1f}<b aria-hidden="true">★</b></strong><span>App Store rating</span></div>
        <div><strong data-count="{len(APPS)}">{len(APPS)}</strong><span>apps live</span></div>
        <div><strong data-count="168">168</strong><span>countries</span></div>
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
      <div><p class="ll-kicker">{len(HUBS)} categories</p><h2 class="ll-h2">Find the app for <em>your</em> problem.</h2></div>
      <p>Every category has its own page with the apps, honest comparisons with alternatives and answers to the questions people ask most.</p>
    </div>
    <div class="ll-hubs ll-stagger">{"".join(tiles)}</div>
  </div>
</section>

<section class="ll-band ll-band--alt" id="apps">
  <div class="ll-wrap">
    <div class="ll-head ll-reveal">
      <div><p class="ll-kicker">Just shipped</p><h2 class="ll-h2">New on the <em>App Store</em>.</h2></div>
      <p>New apps ship every month. These are the latest; the full catalogue, grouped by category, is on the apps page.</p>
    </div>
    <div class="ll-apps ll-stagger">{"".join(app_card(a) for a in newest)}</div>
    <a class="ll-more" href="/apps/">All {len(APPS)} apps <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
  </div>
</section>

<section class="ll-band" id="guides">
  <div class="ll-wrap">
    <div class="ll-head ll-reveal">
      <div><p class="ll-kicker">Buyer's guides</p><h2 class="ll-h2">Compare before you <em>download</em>.</h2></div>
      <p>Side-by-side rankings of the best iOS apps for one need, competitors included. We make one app in every list, and each guide says so up front.</p>
    </div>
    {featured_guides()}
    <a class="ll-more" href="/guides/">All {len(APPS)} guides <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
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

<section class="ll-wrap">
  <div class="ll-cta-band ll-reveal">
    <h2>One problem, one app. <em>Find yours.</em></h2>
    <p class="ll-cta-band__sub">Every app is free to download on iPhone and live in 168 countries. New ones ship every month.</p>
    <div class="ll-hero__cta ll-cta-band__actions">
      <a class="ll-btn" href="/apps/">Browse all {len(APPS)} apps</a>
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
         f"iOS studio with {len(APPS)} focused iPhone apps: health trackers, pregnancy and baby tools, watch and jewelry valuation, home helpers, prayer and Bible apps.",
         body, schema, og_title="Loveiko Labs — focused iPhone apps")


# ───────────────────────────── hub pages ─────────────────────────────
def hub_shots(apps):
    picks = (apps * 3)[:3]
    seen, imgs = {}, []
    for a in picks:
        k = seen.get(a["slug"], 0); seen[a["slug"]] = k + 1
        shots = S(a)["screenshots"]
        imgs.append(f'<img src="{shots[min(k, len(shots) - 1)]}" alt="" width="460" height="1000" decoding="async">')
    return '<div class="ll-hero__shots" aria-hidden="true">' + "".join(imgs) + "</div>"


def build_hub(h):
    apps = hub_apps(h["key"])
    url = f'{SITE}/{h["slug"]}/'
    trail = [("Loveiko Labs", "/"), (h["name"], f'/{h["slug"]}/')]
    others = "".join(f'<a class="t-{o["key"]}" href="/{o["slug"]}/">{o["name"].replace("&", "&amp;")}<span>{len(hub_apps(o["key"]))} apps →</span></a>' for o in HUBS if o["key"] != h["key"])
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero ll-hub-hero--split">
    <div>
      <div class="ll-icons">{"".join(icon(a, 60) for a in apps)}</div>
      <p class="ll-eyebrow">{h["eyebrow"].replace("&", "&amp;")}</p>
      <h1>{h["h1"]}</h1>
      <div class="ll-prose">{"".join(f"<p>{e(p)}</p>" for p in h["intro"])}</div>
      <p class="ll-updated">Last reviewed {TODAY_H} · <a href="/editorial-policy/" class="ll-plain">Editorial policy</a></p>
    </div>
    {hub_shots(apps)}
  </section>

  <section class="ll-section" id="apps">
    <p class="ll-kicker">The apps</p>
    <h2>{h["title"]} by Loveiko Labs</h2>
    <div class="ll-apps ll-stagger">{"".join(app_card(a, large=True) for a in apps)}</div>
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
    <div class="ll-hub-links">{others}</div>
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
    page(f'/{h["slug"]}/', f'{h["title"].capitalize()} for iPhone | Loveiko Labs',
         h["desc"], body, schema, theme=f't-{h["key"]}', active=h["key"])


# ───────────────────────────── apps index / guides index ─────────────────────────────
def build_apps_index():
    trail = [("Loveiko Labs", "/"), ("Apps", "/apps/")]
    sections = "".join(f'''
  <section class="ll-section t-{h["key"]}" id="{h["slug"]}">
    <p class="ll-kicker">{h["name"].replace("&", "&amp;")}</p>
    <h2><a href="/{h["slug"]}/" class="ll-plain">{h["title"]} →</a></h2>
    <div class="ll-apps ll-stagger">{"".join(app_card(a) for a in hub_apps(h["key"]))}</div>
  </section>''' for h in HUBS)
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <p class="ll-eyebrow">The catalogue · {len(APPS)} apps</p>
    <h1>Every Loveiko Labs app, <em>by category</em>.</h1>
    <div class="ll-prose"><p>{len(APPS)} focused iPhone apps across health, pregnancy and baby, resale and valuation, home and style, and mind and faith. All are free to download and each page lists what the app does not do.</p></div>
  </section>
  {sections}
</div>'''
    schema = [crumbs_ld(trail), {"@context": "https://schema.org", "@type": "ItemList", "name": "All Loveiko Labs apps", "numberOfItems": len(APPS),
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE}/apps/{a["slug"]}/', "name": a["name"]} for i, a in enumerate(APPS)]}]
    page("/apps/", f"All {len(APPS)} Loveiko Labs iPhone apps by category | Loveiko Labs",
         f"The full Loveiko Labs catalogue: {len(APPS)} focused iPhone apps for health tracking, pregnancy and baby, resale and valuation, home and style, and mind and faith.", body, schema, active="apps")


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
         "Honest side-by-side comparisons of the best iPhone apps for GLP-1, TRT, PCOS, eczema, pregnancy, watches, jewelry, pests, prayer, affirmations and more.",
         body, schema, active="guides")


# ───────────────────────────── about / editorial ─────────────────────────────
def build_about():
    trail = [("Loveiko Labs", "/"), ("About", "/about/")]
    body = f'''
<div class="ll-wrap">
  {crumbs_html(trail)}
  <section class="ll-hub-hero">
    <p class="ll-eyebrow">iOS studio · since 2024</p>
    <h1>One problem, one app, <em>one honest answer</em>.</h1>
    <div class="ll-prose"><p>Loveiko Labs builds focused, single-purpose iPhone apps. Each one answers one specific, real-world question and ends when that question is answered clearly, with the next step you can actually take. {len(APPS)} apps are live on the App Store in 168 countries, and the catalogue grows every month.</p></div>
  </section>

  <section class="ll-section ll-split" id="studio">
    <div class="ll-reveal">
      <p class="ll-kicker">The studio</p>
      <h2 class="ll-h2">Many apps, one <em>narrow</em> definition of done.</h2>
      <div class="ll-prose">
        <p>Loveiko Labs started in 2024. It is self-funded: no agency work, no investor roadmap, no feature padding.</p>
        <p>Most apps try to do everything. We do the opposite. Every app starts with a single question (is this gold real, is this ingredient okay in pregnancy, why is the baby crying, what do these liver numbers mean) and a feature ships only if it helps answer it. That is what lets us ship a lot of apps without any of them turning into a dashboard.</p>
      </div>
    </div>
    <dl class="ll-facts ll-reveal">
      <div><dt>Founded</dt><dd>2024</dd></div>
      <div><dt>Apps live</dt><dd>{len(APPS)} on iOS</dd></div>
      <div><dt>Available in</dt><dd>168 countries</dd></div>
      <div><dt>Platform</dt><dd>iPhone · iOS 17+</dd></div>
    </dl>
  </section>

  <section class="ll-section" id="principles">
    <p class="ll-kicker">How we build</p>
    <h2>Principles we don't break</h2>
    <div class="ll-principles ll-stagger">
      <div class="ll-principle"><h3>One job, done well</h3><p>Snap, scan, log or record, and get a structured answer fast. No dashboards to learn.</p></div>
      <div class="ll-principle"><h3>Honest about limits</h3><p>No app here claims a certification, guarantee or affiliation it does not have. Every product page carries scope and limitation notes.</p></div>
      <div class="ll-principle"><h3>Grounded in sources</h3><p>Where an app touches health or authentication, its AI leans on public reference material (NIH, FDA, RxNav, clinical society guidance, documented brand references) and says so.</p></div>
      <div class="ll-principle"><h3>Private by default</h3><p>Camera and audio processing stays on-device or in a private request wherever possible. We collect only what an app needs to work.</p></div>
    </div>
  </section>
</div>'''
    schema = [ORG, crumbs_ld(trail), {"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/about/", "name": "About Loveiko Labs",
              "mainEntity": {"@id": SITE + "/#organization"}}]
    page("/about/", "About Loveiko Labs — iOS app studio | Loveiko Labs",
         f"Loveiko Labs is an iOS studio founded in 2024, building {len(APPS)} focused iPhone apps for health, family, resale, the home, prayer and Scripture, one problem per app.",
         body, schema, active="about")


def build_editorial():
    trail = [("Loveiko Labs", "/"), ("Editorial policy", "/editorial-policy/")]
    sections = [
        ("Who writes these pages", "App pages, hub pages and buyer's guides are written and maintained by the Loveiko Labs team. We are app developers, not clinicians, appraisers or authenticators, and we write from that position."),
        ("Disclosure", "We make one app in every buyer's guide. Each guide says so at the top. Where a competitor is cheaper, more established or better suited to a specific need, the guide says that too. We do not accept payment for placement and we do not use affiliate links."),
        ("Sources", "Health pages rely on published guidance from public bodies and clinical societies, such as the FDA, NIH, CDC, ACOG, Mayo Clinic and specialty society guidelines, and on each app's own documented behaviour. Valuation and authentication pages rely on documented brand references and public market data. Competitor details come from their App Store listings at the time of writing."),
        ("Health information", "Nothing on this site is medical advice. Our health apps organise your own records, explain terms and numbers on your own reports and help you prepare for appointments. They do not diagnose or treat any condition. Talk to your clinician before changing medication, supplements or diet."),
        ("Authenticity and valuation", "Photo-based checks are a screening step, not certified authentication or a formal appraisal. For high-value purchases, insurance or sale, use a qualified professional who can inspect the item in person."),
        ("Ratings and numbers", "App Store ratings shown on this site are taken from Apple's public data and refreshed when pages are rebuilt. Prices are in US dollars as listed on the US App Store and may differ by country."),
        ("Updates and corrections", "We review hub pages and guides when apps or competitors change, and the review date is shown on each hub page. When we find an error, or someone points one out, we correct the page and update that date."),
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
CRUMB_LD_RE = re.compile(r'\s*<script type="application/ld\+json" id="ll-crumbs">.*?</script>', re.S)
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
        if title.strip() not in ("Studio", "Loveiko Labs", "Categories"):
            return f'<div><strong>{title.strip()}</strong>{ul}</div>'
    return f'<div><strong>{fallback_title}</strong><ul>{links}</ul></div>'


def patch_common(s, theme, trail, extra_col, legal_default=None):
    old_footer = (FOOT_RE.search(s) or [""])[0] if FOOT_RE.search(s) else ""
    legal = legal_from(old_footer) if old_footer else legal_default
    s = CURSOR_RE.sub("", s)
    s = NAV_RE.sub(lambda _: nav(None), s, count=1)
    s = FOOT_RE.sub(lambda _: footer(extra_col, legal), s, count=1)
    s = SCRIPT_RE.sub(f'<script src="/site.js?v={ASSET_V}" defer></script>', s)
    s = FONTS_RE.sub(FONTS, s, count=1)
    s = THEME_RE.sub(HEAD_COMMON + "\n", s, count=1)
    s = CSS_RE.sub(f'<link rel="stylesheet" href="/styles.css?v={ASSET_V}">', s, count=1)
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
                   lambda m: f'{m.group(1)}\n      <span class="stars">★★★★★</span> <span>{r}</span> <span class="muted">on the App Store</span>\n    {m.group(2)}', s, count=1, flags=re.S)
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


# ───────────────────────────── layout unification for legacy pages ─────────────────────────────
HERO_RE = re.compile(r'<section class="ll-hero( ll-hero--app| ll-hero--guide)?">(.*?)\n  </section>', re.S)
SHOTS_RE = re.compile(r'<div class="ll-hero__shots"[^>]*>.*?</div><!-- /shots -->', re.S)


def shots_html(app, n=3):
    urls = S(app)["screenshots"][:n]
    lazy = 'loading="lazy"'
    imgs = "".join(f'<img src="{u}" alt="{e(app["name"])} screenshot {i + 1}" width="460" height="1000" {"fetchpriority=high" if i == 0 else lazy} decoding="async">' for i, u in enumerate(urls))
    return f'<div class="ll-hero__shots" aria-hidden="true">{imgs}</div><!-- /shots -->'


def patch_layout(s, app=None, guide=False):
    """Bring legacy page markup onto the v3 system: two-column app hero, no inline spacing."""
    m = HERO_RE.search(s)
    if m and app and not guide:
        if m.group(1):
            s = SHOTS_RE.sub(lambda _: shots_html(app), s, count=1)
        else:
            inner = m.group(2)
            icon = re.search(r'\s*<div class="ll-hero__icon">.*?</div>', inner, re.S)
            eb = re.search(r'\s*<p class="ll-eyebrow">.*?</p>', inner, re.S)
            rest = inner
            for x in (icon, eb):
                if x:
                    rest = rest.replace(x.group(0), "", 1)
            ident = f'<div class="ll-hero__id">{icon.group(0).strip() if icon else ""}{eb.group(0).strip() if eb else ""}</div>'
            new = f'<section class="ll-hero ll-hero--app">\n    <div class="ll-hero__text">\n    {ident}{rest}\n    </div>\n    {shots_html(app)}\n  </section>'
            s = s[:m.start()] + new + s[m.end():]
    elif m and guide and not m.group(1):
        s = s[:m.start()] + '<section class="ll-hero ll-hero--guide">' + m.group(2) + "\n  </section>" + s[m.end():]
    s = s.replace('<p style="margin-top:16px;font-size:13.5px;">', '<p class="ll-note">')
    s = s.replace('<p style="margin-top:8px;font-size:13.5px;">', '<p class="ll-note">')
    s = re.sub(r'(<(?:h3|p|div)(?: class="[^"]*")?) style="margin-(?:top|bottom):[0-9.]+(?:px|rem);?"', r"\1", s)
    return s


GLANCE_RE = re.compile(r'\s*<aside class="ll-glance".*?</aside>', re.S)
GUIDE_HERO_RE = re.compile(r'(<section class="ll-hero ll-hero--guide">.*?)(\n  </section>)', re.S)


def add_glance(s, app):
    """Fill the empty side of a guide hero: how many apps are ranked, the category, and our own app disclosed."""
    s = GLANCE_RE.sub("", s)
    m = GUIDE_HERO_RE.search(s)
    if not m:
        return s
    h = HUB[app["hub"]]
    n = len(re.findall(r'class="ll-rank-item\b', s))
    facts = (f'<div><dt>Apps compared</dt><dd>{n}</dd></div>' if n else "") + \
            f'<div><dt>Category</dt><dd><a href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")}</a></dd></div>'
    aside = f'''
    <aside class="ll-glance" aria-label="At a glance">
      <p class="ll-glance__label">At a glance</p>
      <dl class="ll-glance__facts">{facts}</dl>
      <a class="ll-glance__app" href="/apps/{app["slug"]}/">{icon(app, 44)}<span><b>We make {e(app["name"])}</b><small>It is in this ranking. Where a competitor is the better pick, the guide says so.</small></span></a>
    </aside>'''
    return s[:m.end(1)] + aside + s[m.end(1):]


LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def clean_ld(s, app=None):
    """Drop page-level BreadcrumbList nodes (build adds the canonical one) and sync app facts from the store."""
    def fix(m):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        nodes = data.get("@graph") if isinstance(data, dict) else None
        if nodes is None:
            return m.group(0)
        data["@graph"] = [n for n in nodes if n.get("@type") != "BreadcrumbList"]
        if app:
            st = S(app)
            for n in data["@graph"]:
                if n.get("@type") == "MobileApplication" and str(n.get("@id", "")).endswith("/apps/%s/#app" % app["slug"]):
                    if st.get("updated"):
                        n["dateModified"] = st["updated"]
                    if st.get("version"):
                        n["softwareVersion"] = st["version"]
                    if st["count"]:
                        n["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": rating_str(app), "ratingCount": st["count"], "bestRating": 5, "worstRating": 1}
                    else:
                        n.pop("aggregateRating", None)
        return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>"
    return LD_RE.sub(fix, s)


def set_desc(s, desc):
    for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")',
                r'(<meta name="twitter:description" content=")[^"]*(")'):
        s = re.sub(pat, lambda m: m.group(1) + e(desc) + m.group(2), s, count=1)
    return s


def set_titles(s, title):
    t = e(title, quote=False)
    s = re.sub(r"<title>.*?</title>", lambda _: f"<title>{t}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + e(title) + m.group(2), s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + e(title) + m.group(2), s, count=1)
    return s


def patch_pages():
    for a in APPS:
        h = HUB[a["hub"]]
        # app page
        p = ROOT / "apps" / a["slug"] / "index.html"
        if not p.exists() or not (ROOT / a["guide"] / "index.html").exists():
            print("  skip (page missing):", a["slug"])
            continue
        s = p.read_text()
        trail = [("Loveiko Labs", "/"), (h["name"], f'/{h["slug"]}/'), (a["name"], f'/apps/{a["slug"]}/')]
        links = f'<li><a href="/{a["guide"]}/">{e(a["guide_title"])}</a></li><li><a href="/{h["slug"]}/">More {h["name"].replace("&", "&amp;")} apps</a></li>'
        s = patch_common(s, f't-{h["key"]}', trail, app_col(FOOT_RE.search(s).group(0) if FOOT_RE.search(s) else "", e(a["name"]), links))
        s = patch_ratings(s, a)
        s = patch_layout(s, a)
        s = clean_ld(s, a)
        s = set_titles(s, a["seo_title"])
        if a.get("seo_desc"):
            s = set_desc(s, a["seo_desc"])
        p.write_text(s)
        # guide page
        g = ROOT / a["guide"] / "index.html"
        s = g.read_text()
        trail = [("Loveiko Labs", "/"), (h["name"], f'/{h["slug"]}/'), (a["guide_title"], f'/{a["guide"]}/')]
        links = f'<li><a href="/apps/{a["slug"]}/">{e(a["name"])} overview</a></li><li><a href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")} apps</a></li><li><a href="/guides/">All guides</a></li>'
        s = patch_common(s, f't-{h["key"]}', trail, f'<div><strong>Related</strong><ul>{links}</ul></div>')
        s = FAKE_QUOTES_RE.sub("", s)
        s = patch_layout(s, a, guide=True)
        s = add_glance(s, a)
        s = clean_ld(s)
        s = set_titles(s, a["guide_seo_title"])
        if a.get("guide_seo_desc"):
            s = set_desc(s, a["guide_seo_desc"])
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
             f"- About: {SITE}/about/", f"- Editorial policy: {SITE}/editorial-policy/",
             f"- Full site text for AI assistants: {SITE}/llms-full.txt", ""]
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
    s = re.sub(r"with \d+ focused iPhone apps", f"with {len(APPS)} focused iPhone apps", s)
    s = re.sub(r"Portfolio: \d+ shipped iOS apps", f"Portfolio: {len(APPS)} shipped iOS apps", s)
    p.write_text(s)
    print("updated llms.txt")


def build_404():
    tiles = "".join(f'<a class="t-{h["key"]}" href="/{h["slug"]}/">{h["name"].replace("&", "&amp;")}<span>{len(hub_apps(h["key"]))} apps →</span></a>' for h in HUBS)
    body = f'''
<div class="ll-wrap">
  <section class="ll-hub-hero ll-hub-hero--tall">
    <p class="ll-eyebrow">404</p>
    <h1>This page <em>doesn't exist</em>.</h1>
    <div class="ll-prose"><p>The link may be old or mistyped. Pick a category below or go back to the <a href="/">home page</a>.</p></div>
  </section>
  <section class="ll-section"><div class="ll-hub-links">{tiles}</div></section>
</div>'''
    page("/404/", "Page not found | Loveiko Labs", "This page does not exist on loveikolabs.com.", body)
    src = ROOT / "404" / "index.html"
    (ROOT / "404.html").write_text(src.read_text().replace('<link rel="canonical" href="https://loveikolabs.com/404/">', '<meta name="robots" content="noindex">'))
    src.unlink(); src.parent.rmdir()
    print("wrote 404.html")


def build_llms_full():
    """Plain-text dump of every page's main content for AI crawlers (llms-full.txt convention)."""
    from html.parser import HTMLParser

    class T(HTMLParser):
        skip_tags = {"script", "style", "nav", "header", "footer", "svg", "button", "figure"}
        block = {"p", "li", "h1", "h2", "h3", "h4", "tr", "summary", "div", "section", "article", "br", "td", "th"}

        def __init__(self):
            super().__init__(); self.out = []; self.skip = 0; self.in_main = False

        def handle_starttag(self, tag, attrs):
            if tag == "main": self.in_main = True
            if tag in self.skip_tags: self.skip += 1
            if tag in ("h1", "h2", "h3"): self.out.append("\n" + "#" * int(tag[1]) + " ")
            elif tag == "li": self.out.append("\n- ")
            elif tag in ("td", "th"): self.out.append(" | ")
            elif tag in self.block: self.out.append("\n")

        def handle_endtag(self, tag):
            if tag in self.skip_tags and self.skip: self.skip -= 1
            if tag == "main": self.in_main = False

        def handle_data(self, d):
            if self.in_main and not self.skip: self.out.append(d)

    order = ["/", "/about/", "/editorial-policy/", "/guides/"] + [f'/{h["slug"]}/' for h in HUBS] + \
            [x for a in APPS for x in (f'/apps/{a["slug"]}/', f'/{a["guide"]}/')]
    parts = [f"# Loveiko Labs — full site text\n\nGenerated {TODAY_ISO} from {SITE}. Short index: {SITE}/llms.txt\n"]
    for u in order:
        f = ROOT / "index.html" if u == "/" else ROOT / u.strip("/") / "index.html"
        if not f.exists():
            continue
        t = T(); t.feed(f.read_text())
        txt = re.sub(r"[ \t]+", " ", "".join(t.out))
        txt = re.sub(r"(?m)^\s*-\s*$", "", txt)
        txt = re.sub(r"\n\s*\n+", "\n\n", txt).strip()
        parts.append(f"\n\n---\n\nURL: {SITE}{u}\n\n{txt}")
    (ROOT / "llms-full.txt").write_text("".join(parts) + "\n")
    print("wrote llms-full.txt", round((ROOT / "llms-full.txt").stat().st_size / 1024), "KB")


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
    build_llms_full()
