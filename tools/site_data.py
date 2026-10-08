"""Single source of truth for the site's app catalogue and hubs.

Edit this file, then run `python3 tools/build.py` from the repo root.
Store numbers (rating, rating count) live in tools/store.json and are
refreshed from the public iTunes lookup API by `python3 tools/build.py --refresh`.
"""

HUBS = [
    {
        "key": "health",
        "slug": "health",
        "name": "Health",
        "title": "Health tracking apps",
        "h1": "Health apps for <em>one condition</em> at a time.",
        "eyebrow": "Health · 8 apps",
        "meta": "Eight focused iPhone apps for GLP-1, TRT, supplements, hair loss, eczema, PCOS, fatty liver and GERD. They organise your logs, explain your own lab numbers and prepare you for appointments. Not medical advice.",
        "short": "Trackers for GLP-1, TRT, supplements, hair loss, eczema, PCOS, fatty liver and reflux.",
        "intro": [
            "Each app here is built around one condition or routine. They keep your symptoms, doses, meals and lab results in one private record, explain the numbers on your own reports in plain language, and turn months of notes into a short summary you can bring to an appointment.",
            "They do not diagnose, prescribe or replace your clinician. AI answers are grounded in published guidance from bodies such as the FDA, NIH and Mayo Clinic, and every app page lists what the app does not do.",
        ],
        "faq": [
            ("Are these apps a substitute for a doctor?",
             "No. They are organisers and explainers. They help you log what happens between visits, understand the terms on your own lab report and arrive with better questions. Diagnosis and treatment decisions stay with your clinician."),
            ("Where does the AI get its health information?",
             "Answers are grounded in published clinical guidance and public reference sources, such as FDA labelling, NIH resources and Mayo Clinic patient material. Each app page names the sources it relies on and the limits of what it covers."),
            ("Is my health data shared?",
             "Most of the trackers keep your record on your iPhone and need no account. Where a feature uses a cloud AI model, the app's page explains what is sent and when. Each app's privacy label is also listed on its App Store page."),
            ("Which app should I start with?",
             "Pick the one that matches your situation: JabWell for GLP-1 injections, Calibrum for testosterone therapy, StackSnap for supplements, Folik for hair loss, Salvora for eczema, Cysta AI for PCOS, Hepatica for fatty liver and Refluxora for GERD or silent reflux."),
        ],
    },
    {
        "key": "baby",
        "slug": "pregnancy-baby",
        "name": "Pregnancy & Baby",
        "title": "Pregnancy and baby apps",
        "h1": "Calmer answers for <em>pregnancy</em> and the first year.",
        "eyebrow": "Pregnancy & Baby · 2 apps",
        "meta": "Two iPhone apps for expecting and new parents: BumpCheck checks cosmetic, food and medicine ingredients for pregnancy safety, and CrySnap suggests the likely reason a baby is crying.",
        "short": "Ingredient checks during pregnancy and a cry translator for the first months.",
        "intro": [
            "BumpCheck answers the question every pregnant person asks in a store aisle: is this ingredient okay right now? Scan a barcode, photograph a label or paste a list, and it is checked against public CDC, ACOG and NIH guidance.",
            "CrySnap listens to a short recording of your baby's cry and suggests the most likely reason, such as hunger, tiredness or gas, with a confidence score and next steps. Neither app replaces your midwife, OB or paediatrician.",
        ],
        "faq": [
            ("Can BumpCheck tell me a product is 100% safe?",
             "No app can. BumpCheck shows what published guidance says about each ingredient and flags the ones to ask your clinician about. When guidance is unclear, it says so."),
            ("How does CrySnap work?",
             "You record a few seconds of crying. CrySnap's on-device model, trained on more than 10,000 labelled infant cry recordings, analyses the sound and returns the likely reason with a confidence score. It is a calm second opinion at 3 a.m., not a medical assessment."),
            ("When should I call a doctor instead?",
             "Always call your doctor or emergency services for fever in a newborn, breathing difficulty, unusual lethargy, or anything that worries you. CrySnap adds a \"when to call your doctor\" note to any answer that mentions a medical symptom."),
        ],
    },
    {
        "key": "resale",
        "slug": "resale",
        "name": "Resale & Valuation",
        "title": "Resale and valuation apps",
        "h1": "Know what it is and what it is <em>worth</em>.",
        "eyebrow": "Resale & Valuation · 4 apps",
        "meta": "Four iPhone apps for buyers, sellers and resellers: WatchSnap for watches, JewelSnap for jewelry, VeriBag for luxury handbags and SnapFlip for thrift flips. Identify, estimate value and screen authenticity from photos.",
        "short": "Identify, value and screen watches, jewelry, handbags and thrift finds.",
        "intro": [
            "These apps are for the moment before money changes hands: an estate sale, a marketplace listing, a drawer of inherited pieces. Point your camera, and you get an identification, a market value range and the details worth checking.",
            "WatchSnap and VeriBag give a photo-based authenticity screening with the reasons behind it. They are a fast first filter, not certified authentication; for high-value purchases we always recommend a professional inspection as well.",
        ],
        "faq": [
            ("Can a photo app prove a watch or bag is authentic?",
             "No consumer app can guarantee that. WatchSnap and VeriBag compare what they see with documented reference details and tell you which points look consistent and which raise flags. Use them to decide what to inspect further, and use a professional authenticator for expensive purchases."),
            ("Where do the value estimates come from?",
             "From recent market data such as sold listings and marketplace prices for comparable items. Estimates are ranges, and they widen for rare pieces or unusual condition."),
            ("Which app is for which item?",
             "WatchSnap for wristwatches, JewelSnap for rings, necklaces, stones and hallmarks, VeriBag for secondhand luxury handbags, and SnapFlip for general thrift and resale items with real eBay sold prices."),
        ],
    },
    {
        "key": "home",
        "slug": "home-style",
        "name": "Home & Style",
        "title": "Home and style apps",
        "h1": "Small tools for the <em>home</em> and the wardrobe.",
        "eyebrow": "Home & Style · 3 apps",
        "meta": "Three iPhone apps for the home and wardrobe: PestSnap identifies bugs and bites, RoofingCalc Pro is a free offline roofing calculator, and ColorCheck finds your colour season and checks clothes before you buy.",
        "short": "Pest identification, a free roofing calculator and personal colour analysis.",
        "intro": [
            "PestSnap identifies the bug, bite or droppings in a photo and tells you what to do next, from a simple fix to calling a professional. RoofingCalc Pro works offline on a roof or in a truck and turns measurements into squares, pitch, rafters and materials.",
            "ColorCheck finds your 12-season colour palette from a selfie, then gives a BUY or SKIP verdict when you point the camera at a piece of clothing.",
        ],
        "faq": [
            ("Is PestSnap a replacement for an exterminator?",
             "No. It tells you what you are likely dealing with (harmless, nuisance or infestation risk) and suggests do-it-yourself steps or a licensed exterminator. For a confirmed infestation, get an in-person inspection before paying for treatment."),
            ("Is RoofingCalc Pro really free?",
             "Yes. RoofingCalc Pro is free on the App Store and the calculators work without an internet connection."),
            ("How accurate is ColorCheck?",
             "Lighting matters most. ColorCheck combines several photos and asks you to retake them when its confidence is below 70%. It is not a substitute for in-person draping by a trained colour analyst."),
        ],
    },
]

