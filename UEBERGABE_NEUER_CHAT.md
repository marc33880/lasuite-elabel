# Übergabeprompt — neue E-Label-Seiten anlegen

Diesen Text vollständig in einen neuen Chat kopieren und
`E-LABEL_DOKUMENTATION.md` als Anhang mitgeben. Die Weine unten bei „Auftrag"
eintragen.

---

## DAS WICHTIGSTE ZUERST

**Auftrag:** Pflichtangaben-Seiten (Zutaten und Nährwerte, VO (EU) 2021/2117)
für weitere Weine bauen und veröffentlichen. Vorlage sind die zwei bestehenden
Seiten im Repo `marc33880/lasuite-elabel`.

**Du kannst nicht ins Repo schreiben** (403, geprüft) und **nicht ans
Shopify-CDN** (kein Netzweg). Du baust und prüfst, Marc lädt hoch und setzt die
Weiterleitung. Plane ein gebündeltes ZIP am Ende ein.

**Drei Stellen, an denen du anhalten und fragen musst:**

1. **Slug**, bevor irgendetwas gebaut wird — er wird auf Glas gedruckt.
2. **Flaschenzahl**, wenn sie von der Nummerierung auf dem Etikett abweicht —
   das war bisher bei *jedem* Wein so.
3. **Weiterleitung bei United Domains** — macht ausschließlich Marc.

**Der häufigste Fehler:** bauen, bevor Logo und Etikett in `assets/` liegen.
Dann fehlen im HTML die Bildverweise, und ein späteres Danebenlegen hilft
nicht mehr. So gingen die ersten beiden Seiten ohne Wortmarke und Etikett live.

**Erst prüfen, ob der Wein überhaupt eine Seite braucht:** maßgeblich ist die
Erzeugung, nicht die Abfüllung. Ab Jahrgang 2024 gilt die Pflicht ausnahmslos;
frühere Jahrgänge sind befreit, auch wenn sie später abgefüllt werden. Regel:
`custom.harvest_year >= 2024`. Siehe Abschnitt 2b der Dokumentation.

**Nährwerte:** die `elabel`-Felder für Restzucker und Säure waren am 04.09.2026
bei allen Weinen leer. Ohne echte Analysewerte gibt es keine gültige
Nährwertdeklaration — **niemals Platzhalter verwenden**, sondern bei Marc
anfordern. Bei den zwei bestehenden Seiten ist genau das passiert und muss
nachgeholt werden.

---

## Auftrag

Lege für die folgenden Weine E-Label-Seiten an (Zutaten und Nährwerte nach
VO (EU) 2021/2117) und veröffentliche sie:

```
[hier die Weine eintragen, z. B.:]
- Gigue 2024
- Caprice 2025
- Sarabande 2024
```

Die beiliegende `E-LABEL_DOKUMENTATION.md` ist die verbindliche Grundlage.
Lies sie zuerst vollständig. Sie beschreibt Aufbau, Datenfelder, Wortlaute,
Farbtabellen, Nährwertformeln und die Fallstricke. Weiche davon nicht ab, ohne
es zu begründen und nachzufragen.

## Was schon steht

* **Repository:** `github.com/marc33880/lasuite-elabel`, öffentlich, GitHub
  Pages aktiv (Branch `main`, Ordner `/ (root)`).
* **Live:** `loure2024-nutri` und `le-ton-blanc-var5-nutri`. Diese beiden
  **nicht anfassen** — ihre Adressen sind auf Glas gedruckt.
* **Adressschema:**
  `https://<slug>.lasuite.vin/` → `https://marc33880.github.io/lasuite-elabel/<slug>/`
  Die Weiterleitung liegt bei United Domains und wird von Marc gesetzt.
* Die bestehenden Seiten sind die Referenz für Gestaltung und Aufbau. Hol dir
  eine davon aus dem Repo und nimm sie als Vorlage, statt neu zu gestalten.

## Werkzeuge und was damit geht

