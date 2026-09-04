# E-Label lasuite.vin — Dokumentation und Betriebsanleitung

**Stand:** 04.09.2026 · **Status:** live für Louré 2024 und Le Ton blanc Variation 5
(Bildverweise am 04.09.2026 nachgereicht — siehe Abschnitt 6)

Diese Datei ist die vollständige Grundlage für jeden späteren Chat. Sie ist
absichtlich ausführlich: der Vorgang wiederholt sich über Jahre, und der QR-Code
steht auf Glas. Alles, was man zum Neubau bräuchte, steht hier — auch die
Zahlenwerte und Farbtabellen, damit nichts verloren geht, wenn der Quellcode
einmal abhandenkommt.

---

## AUF EINEN BLICK

| | |
|---|---|
| **Was** | Pflichtangaben nach VO (EU) 2021/2117: Zutaten und Nährwerte, eine Seite je Wein, dreisprachig |
| **Wo** | `https://<slug>.lasuite.vin/` → weitergeleitet auf `https://marc33880.github.io/lasuite-elabel/<slug>/` |
| **Repo** | `marc33880/lasuite-elabel`, öffentlich · Zweig `main` = die Seiten · Zweig `source` = der Bauplan |
| **Live** | Louré 2024, Le Ton blanc Variation 5 |
| **Aufwand je neuer Wein** | ca. 10 Minuten, ein- bis zweimal im Jahr |

### Die sieben Regeln

1. **Kein Tracking, keine Cookies, keine fremden Ressourcen.** Rechtlich zwingend,
   nicht verhandelbar (Abschnitt 1).
2. **Nicht auf chateaulasuite.com.** Aus demselben Grund (Abschnitt 1).
3. **Erst Bilder nach `assets/`, dann bauen.** Sonst entstehen Seiten ohne
   Bildverweise (Abschnitt 6 — ist schon passiert).
4. **Alle Pfade relativ** (`../assets/…`), nie mit führendem Schrägstrich
   (Abschnitt 2).
5. **Flaschenzahl gegen das Etikett prüfen.** Wich bisher bei jedem Wein ab
   (Abschnitt 6).
6. **Gedruckte Slugs sind unveränderlich** (Abschnitt 3).
7. **Pflicht und Kür getrennt halten**, Freiwilliges steht davor, nie in der
   Nährwerttabelle (Abschnitt 4).

### Der eine offene Punkt (Stand 04.09.2026)

**Nährwerte der beiden Live-Seiten beruhen teilweise auf Platzhaltern** —
echte Analysewerte für Restzucker und Säure fehlen in Shopify, beim Le Ton
auch der Alkoholgehalt. Details in Abschnitt 8. Alles Übrige ist erledigt.

### Der Ablauf für einen neuen Wein

Metafelder in Shopify füllen → Slug festlegen → Etikettenbild besorgen →
Zahlen gegen das Etikett prüfen → Seite bauen → Marc lädt ins Repo →
Marc setzt die Weiterleitung → nachprüfen. Ausführlich in Abschnitt 5.

### Wie diese Datei zu lesen ist

| Abschnitt | Wofür |
|---|---|
| 1–2 | Hintergrund und Aufbau — einmal lesen, dann nachschlagen |
| 2b | **Welcher Wein braucht überhaupt eine Seite** — zuerst prüfen |
| 3–4 | Spezifikation: Datenfelder, Wortlaute, Farben, Formeln — Nachschlagewerk |
| 4b | Was die Werkzeuge können — **vor der Arbeit lesen** |
| 5 | Der Ablauf — **danach arbeiten** |
| 6 | Fehler, die schon passiert sind — **vorher lesen** |
| 7–9 | Kopplungen, offene Punkte, Protokoll |

---

## 1. Worum es geht

Verordnung (EU) 2021/2117 verlangt für Weine ab Jahrgang 2024 ein
Zutatenverzeichnis und eine Nährwertdeklaration. Beides darf elektronisch
bereitgestellt werden, über einen QR-Code auf dem Etikett. Dieses Projekt
liefert diese Pflichtangaben aus: eine statische Seite je Wein, dreisprachig,
unter einer eigenen Subdomain von `lasuite.vin`.

### Warum das NICHT auf chateaulasuite.com liegt

