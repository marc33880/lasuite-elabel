# E-Label — Zutaten und Nährwerte

Statische Pflichtangaben-Seiten für die Weine von Château LaSuite aux Conseillans.
Ziel der Verordnung (EU) 2021/2117: Weine ab Jahrgang 2024 tragen einen QR-Code,
der auf Zutatenverzeichnis und Nährwertdeklaration verweist.

Eine Seite je Wein, erreichbar über eine eigene Subdomain von `lasuite.vin`.
Alle Daten kommen aus den Shopify-Stammdaten; die ausgelieferte Seite ist
reines HTML ohne Shopify, ohne Framework, ohne Fremd-Request.

Stand dieser Dokumentation: **04.08.2026** — sie ist vollständig, das
Entscheidungsprotokoll am Ende hält auch die verworfenen Wege fest.

> **Welche Adresse gehört wohin?** → **[`URLS.md`](URLS.md)**. Wird von
> `build.py` erzeugt, damit sie nicht veralten kann.
>
> **Live-Stand 04.08.2026: die Seiten sind noch NICHT erreichbar.**
> `lasuite.vin` und beide Wein-Subdomains antworten mit `302` auf
> `https://chateaulasuite.com/` — eine Wildcard-Weiterleitung beim Registrar.
> Die gedruckten QR-Codes landen damit auf der Shop-Startseite statt auf der
> Pflichtangabe. Das ist der Zustand, den „Veröffentlichen" auflöst.

## Warum das nicht einfach eine Seite auf chateaulasuite.com ist

Weil der Leitfaden der EU-Kommission zum elektronischen Etikett
([C/2023/1190](https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=OJ:C_202301190))
es verbietet. Drei Punkte daraus:

* Auf der Zielseite dürfen **keine Nutzerdaten erhoben oder nachverfolgt**
  werden — „ausnahmslos", auch nicht mit Einwilligung.
* Die Pflichtangaben dürfen **nicht zusammen mit Informationen zu Verkaufs-
  oder Vermarktungszwecken** erscheinen; genannt werden ausdrücklich auch
  „Website-Links" und Werbung.
* Die Einbindung „einer E-Commerce-Website oder einer Weingut-Website wird
  ohne Zweifel als ‚Vermarktungszweck' betrachtet".

Eine Shopify-Storefront setzt Cookies, lädt Analytics und bringt Warenkorb und
Shop-Navigation mit. Deshalb ist dieses Projekt der einzige Teil der Website,
der **außerhalb** der Website liegt. Nicht aus technischer Vorliebe.

## Warum statisch

Der QR-Code ist auf Glas gedruckt und soll in 20 Jahren noch funktionieren.
Deshalb ist Shopify hier ausschließlich Redaktionswerkzeug, nicht Laufzeit:
der Build friert den Datenstand in HTML ein. Schrift, Logo und Flaschenbild
liegen lokal. Fällt Shopify oder ein CDN aus, bleibt die Seite unverändert
erreichbar. Zusätzlich landet jeder Datenstand als Archivkopie unter
`archive/`, was gegenüber einer Kontrollbehörde belegt, welcher Wert wann
online stand.

Als Nebeneffekt setzt die Seite keine Cookies und lädt keine Analytics —
was die Verordnung für das elektronische Etikett ohnehin verlangt.

Damit das nicht nur Absicht bleibt, prüft der Produktionsbau es nach:
`assert_selfcontained()` bricht ab, sobald ein `src="http`, ein `url(http`,
ein `@import` oder ein `<link>` auf eine fremde Adresse in der fertigen Seite
steht. Textlinks (`<a href>`) sind erlaubt, sie laden nichts.

## Aufbau der Seite

Die Reihenfolge ist eine Setzung, nicht Zufall:

| # | Block | Pflichtangabe? |
|---|---|---|
| 1 | Wortmarke | nein |
| 2 | Eyebrow „Zutaten und Nährwerte" | nein |
| 3 | Name des Weins, Jahrgang, `0,75 l · 12,5 % vol` | Alkoholgehalt ja |
| 4 | Fermate | nein |
| 5 | **Rebsorte(n)** — gestaffelte Bänder | nein |
| 6 | **Limitierung** — Anzahl Flaschen | nein |
| 7 | **Zutaten** | **ja** |
| 8 | **Nährwerte** je 100 ml | **ja** |
| 9 | Etikett | nein |
| 10 | Button auf die Story-Seite | nein |
| 11 | Erzeuger, Rechtsgrundlage, Stand, Sprachwahl | nein |