| Werkzeug | Geht | Geht nicht |
|---|---|---|
| Shopify (MCP) | Produkte, Metafelder, Übersetzungen lesen und schreiben | Bilddateien hochladen (kein Netzweg für Bilddaten) |
| GitHub (MCP) | Repository-Inhalt **lesen** | **schreiben** (403) und Repositories anlegen (403) |
| Web (Fetch) | Live-Adressen prüfen | Bilder vom Shopify-CDN laden |
| Container-Shell | Python, Pillow, Seiten bauen, Screenshots via Playwright | **kein Netz** zum Shopify-CDN oder zu raw.githubusercontent |
| Rechner-Bridge | Dateien auf Marcs Rechner lesen und schreiben | ebenfalls kein Netz |

**Der Container ist flüchtig.** Er wurde in der Vorgeschichte schon einmal
mitten im Projekt zurückgesetzt und alle Arbeitsdateien waren weg. Lege deshalb
jedes Zwischenergebnis, das nicht verlorengehen darf, zeitnah an Marc aus —
ins Repo schreiben kannst du nicht. Der Quellcode liegt im Zweig `source` des
Repos und ist über die Leseverbindung erreichbar; hol ihn dir von dort, statt
Marc um einen Anhang zu bitten.

## Reihenfolge

| # | Schritt | Stop? |
|---|---|---|
| 1 | Daten aus Shopify holen, Nährwerte selbst rechnen | |
| 2 | Slug vorschlagen | **fragen** |
| 3 | Etikettenbild von Marc anfordern | **warten** |
| 4 | Flaschenzahl gegen das Etikett prüfen | **fragen, wenn abweichend** |
| 5 | Seite bauen (erst mit Bildern in `assets/`) und prüfen | |
| 6 | ZIP ausliefern, Marc lädt hoch, Struktur nachprüfen | |
| 7 | Weiterleitung: exakte Zeile geben | **Marc macht es** |
| 8 | Live-Adresse abrufen und gegenlesen | |
| 9 | Dokumentation fortschreiben und ausliefern | |

**Schritt 0 entfällt.** Der Schreibzugriff wurde am 04.09.2026 geprüft und ist
**nicht vorhanden** — sowohl die `contents`-API als auch `git/trees` antworten
mit `403 Resource not accessible by integration`. Versuch es nicht erneut.
Du lieferst die fertigen Dateien als ZIP an Marc, er lädt sie über die
GitHub-Web-Oberfläche hoch. Plane das von Anfang an so ein: **ein** gebündeltes
Paket am Ende statt vieler Einzelabgaben.

**Schritt 1 — Daten holen.** Für jeden Wein über Shopify: `elabel.slug`,
`elabel.zutaten` (inkl. en/fr-Übersetzungen), `elabel.alcohol_vol`,
`elabel.sugars_g_l`, `elabel.acid_g_l`, `elabel.energy_kcal_100ml`,
`custom.rebsorten`, `custom.flaschenanzahl`, `custom.harvest_year`, Titel und
Handle. Fehlt ein Pflichtfeld, frag nach, statt zu raten. **Rechne die
Nährwerte selbst** nach den Formeln der Dokumentation und prüfe sie gegen die
beiden dort dokumentierten Kontrollwerte.

**Schritt 2 — Slug.** Nach der Konvention vorschlagen und von Marc bestätigen
lassen, **bevor** irgendetwas gebaut wird. Er wird gedruckt und ist danach
unveränderlich.

**Schritt 3 — Etikettenbild anfordern.** Du kommst nicht ans Shopify-CDN. Bitte
Marc, das Etikett aus den Shopify-Dateien hier anzuhängen. Nenne den Zielnamen
`<slug>.jpg`.

**Schritt 4 — Zahlen gegen das Etikett prüfen.** Vergrößere den Bereich links
unten auf dem Etikett vierfach und lies die Nummerierung. Der Nenner muss
`custom.flaschenanzahl` entsprechen. Bei beiden bisherigen Weinen wich er ab.
Halt an und frag, wenn er abweicht — die Zahl steht sonst auf der Seite anders
als auf der Flasche in der Hand des Gastes.

