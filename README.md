# Bitcoin Tour + Museum ₿

Live: GitHub Pages, served from `/docs` on `main`.

| Pad | Pagina | Bron (Claude artifact) |
|---|---|---|
| `/` | Bitcoin Tour | https://claude.ai/artifact/HPGNPKJHp2HLRRBsspzRwv |
| `/museum/` | Museum ₿ | https://claude.ai/artifact/K8fbvwiKExETBWXmh5t5iP |
| `/bitboy/` | Bitboy | https://claude.ai/artifact/LTzfAnd8n9J7U3J6jNWUZi |

## Werkwijze
De Claude-artifacts zijn de bron van waarheid. Nooit direct in `docs/` editen.

Deploy = Claude leest het artifact → `src/<pagina>.html` → `python3 build.py` → upload `src/` + `docs/` naar `main`.

`build.py` zet artifact-links om naar relatieve paden, haalt ingebakken beelden eruit naar `img/`, en voegt een download-fallback toe voor buiten Claude.
Bitboy's Hall of Fame (gedeelde database) werkt alleen binnen Claude; op de live site toont hij geen scores.