Das Freiwillige (5, 6) steht **vor** den Pflichtangaben und ist von ihnen durch
eigene Überschriften getrennt. Es darf nie in die Nährwerttabelle rutschen:
gegenüber einer Kontrolle ist die saubere Trennung von Pflicht und Kür das
Argument. Marketing (Preise, Bewertungen, Newsletter) hat auf dieser Seite
nichts zu suchen — siehe „Was bewusst nicht auf der Seite steht".

## Datenfelder in Shopify

Alle am Produkt. Namespace `elabel` ist für diese Seite angelegt und im
Produkt-Editor angepinnt; die `custom.*`-Felder sind **dieselben**, aus denen
die PDP ihre Faktenreihe und ihre Assemblage-Sektion baut — bewusst keine
Zweitpflege.

| Feld | Typ | Pflicht | Zweck |
|---|---|---|---|
| `elabel.slug` | Text, eindeutig | ja | Subdomain ohne `.lasuite.vin`, z. B. `loure2024-nutri` |
| `elabel.zutaten` | Rich Text, übersetzbar | ja | Zutatenverzeichnis, Allergene **fett** |
| `elabel.alcohol_vol` | Dezimalzahl | ja | Alkohol in % vol, z. B. `12.5` |
| `elabel.sugars_g_l` | Dezimalzahl | ja | Restzucker in g/l |
| `elabel.acid_g_l` | Dezimalzahl | nein | Gesamtsäure in g/l, verfeinert den Brennwert |
| `elabel.energy_kcal_100ml` | Dezimalzahl | nein | nur bei vorliegendem Laborwert |
| `custom.rebsorten` | Text | nein | Rebsorten — dasselbe Feld wie auf der PDP |
| `custom.flaschenanzahl` | Ganzzahl | nein | Limitierung — dasselbe Feld wie auf der PDP |
| `custom.harvest_year` | Ganzzahl | ja | Aufnahmeregel (siehe unten) |

Fett, gesättigte Fettsäuren, Eiweiß und Salz sind bei Wein konstant und stehen
fest im Template (`0 g`, `0 g`, `< 0,5 g`, `< 0,01 g`) — dafür braucht es kein
Datenfeld. Brennwert und Kohlenhydrate werden gerechnet.

Übersetzungen der Zutatenliste (fr/en) über *Translate & Adapt* am Metafeld.
Fehlt eine Übersetzung, greift die deutsche Fassung. Alle übrigen Wortlaute
liegen im Wörterbuch `T` in `build.py` und sind dort dreisprachig gepflegt —
nicht in Shopify.

### Zwei Absätze in `elabel.zutaten`

Der **erste** Absatz ist das Zutatenverzeichnis (`Trauben`). Jeder **weitere**
Absatz wird als Zusatzstoff- oder Hinweiszeile gesetzt: kleiner, leiser, mit
Abstand (`.ingredients p+p`) — damit der Klassenname nicht wie eine weitere
Zutat gelesen wird.

```
Trauben
Antioxidationsmittel: **Sulfite**
```

Warum der Klassenname trotzdem stehen bleibt: Zusatzstoffe sind nach Art. 18
i. V. m. Anhang VII Teil C VO (EU) 1169/2011 mit dem **Klassennamen**, gefolgt
von Bezeichnung oder E-Nummer, anzugeben. Der Schutzverband deutscher Wein
führt für Wein genau die Wortlaute *„Antioxidationsmittel: Schwefeldioxid"* und
*„Antioxidationsmittel: Sulfite"* als Beispiel. Zulässige Alternative wäre
`Konservierungsstoff: Sulfite` — E 220–228 gehören beiden Zusatzstoffklassen
an. Weglassen ist **keine** Alternative; gelöst ist der Konflikt typografisch,
nicht redaktionell.

Die Fettung von „Sulfite" ist die Allergen-Hervorhebung und ersetzt eine
separate Zeile „Enthält Sulfite" **im Zutatenverzeichnis**. Achtung, davon
unberührt: **auf dem gedruckten Etikett** muss „Enthält Sulfite" trotz
QR-Code weiterhin stehen — die Allergenangabe darf nicht nur digital erfolgen.

