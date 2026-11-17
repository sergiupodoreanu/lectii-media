# -*- coding: utf-8 -*-
"""
02 – POSTER TIPOGRAFIC (afiș „cuvinte umplute pe lățime”)
Scriu o frază, scriptul o desface în cuvinte și așază fiecare cuvânt pe un rând,
cu corpul de literă calculat astfel încât cuvântul să umple lățimea paginii.
Cuvintele scurte devin uriașe, cele lungi mai mici – efect de afiș modern.

Rulare: Script > Execute Script... > 02_poster_tipografic.py
"""
try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

MM = 72.0 / 25.4          # 1 mm = 2.835 pt
PALETA = [                # (nume, R, G, B)
    ("Poster_Galben", 255, 200, 0),
    ("Poster_Rosu", 230, 40, 60),
    ("Poster_Turcoaz", 0, 190, 200),
    ("Poster_Alb", 255, 255, 255),
    ("Poster_Roz", 255, 120, 180),
]


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def font_gros():
    """Alege un font bold disponibil în sistem."""
    fonturi = scribus.getFontNames()
    for pref in ("DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold",
                 "Noto Sans Bold", "Ubuntu Bold"):
        if pref in fonturi:
            return pref
    for f in fonturi:
        if "Bold" in f:
            return f
    return fonturi[0]


def potriveste(cadru, corp):
    """Micșorează corpul de literă până când textul încape în cadru
    (lățimea literelor diferă de la un font la altul)."""
    for _ in range(80):
        try:
            scribus.layoutText(cadru)
        except Exception:
            pass
        if not scribus.textOverflows(cadru):
            break
        corp *= 0.96
        scribus.setFontSize(corp, cadru)
        scribus.setLineSpacing(corp, cadru)
    return corp


def main():
    fraza = scribus.valueDialog("Poster tipografic", "Fraza afișului:",
                                "GRAFICA ESTE LIMBAJUL FORMELOR SI AL CULORII")
    if not fraza:
        return
    cuvinte = fraza.split()

    scribus.newDocument((297.0, 420.0), (15, 15, 15, 15), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    sus, st, jos, dr = 15, 15, 15, 15
    lat = w - st - dr

    for nume, r, g, b in PALETA:
        culoare(nume, r, g, b)
    culoare("Poster_Fundal", 20, 20, 25)

    scribus.setRedraw(False)
    fundal = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Poster_Fundal", fundal)
    scribus.setLineColor("None", fundal)

    font = font_gros()
    y = sus
    i = 0
    spatiu = 2.0            # mm între rânduri
    while True:
        cuv = cuvinte[i % len(cuvinte)]
        # lățimea unei litere ≈ 0,62 din corp (font bold); calculăm corpul în pt
        corp = lat * MM / (0.62 * len(cuv))
        corp = min(corp, 420.0)
        inaltime = corp * 1.3 / MM           # înălțimea cadrului în mm
        cadru = scribus.createText(st, y, lat, inaltime)
        scribus.setText(cuv, cadru)
        scribus.setFont(font, cadru)
        scribus.setFontSize(corp, cadru)
        scribus.setLineSpacing(corp * 1.0, cadru)
        scribus.setTextAlignment(scribus.ALIGN_CENTERED, cadru)
        scribus.setTextColor(PALETA[i % len(PALETA)][0], cadru)
        corp = potriveste(cadru, corp)       # corecție după fontul real
        inaltime = corp * 1.3 / MM
        ramas = h - jos - y                  # cât loc mai este pe pagină
        if inaltime > ramas:
            if ramas < 20:
                scribus.deleteObject(cadru)  # nu mai încape niciun rând
                break
            corp = ramas * MM / 1.3          # ultimul rând: cât permite spațiul rămas
            scribus.setFontSize(corp, cadru)
            scribus.setLineSpacing(corp, cadru)
            inaltime = ramas
        scribus.sizeObject(lat, inaltime, cadru)
        y += inaltime + spatiu
        i += 1

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Poster", "%d rânduri așezate. Schimbă fraza și rulează din nou!"
                       % i, scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
