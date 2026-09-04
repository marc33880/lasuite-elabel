#!/usr/bin/env python3
"""
Zieht die E-Label-Daten aus den Shopify-Stammdaten und schreibt wines.json.

Aufgenommen wird jeder Wein, der
  * ein gefuelltes elabel.slug hat  UND
  * custom.harvest_year >= 2024 (bzw. MIN_VINTAGE)

Damit entsteht die Seite eines neuen Weins automatisch, sobald der Slug
eingetragen ist. Kein manuelles Anlegen, kein Template pro Wein.

Aufruf:
  export SHOPIFY_STORE=nqexu6-bs
  export SHOPIFY_TOKEN=shpat_...        # Custom App, Scope: read_products,
  python3 fetch_shopify.py              #   read_translations, read_content
"""
import json
import os
import sys
import urllib.request

STORE = os.environ.get("SHOPIFY_STORE", "nqexu6-bs")
TOKEN = os.environ.get("SHOPIFY_TOKEN")
API = "2025-07"
MIN_VINTAGE = 2024
SHOP_URL = "https://chateaulasuite.com"
STORY_VIEW = "story-2"          # Template product.story-2.json
LANGS = ("de", "en", "fr")
LOCALE_PREFIX = {"de": "", "en": "/en", "fr": "/fr"}
PRODUCER = "Ch&acirc;teau LaSuite aux Conseillans &middot; Bordeaux &middot; France"

ENDPOINT = "https://%s.myshopify.com/admin/api/%s/graphql.json" % (STORE, API)

PRODUCTS_Q = """
query Wines($cursor: String) {
  products(first: 50, after: $cursor, query: "status:active OR status:draft") {
    pageInfo { hasNextPage endCursor }
    edges { node {
      id title handle
      featuredMedia { ... on MediaImage { image { url } } }
      variants(first: 1) { edges { node { title } } }
      harvest:  metafield(namespace: "custom",  key: "harvest_year")      { value }
      grapes:   metafield(namespace: "custom",  key: "rebsorten")         { value }
      bottles:  metafield(namespace: "custom",  key: "flaschenanzahl")    { value }
      slug:     metafield(namespace: "elabel",  key: "slug")              { value }
      zutaten:  metafield(namespace: "elabel",  key: "zutaten")           { id value }
      alc:      metafield(namespace: "elabel",  key: "alcohol_vol")       { value }
      sugar:    metafield(namespace: "elabel",  key: "sugars_g_l")        { value }
      acid:     metafield(namespace: "elabel",  key: "acid_g_l")          { value }
      kcal:     metafield(namespace: "elabel",  key: "energy_kcal_100ml") { value }
    } }
  }
}
"""

TRANSLATION_Q = """
query Tr($ids: [ID!]!, $locale: String!) {
  translatableResourcesByIds(resourceIds: $ids, first: 100) {
    edges { node { resourceId translations(locale: $locale) { key value } } }
  }
}
"""


def call(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": TOKEN,
    })
    with urllib.request.urlopen(req, timeout=45) as r:
        data = json.loads(r.read().decode())
    if "errors" in data:
        raise SystemExit("Shopify-Fehler: %s" % data["errors"])
    return data["data"]


def to_int(value):
    """'1211' -> 1211; '1.211 Flaschen' -> 1211; leer/unlesbar -> None."""
    digits = "".join(c for c in (value or "") if c.isdigit())
    return int(digits) if digits else None


def rich_text_to_html(value):
    """Shopify rich_text_field (JSON) -> schlankes HTML."""
    if not value:
        return ""
    try:
        doc = json.loads(value)
    except (ValueError, TypeError):
        return "<p>%s</p>" % value

    def node(n):
        t = n.get("type")
        kids = "".join(node(c) for c in n.get("children", []))
        if t == "root":
            return kids
        if t == "paragraph":
            return "<p>%s</p>" % kids
        if t == "list":
            tag = "ol" if n.get("listType") == "ordered" else "ul"
            return "<%s>%s</%s>" % (tag, kids, tag)
        if t == "list-item":
            return "<li>%s</li>" % kids
        if t == "text":
            s = (n.get("value") or "").replace("&", "&amp;").replace("<", "&lt;")
            if n.get("bold"):
                s = "<strong>%s</strong>" % s
            if n.get("italic"):
                s = "<em>%s</em>" % s
            return s
        if t == "link":
            # Auf dem E-Label unerwuenscht: Link wird zu reinem Text degradiert.
            return kids
        return kids

    return node(doc)