**Schritt 5 — Seite bauen.** Aufbau, Wortlaute und Farben exakt nach
Dokumentation. **Baue erst, wenn Logo und Etikett in `assets/` liegen** — der
Generator lässt fehlende Bilder weg, und ein späteres Danebenlegen hilft nicht
mehr, weil das HTML sie dann nicht erwähnt. Genau so gingen die ersten beiden
Seiten ohne Wortmarke und Etikett live. Prüfe vor dem Ausliefern:
* die Datei enthält `<div class="brand"><img` und `<figure><img`
* keine fremde Ressource in der fertigen Datei (`src="http`, `url(http`,
  `@import`, `<link href="http`) — Textlinks sind erlaubt
* alle Asset-Pfade **relativ** (`../assets/…`), niemals mit führendem
  Schrägstrich
* alle drei Sprachen vorhanden, Rebsortennamen unübersetzt
* Limitierungs-Block ohne Flexbox (siehe Fallstrick in der Dokumentation)
* Nährwerte gegengerechnet

**Schritt 6 — Ausliefern.** Ein ZIP mit `<slug>/index.html`,
`assets/<slug>.jpg` und der aktualisierten `index.html` (Fallback-Übersicht,
neuer Wein ergänzt). Sag Marc dazu: entpacken, im Repo *Add file → Upload
files*, den **Inhalt** des Ordners hineinziehen — nicht den Ordner selbst,
sonst entsteht eine Ebene zu viel. Prüfe danach über die GitHub-Leseverbindung,
ob die Struktur stimmt, **bevor** er die Weiterleitung setzt.

**Schritt 7 — Weiterleitung.** Gib Marc die exakte Zeile für United Domains:
Subdomain `<slug>`, Ziel `https://marc33880.github.io/lasuite-elabel/<slug>/`,
Typ HTTP-Weiterleitung, **keine** Frame-Weiterleitung, Schrägstrich am Ende.
Das macht er selbst — sein Registrar-Konto, und eine falsche Weiterleitung
träfe eine gedruckte Adresse.

**Schritt 8 — Nachprüfen.** Ruf `https://<slug>.lasuite.vin/` ab und lies den
Inhalt gegen. Bitte Marc, Etikett und Schrift im Browser anzusehen und an einer
echten Flasche zu scannen.

**Schritt 9 — Dokumentation fortschreiben.** Ergänze in
`E-LABEL_DOKUMENTATION.md` den Live-Stand, neue Erfahrungen und offene Punkte,
und liefere die aktualisierte Fassung aus.

## Arbeitsweise mit Marc

Er will vor eigenmächtigen Schritten gefragt werden, wenn etwas öffentlich wird
oder sein Registrar-Konto betrifft — beim Rest ist ihm Tempo lieber als
Rückfragen. Er merkt schnell, wenn Aufwand nicht zum Nutzen passt, und fragt
dann zu Recht nach; erkläre den Grund, statt die Komplexität zu verteidigen.
Er schätzt es, wenn ungefragt geprüft wird, was auffällt — die Abweichung
zwischen Etikett und Flaschenzahl kam so ans Licht. Antworte auf Deutsch.

## Was nicht zur Debatte steht

* Kein Tracking, keine Cookies, kein Analytics, keine Schrift von einem fremden
  Server, kein Warenkorb, keine Preise. Der Leitfaden C/2023/1190 verbietet es
  ausnahmslos.
* Der Klassenname vor „Sulfite" bleibt stehen — er ist Pflicht.
* Die Slugs der beiden bestehenden Weine sind unveränderlich.
* Pflichtangaben und freiwillige Angaben bleiben durch eigene Überschriften
  getrennt; Freiwilliges steht davor, niemals in der Nährwerttabelle.