Der Leitfaden der EU-Kommission zum elektronischen Etikett
([C/2023/1190](https://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=OJ:C_202301190))
verbietet es. Drei Punkte daraus:

* Auf der Zielseite dürfen **keine Nutzerdaten erhoben oder nachverfolgt**
  werden — „ausnahmslos", auch nicht mit Einwilligung.
* Die Pflichtangaben dürfen **nicht zusammen mit Informationen zu Verkaufs-
  oder Vermarktungszwecken** erscheinen; genannt werden ausdrücklich auch
  „Website-Links" und Werbung.
* Die Einbindung „einer E-Commerce-Website oder einer Weingut-Website wird
  ohne Zweifel als ‚Vermarktungszweck' betrachtet".

Eine Shopify-Storefront setzt Cookies, lädt Analytics und bringt Warenkorb und
Shop-Navigation mit. Deshalb ist dies der einzige Teil des Webauftritts, der
außerhalb davon liegt. Das ist kein technischer Geschmack, sondern der Grund
für das ganze Projekt.

Zusätzlich verlangt der Leitfaden „sofortigen Zugang" ohne „Durchlaufen
dazwischenliegender Websites". Eine technische Weiterleitung auf denselben
Inhalt ist nach hiesigem Verständnis kein dazwischenliegender *Auftritt* —
eine Weiterleitung auf die Shop-Startseite wäre es eindeutig.

---

## 2. Wie es heute aufgebaut ist

```
QR-Code auf dem Glas
   │
   ▼
https://<slug>.lasuite.vin/            Subdomain bei United Domains
   │                                   HTTP-Weiterleitung (302)
   ▼
https://marc33880.github.io/lasuite-elabel/<slug>/
                                       GitHub Pages, statisches HTML
```

**Kein Cloudflare, keine Automatik, kein Server.** Beides war in einer früheren
Fassung vorgesehen und wurde wieder entfernt: Cloudflare nur, weil zunächst an
Wildcard-Subdomains festgehalten wurde; mit einer Weiterleitung pro Wein ist es
überflüssig. Die tägliche Neubau-Automatik war Maschinerie für einen Fall, der
ein- bis zweimal im Jahr eintritt.

### Das Repository

`github.com/marc33880/lasuite-elabel` — **öffentlich** (GitHub Pages liefert im
kostenlosen Tarif nur öffentliche Repositories aus). Es enthält nichts
Schützenswertes: keine Zugänge, keine Preise, keine Kundendaten.

GitHub Pages: *Settings → Pages → Deploy from a branch*, Branch `main`,
Ordner `/ (root)`.

Struktur:

```
index.html                        Fallback-Übersicht, fängt Tippfehler ab
<slug>/index.html                 eine Seite je Wein
assets/jost-200|300|400|500.woff2 Schrift, SIL Open Font License
assets/OFL.txt                    Lizenztext
assets/logo.png                   Wortmarke
assets/<slug>.jpg                 Etikett je Wein
.nojekyll                         leer; verhindert Jekyll-Verarbeitung
```

**Alle Pfade in den Seiten sind relativ** (`../assets/…`). Das ist zwingend:
die Seiten liegen bei GitHub Pages in einem Unterordner, ein absoluter Pfad
(`/assets/…`) zeigte dort ins Leere. Relativ funktionieren dieselben Dateien
unter einer Subdomain, in einem Unterordner und lokal geöffnet.

### Aktueller Live-Stand

| Wein | Slug | Gedruckte Adresse | Ziel |
|---|---|---|---|
| Louré 2024 | `loure2024-nutri` | `https://loure2024-nutri.lasuite.vin/` | `…/lasuite-elabel/loure2024-nutri/` |
| Le Ton blanc Variation 5 | `le-ton-blanc-var5-nutri` | `https://le-ton-blanc-var5-nutri.lasuite.vin/` | `…/lasuite-elabel/le-ton-blanc-var5-nutri/` |

Geprüft am 04.09.2026: beide Weiterleitungen antworten mit `302`, HTTPS greift
ohne Zertifikatsfehler. **Ein manueller Eingriff des United-Domains-Supports war
nicht nötig.**

Die Weiterleitung der Startseite `lasuite.vin` → `chateaulasuite.com` bleibt
bewusst bestehen (SEO). Sie stört die Subdomain-Einträge nicht. Hinweis: sie
läuft als `302`, also *temporär*, und vererbt damit kaum Linkkraft — für die
SEO-Absicht wäre eine `301` der richtige Typ.

---

## 2b. Welche Weine überhaupt eine Seite brauchen

**Die Regel:** maßgeblich ist die **Erzeugung (Vinifikation)**, nicht die
Abfüllung. Weine, die vor dem 08.12.2023 den erforderlichen Mindestalkohol- und
Säuregehalt erreicht haben, sind befreit — auch wenn sie erst Jahre später
abgefüllt oder freigegeben werden. **Ab Jahrgang 2024 gilt die Pflicht
ausnahmslos.**

Ein Sarabande 2016, der 2027 abgefüllt wird, braucht also **keine** Seite. Ein
Caprice 2024 braucht eine, sobald er in den Verkehr kommt.

Technisch abgebildet als `custom.harvest_year >= 2024`. Das ist deckungsgleich
mit der Regel und leicht konservativ.

**Kandidaten laut Shopify (Stand 04.09.2026):**

| Wein | Jahrgang | Stand |
|---|---|---|
| Louré 2024 | 2024 | **live** |
| Le Ton Variation blanc 5 | 2024 | **live** |
| Caprice 2024 | 2024 | offen |
| Allemande 2025 | 2025 | offen |
| Caprice 2025 | 2025 | offen |
| Prélude 2026 | 2026 | offen |
| Intermezzo 2026 | 2026 | offen |

Ein „Prélude 2025" existiert in Shopify nicht — angelegt sind Prélude 2023 und
Prélude 2026. Alle übrigen Weine (Gigue, Sarabande, Le Ton rouge 2–4, Prélude
2023, Caprice 2023) liegen vor dem Stichtag und brauchen nichts.

Quellen: [IT-Recht Kanzlei](https://www.it-recht-kanzlei.de/weinverkauf-gesetzliche-neuerungen-2023-zutatenverzeichnis-naehrwertangaben.html),
[Schutzverband deutscher Wein, Rundschreiben 3-2023](https://www.schutzverband-deutscher-wein.de/downloads/Rundschreiben%203-2023%20Zutaten%20und%20N%C3%A4hrwertdeklaration%20UPDATE%20aktualisiert%2012.12.23.pdf).

---

## 3. Datenfelder in Shopify

Alle am Produkt. Namespace `elabel` ist für dieses Projekt angelegt und im
Produkt-Editor angepinnt. Die `custom.*`-Felder sind **dieselben**, aus denen
die Produktseite ihre Faktenreihe und ihre Assemblage-Sektion baut — bewusst
keine Zweitpflege.

| Feld | Typ | Pflicht | Zweck |
|---|---|---|---|
| `elabel.slug` | Text, eindeutig | ja | Subdomain ohne `.lasuite.vin` |
| `elabel.zutaten` | Rich Text, übersetzbar | ja | Zutatenverzeichnis, Allergene **fett** |
| `elabel.alcohol_vol` | Dezimalzahl | ja | Alkohol in % vol, z. B. `12.5` |
| `elabel.sugars_g_l` | Dezimalzahl | ja | Restzucker in g/l |
| `elabel.acid_g_l` | Dezimalzahl | nein | Gesamtsäure in g/l, verfeinert den Brennwert |
| `elabel.energy_kcal_100ml` | Dezimalzahl | nein | nur bei vorliegendem Laborwert |
| `custom.rebsorten` | Text | nein | z. B. `55% Merlot, 25% Cabernet Sauvignon` |
| `custom.flaschenanzahl` | Ganzzahl | nein | Limitierung |
| `custom.harvest_year` | Ganzzahl | ja | Aufnahmeregel |

**Aufnahmeregel:** ein Wein bekommt eine Seite, wenn `elabel.slug` gefüllt ist
und `custom.harvest_year >= 2024`. Fehlt `elabel.alcohol_vol`, wird er
übersprungen — ohne Alkoholgehalt ist die Seite keine gültige Pflichtangabe.

Übersetzungen der Zutatenliste (en/fr) über *Translate & Adapt* am Metafeld.
Fehlt eine, greift die deutsche Fassung. Alle übrigen Wortlaute stehen fest im
Generator, nicht in Shopify.

### Slug-Konvention

```
<wein>-<kennung>-nutri
```

* Jahrgangsweine: Kennung = Jahrgang → `gigue-2024-nutri`
* Le-Ton-Familie: Kennung = `varN` → `le-ton-rouge-var5-nutri`
* Kleinbuchstaben, keine Akzente, Bindestrich als einziger Trenner
* kurz halten — die URL-Länge bestimmt die Dichte des gedruckten QR-Codes

**Bereits gedruckt und damit unveränderlich:** `loure2024-nutri`,
`le-ton-blanc-var5-nutri`.

---

## 4. Aufbau der Seite

| # | Block | Pflichtangabe? |
|---|---|---|
| 1 | Wortmarke | nein |
| 2 | Eyebrow „Zutaten und Nährwerte" | nein |
| 3 | Name, Jahrgang, `0,75 l · 12,5 % vol` | Alkoholgehalt ja |
| 4 | Fermate | nein |
| 5 | **Rebsorte(n)** — gestaffelte Bänder | nein |
| 6 | **Limitierung** — Anzahl Flaschen | nein |
| 7 | **Zutaten** | **ja** |
| 8 | **Nährwerte** je 100 ml | **ja** |
| 9 | Etikett | nein |
| 10 | Button auf die Story-Seite | nein |
| 11 | Erzeuger, Rechtsgrundlage, Stand, Sprachwahl | nein |

Das Freiwillige (5, 6) steht **vor** den Pflichtangaben, durch eigene
Überschriften getrennt. Es darf nie in die Nährwerttabelle rutschen: gegenüber
einer Kontrolle ist die saubere Trennung von Pflicht und Kür das Argument.

### Zutaten: die Zwei-Absatz-Regel

Der **erste** Absatz von `elabel.zutaten` ist das Zutatenverzeichnis
(`Trauben`). Jeder **weitere** Absatz wird kleiner, leiser und mit Abstand
gesetzt (`.ingredients p+p`), damit der Klassenname nicht wie eine weitere
Zutat gelesen wird:

```
Trauben
Antioxidationsmittel: **Sulfite**
```

Der Klassenname bleibt, weil er Pflicht ist: Zusatzstoffe sind nach Art. 18
i. V. m. Anhang VII Teil C VO (EU) 1169/2011 mit dem Klassennamen, gefolgt von
Bezeichnung oder E-Nummer, anzugeben. Der Schutzverband deutscher Wein führt
für Wein die Wortlaute *„Antioxidationsmittel: Schwefeldioxid"* und
*„Antioxidationsmittel: Sulfite"* als Beispiel. Zulässige Alternative wäre
`Konservierungsstoff: Sulfite` (E 220–228 gehören beiden Klassen an).
**Weglassen ist keine Alternative** — der Konflikt wurde typografisch gelöst,
nicht redaktionell.

Die Fettung von „Sulfite" ist die Allergen-Hervorhebung und ersetzt die Zeile
„Enthält Sulfite" *im Zutatenverzeichnis*. Davon unberührt: **auf dem
gedruckten Etikett** muss „Enthält Sulfite" trotz QR-Code weiterhin stehen,
die Allergenangabe darf nicht nur digital erfolgen.

### Rebsorten

Format wie auf der Produktseite: `55% Merlot, 25% Cabernet Sauvignon, …`.
Getrennt wird an Kommas; ein Prozentwert wird daran erkannt, dass der erste
Abschnitt eine Ziffer enthält. Steht keine Ziffer davor, gilt der ganze
Abschnitt als Sortenname.

Dargestellt als **gestaffelte Bänder** wie in der Assemblage-Sektion der
Produktseite: größter Anteil oben und am höchsten, danach abfallend.
Höhen: erstes Band `clamp(86px,18vw,112px)`, danach `64px` minus 6 px je
Position, Untergrenze 44 px. Anders als die Produktseite wird **nicht** nach
vier Sorten abgeschnitten — hier ist Information der Zweck.

Rebsortennamen sind Eigennamen und werden **nicht** übersetzt (Sperrliste im
TRANSLATION_BRIEF). Nur die Überschrift wechselt, Singular oder Plural je nach
Anzahl: `Rebsorte`/`Rebsorten` · `Grape variety`/`Grape varieties` ·
`Cépage`/`Cépages`.

**Farbtabelle** (Spiegel von `snippets/lasuite-rebsorte-farbe.liquid`, SSoT
`00_Guidelines/Website/Rebsorten_Farbtabelle.md`). Die Reihenfolge der
Prüfungen ist bedeutsam — `cabernet franc` muss vor `cabernet` stehen:

| Prüfung (Kleinschreibung, enthält) | Farbe |
|---|---|
| `cabernet` + `franc` + `sauvignon` | `#5C5C74` |
| `cabernet franc` | `#77697E` |
| `cabernet` | `#45536A` |
| `merlot` | `#8A3B40` |
| `malbec` / `côt` / `cot` | `#6E4356` |
| `castet` | `#3B4652` |
| `alvarinho` / `albariño` / `albarino` | `#C6CBAE` |
| `sémillon` / `semillon` | `#DFCF9B` |
| `sauvignon` | `#A2AC85` |
| kein Treffer | `#8B857F` (grau — ein Tippfehler wird sichtbar) |

Beschriftung: Tinte `#2A2722`, wenn die Wahrnehmungshelligkeit
`(r*299 + g*587 + b*114)/1000` über 145 liegt, sonst Weiß.

### Limitierung

`custom.flaschenanzahl` als **Zahl**, ohne das Wort „Flaschen". Einheit und
Tausendertrennung setzt der Generator:

| | Überschrift | Wert |
|---|---|---|
| de | Limitierung | `1.211 Flaschen` |
| en | Limited edition | `1,211 bottles` |
| fr | Édition limitée | `1 211 bouteilles` (geschütztes Leerzeichen) |

Typografisch greift der Block die Sprache der Rebsorten-Bänder auf — große
leichte Ziffer, kleine Versalien daneben — aber ohne Farbfläche.

> **Achtung, Fallstrick:** die Sprachumschaltung arbeitet mit
> `[data-lang]{display:none}` plus `html[lang="…"] [data-lang="…"]{display:revert}`.
> Diese Regel hat höhere Spezifität als jede Komponenten-Regel. Ein `display:flex`
> auf einem Element, dessen Kinder `[data-lang]`-Spans sind, wirkt **nicht**.
> Deshalb arbeitet der Limitierungs-Block mit Inline-Elementen und `margin-left`
> statt mit Flex und `gap`. Die Rebsorten-Bänder dürfen Flex benutzen, weil dort
> keine `[data-lang]`-Spans stehen.

### Brennwertberechnung

Nach VO (EU) 1169/2011 Anhang XIV. Berechnung aus Analysewerten ist zulässig;
Glycerin darf mit ca. 10 % des Alkohols (g/l) geschätzt werden.

| Bestandteil | kcal/g | kJ/g |
|---|---|---|
| Alkohol | 7,0 | 29 |
| Zucker | 4,0 | 17 |
| Glycerin (Polyol) | 2,4 | 10 |
| Organische Säuren | 3,0 | 13 |

Kohlenhydrate im Sinne der Verordnung = Zucker + mehrwertige Alkohole, deshalb
liegt der Kohlenhydratwert über dem Zuckerwert. Rundung: Brennwert ganzzahlig,
Gramm unter 10 auf 0,1 g, Salz auf 0,01 g.

Konstant und fest im Template, kein Datenfeld nötig:
Fett `0 g` · davon gesättigte `0 g` · Eiweiß `< 0,5 g` · Salz `< 0,01 g`.

Kontrollwerte zum Gegenrechnen:

| Wein | Alkohol | Zucker | Säure | Ergebnis |
|---|---|---|---|---|
| Louré 2024 | 12,5 % | 1,5 g/l | 5,4 g/l | 306 kJ / 74 kcal · KH 1,1 g · Zucker 0,2 g |
| Le Ton blanc Var. 5 | 13,0 % | 1,5 g/l | 5,4 g/l | 317 kJ / 77 kcal · KH 1,2 g · Zucker 0,2 g |

### Gestaltung

Jost 200/300/400/500. Shell `#F1EFEA` als Karte auf Paper `#E7E5DE`, Gold
`#AC967C` für Linien und Marke, Tinte `#2A2722`, weiche Tinte `#5D574F`,
gedämpft `#6A655C`, Linien `rgba(42,39,34,.13)`. Karte `max-width: 30rem`.

**Die Fermate** ist das echte Zeichen, Pfad wörtlich aus
`snippets/lasuite-fermate-svg.liquid` (dort vektorisiert aus
`Domaine_Assets/web_assets/brand-fermate.png`), `viewBox 0 0 255 166`, 60 px
breit, Gold. **Kein Nachbau** — sonst driften Etikett und Website auseinander.
Ändert sich die Marke, wird der Pfad neu kopiert, nicht neu gezeichnet.

**Das Etikett** wird mit `min(60%, 196px)` dargestellt. Fehlt die Bilddatei,
entfällt das Element ganz — ein Icon für ein kaputtes Bild untergräbt das
Vertrauen mehr als eine fehlende Abbildung.

**Der Button** zur Story-Seite: 1 px Goldrahmen, im Hover mit Tinte gefüllt,
Pfeil wandert. Beschriftung individualisiert:
„Mehr über Herkunft und Geschichte des Louré 2024" ·
„More on the origin and story of …" ·
„En savoir plus sur l'origine et l'histoire du …".

### Barrierefreiheit

Der Inhalt ist Pflichtangabe; Lesbarkeit ist Teil der Anforderung.

* `--muted` liegt bei `#6A655C` (Shell 5,1:1, Paper 4,6:1). Der ursprüngliche
  Wert `#8E897F` erreichte nur 3,0:1.
* Spurenzeilen der Nährwerttabelle tragen `--muted` statt `#9C978E` (2,5:1).
* Die Zusatzstoffzeile trägt `--ink-soft` `#5D574F` (6,2:1).
* Der Button-Hover füllt mit Tinte, nicht mit Gold — Gold als Fläche hinter
  11-px-Versalien ergäbe nur 3,7:1.

**Offen, bewusst nicht geändert (Marc-Entscheidung 04.08.2026):** die kleinen
Überschriften stehen in `--gold-deep` `#8C785F`, also bei ~3,35:1. Das Theme
hat dafür in `lasuite-tokens.liquid` V2.1 den Token `--ls-gold-text` `#584A39`
eingeführt. Ein Wechsel wäre eine Zeile, verändert aber den Charakter der Seite.

### Selbstprüfung

Der Produktionsbau ruft `assert_selfcontained()` auf und bricht ab, sobald ein
`src="http`, ein `url(http`, ein `@import` oder ein `<link>` auf eine fremde
Adresse in der fertigen Seite steht. Textlinks (`<a href>`) sind erlaubt, sie
laden nichts. Damit bleibt die Zusage „kein Fremd-Request, kein Cookie, kein
Tracking" überprüfbar statt bloß beabsichtigt.

---

## 4b. Was die Werkzeuge können — und was nicht

Geprüft am 04.09.2026. Diese Grenzen bestimmen den Ablauf und sind kein
Versehen, das man umgehen könnte:

| Werkzeug | Kann | Kann nicht |
|---|---|---|
| Shopify (MCP) | Produkte, Metafelder, Übersetzungen lesen und schreiben | Bilddateien hochladen |
| GitHub (MCP) | Repository-Inhalt **lesen** | **schreiben** (403) und Repositories anlegen (403) |
| Web-Abruf | Live-Adressen prüfen, Weiterleitungen verfolgen | Bilder vom Shopify-CDN laden |
| Container-Shell | Python, Pillow, Playwright, Seiten bauen | kein Netz zum Shopify-CDN |
| Rechner-Bridge | Dateien auf Marcs Rechner lesen und schreiben | ebenfalls kein Netz |

**Daraus folgt der Arbeitsteilung:** Claude baut, prüft und liefert die
Dateien; Marc lädt sie über die GitHub-Web-Oberfläche hoch und setzt die
Weiterleitung. Das Etikettenbild kommt von Marc, weil kein Werkzeug ans CDN
kommt.

**Der Container ist flüchtig.** Er wurde während der Erstellung schon einmal
zurückgesetzt und alle Arbeitsdateien waren weg. Zwischenergebnisse deshalb
zeitnah ausliefern.

## 5. Einen neuen Wein anlegen

**Voraussetzung:** die Metafelder aus Abschnitt 3 sind am Produkt gefüllt und
`custom.harvest_year >= 2024`.

1. **Slug festlegen** nach der Konvention und in `elabel.slug` eintragen.
   Er wird auf Glas gedruckt und ist danach unveränderlich.
2. **Daten aus Shopify holen** und die Nährwerte rechnen lassen.
3. **Etikettenbild besorgen.** Der Claude-Container hat keinen Zugang zum
   Shopify-CDN — das Bild muss aus Shopify heruntergeladen und im Chat
   angehängt werden. Zielname: `<slug>.jpg`.
4. **Zahlen gegen das Etikett prüfen.** Siehe Abschnitt 6 — dieser Schritt hat
   sich bereits zweimal ausgezahlt.
5. **Seite bauen** — erst nachdem Logo und Etikett in `assets/` liegen, sonst
   fehlen die Bildverweise im HTML (siehe Abschnitt 6). Gegenprobe: die Datei
   muss `<div class="brand"><img` und `<figure><img` enthalten.
   Dann `<slug>/index.html` und `assets/<slug>.jpg` **an Marc ausliefern**;
   hochladen muss er, Claude hat keinen Schreibzugriff. Nichts an den
   bestehenden Dateien ändern.
6. **Weiterleitung bei United Domains** anlegen: Subdomain `<slug>`, Ziel
   `https://marc33880.github.io/lasuite-elabel/<slug>/`, Typ **HTTP 301/302**,
   **keine** Frame-Weiterleitung, Schrägstrich am Ende. Das macht Marc.
7. **Nachprüfen:** die gedruckte Adresse abrufen, den Inhalt gegenlesen,
   Etikett und Schrift im Browser ansehen, an der echten Flasche scannen.

**Zeitbedarf:** rund zehn Minuten. Der Vorgang fällt ein- bis zweimal im Jahr an.

---

## 6. Erfahrungen, die Zeit gekostet haben

**Die Flaschenzahl auf dem Etikett gegen `custom.flaschenanzahl` prüfen.**
Bei beiden bisherigen Weinen wich sie ab: das Etikett trug 1011 bzw. 1123,
Shopify 1211 bzw. 1389. Korrigiert wurden die Etiketten. Der Gast hält beim
Scannen die Flasche in der Hand — eine Zahl, die dem Etikett widerspricht,
liest sich wie ein Fehler. Der Ziffernstand ist auf dem Bild klein; zum Prüfen
den Bereich links unten vierfach vergrößern.

**Erst die Bilder nach `assets/` legen, dann bauen.** Der Generator lässt ein
fehlendes Bild bewusst weg, statt ein kaputtes Bild-Icon zu zeigen. Baut man,
bevor `logo.png` und `<slug>.jpg` dort liegen, entstehen Seiten **ohne**
`<img>`-Verweise — und die Bilder später danebenzulegen hilft nicht mehr, weil
das HTML sie nicht erwähnt. Genau so gingen die beiden ersten Seiten am
04.09.2026 ohne Wortmarke und ohne Etikett live; der Fehler fiel erst beim
Nachbauen aus dem Quellcode auf. **Gegenprobe vor dem Ausliefern:** die fertige
Datei muss `<div class="brand"><img` und `<figure><img` enthalten.

**Absolute Pfade brechen bei GitHub Pages.** Die Seiten liegen dort in einem
Unterordner. Mit `/assets/…` wären Bilder und Schrift leer geblieben, und der
Fehler wäre erst nach dem Hochladen aufgefallen.

**Beim Hochladen muss der *Inhalt* des Ordners in den Browser gezogen werden,
nicht der Ordner.** Sonst entsteht eine Ebene zu viel und keine Adresse
stimmt mehr. Vor dem Einschalten von Pages im Repo nachsehen: oben müssen
`assets`, `index.html` und die Wein-Ordner stehen.

**`.nojekyll` ist unter Windows versteckt** und kommt beim Markieren oft nicht
mit. Sie muss nachgelegt werden.

**United Domains braucht für HTTPS-Weiterleitungen keinen Support-Eingriff.**
Am 04.09.2026 geprüft: beide Subdomains lösen ohne Zertifikatsfehler auf.

---

## 7. Kopplungen an das Theme

Dieses Projekt lebt außerhalb des Themes, hängt aber an vier Stellen daran.
Wer dort arbeitet, zieht es hier nach:

| Im Theme | Hier | Bei Änderung |
|---|---|---|
| `snippets/lasuite-fermate-svg.liquid` | Konstante `FERMATE` | Pfad wörtlich neu kopieren |
| `snippets/lasuite-rebsorte-farbe.liquid` | Farbtabelle (Abschnitt 4) | Sorte ergänzen, Prüfreihenfolge beachten |
| `sections/main-product-story.liquid`, Assemblage | Rebsorten-Staffelung | Darstellung angleichen |
| `custom.rebsorten`, `custom.flaschenanzahl` | Datenabruf | Feldnamen sind geteilt, nicht umbenennen |

Ebenfalls gelesen: `00_Guidelines/Website/Rebsorten_Farbtabelle.md` und
`11_Redesign_Crew/_i18n/TRANSLATION_BRIEF.md` (Rebsortennamen nicht übersetzen).

Berührungspunkt in der anderen Richtung: der einzige ausgehende Link führt auf
`?view=story-2` des jeweiligen Weins. Wird dieses Template umbenannt oder
abgeschafft, bricht ein Link auf einer Seite, deren Adresse auf Glas gedruckt
ist.

**Offener Punkt:** ein Eintrag im Konsistenzregister der Redesign-Crew, der
diese Kopplungen festhält. Der fertige Text lag in `REGISTER-EINTRAG.md`.

---

## 8. Offene Punkte

| Punkt | Stand |
|---|---|
| **Nährwerte beruhen auf Platzhaltern** | Die `elabel`-Felder für Restzucker und Säure sind bei beiden Live-Weinen **leer**, beim Le Ton auch `alcohol_vol`. `fetch_shopify.py` wurde nie mit echtem Zugang ausgeführt; die Werte in `wines.json` (Zucker 1,5 g/l, Säure 5,4 g/l, Le Ton 13,0 % vol) stammen aus der Vorschau. Daraus werden Brennwert und Kohlenhydrate gerechnet. **Zu tun:** echte Analysewerte eintragen, Seiten neu bauen, hochladen. Der Alkoholgehalt des Le Ton ist der dringlichste Wert — er steht auch auf dem gedruckten Etikett. |
| Story-Button rechtlich | Marc-Entscheidung 04.08.2026: bleibt drin. Der Leitfaden nennt „Website-Links" als Vermarktungszweck; die Zielseite hat keinen Verkaufsteil, liegt aber auf der Shop-Domain. Zum Entfernen: Block `.cta` und die Zeile `%(story)s` aus dem Template nehmen. |
| `--gold-deep` in kleiner Typografie | ~3,35:1, unter WCAG AA. Bewusst nicht geändert. |
| ~~Le Ton: Produktbild und Alternativtext~~ | **Erledigt am 04.09.2026:** `Le_Ton_blanc_Variation_5.jpg` ist gesetzt, Alternativtext angeglichen. |
| Szenenbilder Louré | `Loure_freigestellt.png`, `Loure_Tischszene.png` — laut Marc nicht betroffen. |
| Bauplan im Repo | Quellcode (`build.py`, Datenabruf, Nährwertrechnung) soll in einen eigenen Zweig, damit ein neuer Chat dort ansetzen kann. Noch offen. |
| Schreibzugriff auf das Repo | **Geklärt am 04.09.2026: nein.** Beide Wege (`contents`-API und `git/trees`-API) antworten mit `403 Resource not accessible by integration`. Die GitHub-Verbindung kann nur lesen. Dateien müssen von Marc über die Web-Oberfläche hochgeladen werden. |

---

## 9. Entscheidungsprotokoll

**04.08.2026 — Grundgerüst.** Sechs Metafelder im Namespace `elabel`,
Generator, Nährwertrechnung, erste Vorschau des Louré 2024.

**04.08.2026 — Durchgang 1.** Echte Fermate statt Nachbau · „Antioxidationsmittel"
bleibt (Pflicht), aber als eigene leisere Zeile · Rebsorten als neue Kategorie ·
Etikett 104 → 196 px · Linktext individualisiert · Kasten-Button statt
unterstrichenem Link. Nebenbei `--muted` und Spurenzeilen auf WCAG AA gezogen.

**04.08.2026 — Durchgang 2.** Linktext auf „Herkunft und Geschichte", weil
„Rebsorten" nach Durchgang 1 redundant war · Limitierung als eigene Kategorie ·
`display:revert`-Fallstrick gefunden.

**04.08.2026 — Kurskorrektur.** Marc fragte, warum dieser Teil Infrastruktur
braucht, die die übrige Website nicht braucht. Ergebnis: die Trennung von der
Website ist zwingend, Cloudflare und die tägliche Automatik waren es nicht.
Relative Pfade wurden dadurch nötig; Jost wanderte ins Repo.

**04.09.2026 — Veröffentlichung.** Etiketten korrigiert (1011 → 1211,
1123 → 1389), Repo angelegt, Dateien hochgeladen, GitHub Pages eingeschaltet,
Weiterleitungen bei United Domains gesetzt. Beide Seiten live und geprüft.
