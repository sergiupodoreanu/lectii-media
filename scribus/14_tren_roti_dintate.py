# -*- coding: utf-8 -*-
"""
14 – TREN DE ROȚI DINȚATE (angrenaj cilindric cu dinți drepți)
Desenează un lanț de roți dințate care angrenează corect: același modul m,
distanța dintre axe a = m·(z1 + z2)/2, dinții unei roți intră în golurile
celeilalte (fazare pe jumătate de pas). Fiecare roată are efect de grosime
(straturi deplasate), butuc cu pană, cercuri de divizare și etichete
(z, d, raport de transmitere).

Rulare: Script > Execute Script... > 14_tren_roti_dintate.py
Cere: modulul și lista numerelor de dinți (ex. 12,30,18,45).
"""
import math

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

PALETA = [(70, 130, 200), (220, 140, 50), (90, 170, 100), (200, 80, 90), (150, 110, 200), (60, 180, 190)]


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def font(pref):
    """Caută primul font instalat din listă. Scribus numește fonturile cu tot cu
    stil („Arial Regular”, „DejaVu Sans Book”), deci încercăm și aceste variante;
    apoi fonturi obișnuite din Windows, care au diacritice românești."""
    fonturi = scribus.getFontNames()
    for p in pref:
        for cand in (p, p + " Regular", p + " Book", p + " Roman"):
            if cand in fonturi:
                return cand
    stil = pref[0] if pref else ""
    if "Bold" in stil:
        rezerva = ["Arial Bold", "Verdana Bold", "Tahoma Bold", "Segoe UI Bold", "Calibri Bold"]
    elif "Italic" in stil or "Oblique" in stil:
        rezerva = ["Times New Roman Italic", "Arial Italic", "Georgia Italic", "Calibri Italic"]
    else:
        rezerva = ["Arial Regular", "Times New Roman Regular", "Verdana Regular",
                   "Tahoma Regular", "Segoe UI Regular", "Calibri Regular"]
    for cand in rezerva:
        if cand in fonturi:
            return cand
    return fonturi[0]


def text(x, y, w, h, s, f, corp, cul, al=scribus.ALIGN_CENTERED):
    t = scribus.createText(x, y, w, h)
    scribus.setText(s, t)
    scribus.setFont(f, t)
    scribus.setFontSize(corp, t)
    scribus.setTextColor(cul, t)
    scribus.setTextAlignment(al, t)
    return t


def contur_roata(cx, cy, z, m, faza):
    """poligonul unei roți dințate cu dinți trapezoidali (aproximare a evolventei)"""
    rp = m * z / 2.0
    ra, rf = rp + m, rp - 1.25 * m
    pas = 2 * math.pi / z
    pts = []
    # pe un pas: gol (la rf) → flanc → vârf (la ra) → flanc → gol
    profil = [(0.00, rf), (0.18, rf), (0.30, rp), (0.36, ra), (0.64, ra), (0.70, rp), (0.82, rf), (1.00, rf)]
    for i in range(z):
        for f, r in profil[:-1]:
            a = faza + (i + f) * pas
            pts += [cx + r * math.cos(a), cy + r * math.sin(a)]
    return pts


