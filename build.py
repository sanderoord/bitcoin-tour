#!/usr/bin/env python3
"""Build static site from Claude artifact exports.

src/<page>.html  (raw artifact HTML)  ->  docs/<path>/index.html + extracted images.
Artifact links are rewritten to relative site paths; data-URI images become files;
a tiny shim gives window.claude.use("downloads") a plain browser-download fallback.
"""
import base64, hashlib, pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "docs"
DOMAIN = "bitcointour.nl"  # GitHub Pages custom domain (docs/CNAME)

PAGES = {  # source file -> (artifact id, folder in site)
    "tour":   ("HPGNPKJHp2HLRRBsspzRwv", ""),
    "museum": ("K8fbvwiKExETBWXmh5t5iP", "museum"),
    "bitboy": ("LTzfAnd8n9J7U3J6jNWUZi", "bitboy"),
}

WRAP = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>'  # artifact page skeleton (doctype = standards mode; quirks mode breaks Lenis scrolling)

SHIM = """<script>/* static-hosting shim: downloads fallback, no db/user */
if(!window.claude){window.claude={use:async function(n){if(n!=="downloads")return null;return{save:async function(o){var u=URL.createObjectURL(o.data),a=document.createElement("a");a.href=u;a.download=o.filename||"download";document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},4000);}};}};}
</script>"""

SHARE = {  # link previews (WhatsApp, LinkedIn, X ...): title, description; image = og/<page>.jpg (1200x630)
    "tour":   ("Bitcoin Tour: snap bitcoin in zestien werelden",
               "Een reis langs geld dat niemand kan bijdrukken. Geen jargon, wel diepgang. Er komen nooit meer dan 21 miljoen bitcoin."),
    "museum": ("Museum ₿: de geschiedenis van bitcoin",
               "Van een pdf'je van negen pagina's tot geld waar hele landen op draaien. De echte momenten, als hologram in een oud gebouw."),
    "bitboy": ("Bitboy: vang de 21 munten",
               "Speel het pocketspel van Museum ₿. Vang de 21 munten die er ooit komen. Mis je er een, dan is hij voorgoed weg."),
}


def share_tags(name, folder):
    t, d = (x.replace("&", "&amp;").replace('"', "&quot;") for x in SHARE[name])
    url = f"https://{DOMAIN}/" + (folder + "/" if folder else "")
    img = f"https://{DOMAIN}/og/{name}.jpg"
    return (f'<meta name="description" content="{d}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Bitcoin Tour">'
            f'<meta property="og:locale" content="nl_NL"><meta property="og:url" content="{url}">'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
            f'<meta property="og:image" content="{img}"><meta property="og:image:secure_url" content="{img}">'
            f'<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200">'
            f'<meta property="og:image:height" content="630"><meta property="og:image:alt" content="{t}">'
            f'<meta name="twitter:card" content="summary_large_image"><link rel="canonical" href="{url}">')


def rel(from_dir, to_dir):
    up = "../" if from_dir else ""
    return up + (to_dir + "/" if to_dir else "") or "./"


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    for name, (aid, folder) in PAGES.items():
        html = (SRC / f"{name}.html").read_text(encoding="utf-8")
        dest = OUT / folder if folder else OUT
        (dest / "img").mkdir(parents=True, exist_ok=True)

        # 1. artifact links -> relative site paths
        for _, (tid, tfolder) in PAGES.items():
            target = rel(folder, tfolder) or "./"
            html = html.replace(f"https://claude.ai/artifact/{tid}", target)

        # 2. data-URI images -> files
        def extract(m):
            ext, b64 = m.group(1), m.group(2)
            data = base64.b64decode(b64)
            fn = f"img/{hashlib.sha1(data).hexdigest()[:12]}.{'jpg' if ext == 'jpeg' else ext}"
            (dest / fn).write_bytes(data)
            return fn
        html = re.sub(r"data:image/(jpeg|png|webp|gif|avif);base64,([A-Za-z0-9+/=]+)", extract, html)

        # 3. raw artifact source? wrap it in the page skeleton
        if not html.lstrip().lower().startswith("<!doctype"):
            html = WRAP + "\n" + html + "\n\n</body></html>"

        # 4. link-preview tags in <head>
        if name in SHARE:
            html = html.replace("</head>", share_tags(name, folder) + "</head>", 1)

        # 5. shim before first script
        html = html.replace("<script", SHIM + "<script", 1)

        if not any((dest / "img").iterdir()):
            (dest / "img").rmdir()
        (dest / "index.html").write_text(html, encoding="utf-8")
        left = re.findall(r"claude\.ai/artifact/\w+", html)
        print(f"{name:7} -> {dest.relative_to(ROOT)}/index.html  {len(html)//1024} KB  unmapped links: {sorted(set(left)) or 'none'}")
    (OUT / ".nojekyll").write_text("")
    if (ROOT / "og").exists():
        shutil.copytree(ROOT / "og", OUT / "og")
    (OUT / "CNAME").write_text(DOMAIN + "\n")


if __name__ == "__main__":
    build()
