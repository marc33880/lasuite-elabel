#!/usr/bin/env python3
"""
Generator für die E-Label-Seiten (Zutaten und Nährwerte) von Château LaSuite.

Erzeugt pro Wein EINE statische HTML-Datei mit allen drei Sprachen inline.
Kein JavaScript-Framework, kein Cookie, kein externer Request zur Laufzeit.

  python3 build.py            # baut aus wines.json nach dist/
"""
import json
import os
import shutil
import sys
from datetime import date

import nutrition

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
LANGS = ("de", "en", "fr")

# --------------------------------------------------------------------------
# Wortlaute. Bewusst knapp: nur was die Verordnung verlangt.
# --------------------------------------------------------------------------
T = {
    "de": {
        "eyebrow": "Zutaten und Nährwerte",
        "ingredients": "Zutaten",
        "nutrition": "Nährwerte",
        "grape": "Rebsorte",
        "grapes": "Rebsorten",
        "limit": "Limitierung",
        "bottles": "Flaschen",
        "per": "je 100 ml",
        "energy": "Brennwert",
        "fat": "Fett",
        "saturates": "davon gesättigte Fettsäuren",
        "carbs": "Kohlenhydrate",
        "sugars": "davon Zucker",
        "protein": "Eiweiß",
        "salt": "Salz",
        "trace": "&lt; 0,5",
        "salt_trace": "&lt; 0,01",
        "zero": "0",
        "more": "Mehr über Herkunft und Geschichte des %s",
        "vol": "% vol",
        "litre": "0,75 l",
        "as_of": "Stand",
        "legal": "Pflichtangaben gemäß Verordnung (EU) 2021/2117.",
    },
    "en": {
        "eyebrow": "Ingredients and nutrition",
        "ingredients": "Ingredients",
        "nutrition": "Nutrition",
        "grape": "Grape variety",
        "grapes": "Grape varieties",
        "limit": "Limited edition",
        "bottles": "bottles",
        "per": "per 100 ml",
        "energy": "Energy",
        "fat": "Fat",
        "saturates": "of which saturates",
        "carbs": "Carbohydrate",
        "sugars": "of which sugars",
        "protein": "Protein",
        "salt": "Salt",
        "trace": "&lt; 0.5",
        "salt_trace": "&lt; 0.01",
        "zero": "0",
        "more": "More on the origin and story of %s",
        "vol": "% vol",
        "litre": "0.75 l",
        "as_of": "Last updated",
        "legal": "Mandatory particulars pursuant to Regulation (EU) 2021/2117.",
    },
    "fr": {
        "eyebrow": "Ingrédients et valeurs nutritionnelles",
        "ingredients": "Ingrédients",
        "nutrition": "Valeurs nutritionnelles",
        "grape": "Cépage",
        "grapes": "Cépages",
        "limit": "Édition limitée",
        "bottles": "bouteilles",
        "per": "pour 100 ml",
        "energy": "Énergie",
        "fat": "Matières grasses",
        "saturates": "dont acides gras saturés",
        "carbs": "Glucides",
        "sugars": "dont sucres",
        "protein": "Protéines",
        "salt": "Sel",
        "trace": "&lt; 0,5",
        "salt_trace": "&lt; 0,01",
        "zero": "0",
        "more": "En savoir plus sur l'origine et l'histoire du %s",
        "vol": "% vol",
        "litre": "0,75 l",
        "as_of": "Mise à jour",
        "legal": "Mentions obligatoires conformément au règlement (UE) 2021/2117.",
    },
}

