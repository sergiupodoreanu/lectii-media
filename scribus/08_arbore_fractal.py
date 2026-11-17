# -*- coding: utf-8 -*-
"""
08 – ARBORE FRACTAL
Desenează recursiv un copac: fiecare ramură se desface în două ramuri mai scurte,
rotite stânga/dreapta. Grosimea scade, culoarea trece de la maro (trunchi)
la verde (frunze). Puțin hazard → fiecare copac e altfel.

Rulare: Script > Execute Script... > 08_arbore_fractal.py
Cere: adâncimea (nivele) și unghiul de ramificare.
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


def amestec(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def ramura(x, y, lung, unghi, nivel, maxim, deschidere, contor):
    if nivel > maxim or lung < 0.8:
        return
    a = math.radians(unghi)
    x2 = x + lung * math.cos(a)
    y2 = y - lung * math.sin(a)
    lin = scribus.createLine(x, y, x2, y2)
    scribus.setLineColor("Arb_%02d" % nivel, lin)
    scribus.setLineWidth(max(0.2, 5.0 * (1 - nivel / float(maxim + 1)) ** 2), lin)
    try:
        scribus.setLineEnd(scribus.CAP_ROUND, lin)
    except Exception:
        pass
    contor[0] += 1
    # frunze la vârf
    if nivel == maxim:
        d = random.uniform(1.5, 3.0)
        fr = scribus.createEllipse(x2 - d / 2, y2 - d / 2, d, d)
        scribus.setFillColor("Arb_Frunza%d" % random.randint(0, 2), fr)
        scribus.setLineColor("None", fr)
        scribus.setFillTransparency(0.7, fr)
        return
    scurtare = random.uniform(0.66, 0.78)
    ramura(x2, y2, lung * scurtare, unghi + deschidere + random.uniform(-8, 8),
           nivel + 1, maxim, deschidere, contor)
    ramura(x2, y2, lung * scurtare, unghi - deschidere + random.uniform(-8, 8),
           nivel + 1, maxim, deschidere, contor)


def main():
    maxim = int(scribus.valueDialog("Arbore fractal", "Nivele (6–11; 11 = ~4000 ramuri):", "9") or 9)
    maxim = max(2, min(12, maxim))
    deschidere = float(scribus.valueDialog("Arbore fractal", "Unghi de ramificare (15–45):", "25") or 25)

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()

    # cer (benzi de gradient) + pământ
    for k in range(20):
        r, g, b = amestec((20, 30, 70), (180, 200, 240), k / 19.0)
        culoare("Arb_Cer%02d" % k, r, g, b)
        band = scribus.createRect(0, h * 0.85 * k / 20, w, h * 0.85 / 20 + 0.5)
        scribus.setFillColor("Arb_Cer%02d" % k, band)
        scribus.setLineColor("None", band)
    culoare("Arb_Pamant", 60, 90, 40)
    sol = scribus.createRect(0, h * 0.85, w, h * 0.15)
    scribus.setFillColor("Arb_Pamant", sol)
    scribus.setLineColor("None", sol)

    # culorile nivelelor: maro → verde
    for n in range(maxim + 1):
        r, g, b = amestec((90, 55, 25), (40, 160, 60), n / float(maxim))
        culoare("Arb_%02d" % n, r, g, b)
    culoare("Arb_Frunza0", 120, 200, 80)
    culoare("Arb_Frunza1", 230, 180, 60)
    culoare("Arb_Frunza2", 220, 90, 70)

    scribus.setRedraw(False)
    contor = [0]
    ramura(w / 2.0, h * 0.85, h * 0.2, 90, 0, maxim, deschidere, contor)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Arbore fractal", "%d ramuri desenate. Rulează din nou: copacul va fi altul!"
                       % contor[0], scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