def main():
    if not TOKEN:
        sys.exit("SHOPIFY_TOKEN fehlt. Custom App in Shopify anlegen, "
                 "Scopes read_products + read_translations.")

    nodes, cursor = [], None
    while True:
        d = call(PRODUCTS_Q, {"cursor": cursor})["products"]
        nodes += [e["node"] for e in d["edges"]]
        if not d["pageInfo"]["hasNextPage"]:
            break
        cursor = d["pageInfo"]["endCursor"]

    wines, skipped = [], []
    for n in nodes:
        slug = (n.get("slug") or {}).get("value")
        harvest = (n.get("harvest") or {}).get("value")
        if not slug:
            continue
        if not harvest or int(harvest) < MIN_VINTAGE:
            skipped.append((n["title"], "Jahrgang %s < %d" % (harvest, MIN_VINTAGE)))
            continue
        alc = (n.get("alc") or {}).get("value")
        if not alc:
            skipped.append((n["title"], "elabel.alcohol_vol fehlt"))
            continue

        title = n["title"]
        # "Louré 2024" -> Name "Louré", Jahrgang "2024"
        name, vintage = title, harvest
        if title.endswith(" " + str(harvest)):
            name = title[: -(len(str(harvest)) + 1)]

        zut = n.get("zutaten") or {}
        wines.append({
            "slug": slug,
            "name": name,
            "vintage": vintage,
            # Dasselbe Feld, aus dem die PDP ihre Assemblage-Schichtung baut.
            # Rebsortennamen sind Eigennamen und werden nicht uebersetzt.
            "grapes": ((n.get("grapes") or {}).get("value") or "").strip(),
            # Limitierung, dieselbe Zahl wie in der Faktenreihe der PDP.
            "bottles": to_int((n.get("bottles") or {}).get("value")),
            "alcohol_vol": float(alc),
            "sugars_g_l": float((n.get("sugar") or {}).get("value") or 0),
            "acid_g_l": float((n.get("acid") or {}).get("value") or 0),
            "energy_kcal_override": (n.get("kcal") or {}).get("value"),
            "_zutaten_gid": zut.get("id"),
            "ingredients": {"de": rich_text_to_html(zut.get("value"))},
            "story_url": {l: "%s%s/products/%s?view=%s"
                             % (SHOP_URL, LOCALE_PREFIX[l], n["handle"], STORY_VIEW)
                          for l in LANGS},
            "logo": LOGO_URL,
            "bottle": ((n.get("featuredMedia") or {}).get("image") or {}).get("url", ""),
            "producer": PRODUCER,
        })

    # Uebersetzungen der Zutatenliste (fr / en) nachladen
    gids = [w["_zutaten_gid"] for w in wines if w["_zutaten_gid"]]
    for lang in ("en", "fr"):
        if not gids:
            break
        d = call(TRANSLATION_Q, {"ids": gids, "locale": lang})
        by_id = {e["node"]["resourceId"]: e["node"]["translations"]
                 for e in d["translatableResourcesByIds"]["edges"]}
        for w in wines:
            tr = by_id.get(w["_zutaten_gid"]) or []
            val = next((t["value"] for t in tr if t["key"] == "value"), None)
            w["ingredients"][lang] = rich_text_to_html(val) if val \
                else w["ingredients"]["de"]

    for w in wines:
        w.pop("_zutaten_gid", None)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "wines.json"), "w", encoding="utf-8") as f:
        json.dump(wines, f, ensure_ascii=False, indent=2)

    print("%d Wein(e) uebernommen:" % len(wines))
    for w in wines:
        miss = [] if w["sugars_g_l"] else ["Restzucker fehlt -> als 0 g gerechnet"]
        print("  %-26s %s %s  %s" % (w["slug"], w["name"], w["vintage"],
                                     ("  ! " + "; ".join(miss)) if miss else ""))
    if skipped:
        print("\nUebersprungen:")
        for t, why in skipped:
            print("  %-28s %s" % (t, why))


LOGO_URL = ("https://cdn.shopify.com/s/files/1/0908/1690/5594/files/"
            "Logo_LaSuite_transparent_final.png?v=1753997357")

if __name__ == "__main__":
    main()
