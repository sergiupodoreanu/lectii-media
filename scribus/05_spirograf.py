# -*- coding: utf-8 -*-
"""
05 – SPIROGRAF (curbe hipotrohoide, ca jucăria Spirograph)
Desenează mai multe curbe matematice suprapuse, în culori diferite,
din polilinii cu mii de puncte. Parametrii R, r, d dau forme complet diferite.

x(t) = (R - r)·cos t + d·cos((R - r)/r · t)
y(t) = (R - r)·sin t - d·sin((R - r)/r · t)

Rulare: Script > Execute Script... > 05_spirograf.py
"""
import math
import colorsys

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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def spirograf(cx, cy, R, r, d, scara, puncte=1500):
    # numărul de rotații până când curba se închide
    rot = r // gcd(int(R), int(r))
    lista = []
    for i in range(puncte + 1):
        t = 2 * math.pi * rot * i / puncte
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        lista += [cx + x * scara, cy + y * scara]
    return lista


def main():
    nr = scribus.valueDialog("Spirograf", "Câte curbe suprapuse (1–8):", "5")
    nr = max(1, min(8, int(nr or 5)))

    if not scribus.haveDoc():
        scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                            1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    cx, cy = w / 2.0, h / 2.0
    raza_max = min(w, h) / 2.0 - 15

    culoare("Spiro_Fundal", 10, 10, 20)
    fundal = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Spiro_Fundal", fundal)
    scribus.setLineColor("None", fundal)

    # seturi de parametri (R, r, d) care dau forme frumoase
    seturi = [(100, 37, 40), (100, 43, 60), (100, 61, 45), (100, 29, 70),
              (100, 71, 30), (100, 53, 55), (100, 23, 40), (100, 67, 65)]

    scribus.setRedraw(False)
    obiecte = [fundal]
    for i in range(nr):
        R, r, d = seturi[i % len(seturi)]
        intindere = (R - r) + d                     # raza maximă a curbei
        scara = raza_max / float(intindere)
        rr, gg, bb = [int(255 * v) for v in colorsys.hsv_to_rgb(i / float(nr), 0.7, 1.0)]
        nume = "Spiro_%d" % (i + 1)
        culoare(nume, rr, gg, bb)
        linie = scribus.createPolyLine(spirograf(cx, cy, R, r, d, scara))
        scribus.setLineColor(nume, linie)
        scribus.setLineWidth(0.35, linie)
        scribus.setFillColor("None", linie)
        obiecte.append(linie)

    scribus.groupObjects(obiecte)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Spirograf", "%d curbe desenate. Modifică seturile (R, r, d) "
                       "din script și vezi ce se întâmplă!" % nr, scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
