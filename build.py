#!/usr/bin/env python3
"""Generate the Vercel static rebuild of the portfolio site — fancy version.

Source of truth: the live Google Sites portfolio (fetched 2026-11-17) and
~/workspace/nsda-level4-portfolio/09-portfolio-website-pack.md, plus the
verified live updates (Contact, About Training, 6 Reels).

This version is the dark premium design Anisur asked for on 2026-11-17:
fancy effects YES, maroon-suit photo YES, title 'Digital Marketer |
Founder, Veneer Monet', site link anisurrahman.vercel.app if available.

Effects (all built here from scratch, no outside code):
- Hanging ID card with Verlet-rope physics (script.js), photo me-card.webp.
- Mask reveal on the About photo (me-front.webp under me-mask.webp,
  Spider-Man — the default hero; swap the masked file to change hero).
- Cursor follower ring (script.js). The goo button is a glossy CSS pill,
  not the WebGL version — its code lives in a repo that cannot be fetched
  (see README), so the pill is the honest fallback.
- The uploaded 'Portfolio-Guide-for-Claude' PDF is NOT used (failed a
  safety check); its instructions and code links are not followed.
- The Google Sites site stays live and untouched; this is a separate copy.

Rules enforced here (standing rules, 2026-11-15):
- Full legal name 'Md. Anisur Rahman' everywhere; 'Veneer Monet' only as brand/project.
- NO 'Level 4' phrase, NO 'Digital Marketing for Freelancing' phrase, no unit codes.
- 'E-Learning' always capital E. Real phone +8801577809069, email anisuranik6@gmail.com.
- No fake claims: first sale still pending; follower counts not stated as fact.

Run: python3 build.py — regenerates all 11 pages, styles.css, robots.txt,
sitemap.xml. script.js and assets/ are hand-written and not touched.
"""
import os

OUT = os.path.expanduser("~/workspace/nsda-level4-portfolio/vercel-rebuild")
BASE = "https://anisurrahman.vercel.app"  # Vercel project name 'anisurrahman'; confirm on first deploy
META = ("Digital marketer from Bangladesh. Local SEO, Google Business Profile, "
        "email marketing, YouTube marketing and Google Ads — with real work on "
        "Pinterest, Gumroad, Instagram and Facebook.")
GA = "G-6Z69CGL8GR"
CV = "https://drive.google.com/file/d/1XP0N8HguOGE4a4vWPSFzMBL2yZEAsR4X/view"
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdoa5DA7G7di8MTTwgbKLN9BCHksnGnCCdA-rZlcy7wonENxg/viewform"

NAV = [
    ("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
    ("my-work/index.html", "My Work"), ("evidence.html", "Evidence"),
    ("what-i-learned.html", "What I Learned"), ("contact.html", "Contact"),
]

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;700&display=swap" rel="stylesheet">"""

CHROME = """<div class="cur-dot" aria-hidden="true"></div><div class="cur-ring" aria-hidden="true"></div><div class="cur-halo" aria-hidden="true"></div>
<a class="goo" href="/contact.html">let's collab</a>
<script src="{prefix}script.js" defer></script>"""

def nav_html(current):
    items = []
    for href, label in NAV:
        cls = ' class="active"' if href == current else ""
        items.append(f'<a href="/{href}"{cls}>{label}</a>')
    return '<nav>' + " ".join(items) + "</nav>"

def page(path, title, desc, body, extra_head=""):
    depth = path.count("/")
    prefix = "../" * depth
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Md. Anisur Rahman</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}/{path}">
{FONTS}
<link rel="stylesheet" href="{prefix}styles.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');</script>
{extra_head}</head>
<body class="std">
<header><div class="wrap"><a class="brand" href="/index.html">Md. Anisur Rahman</a><p class="tag">Digital Marketer — Cumilla, Bangladesh</p>{nav_html(path)}</div></header>
<main class="wrap narrow">
{body}
</main>
<footer><div class="wrap"><p>Md. Anisur Rahman — Digital Marketer, Cumilla, Bangladesh · <a href="mailto:anisuranik6@gmail.com">anisuranik6@gmail.com</a> · +8801577809069</p><p><a href="https://www.pinterest.com/veneermonet/">Pinterest</a> · <a href="https://veneermonet.gumroad.com/">Gumroad</a> · <a href="https://www.instagram.com/veneermonet/">Instagram</a> · <a href="https://www.facebook.com/veneermonet/">Facebook</a> · <a href="https://www.linkedin.com/in/anisurmarketer">LinkedIn</a></p></div></footer>
{CHROME.format(prefix=prefix)}
</body>
</html>
"""
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Md. Anisur Rahman",
  "description": "Digital marketing freelancer in Cumilla, Bangladesh — local SEO, Google Business Profile, Search Console and Analytics, email marketing and video marketing.",
  "telephone": "+8801577809069",
  "url": "https://anisurrahman.vercel.app",
  "address": {"@type": "PostalAddress", "addressLocality": "Cumilla", "addressCountry": "BD"},
  "areaServed": "Cumilla, Bangladesh",
  "knowsAbout": ["Local SEO", "Google Business Profile", "Google Search Console", "Google Analytics", "Email Marketing", "Video Marketing"],
  "sameAs": ["https://www.linkedin.com/in/anisurmarketer", "https://www.pinterest.com/veneermonet/", "https://veneermonet.gumroad.com/"]
}
</script>"""

