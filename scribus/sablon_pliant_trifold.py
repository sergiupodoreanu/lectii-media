# -*- coding: utf-8 -*-
# Pliant A4 in trei, pliere in C (roll fold), pentru tipar - Scribus 1.6
# Panoul care intra inauntru are 97 mm, celelalte 100 mm.
import scribus

W, H, BLEED, MARG, GUT = 297.0, 210.0, 3.0, 8.0, 5.0   # GUT = margine la pliu
EXT = [97.0, 100.0, 100.0]     # exterior: clapa | spate | fata
INT = [100.0, 100.0, 97.0]     # interior: 1 | 2 | 3 (intra inauntru)

scribus.newDocument((W, H), (MARG, MARG, MARG, MARG), scribus.LANDSCAPE,
                    1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 2)
scribus.setBleeds(BLEED, BLEED, BLEED, BLEED)

scribus.defineColorCMYK("Negru bogat", 153, 102, 102, 255)
scribus.defineColorCMYK("Verde",       204, 0,   255, 51)
scribus.defineColorCMYK("Galben",      0,   38,  255, 0)
scribus.defineColorCMYK("Gri deschis", 0,   0,   0,   20)

fonts = scribus.getFontNames()
def f(*cand):
    return next((x for x in cand if x in fonts), fonts[0])
FB = f("Arial Bold", "Liberation Sans Bold", "DejaVu Sans Bold")
FR = f("Arial Regular", "Liberation Sans Regular", "DejaVu Sans Book")

for L in ("Fundal", "Imagini", "Text", "Ghidaje"):
    scribus.createLayer(L)

def text(x, y, w, h, nume, s, font, size, col, al=scribus.ALIGN_LEFT):
    scribus.createText(x, y, w, h, nume); scribus.setText(s, nume)
    scribus.setFont(font, nume); scribus.setFontSize(size, nume)
    scribus.setTextColor(col, nume); scribus.setTextAlignment(al, nume)
    scribus.setTextDistances(3, 3, 3, 3, nume)

def panouri(latimi):
    x, out = 0.0, []
    for l in latimi:
        out.append((x, l)); x += l
    return out, [out[1][0], out[2][0]]

def pagina(nr, latimi, titluri, sufix):
    scribus.gotoPage(nr)
    p, pliuri = panouri(latimi)
    scribus.setVGuides(pliuri + [pliuri[0] - GUT, pliuri[0] + GUT,
                                 pliuri[1] - GUT, pliuri[1] + GUT])
    scribus.setHGuides([MARG, H - MARG])
    scribus.setActiveLayer("Fundal")
    n = "fundal_" + sufix
    scribus.createRect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, n)
    scribus.setFillColor("Gri deschis", n); scribus.setLineColor("None", n)
    for i, ((x, l), titlu) in enumerate(zip(p, titluri)):
        xi = x + (MARG if i == 0 else GUT)
        xe = x + l - (MARG if i == 2 else GUT)
        scribus.setActiveLayer("Imagini")
        scribus.createImage(xi, MARG, xe - xi, 55, "img_%s_%d" % (sufix, i))
        scribus.setActiveLayer("Text")
        text(xi, MARG + 58, xe - xi, 14, "titlu_%s_%d" % (sufix, i), titlu, FB, 16, "Verde")
        text(xi, MARG + 74, xe - xi, H - 2 * MARG - 74, "text_%s_%d" % (sufix, i),
             "Text de completat. Nu depăși ghidajele de 5 mm de la pliu.", FR, 10, "Negru bogat")

pagina(1, EXT, ["CLAPĂ (intră înăuntru)", "SPATE – contact, adresă, QR", "FAȚĂ – titlu & imagine"], "ext")
pagina(2, INT, ["INTERIOR 1", "INTERIOR 2", "INTERIOR 3 (panou îngust)"], "int")

# fata (pag. 1, panoul 3): fundal colorat
scribus.gotoPage(1)
scribus.setActiveLayer("Fundal")
scribus.createRect(197, -BLEED, 100 + BLEED, H + 2 * BLEED, "fundal_fata")
scribus.setFillColor("Verde", "fundal_fata"); scribus.setLineColor("None", "fundal_fata")
scribus.setTextColor("White", "titlu_ext_2"); scribus.setFontSize(26, "titlu_ext_2")
scribus.setTextColor("White", "text_ext_2")
# QR pe spate
scribus.setActiveLayer("Imagini")
scribus.createImage(97 + 100 - GUT - 28, H - MARG - 28, 28, 28, "cod_QR")
scribus.setFillColor("White", "cod_QR"); scribus.setLineColor("None", "cod_QR")

# instructiuni pe strat netiparit
scribus.setActiveLayer("Ghidaje")
text(MARG, H - MARG - 12, W - 2 * MARG, 12, "instructiuni",
     "PLIERE ÎN C: clapa de 97 mm intră în interior. Textul la min. 5 mm de pliu. "
     "Export: PDF/X-1a · Coated FOGRA39 · bleed 3 mm · crop marks · 300 dpi · Preflight fără erori.",
     FR, 7, "Galben")
scribus.setLayerPrintable("Ghidaje", False); scribus.setLayerLocked("Ghidaje", True)
scribus.setActiveLayer("Text"); scribus.gotoPage(1)
scribus.messageBox("Șablon gata", "File → Save as Template… → „Pliant A4 trifold”", scribus.ICON_INFORMATION)
