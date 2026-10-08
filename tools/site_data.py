"""Single source of truth for the site's app catalog and hubs.

Edit this file, then run `python3 tools/build.py` from the repo root.
Store numbers (rating, rating count) live in tools/store.json and are
refreshed from the public iTunes lookup API by `python3 tools/build.py --refresh`.
"""

HUBS = [
    {
        "key": "health",
        "desc": 'Eight focused iPhone health trackers for GLP-1, TRT, supplements, hair loss, eczema, PCOS, fatty liver and GERD. Organize logs and labs. Not medical advice.',
        "slug": "health",
        "name": "Health",
        "title": "Health tracking apps",
        "h1": "Health apps for <em>one condition</em> at a time.",
        "eyebrow": "Health · 8 apps",
        "meta": "Eight focused iPhone apps for GLP-1, TRT, supplements, hair loss, eczema, PCOS, fatty liver and GERD. They organize your logs, explain your own lab numbers and prepare you for appointments. Not medical advice.",
        "short": "Trackers for GLP-1, TRT, supplements, hair loss, eczema, PCOS, fatty liver and reflux.",
        "intro": [
            "Each app here is built around one condition or routine. They keep your symptoms, doses, meals and lab results in one private record, explain the numbers on your own reports in plain language, and turn months of notes into a short summary you can bring to an appointment.",
            "They do not diagnose, prescribe or replace your clinician. AI answers are grounded in published guidance from bodies such as the FDA, NIH and Mayo Clinic, and every app page lists what the app does not do.",
        ],
        "faq": [
            ("Are these apps a substitute for a doctor?",
             "No. They are organizers and explainers. They help you log what happens between visits, understand the terms on your own lab report and arrive with better questions. Diagnosis and treatment decisions stay with your clinician."),
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
        "desc": 'BumpCheck checks ingredients for pregnancy safety against CDC, ACOG and NIH guidance, and CrySnap suggests why your baby is crying. iPhone apps.',
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
        "desc": 'Identify, value and screen watches, jewelry, luxury handbags and thrift finds from a photo with WatchSnap, JewelSnap, VeriBag and SnapFlip.',
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
        "desc": 'PestSnap identifies bugs and bites, RoofingCalc Pro is a free offline roofing calculator, and ColorCheck finds your color season. iPhone apps.',
        "slug": "home-style",
        "name": "Home & Style",
        "title": "Home and style apps",
        "h1": "Small tools for the <em>home</em> and the wardrobe.",
        "eyebrow": "Home & Style · 3 apps",
        "meta": "Three iPhone apps for the home and wardrobe: PestSnap identifies bugs and bites, RoofingCalc Pro is a free offline roofing calculator, and ColorCheck finds your color season and checks clothes before you buy.",
        "short": "Pest identification, a free roofing calculator and personal color analysis.",
        "intro": [
            "PestSnap identifies the bug, bite or droppings in a photo and tells you what to do next, from a simple fix to calling a professional. RoofingCalc Pro works offline on a roof or in a truck and turns measurements into squares, pitch, rafters and materials.",
            "ColorCheck finds your 12-season color palette from a selfie, then gives a BUY or SKIP verdict when you point the camera at a piece of clothing.",
        ],
        "faq": [
            ("Is PestSnap a replacement for an exterminator?",
             "No. It tells you what you are likely dealing with (harmless, nuisance or infestation risk) and suggests do-it-yourself steps or a licensed exterminator. For a confirmed infestation, get an in-person inspection before paying for treatment."),
            ("Is RoofingCalc Pro really free?",
             "Yes. RoofingCalc Pro is free on the App Store and the calculators work without an internet connection."),
            ("How accurate is ColorCheck?",
             "Lighting matters most. ColorCheck combines several photos and asks you to retake them when its confidence is below 70%. It is not a substitute for in-person draping by a trained color analyst."),
        ],
    },
    {
        "key": "mind",
        "desc": 'Two Sparrows puts a Bible verse on your Lock Screen, Sakinah explains the words of your salah, and Herself plays one-minute affirmation scenes. iPhone.',
        "slug": "mind-faith",
        "name": "Mind & Faith",
        "title": "Mind and faith apps",
        "h1": "Quiet daily practice for <em>mind</em> and faith.",
        "eyebrow": "Mind & Faith · 3 apps",
        "meta": "Three iPhone apps for daily practice: Two Sparrows puts a Bible verse of the day on your Lock Screen, Home Screen and StandBy, Sakinah explains the words of the Muslim prayer phrase by phrase, and Herself turns your goals into one-minute affirmation scenes read in a copy of your own voice.",
        "short": "A Bible verse on your Lock Screen, the words of your salah explained, and a calm affirmation practice.",
        "intro": [
            "Two Sparrows is a Bible verse widget for your Lock Screen, Home Screen and StandBy. A new verse arrives every morning, chosen for what is on your heart, with every verse quoted from the Berean Standard Bible. No ads, no feed, no streaks.",
            "Sakinah explains the salah you already know by heart: Al-Fatiha, the words of the prayer and short surahs, one phrase at a time, with the Arabic text, its meaning and recitation. Prayer times and the qibla are included and stay free.",
            "Herself is a self-practice tool for calm and confidence. You describe what you want, read aloud for 15 seconds, and hear a one-minute scene of your moment going well in an AI voice made from yours. It is not therapy and does not promise results.",
        ],
        "faq": [
            ("Does Two Sparrows write its own Bible verses with AI?",
             "No. Every verse comes from the Berean Standard Bible. AI only helps find verses that fit how you feel or what you type, and the Scripture only setting hides every AI feature."),
            ("Does Sakinah give religious rulings?",
             "No. Sakinah explains the meaning of the words. It does not judge your prayer or your pronunciation and does not give fatwas. For practice, follow your teacher and your community."),
            ("Are prayer times and qibla free in Sakinah?",
             "Yes. Prayer times for your city and the qibla direction stay free even if your subscription ends."),
            ("What happens to my voice in Herself?",
             "You read a fresh 15 seconds before each chapter. The recording is deleted right after the voice copy is made, the voice copy is deleted within an hour after your scene, and your scenes stay on your iPhone."),
            ("Is Herself a replacement for therapy?",
             "No. Herself is a self-practice tool for adults. It is not therapy or medical care. If you are in crisis, call or text 988 in the US or your local emergency number."),
        ],
    },

]

# Order inside each hub = display order.
APPS = [
    # ── Health
    {"slug": "jabwell", "name": "JabWell", "hub": "health", "store_id": 6764151811, "guide": "best-glp1-tracker-apps-2026", "guide_title": "Best GLP-1 tracker apps 2026", "seo_title": 'JabWell: GLP-1 Tracker & AI Nurse for Ozempic, Mounjaro', "guide_seo_title": 'Best GLP-1 Tracker Apps 2026: 7 iPhone Apps Compared', "seo_desc": 'GLP-1 shot tracker for Ozempic, Wegovy, Mounjaro and Zepbound, with an AI nurse grounded in FDA guidance, side-effect logs and dose history. iPhone.', "guide_seo_desc": 'We compare 7 GLP-1 tracker apps for iPhone on injection logs, side effects, AI help, privacy and price, and say where competitors are the better pick.',
     "tagline": "GLP-1 shot tracker with an AI nurse for Ozempic, Wegovy, Mounjaro and Zepbound users.", "tag": "GLP-1"},
    {"slug": "calibrum", "name": "Calibrum", "hub": "health", "store_id": 6765701652, "guide": "best-trt-tracker-apps-2026", "guide_title": "Best TRT tracker apps 2026", "seo_title": 'Calibrum: TRT Tracker & Testosterone Lab Decoder', "guide_seo_title": 'Best TRT Tracker Apps 2026: 7 iPhone Apps Compared', "seo_desc": 'TRT tracker for men on testosterone therapy: log injections, decode your labs, prepare for doctor visits and ask a cited AI coach. iPhone.', "guide_seo_desc": 'We compare 7 TRT tracker apps for iPhone on injection logs, lab tracking, AI help, privacy and price, with honest notes on where others win.',
     "tagline": "TRT tracker that decodes your labs and helps you prepare for doctor visits.", "tag": "TRT"},
    {"slug": "stacksnap", "name": "StackSnap", "hub": "health", "store_id": 6761888709, "guide": "best-supplement-tracker-apps-2026", "guide_title": "Best supplement tracker apps 2026", "seo_title": 'StackSnap: Supplement Tracker & Vitamin Label Scanner', "guide_seo_title": 'Best Supplement Tracker Apps 2026, Ranked', "seo_desc": 'Scan supplement labels, spot duplicate nutrients and over-limit doses, and see what your stack really costs per month. iPhone app.', "guide_seo_desc": 'Honest ranking of the best supplement tracker apps for iPhone: label scanning, interaction flags, cost tracking and where each app falls short.',
     "tagline": "Scan supplement labels, spot duplicate nutrients and see what your stack really costs.", "tag": "Supplements"},
    {"slug": "folik", "name": "Folik", "hub": "health", "store_id": 6766260530, "guide": "best-hair-loss-tracker-apps-2026", "guide_title": "Best hair loss tracker apps 2026", "seo_title": 'Folik: Hair Loss Tracker & Free Norwood Calculator', "guide_seo_title": 'Best Hair Loss Tracker Apps 2026: 7 Apps Compared', "seo_desc": 'Hair-loss coach with a free Norwood/Ludwig stage estimate, monthly progress photos and an AI coach that cites dermatology sources. iPhone.', "guide_seo_desc": 'We compare 7 hair loss tracker apps for iPhone on photo tracking, staging, treatment logs, AI help and price, including where others win.',
     "tagline": "Hair-loss coach with a free Norwood/Ludwig stage estimate and month-by-month progress photos.", "tag": "Hair loss"},
    {"slug": "salvora", "name": "Salvora", "hub": "health", "store_id": 6768401099, "guide": "best-eczema-tracker-apps-2026", "guide_title": "Best eczema tracker apps 2026", "seo_title": 'Salvora: Eczema Tracker for Flares, Itch & Triggers', "guide_seo_title": 'Best Eczema Tracker Apps 2026: 6 iPhone Apps Compared', "seo_desc": 'Private eczema record: track flares, itch, sleep and triggers, follow a severity trend and share a photo timeline with your dermatologist.', "guide_seo_desc": 'We compare 6 eczema tracker apps for iPhone on flare logs, triggers, photos, privacy and price, and note where each competitor is stronger.',
     "tagline": "Private eczema record for flares, itch, sleep and triggers, with a photo timeline for your dermatologist.", "tag": "Eczema"},
    {"slug": "cysta", "name": "Cysta AI", "hub": "health", "store_id": 6769523580, "guide": "best-pcos-tracker-apps-2026", "guide_title": "Best PCOS tracker apps 2026", "seo_title": 'Cysta AI: PCOS Tracker for Cycles, Symptoms & Labs', "guide_seo_title": 'Best PCOS Tracker Apps 2026: 7 iPhone Apps Compared', "seo_desc": 'PCOS tracker for irregular cycles, symptoms, meals and labs, with an evidence-informed AI coach and a doctor-ready PDF. iPhone app.', "guide_seo_desc": 'We compare 7 PCOS tracker apps for iPhone on cycle tracking, symptoms, labs, AI help, privacy and price, with honest trade-offs for each.',
     "tagline": "PCOS tracker for cycles, symptoms, meals and labs, with an AI coach and a doctor-ready PDF.", "tag": "PCOS"},
    {"slug": "hepatica", "name": "Hepatica", "hub": "health", "store_id": 6771344641, "guide": "best-fatty-liver-apps-2026", "guide_title": "Best fatty liver apps 2026", "seo_title": 'Hepatica: Fatty Liver Diet & Liver Lab Results App', "guide_seo_title": 'Best Fatty Liver Apps 2026: MASLD/NAFLD Apps Compared', "seo_desc": 'Fatty liver companion: understand ALT, AST, GGT and FIB-4 against your own report, check how meals fit and prepare questions. iPhone.', "guide_seo_desc": 'We compare 6 fatty liver (MASLD/NAFLD) apps for iPhone on lab tracking, diet help, AI features and price, and say where others are better.',
     "tagline": "Fatty-liver companion that explains ALT, AST, GGT and FIB-4 against your own report.", "tag": "Fatty liver"},
    {"slug": "refluxora", "name": "Refluxora", "hub": "health", "store_id": 6772436586, "guide": "best-acid-reflux-gerd-apps-2026", "guide_title": "Best acid reflux & GERD apps 2026", "seo_title": 'Refluxora: GERD & Silent Reflux (LPR) Tracker', "guide_seo_title": 'Best Acid Reflux & GERD Apps 2026: 7 Trackers Compared', "seo_desc": 'GERD and silent reflux (LPR) tracker for meals, heartburn and throat and voice symptoms, with lab results explained and an appointment report.', "guide_seo_desc": 'We compare 7 acid reflux and GERD tracker apps for iPhone on meal and symptom logs, LPR support, reports and price, with honest trade-offs.',
     "tagline": "GERD and silent-reflux tracker for meals, heartburn and throat symptoms, with an appointment report.", "tag": "GERD / LPR"},
    # ── Pregnancy & Baby
    {"slug": "bumpcheck", "name": "BumpCheck", "hub": "baby", "store_id": 6762022952, "guide": "best-pregnancy-ingredient-checker-apps-2026", "guide_title": "Best pregnancy ingredient checker apps 2026", "seo_title": 'BumpCheck: Pregnancy-Safe Ingredient Checker', "guide_seo_title": 'Best Pregnancy Ingredient Checker Apps 2026', "seo_desc": 'Check cosmetic, food and medicine ingredients for pregnancy safety against CDC, ACOG and NIH guidance. Scan a barcode or photograph a label.', "guide_seo_desc": 'We rank 7 pregnancy ingredient checker apps and tools on sources, scanning, coverage and price, and explain where each one falls short.',
     "tagline": "Check cosmetic, food and medicine ingredients for pregnancy safety against CDC, ACOG and NIH guidance.", "tag": "Pregnancy"},
    {"slug": "crysnap", "name": "CrySnap", "hub": "baby", "store_id": 6763694086, "guide": "best-baby-cry-translator-apps-2026", "guide_title": "Best baby cry translator apps 2026", "seo_title": 'CrySnap: AI Baby Cry Translator for iPhone', "guide_seo_title": 'Best Baby Cry Translator Apps 2026: 6 Apps Ranked', "seo_desc": "Record your baby's cry and get the likely reason (hungry, tired, gas, colic) with a confidence score and next steps. Calm help at 3 a.m.", "guide_seo_desc": 'We rank 6 baby cry translator apps for iPhone on how they analyse cries, extra parenting help, privacy and price, with honest limits.',
     "tagline": "Record your baby's cry and get the likely reason (hungry, tired, gas or colic) with next steps.", "tag": "Baby"},
    # ── Resale & Valuation
    {"slug": "watchsnap", "name": "WatchSnap", "hub": "resale", "store_id": 6761362953, "guide": "best-watch-identifier-apps-2026", "guide_title": "Best watch identifier apps 2026", "seo_title": 'WatchSnap: AI Watch Identifier & Rolex Checker', "guide_seo_title": 'Best Watch Identifier Apps 2026, Ranked', "seo_desc": "Identify a watch's brand, reference, year and value from a photo, with a Likely Genuine or Potential Replica screening and warning signs.", "guide_seo_desc": 'We rank the best watch identifier apps of 2026 on identification, authenticity screening, value data and price, including marketplaces.',
     "tagline": "Identify a watch's brand, reference and value, with a Likely Genuine or Potential Replica screening.", "tag": "Watches"},
    {"slug": "jewelsnap", "name": "JewelSnap", "hub": "resale", "store_id": 6761104642, "guide": "best-jewelry-identifier-apps-2026", "guide_title": "Best jewelry identifier apps 2026", "seo_title": 'JewelSnap: AI Jewelry Identifier & Hallmark Decoder', "guide_seo_title": 'Best Jewelry Identifier Apps 2026, Ranked', "seo_desc": 'Identify jewelry metal, stones, era and hallmarks from a photo, get a market value range and run a stolen-property check. iPhone app.', "guide_seo_desc": 'We rank the best jewelry identifier apps of 2026 on identification, hallmark decoding, valuation and price, and where each one falls short.',
     "tagline": "Identify metal, stones, era and hallmarks, estimate value and run a stolen-property check.", "tag": "Jewelry"},
    {"slug": "veribag", "name": "VeriBag", "hub": "resale", "store_id": 6762181054, "guide": "best-handbag-authentication-apps-2026", "guide_title": "Best handbag authentication apps 2026", "seo_title": 'VeriBag: Luxury Handbag Legit Check (22 Points)', "guide_seo_title": 'Best Handbag Authentication Apps 2026, Ranked', "seo_desc": '22-point photo reference check for secondhand luxury handbags with a shareable report and QR link. A screening step, not certified authentication.', "guide_seo_desc": 'We rank handbag authentication apps and services for 2026: photo checks vs physical authentication, price, speed and when to pay a pro.',
     "tagline": "22-point photo reference check for secondhand luxury handbags, with a shareable report.", "tag": "Handbags"},
    {"slug": "snapflip", "name": "SnapFlip", "hub": "resale", "store_id": 6761262922, "guide": "best-thrift-flipping-apps-2026", "guide_title": "Best thrift flipping apps 2026", "seo_title": 'SnapFlip: Thrift Scanner with Real eBay Sold Prices', "guide_seo_title": 'Best Thrift Flipping Apps 2026, Ranked', "seo_desc": 'Thrift scanner with real eBay sold prices, a flip score and listing help, so you know what to buy before you reach the checkout. iPhone.', "guide_seo_desc": 'We rank the best thrift flipping apps of 2026 on sold-price data, scanning speed, listing tools and price, with honest trade-offs.',
     "tagline": "Thrift scanner with real eBay sold prices and a flip score before you buy.", "tag": "Thrift"},
    # ── Home & Style
    {"slug": "pestsnap", "name": "PestSnap", "hub": "home", "store_id": 6762886416, "guide": "best-pest-identifier-apps-2026", "guide_title": "Best pest identifier apps 2026", "seo_title": 'PestSnap: AI Bug & Bite Identifier for Your Home', "guide_seo_title": 'Best Pest Identifier Apps 2026: 7 Bug ID Apps Ranked', "seo_desc": 'Snap a bug, bite or droppings and get the likely pest, how serious it is, DIY steps or when to call a licensed exterminator. iPhone app.', "guide_seo_desc": 'We rank 7 pest and bug identifier apps on accuracy for home pests, bite checks, next-step advice and price, with honest notes on each.',
     "tagline": "Snap a bug, bite or droppings and get the likely pest and what to do next.", "tag": "Pests"},
    {"slug": "roofingcalc", "name": "RoofingCalc Pro", "hub": "home", "store_id": 6761068784, "guide": "best-roofing-calculator-apps-2026", "guide_title": "Best roofing calculator apps 2026", "seo_title": 'RoofingCalc Pro: Free Offline Roofing Calculator', "guide_seo_title": 'Best Roofing Calculator Apps 2026: 7 Apps Compared', "seo_desc": 'Free offline roofing calculator for iPhone and iPad: roof area in squares, pitch, rafters, shingle bundles, job cost and PDF estimates.', "guide_seo_desc": 'We compare 7 roofing calculator apps for roofers and homeowners on measurements, pitch and rafter tools, offline use, estimates and price.',
     "tagline": "Free offline roofing calculator for area, squares, pitch, rafters and materials.", "tag": "Roofing"},
    {"slug": "colorcheck", "name": "ColorCheck", "hub": "home", "store_id": 6761604617, "guide": "best-color-analysis-apps-2026", "guide_title": "Best color analysis apps 2026", "seo_title": 'ColorCheck: AI Color Analysis & 12-Season Palette', "guide_seo_title": 'Best Color Analysis Apps 2026, Ranked', "seo_desc": 'Find your 12-season color palette from a selfie, then point your camera at clothing for a BUY or SKIP verdict. iPhone color analysis app.', "guide_seo_desc": 'We rank the best AI color analysis apps of 2026 on season accuracy, palettes, shopping help and price, and when to book a human analyst.',
     "tagline": "Find your 12-season color palette, then get BUY or SKIP on any piece of clothing.", "tag": "Color"},
    # ── Mind & Faith
    {"slug": "sakinah", "name": "Sakinah", "hub": "mind", "store_id": 6818006263, "guide": "best-quran-prayer-apps-2026", "guide_title": "Best Quran & prayer apps 2026", "seo_title": 'Sakinah: Understand Your Salah, Phrase by Phrase', "guide_seo_title": 'Best Quran & Prayer Apps 2026 to Understand Salah',
     "tagline": "Understand the words of your salah phrase by phrase, with recitation, prayer times and qibla.", "tag": "Prayer"},
    {"slug": "herself", "name": "Herself", "hub": "mind", "store_id": 6816159497, "guide": "best-affirmation-apps-2026", "guide_title": "Best affirmation apps 2026", "seo_title": 'Herself: Affirmations in Your Own Voice', "guide_seo_title": 'Best Affirmation Apps 2026: 5 iPhone Apps Compared',
     "tagline": "One-minute affirmation scenes of your moment going well, read in an AI copy of your own voice.", "tag": "Affirmations"},
    {"slug": "two-sparrows", "name": "Two Sparrows", "hub": "mind", "store_id": 6815332799, "guide": "best-bible-verse-widget-apps-2026", "guide_title": "Best Bible verse widget apps 2026", "seo_title": 'Two Sparrows: Bible Verse Widget for Your Lock Screen', "guide_seo_title": 'Best Bible Verse Widget Apps 2026: 7 iPhone Apps Compared',
     "tagline": "A Bible verse of the day on your Lock Screen, Home Screen and StandBy, every verse quoted from Scripture.", "tag": "Bible"},
]

# Hero carousel: (app slug, index into the App Store screenshot list)
HERO_POSTERS = [
    ("watchsnap", 1), ("cysta", 0), ("crysnap", 0), ("stacksnap", 0),
    ("colorcheck", 0), ("two-sparrows", 0), ("sakinah", 0), ("jewelsnap", 0), ("herself", 0), ("veribag", 0),
]

SITE = "https://loveikolabs.com"
