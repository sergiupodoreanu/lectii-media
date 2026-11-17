# -*- coding: utf-8 -*-
"""
17 – MACHETĂ DE ZIAR (prima pagină, format A3)
Generează prima pagină a unui ziar model:
  - frontispiciu (numele ziarului) cu linia de dată, ediție, preț;
  - grilă de 5 coloane cu spațiu de 4 mm;
  - articolul principal pe 3 coloane cu titlu mare, subtitlu, foto și legendă;
  - două articole secundare pe 2 coloane, cu text înlănțuit între coloane;
  - „scurt din țară” (casetă cu bulinele), previziunea vremii, index.
Textul din coloane este înlănțuit (linkTextFrames) – când editezi, curge singur.

Rulare: Script > Execute Script... > 17_ziar.py
"""
import datetime

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

LOREM = ("Consiliul local a aprobat ieri, cu unanimitate de voturi, proiectul de modernizare a "
         "laboratoarelor din liceele tehnologice. Investiția, estimată la 4,2 milioane de lei, "
         "vizează echipamente pentru electronică, automatizări și grafică digitală. ",
         "Potrivit directorului, lucrările vor începe în vacanța de iarnă și se vor încheia "
         "până la sfârșitul anului școlar. „Elevii vor lucra pe aceleași echipamente pe care le "
         "vor găsi în fabrici”, a declarat acesta pentru ziarul nostru. ",
         "Reprezentanții agenților economici parteneri au salutat decizia și au anunțat că vor "
         "oferi locuri de practică suplimentare începând cu semestrul al doilea. Cererea de "
         "tehnicieni calificați a crescut cu 30 la sută față de anul trecut. ",
         "Părinții prezenți la ședință au ridicat problema transportului elevilor din comunele "
         "învecinate. Primăria a promis o analiză a traseelor în următoarele două săptămâni. ")


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


def text(x, y, w, h, s, f, corp, cul="Black", al=scribus.ALIGN_LEFT, interlinie=None):
    t = scribus.createText(x, y, w, h)
    scribus.setText(s, t)
    scribus.setFont(f, t)
    scribus.setFontSize(corp, t)
    scribus.setLineSpacing(interlinie or corp * 1.15, t)
    scribus.setTextColor(cul, t)
    scribus.setTextAlignment(al, t)
    return t


def rect(x, y, w, h, cul):
    r = scribus.createRect(x, y, w, h)
    scribus.setFillColor(cul, r)
    scribus.setLineColor("None", r)
    return r


def linie(x1, y1, x2, y2, cul="Black", g=0.3):
    l = scribus.createLine(x1, y1, x2, y2)
    scribus.setLineColor(cul, l)
    scribus.setLineWidth(g, l)
    return l


def foto(x, y, w, h, f):
    rect(x, y, w, h, "Z_Gri")
    text(x, y + h / 2 - 4, w, 8, "FOTO", f, 9, "Z_GriText", scribus.ALIGN_CENTERED)
    img = scribus.createImage(x, y, w, h)
    scribus.setLineColor("Black", img)
    scribus.setLineWidth(0.3, img)


def coloane_inlantuite(x, y, w, h, n, gol, s, f, corp):
    """n cadre de text alăturate, înlănțuite: textul curge din unul în următorul"""
    cw = (w - (n - 1) * gol) / n
    cadre = []
    for i in range(n):
        c = scribus.createText(x + i * (cw + gol), y, cw, h)
        cadre.append(c)
    scribus.setText(s, cadre[0])
    scribus.setFont(f, cadre[0])
    scribus.setFontSize(corp, cadre[0])
    scribus.setLineSpacing(corp * 1.18, cadre[0])
    scribus.setTextAlignment(scribus.ALIGN_BLOCK, cadre[0])
    for i in range(n - 1):
        try:
            scribus.linkTextFrames(cadre[i], cadre[i + 1])
        except Exception:
            pass
    return cadre


