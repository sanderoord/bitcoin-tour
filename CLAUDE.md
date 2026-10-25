# Bitcoin Tour – werkwijze

- Bron van waarheid: de Claude-artifacts (Tour HPGNPKJHp2HLRRBsspzRwv, Museum K8fbvwiKExETBWXmh5t5iP, Bitboy LTzfAnd8n9J7U3J6jNWUZi).
- Deploy: artifact-HTML (volledig, met doctype) → src/<tour|museum|bitboy>.html → `python3 build.py` → commit src/ + docs/ → push naar main.
- Nooit direct in docs/ editen; build.py overschrijft docs/ volledig.
- GitHub Pages serveert /docs op main, domein bitcointour.nl (docs/CNAME).