CSS = """*{box-sizing:border-box}
:root{--bg:#121110;--panel:#1a1917;--text:#fbf9f5;--body:#a8a39b;--accent:#ff3b2f;--accent-soft:#ff8a80;--cream:#f7f5f1;--border:rgba(255,255,255,.08);--mono:"Geist Mono",ui-monospace,SFMono-Regular,Menlo,monospace}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Geist",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;line-height:1.65}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:2000;opacity:.05;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='0.6'/%3E%3C/svg%3E")}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
.wrap.narrow{max-width:760px}
h1,h2,h3{font-weight:600;letter-spacing:-.03em;line-height:1.05}
h1{font-size:1.9rem}
h2{margin-top:1.6em;font-size:1.45rem}
a{color:var(--accent-soft)}
img{max-width:100%}
.label{font-family:var(--mono);text-transform:uppercase;letter-spacing:.1em;font-size:.8rem;color:var(--body)}
/* ---- standard pages ---- */
body.std header{border-bottom:1px solid var(--border);padding:22px 0 14px}
body.std header .brand{color:var(--text);font-size:1.35rem;font-weight:700;text-decoration:none}
body.std header .tag{color:var(--body);margin:4px 0 12px}
body.std nav a{color:var(--body);text-decoration:none;margin-right:16px;font-size:.95rem}
body.std nav a.active,body.std nav a:hover{color:var(--text);text-decoration:underline}
body.std main{padding:28px 0 110px}
body.std footer{border-top:1px solid var(--border);padding:18px 0 110px;color:var(--body);font-size:.9rem}
body.std footer a{color:var(--body)}
footer{border-top:1px solid var(--border);padding:18px 0 110px;color:var(--body);font-size:.9rem}
footer a{color:var(--body)}
.button{display:inline-block;background:var(--cream);color:#121110;padding:10px 18px;border-radius:999px;text-decoration:none;margin-top:8px;font-weight:600}
.about-photo{max-width:280px;border-radius:12px;display:block;margin:6px 0 4px}
.about-photo-cap{color:var(--body);font-size:.9rem;margin:0 0 18px}
/* ---- loader / progress / nav pill ---- */
.loader{position:fixed;inset:0;background:var(--bg);z-index:5000;display:flex;align-items:center;justify-content:center;transition:opacity .4s}
.loader.done{opacity:0;pointer-events:none}
.loader .tc{font-family:var(--mono);font-size:1rem;letter-spacing:.2em}
.loader .tc b{color:var(--accent)}
.progress{position:fixed;top:0;left:0;height:2px;background:var(--accent);z-index:101;width:0}
.navpill{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:100;display:flex;gap:2px;align-items:center;padding:7px 9px;border-radius:999px;background:rgba(26,25,23,.72);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid var(--border);transition:transform .35s;max-width:calc(100vw - 24px)}
.navpill.hidden{transform:translate(-50%,-140%)}
.navpill a{color:var(--text);text-decoration:none;padding:6px 12px;border-radius:999px;font-size:.92rem;white-space:nowrap}
.navpill a:hover{background:rgba(255,255,255,.08)}
.navpill .brand-link{font-weight:700}
.navpill .cta{background:var(--cream);color:#121110;font-weight:600}
/* ---- hero ---- */
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:start;padding:clamp(118px,16vw,168px) 0 clamp(56px,7vw,104px)}
.badge{display:inline-flex;gap:8px;align-items:center;border:1px solid var(--border);border-radius:999px;padding:6px 14px;font-size:.85rem;color:var(--body)}
.badge .dot{width:8px;height:8px;border-radius:50%;background:#22c55e}
.hero h1{font-size:clamp(3rem,7.5vw,5.4rem);line-height:.95;letter-spacing:-.055em;margin:22px 0 6px}
.hero .role{font-family:var(--mono);color:var(--accent);font-size:.95rem;letter-spacing:.08em;text-transform:uppercase;margin:0 0 18px}
.hero .tagline{font-size:1.25rem;color:var(--body);max-width:34rem;margin:0}
.hero .actions{display:flex;gap:12px;margin:28px 0 22px;flex-wrap:wrap}
.btn{display:inline-block;padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:600}
.btn-cream{background:var(--cream);color:#121110}
.btn-ghost{border:1px solid var(--border);color:var(--text)}
.tools{display:flex;gap:8px;flex-wrap:wrap}
.tools span{border:1px solid var(--border);border-radius:999px;padding:5px 12px;font-size:.85rem;color:var(--body)}
/* ---- ID card ---- */
.idwrap{position:relative;height:600px}
.idstrap{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.idcard{position:absolute;left:0;top:0;width:250px;background:var(--cream);color:#1c1a17;border-radius:18px;box-shadow:0 30px 60px rgba(0,0,0,.5);padding:16px 16px 16px;cursor:grab;will-change:transform;touch-action:none;transform-origin:50% 0}
.idcard:active{cursor:grabbing}
.idcard .clip{position:absolute;top:-13px;left:50%;transform:translateX(-50%);width:54px;height:20px;background:linear-gradient(#dcdcdc,#9a9a9a);border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.4)}
.idcard .slot{position:absolute;top:7px;left:50%;transform:translateX(-50%);width:70px;height:8px;border-radius:4px;background:#e7e4df;box-shadow:inset 0 1px 3px rgba(0,0,0,.25)}
.idcard .top{display:flex;justify-content:space-between;font-family:var(--mono);font-size:.72rem;letter-spacing:.12em}
.idcard .rec{color:var(--accent);font-weight:700}
.idcard .photo{position:relative;margin:12px 0 10px;border-radius:10px;overflow:hidden}
.idcard .photo img{display:block;width:100%;height:210px;object-fit:cover;object-position:top}
.idcard .photo .c{position:absolute;width:18px;height:18px;border:2px solid #fff}
.idcard .photo .tl{top:8px;left:8px;border-right:0;border-bottom:0}
.idcard .photo .tr{top:8px;right:8px;border-left:0;border-bottom:0}
.idcard .photo .bl{bottom:8px;left:8px;border-right:0;border-top:0}
.idcard .photo .br{bottom:8px;right:8px;border-left:0;border-top:0}
.idcard .job{font-family:var(--mono);color:var(--accent);font-size:.75rem;letter-spacing:.14em;text-transform:uppercase}
.idcard .job2{font-size:.85rem;color:#6b6560;margin-top:2px}
.idcard .name{font-size:1.45rem;font-weight:700;letter-spacing:-.02em;line-height:1.05;margin:6px 0 8px}
.idcard .meta{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;color:#6b6560;display:flex;justify-content:space-between}
.barcode{height:34px;margin-top:10px;background:repeating-linear-gradient(90deg,#1c1a17 0 2px,transparent 2px 5px,#1c1a17 5px 6px,transparent 6px 10px,#1c1a17 10px 13px,transparent 13px 15px)}
.idcap{position:absolute;bottom:0;left:0;right:0;text-align:center;color:var(--body);font-family:var(--mono);font-size:.75rem;letter-spacing:.14em;margin:0}
/* ---- skills strip ---- */
.strip{border-top:1px solid var(--border);border-bottom:1px solid var(--border);overflow:hidden;padding:18px 0}
.strip-track{display:flex;width:max-content;animation:scrollx 22s linear infinite}
.strip-track span{font-size:1.15rem;font-weight:600;letter-spacing:-.02em;padding:0 18px;white-space:nowrap}
.strip-track i{color:var(--accent);font-style:normal;align-self:center}
@keyframes scrollx{to{transform:translateX(-50%)}}
/* ---- sections ---- */
section{padding:clamp(56px,7vw,104px) 0}
.sec-head{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:28px;flex-wrap:wrap}
.sec-head h2{margin:8px 0 0;font-size:clamp(1.7rem,3.5vw,2.4rem)}
.work-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.work-card{background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:26px}
.work-card:hover{border-color:rgba(255,59,47,.5)}
.work-card .num{font-size:2.6rem;font-weight:700;letter-spacing:-.04em;color:var(--accent);line-height:1}
.work-card h3{margin:14px 0 6px;font-size:1.35rem}
.work-card p{color:var(--body);margin:0 0 14px}
.work-card a{color:var(--text);font-weight:600;text-decoration:none;border-bottom:1px solid var(--accent)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.step{border-top:2px solid var(--accent);padding-top:16px}
.step .n{font-family:var(--mono);color:var(--accent);font-size:.8rem;letter-spacing:.1em}
.step h3{margin:10px 0 6px;font-size:1.15rem}
.step p{color:var(--body);font-size:.95rem;margin:0}
.about-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:48px;align-items:center}
.about-grid h2{margin:8px 0 14px;font-size:clamp(1.7rem,3.5vw,2.4rem)}
.about-grid p{color:var(--body)}
.about-grid p strong{color:var(--text)}
.reveal{position:relative;border-radius:20px;overflow:hidden;aspect-ratio:3/4;max-width:420px;cursor:crosshair;touch-action:none;background:#2a2724}
.reveal img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.reveal .top{--mx:50%;--my:40%;--r:0px;-webkit-mask-image:radial-gradient(circle var(--r) at var(--mx) var(--my),#000 98%,transparent 100%);mask-image:radial-gradient(circle var(--r) at var(--mx) var(--my),#000 98%,transparent 100%)}
.lens-ring{position:absolute;border:2px solid rgba(255,255,255,.9);border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);opacity:0;box-shadow:0 0 0 4px rgba(0,0,0,.15);z-index:2}
.reveal-cap{text-align:center;color:var(--body);font-family:var(--mono);font-size:.75rem;letter-spacing:.14em;margin:14px 0 0;max-width:420px}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.pills span{border:1px solid var(--border);border-radius:999px;padding:6px 14px;font-size:.9rem}
.contact-card{background:var(--cream);color:#1c1a17;border-radius:20px;padding:clamp(28px,5vw,56px)}
.contact-card .label{color:#8a7f78}
.contact-card h2{color:#1c1a17;margin:8px 0 10px;font-size:clamp(1.8rem,4vw,2.6rem)}
.contact-card p.lede{color:#4a443f;margin:0 0 10px}
.contact-row{display:flex;justify-content:space-between;align-items:center;gap:16px;border-top:1px solid rgba(0,0,0,.12);padding:16px 0;flex-wrap:wrap}
.contact-row a{color:#1c1a17;font-weight:600;text-decoration:none}
.contact-row .muted{color:#6b6560}
.copybtn{border:1px solid rgba(0,0,0,.25);background:transparent;border-radius:999px;padding:8px 16px;cursor:pointer;font-weight:600;color:#1c1a17}
.socials{display:flex;gap:8px;flex-wrap:wrap;padding-top:16px}
.socials a{border:1px solid rgba(0,0,0,.25);border-radius:999px;padding:8px 16px;color:#1c1a17;text-decoration:none;font-weight:600}
/* ---- goo pill + cursor ---- */
.goo{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:90;background:linear-gradient(180deg,#2b2b2b,#000);color:#fff;border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:14px 30px;font-weight:700;font-size:1.05rem;text-decoration:none;box-shadow:0 12px 32px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.25)}
.goo:hover{animation:wobble .6s ease}
@keyframes wobble{0%{transform:translateX(-50%) scale(1)}30%{transform:translateX(-50%) scale(1.12,.88)}60%{transform:translateX(-50%) scale(.94,1.08)}100%{transform:translateX(-50%) scale(1)}}
.cur-dot,.cur-ring,.cur-halo{position:fixed;top:0;left:0;pointer-events:none;z-index:3000;border-radius:50%;transform:translate(-50%,-50%)}
.cur-dot{width:5px;height:5px;background:#fff}
.cur-ring{width:34px;height:34px;border:1.5px solid rgba(255,255,255,.85);transition:width .2s,height .2s,border-color .2s,box-shadow .2s,opacity .2s}
.cur-ring.big{width:56px;height:56px;border-color:var(--accent);box-shadow:0 0 18px rgba(255,59,47,.45)}
.cur-halo{width:40px;height:40px;background:rgba(255,255,255,.06)}
body.no-cur .cur-dot,body.no-cur .cur-ring,body.no-cur .cur-halo{opacity:0}
@media (hover:none),(prefers-reduced-motion:reduce){.cur-dot,.cur-ring,.cur-halo{display:none}}
@media (prefers-reduced-motion:reduce){.strip-track{animation:none}.goo:hover{animation:none}html{scroll-behavior:auto}}
/* ---- responsive ---- */
@media (max-width:900px){
.hero{grid-template-columns:1fr;padding-top:110px}
.idwrap{height:580px;max-width:420px;margin:0 auto;width:100%}
.work-grid{grid-template-columns:1fr}
.steps{grid-template-columns:repeat(2,1fr)}
.about-grid{grid-template-columns:1fr}
}
@media (max-width:700px){
.navpill a:not(.brand-link):not(.cta){display:none}
.steps{grid-template-columns:1fr}
.hero h1{font-size:2.7rem}
.idcard{width:220px}
}
"""