# --------------------------------------------------------------------------
# Die ECHTE Fermate (Pinselstrich, vektorisiert). Wortgleich uebernommen aus
# dem Theme: snippets/lasuite-fermate-svg.liquid — Quelle dort
# Domaine_Assets/web_assets/brand-fermate.png. Kein Nachbau: waere das Zeichen
# hier nachgezeichnet, drifteten Etikett und Website auseinander.
# Aendert sich die Marke, wird dieser Pfad aus dem Snippet neu kopiert.
# --------------------------------------------------------------------------
FERMATE = (
    '<svg class="fermate" viewBox="0 0 255 166" fill="currentColor" '
    'fill-rule="evenodd" aria-hidden="true"><path d="'
    'M135,129 L127,130 L124,132 L119,130 L113,134 L109,140 L109,150 L108,152 '
    'L119,165 L125,165 L126,161 L135,162 L134,160 L135,155 L138,155 L140,157 '
    'L141,161 L143,162 L143,159 L146,156 L144,150 L150,148 L142,140 L142,138 '
    'L139,135 L139,132 L137,132Z '
    'M0,116 L0,141 L2,142 L4,149 L5,139 L3,138 L3,134 L7,126 L6,125 L6,119 '
    'L8,113 L8,107 L11,102 L13,93 L17,89 L19,82 L23,78 L25,73 L44,53 L49,51 '
    'L50,48 L54,44 L60,41 L64,37 L70,35 L73,32 L78,31 L90,24 L94,24 L104,21 '
    'L123,19 L125,17 L127,17 L128,19 L135,18 L142,21 L153,22 L159,25 L165,25 '
    'L172,29 L175,29 L184,35 L191,38 L212,52 L231,75 L230,78 L231,82 L233,85 '
    'L235,94 L240,103 L243,114 L245,142 L246,143 L245,151 L247,146 L247,141 '
    'L250,140 L251,143 L254,142 L254,140 L250,140 L248,138 L249,134 L254,135 '
    'L254,125 L253,128 L250,127 L250,119 L254,118 L254,117 L250,116 L251,113 '
    'L254,113 L254,111 L252,110 L252,104 L247,103 L242,87 L242,82 L236,69 '
    'L233,66 L229,57 L225,53 L224,50 L215,40 L212,38 L208,38 L201,33 L197,32 '
    'L196,28 L188,23 L189,20 L191,20 L192,22 L196,22 L198,26 L202,27 L210,33 '
    'L202,25 L198,24 L197,21 L192,17 L188,17 L185,13 L175,9 L170,10 L166,7 '
    'L162,7 L154,3 L150,3 L148,0 L111,0 L110,2 L99,3 L93,6 L79,10 L74,15 '
    'L70,16 L66,19 L62,19 L52,26 L45,33 L45,35 L42,38 L40,38 L30,49 L26,56 '
    'L26,58 L22,62 L21,66 L19,67 L17,73 L14,75 L9,86 L8,93 L5,97 L5,106 '
    'L2,115Z '
    'M176,14 L177,13 L181,14 L183,16 L183,18 L180,19 L176,16Z"/></svg>')

# --------------------------------------------------------------------------
# Rebsortenfarben. Spiegel von snippets/lasuite-rebsorte-farbe.liquid, damit
# die Schichtung hier genauso faerbt wie auf der PDP. SSoT der Werte:
# 00_Guidelines/Website/Rebsorten_Farbtabelle.md (Workspace).
# Die Reihenfolge der Pruefungen ist bedeutsam — "cabernet franc" muss vor
# "cabernet" stehen, sonst gewinnt der falsche Treffer.
# --------------------------------------------------------------------------
GRAPE_COLORS = [
    (("cabernet", "franc", "sauvignon"), "#5C5C74"),
    (("cabernet franc",), "#77697E"),
    (("cabernet",), "#45536A"),
    (("merlot",), "#8A3B40"),
    (("malbec",), "#6E4356"), (("côt",), "#6E4356"), (("cot",), "#6E4356"),
    (("castet",), "#3B4652"),
    (("alvarinho",), "#C6CBAE"), (("albariño",), "#C6CBAE"),
    (("albarino",), "#C6CBAE"),
    (("sémillon",), "#DFCF9B"), (("semillon",), "#DFCF9B"),
    (("sauvignon",), "#A2AC85"),
]
GRAPE_FALLBACK = "#8B857F"      # --ls-mole: ein Tippfehler wird grau sichtbar


def grape_color(name):
    g = name.lower().replace("-", " ").replace("&", " und ")
    for needles, hexval in GRAPE_COLORS:
        if all(n in g for n in needles):
            return hexval
    return GRAPE_FALLBACK