def roata(cx, cy, z, m, faza, cul_baza, f_bold, f_reg, eticheta):
    r, g, b = cul_baza
    culoare("Ang_%s_Umbra" % eticheta, int(r * 0.45), int(g * 0.45), int(b * 0.45))
    culoare("Ang_%s_Fata" % eticheta, r, g, b)
    culoare("Ang_%s_Lumina" % eticheta, min(255, r + 60), min(255, g + 60), min(255, b + 60))
    rp = m * z / 2.0
    # grosimea: 6 straturi deplasate în jos-dreapta, întunecate
    for k in range(6, 0, -1):
        p = scribus.createPolygon(contur_roata(cx + 0.5 * k, cy + 0.6 * k, z, m, faza))
        scribus.setFillColor("Ang_%s_Umbra" % eticheta, p)
        scribus.setLineColor("None", p)
    p = scribus.createPolygon(contur_roata(cx, cy, z, m, faza))
    scribus.setFillColor("Ang_%s_Fata" % eticheta, p)
    scribus.setLineColor("Ang_%s_Umbra" % eticheta, p)
    scribus.setLineWidth(0.3, p)
    # reflex (semilună deschisă) pe partea de sus-stânga
    rr = rp * 0.72
    refl = scribus.createEllipse(cx - rr, cy - rr, 2 * rr, 2 * rr)
    scribus.setFillColor("Ang_%s_Lumina" % eticheta, refl)
    scribus.setLineColor("None", refl)
    scribus.setFillTransparency(0.35, refl)
    # cercul de divizare (linie subțire)
    cd = scribus.createEllipse(cx - rp, cy - rp, 2 * rp, 2 * rp)
    scribus.setFillColor("None", cd)
    scribus.setLineColor("Ang_Linie", cd)
    scribus.setLineWidth(0.25, cd)
    # inel interior, spițe/găuri, butuc și pană
    ri = rp * 0.6
    inel = scribus.createEllipse(cx - ri, cy - ri, 2 * ri, 2 * ri)
    scribus.setFillColor("Ang_%s_Umbra" % eticheta, inel)
    scribus.setLineColor("None", inel)
    scribus.setFillTransparency(0.35, inel)
    if rp > 22:
        for i in range(5):
            a = faza + i * 2 * math.pi / 5
            d = rp * 0.16
            gx, gy = cx + rp * 0.42 * math.cos(a), cy + rp * 0.42 * math.sin(a)
            gaura = scribus.createEllipse(gx - d, gy - d, 2 * d, 2 * d)
            scribus.setFillColor("Ang_Fundal", gaura)
            scribus.setLineColor("Ang_%s_Umbra" % eticheta, gaura)
            scribus.setLineWidth(0.3, gaura)
    rb = max(4.0, rp * 0.18)
    butuc = scribus.createEllipse(cx - rb, cy - rb, 2 * rb, 2 * rb)
    scribus.setFillColor("Ang_Otel", butuc)
    scribus.setLineColor("Ang_%s_Umbra" % eticheta, butuc)
    scribus.setLineWidth(0.3, butuc)
    pana = scribus.createRect(cx - rb * 0.25, cy - rb * 1.15, rb * 0.5, rb * 0.5)
    scribus.setFillColor("Ang_Fundal", pana)
    scribus.setLineColor("Ang_%s_Umbra" % eticheta, pana)
    scribus.setLineWidth(0.3, pana)
    # eticheta se desenează la sfârșit (în main), ca să nu fie acoperită de roata vecină
    return (cx, cy + rp + m + 6, "%s   z = %d\nd = %.0f mm" % (eticheta, z, 2 * rp))


