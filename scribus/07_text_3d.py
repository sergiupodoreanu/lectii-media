# -*- coding: utf-8 -*-
"""
07 – TITLU 3D CU EXTRUZIE ȘI REFLEXIE
Un cuvânt scris de 25 de ori, fiecare copie deplasată puțin pe diagonală și
cu o nuanță tot mai deschisă → efect de literă „extrudată” în 3D.
Sub el, o copie răsturnată, semitransparentă → reflexie ca pe o suprafață lucioasă.

Rulare: Script > Execute Script... > 07_text_3d.py
"""
import colorsys

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

MM = 72.0 / 25.4


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def font_gros():
    fonturi = scribus.getFontNames()
    for p in ("DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold", "Impact"):
        if p in fonturi:
            return p
    for f in fonturi:
        if "Bold" in f:
            return f
    return fonturi[0]


def text(x, y, w, h, s, f, corp, cul):
    t = scribus.createText(x, y, w, h)
    scribus.setText(s, t)
    scribus.setFont(f, t)
    scribus.setFontSize(corp, t)
    scribus.setLineSpacing(corp, t)
    scribus.setTextColor(cul, t)
    scribus.setTextAlignment(scribus.ALIGN_CENTERED, t)
    return t


def main():
    cuv = scribus.valueDialog("Titlu 3D", "Cuvântul (scurt, cu majuscule):", "MOISIL")
    if not cuv:
        return
    nuanta = float(scribus.valueDialog("Titlu 3D", "Nuanța 0–360 (0 roșu, 120 verde, 220 albastru, 280 violet):", "210") or 210)
    straturi = 25

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()

    culoare("T3D_Fundal", 12, 12, 18)
    scribus.setRedraw(False)
    fnd = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("T3D_Fundal", fnd)
    scribus.setLineColor("None", fnd)

    f = font_gros()
    lat = w - 40
    corp = min(lat * MM / (0.68 * len(cuv)), 300.0)
    # probă: micșorăm corpul până când cuvântul încape pe lățime cu fontul real
    proba = text(20, 20, lat, corp * 1.3 / MM, cuv, f, corp, "T3D_Fundal")
    for _ in range(80):
        try:
            scribus.layoutText(proba)
        except Exception:
            pass
        if not scribus.textOverflows(proba):
            break
        corp *= 0.96
        scribus.setFontSize(corp, proba)
        scribus.setLineSpacing(corp, proba)
    scribus.deleteObject(proba)
    inalt = corp * 1.3 / MM
    x0, y0 = 20, h * 0.42 - inalt / 2

    # culorile straturilor: de la închis (spate) la deschis (față)
    for i in range(straturi):
        v = 0.25 + 0.75 * i / (straturi - 1)          # luminozitate
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(nuanta / 360.0, 0.9, v)]
        culoare("T3D_%02d" % i, r, g, b)

    # extruzia: copii deplasate spre stânga-jos, cea din față ultima
    pas = 0.9
    for i in range(straturi):
        dep = (straturi - 1 - i) * pas
        text(x0 - dep, y0 + dep, lat, inalt, cuv, f, corp, "T3D_%02d" % i)

    # reflexia: copie răsturnată vertical, sub cuvânt, semitransparentă
    culoare("T3D_Reflex", 120, 160, 220)
    yr = y0 + inalt + 2
    refl = text(x0, yr, lat, inalt, cuv, f, corp, "T3D_Reflex")
    try:
        scribus.flipObject(False, True, refl)          # oglindire verticală
    except Exception:
        pass
    scribus.setFillTransparency(0.25, refl)
    # „ceață” care estompează reflexia spre jos (benzi tot mai opace)
    benzi = 12
    for k in range(benzi):
        by = yr + inalt * 0.15 + k * (inalt * 0.9 / benzi)
        bh = inalt * 0.9 / benzi + 0.3
        band = scribus.createRect(0, by, w, bh)
        scribus.setFillColor("T3D_Fundal", band)
        scribus.setLineColor("None", band)
        scribus.setFillTransparency(0.25 + 0.75 * k / (benzi - 1), band)

    # linia de „podea”
    culoare("T3D_Linie", 80, 100, 140)
    lin = scribus.createLine(20, y0 + inalt + 1, w - 20, y0 + inalt + 1)
    scribus.setLineColor("T3D_Linie", lin)
    scribus.setLineWidth(0.4, lin)

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Titlu 3D", "%d straturi + reflexie. Încearcă alt cuvânt sau altă nuanță!"
                       % straturi, scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