def on_color(hexval):
    """Beschriftung: helle Sorten tragen Tinte, dunkle Weiss (wie auf der PDP)."""
    r, g, b = (int(hexval[i:i + 2], 16) for i in (1, 3, 5))
    return "#2A2722" if (r * 299 + g * 587 + b * 114) / 1000.0 > 145 else "#fff"


def split_grapes(raw):
    """'100% Sauvignon blanc, 40 % Merlot' -> [('100%','Sauvignon blanc'), ...]"""
    out = []
    for part in (raw or "").replace("\n", " ").split(","):
        p = " ".join(part.split())
        if not p:
            continue
        head = p.split(" ")[0]
        if any(c.isdigit() for c in head):
            pc = head
            nm = p[len(head):].strip().lstrip("%").strip()
        else:
            pc, nm = "", p
        out.append((pc, nm))
    return out


# Tausendertrennung: Punkt (de), Komma (en), geschuetztes Leerzeichen (fr).
THOUSANDS = {"de": ".", "en": ",", "fr": "&nbsp;"}


def fmt_int(n, lang):
    return "{:,}".format(int(n)).replace(",", THOUSANDS[lang])


def grape_layers(raw):
    """Gestaffelte Baender wie in der Assemblage-Sektion der PDP."""
    layers = split_grapes(raw)
    if not layers:
        return ""
    html = []
    for i, (pc, nm) in enumerate(layers):
        if i == 0:
            h = "clamp(86px,18vw,112px)"
        else:
            h = "%dpx" % max(44, 64 - (i - 1) * 6)
        col = grape_color(nm)
        html.append(
            '<div class="glayer" style="height:%s;background:%s;color:%s">'
            '<span class="pc">%s</span><span class="nm">%s</span></div>'
            % (h, col, on_color(col), pc, nm))
    return '<div class="strat">%s</div>' % "".join(html)

# LOCAL_ASSETS=1 -> Schrift, Logo und Flaschenbilder werden aus assets/ geladen
# (fetch_assets.py holt sie einmalig). Das ist der Modus fuer das Deployment:
# die Seite hat dann keinen einzigen externen Request mehr und funktioniert auch,
# wenn Shopify oder Google Fonts in 20 Jahren nicht mehr existieren.
LOCAL_ASSETS = os.environ.get("LOCAL_ASSETS") == "1"

FONT_HEAD = "" if LOCAL_ASSETS else (
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
    '?family=Jost:wght@200;300;400;500&display=swap">')

FONT_CSS = """
@font-face{font-family:'Jost';src:url('{A}jost-200.woff2') format('woff2');
  font-weight:200;font-style:normal;font-display:swap}
@font-face{font-family:'Jost';src:url('{A}jost-300.woff2') format('woff2');
  font-weight:300;font-style:normal;font-display:swap}
@font-face{font-family:'Jost';src:url('{A}jost-400.woff2') format('woff2');
  font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:'Jost';src:url('{A}jost-500.woff2') format('woff2');
  font-weight:500;font-style:normal;font-display:swap}
""" if LOCAL_ASSETS else ""

