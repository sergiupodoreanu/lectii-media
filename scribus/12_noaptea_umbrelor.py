# -*- coding: utf-8 -*-
"""
12 – NOAPTEA UMBRELOR (compoziție Halloween)
O lume fantastică: lună uriașă cu halou, copaci morți fractali, ceață în straturi,
cimitir cu pietre înclinate, dovleci cu ochi de foc, lilieci, fantome
semitransparente, ochi roșii în întuneric – și, în centru, un om singur
a cărui umbră-suflet e trasă într-un vârtej violet către lumea umbrelor.
Titlu cu litere „sângerânde”.

Rulare: Script > Execute Script... > 12_noaptea_umbrelor.py
Fiecare rulare dă altă scenă (hazard controlat).
"""
import math
import random

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

MM = 72.0 / 25.4
W = H = 0.0


# ---------- utilitare ----------
def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def amestec(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def font_gros():
    fonturi = scribus.getFontNames()
    for p in ("DejaVu Serif Bold", "Liberation Serif Bold", "Times New Roman Bold",
              "DejaVu Sans Bold", "Arial Bold"):
        if p in fonturi:
            return p
    for f in fonturi:
        if "Bold" in f:
            return f
    return fonturi[0]


def rect(x, y, w, h, cul, alfa=1.0):
    r = scribus.createRect(x, y, w, h)
    scribus.setFillColor(cul, r)
    scribus.setLineColor("None", r)
    if alfa < 1.0:
        scribus.setFillTransparency(alfa, r)
    return r


def cerc(x, y, d, cul, alfa=1.0):
    e = scribus.createEllipse(x - d / 2, y - d / 2, d, d)
    scribus.setFillColor(cul, e)
    scribus.setLineColor("None", e)
    if alfa < 1.0:
        scribus.setFillTransparency(alfa, e)
    return e


def elipsa(x, y, w, h, cul, alfa=1.0):
    e = scribus.createEllipse(x - w / 2, y - h / 2, w, h)
    scribus.setFillColor(cul, e)
    scribus.setLineColor("None", e)
    if alfa < 1.0:
        scribus.setFillTransparency(alfa, e)
    return e


def poligon(puncte, cul, alfa=1.0):
    plat = []
    for px, py in puncte:
        plat += [px, py]
    p = scribus.createPolygon(plat)
    scribus.setFillColor(cul, p)
    scribus.setLineColor("None", p)
    if alfa < 1.0:
        scribus.setFillTransparency(alfa, p)
    return p


def halou(x, y, d, cul, inele=6, alfa=0.12):
    """cercuri concentrice tot mai mari și transparente = strălucire"""
    for k in range(inele, 0, -1):
        cerc(x, y, d * (1 + 0.35 * k), cul, alfa)


# ---------- elementele scenei ----------
def cer():
    for k in range(30):
        r, g, b = amestec((5, 2, 15), (70, 20, 90), k / 29.0)
        culoare("Hw_Cer%02d" % k, r, g, b)
        rect(0, H * k / 30, W, H / 30 + 0.5, "Hw_Cer%02d" % k)
    for i in range(160):
        cerc(random.uniform(0, W), random.uniform(0, H * 0.6),
             random.uniform(0.15, 0.5), "White", random.uniform(0.3, 0.9))


def luna(x, y, d):
    halou(x, y, d, "Hw_LunaHalo", inele=8, alfa=0.08)
    cerc(x, y, d, "Hw_Luna")
    # cratere
    for i in range(7):
        a = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, d * 0.38)
        cerc(x + r * math.cos(a), y + r * math.sin(a), random.uniform(2, 6), "Hw_LunaUmbra", 0.35)


def ramura(x, y, lung, unghi, nivel, maxim):
    if nivel > maxim:
        return
    a = math.radians(unghi)
    x2, y2 = x + lung * math.cos(a), y - lung * math.sin(a)
    # ramură = poligon subțire (ca să pot da grosime variabilă cu umplere neagră)
    g1 = 3.0 * (1 - nivel / float(maxim + 1)) ** 2 + 0.15
    g2 = g1 * 0.6
    nx, ny = -math.sin(a), -math.cos(a)
    poligon([(x + nx * g1, y + ny * g1), (x2 + nx * g2, y2 + ny * g2),
             (x2 - nx * g2, y2 - ny * g2), (x - nx * g1, y - ny * g1)], "Hw_Negru")
    if nivel == maxim:
        return
    n = random.choice([2, 2, 3])
    for k in range(n):
        dev = random.uniform(20, 45) * (1 if k % 2 else -1) + random.uniform(-10, 10)
        ramura(x2, y2, lung * random.uniform(0.6, 0.75), unghi + dev, nivel + 1, maxim)


