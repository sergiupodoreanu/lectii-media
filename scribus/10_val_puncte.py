# -*- coding: utf-8 -*-
"""
10 – VAL DE PUNCTE (raster tipografic „viu”)
O grilă de puncte în care diametrul și culoarea fiecărui punct urmează o
funcție matematică z = sin(x)·cos(y) + unde circulare. Rezultatul arată ca un
relief 3D / o suprafață de apă văzută de sus – principiul rasterului din tipar
(puncte mari = ton închis, puncte mici = ton deschis).

Rulare: Script > Execute Script... > 10_val_puncte.py
Cere: numărul de coloane și „frecvența” valurilor.
"""
import math
import colorsys

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

TREPTE = 16     # câte culori distincte pe scara de valori


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def functie(u, v, frecv):
    """u, v în [0, 1]. Returnează o valoare în [0, 1]."""
    z1 = math.sin(u * frecv * math.pi) * math.cos(v * frecv * math.pi)
    d = math.hypot(u - 0.5, v - 0.5)
    z2 = math.sin(d * frecv * 2.2 * math.pi)
    return (z1 * 0.6 + z2 * 0.4 + 1) / 2.0


def main():
    col = int(scribus.valueDialog("Val de puncte", "Coloane (20–60):", "36") or 36)
    frecv = float(scribus.valueDialog("Val de puncte", "Frecvența valurilor (1–6):", "3") or 3)
    col = max(5, min(90, col))

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    m = 12.0
    pas = (w - 2 * m) / col
    rnd = int((h - 2 * m) / pas)

    culoare("Val_Fundal", 15, 20, 35)
    fnd = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Val_Fundal", fnd)
    scribus.setLineColor("None", fnd)

    # scara de culori: albastru adânc → turcoaz → galben
    for k in range(TREPTE):
        t = k / float(TREPTE - 1)
        hue = 0.62 - 0.48 * t              # 0.62 albastru → 0.14 galben
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, 0.85, 0.5 + 0.5 * t)]
        culoare("Val_%02d" % k, r, g, b)

    scribus.setRedraw(False)
    scribus.progressTotal(rnd)
    total = 0
    for j in range(rnd):
        for i in range(col):
            u, v = (i + 0.5) / col, (j + 0.5) / rnd
            z = functie(u, v, frecv)
            d = pas * (0.15 + 0.85 * z)
            x = m + i * pas + pas / 2 - d / 2
            y = m + j * pas + pas / 2 - d / 2
            e = scribus.createEllipse(x, y, d, d)
            scribus.setFillColor("Val_%02d" % int(z * (TREPTE - 1)), e)
            scribus.setLineColor("None", e)
            total += 1
        scribus.progressSet(j + 1)

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Val de puncte", "%d puncte (%d x %d). Schimbă funcția `functie()` și rulează!"
                       % (total, col, rnd), scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
