#!/usr/bin/env python3
"""
Holt die Bilder einmalig nach assets/, damit die fertigen Seiten zur Laufzeit
keinen einzigen Fremd-Request mehr brauchen:

  assets/logo.png                     Wortmarke
  assets/<slug>.jpg                   Etikett je Wein

Die Schrift Jost liegt bereits im Repo (assets/jost-*.woff2, SIL Open Font
License, aus dem npm-Paket @fontsource/jost). Sie wird NICHT mehr geholt: fuer
die Veroeffentlichung soll niemand auf Google Fonts angewiesen sein, und vier
Dateien von je 10 KB gehoeren in ein Repo, das zwanzig Jahre halten soll.
Zum Erneuern:  npm pack @fontsource/jost  und die latin-Subsets kopieren.

Danach:  LOCAL_ASSETS=1 python3 build.py
"""
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
UA = {"User-Agent": "Mozilla/5.0 (compatible; lasuite-elabel-build)"}

GF_CSS = ("https://fonts.googleapis.com/css2"
          "?family=Jost:wght@200;300;400;500&display=swap")
OFL = "https://raw.githubusercontent.com/google/fonts/main/ofl/jost/OFL.txt"


def get(url, dest, binary=True):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    mode = "wb" if binary else "w"
    with open(dest, mode) as f:
        f.write(data if binary else data.decode())
    print("  %-34s %6.1f KB" % (os.path.basename(dest), len(data) / 1024.0))


def fonts():
    req = urllib.request.Request(GF_CSS, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        css = r.read().decode()
    # Google liefert je Gewicht einen @font-face-Block mit latin-Subset zuletzt.
    blocks = css.split("@font-face")
    found = {}
    for b in blocks:
        w = re.search(r"font-weight:\s*(\d+)", b)
        u = re.search(r"url\((https://[^)]+\.woff2)\)", b)
        if w and u and w.group(1) in ("200", "300", "400", "500"):
            found[w.group(1)] = u.group(1)   # letzter Treffer = latin
    for weight, url in sorted(found.items()):
        get(url, os.path.join(ASSETS, "jost-%s.woff2" % weight))
    get(OFL, os.path.join(ASSETS, "OFL.txt"), binary=False)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ROOT, "wines.json"), encoding="utf-8") as f:
        wines = json.load(f)

    print("Bilder:")
    get(wines[0]["logo"], os.path.join(ASSETS, "logo.png"))
    for w in wines:
        if w.get("bottle"):
            get(w["bottle"], os.path.join(ASSETS, "%s.jpg" % w["slug"]))
    print("\nFertig. Jetzt:  LOCAL_ASSETS=1 python3 build.py")


if __name__ == "__main__":
    main()
