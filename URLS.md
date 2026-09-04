# Adressen je Wein

**Generiert von `build.py` — nicht von Hand pflegen.** Stand: 04.09.2026

## Was trage ich bei United Domains ein?

Je Wein **eine Weiterleitung**: von der Subdomain in Spalte 2 auf das Ziel in
Spalte 3. Als Typ eine normale HTTP-Weiterleitung (301), **keine**
Frame-Weiterleitung — ein Frame bricht auf Mobilgeraeten und verdeckt die
echte Adresse.

| Wein | Von (steht im QR-Code auf dem Glas) | Nach (Weiterleitungsziel) |
|---|---|---|
| Louré 2024 | `https://loure2024-nutri.lasuite.vin/` | `https://marc33880.github.io/lasuite-elabel/loure2024-nutri/` |
| Le Ton blanc Variation 5 | `https://le-ton-blanc-var5-nutri.lasuite.vin/` | `https://marc33880.github.io/lasuite-elabel/le-ton-blanc-var5-nutri/` |

Drei Dinge, die dabei schiefgehen koennen:

1. **Der Pfad muss mit ins Ziel.** Ohne `/<slug>/` am Ende landet der Gast auf der
   Uebersichtsseite statt beim Wein.
2. **Der abschliessende Schraegstrich gehoert dazu.** `…/loure2024-nutri` ohne
   Schraegstrich ergibt bei manchen Hostern einen zusaetzlichen Sprung.
3. **Die bestehende Wildcard-Weiterleitung muss weg** oder zumindest hinter den
   einzelnen Eintraegen liegen. Sie schickt derzeit *alles* auf
   `chateaulasuite.com` — auch die beiden Wein-Subdomains.

## Bereits gedruckt und damit unveraenderlich

`loure2024-nutri`, `le-ton-blanc-var5-nutri`. Die Subdomain ist die einzige
Adresse auf dem Glas; ihre Laenge bestimmt die Dichte des QR-Codes, deshalb ist
sie kurz und ohne Pfad. Wer einen Wein ergaenzt, haelt sich an die
Slug-Konvention im README.

## Wenn der Ort der Seiten wechselt

Nur eine Zeile aendert sich — die Adressen im QR-Code bleiben, weil die
Weiterleitung davorsteht:

```bash
HOST_BASE=https://beispiel.de/elabel python3 build.py
```

Dann steht in dieser Tabelle das neue Ziel, und bei United Domains werden die
Eintraege einmal umgestellt.