def copac_mort(x, y, inalt):
    ramura(x, y, inalt, 90 + random.uniform(-8, 8), 0, 7)


def deal(y_sus):
    puncte = [(0, H)]
    x = 0.0
    while x <= W:
        puncte.append((x, y_sus + 6 * math.sin(x / 25.0) + 3 * math.sin(x / 7.0)))
        x += 4
    puncte += [(W, H)]
    poligon(puncte, "Hw_Negru")


def ceata(y, grosime, alfa):
    for i in range(14):
        elipsa(random.uniform(-10, W + 10), y + random.uniform(-grosime / 3, grosime / 3),
               random.uniform(60, 130), grosime, "Hw_Ceata", alfa)


def piatra_funerara(x, y, w, h, inclinare):
    p = scribus.createRect(x - w / 2, y - h, w, h)
    scribus.setFillColor("Hw_Piatra", p)
    scribus.setLineColor("Hw_Negru", p)
    scribus.setLineWidth(0.3, p)
    scribus.setCornerRadius(int(round(w * 0.4 * MM)), p)   # în puncte, întreg
    scribus.rotateObject(inclinare, p)
    # cruce
    rect(x - 0.6, y - h * 0.8, 1.2, h * 0.5, "Hw_Negru")
    rect(x - w * 0.25, y - h * 0.68, w * 0.5, 1.2, "Hw_Negru")


def dovleac(x, y, d):
    halou(x, y, d * 0.8, "Hw_Foc", inele=4, alfa=0.15)
    for k in (-1, 0, 1):
        elipsa(x + k * d * 0.25, y, d * 0.5, d * 0.8, "Hw_Dovleac")
    rect(x - d * 0.06, y - d * 0.55, d * 0.12, d * 0.18, "Hw_Verde")
    # ochi triunghiulari + gură zimțată, luminoase
    poligon([(x - d * 0.28, y - d * 0.05), (x - d * 0.12, y - d * 0.05), (x - d * 0.2, y - d * 0.22)], "Hw_Foc")
    poligon([(x + d * 0.28, y - d * 0.05), (x + d * 0.12, y - d * 0.05), (x + d * 0.2, y - d * 0.22)], "Hw_Foc")
    gura = []
    n = 7
    for i in range(n + 1):
        gx = x - d * 0.3 + d * 0.6 * i / n
        gura.append((gx, y + d * 0.12 + (d * 0.08 if i % 2 else 0)))
    for i in range(n, -1, -1):
        gx = x - d * 0.3 + d * 0.6 * i / n
        gura.append((gx, y + d * 0.28 - (d * 0.06 if i % 2 else 0)))
    poligon(gura, "Hw_Foc")


def fantoma(x, y, h, alfa):
    w = h * 0.6
    puncte = []
    for i in range(13):                       # cap rotund
        a = math.pi + math.pi * i / 12
        puncte.append((x + w / 2 * math.cos(a), y - h * 0.6 + w / 2 * math.sin(a)))
    n = 6                                     # poală vălurită
    for i in range(n + 1):
        px = x + w / 2 - w * i / n
        puncte.append((px, y + h * 0.4 - (h * 0.1 if i % 2 else 0)))
    halou(x, y - h * 0.2, w, "Hw_FantHalo", inele=3, alfa=0.08)
    poligon(puncte, "Hw_Fantoma", alfa)
    elipsa(x - w * 0.18, y - h * 0.6, w * 0.13, h * 0.12, "Hw_Negru", 0.8)
    elipsa(x + w * 0.18, y - h * 0.6, w * 0.13, h * 0.12, "Hw_Negru", 0.8)
    elipsa(x, y - h * 0.4, w * 0.15, h * 0.16, "Hw_Negru", 0.7)


def liliac(x, y, s, unghi):
    puncte = [(-4, 0), (-3.2, -1.2), (-2.2, -0.3), (-1.2, -1.4), (-0.4, -0.5),
              (0, -1.1), (0.4, -0.5), (1.2, -1.4), (2.2, -0.3), (3.2, -1.2), (4, 0),
              (2.6, 0.6), (1.3, 0.2), (0, 1.2), (-1.3, 0.2), (-2.6, 0.6)]
    b = poligon([(x + px * s, y + py * s) for px, py in puncte], "Hw_Negru")
    scribus.rotateObject(unghi, b)


