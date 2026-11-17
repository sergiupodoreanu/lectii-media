# -*- coding: utf-8 -*-
"""
04 – CĂRȚI DE VIZITĂ DIN CSV (mail-merge)
Citește un fișier CSV cu coloanele: nume,functie,telefon,email
și așază 10 cărți de vizită (85 x 55 mm) pe fiecare pagină A4,
cu bandă colorată, colțuri rotunjite și linii de tăiere.
Dacă nu alegi un fișier, folosește date demonstrative (clasa).

Format CSV (prima linie = antet):
nume,functie,telefon,email
Popescu Ana,Grafician,0722 000 111,ana@exemplu.ro

Rulare: Script > Execute Script... > 04_carti_vizita_csv.py
"""
import csv

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

CARD_W, CARD_H = 85.0, 55.0
COL, RND = 2, 5

DEMO = [
    {"nume": "Popescu Ana", "functie": "Grafician", "telefon": "0722 000 111", "email": "ana@exemplu.ro"},
    {"nume": "Ionescu Mihai", "functie": "Tehnoredactor", "telefon": "0733 222 333", "email": "mihai@exemplu.ro"},
    {"nume": "Dumitru Elena", "functie": "Fotograf", "telefon": "0744 444 555", "email": "elena@exemplu.ro"},
    {"nume": "Stan Andrei", "functie": "Web designer", "telefon": "0755 666 777", "email": "andrei@exemplu.ro"},
    {"nume": "Radu Ioana", "functie": "Ilustrator", "telefon": "0766 888 999", "email": "ioana@exemplu.ro"},
    {"nume": "Marin Vlad", "functie": "Editor video", "telefon": "0777 111 222", "email": "vlad@exemplu.ro"},
    {"nume": "Gheorghe Maria", "functie": "DTP operator", "telefon": "0788 333 444", "email": "maria@exemplu.ro"},
    {"nume": "Constantin Dan", "functie": "Tipograf", "telefon": "0799 555 666", "email": "dan@exemplu.ro"},
    {"nume": "Nistor Alina", "functie": "Art director", "telefon": "0721 777 888", "email": "alina@exemplu.ro"},
    {"nume": "Toma Cristian", "functie": "Motion designer", "telefon": "0732 999 000", "email": "cristi@exemplu.ro"},
    {"nume": "Barbu Diana", "functie": "Copywriter", "telefon": "0743 121 212", "email": "diana@exemplu.ro"},
    {"nume": "Lupu Robert", "functie": "Programator", "telefon": "0754 343 434", "email": "robert@exemplu.ro"},
]


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def font(pref_list):
    """Caută primul font instalat din listă. Scribus numește fonturile cu tot cu
    stil („Arial Regular”, „DejaVu Sans Book”), deci încercăm și aceste variante;
    apoi fonturi obișnuite din Windows, care au diacritice românești."""
    fonturi = scribus.getFontNames()
    for p in pref_list:
        for cand in (p, p + " Regular", p + " Book", p + " Roman"):
            if cand in fonturi:
                return cand
    stil = pref_list[0] if pref_list else ""
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


def text(x, y, w, h, s, f, corp, cul, align=scribus.ALIGN_LEFT):
    t = scribus.createText(x, y, w, h)
    scribus.setText(s, t)
    scribus.setFont(f, t)
    scribus.setFontSize(corp, t)
    scribus.setTextColor(cul, t)
    scribus.setTextAlignment(align, t)
    return t


def citeste_csv():
    cale = scribus.fileDialog("Alege fișierul CSV (Anulează = date demo)", "*.csv")
    if not cale:
        return DEMO
    with open(cale, "r", encoding="utf-8-sig", newline="") as f:
        return [{k.strip().lower(): (v or "").strip() for k, v in r.items()}
                for r in csv.DictReader(f)]


def carte(x, y, d, f_bold, f_reg):
    fundal = scribus.createRect(x, y, CARD_W, CARD_H)
    scribus.setFillColor("White", fundal)
    scribus.setLineColor("CV_Taiere", fundal)
    scribus.setLineWidth(0.2, fundal)
    scribus.setCornerRadius(3, fundal)

    banda = scribus.createRect(x, y, CARD_W, 14)
    scribus.setFillColor("CV_Banda", banda)
    scribus.setLineColor("None", banda)

    text(x + 5, y + 3, CARD_W - 10, 9, d.get("nume", ""), f_bold, 13, "White")
    text(x + 5, y + 17, CARD_W - 10, 7, d.get("functie", ""), f_reg, 9, "CV_Accent")
    text(x + 5, y + 33, CARD_W - 10, 6, "Tel: " + d.get("telefon", ""), f_reg, 8, "CV_Text")
    text(x + 5, y + 40, CARD_W - 10, 6, d.get("email", ""), f_reg, 8, "CV_Text")
    text(x + 5, y + 47, CARD_W - 10, 6, "Liceul Tehnologic Grigore C. Moisil Buzau",
         f_reg, 6, "CV_Accent")

    # element grafic: cerc de accent în colțul din dreapta-jos
    cerc = scribus.createEllipse(x + CARD_W - 16, y + CARD_H - 16, 10, 10)
    scribus.setFillColor("CV_Accent", cerc)
    scribus.setLineColor("None", cerc)
    scribus.setFillTransparency(0.6, cerc)


def main():
    date = citeste_csv()
    if not date:
        scribus.messageBox("CSV", "Fișierul nu conține date.", scribus.ICON_WARNING)
        return

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    x0 = (w - COL * CARD_W) / 2.0
    y0 = (h - RND * CARD_H) / 2.0

    culoare("CV_Banda", 25, 55, 110)
    culoare("CV_Accent", 0, 150, 170)
    culoare("CV_Text", 50, 50, 50)
    culoare("CV_Taiere", 180, 180, 180)
    f_bold = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    f_reg = font(["DejaVu Sans", "Liberation Sans", "Arial"])

    scribus.setRedraw(False)
    scribus.progressTotal(len(date))
    pe_pagina = COL * RND
    for i, d in enumerate(date):
        if i > 0 and i % pe_pagina == 0:
            scribus.newPage(-1)
            scribus.gotoPage(i // pe_pagina + 1)
        k = i % pe_pagina
        x = x0 + (k % COL) * CARD_W
        y = y0 + (k // COL) * CARD_H
        carte(x, y, d, f_bold, f_reg)
        scribus.progressSet(i + 1)

    scribus.gotoPage(1)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Cărți de vizită", "%d cărți de vizită pe %d pagini."
                       % (len(date), (len(date) - 1) // pe_pagina + 1),
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