Quellen: [Schutzverband deutscher Wein, Rundschreiben 3-2023](https://www.schutzverband-deutscher-wein.de/downloads/Rundschreiben%203-2023%20Zutaten%20und%20N%C3%A4hrwertdeklaration%20UPDATE%20aktualisiert%2012.12.23.pdf),
[IT-Recht Kanzlei zur Wein-Zutatenkennzeichnung](https://www.it-recht-kanzlei.de/weinverkauf-gesetzliche-neuerungen-2023-zutatenverzeichnis-naehrwertangaben.html).

### Rebsorten

`custom.rebsorten`, Format wie auf der PDP: `55% Merlot, 25% Cabernet
Sauvignon, …`. `split_grapes()` trennt an Kommas und erkennt den Prozentwert
daran, dass der erste Abschnitt eine Ziffer enthält — steht keine Ziffer davor
(`Cabernet Sauvignon, Merlot`), gilt der ganze Abschnitt als Sortenname und
nichts wird abgeschnitten.

Dargestellt als **gestaffelte Bänder**: dieselbe Darstellung wie die
Assemblage-Sektion der PDP, größter Anteil oben und am höchsten, danach
abfallend bis zu einer Untergrenze von 44 px. Anders als die PDP schneidet die
Seite **nicht** nach vier Sorten ab — hier ist Information der Zweck.

Die Farben sind ein Spiegel von `snippets/lasuite-rebsorte-farbe.liquid`,
SSoT `00_Guidelines/Website/Rebsorten_Farbtabelle.md`. Zwei Regeln daraus
gelten hier genauso:

* Die **Reihenfolge der Prüfungen** ist bedeutsam. `cabernet franc` muss vor
  `cabernet` stehen, sonst gewinnt der falsche Treffer.
* Kein Treffer → graues Ausweichband (`--ls-mole` #8B857F). Ein Tippfehler im
  Metafeld wird so als grauer Streifen sichtbar, statt sich als falsche
  Rebsorte zu tarnen.

Helle Sorten (Sauvignon Blanc, Alvarinho, Sémillon) tragen die Beschriftung in
Tinte, dunkle in Weiß — Umschlagpunkt bei einer Wahrnehmungshelligkeit von 145,
identisch zur PDP (`on_color()`).

Rebsortennamen sind Eigennamen und werden **nicht** übersetzt (Sperrliste in
`11_Redesign_Crew/_i18n/TRANSLATION_BRIEF.md`). Nur die Überschrift wechselt,
Singular oder Plural je nach Anzahl:

| | 1 Sorte | mehrere |
|---|---|---|
| de | Rebsorte | Rebsorten |
| en | Grape variety | Grape varieties |
| fr | Cépage | Cépages |

Fehlt `custom.rebsorten`, entfällt der Block ersatzlos.

### Limitierung

`custom.flaschenanzahl` — eine **Zahl**, keine Zeichenkette mit „Flaschen"
darin (`to_int()` in `fetch_shopify.py` zieht notfalls die Ziffern heraus).
Einheit und Tausendertrennung setzt die Seite selbst:

| | Überschrift | Wert |
|---|---|---|
| de | Limitierung | `1.211 Flaschen` |
| en | Limited edition | `1,211 bottles` |
| fr | Édition limitée | `1 211 bouteilles` (geschütztes Leerzeichen) |

Typografisch greift der Block die Sprache der Rebsorten-Bänder auf — große
leichte Ziffer, kleine Versalien daneben — aber ohne Farbfläche, sonst hätte
die Reihe zwei konkurrierende Blöcke. Fehlt das Feld, entfällt der Block.

### Slug-Konvention

```
<wein>-<kennung>-nutri.lasuite.vin
```

* Jahrgangsweine: Kennung = Jahrgang → `gigue-2024-nutri`, `caprice-2025-nutri`
* Le-Ton-Familie: Kennung = `varN` → `le-ton-rouge-var5-nutri`
* Kleinbuchstaben, keine Akzente, Bindestrich als einziger Trenner
* kurz halten — die URL-Länge bestimmt die Dichte des gedruckten QR-Codes

Bereits gedruckt und deshalb **unveränderlich**: `loure2024-nutri`,
`le-ton-blanc-var5-nutri`.

## Gestaltung

Die Seite gehört nicht zum Theme (kein Liquid, kein Shopify zur Laufzeit),
folgt aber demselben Design-System: Jost in 200/300/400/500, Shell `#F1EFEA`
als Karte auf Paper `#E7E5DE`, Gold `#AC967C` für Linien und Marke, Tinte
`#2A2722`.

### Die Fermate

Das **echte** Zeichen, Pfad wörtlich aus `snippets/lasuite-fermate-svg.liquid`
übernommen (dort vektorisiert aus `Domaine_Assets/web_assets/brand-fermate.png`),
`viewBox 0 0 255 166`, 60 px breit, `currentColor` in Gold. Vorher stand hier
ein nachgezeichneter Bogen mit Punkt — er sah der Fermate nur ähnlich. Kein
Nachbau mehr: sonst driften Etikett und Website auseinander. Ändert sich die
Marke, wird der Pfad aus dem Snippet **neu kopiert**, nicht neu gezeichnet.

### Der Weg zur Story-Seite

Ein **Kasten-Button**, kein unterstrichener Link: 1 px Goldrahmen, im Hover
füllt er sich mit Tinte, der Pfeil wandert 4 px nach rechts. Begründung: hinter
dem Link liegt echter Mehrwert — die `?view=story-2`-Seite ist eine reine
Infoseite ohne Verkaufsteil.

Beschriftung, individualisiert je Wein:

* de — „Mehr über Herkunft und Geschichte des Louré 2024"
* en — „More on the origin and story of Louré 2024"
* fr — „En savoir plus sur l'origine et l'histoire du Louré 2024"

Der Name ist `name + vintage`. Bei der Le-Ton-Familie wird daraus „des Le Ton
blanc Variation 5" bzw. „du Le Ton blanc Variation 5" — grammatisch im
Französischen unschön. Wenn das stören soll, braucht es ein eigenes,
übersetzbares Metafeld für den Linknamen; bewusst **nicht** angelegt, solange
es nur eine Handvoll Weine betrifft.

„Rebsorten" ist aus dem Linktext verschwunden, seit die Rebsorten auf der Seite
selbst stehen — der Hinweis wäre redundant gewesen.

### Sprachumschaltung — eine Falle

Alle drei Sprachen liegen inline in derselben Datei, geschaltet über
`[data-lang]{display:none}` plus `html[lang="…"] [data-lang="…"]{display:revert}`.
Diese Regel hat eine höhere Spezifität als jede Komponenten-Regel hier.

**Folge:** ein `display:flex` auf einem Element, dessen Kinder `[data-lang]`-Spans
sind, wird überschrieben und wirkt nicht. Deshalb arbeitet der
Limitierungs-Block mit Inline-Elementen und `margin-left` statt mit Flex und
`gap`. Die Rebsorten-Bänder dürfen Flex benutzen, weil Sortennamen nicht
übersetzt werden und dort keine `[data-lang]`-Spans stehen.

Die Sprache wird per JavaScript aus `navigator.language` gesetzt, Fallback
Englisch; die Fußzeile erlaubt manuelles Umschalten. Ohne JavaScript bleibt es
bei `lang="de"` aus dem `<html>`-Tag — das ist der bewusste Fallback, keine
leere Seite.

### Größen

* Etikett: `min(60%, 196px)` — vorher 104 px, für den Bildzweck zu klein.
* Fermate: 60 px.
* Karte: `max-width: 30rem`.

## Barrierefreiheit

Der Inhalt dieser Seite ist Pflichtangabe. Lesbarkeit ist damit nicht
Geschmacksfrage, sondern Teil der Anforderung („leicht sichtbar, deutlich
lesbar").

* `--muted` von `#8E897F` auf **`#6A655C`** korrigiert. Der alte Wert lag bei
  3,0:1 auf Shell und damit unter WCAG AA. Der neue schafft Shell 5,1:1 und
  Paper 4,6:1 und bleibt warm. Betrifft Fußzeile, Tabellen-Caption,
  Sprachwahl.
* Die Spurenzeilen der Nährwerttabelle (`0 g`, `< 0,5 g`) trugen `#9C978E`
  (≈ 2,5:1) und tragen jetzt `--muted`. Sie bleiben leiser als die übrigen
  Zeilen, aber lesbar.
* Die Zusatzstoffzeile trägt `--ink-soft` `#5D574F` (6,2:1) statt `--muted` —
  sie ist Pflichtangabe und darf nicht die leiseste Zeile der Seite sein.
* `prefers-contrast: more` zieht `--muted` zusätzlich auf `#5D574F`.
* Der Hover des Buttons füllt mit Tinte, nicht mit Gold: `--gold-deep` als
  Fläche hinter 11-px-Versalien ergäbe nur 3,7:1.

**Offen, bewusst nicht geändert (Marc-Entscheidung 04.08.2026):** die kleinen
Überschriften (Eyebrow, `h2`, Jahrgang) stehen in `--gold-deep` `#8C785F` und
liegen damit bei ~3,35:1 — genau der Fall, für den das Theme in
`lasuite-tokens.liquid` V2.1 den Token `--ls-gold-text` `#584A39` eingeführt
hat. Ein Ersetzen wäre eine Zeile, verändert aber den Charakter der Seite.
Wer das später nachzieht: `--gold-deep` bleibt für Linien, Fermate und Pfeil;
nur die kleine Typografie wechselt.

## Brennwertberechnung

Nach VO (EU) 1169/2011 Anhang XIV; Berechnung aus Analysewerten ist zulässig,
Glycerin darf mit ca. 10 % des Alkohols (g/l) geschätzt werden.

| Bestandteil | kcal/g | kJ/g |
|---|---|---|
| Alkohol | 7,0 | 29 |
| Zucker | 4,0 | 17 |
| Glycerin (Polyol) | 2,4 | 10 |
| Organische Säuren | 3,0 | 13 |

Kohlenhydrate im Sinne der Verordnung = Zucker + mehrwertige Alkohole,
deshalb liegt der Kohlenhydratwert über dem Zuckerwert. Rundung: Brennwert
ganzzahlig, Gramm unter 10 auf 0,1 g, Salz auf 0,01 g.

Kontrolle: `python3 nutrition.py` prüft drei Referenzfälle
(trockener Weißwein, Rotwein, Süßwein).

## Aufnahmeregel

Ein Wein bekommt seine Seite automatisch, sobald `elabel.slug` gefüllt ist und
`custom.harvest_year >= 2024`. Kein Template, kein DNS-Eintrag, kein Deploy von
Hand. Fehlt `elabel.alcohol_vol`, wird der Wein übersprungen — ohne
Alkoholgehalt ist die Seite keine gültige Pflichtangabe.
`fetch_shopify.py` meldet am Ende, welche Weine warum übersprungen wurden.

## Bauen

```bash
export SHOPIFY_STORE=nqexu6-bs
export SHOPIFY_TOKEN=shpat_…        # Custom App: read_products, read_translations
python3 fetch_shopify.py            # -> wines.json
python3 fetch_assets.py             # -> assets/ (Jost, Logo, Etiketten)
LOCAL_ASSETS=1 python3 build.py     # -> dist/   (Produktionsfassung)
```

Ohne `LOCAL_ASSETS` zeigt der Build auf Google Fonts und das Shopify-CDN —
praktisch für die Vorschau, **nicht** für die Veröffentlichung. Nur der
Produktionslauf führt die Selbstprüfung `assert_selfcontained()` aus.

`python3 nutrition.py` prüft die Rechnung, `python3 build.py` ohne Argumente
baut die Vorschau. Die mitgelieferte `wines.json` enthält den zuletzt
geprüften Datenstand (Louré 2024, Le Ton blanc Variation 5) und wird beim
ersten echten `fetch_shopify.py` überschrieben.

## Veröffentlichen

### Aktueller Stand (04.08.2026)

**Nichts ist live.** Geprüft am 04.08.2026:

| Adresse | Antwort |
|---|---|
| `https://lasuite.vin/` | `302` → `https://chateaulasuite.com/` |
| `https://loure2024-nutri.lasuite.vin/` | `302` → `https://chateaulasuite.com/` |
| `https://le-ton-blanc-var5-nutri.lasuite.vin/` | `302` → `https://chateaulasuite.com/` |

Die Domain existiert, und es liegt eine **Wildcard-Weiterleitung** darauf, die
alles auf die Shop-Startseite schickt. Für die beiden bereits abgefüllten Weine
heißt das: der QR-Code auf dem Glas führt zur Startseite, nicht zur
Pflichtangabe. Das ist der Zustand, den die Veröffentlichung auflöst — und der
Grund, warum sie keine Kür ist.

### Der Weg (Marc-Entscheidung 04.08.2026)

Die Seiten liegen auf **GitHub Pages**, und bei **United Domains** steht je Wein
eine Weiterleitung darauf. Kein Cloudflare, kein neues Konto: der GitHub-Zugang
besteht schon, GitHub Pages ist für öffentliche Repositories kostenlos und
liefert reines HTML aus — ohne Cookies, ohne Analytics, ohne Warenkorb. Genau
das, was der Leitfaden verlangt.

**Das Repository ist hier der Hosting-Ort, nicht Automatisierung.** Das war in
einer früheren Fassung dieser Dokumentation unklar formuliert: es geht nicht um
Versionsverwaltung um ihrer selbst willen, sondern darum, dass GitHub Pages den
Inhalt eines Repositories als Website ausliefert.

Einmalig einzurichten:

1. Auf GitHub ein **öffentliches** Repository `lasuite-elabel` anlegen.
   Öffentlich, weil GitHub Pages im kostenlosen Tarif nur öffentliche
   Repositories ausliefert. Es ist nichts Geheimes darin — keine Zugänge,
   keine Preise, keine Kundendaten.
2. Den Inhalt von `dist/` hochladen (Web-Oberfläche: *Add file → Upload files*,
   Ordner hineinziehen).
3. *Settings → Pages → Source: Deploy from a branch*, Branch `main`, Ordner
   `/ (root)`. Nach ein bis zwei Minuten liegt die Seite unter
   `https://<konto>.github.io/lasuite-elabel/<slug>/`.
4. Bei United Domains je Wein eine Weiterleitung eintragen — die genauen
   Adressen stehen in [`URLS.md`](URLS.md). Die bestehende
   Wildcard-Weiterleitung auf `chateaulasuite.com` muss dabei weg oder
   hinter die einzelnen Einträge.

Deshalb sind alle Pfade in den Seiten **relativ** (`../assets/…`): so
funktioniert dieselbe Datei unter einer Subdomain, in einem Unterordner und
lokal geöffnet. Ein absoluter Pfad (`/assets/…`) würde auf GitHub Pages ins
Leere zeigen, weil die Seite dort in einem Unterordner liegt.

### Was das kostet — und wo der Haken sitzt

* **Ein zusätzlicher Sprung.** Der Gast scannt `loure2024-nutri.lasuite.vin`
  und wird auf `github.io` weitergeleitet. Der Leitfaden verlangt „sofortigen
  Zugang" ohne „Durchlaufen dazwischenliegender Websites". Eine technische
  301-Weiterleitung auf denselben Inhalt ist nach hiesigem Verständnis kein
  dazwischenliegender *Auftritt* — der heutige Zustand (Weiterleitung auf die
  Shop-Startseite) ist es dagegen eindeutig. Restrisiko: gering, aber nicht
  null.
* **Die sichtbare Adresse wechselt** auf `github.io`. Eine Frame-Weiterleitung
  würde das verbergen, bricht aber auf Mobilgeräten — deshalb nicht.
* **Abhängigkeit von der Weiterleitung des Registrars** über die Lebensdauer
  der Flasche. Wer das später auflösen will, legt die Seiten hinter einen
  Dienst, der beliebige Subdomains von `lasuite.vin` selbst bedienen kann; dann
  entfällt die Weiterleitung. `src/worker.js` und `wrangler.toml` liegen für
  diesen Fall im Repo, ungenutzt.

### Was bewusst NICHT eingerichtet wird

`.github/workflows/deploy.yml` baut die Seiten täglich neu aus den
Shopify-Stammdaten. Für zwei Weine, deren Zutaten und Nährwerte sich nach der
Abfüllung nie mehr ändern, ist das Maschinerie ohne Zweck — und sie bräuchte
einen Shopify-Zugang als Secret. **Nicht aktivieren.** Die Datei bleibt liegen,
falls das Repertoire später so wächst, dass Handarbeit lästig wird.

Der übliche Weg bei einem neuen Jahrgang ist stattdessen: Werte in Shopify
pflegen, `fetch_shopify.py` und `build.py` einmal laufen lassen, `dist/`
hochladen, eine Weiterleitung ergänzen. Zehn Minuten, ein- bis zweimal im Jahr.

## Was bewusst nicht auf der Seite steht

Keine Preise, keine Bewertungen, kein Newsletter, kein Social, kein Tracking,
kein Cookie-Banner, keine Schriftart von einem fremden Server, kein
Warenkorb.

### Der Story-Button — offener Punkt, bewusst offen

Der einzige Weg nach draußen führt auf die Story-Seite des Weins
(`?view=story-2`) — eine reine Infoseite ohne Verkaufsteil.

**Das ist rechtlich die angreifbarste Stelle der Seite.** Der Leitfaden nennt
„Website-Links" ausdrücklich als Vermarktungszweck und wertet die Einbindung
einer „E-Commerce-Website oder einer Weingut-Website" als solchen. Dass
`?view=story-2` selbst nichts verkauft, hilft nur begrenzt: die Adresse liegt
auf der Shop-Domain.

**Marc-Entscheidung 04.08.2026: der Button bleibt.** Begründung: hinter dem
Link liegt für den Gast echter Mehrwert, und die Zielseite enthält keinen
Verkaufsteil. Wer die Entscheidung später revidieren will, entfernt in
`build.py` den Block `.cta` und die Zeile `%(story)s` aus dem Template — es
hängt nichts anderes daran. Der Rest der Seite ist davon unberührt und
unstrittig.

Wer die Frage anwaltlich klären lassen möchte, braucht dafür drei Angaben: den
genauen Wortlaut des Buttons, die Ziel-URL, und den Hinweis, dass die
Zielseite keinen Warenkorb, keine Preise und keinen Bestellvorgang enthält —
aber Teil der Weingut-Website ist.

## Kopplungen an das Theme

Diese Seite lebt außerhalb des Themes, hängt aber an drei Stellen daran. Wer
dort etwas ändert, ändert es hier mit:

| Im Theme | Hier | Bei Änderung |
|---|---|---|
| `snippets/lasuite-fermate-svg.liquid` | Konstante `FERMATE` in `build.py` | Pfad neu kopieren |
| `snippets/lasuite-rebsorte-farbe.liquid` | `GRAPE_COLORS` in `build.py` | neue Sorte ergänzen, Prüfreihenfolge beachten |
| `sections/main-product-story.liquid` (Assemblage) | `grape_layers()` | Darstellung angleichen, wenn die PDP sie ändert |
| `custom.rebsorten`, `custom.flaschenanzahl` | `fetch_shopify.py` | Feldnamen sind geteilt, nicht umbenennen |

Ebenfalls geteilt, aber nur gelesen: das Wortlaut-Verbot für Rebsortennamen aus
`11_Redesign_Crew/_i18n/TRANSLATION_BRIEF.md` und die Farbtabelle
`00_Guidelines/Website/Rebsorten_Farbtabelle.md`.

**Noch zu tun (außerhalb dieses Repos):** ein Eintrag im Konsistenzregister der
Redesign-Crew, der diese vier Kopplungen festhält — sonst weiß die Theme-Seite
nichts von diesem Repo. Der fertige Text dafür liegt in
[`REGISTER-EINTRAG.md`](REGISTER-EINTRAG.md) und muss nur eingefügt werden.

## Entscheidungsprotokoll

**04.08.2026 — Grundgerüst.** Sechs Metafelder im Namespace `elabel` angelegt,
`fetch_shopify.py` / `nutrition.py` / `build.py` / Worker / Workflow gebaut,
erste Vorschau des Louré 2024.

**04.08.2026 — Marc-Durchgang 1.** Sechs Punkte:

1. *Fermate.* Der nachgezeichnete Bogen ist raus, das echte Zeichen aus dem
   Theme-Snippet ist drin.
2. *„Antioxidationsmittel".* Sollte weg oder ersetzt werden. Nach Prüfung der
   Rechtslage: der Klassenname ist Pflicht, Weglassen ist keine Option,
   `Konservierungsstoff` die einzige zulässige Alternative. Gelöst wurde es
   typografisch — eigene, leisere Zeile, „Sulfite" fett. Marc hat das so
   abgenommen.
3. *Rebsorten.* Neue Kategorie mit eigener Überschrift, gestaffelt wie auf der
   PDP, aus `custom.rebsorten`. Mit vier Sorten (Sarabande-Muster)
   gegengeprüft.
4. *Etikett.* 104 → 196 px.
5. *Linktext.* Individualisiert um den Weinnamen.
6. *Button.* Kasten statt unterstrichenem Link.

Nebenbei ohne Auftrag korrigiert: `--muted` und die Spurenzeilen auf WCAG AA.
Angeboten und **abgelehnt**: `--gold-deep` in der kleinen Typografie auf
`--ls-gold-text` ziehen.

**04.08.2026 — Marc-Durchgang 2.** Linktext auf „Mehr über **Herkunft und
Geschichte** des Louré 2024" geändert, weil „Rebsorten" nach Punkt 3 redundant
war. Limitierung als eigene Kategorie zwischen Rebsorten und Zutaten ergänzt,
Quelle `custom.flaschenanzahl`, Einheit und Tausendertrennung dreisprachig.
Dabei die `display:revert`-Falle der Sprachumschaltung gefunden und den Block
auf Inline-Elemente umgebaut.

**04.08.2026 — Finalisierung.** `assert_selfcontained()` als Selbstprüfung des
Produktionsbaus ergänzt, Produktionslauf mit lokalen Assets verifiziert (keine
Fremd-Requests), diese Dokumentation vollständig neu geschrieben.

**04.08.2026 — Adressen und Live-Prüfung.** Nachgemessen, was unter
`lasuite.vin` tatsächlich antwortet: eine Wildcard-Weiterleitung auf die
Shop-Startseite, also **keine** der beiden Seiten live, obwohl die QR-Codes
gedruckt sind. Daraus drei Ergänzungen:

* `URLS.md` wird beim Bauen generiert und beantwortet ein für alle Mal, welche
  Adresse gedruckt ist und was als Weiterleitungsziel gehört. Kein
  handgepflegtes Dokument, das veralten kann.
* `src/worker.js` kennt jetzt einen **zweiten, pfadbasierten Weg**
  (`…/loure2024-nutri/`). Ohne ihn liefe jede Registrar-Weiterleitung auf der
  Übersichtsseite auf statt beim Wein — der Fehler wäre erst am Glas
  aufgefallen.
* `REGISTER-EINTRAG.md` enthält den fertigen Text für das Konsistenzregister
  der Redesign-Crew, damit die Theme-Seite von den vier Kopplungen weiß.

**04.08.2026 — Kurskorrektur nach Rückfrage.** Marc hat zu Recht gefragt, warum
dieser Teil Infrastruktur braucht, die die ganze übrige Website nicht braucht.
Ergebnis der Prüfung:

* **Berechtigt:** die Trennung von der Website. Der Leitfaden C/2023/1190
  verbietet Tracking ausnahmslos und wertet Shop- und Weingut-Links als
  Vermarktung. Eine Shopify-Seite ist deshalb keine Option — das ist der Grund
  für das ganze Projekt und stand vorher nicht deutlich genug in dieser Datei.
* **Nicht berechtigt:** Cloudflare, die GitHub-Action, der tägliche Neubau, die
  Archivkopien. Cloudflare war meine Wahl, weil ich an Wildcard-Subdomains
  festhielt; mit einer Weiterleitung pro Wein — dem Weg, den Marc von Anfang an
  im Kopf hatte — braucht es das nicht. Die Automatik war Maschinerie für einen
  Fall, der zweimal im Jahr eintritt. Beides ist aus dem Weg genommen: der
  Worker liegt ungenutzt im Repo, die Action bleibt deaktiviert.
* **Neu nötig geworden:** relative Asset-Pfade, damit die Seiten in einem
  Unterordner laufen. Mit absoluten Pfaden hätte GitHub Pages leere Bilder und
  eine falsche Schrift gezeigt — der Fehler wäre erst nach dem Hochladen
  aufgefallen.
* Die Schrift Jost liegt jetzt **im Repo** (`assets/jost-*.woff2`, SIL OFL,
  Quelle `@fontsource/jost`), damit `fetch_assets.py` für die Veröffentlichung
  nicht mehr gebraucht wird. Es holt nur noch Logo und Etikettenbilder.
* Der Story-Button bleibt auf Marc-Entscheidung drin, das Risiko ist oben
  dokumentiert.
