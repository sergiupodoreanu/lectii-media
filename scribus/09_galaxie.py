# -*- coding: utf-8 -*-
"""
09 – GALAXIE SPIRALĂ
Mii de „stele” (cercuri mici, semitransparente) așezate pe brațe spiralate
logaritmice, cu împrăștiere aleatoare; nucleu luminos din cercuri concentrice
tot mai transparente (efect de strălucire) și câteva stele mari cu halou.

Rulare: Script > Execute Script... > 09_galaxie.py
Cere: numărul de brațe și numărul de stele.
"""
import math
import random

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def cerc(x, y, d, cul, alfa):
    e = scribus.createEllipse(x - d / 2, y - d / 2, d, d)
    scribus.setFillColor(cul, e)
    scribus.setLineColor("None", e)
    scribus.setFillTransparency(alfa, e)
    return e


def main():
    brate = int(scribus.valueDialog("Galaxie", "Număr de brațe (2–6):", "3") or 3)
    stele = int(scribus.valueDialog("Galaxie", "Număr de stele (500–3000):", "1500") or 1500)
    brate = max(1, min(8, brate))

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    cx, cy = w / 2.0, h / 2.0
    rmax = min(w, h) / 2.0 - 8

    culoare("Gal_Fundal", 4, 4, 12)
    fnd = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Gal_Fundal", fnd)
    scribus.setLineColor("None", fnd)

    # paleta stelelor: albastru (exterior) → alb → galben (interior)
    paleta = [("Gal_Albastru", 120, 160, 255), ("Gal_Alb", 240, 245, 255),
              ("Gal_Galben", 255, 230, 150), ("Gal_Portocaliu", 255, 180, 90),
              ("Gal_Roz", 255, 150, 200)]
    for n, r, g, b in paleta:
        culoare(n, r, g, b)

    scribus.setRedraw(False)
    scribus.progressTotal(stele)

    # stele de fundal, împrăștiate uniform
    for i in range(stele // 6):
        cerc(random.uniform(0, w), random.uniform(0, h), random.uniform(0.15, 0.5),
             "Gal_Alb", random.uniform(0.3, 0.9))

    # brațele spiralate: r = a * e^(b*theta)
    b = 0.27
    for i in range(stele):
        brat = i % brate
        t = random.uniform(0, 3.2 * math.pi)
        r = rmax * 0.06 * math.exp(b * t)
        if r > rmax:
            continue
        theta = t + brat * 2 * math.pi / brate
        # împrăștiere perpendiculară pe braț, mai mare spre exterior
        imprastiere = random.gauss(0, 1.5 + r * 0.08)
        x = cx + r * math.cos(theta) - imprastiere * math.sin(theta)
        y = cy + r * math.sin(theta) + imprastiere * math.cos(theta)
        frac = r / rmax
        if frac < 0.25:
            cul = random.choice(["Gal_Galben", "Gal_Portocaliu", "Gal_Alb"])
        elif frac < 0.6:
            cul = random.choice(["Gal_Alb", "Gal_Alb", "Gal_Galben", "Gal_Roz"])
        else:
            cul = random.choice(["Gal_Albastru", "Gal_Albastru", "Gal_Alb"])
        d = random.uniform(0.2, 1.4) * (1.3 - frac)
        cerc(x, y, d, cul, random.uniform(0.35, 0.95))
        scribus.progressSet(i + 1)

    # nucleul: cercuri concentrice cu transparență crescândă (strălucire)
    for k in range(14, 0, -1):
        d = rmax * 0.03 * k
        cerc(cx, cy, d, "Gal_Galben", 0.12 if k > 2 else 0.6)
    cerc(cx, cy, rmax * 0.06, "Gal_Alb", 0.95)

    # câteva stele mari cu halou
    for i in range(7):
        x, y = random.uniform(15, w - 15), random.uniform(15, h - 15)
        for k in range(4, 0, -1):
            cerc(x, y, 1.2 * k, "Gal_Albastru", 0.15)
        cerc(x, y, 1.0, "Gal_Alb", 1.0)
        for ang in (0, 90):
            lin1 = scribus.createLine(x - 3, y, x + 3, y) if ang == 0 else scribus.createLine(x, y - 3, x, y + 3)
            scribus.setLineColor("Gal_Alb", lin1)
            scribus.setLineWidth(0.15, lin1)

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Galaxie", "Gata. Fiecare rulare dă altă galaxie (hazard).",
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
