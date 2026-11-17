# -*- coding: utf-8 -*-
"""
16 – MACHETĂ DE REVISTĂ (copertă + 3 pagini interioare)
Generează automat o revistă model:
  pag. 1 – copertă: cadru mare pentru foto, titlul revistei (masthead), 4 titluri de
           articole („cover lines”), cod de bare, dată/preț;
  pag. 2 – cuprins („sumar”) cu numere mari de pagină;
  pag. 3 – articol: supratitlu, titlu, autor, text pe 3 coloane cu literă inițială
           (drop cap), citat scos în evidență, foto cu legendă;
  pag. 4 – pagină de imagini (grilă modulară 3 x 4) cu titluri.
Toate paginile au antet/folio (nume revistă + număr pagină) și margini corecte.

Rulare: Script > Execute Script... > 16_revista.py
Cere: numele revistei și tema numărului.
"""
try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

LOREM = ("Tehnoredactarea este arta de a așeza textul și imaginile în pagină astfel încât "
         "cititorul să înțeleagă mesajul fără efort. Grila de coloane, ierarhia titlurilor și "
         "spațiul alb sunt instrumentele de bază ale machetatorului. ",
         "O pagină bună se citește de la stânga la dreapta și de sus în jos, urmând un traseu "
         "vizual pe care designerul l-a construit cu ajutorul contrastelor: mare–mic, gros–subțire, "
         "colorat–neutru. Litera inițială ornamentală atrage ochiul la începutul articolului. ",
         "Corpul de literă pentru text curent este de obicei între 9 și 11 puncte, cu interlinie "
         "cu 20 la sută mai mare. Coloanele înguste cer un corp mai mic, coloanele late unul mai "
         "mare. Nu se lasă niciodată o linie singură la începutul sau la sfârșitul coloanei. ",
         "Imaginile se așază pe grila modulară, aliniate la coloane, iar legendele se pun sub "
         "sau lângă ele, cu un corp mai mic și adesea cu caractere cursive. Un citat scos în "
         "evidență rupe monotonia coloanelor și oferă un al doilea punct de intrare în text. ")
MM = 72.0 / 25.4


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
    scribus.setLineSpacing(interlinie or corp * 1.2, t)
    scribus.setTextColor(cul, t)
    scribus.setTextAlignment(al, t)
    return t


def rect(x, y, w, h, cul, alfa=1.0):
    r = scribus.createRect(x, y, w, h)
    scribus.setFillColor(cul, r)
    scribus.setLineColor("None", r)
    if alfa < 1:
        scribus.setFillTransparency(alfa, r)
    return r


def cadru_foto(x, y, w, h, eticheta, f):
    """cadru de imagine gol + fundal gri + eticheta „FOTO” – se înlocuiește cu poza reală"""
    rect(x, y, w, h, "Rev_Gri")
    text(x, y + h / 2 - 5, w, 10, eticheta, f, 9, "Rev_GriText", scribus.ALIGN_CENTERED)
    img = scribus.createImage(x, y, w, h)
    scribus.setLineColor("None", img)
    return img


def folio(nume, pag, W, H, m, f):
    """antet și număr de pagină"""
    linie = scribus.createLine(m, H - m + 3, W - m, H - m + 3)
    scribus.setLineColor("Rev_Accent", linie)
    scribus.setLineWidth(0.5, linie)
    if pag % 2 == 0:
        text(m, H - m + 4, 60, 6, "%d   |   %s" % (pag, nume.upper()), f, 7, "Rev_GriText")
    else:
        text(W - m - 60, H - m + 4, 60, 6, "%s   |   %d" % (nume.upper(), pag), f, 7, "Rev_GriText", scribus.ALIGN_RIGHT)