CSS = FONT_CSS + """
:root{
  --shell:#F1EFEA; --paper:#E7E5DE; --ink:#2A2722; --ink-soft:#5D574F;
  --gold:#AC967C; --gold-deep:#8C785F; --muted:#6A655C; --line:rgba(42,39,34,.13);
  /* --muted war #8E897F = 3,0:1 auf Shell und damit unter WCAG AA. Auf einer
     Seite, deren Inhalt Pflichtangabe ist, ist Lesbarkeit nicht optional.
     #6A655C ist der hellste Wert, der auf Shell (5,1:1) UND Paper (4,6:1) AA
     schafft und warm bleibt. */
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'Jost',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-weight:300; font-size:16px; line-height:1.7;
  -webkit-font-smoothing:antialiased;
}
.wrap{
  max-width:30rem; margin:14px auto; padding:40px 26px 46px;
  background:var(--shell); border:1px solid rgba(42,39,34,.07); border-radius:2px;
  box-shadow:0 1px 2px rgba(42,39,34,.03), 0 12px 34px rgba(42,39,34,.045);
}
@media (min-width:34rem){.wrap{margin:34px auto; padding:52px 44px 54px}}
[data-lang]{display:none}
html[lang="de"] [data-lang="de"],
html[lang="en"] [data-lang="en"],
html[lang="fr"] [data-lang="fr"]{display:revert}

/* Kopf */
.brand{text-align:center; margin-bottom:34px}
.brand img{width:190px; max-width:62%; height:auto; display:inline-block}
.eyebrow{
  font-size:10px; letter-spacing:.28em; text-transform:uppercase;
  color:var(--gold-deep); font-weight:500; text-align:center; margin:0 0 22px;
}
h1{
  font-size:clamp(2.1rem,10vw,2.9rem); font-weight:200; letter-spacing:.015em;
  line-height:1.08; margin:0; text-align:center;
}
.vintage{
  font-size:14px; letter-spacing:.34em; color:var(--gold-deep);
  text-align:center; margin:14px 0 0; font-weight:400;
}
.meta{
  font-size:13px; letter-spacing:.06em; color:var(--muted);
  text-align:center; margin:18px 0 0;
}
.rule{text-align:center; margin:32px 0 4px; color:var(--gold)}
.fermate{width:60px; height:auto; display:inline-block; vertical-align:middle}

/* Blöcke */
section{margin-top:36px}
h2{
  font-size:10px; letter-spacing:.26em; text-transform:uppercase;
  font-weight:500; color:var(--gold-deep); margin:0 0 16px;
  padding-bottom:10px; border-bottom:1px solid var(--line);
}
.ingredients{font-size:15.5px; line-height:1.8; color:var(--ink-soft); margin:0}
.ingredients p{margin:0 0 .6em}
.ingredients p:last-child{margin:0}
.ingredients strong{font-weight:500; color:var(--ink)}
/* Zweiter und jeder weitere Absatz = Zusatzstoff-/Hinweiszeile. Sie steht
   bewusst eigenstaendig und leiser, damit der Klassenname nicht wie eine
   weitere Zutat gelesen wird. Das Allergen bleibt hervorgehoben (fett). */
.ingredients p+p{
  margin-top:15px; font-size:13px; letter-spacing:.05em; color:var(--ink-soft);
}
.ingredients p+p strong{font-size:14.5px; letter-spacing:0}

/* Rebsorten: gestaffelte Baender wie in der Assemblage-Sektion der PDP */
.strat{border:1px solid rgba(42,39,34,.14)}
.glayer{
  display:flex; align-items:center; gap:14px;
  padding:0 clamp(14px,4vw,22px); color:#fff;
}
.glayer .pc{
  font-weight:200; font-size:clamp(1.5rem,7vw,2.4rem); line-height:1;
  min-width:2.4em; font-variant-numeric:tabular-nums;
}
.glayer .nm{font-size:11.5px; letter-spacing:.14em; text-transform:uppercase; opacity:.94}

/* Limitierung: dieselbe Typografie wie die Baender — grosse leichte Ziffer,
   kleine Versalien daneben — nur ohne Flaeche, damit die Reihe ruhig bleibt. */
/* Kein Flex: die Ziffer sitzt in einem [data-lang]-Span, dessen display von
   der Sprachumschaltung gesetzt wird und jede Flex-Regel hier ueberschreibt.
   Inline-Elemente stehen ohnehin auf gemeinsamer Grundlinie. */
.limit{margin:0}
.limit .n{
  font-weight:200; font-size:clamp(1.9rem,8vw,2.5rem); line-height:1;
  color:var(--ink); font-variant-numeric:tabular-nums; font-feature-settings:"tnum";
}
.limit .u{
  margin-left:.6em; font-size:11.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-soft);
}

/* Nährwerttabelle */
table{width:100%; border-collapse:collapse; font-size:15px}
caption{
  caption-side:top; text-align:right; font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); padding-bottom:8px;
}
th,td{padding:11px 0; border-bottom:1px solid var(--line); vertical-align:baseline}
tr:last-child th,tr:last-child td{border-bottom:0}
th{text-align:left; font-weight:300; color:var(--ink-soft); padding-right:14px}
td{
  text-align:right; white-space:nowrap; font-weight:400;
  font-variant-numeric:tabular-nums; font-feature-settings:"tnum";
}
tr.sub th{padding-left:16px; font-size:14px; color:var(--muted)}
tr.energy th{color:var(--ink); font-weight:400}
tr.energy td{font-size:16.5px}
tr.trace th,tr.trace td{color:var(--muted)}

/* Etikett */
figure{margin:40px 0 0; text-align:center}
figure img{width:min(60%,196px); height:auto; display:inline-block; opacity:.96}

/* Weg zur Story: Kasten-Button, weil dahinter echter Mehrwert liegt */
.cta{margin:40px 0 0}
.cta a{
  display:block; padding:16px 22px; border:1px solid var(--gold); background:transparent;
  font-size:11px; letter-spacing:.17em; text-transform:uppercase;
  font-weight:500; line-height:1.55; text-align:center;
  color:var(--ink); text-decoration:none;
  transition:background .3s, color .3s, border-color .3s;
}
.cta a:hover,.cta a:focus-visible{
  background:var(--ink); border-color:var(--ink); color:var(--shell);
}
.cta .arrow{
  display:inline-block; margin-left:.6em; color:var(--gold-deep);
  transition:transform .4s, color .3s;
}
.cta a:hover .arrow,.cta a:focus-visible .arrow{
  color:var(--gold); transform:translateX(4px);
}

/* Fuß */
footer{
  margin-top:46px; padding-top:22px; border-top:1px solid var(--line);
  font-size:11.5px; line-height:1.75; color:var(--muted); text-align:center;
}
footer p{margin:0 0 5px}
.langs{margin-top:18px; font-size:11px; letter-spacing:.2em; text-transform:uppercase}
.langs button{
  background:none; border:0; padding:4px 6px; cursor:pointer; color:var(--muted);
  font:inherit; letter-spacing:inherit; text-transform:inherit;
}
.langs button[aria-current="true"]{color:var(--gold-deep); font-weight:500}
.langs span{color:var(--line)}
@media (prefers-contrast:more){:root{--muted:#5D574F}}
"""

