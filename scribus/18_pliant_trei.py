# -*- coding: utf-8 -*-
"""
18 – PLIANT ÎN TREI (broșură A4 landscape, față + verso)
Generează un pliant tip „trifold”: 2 pagini A4 landscape, fiecare împărțită în
3 panouri de 99 mm cu linii de pliere (ghidaje):
  FAȚĂ  (pag. 1): panoul din interior-stânga | verso-copertă (contact, hartă) | COPERTA
  VERSO (pag. 2): cele 3 panouri interioare: prezentare, oferta/servicii, program
Include bandă colorată, pictograme geometrice, listă cu buline, casetă de contact,
cod QR simulat. Ordinea panourilor respectă plierea „în fereastră” (C-fold).

Rulare: Script > Execute Script... > 18_pliant_trei.py
Cere: titlul și subtitlul.
"""
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
    scribus.setLineSpacing(interlinie or corp * 1.25, t)
    scribus.setTextColor(cul, t)
    scribus.setTextAlignment(al, t)
    return t


def rect(x, y, w, h, cul, alfa=1.0, raza=0):
    r = scribus.createRect(x, y, w, h)
    scribus.setFillColor(cul, r)
    scribus.setLineColor("None", r)
    if alfa < 1:
        scribus.setFillTransparency(alfa, r)
    if raza:
        # Scribus cere raza în puncte, număr întreg (1 mm = 2,835 pt)
        scribus.setCornerRadius(max(1, int(round(raza * 2.835))), r)
    return r


def cerc(x, y, d, cul):
    e = scribus.createEllipse(x - d / 2, y - d / 2, d, d)
    scribus.setFillColor(cul, e)
    scribus.setLineColor("None", e)
    return e


def foto(x, y, w, h, f, eticheta="FOTO"):
    rect(x, y, w, h, "P_Gri")
    text(x, y + h / 2 - 4, w, 8, eticheta, f, 9, "P_GriText", scribus.ALIGN_CENTERED)
    img = scribus.createImage(x, y, w, h)
    scribus.setLineColor("None", img)


def pictograma(x, y, tip):
    """pictograme simple din forme: bec, roată, ecran, semnal"""
    cerc(x, y, 14, "P_Accent")
    if tip == "bec":
        cerc(x, y - 1, 6, "White")
        rect(x - 1.5, y + 2, 3, 3, "White")
    elif tip == "roata":
        for k in range(8):
            import math
            a = math.radians(45 * k)
            rect(x + 4 * math.cos(a) - 1, y + 4 * math.sin(a) - 1, 2, 2, "White")
        cerc(x, y, 5, "White")
        cerc(x, y, 2, "P_Accent")
    elif tip == "ecran":
        rect(x - 4.5, y - 3.5, 9, 6, "White", raza=0.5)
        rect(x - 2, y + 3, 4, 1.2, "White")
    else:  # semnal
        for k, d in enumerate((3, 6, 9)):
            e = scribus.createEllipse(x - d / 2, y - d / 2, d, d)
            scribus.setFillColor("None", e)
            scribus.setLineColor("White", e)
            scribus.setLineWidth(0.8, e)


def cod_qr(x, y, s):
    """simulare QR: grilă 21x21 cu cele 3 pătrate de reper"""
    rect(x, y, s, s, "White")
    n = 21
    c = s / n
    for i in range(n):
        for j in range(n):
            reper = (i < 7 and j < 7) or (i < 7 and j >= n - 7) or (i >= n - 7 and j < 7)
            if reper:
                continue
            if random.random() < 0.45:
                rect(x + j * c, y + i * c, c, c, "Black")
    for (i0, j0) in ((0, 0), (0, n - 7), (n - 7, 0)):
        rect(x + j0 * c, y + i0 * c, 7 * c, 7 * c, "Black")
        rect(x + (j0 + 1) * c, y + (i0 + 1) * c, 5 * c, 5 * c, "White")
        rect(x + (j0 + 2) * c, y + (i0 + 2) * c, 3 * c, 3 * c, "Black")