def main():
    nume = scribus.valueDialog("Revistă", "Numele revistei:", "MOISIL MAG") or "MOISIL MAG"
    tema = scribus.valueDialog("Revistă", "Tema numărului:", "Grafica digitală în școală") or "Tema numărului"

    m = 15.0
    scribus.newDocument((210.0, 297.0), (m, m, m, m), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 4)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()
    lat = W - 2 * m
    culoare("Rev_Accent", 200, 30, 60)
    culoare("Rev_Inchis", 25, 25, 35)
    culoare("Rev_Gri", 225, 225, 228)
    culoare("Rev_GriText", 120, 120, 130)
    culoare("Rev_Galben", 250, 200, 40)
    fb = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    fr = font(["DejaVu Serif", "Liberation Serif", "Times New Roman", "DejaVu Sans"])
    fs = font(["DejaVu Sans", "Liberation Sans", "Arial"])
    fi = font(["DejaVu Serif Italic", "Liberation Serif Italic", "DejaVu Sans Oblique", "DejaVu Serif"])
    scribus.setRedraw(False)

    # ---------- pag. 1: coperta ----------
    scribus.gotoPage(1)
    cadru_foto(0, 0, W, H, "FOTO DE COPERTĂ (plină, cu bleed)", fs)
    rect(0, 0, W, 62, "Rev_Inchis", 0.55)                       # bandă transparentă sus
    text(m, 10, lat, 30, nume, fb, 64, "White", scribus.ALIGN_LEFT, 64)
    text(m, 42, lat, 8, "Nr. 1  •  octombrie 2026  •  %s" % tema, fs, 10, "Rev_Galben")
    # cover lines (titluri de articole) în stânga jos
    rect(0, H * 0.55, W * 0.55, H * 0.45, "Rev_Inchis", 0.6)
    cl = [("INTERVIU", "Cum ajungi grafician la 20 de ani"), ("ATELIER", "Scribus, InDesign-ul liber"),
          ("TIPAR", "CMYK sau RGB? Răspunsul scurt"), ("CONCURS", "Afișul lunii, votat de voi")]
    y = H * 0.57
    for supra, titlu in cl:
        text(m, y, 8, 5, "", fs, 6)
        rect(m, y + 1, 3, 8, "Rev_Accent")
        text(m + 6, y, W * 0.5, 5, supra, fb, 8, "Rev_Galben")
        text(m + 6, y + 5, W * 0.55 - m - 10, 13, titlu, fb, 13, "White", scribus.ALIGN_LEFT, 15)
        y += 24
    # cod de bare (simulat) + preț
    bx = W - m - 34
    rect(bx, H - m - 14, 34, 14, "White")
    import random
    xx = bx + 2
    while xx < bx + 32:
        g = random.choice((0.3, 0.5, 0.8, 1.0))
        rect(xx, H - m - 12, g, 10, "Black")
        xx += g + random.choice((0.4, 0.7, 1.0))
    text(bx, H - m - 2.5, 34, 3, "ISSN 1234-5678   PREȚ 10 LEI", fs, 4, "Black", scribus.ALIGN_CENTERED)

    # ---------- pag. 2: sumar ----------
    scribus.gotoPage(2)
    text(m, m, lat, 20, "SUMAR", fb, 36, "Rev_Inchis")
    rect(m, m + 18, 30, 1.5, "Rev_Accent")
    y = m + 30
    sumar = [(4, "Editorial", "De ce învățăm machetare"), (6, "Interviu", "Cum ajungi grafician la 20 de ani"),
             (10, "Atelier", "Scribus, InDesign-ul liber"), (14, "Tipar", "CMYK sau RGB? Răspunsul scurt"),
             (18, "Galerie", "Afișele lunii"), (22, "Concurs", "Votează afișul preferat")]
    for pag, rub, tit in sumar:
        text(m, y, 22, 14, "%02d" % pag, fb, 30, "Rev_Accent")
        text(m + 26, y + 1, lat - 26, 5, rub.upper(), fb, 8, "Rev_GriText")
        text(m + 26, y + 6, lat - 26, 8, tit, fr, 14, "Rev_Inchis")
        l = scribus.createLine(m, y + 17, W - m, y + 17)
        scribus.setLineColor("Rev_Gri", l)
        scribus.setLineWidth(0.3, l)
        y += 22
    cadru_foto(m, y + 4, lat, H - m - y - 4, "FOTO", fs)
    folio(nume, 2, W, H, m, fs)

    # ---------- pag. 3: articol pe 3 coloane ----------
    scribus.gotoPage(3)
    text(m, m, lat, 5, "ATELIER", fb, 9, "Rev_Accent")
    text(m, m + 5, lat, 22, "Scribus, InDesign-ul liber", fb, 30, "Rev_Inchis", scribus.ALIGN_LEFT, 31)
    text(m, m + 27, lat, 5, "de Prof. Sergiu Podoreanu  •  foto: elevii clasei a XII-a", fi, 9, "Rev_GriText")
    rect(m, m + 34, lat, 0.6, "Rev_Inchis")
    ytext = m + 38
    inalt = H - m - ytext
    corp = text(m, ytext, lat, inalt, "".join(LOREM * 3), fr, 9.5, "Black", scribus.ALIGN_LEFT, 12)
    try:
        scribus.setColumns(3, corp)
        scribus.setColumnGap(5, corp)
    except Exception:
        pass
    # literă inițială (drop cap) prin stil de paragraf, dacă versiunea permite
    try:
        scribus.createParagraphStyle("Rev_Articol", linespacingmode=1, linespacing=12,
                                     alignment=3, hasdropcap=1, dropcaplines=3)
        scribus.setStyle("Rev_Articol", corp)
        scribus.setFont(fr, corp)
        scribus.setFontSize(9.5, corp)
    except Exception:
        pass
    # citat scos în evidență (peste coloana din mijloc) – textul curge în jur
    cw = (lat - 10) / 3.0
    qx, qy = m + cw + 5, ytext + 55
    citat = text(qx - 2, qy, cw + 4, 40, "„O pagină bună se citește fără efort, urmând traseul construit de designer.”",
                 fi, 14, "Rev_Accent", scribus.ALIGN_CENTERED, 17)
    rect(qx - 2, qy - 2, cw + 4, 1, "Rev_Accent")
    rect(qx - 2, qy + 40, cw + 4, 1, "Rev_Accent")
    try:
        scribus.setTextFlowMode(citat, 1)       # textul din coloane curge în jurul citatului
    except Exception:
        pass
    # foto în coloana din dreapta, jos
    fx, fy = m + 2 * (cw + 5), H - m - 60
    cadru_foto(fx, fy, cw, 45, "FOTO", fs)
    leg = text(fx, fy + 46, cw, 12, "Fig. 1 – Elevii lucrând în Scribus la laboratorul de informatică.", fi, 7, "Rev_GriText")
    try:
        scribus.setTextFlowMode(leg, 1)
        img_frames = [fx]
    except Exception:
        pass
    folio(nume, 3, W, H, m, fs)

    # ---------- pag. 4: grilă modulară de imagini ----------
    scribus.gotoPage(4)
    text(m, m, lat, 5, "GALERIE", fb, 9, "Rev_Accent")
    text(m, m + 5, lat, 14, "Afișele lunii", fb, 24, "Rev_Inchis")
    col, rnd, gol = 3, 4, 4.0
    gy0 = m + 24
    gw = (lat - (col - 1) * gol) / col
    gh = (H - m - gy0 - (rnd - 1) * gol) / rnd
    k = 1
    for r in range(rnd):
        for c in range(col):
            x = m + c * (gw + gol)
            y = gy0 + r * (gh + gol)
            if r == 0 and c == 0:
                continue
            cadru_foto(x, y, gw, gh - 8, "FOTO %d" % k, fs)
            text(x, y + gh - 7, gw, 7, "Afiș nr. %d – autor elev" % k, fs, 7, "Rev_GriText")
            k += 1
    # primul modul: casetă colorată cu text
    rect(m, gy0, gw, gh - 8, "Rev_Accent")
    text(m + 3, gy0 + 3, gw - 6, gh - 14, "12 afișe realizate de elevi în Inkscape și Scribus. Votează-l pe cel preferat la pagina 22.",
         fb, 9, "White", scribus.ALIGN_LEFT, 12)
    folio(nume, 4, W, H, m, fs)

    scribus.gotoPage(1)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Revistă", "Macheta „%s” – 4 pagini. Înlocuiește cadrele FOTO (clic dreapta > Get Image)."
                       % nume, scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
