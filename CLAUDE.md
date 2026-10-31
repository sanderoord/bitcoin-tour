# Bitcoin Tour – werkwijze

- Bron van waarheid: de Claude-artifacts (Tour HPGNPKJHp2HLRRBsspzRwv, Museum K8fbvwiKExETBWXmh5t5iP, Bitboy LTzfAnd8n9J7U3J6jNWUZi).
- Deploy: artifact-HTML (volledig, met doctype) → src/<tour|museum|bitboy>.html → `python3 build.py` → commit src/ + docs/ → push naar main.
- Nooit direct in docs/ editen; build.py overschrijft docs/ volledig.
- GitHub Pages serveert /docs op main, domein bitcointour.nl (docs/CNAME).

## Link previews
`build.py` zet Open Graph-tags (SHARE-dict) in elke pagina; afbeeldingen staan in `og/<page>.jpg` (1200x630, <300 KB) en worden naar `docs/og/` gekopieerd. Teksten aanpassen = SHARE in build.py.

## Zijspoor aanval (07b-d)
PRO-werelden aanval/zwerm/staat (camp-fu, 3D via mkKit). Cijfers: HR snapshot 1200 EH/s (live via mempool hashrate/3d op de site), S21 XP 270 TH/s/3,645 kW/€6000, stroom €0,05/kWh. Landen: Hashrate Index jan 2026.