JS = """
(function(){
  var ok=['de','en','fr'];
  function set(l){
    document.documentElement.lang=l;
    var b=document.querySelectorAll('.langs button');
    for(var i=0;i<b.length;i++){b[i].setAttribute('aria-current', b[i].dataset.l===l ? 'true':'false');}
  }
  var n=(navigator.language||'de').slice(0,2).toLowerCase();
  set(ok.indexOf(n)>=0 ? n : 'en');
  document.addEventListener('click',function(e){
    var t=e.target.closest && e.target.closest('.langs button');
    if(t){set(t.dataset.l);}
  });
})();
"""


def spans(values):
    """{'de':'…','en':'…','fr':'…'} -> drei sprachgeschaltete Spans."""
    return "".join('<span data-lang="%s">%s</span>' % (l, values[l]) for l in LANGS)


def per_lang(fn):
    return spans({l: fn(l) for l in LANGS})


def render(w, today, apath=""):
    n = nutrition.compute(w["alcohol_vol"], w.get("sugars_g_l"),
                          w.get("acid_g_l"), w.get("energy_kcal_override"))
    fg = nutrition.fmt_g

    def row(cls, label_key, cell_fn):
        label = spans({l: T[l][label_key] for l in LANGS})
        return ('<tr%s><th>%s</th><td>%s</td></tr>'
                % (' class="%s"' % cls if cls else "", label, per_lang(cell_fn)))

    rows = "".join([
        row("energy", "energy",
            lambda l: "%d kJ / %d kcal" % (n["kj"], n["kcal"])),
        row("trace", "fat", lambda l: T[l]["zero"] + "&nbsp;g"),
        row("trace sub", "saturates", lambda l: T[l]["zero"] + "&nbsp;g"),
        row("", "carbs", lambda l: fg(n["carbs"], l) + "&nbsp;g"),
        row("sub", "sugars", lambda l: fg(n["sugars"], l) + "&nbsp;g"),
        row("trace", "protein", lambda l: T[l]["trace"] + "&nbsp;g"),
        row("trace", "salt", lambda l: T[l]["salt_trace"] + "&nbsp;g"),
    ])

    ing = spans({l: w["ingredients"].get(l, w["ingredients"]["de"]) for l in LANGS})

    # Rebsorten. Eigennamen und werden NICHT uebersetzt (Sperrliste im
    # TRANSLATION_BRIEF) — nur die Ueberschrift wechselt die Sprache.
    grapes_raw = w.get("grapes") or ""
    n_grapes = len(split_grapes(grapes_raw))
    if n_grapes:
        h_grapes = spans({l: T[l]["grapes" if n_grapes > 1 else "grape"]
                          for l in LANGS})
        grapes = ('\n  <section>\n    <h2>%s</h2>\n    %s\n  </section>\n'
                  % (h_grapes, grape_layers(grapes_raw)))
    else:
        grapes = ""

    # Limitierung. Quelle ist custom.flaschenanzahl — dasselbe Feld, das die
    # PDP in der Faktenreihe zeigt. Fehlt es, entfaellt der Block ersatzlos.
    bottles = w.get("bottles")
    if bottles:
        limit = ('\n  <section>\n    <h2>%s</h2>\n    <p class="limit">%s</p>'
                 '\n  </section>\n'
                 % (spans({l: T[l]["limit"] for l in LANGS}),
                    spans({l: '<span class="n">%s</span>'
                              '<span class="u">%s</span>'
                              % (fmt_int(bottles, l), T[l]["bottles"])
                           for l in LANGS})))
    else:
        limit = ""

    label = "%s %s" % (w["name"], w["vintage"])
    story = spans({l: '<a href="%s"><span>%s</span>'
                      '<span class="arrow" aria-hidden="true">&rarr;</span></a>'
                      % (w["story_url"][l], T[l]["more"] % label)
                   for l in LANGS})

    alc = ("%.1f" % float(w["alcohol_vol"]))
    meta = per_lang(lambda l: "%s &middot; %s&nbsp;%s"
                    % (T[l]["litre"],
                       alc.replace(".", ",") if l != "en" else alc,
                       T[l]["vol"]))

    return """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<meta name="referrer" content="no-referrer">
<title>%(title)s &middot; %(eyebrow_de)s</title>
%(font_head)s
<style>%(css)s</style>
</head>
<body>
<div class="wrap">

  <div class="brand">%(logo_img)s</div>

  <p class="eyebrow">%(eyebrow)s</p>
  <h1>%(name)s</h1>
  <p class="vintage">%(vintage)s</p>
  <p class="meta">%(meta)s</p>
  <div class="rule">%(fermate)s</div>
%(grapes)s%(limit)s
  <section>
    <h2>%(h_ing)s</h2>
    <div class="ingredients">%(ing)s</div>
  </section>

  <section>
    <h2>%(h_nut)s</h2>
    <table>
      <caption>%(per)s</caption>
      <tbody>%(rows)s</tbody>
    </table>
  </section>

%(bottle_fig)s

  <p class="cta">%(story)s</p>

  <footer>
    <p>%(producer)s</p>
    <p>%(legal)s</p>
    <p>%(as_of)s %(today)s</p>
    <p class="langs">
      <button type="button" data-l="de">DE</button><span>&middot;</span
      ><button type="button" data-l="en">EN</button><span>&middot;</span
      ><button type="button" data-l="fr">FR</button>
    </p>
  </footer>

</div>
<script>%(js)s</script>
</body>
</html>
""" % {
        "title": "%s %s" % (w["name"], w["vintage"]),
        "eyebrow_de": T["de"]["eyebrow"],
        "font_head": FONT_HEAD,
        "css": CSS.replace("{A}", apath),
        "js": JS,
        # Fehlt ein Bild, entfaellt das Element ganz. Ein Icon fuer ein
        # kaputtes Bild untergraebt auf einer Pflichtangaben-Seite mehr
        # Vertrauen als eine fehlende Abbildung.
        "logo_img": ('<img src="%s" alt="Ch&acirc;teau LaSuite aux Conseillans">'
                     % w["logo"]) if w["logo"] else "",
        "bottle_fig": ('  <figure><img src="%s" alt="%s %s"></figure>\n'
                       % (w["bottle"], w["name"], w["vintage"]))
                      if w["bottle"] else "",
        "name": w["name"],
        "vintage": w["vintage"],
        "eyebrow": spans({l: T[l]["eyebrow"] for l in LANGS}),
        "meta": meta,
        "fermate": FERMATE,
        "grapes": grapes,
        "limit": limit,
        "h_ing": spans({l: T[l]["ingredients"] for l in LANGS}),
        "h_nut": spans({l: T[l]["nutrition"] for l in LANGS}),
        "per": spans({l: T[l]["per"] for l in LANGS}),
        "rows": rows,
        "ing": ing,
        "story": story,
        "producer": w["producer"],
        "legal": spans({l: T[l]["legal"] for l in LANGS}),
        "as_of": spans({l: T[l]["as_of"] for l in LANGS}),
        "today": today,
    }


