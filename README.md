# E-Label lasuite.vin — Quellcode

Dieser Zweig (`source`) enthält den Bauplan. Er wird von GitHub Pages **nicht**
ausgeliefert — veröffentlicht wird ausschließlich der Zweig `main`.

**Die verbindliche Anleitung ist [`E-LABEL_DOKUMENTATION.md`](E-LABEL_DOKUMENTATION.md).**
Dort stehen Aufbau, Datenfelder, Wortlaute, Farbtabellen, Nährwertformeln, die
Fallstricke und das Entscheidungsprotokoll. Für einen neuen Chat, der weitere
Weine anlegen soll, ist [`UEBERGABE_NEUER_CHAT.md`](UEBERGABE_NEUER_CHAT.md)
der Startpunkt.

## Dateien

| Datei | Zweck |
|---|---|
| `build.py` | erzeugt aus `wines.json` die fertigen Seiten nach `dist/` |
| `fetch_shopify.py` | holt die Stammdaten aus Shopify nach `wines.json` |
| `fetch_assets.py` | holt Logo und Etiketten nach `assets/` (Schrift liegt schon dort) |
| `nutrition.py` | Brennwert- und Kohlenhydratrechnung, mit Selbsttest |
| `wines.json` | zuletzt geprüfter Datenstand |
| `assets/jost-*.woff2` | Schrift Jost, SIL Open Font License (`OFL.txt`) |
| `src/worker.js`, `wrangler.toml` | ungenutzt — Cloudflare-Variante, aufgehoben |
| `.github/workflows/deploy.yml` | ungenutzt — **nicht aktivieren**, siehe Doku |

## Bauen

```bash
python3 nutrition.py                # Selbsttest der Rechnung
export SHOPIFY_STORE=nqexu6-bs
export SHOPIFY_TOKEN=shpat_…        # Custom App: read_products, read_translations
python3 fetch_shopify.py            # -> wines.json
# Logo und Etiketten als assets/logo.png bzw. assets/<slug>.jpg ablegen
LOCAL_ASSETS=1 python3 build.py     # -> dist/
```

**Reihenfolge beachten:** ohne die Bilder in `assets/` entstehen Seiten ohne
Bildverweise, und ein späteres Danebenlegen hilft nicht mehr. Der
Produktionslauf prüft zusätzlich selbst, dass keine fremde Ressource in der
fertigen Seite steht.

Der Inhalt von `dist/` ist das, was in den Zweig `main` gehört.