def main():
    m = float(scribus.valueDialog("Tren de roți dințate", "Modulul m (mm):", "2.5") or 2.5)
    lista = scribus.valueDialog("Tren de roți dințate", "Numerele de dinți, separate prin virgulă:", "12,30,18,45")
    zs = [int(v) for v in lista.replace(";", ",").split(",") if v.strip()]
    if len(zs) < 2:
        zs = [12, 30]

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()
    culoare("Ang_Fundal", 240, 238, 232)
    culoare("Ang_Otel", 175, 180, 190)
    culoare("Ang_Linie", 90, 90, 90)
    culoare("Ang_Text", 40, 40, 40)
    culoare("Ang_Accent", 200, 60, 40)
    fnd = scribus.createRect(0, 0, W, H)
    scribus.setFillColor("Ang_Fundal", fnd)
    scribus.setLineColor("None", fnd)
    # caroiaj de desen tehnic
    for x in range(10, int(W), 10):
        l = scribus.createLine(x, 0, x, H)
        scribus.setLineColor("Ang_Otel", l)
        scribus.setLineWidth(0.1, l)
    for y in range(10, int(H), 10):
        l = scribus.createLine(0, y, W, y)
        scribus.setLineColor("Ang_Otel", l)
        scribus.setLineWidth(0.1, l)

    fb = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    fr = font(["DejaVu Sans", "Liberation Sans", "Arial"])

    # așezarea roților: în zig-zag pe orizontală, centrele la distanța a = m(z1+z2)/2
    scribus.setRedraw(False)
    centre = []
    x, y = 0.0, 0.0
    unghi = 0.0
    for i, z in enumerate(zs):
        if i > 0:
            a = m * (zs[i - 1] + z) / 2.0
            unghi = math.radians(-25 if i % 2 else 25)
            x += a * math.cos(unghi)
            y += a * math.sin(unghi)
        centre.append((x, y, unghi))
    # centrare pe pagină
    xs = [c[0] for c in centre]
    ys = [c[1] for c in centre]
    rmax = m * max(zs) / 2.0 + m
    ox = W / 2.0 - (min(xs) + max(xs)) / 2.0
    oy = H / 2.0 - (min(ys) + max(ys)) / 2.0 + 4
    scara = min(1.0, (W - 40) / (max(xs) - min(xs) + 2 * rmax + 1e-6), (H - 60) / (max(ys) - min(ys) + 2 * rmax + 1e-6))
    m_des = m * scara

    faze = []
    etichete = []
    for i, z in enumerate(zs):
        cx = W / 2.0 + (centre[i][0] - (min(xs) + max(xs)) / 2.0) * scara
        cy = H / 2.0 + 4 + (centre[i][1] - (min(ys) + max(ys)) / 2.0) * scara
        if i == 0:
            faza = 0.0
        else:
            # fazare: dintele roții anterioare pe linia centrelor ↔ golul roții curente
            ang = centre[i][2]
            pas_prev = 2 * math.pi / zs[i - 1]
            # unghiul, pe roata anterioară, al primului dinte față de linia centrelor
            dif = (ang - faze[i - 1]) % pas_prev
            # centrul golului roții anterioare e la 0.0 din pas, vârful dintelui la 0.5
            frac_prev = dif / pas_prev                  # 0 = gol pe linia centrelor
            pas_cur = 2 * math.pi / z
            # pe roata curentă, direcția spre roata anterioară = ang + π; acolo trebuie
            # complementul: dacă la vecin e gol (0) aici e dinte (0.5)
            faza = (ang + math.pi) - (0.5 - frac_prev) * pas_cur
        faze.append(faza)
        etichete.append(roata(cx, cy, z, m_des, faza, PALETA[i % len(PALETA)], fb, fr, "R%d" % (i + 1)))
        # axa
        ax = scribus.createLine(cx - 6, cy, cx + 6, cy)
        scribus.setLineColor("Ang_Accent", ax)
        scribus.setLineWidth(0.2, ax)
        ay = scribus.createLine(cx, cy - 6, cx, cy + 6)
        scribus.setLineColor("Ang_Accent", ay)
        scribus.setLineWidth(0.2, ay)

    for ex, ey, et in etichete:
        text(ex - 30, ey, 60, 12, et, fb, 8, "Ang_Text")

    # titlu și calcul
    text(12, 8, W - 24, 12, "TREN DE ROȚI DINȚATE  –  modul m = %.2f mm" % m, fb, 16, "Ang_Text", scribus.ALIGN_LEFT)
    i_total = 1.0
    parti = []
    for k in range(1, len(zs)):
        i_k = zs[k] / float(zs[k - 1])
        i_total *= i_k
        parti.append("i%d = z%d/z%d = %d/%d = %.2f" % (k, k + 1, k, zs[k], zs[k - 1], i_k))
    text(12, H - 22, W - 24, 16, "   |   ".join(parti) + "\nraport total i = %.3f   (turația la ieșire = turația la intrare / i)   |   a = m·(z1+z2)/2 între fiecare pereche"
         % i_total, fr, 8, "Ang_Text", scribus.ALIGN_LEFT)

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Tren de roți", "%d roți, raport total i = %.3f" % (len(zs), i_total), scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
