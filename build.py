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

SHIM = """<script>/* static-hosting shim: downloads fallback, no db/user */
if(!window.claude){window.claude={use:async function(n){if(n!=="downloads")return null;return{save:async function(o){var u=URL.createObjectURL(o.data),a=document.createElement("a");a.href=u;a.download=o.filename||"download";document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},4000);}};}};}
</script>"""


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

        # 3. shim before first script
        html = html.replace("<script", SHIM + "<script", 1)

        if not any((dest / "img").iterdir()):
            (dest / "img").rmdir()
        (dest / "index.html").write_text(html, encoding="utf-8")
        left = re.findall(r"claude\.ai/artifact/\w+", html)
        print(f"{name:7} -> {dest.relative_to(ROOT)}/index.html  {len(html)//1024} KB  unmapped links: {sorted(set(left)) or 'none'}")
    (OUT / ".nojekyll").write_text("")
    (OUT / "CNAME").write_text(DOMAIN + "\n")


if __name__ == "__main__":
    build()
