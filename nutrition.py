"""
Nährwertberechnung für Wein-E-Labels.

Grundlage: VO (EU) 1169/2011 Anhang XIV (Umrechnungsfaktoren) sowie die
Auslegung des LGL Bayern zur Wein-Nährwertdeklaration (Berechnung aus
Durchschnitts-/Analysewerten zulässig, Glycerin schätzbar als ca. 10 % des
gebildeten Alkohols in g/l).

Umrechnungsfaktoren:
  Alkohol (Ethanol)          7,0 kcal/g   29 kJ/g
  Kohlenhydrate (Zucker)     4,0 kcal/g   17 kJ/g
  Polyole (Glycerin)         2,4 kcal/g   10 kJ/g
  Organische Säuren          3,0 kcal/g   13 kJ/g

Bezugsgröße aller Ausgabewerte: 100 ml.
Rundung nach VO 1169/2011 Anhang V bzw. Leitlinien:
  Brennwert            ohne Dezimalstelle
  Kohlenhydrate/Zucker < 10 g -> 0,1 g genau, >= 10 g -> ganzzahlig
  Salz                 0,01 g genau
"""

ETHANOL_DENSITY = 0.78924  # g/ml -> Alkohol g/l = %vol * 7,8924

KCAL_ALCOHOL, KJ_ALCOHOL = 7.0, 29.0
KCAL_CARB, KJ_CARB = 4.0, 17.0
KCAL_POLYOL, KJ_POLYOL = 2.4, 10.0
KCAL_ACID, KJ_ACID = 3.0, 13.0

GLYCEROL_SHARE = 0.10  # Glycerin ~ 10 % des Alkohols (g/l)


def compute(alcohol_vol, sugars_g_l=0.0, acid_g_l=0.0, kcal_override=None):
    """Liefert ein Dict mit allen sieben Pflichtangaben je 100 ml."""
    alcohol_vol = float(alcohol_vol)
    sugars_g_l = float(sugars_g_l or 0.0)
    acid_g_l = float(acid_g_l or 0.0)

    # Gramm je 100 ml
    alcohol_g = alcohol_vol * ETHANOL_DENSITY * 10 / 10      # %vol -> g/100ml
    glycerol_g = (alcohol_vol * ETHANOL_DENSITY * 10) * GLYCEROL_SHARE / 10
    sugars_g = sugars_g_l / 10
    acid_g = acid_g_l / 10

    # Kohlenhydrate im Sinne der VO = Zucker + mehrwertige Alkohole (Glycerin)
    carbs_g = sugars_g + glycerol_g

    kcal = (alcohol_g * KCAL_ALCOHOL + sugars_g * KCAL_CARB
            + glycerol_g * KCAL_POLYOL + acid_g * KCAL_ACID)
    kj = (alcohol_g * KJ_ALCOHOL + sugars_g * KJ_CARB
          + glycerol_g * KJ_POLYOL + acid_g * KJ_ACID)

    if kcal_override:
        kcal = float(kcal_override)
        kj = kcal * 4.184

    return {
        "kj": int(round(kj)),
        "kcal": int(round(kcal)),
        "fat": 0.0,
        "saturates": 0.0,
        "carbs": _round_g(carbs_g),
        "sugars": _round_g(sugars_g),
        "protein": None,   # -> "< 0,5 g"
        "salt": None,      # -> "< 0,01 g"
        "_alcohol_g": round(alcohol_g, 2),
        "_glycerol_g": round(glycerol_g, 2),
    }


def _round_g(v):
    return int(round(v)) if v >= 10 else round(v + 1e-9, 1)


def fmt_g(v, lang):
    """Grammwert sprachgerecht formatieren."""
    if isinstance(v, int):
        s = str(v)
    else:
        s = ("%.1f" % v)
    if lang in ("de", "fr"):
        s = s.replace(".", ",")
    return s


if __name__ == "__main__":
    # Plausibilitätsprüfung: trockener Weißwein 12,5 % vol
    r = compute(12.5, sugars_g_l=1.5, acid_g_l=5.4)
    print(r)
    assert 70 <= r["kcal"] <= 78, r
    # Rotwein 14 % vol, 2 g/l Zucker
    r2 = compute(14.0, sugars_g_l=2.0, acid_g_l=5.0)
    print(r2)
    assert 78 <= r2["kcal"] <= 88, r2
    # Süßwein 11 % vol, 120 g/l Zucker
    r3 = compute(11.0, sugars_g_l=120.0, acid_g_l=6.0)
    print(r3)
    assert r3["carbs"] >= 12, r3
    print("Plausibilitaetspruefung OK")