def main():
    nume = scribus.valueDialog("Ziar", "Numele ziarului:", "GAZETA MOISIL") or "GAZETA MOISIL"
    m = 12.0
    scribus.newDocument((297.0, 420.0), (m, m, m, m), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()
    lat = W - 2 * m
    gol = 4.0
    cw = (lat - 4 * gol) / 5.0             # lățimea unei coloane
    culoare("Z_Gri", 225, 225, 225)
    culoare("Z_GriText", 110, 110, 110)
    culoare("Z_Rosu", 190, 20, 30)
    culoare("Z_Albastru", 20, 50, 110)
    culoare("Z_Caseta", 240, 236, 220)
    fb = font(["DejaVu Serif Bold", "Liberation Serif Bold", "Times New Roman Bold", "DejaVu Sans Bold"])
    fr = font(["DejaVu Serif", "Liberation Serif", "Times New Roman"])
    fs = font(["DejaVu Sans", "Liberation Sans", "Arial"])
    fsb = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    fi = font(["DejaVu Serif Italic", "Liberation Serif Italic", "DejaVu Serif"])
    try:
        scribus.setVGuides([m + i * (cw + gol) - gol for i in range(1, 5)] +
                           [m + i * (cw + gol) for i in range(1, 5)])
    except Exception:
        pass
    scribus.setRedraw(False)

    # ---------- frontispiciul ----------
    azi = datetime.date.today()
    text(m, m, lat, 5, "%s   •   Anul I, nr. 1   •   www.moisilbuzau.ro" % azi.strftime("%d.%m.%Y"), fs, 8, "Z_GriText")
    text(m, m, lat, 5, "PREȚ 3 LEI   •   16 PAGINI", fs, 8, "Z_GriText", scribus.ALIGN_RIGHT)
    linie(m, m + 6, W - m, m + 6, "Black", 0.4)
    text(m, m + 7, lat, 34, nume, fb, 76, "Black", scribus.ALIGN_CENTERED, 76)
    linie(m, m + 41, W - m, m + 41, "Black", 1.2)
    linie(m, m + 42.5, W - m, m + 42.5, "Black", 0.3)
    # bandă „în acest număr”
    yb = m + 45
    rect(m, yb, lat, 14, "Z_Caseta")
    for i, (rub, tit) in enumerate((("SPORT", "Echipa liceului, campioană județeană"),
                                    ("CULTURĂ", "Expoziție de afișe în holul școlii"),
                                    ("TEHNIC", "Laborator nou de automatizări"))):
        x = m + i * lat / 3
        text(x + 3, yb + 2, lat / 3 - 6, 4, rub + "  •  pag. %d" % (5 + 3 * i), fsb, 7, "Z_Rosu")
        text(x + 3, yb + 6, lat / 3 - 6, 8, tit, fr, 11, "Black")
        if i:
            linie(x, yb + 2, x, yb + 12, "Z_GriText", 0.2)

    # ---------- articolul principal (coloanele 1–3) ----------
    y0 = yb + 20
    w3 = 3 * cw + 2 * gol
    text(m, y0, w3, 5, "ÎNVĂȚĂMÂNT", fsb, 9, "Z_Rosu")
    text(m, y0 + 5, w3, 34, "Laboratoare noi pentru liceele tehnologice din județ", fb, 27, "Black", scribus.ALIGN_LEFT, 29)
    text(m, y0 + 40, w3, 12, "Investiție de 4,2 milioane de lei, aprobată în unanimitate; lucrările încep în vacanța de iarnă",
         fi, 13, "Z_GriText", scribus.ALIGN_LEFT, 15)
    foto(m, y0 + 55, w3, 95, fs)
    text(m, y0 + 151, w3, 6, "Laboratorul de electronică va fi complet reechipat până în vară.   Foto: arhiva liceului", fi, 8, "Z_GriText")
    text(m, y0 + 160, w3, 5, "de REPORTER LOCAL", fsb, 8, "Black")
    ya = y0 + 166
    coloane_inlantuite(m, ya, w3, H - m - ya - 4, 3, gol, "".join(LOREM * 3), fr, 9.5)

    # ---------- articole secundare (coloanele 4–5) ----------
    x2 = m + 3 * (cw + gol)
    w2 = 2 * cw + gol
    linie(x2 - gol / 2, y0, x2 - gol / 2, H - m, "Black", 0.2)
    text(x2, y0, w2, 5, "COMUNITATE", fsb, 9, "Z_Albastru")
    text(x2, y0 + 5, w2, 22, "Practică la agenții economici: 120 de locuri noi", fb, 17, "Black", scribus.ALIGN_LEFT, 19)
    ya2 = y0 + 30
    coloane_inlantuite(x2, ya2, w2, 70, 2, gol, "".join(LOREM[2:] * 2), fr, 9)
    linie(x2, ya2 + 74, W - m, ya2 + 74, "Black", 0.3)

    y3 = ya2 + 78
    foto(x2, y3, w2, 55, fs)
    text(x2, y3 + 58, w2, 5, "SPORT", fsb, 9, "Z_Rosu")
    text(x2, y3 + 63, w2, 18, "Echipa liceului, campioană județeană la fotbal", fb, 18, "Black", scribus.ALIGN_LEFT, 20)
    coloane_inlantuite(x2, y3 + 84, w2, 60, 2, gol, "".join(LOREM[1:3]) + LOREM[1], fr, 9)

    # ---------- casetă „pe scurt” + vreme ----------
    yc = y3 + 150
    rect(x2, yc, w2, H - m - yc - 4, "Z_Caseta")
    text(x2 + 3, yc + 2, w2 - 6, 6, "PE SCURT", fsb, 10, "Z_Albastru")
    linie(x2 + 3, yc + 9, W - m - 3, yc + 9, "Z_Albastru", 0.4)
    scurt = ["Concurs de afișe: înscrieri până pe 15 octombrie.",
             "Olimpiada de informatică, etapa pe școală, sâmbătă.",
             "Bursele profesionale se plătesc pe 20 ale lunii.",
             "Cerc de robotică, miercuri, ora 15, sala 12."]
    yy = yc + 12
    for s in scurt:
        rect(x2 + 3, yy + 1.5, 1.8, 1.8, "Z_Rosu")
        text(x2 + 7, yy, w2 - 10, 9, s, fr, 8.5, "Black", scribus.ALIGN_LEFT, 10)
        yy += 10
    text(x2 + 3, yy + 2, w2 - 6, 5, "VREMEA  •  Buzău", fsb, 8, "Z_GriText")
    text(x2 + 3, yy + 7, w2 - 6, 6, "Azi 18°  |  Mâine 15°  |  Vineri 12°, ploaie", fs, 8, "Black")

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Ziar", "Prima pagină a ziarului „%s” e gata (A3, 5 coloane)." % nume, scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