def render_index(wines, apath=""):
    """Fallback-Übersicht: fängt Tippfehler und alte Adressen ab, nie ein 404."""
    items = "\n".join(
        '      <li><a href="/%s/">%s %s</a></li>' % (w["slug"], w["name"], w["vintage"])
        for w in wines)
    return """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Ch&acirc;teau LaSuite &middot; Zutaten und N&auml;hrwerte</title>
%s
<style>%s
  ul{list-style:none;padding:0;margin:0}
  li{border-bottom:1px solid var(--line)}
  li a{display:block;padding:15px 0;color:var(--ink);text-decoration:none;font-size:16px}
  li a:hover{color:var(--gold-deep)}
</style>
</head>
<body>
<div class="wrap">
  <div class="brand"><img src="%s" alt="Ch&acirc;teau LaSuite aux Conseillans"></div>
  <p class="eyebrow">Zutaten und N&auml;hrwerte</p>
  <div class="rule">%s</div>
  <section>
    <ul>
%s
    </ul>
  </section>
  <footer><p>Pflichtangaben gem&auml;&szlig; Verordnung (EU) 2021/2117.</p></footer>
</div>
</body>
</html>
""" % (FONT_HEAD, CSS.replace("{A}", apath),
       (apath + "logo.png") if apath else wines[0]["logo"], FERMATE, items)


