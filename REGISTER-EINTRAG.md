# Eintrag für das Konsistenzregister der Redesign-Crew

Diesen Block in das Konsistenzregister im Workspace einfügen
(`11_Redesign_Crew/…`). Zweck: das Theme weiß bisher nicht, dass es ein
zweites Projekt gibt, das an vier seiner Stellen hängt. Ohne den Eintrag
verändert irgendwann jemand die Fermate oder die Rebsortenfarben, und das
gedruckte E-Label driftet still auseinander.

---

## E-Label lasuite.vin — externes Projekt mit Rückkopplung ins Theme

**Angelegt:** 04.08.2026
**Repo:** `marc33880/lasuite-elabel`
**Was es ist:** statische Pflichtangaben-Seiten (Zutaten und Nährwerte nach
VO (EU) 2021/2117), eine Subdomain je Wein unter `lasuite.vin`, gebaut aus den
Shopify-Stammdaten und ausgeliefert von einem Cloudflare Worker. Kein Liquid,
kein Shopify zur Laufzeit — Shopify ist dort nur Redaktionswerkzeug.

**Vier Kopplungen. Wer im Theme daran arbeitet, zieht sie dort nach:**

| Im Theme | Im E-Label-Repo | Bei Änderung |
|---|---|---|
| `snippets/lasuite-fermate-svg.liquid` | Konstante `FERMATE` in `build.py` | Pfad wörtlich neu kopieren, nicht neu zeichnen |
| `snippets/lasuite-rebsorte-farbe.liquid` | `GRAPE_COLORS` in `build.py` | neue Sorte ergänzen; Prüfreihenfolge beachten (`cabernet franc` vor `cabernet`) |
| `sections/main-product-story.liquid`, Assemblage-Sektion | `grape_layers()` in `build.py` | Darstellung angleichen, wenn die Staffelung sich ändert |
| Metafelder `custom.rebsorten`, `custom.flaschenanzahl` | `fetch_shopify.py` | Feldnamen sind geteilt — nicht umbenennen, nicht löschen |

**Zusätzlich gelesen, aber nicht kopiert:**

* `00_Guidelines/Website/Rebsorten_Farbtabelle.md` — SSoT der Sortenfarben
* `11_Redesign_Crew/_i18n/TRANSLATION_BRIEF.md` — Rebsortennamen sind
  Eigennamen und werden nicht übersetzt. Das gilt auf dem E-Label genauso;
  würde eine Sprachfassung sie übersetzen, fände die Farbtabelle die Sorte
  nicht mehr.

**Was das E-Label vom Theme bewusst NICHT übernimmt:**

* Keine Tokens per `lasuite-tokens.liquid` — die Seite muss ohne Shopify
  funktionieren, die Werte stehen deshalb als Kopie im CSS.
* Kein `--gold-deep` als Flächenfarbe hinter kleiner Schrift (3,7:1).
* `--muted` ist dort **dunkler** als im Theme (`#6A655C` statt `#8E897F`),
  weil der Seiteninhalt Pflichtangabe ist und WCAG AA erreichen muss.
  Offen im Theme wie im E-Label: `--gold-deep` in kleiner Typografie
  (~3,35:1) — im Theme gelöst durch `--ls-gold-text`, im E-Label auf
  Marc-Entscheidung 04.08.2026 zunächst unverändert gelassen.

**Berührungspunkt in der anderen Richtung:** der einzige ausgehende Link der
E-Label-Seite führt auf `?view=story-2` des jeweiligen Weins. Wird dieses
Template umbenannt oder abgeschafft, bricht der Link auf einer Seite, deren
Adresse auf Glas gedruckt ist. `STORY_VIEW` in `fetch_shopify.py` ist die
Stelle, die dann angepasst werden muss.