# Order inside each hub = display order.
APPS = [
    # ── Health
    {"slug": "jabwell", "name": "JabWell", "hub": "health", "store_id": 6764151811, "guide": "best-glp1-tracker-apps-2026", "guide_title": "Best GLP-1 tracker apps 2026",
     "tagline": "GLP-1 shot tracker with an AI nurse for Ozempic, Wegovy, Mounjaro and Zepbound users.", "tag": "GLP-1"},
    {"slug": "calibrum", "name": "Calibrum", "hub": "health", "store_id": 6765701652, "guide": "best-trt-tracker-apps-2026", "guide_title": "Best TRT tracker apps 2026",
     "tagline": "TRT tracker that decodes your labs and helps you prepare for doctor visits.", "tag": "TRT"},
    {"slug": "stacksnap", "name": "StackSnap", "hub": "health", "store_id": 6761888709, "guide": "best-supplement-tracker-apps-2026", "guide_title": "Best supplement tracker apps 2026",
     "tagline": "Scan supplement labels, spot duplicate nutrients and see what your stack really costs.", "tag": "Supplements"},
    {"slug": "folik", "name": "Folik", "hub": "health", "store_id": 6766260530, "guide": "best-hair-loss-tracker-apps-2026", "guide_title": "Best hair loss tracker apps 2026",
     "tagline": "Hair-loss coach with a free Norwood/Ludwig stage estimate and month-by-month progress photos.", "tag": "Hair loss"},
    {"slug": "salvora", "name": "Salvora", "hub": "health", "store_id": 6768401099, "guide": "best-eczema-tracker-apps-2026", "guide_title": "Best eczema tracker apps 2026",
     "tagline": "Private eczema record for flares, itch, sleep and triggers, with a photo timeline for your dermatologist.", "tag": "Eczema"},
    {"slug": "cysta", "name": "Cysta AI", "hub": "health", "store_id": 6769523580, "guide": "best-pcos-tracker-apps-2026", "guide_title": "Best PCOS tracker apps 2026",
     "tagline": "PCOS tracker for cycles, symptoms, meals and labs, with an AI coach and a doctor-ready PDF.", "tag": "PCOS"},
    {"slug": "hepatica", "name": "Hepatica", "hub": "health", "store_id": 6771344641, "guide": "best-fatty-liver-apps-2026", "guide_title": "Best fatty liver apps 2026",
     "tagline": "Fatty-liver companion that explains ALT, AST, GGT and FIB-4 against your own report.", "tag": "Fatty liver"},
    {"slug": "refluxora", "name": "Refluxora", "hub": "health", "store_id": 6772436586, "guide": "best-acid-reflux-gerd-apps-2026", "guide_title": "Best acid reflux & GERD apps 2026",
     "tagline": "GERD and silent-reflux tracker for meals, heartburn and throat symptoms, with an appointment report.", "tag": "GERD / LPR"},
    # ── Pregnancy & Baby
    {"slug": "bumpcheck", "name": "BumpCheck", "hub": "baby", "store_id": 6762022952, "guide": "best-pregnancy-ingredient-checker-apps-2026", "guide_title": "Best pregnancy ingredient checker apps 2026",
     "tagline": "Check cosmetic, food and medicine ingredients for pregnancy safety against CDC, ACOG and NIH guidance.", "tag": "Pregnancy"},
    {"slug": "crysnap", "name": "CrySnap", "hub": "baby", "store_id": 6763694086, "guide": "best-baby-cry-translator-apps-2026", "guide_title": "Best baby cry translator apps 2026",
     "tagline": "Record your baby's cry and get the likely reason (hungry, tired, gas or colic) with next steps.", "tag": "Baby"},
    # ── Resale & Valuation
    {"slug": "watchsnap", "name": "WatchSnap", "hub": "resale", "store_id": 6761362953, "guide": "best-watch-identifier-apps-2026", "guide_title": "Best watch identifier apps 2026",
     "tagline": "Identify a watch's brand, reference and value, with a Likely Genuine or Potential Replica screening.", "tag": "Watches"},
    {"slug": "jewelsnap", "name": "JewelSnap", "hub": "resale", "store_id": 6761104642, "guide": "best-jewelry-identifier-apps-2026", "guide_title": "Best jewelry identifier apps 2026",
     "tagline": "Identify metal, stones, era and hallmarks, estimate value and run a stolen-property check.", "tag": "Jewelry"},
    {"slug": "veribag", "name": "VeriBag", "hub": "resale", "store_id": 6762181054, "guide": "best-handbag-authentication-apps-2026", "guide_title": "Best handbag authentication apps 2026",
     "tagline": "22-point photo reference check for secondhand luxury handbags, with a shareable report.", "tag": "Handbags"},
    {"slug": "snapflip", "name": "SnapFlip", "hub": "resale", "store_id": 6761262922, "guide": "best-thrift-flipping-apps-2026", "guide_title": "Best thrift flipping apps 2026",
     "tagline": "Thrift scanner with real eBay sold prices and a flip score before you buy.", "tag": "Thrift"},
    # ── Home & Style
    {"slug": "pestsnap", "name": "PestSnap", "hub": "home", "store_id": 6762886416, "guide": "best-pest-identifier-apps-2026", "guide_title": "Best pest identifier apps 2026",
     "tagline": "Snap a bug, bite or droppings and get the likely pest and what to do next.", "tag": "Pests"},
    {"slug": "roofingcalc", "name": "RoofingCalc Pro", "hub": "home", "store_id": 6761068784, "guide": "best-roofing-calculator-apps-2026", "guide_title": "Best roofing calculator apps 2026",
     "tagline": "Free offline roofing calculator for area, squares, pitch, rafters and materials.", "tag": "Roofing"},
    {"slug": "colorcheck", "name": "ColorCheck", "hub": "home", "store_id": 6761604617, "guide": "best-color-analysis-apps-2026", "guide_title": "Best color analysis apps 2026",
     "tagline": "Find your 12-season colour palette, then get BUY or SKIP on any piece of clothing.", "tag": "Colour"},
]

# Hero carousel: (app slug, index into the App Store screenshot list)
HERO_POSTERS = [
    ("watchsnap", 1), ("cysta", 0), ("crysnap", 0), ("stacksnap", 0),
    ("colorcheck", 0), ("jewelsnap", 0), ("refluxora", 0), ("veribag", 0),
]

SITE = "https://loveikolabs.com"
EMAIL = "loveykovl@gmail.com"
FOUNDER = "Valeriy Loveyko"
