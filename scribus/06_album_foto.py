# -*- coding: utf-8 -*-
"""
06 – ALBUM FOTO AUTOMAT DIN FOLDER
Alegi un folder cu poze (jpg/png/tif); scriptul face:
  - o copertă cu titlul și numărul de fotografii,
  - pagini A4 landscape cu grilă de N x M poze,
  - fiecare poză în „ramă” albă cu umbră și legendă (numele fișierului).
Pozele sunt scalate proporțional în cadru.

Rulare: Script > Execute Script... > 06_album_foto.py
Cere: folderul, titlul albumului, numărul de coloane și de rânduri.
"""
import os

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

EXT = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp")


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


def lista_poze(folder):
    return sorted(os.path.join(folder, f) for f in os.listdir(folder)
                  if f.lower().endswith(EXT))


def poza(cale, x, y, w, h, f_reg):
    """Ramă albă + umbră + imagine + legendă în dreptunghiul (x, y, w, h)."""
    marg = 3.0            # marginea ramei
    leg = 7.0             # spațiu pentru legendă
    # umbra (dreptunghi gri, deplasat)
    umbra = scribus.createRect(x + 1.5, y + 1.5, w, h)
    scribus.setFillColor("Album_Umbra", umbra)
    scribus.setLineColor("None", umbra)
    scribus.setFillTransparency(0.5, umbra)
    # rama
    rama = scribus.createRect(x, y, w, h)
    scribus.setFillColor("White", rama)
    scribus.setLineColor("None", rama)
    # imaginea
    img = scribus.createImage(x + marg, y + marg, w - 2 * marg, h - 2 * marg - leg)
    scribus.loadImage(cale, img)
    scribus.setScaleImageToFrame(True, True, img)     # scalare proporțională
    # legenda
    nume = os.path.splitext(os.path.basename(cale))[0]
    text(x + marg, y + h - leg - 1, w - 2 * marg, leg, nume, f_reg, 8,
         "Album_Text", scribus.ALIGN_CENTERED)


def main():
    folder = scribus.fileDialog("Alege folderul cu fotografii", "", "", False, False, True)
    if not folder:
        return
    poze = lista_poze(folder)
    if not poze:
        scribus.messageBox("Album", "Nu am găsit imagini (jpg/png/tif) în folder.",
                           scribus.ICON_WARNING)
        return

    titlu = scribus.valueDialog("Album", "Titlul albumului:", os.path.basename(folder) or "Album foto")
    col = max(1, int(scribus.valueDialog("Album", "Coloane pe pagină:", "3") or 3))
    rnd = max(1, int(scribus.valueDialog("Album", "Rânduri pe pagină:", "2") or 2))

    scribus.newDocument((210.0, 297.0), (12, 12, 12, 12), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()

    culoare("Album_Fundal", 235, 232, 225)
    culoare("Album_Coperta", 35, 45, 70)
    culoare("Album_Umbra", 60, 60, 60)
    culoare("Album_Text", 60, 60, 60)
    culoare("Album_Accent", 200, 120, 40)
    f_bold = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    f_reg = font(["DejaVu Sans", "Liberation Sans", "Arial"])

    scribus.setRedraw(False)
    scribus.progressTotal(len(poze))

    # ---- coperta ----
    cop = scribus.createRect(0, 0, w, h)
    scribus.setFillColor("Album_Coperta", cop)
    scribus.setLineColor("None", cop)
    bara = scribus.createRect(0, h * 0.62, w, 3)
    scribus.setFillColor("Album_Accent", bara)
    scribus.setLineColor("None", bara)
    text(20, h * 0.35, w - 40, 30, titlu, f_bold, 44, "White", scribus.ALIGN_LEFT)
    text(20, h * 0.66, w - 40, 12, "%d fotografii" % len(poze), f_reg, 16, "White")
    # prima poză ca vinietă pe copertă
    vin_w = w * 0.28
    vin_h = vin_w * 0.75
    poza(poze[0], w - vin_w - 20, h - vin_h - 20, vin_w, vin_h, f_reg)

    # ---- paginile cu poze ----
    marg = 12.0
    titlu_h = 12.0
    gol = 8.0                                # spațiu între poze
    cw = (w - 2 * marg - (col - 1) * gol) / col
    ch = (h - 2 * marg - titlu_h - (rnd - 1) * gol) / rnd
    pe_pagina = col * rnd
    pagina = 1
    for i, cale in enumerate(poze):
        if i % pe_pagina == 0:
            scribus.newPage(-1)
            pagina += 1
            scribus.gotoPage(pagina)
            fnd = scribus.createRect(0, 0, w, h)
            scribus.setFillColor("Album_Fundal", fnd)
            scribus.setLineColor("None", fnd)
            text(marg, marg - 2, w - 2 * marg, titlu_h, titlu, f_bold, 14, "Album_Coperta")
            text(marg, marg - 2, w - 2 * marg, titlu_h, "pag. %d" % (pagina - 1),
                 f_reg, 10, "Album_Text", scribus.ALIGN_RIGHT)
        k = i % pe_pagina
        x = marg + (k % col) * (cw + gol)
        y = marg + titlu_h + (k // col) * (ch + gol)
        poza(cale, x, y, cw, ch, f_reg)
        scribus.progressSet(i + 1)

    scribus.gotoPage(1)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Album", "%d fotografii pe %d pagini (+ copertă)."
                       % (len(poze), pagina - 1), scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