# ---- About ----
page("about.html", "About", META, f"""
<h1>About — Md. Anisur Rahman</h1>
<img class="about-photo" src="/assets/me-front.webp" alt="Md. Anisur Rahman in a maroon suit">
<p class="about-photo-cap">Md. Anisur Rahman — Digital Marketer, Founder of Veneer Monet.</p>
<p>I'm Md. Anisur Rahman, a digital marketing student in Bangladesh and the founder of Veneer Monet, a nail-art brand for beginners.</p>
<p>I learned digital marketing by doing it on my own brand first: I plan and publish Pinterest campaigns, run a Gumroad store with five digital products, publish Instagram Reels, and manage a Facebook Page. Everything on this site is my own work — real accounts, real numbers.</p>
<h2>Skills &amp; tools</h2>
<p>Skills: Local SEO · Google Business Profile · Google Search Console · Google Analytics · Email Marketing (Mailchimp) · YouTube SEO · Google Ads · Pinterest Marketing · Content Planning.</p>
<h2>Training</h2>
<p>Freelancing Training — Digital Marketing (64 Districts Programme), E-Learning and Earning Ltd, July–September 2026. A Department of Youth Development programme (Ministry of Youth and Sports) for freelancing training in all 64 districts.</p>
<p><a class="button" href="{CV}">Download CV (PDF)</a></p>
""")

