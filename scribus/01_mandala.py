# -*- coding: utf-8 -*-
"""
01 – MANDALA GENERATIVĂ
Desenează o mandala din „petale” colorate, pe inele concentrice.
Culorile parcurg tot cercul cromatic (HSV), petalele sunt semitransparente.

Rulare: Scribus > Script > Execute Script... > 01_mandala.py
Cere: numărul de petale pe inel și numărul de inele.
"""
import math
import colorsys

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit


def culoare(nume, r, g, b):
    """Definește o culoare RGB (cu revenire pe CMYK la versiuni vechi)."""
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def petala(cx, cy, raza, lungime, latime, unghi_grade, puncte=28):
    """Returnează lista plată [x1,y1,x2,y2,...] a unei elipse rotite
    în jurul centrului paginii (fără a folosi rotateObject)."""
    a = math.radians(unghi_grade)
    lista = []
    for i in range(puncte):
        t = 2 * math.pi * i / puncte
        # elipsa locală: centrul la distanța `raza` de centrul paginii, pe axa y
        lx = latime / 2 * math.cos(t)
        ly = -raza + lungime / 2 * math.sin(t)
        # rotire în jurul originii (centrul paginii)
        x = cx + lx * math.cos(a) - ly * math.sin(a)
        y = cy + lx * math.sin(a) + ly * math.cos(a)
        lista += [x, y]
    return lista


def main():
    n = scribus.valueDialog("Mandala", "Petale pe inel (6–36):", "12")
    inele = scribus.valueDialog("Mandala", "Număr de inele (3–10):", "6")
    n = max(3, int(n or 12))
    inele = max(1, int(inele or 6))

    if not scribus.haveDoc():
        scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                            1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    cx, cy = w / 2.0, h / 2.0
    rmax = min(w, h) / 2.0 - 15

    scribus.setRedraw(False)
    scribus.progressReset()
    scribus.progressTotal(inele * n)

    # fundal întunecat
    culoare("Mandala_Fundal", 18, 18, 38)
    fundal = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Mandala_Fundal", fundal)
    scribus.setLineColor("None", fundal)

    obiecte = [fundal]
    pas = rmax / inele
    for i in range(inele):
        raza = pas * (i + 0.6)
        lungime = pas * 1.7
        latime = min(2 * math.pi * raza / n * 0.85, lungime)
        r, g, b = [int(255 * v) for v in colorsys.hsv_to_rgb(i / float(inele), 0.85, 1.0)]
        nume = "Mandala_Inel_%02d" % (i + 1)
        culoare(nume, r, g, b)
        decalaj = (i % 2) * (180.0 / n)   # inelele alterneze pozițiile petalelor
        for k in range(n):
            unghi = 360.0 * k / n + decalaj
            p = scribus.createPolygon(petala(cx, cy, raza, lungime, latime, unghi))
            scribus.setFillColor(nume, p)
            scribus.setLineColor("White", p)
            scribus.setLineWidth(0.25, p)
            scribus.setFillTransparency(0.55, p)   # 1 = opac, 0 = transparent
            obiecte.append(p)
            scribus.progressSet(i * n + k + 1)

    # nucleul central
    culoare("Mandala_Nucleu", 255, 240, 120)
    nucleu = scribus.createEllipse(cx - pas * 0.5, cy - pas * 0.5, pas, pas)
    scribus.setFillColor("Mandala_Nucleu", nucleu)
    scribus.setLineColor("White", nucleu)
    scribus.setLineWidth(0.6, nucleu)
    obiecte.append(nucleu)

    scribus.groupObjects(obiecte)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Mandala", "Gata: %d petale x %d inele = %d obiecte."
                       % (n, inele, n * inele), scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
