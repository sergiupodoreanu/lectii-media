# -*- coding: utf-8 -*-
"""
11 – TEXT PE SPIRALĂ
Literele unei fraze sunt așezate una câte una pe o spirală arhimedică
(r = a + b·θ), fiecare rotită după tangenta la curbă; corpul de literă
crește spre exterior, culoarea parcurge cercul cromatic.

Rulare: Script > Execute Script... > 11_text_spirala.py
"""
import math
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
    for p in ("DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"):
        if p in fonturi:
            return p
    for f in fonturi:
        if "Bold" in f:
            return f
    return fonturi[0]


def main():
    fraza = scribus.valueDialog("Text pe spirală", "Textul (se repetă până umple spirala):",
                                "PRODUCTIE MEDIA * LICEUL MOISIL BUZAU * ")
    if not fraza:
        return
    ture = float(scribus.valueDialog("Text pe spirală", "Număr de ture (2–6):", "4") or 4)

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    cx, cy = w / 2.0, h / 2.0
    rmax = min(w, h) / 2.0 - 12

    culoare("Spir_Fundal", 250, 246, 238)
    fnd = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Spir_Fundal", fnd)
    scribus.setLineColor("None", fnd)

    f = font_gros()
    ncul = 24
    for k in range(ncul):
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(k / float(ncul), 0.8, 0.8)]
        culoare("Spir_%02d" % k, r, g, b)

    scribus.setRedraw(False)
    theta_max = ture * 2 * math.pi
    a = 6.0                             # raza de start
    b = (rmax - a) / theta_max          # creșterea razei pe radian
    theta = 0.0
    i = 0
    n = 0
    while theta < theta_max:
        r = a + b * theta
        corp_pt = 10 + 26 * (r / rmax)           # corpul crește spre exterior
        lat_mm = corp_pt * 0.7 / MM              # lățimea aproximativă a literei
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        ch = fraza[i % len(fraza)]
        i += 1
        if ch != " ":
            fw, fh = lat_mm * 1.6, corp_pt * 1.2 / MM
            t = scribus.createText(x - fw / 2, y - fh / 2, fw, fh)
            scribus.setText(ch, t)
            scribus.setFont(f, t)
            scribus.setFontSize(corp_pt, t)
            scribus.setLineSpacing(corp_pt, t)
            scribus.setTextAlignment(scribus.ALIGN_CENTERED, t)
            scribus.setTextColor("Spir_%02d" % (n % ncul), t)
            # rotire după tangentă (Scribus rotește în sens trigonometric)
            unghi_tangenta = math.degrees(theta) + 90
            scribus.rotateObject(-unghi_tangenta, t)
            n += 1
        # pasul unghiular astfel încât literele să fie la distanță ≈ lat_mm
        theta += lat_mm * 1.15 / max(r, 1.0)

    # ghidajul spiralei, subțire, în spate (opțional – comentează dacă nu-l vrei)
    culoare("Spir_Ghid", 200, 195, 185)
    puncte = []
    tt = 0.0
    while tt <= theta_max:
        rr = a + b * tt
        puncte += [cx + rr * math.cos(tt), cy + rr * math.sin(tt)]
        tt += 0.05
    ghid = scribus.createPolyLine(puncte)
    scribus.setLineColor("Spir_Ghid", ghid)
    scribus.setLineWidth(0.3, ghid)
    scribus.setFillColor("None", ghid)

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Text pe spirală", "%d litere așezate pe %.0f ture." % (n, ture),
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