# ---- Services ----
page("services.html", "Services", META, """
<h1>Services</h1>
<h2>Local SEO</h2>
<p>I optimise a local business website and its citations so it ranks for "near me" searches in its own city. Includes keyword research, on-page fixes, NAP consistency and review strategy.</p>
<h2>Google Business Profile Setup</h2>
<p>I set up and optimise a complete business profile: categories, hours, services, photos, posts and review replies.</p>
<h2>Email Marketing</h2>
<p>I build a permission-based list and write campaigns that sell without spamming: welcome emails, promotions and newsletters, with open and click reporting.</p>
<h2>YouTube Marketing</h2>
<p>I optimise a channel and its videos: keyword titles, descriptions, tags, thumbnails and end screens, plus Shorts from existing video.</p>
<h2>Google Ads Campaigns</h2>
<p>I plan and manage small-budget Search and social campaigns with clear tracking: clicks, conversions, cost per result and ROI.</p>
""")

# ---- My Work index ----
page("my-work/index.html", "My Work", META, """
<h1>My Work</h1>
<p>Four case studies from my live project, Veneer Monet — each one Problem → Action → Result, with honest numbers.</p>
<ul>
<li><a href="/my-work/pinterest-video-campaign.html">Case Study 1 — Pinterest Video Campaign</a>: a new nail-art brand with no audience and no sales channel.</li>
<li><a href="/my-work/gumroad-store-and-funnel.html">Case Study 2 — Gumroad Store &amp; Funnel</a>: beginner nail guides needed a store that sells without a website.</li>
<li><a href="/my-work/instagram-reels.html">Case Study 3 — Instagram Reels</a>: the same nail looks needed a second audience outside Pinterest.</li>
<li><a href="/my-work/facebook-page-and-groups.html">Case Study 4 — Facebook Page &amp; Groups</a>: a new Page with no followers needed trust in real nail communities.</li>
</ul>
""")