# Ort, an dem die fertigen Seiten liegen. Alles darunter ist Pfad + Slug,
# deshalb laesst sich der Ort wechseln, ohne dass eine Seite angepasst werden
# muss. Setzbar per Umgebungsvariable, damit URLS.md immer stimmt.
HOST_BASE = os.environ.get(
    "HOST_BASE", "https://marc33880.github.io/lasuite-elabel").rstrip("/")


def write_urls(wines):
    """Schreibt URLS.md — die eine Datei, die auf die Frage antwortet:
    welche Adresse gehoert wohin? Generiert, damit sie nie veraltet."""
    rows = "\n".join(
        "| %s %s | `https://%s.lasuite.vin/` | `%s/%s/` |"
        % (w["name"], w["vintage"], w["slug"], HOST_BASE, w["slug"])
        for w in wines)
    text = """# Adressen je Wein

**Generiert von `build.py` — nicht von Hand pflegen.** Stand: %s

## Was trage ich bei United Domains ein?

Je Wein **eine Weiterleitung**: von der Subdomain in Spalte 2 auf das Ziel in
Spalte 3. Als Typ eine normale HTTP-Weiterleitung (301), **keine**
Frame-Weiterleitung — ein Frame bricht auf Mobilgeraeten und verdeckt die
echte Adresse.

| Wein | Von (steht im QR-Code auf dem Glas) | Nach (Weiterleitungsziel) |
|---|---|---|
%s

Drei Dinge, die dabei schiefgehen koennen:

1. **Der Pfad muss mit ins Ziel.** Ohne `/%s/` am Ende landet der Gast auf der
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
""" % (date.today().strftime("%d.%m.%Y"), rows, "<slug>")
    with open(os.path.join(ROOT, "URLS.md"), "w", encoding="utf-8") as f:
        f.write(text)