def ochi_rosii(x, y, dist):
    for k in (-1, 1):
        halou(x + k * dist / 2, y, 0.8, "Hw_Rosu", inele=3, alfa=0.2)
        cerc(x + k * dist / 2, y, 0.8, "Hw_Rosu")


def om(x, y, h, cul, alfa=1.0, brat_sus=True):
    """siluetă simplă: cap, trunchi, brațe, picioare; originea = tălpi"""
    cerc(x, y - h * 0.88, h * 0.16, cul, alfa)
    poligon([(x - h * 0.09, y - h * 0.78), (x + h * 0.09, y - h * 0.78),
             (x + h * 0.08, y - h * 0.4), (x - h * 0.08, y - h * 0.4)], cul, alfa)
    poligon([(x - h * 0.07, y - h * 0.42), (x - h * 0.01, y - h * 0.42),
             (x - h * 0.06, y), (x - h * 0.12, y)], cul, alfa)
    poligon([(x + h * 0.01, y - h * 0.42), (x + h * 0.07, y - h * 0.42),
             (x + h * 0.14, y), (x + h * 0.08, y)], cul, alfa)
    # braț stâng pe lângă corp, braț drept întins spre vârtej
    poligon([(x - h * 0.09, y - h * 0.76), (x - h * 0.05, y - h * 0.76),
             (x - h * 0.13, y - h * 0.45), (x - h * 0.16, y - h * 0.47)], cul, alfa)
    if brat_sus:
        poligon([(x + h * 0.08, y - h * 0.76), (x + h * 0.11, y - h * 0.72),
                 (x + h * 0.36, y - h * 0.92), (x + h * 0.34, y - h * 0.96)], cul, alfa)


def vartej(x, y, raza):
    halou(x, y, raza * 0.5, "Hw_Violet", inele=5, alfa=0.1)
    for k in range(3):
        puncte = []
        t = 0.0
        while t < 5 * 2 * math.pi:
            r = raza * (0.04 + 0.96 * t / (10 * math.pi))
            a = t + k * 2 * math.pi / 3
            puncte += [x + r * math.cos(a), y + r * math.sin(a) * 0.7]
            t += 0.08
        lin = scribus.createPolyLine(puncte)
        scribus.setLineColor("Hw_VioletDeschis" if k else "Hw_Violet", lin)
        scribus.setLineWidth(0.9 if k == 0 else 0.5, lin)
        scribus.setFillColor("None", lin)
    cerc(x, y, raza * 0.12, "White", 0.9)
    halou(x, y, raza * 0.12, "White", inele=3, alfa=0.25)


def suflet_smuls(x0, y0, x1, y1, h):
    """copii tot mai transparente și mai mici ale omului, trase spre vârtej"""
    n = 9
    for k in range(1, n + 1):
        t = k / float(n)
        # traseu curbat (arc) de la om la vârtej
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t - 25 * math.sin(t * math.pi)
        om(x, y, h * (1 - 0.7 * t), "Hw_Suflet", alfa=0.55 * (1 - t) + 0.05, brat_sus=True)
    # „fire” de energie între om și vârtej
    for i in range(12):
        puncte = []
        for k in range(30):
            t = k / 29.0
            x = x0 + (x1 - x0) * t + random.uniform(-2, 2)
            y = y0 - h * 0.6 + (y1 - y0 + h * 0.6) * t - (20 + 6 * i) * math.sin(t * math.pi) + random.uniform(-2, 2)
            puncte += [x, y]
        lin = scribus.createPolyLine(puncte)
        scribus.setLineColor("Hw_VioletDeschis", lin)
        scribus.setLineWidth(0.25, lin)
        scribus.setFillColor("None", lin)
        try:
            scribus.setLineTransparency(0.5, lin)
        except Exception:
            pass


