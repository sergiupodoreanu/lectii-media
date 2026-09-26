# -*- coding: utf-8 -*-
# Pliant A4 pliere in Z (acordeon), 3 panouri egale de 99 mm - Scribus 1.6
import scribus

W, H, BLEED, MARG, GUT = 297.0, 210.0, 3.0, 8.0, 5.0
P = W / 3.0                          # 99 mm
PLIURI = [P, 2 * P]

scribus.newDocument((W, H), (MARG, MARG, MARG, MARG), scribus.LANDSCAPE,
                    1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 2)
scribus.setBleeds(BLEED, BLEED, BLEED, BLEED)

scribus.defineColorCMYK("Negru bogat", 153, 102, 102, 255)
scribus.defineColorCMYK("Bordo",       0,   255, 153, 77)
scribus.defineColorCMYK("Crem",        0,   13,  38,  0)
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

def ghidaje():
    scribus.setVGuides(PLIURI + [p - GUT for p in PLIURI] + [p + GUT for p in PLIURI])
    scribus.setHGuides([MARG, H - MARG])

def fundal(nume, col):
    scribus.setActiveLayer("Fundal")
    scribus.createRect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, nume)
    scribus.setFillColor(col, nume); scribus.setLineColor("None", nume)

def panou(i, titlu, sufix):
    xi = i * P + (MARG if i == 0 else GUT)
    xe = (i + 1) * P - (MARG if i == 2 else GUT)
    scribus.setActiveLayer("Imagini")
    scribus.createImage(xi, MARG, xe - xi, 55, "img_%s_%d" % (sufix, i))
    scribus.setActiveLayer("Text")
    text(xi, MARG + 58, xe - xi, 14, "titlu_%s_%d" % (sufix, i), titlu, FB, 16, "Bordo")
    text(xi, MARG + 74, xe - xi, H - 2 * MARG - 74, "text_%s_%d" % (sufix, i),
         "Text de completat. Păstrează 5 mm față de pliu.", FR, 10, "Negru bogat")

# ---------- PAGINA 1: exterior ----------
scribus.gotoPage(1); ghidaje()
fundal("fundal_ext", "Crem")
panou(0, "SPATE – contact, adresă, QR", "ext")
panou(1, "PANOU MIJLOC – rezumat / hartă", "ext")
scribus.setActiveLayer("Fundal")
scribus.createRect(2 * P, -BLEED, P + BLEED, H + 2 * BLEED, "fundal_fata")
scribus.setFillColor("Bordo", "fundal_fata"); scribus.setLineColor("None", "fundal_fata")
scribus.setActiveLayer("Imagini")
scribus.createImage(2 * P + GUT, MARG, P - GUT - MARG, 95, "img_fata")
scribus.setActiveLayer("Text")
text(2 * P + GUT, MARG + 100, P - GUT - MARG, 40, "titlu_fata",
     "TITLUL PLIANTULUI", FB, 24, "White", scribus.ALIGN_CENTERED)
text(2 * P + GUT, MARG + 142, P - GUT - MARG, 30, "subtitlu_fata",
     "Slogan / eveniment / dată", FR, 13, "Crem", scribus.ALIGN_CENTERED)
scribus.setActiveLayer("Imagini")
scribus.createImage(P - GUT - 28, H - MARG - 28, 28, 28, "cod_QR")
scribus.setFillColor("White", "cod_QR"); scribus.setLineColor("None", "cod_QR")

# ---------- PAGINA 2: interior continuu ----------
scribus.gotoPage(2); ghidaje()
fundal("fundal_int", "Gri deschis")
scribus.setActiveLayer("Fundal")
scribus.createRect(-BLEED, -BLEED, W + 2 * BLEED, 38 + BLEED, "banda_int")
scribus.setFillColor("Bordo", "banda_int"); scribus.setLineColor("None", "banda_int")
scribus.setActiveLayer("Text")
text(MARG, MARG, W - 2 * MARG, 24, "titlu_int",
     "TITLU CONTINUU PE TOATE CELE 3 PANOURI", FB, 22, "White", scribus.ALIGN_CENTERED)
scribus.setActiveLayer("Imagini")
scribus.createImage(-BLEED, 40, W + 2 * BLEED, 60, "img_panorama")
for i, t in enumerate(["PASUL 1", "PASUL 2", "PASUL 3"]):
    xi = i * P + (MARG if i == 0 else GUT)
    xe = (i + 1) * P - (MARG if i == 2 else GUT)
    scribus.setActiveLayer("Text")
    text(xi, 104, xe - xi, 14, "titlu_int_%d" % i, t, FB, 16, "Bordo")
    text(xi, 120, xe - xi, H - MARG - 120, "text_int_%d" % i,
         "Text de completat. Ordinea de citire: fața → int.1 → int.2 → int.3 → mijloc → spate.",
         FR, 10, "Negru bogat")

# ---------- Ghidaje (netiparit) ----------
scribus.gotoPage(1); scribus.setActiveLayer("Ghidaje")
text(MARG, H - MARG - 12, W - 2 * MARG, 12, "instructiuni",
     "PLIERE ÎN Z: 3 panouri egale de 99 mm, pliuri la 99 și 198 mm. Text la min. 5 mm de pliu. "
     "Export: PDF/X-1a · Coated FOGRA39 · bleed 3 mm · crop marks · 300 dpi · Preflight fără erori.",
     FR, 7, "Bordo")
scribus.setLayerPrintable("Ghidaje", False); scribus.setLayerLocked("Ghidaje", True)
scribus.setActiveLayer("Text")
scribus.messageBox("Șablon gata", "File → Save as Template… → „Pliant A4 pliere Z”", scribus.ICON_INFORMATION)