def assert_selfcontained(html, where):
    """Die Verordnung verlangt eine Seite ohne Tracking, die Haltbarkeitsidee
    eine ohne Fremd-Request. Beides ist leicht versehentlich kaputtzumachen —
    ein zusaetzliches <link> auf Google Fonts genuegt. Deshalb bricht der
    Produktionsbau ab, statt es stillschweigend auszuliefern. Links im Text
    (<a href>) sind erlaubt: sie laden nichts, bis jemand klickt."""
    bad = []
    for needle in ('src="http', "src='http", "url(http", "srcset=\"http",
                   "@import"):
        if needle in html:
            bad.append(needle)
    for tag in ("<link", "<script src"):
        i = 0
        while True:
            i = html.find(tag, i)
            if i < 0:
                break
            end = html.find(">", i)
            if "http" in html[i:end]:
                bad.append(html[i:end][:60])
            i = end
    if bad:
        sys.exit("%s laedt fremde Ressourcen: %s" % (where, "; ".join(bad)))


def main():
    with open(os.path.join(ROOT, "wines.json"), encoding="utf-8") as f:
        wines = json.load(f)

    # Relative Pfade, kein fuehrender Schraegstrich: so laeuft dieselbe
    # Datei unter einer Subdomain (loure2024-nutri.lasuite.vin/), in einem
    # Unterordner (…github.io/lasuite-elabel/loure2024-nutri/) und lokal
    # geoeffnet. Ein absoluter Pfad wuerde im Unterordner ins Leere zeigen.
    if LOCAL_ASSETS:
        adir = os.path.join(ROOT, "assets")
        for w in wines:
            w["logo"] = ("../assets/logo.png"
                         if os.path.isfile(os.path.join(adir, "logo.png")) else "")
            bn = "%s.jpg" % w["slug"]
            w["bottle"] = ("../assets/" + bn
                           if os.path.isfile(os.path.join(adir, bn)) else "")
    today = {"de": date.today().strftime("%d.%m.%Y"),
             "en": date.today().strftime("%Y-%m-%d"),
             "fr": date.today().strftime("%d/%m/%Y")}
    today_html = spans(today)

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    if LOCAL_ASSETS:
        src = os.path.join(ROOT, "assets")
        if not os.path.isdir(src):
            sys.exit("assets/ fehlt - erst 'python3 fetch_assets.py' laufen lassen.")
        shutil.copytree(src, os.path.join(DIST, "assets"))
        print("  assets/                    -> dist/assets/")
        # Die Schrift liegt im Repo. Die Bilder nicht - sie kommen aus dem
        # Shopify-CDN und muessen einmal geholt oder abgelegt werden. Fehlen
        # sie, bleibt die Seite gueltig, zeigt aber ein leeres Bild: deshalb
        # eine deutliche Warnung statt eines stillen Durchlaufs.
        missing = [n for n in ["logo.png"] + ["%s.jpg" % w["slug"] for w in wines]
                   if not os.path.isfile(os.path.join(src, n))]
        if missing:
            print("  ! Bilder fehlen in assets/: %s" % ", ".join(missing))
            print("    -> python3 fetch_assets.py  oder von Hand ablegen")

    for w in wines:
        out = os.path.join(DIST, w["slug"])
        os.makedirs(out, exist_ok=True)
        page = render(w, today_html, "../assets/" if LOCAL_ASSETS else "")
        if LOCAL_ASSETS:
            assert_selfcontained(page, w["slug"])
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print("  %-26s -> %s.lasuite.vin" % (w["slug"] + "/index.html", w["slug"]))

    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index(wines, "assets/" if LOCAL_ASSETS else ""))
    print("  index.html                 -> Fallback-Uebersicht")
    write_urls(wines)
    print("  URLS.md                    -> Adressen je Wein")
    print("%d Seite(n) erzeugt in dist/" % len(wines))
    print("\nAdressen im QR-Code:")
    for w in wines:
        print("  https://%s.lasuite.vin/" % w["slug"])


if __name__ == "__main__":
    main()