def titlu(text_titlu, y):
    f = font_gros()
    corp = min((W - 30) * MM / (0.62 * len(text_titlu)), 72.0)
    inalt = corp * 1.2 / MM
    for dx, dy, cul in ((1.2, 1.2, "Hw_Negru"), (0, 0, "Hw_Sange")):
        t = scribus.createText(15 + dx, y + dy, W - 30, inalt)
        scribus.setText(text_titlu, t)
        scribus.setFont(f, t)
        scribus.setFontSize(corp, t)
        scribus.setLineSpacing(corp, t)
        scribus.setTextAlignment(scribus.ALIGN_CENTERED, t)
        scribus.setTextColor(cul, t)
    # picături de sânge sub litere
    lat_text = len(text_titlu) * 0.62 * corp / MM
    x0 = W / 2 - lat_text / 2
    for i in range(18):
        x = x0 + random.uniform(0, lat_text)
        lung = random.uniform(3, 14)
        gros = random.uniform(0.8, 1.8)
        rect(x - gros / 2, y + inalt * 0.75, gros, lung, "Hw_Sange")
        cerc(x, y + inalt * 0.75 + lung, gros * 1.6, "Hw_Sange")


# ---------- scena ----------
def main():
    global W, H
    scribus.newDocument((297.0, 420.0), (0, 0, 0, 0), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()

    for n, r, g, b in [("Hw_Negru", 5, 3, 8), ("Hw_Luna", 255, 200, 90),
                       ("Hw_LunaHalo", 255, 160, 60), ("Hw_LunaUmbra", 180, 120, 50),
                       ("Hw_Ceata", 170, 160, 200), ("Hw_Piatra", 90, 90, 105),
                       ("Hw_Dovleac", 240, 110, 20), ("Hw_Foc", 255, 230, 60),
                       ("Hw_Verde", 60, 100, 40), ("Hw_Fantoma", 220, 230, 255),
                       ("Hw_FantHalo", 160, 200, 255), ("Hw_Rosu", 255, 20, 20),
                       ("Hw_Violet", 150, 40, 220), ("Hw_VioletDeschis", 210, 150, 255),
                       ("Hw_Suflet", 180, 210, 255), ("Hw_Sange", 170, 10, 20)]:
        culoare(n, r, g, b)

    scribus.setRedraw(False)
    scribus.progressTotal(10)

    cer();                                              scribus.progressSet(1)
    luna(W * 0.78, H * 0.22, 70);                       scribus.progressSet(2)
    # lilieci în fața lunii
    for i in range(14):
        liliac(W * 0.78 + random.uniform(-90, 60), H * 0.22 + random.uniform(-50, 50),
               random.uniform(0.7, 1.8), random.uniform(-30, 30))
    ceata(H * 0.62, 18, 0.07);                          scribus.progressSet(3)
    # dealuri și copaci morți
    deal(H * 0.70)
    for x in (W * 0.08, W * 0.22, W * 0.90):
        copac_mort(x, H * 0.70, random.uniform(45, 60))
    scribus.progressSet(4)
    # cimitir
    for i in range(9):
        x = W * 0.05 + i * W * 0.045 + random.uniform(-4, 4)
        piatra_funerara(x, H * 0.72 + random.uniform(0, 4), random.uniform(9, 13),
                        random.uniform(14, 20), random.uniform(-14, 14))
    piatra_funerara(W * 0.93, H * 0.74, 12, 18, 10)
    scribus.progressSet(5)
    ceata(H * 0.74, 14, 0.12)
    # dovleci
    for x, d in ((W * 0.15, 22), (W * 0.30, 16), (W * 0.88, 20)):
        dovleac(x, H * 0.80, d)
    scribus.progressSet(6)
    # vârtejul lumii umbrelor și omul
    vx, vy = W * 0.62, H * 0.42
    vartej(vx, vy, 75)
    ox, oy = W * 0.40, H * 0.82
    suflet_smuls(ox, oy, vx, vy, 55)
    om(ox, oy, 55, "Hw_Negru")
    # umbra lungă a omului, spre spectator
    poligon([(ox - 4, oy), (ox + 4, oy), (ox + 40, oy + 22), (ox + 20, oy + 22)], "Hw_Negru", 0.6)
    scribus.progressSet(7)
    # fantome
    for x, y, h, a in ((W * 0.12, H * 0.45, 40, 0.45), (W * 0.50, H * 0.20, 28, 0.35),
                       (W * 0.95, H * 0.55, 34, 0.5)):
        fantoma(x, y, h, a)
    scribus.progressSet(8)
    # ochi roșii în întuneric
    for i in range(8):
        ochi_rosii(random.uniform(10, W - 10), random.uniform(H * 0.66, H * 0.78), random.uniform(3, 5))
    ceata(H * 0.90, 24, 0.15)
    scribus.progressSet(9)
    titlu("NOAPTEA UMBRELOR", 12)
    scribus.progressSet(10)

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Noaptea umbrelor", "Scena e gata. Rulează din nou pentru altă noapte…",
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