def case(path, title, problem, action, result, learned, link_label, link_url):
    learned_html = f"<h2>What I learned</h2><p>{learned}</p>" if learned else ""
    page(path, title, META, f"""
<h1>{title}</h1>
<h2>Problem</h2><p>{problem}</p>
<h2>Action</h2><p>{action}</p>
<h2>Result</h2><p>{result}</p>
{learned_html}
<p>{link_label}: <a href="{link_url}">{link_url}</a></p>
<p><a href="/my-work/index.html">← Back to My Work</a></p>
""")

case("my-work/pinterest-video-campaign.html", "Pinterest Video Campaign",
     "A new nail-art brand with no audience and no sales channel.",
     "I planned and scheduled 63 video pins in 3 weekly campaigns (21 pins per week, 3 per day), one board only, each pin with its own creative, SEO title, description, alt text and destination link.",
     "Campaigns 1–2 published 31 Oct – 13 Nov 2026 (42 pins). Campaign 3 scheduled 14–21 Nov 2026 (21 pins). Impressions 35 over 4 days (6 Nov) rising to 143 (9 Nov). 459 monthly views (14 Nov, logged-out profile view). First sale still pending.",
     "Distribution is the bottleneck — each pin gets a small seed audience, and saves widen it. Schedule slowly like a human or the bot check triggers. Title, image and overlay must match, or the pin confuses people.",
     "Pinterest profile", "https://www.pinterest.com/veneermonet/")

case("my-work/gumroad-store-and-funnel.html", "Gumroad Store and Funnel",
     "Beginner nail guides needed a store that sells without a website.",
     "I set up 5 digital products on Gumroad (3 full books at $9.99, a $3.99 starter pack, a free checklist), wrote all descriptions, and linked them into a funnel: free checklist → starter pack → full books.",
     "Store live with 5 published products; funnel cross-links verified on every product page. 0 paid sales as of the 2 Nov check. First sale still pending. Illustrations work best framed as a blueprint advantage, not an apology for no photos. Checkout must stay simple — I removed 4 shipping fields that did not belong on a digital product.",
     "",
     "Gumroad store", "https://veneermonet.gumroad.com/")

case("my-work/instagram-reels.html", "Instagram Reels",
     "The same nail looks needed a second audience outside Pinterest.",
     "I adapted the campaign videos into 9:16 Reels with book-specific captions and a bio link to the store.",
     "6 Reels published (Nov 2026); profile customised with logo, bio and store link. Reels: <a href=\"https://www.instagram.com/reel/DfhDF0Uj5rx/\">#1 Thanksgiving Cocoa Nude</a>, <a href=\"https://www.instagram.com/reel/Dfhzxq1j6xm/\">#2 Thanksgiving Blush Fade</a>, <a href=\"https://www.instagram.com/reel/DfjSy4AjwJF/\">#3 Thanksgiving Jewel Canvas Set</a>, <a href=\"https://www.instagram.com/reel/DfmsLL-j6eC/\">#4 Thanksgiving Pearl Veil</a>, <a href=\"https://www.instagram.com/reel/Dfy-abSj-wz/\">#5 Thanksgiving Raised Petals</a>, <a href=\"https://www.instagram.com/reel/Dfy_GeIiYSU/\">#6 Thanksgiving Milky Chrome</a>.",
     "",
     "Instagram profile", "https://www.instagram.com/veneermonet/")

case("my-work/facebook-page-and-groups.html", "Facebook Page and Groups",
     "A new Page with no followers needed trust in real nail communities.",
     "I created the Page, published a pinned welcome post and a Reel, joined 38 nail groups as the Page, posting link-free look-only content where group rules allow it.",
     "Page live with pinned welcome post. Last 7 days to 10 Nov: 151 views, 92 unique viewers, 8 engagements, 0 followers. Group posts (re-check 11 Nov): 2 live, 8 pending, 8 removed, 3 declined, 4 could not post.",
     "A new Page's posts get filtered by group moderation — removals were about the Page having no group history, not about the content. So: clean look-only posts, no links, respect each group's rules, never repost removed content.",
     "Facebook Page", "https://www.facebook.com/veneermonet")