def main():
    titlu = scribus.valueDialog("Pliant", "Titlul pliantului:", "Producție media") or "Producție media"
    sub = scribus.valueDialog("Pliant", "Subtitlu:", "Liceul Tehnologic „Grigore C. Moisil” Buzău") or ""

    scribus.newDocument((210.0, 297.0), (0, 0, 0, 0), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 2)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()
    P = W / 3.0                     # lățimea unui panou (99 mm)
    m = 8.0                         # marginea interioară a panoului
    culoare("P_Accent", 0, 120, 140)
    culoare("P_Inchis", 20, 40, 55)
    culoare("P_Deschis", 225, 240, 242)
    culoare("P_Gri", 225, 225, 225)
    culoare("P_GriText", 110, 110, 110)
    culoare("P_Galben", 250, 190, 30)
    fb = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    fs = font(["DejaVu Sans", "Liberation Sans", "Arial"])
    fi = font(["DejaVu Sans Oblique", "Liberation Sans Italic", "DejaVu Sans"])
    scribus.setRedraw(False)

    for pag in (1, 2):
        scribus.gotoPage(pag)
        try:
            scribus.setVGuides([P, 2 * P])
        except Exception:
            pass
        rect(0, 0, W, H, "White")
        # linii de pliere (semne subțiri sus/jos, în afara zonei tipărite)
        for x in (P, 2 * P):
            for y in (0, H - 4):
                l = scribus.createLine(x, y, x, y + 4)
                scribus.setLineColor("P_GriText", l)
                scribus.setLineWidth(0.2, l)

    # ================= PAG. 1 (fața exterioară) =================
    scribus.gotoPage(1)
    # --- panoul 3 (dreapta) = COPERTA ---
    x = 2 * P
    rect(x, 0, P, H, "P_Inchis")
    foto(x, 0, P, H * 0.5, fs, "FOTO COPERTĂ")
    rect(x, H * 0.5 - 6, P, 6, "P_Accent")
    text(x + m, H * 0.55, P - 2 * m, 40, titlu, fb, 30, "White", scribus.ALIGN_LEFT, 32)
    text(x + m, H * 0.55 + 42, P - 2 * m, 14, sub, fs, 10, "P_Galben", scribus.ALIGN_LEFT, 12)
    rect(x + m, H - 28, 24, 1, "P_Galben")
    text(x + m, H - 24, P - 2 * m, 14, "Calificare: Tehnician producție media\nDurata: 4 ani  •  Nivel 4", fs, 8, "White")

    # --- panoul 2 (mijloc) = verso-copertă: CONTACT ---
    x = P
    rect(x, 0, P, H, "P_Deschis")
    text(x + m, m, P - 2 * m, 10, "CONTACT", fb, 16, "P_Accent")
    rect(x + m, m + 11, 20, 1, "P_Accent")
    contact = [("Adresă", "Str. Exemplu nr. 1, Buzău"), ("Telefon", "0238 000 000"),
               ("E-mail", "secretariat@moisil.ro"), ("Web", "www.moisilbuzau.ro"),
               ("Program", "luni – vineri, 8:00 – 16:00")]
    y = m + 18
    for k, v in contact:
        text(x + m, y, P - 2 * m, 5, k.upper(), fb, 7, "P_GriText")
        text(x + m, y + 5, P - 2 * m, 7, v, fs, 10, "P_Inchis")
        y += 15
    foto(x + m, y + 4, P - 2 * m, 50, fs, "HARTĂ")
    cod_qr(x + m, H - m - 30, 30)
    text(x + m + 34, H - m - 30, P - 2 * m - 34, 30, "Scanează pentru înscrieri online și galeria lucrărilor elevilor.",
         fi, 8, "P_GriText")

    # --- panoul 1 (stânga) = clapa interioară: DE CE NOI ---
    x = 0
    rect(0, 0, P, 30, "P_Accent")
    text(m, 8, P - 2 * m, 16, "De ce să alegi\nproducția media?", fb, 14, "White", scribus.ALIGN_LEFT, 16)
    argumente = ["Lucrezi în Inkscape, Scribus, GIMP și Blender din primul an",
                 "Practică la tipografii, agenții de publicitate și televiziuni",
                 "Laborator cu 25 de stații grafice și imprimantă A3+",
                 "Portofoliu personal la absolvire",
                 "Concursuri și expoziții în fiecare semestru"]
    y = 40
    for a in argumente:
        cerc(m + 3, y + 4, 4, "P_Galben")
        text(m + 10, y, P - 2 * m - 10, 14, a, fs, 9.5, "P_Inchis", scribus.ALIGN_LEFT, 11.5)
        y += 20
    foto(m, y + 4, P - 2 * m, H - y - 4 - m, fs)

    # ================= PAG. 2 (interiorul) =================
    scribus.gotoPage(2)
    rect(0, 0, W, 22, "P_Inchis")
    text(m, 6, W - 2 * m, 12, titlu.upper() + "   •   CE VEI ÎNVĂȚA", fb, 14, "White")
    # panou 1: prezentare
    x = 0
    text(x + m, 30, P - 2 * m, 12, "Prezentare", fb, 18, "P_Accent")
    text(x + m, 44, P - 2 * m, 60, ("Producția media îmbină grafica, fotografia, textul și video într-un singur "
                                   "flux de lucru: de la idee, la machetă, la tipar sau ecran. Vei învăța să "
                                   "gândești în grile, culori și tipografie, dar și să folosești uneltele "
                                   "profesioniștilor."), fs, 9.5, "P_Inchis", scribus.ALIGN_LEFT, 12)
    foto(x + m, 108, P - 2 * m, 70, fs)
    text(x + m, 180, P - 2 * m, 10, "Atelierul de machetare, anul II", fi, 7.5, "P_GriText")
    # panou 2: module cu pictograme
    x = P
    rect(x, 22, P, H - 22, "P_Deschis")
    text(x + m, 30, P - 2 * m, 12, "Module de studiu", fb, 18, "P_Accent")
    module = [("bec", "Proiectare grafică", "Compoziție, culoare, tipografie, identitate vizuală"),
              ("ecran", "Tehnoredactare", "Machetare de reviste, ziare, cărți, pliante"),
              ("roata", "Procesare imagine", "Retuș foto, vectorizare, pregătire pentru tipar"),
              ("semnal", "Producție video", "Filmare, montaj, grafică animată")]
    y = 48
    for tip, nume, desc in module:
        pictograma(x + m + 7, y + 7, tip)
        text(x + m + 18, y, P - 2 * m - 18, 6, nume, fb, 10.5, "P_Inchis")
        text(x + m + 18, y + 6, P - 2 * m - 18, 14, desc, fs, 8, "P_GriText", scribus.ALIGN_LEFT, 9.5)
        y += 34
    # panou 3: program + casetă
    x = 2 * P
    text(x + m, 30, P - 2 * m, 12, "Program și admitere", fb, 18, "P_Accent")
    rand = [("Anul I", "Bazele graficii, desen, fotografie"), ("Anul II", "Machetare, DTP, tipar"),
            ("Anul III", "Video, animație, web"), ("Anul IV", "Proiect de certificare, practică")]
    y = 46
    for an, ce in rand:
        rect(x + m, y, 20, 9, "P_Accent", raza=1.5)
        text(x + m, y + 1.5, 20, 6, an, fb, 8, "White", scribus.ALIGN_CENTERED)
        text(x + m + 24, y + 1, P - 2 * m - 24, 9, ce, fs, 8.5, "P_Inchis")
        y += 14
    rect(x + m, y + 6, P - 2 * m, 52, "P_Galben", raza=3)
    text(x + m + 5, y + 10, P - 2 * m - 10, 44, ("ÎNSCRIERI\n\nDosarul se depune la secretariat între 1 și 15 iulie. "
                                                 "Probă de aptitudini: desen și compoziție (2 ore)."),
         fb, 9, "P_Inchis", scribus.ALIGN_LEFT, 11.5)
    foto(x + m, y + 64, P - 2 * m, H - y - 64 - m, fs)

    scribus.gotoPage(1)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.messageBox("Pliant", "Pliant în trei, 2 fețe. Tipărește față-verso (întoarcere pe latura scurtă).",
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