# ---- Evidence ----
page("evidence.html", "Evidence", META, """
<h1>Evidence</h1>
<p>The work on this site is real — live accounts, real numbers. Screenshots of each account are filed in the printed portfolio folder, behind the matching unit file, with the date and what each screenshot shows written underneath.</p>
<ul>
<li><strong>Pinterest</strong> — profile and scheduled pins: <a href="https://www.pinterest.com/veneermonet/">pinterest.com/veneermonet</a></li>
<li><strong>Gumroad store</strong> — 5 published products: <a href="https://veneermonet.gumroad.com/">veneermonet.gumroad.com</a></li>
<li><strong>Instagram</strong> — 6 Reels, profile customised: <a href="https://www.instagram.com/veneermonet/">instagram.com/veneermonet</a></li>
<li><strong>Facebook Page</strong> — pinned welcome post and Reel: <a href="https://www.facebook.com/veneermonet/">facebook.com/veneermonet</a></li>
<li><strong>Analytics</strong> — Google Analytics is active on this site (Measurement ID G-6Z69CGL8GR). Search Console verification is in progress — the Google Sites version of this site could not be verified (Google returned an "Internal error" 6 times), which is one reason this site was rebuilt here, where a real sitemap and meta description are possible.</li>
</ul>
<p>Nothing here is invented: where a result is still pending — the first sale, for example — it says so.</p>
""")

# ---- What I learned ----
page("what-i-learned.html", "What I Learned", META, """
<h1>What I Learned</h1>
<ul>
<li><strong>Distribution is the bottleneck.</strong> Each Pinterest pin gets a small seed audience, and saves widen it. Good content alone does not bring traffic.</li>
<li><strong>Schedule slowly, like a human</strong> — or the bot check triggers. Wait for pages and uploads to fully load, pause between pins.</li>
<li><strong>Title, image and overlay must match</strong>, or the pin confuses people. A pin should need no explanation.</li>
<li><strong>Frame illustrations as a blueprint advantage</strong>, not an apology for having no photos. The guides are illustrated workbooks — canvases, sizing profiles, ledgers and practice pages.</li>
<li><strong>Keep checkout simple for a digital product.</strong> Shipping fields do not belong on a download — I removed 4 of them from the Gumroad checkout.</li>
<li><strong>New Pages get filtered by group moderation.</strong> Removals were about the Page having no group history, not about the content — so clean look-only posts, no links, respect each group's rules, never repost removed content.</li>
<li><strong>Local SEO basics:</strong> Relevance, Proximity and Prominence decide local ranking; NAP (Name, Address, Phone) must stay identical everywhere; a Google Business Profile is set up in 7 steps and verified by Google before it can rank.</li>
</ul>
""")

# ---- Contact ----
page("contact.html", "Contact", META, f"""
<h1>Contact</h1>
<h2>Email</h2>
<p>Email: <a href="mailto:anisuranik6@gmail.com">anisuranik6@gmail.com</a></p>
<p>Phone: <a href="tel:+8801577809069">+8801577809069</a></p>
<h2>Elsewhere online</h2>
<ul>
<li>Pinterest: <a href="https://www.pinterest.com/veneermonet/">pinterest.com/veneermonet</a></li>
<li>Instagram: <a href="https://www.instagram.com/veneermonet/">instagram.com/veneermonet</a></li>
<li>Gumroad store: <a href="https://veneermonet.gumroad.com/">veneermonet.gumroad.com</a></li>
<li>Facebook: Md Anisur Rahman</li>
<li>LinkedIn: <a href="https://www.linkedin.com/in/anisurmarketer">linkedin.com/in/anisurmarketer</a></li>
</ul>
<p>Contact Md. Anisur Rahman, a digital marketer in Bangladesh, for Local SEO, Google Business Profile setup, email marketing and YouTube marketing. I reply to every message. For work enquiries, tell me your business type, your city, and what you want — more calls, more visits, or more sales.</p>
<h2>Send a message</h2>
<p><a class="button" href="{FORM}">Open the contact form</a></p>
""")

# ---- Home (fancy) ----
HOME_BODY = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Local SEO &amp; Digital Marketing Freelancer, Bangladesh | Md. Anisur Rahman</title>
<meta name="description" content="Digital marketer from Bangladesh. Local SEO, Google Business Profile, email marketing, YouTube marketing and Google Ads — with real work on Pinterest, Gumroad, Instagram and Facebook.">
<link rel="canonical" href="{BASE}/index.html">
{FONTS}
<link rel="stylesheet" href="styles.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','{GA}');</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Md. Anisur Rahman",
  "description": "Digital marketing freelancer in Cumilla, Bangladesh — local SEO, Google Business Profile, Search Console and Analytics, email marketing and video marketing.",
  "telephone": "+8801577809069",
  "url": "{BASE}",
  "address": {"@type": "PostalAddress", "addressLocality": "Cumilla", "addressCountry": "BD"},
  "areaServed": "Cumilla, Bangladesh",
  "knowsAbout": ["Local SEO", "Google Business Profile", "Google Search Console", "Google Analytics", "Email Marketing", "Video Marketing"],
  "sameAs": ["https://www.linkedin.com/in/anisurmarketer", "https://www.pinterest.com/veneermonet/", "https://veneermonet.gumroad.com/"]
}
</script>
<noscript><style>.loader{display:none}.idcard{left:50%;top:150px;margin-left:-125px}</style></noscript>
</head>
<body>
<div class="loader"><div class="tc"><b>&#9679; REC</b> <span>00:00:00:00</span></div></div>
<div class="progress"></div>
<nav class="navpill"><a class="brand-link" href="/index.html">Md. Anisur Rahman</a><a href="#work">Work</a><a href="#process">Process</a><a href="#about">About</a><a class="cta" href="#contact">Let&rsquo;s talk</a></nav>
<header class="hero wrap">
<div class="hero-text">
<span class="badge"><span class="dot"></span> Available for new projects</span>
<h1>Md. Anisur<br>Rahman</h1>
<p class="role">Digital Marketer &middot; Founder, Veneer Monet</p>
<p class="tagline">I help small businesses in Bangladesh get found on Google &mdash; and turn clicks into customers.</p>
<div class="actions"><a class="btn btn-cream" href="#work">See my work</a><a class="btn btn-ghost" href="#contact">Start a project</a></div>
<div class="tools"><span>Local SEO</span><span>Google Business Profile</span><span>Search Console</span><span>Analytics</span><span>Mailchimp</span><span>Pinterest</span></div>
</div>
<div class="idwrap">
<svg class="idstrap" aria-hidden="true"><path id="strapPath" d="M 0 0" fill="none" stroke="#ff3b2f" stroke-width="14"></path><text font-size="9" letter-spacing="2" fill="#f7f5f1" font-family="monospace"><textPath href="#strapPath" startOffset="0">DIGITAL MARKETER &#8226; MD. ANISUR RAHMAN &#8226; DIGITAL MARKETER &#8226; MD. ANISUR RAHMAN &#8226; DIGITAL MARKETER &#8226; MD. ANISUR RAHMAN &#8226; </textPath></text></svg>
<div class="idcard" id="idcard">
<div class="clip"></div><div class="slot"></div>
<div class="top"><span>CREW PASS</span><span class="rec">&#9679; REC</span></div>
<div class="photo"><img src="/assets/me-card.webp" alt="Md. Anisur Rahman"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i></div>
<div class="job">Digital Marketer</div>
<div class="job2">Founder, Veneer Monet</div>
<div class="name">Md. Anisur Rahman</div>
<div class="meta"><span>ID &middot; 2026</span><span>AR-01</span></div>
<div class="barcode"></div>
</div>
<p class="idcap">GRAB THE CARD &uarr;</p>
</div>
</header>
<div class="strip"><div class="strip-track"><span>Local SEO</span><i>&#10022;</i><span>Google Business Profile</span><i>&#10022;</i><span>Search Console</span><i>&#10022;</i><span>Google Analytics</span><i>&#10022;</i><span>Email Marketing</span><i>&#10022;</i><span>Video Marketing</span><i>&#10022;</i><span>Local SEO</span><i>&#10022;</i><span>Google Business Profile</span><i>&#10022;</i><span>Search Console</span><i>&#10022;</i><span>Google Analytics</span><i>&#10022;</i><span>Email Marketing</span><i>&#10022;</i><span>Video Marketing</span><i>&#10022;</i></div></div>
<section id="work" class="wrap">
<div class="sec-head"><div><p class="label">01 &mdash; Selected work</p><h2>Real work, honest numbers.</h2></div><a class="btn btn-ghost" href="/my-work/index.html">All case studies &rarr;</a></div>
<div class="work-grid">
<article class="work-card"><div class="num">63</div><p class="label">Pinterest Video Campaign</p><h3>A new brand, no audience.</h3><p>63 video pins in 3 weekly campaigns &mdash; 21 a week, 3 a day, one board. Each pin with its own creative, SEO title and destination link.</p><a href="/my-work/pinterest-video-campaign.html">Read the case study &rarr;</a></article>
<article class="work-card"><div class="num">5</div><p class="label">Gumroad Store &amp; Funnel</p><h3>A store that sells without a website.</h3><p>5 digital products &mdash; 3 full books at $9.99, a $3.99 starter pack, a free checklist &mdash; linked into a funnel: free &rarr; starter &rarr; full books.</p><a href="/my-work/gumroad-store-and-funnel.html">Read the case study &rarr;</a></article>
<article class="work-card"><div class="num">6</div><p class="label">Instagram Reels</p><h3>The same looks, a second audience.</h3><p>Campaign videos adapted into 9:16 Reels with book-specific captions and a bio link to the store.</p><a href="/my-work/instagram-reels.html">Read the case study &rarr;</a></article>
<article class="work-card"><div class="num">38</div><p class="label">Facebook Page &amp; Groups</p><h3>Trust in real nail communities.</h3><p>A new Page, a pinned welcome post, and 38 nail groups joined &mdash; link-free, look-only posts where the rules allow it.</p><a href="/my-work/facebook-page-and-groups.html">Read the case study &rarr;</a></article>
</div>
</section>
<section id="process" class="wrap">
<p class="label">02 &mdash; Process</p>
<h2>How a campaign comes together.</h2>
<div class="steps">
<div class="step"><p class="n">STEP 01</p><h3>Plan the week</h3><p>21 pins, 3 a day, one board. Every look matched to the book it teaches.</p></div>
<div class="step"><p class="n">STEP 02</p><h3>Make the creative</h3><p>Nails only, no hands. Title, image and overlay must match, or the pin confuses people.</p></div>
<div class="step"><p class="n">STEP 03</p><h3>Schedule slowly</h3><p>Like a human &mdash; wait for uploads, pause between pins, fill the tagged topics.</p></div>
<div class="step"><p class="n">STEP 04</p><h3>Measure honestly</h3><p>Impressions, saves, clicks. First sale still pending &mdash; stated, not hidden.</p></div>
</div>
</section>
<section id="about" class="wrap">
<div class="about-grid">
<div><div class="reveal"><img src="/assets/me-front.webp" alt="Md. Anisur Rahman, portrait"><img class="top" src="/assets/me-mask.webp" alt=""><div class="lens-ring"></div></div><p class="reveal-cap">HOVER THE PHOTO</p></div>
<div><p class="label">03 &mdash; About</p><h2>Marketing, learned by doing it.</h2><p>I&rsquo;m <strong>Md. Anisur Rahman</strong>, a digital marketing student in Bangladesh and the founder of Veneer Monet, a nail-art brand for beginners.</p><p>I learned digital marketing by doing it on my own brand first: I plan and publish Pinterest campaigns, run a Gumroad store with five digital products, publish Instagram Reels, and manage a Facebook Page. Everything on this site is my own work &mdash; real accounts, real numbers.</p><div class="pills"><span>Local SEO</span><span>Content planning</span><span>Honest numbers</span></div><p style="margin-top:22px"><a class="btn btn-ghost" href="/about.html">More about me &rarr;</a></p></div>
</div>
</section>
<section id="contact" class="wrap">
<div class="contact-card">
<p class="label">04 &mdash; Contact</p>
<h2>Let&rsquo;s get your business found.</h2>
<p class="lede">Local SEO, Google Business Profile setup, email marketing and YouTube marketing. I reply to every message.</p>
<div class="contact-row"><div><strong>Email</strong><br><a href="mailto:anisuranik6@gmail.com">anisuranik6@gmail.com</a></div><button class="copybtn" data-email="anisuranik6@gmail.com" type="button">Copy</button></div>
<div class="contact-row"><div><strong>Phone</strong><br><a href="tel:+8801577809069">+8801577809069</a></div><span class="muted">Cumilla, Bangladesh</span></div>
<div class="socials"><a href="https://www.pinterest.com/veneermonet/">Pinterest</a><a href="https://veneermonet.gumroad.com/">Gumroad</a><a href="https://www.instagram.com/veneermonet/">Instagram</a><a href="https://www.facebook.com/veneermonet/">Facebook</a><a href="https://www.linkedin.com/in/anisurmarketer">LinkedIn</a></div>
</div>
</section>
<footer><div class="wrap"><p>Md. Anisur Rahman &mdash; Digital Marketer, Cumilla, Bangladesh &middot; <a href="mailto:anisuranik6@gmail.com">anisuranik6@gmail.com</a> &middot; +8801577809069</p><p><a href="https://www.pinterest.com/veneermonet/">Pinterest</a> &middot; <a href="https://veneermonet.gumroad.com/">Gumroad</a> &middot; <a href="https://www.instagram.com/veneermonet/">Instagram</a> &middot; <a href="https://www.facebook.com/veneermonet/">Facebook</a> &middot; <a href="https://www.linkedin.com/in/anisurmarketer">LinkedIn</a></p></div></footer>
<div class="cur-dot" aria-hidden="true"></div><div class="cur-ring" aria-hidden="true"></div><div class="cur-halo" aria-hidden="true"></div>
<a class="goo" href="#contact">let&rsquo;s collab</a>
<script src="script.js" defer></script>
</body>
</html>
"""

def home_page():
    html = HOME_BODY.replace("{BASE}", BASE).replace("{GA}", GA).replace("{FONTS}", FONTS)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(html)

home_page()

# ---- CSS / robots / sitemap ----
with open(os.path.join(OUT, "styles.css"), "w") as f:
    f.write(CSS)

pages = ["", "about.html", "services.html", "my-work/index.html",
         "my-work/pinterest-video-campaign.html", "my-work/gumroad-store-and-funnel.html",
         "my-work/instagram-reels.html", "my-work/facebook-page-and-groups.html",
         "evidence.html", "what-i-learned.html", "contact.html"]
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in pages:
        loc = BASE + "/" + p if p else BASE + "/"
        f.write(f"  <url><loc>{loc}</loc></url>\n")
    f.write("</urlset>\n")

print("built", OUT)
print(sorted(os.listdir(OUT)))
print(sorted(os.listdir(os.path.join(OUT, "my-work"))))
print(sorted(os.listdir(os.path.join(OUT, "assets"))))
