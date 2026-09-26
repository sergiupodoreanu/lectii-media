# -*- coding: utf-8 -*-
# Sablon afis A3 pentru tipar - Scribus 1.6 (Script > Execute Script...)
# Dupa rulare: File > Save as Template...  ("Afis A3 tipar")
import scribus

W, H, BLEED, MARG, SAFE = 297.0, 420.0, 3.0, 15.0, 10.0

scribus.newDocument((W, H), (MARG, MARG, MARG, MARG), scribus.PORTRAIT,
                    1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
scribus.setBleeds(BLEED, BLEED, BLEED, BLEED)

# --- culori CMYK (0-255) ---
scribus.defineColorCMYK("Negru bogat", 153, 102, 102, 255)   # 60/40/40/100
scribus.defineColorCMYK("Albastru",    255, 153, 0,   26)    # 100/60/0/10
scribus.defineColorCMYK("Portocaliu",  0,   153, 255, 0)     # 0/60/100/0
scribus.defineColorCMYK("Gri deschis", 0,   0,   0,   26)    # 0/0/0/10

# --- font disponibil ---
fonts = scribus.getFontNames()
def f(*cand):
    return next((x for x in cand if x in fonts), fonts[0])
FB = f("Arial Bold", "Liberation Sans Bold", "DejaVu Sans Bold")
FR = f("Arial Regular", "Liberation Sans Regular", "DejaVu Sans Book")

# --- ghidaje: zona sigura + axa centrala ---
scribus.setVGuides([SAFE, W - SAFE, W / 2])
scribus.setHGuides([SAFE, H - SAFE])

def text(x, y, w, h, nume, s, font, size, col, al=scribus.ALIGN_LEFT):
    scribus.createText(x, y, w, h, nume)
    scribus.setText(s, nume)
    scribus.setFont(font, nume)
    scribus.setFontSize(size, nume)
    scribus.setTextColor(col, nume)
    scribus.setTextAlignment(al, nume)
    scribus.setTextDistances(4, 4, 4, 4, nume)

for L in ("Fundal", "Imagini", "Text", "Ghidaje"):
    scribus.createLayer(L)

# --- Fundal ---
scribus.setActiveLayer("Fundal")
scribus.createRect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, "fundal")
scribus.setFillColor("Gri deschis", "fundal"); scribus.setLineColor("None", "fundal")
scribus.createRect(-BLEED, H - 60, W + 2 * BLEED, 60 + BLEED, "banda_jos")
scribus.setFillColor("Albastru", "banda_jos"); scribus.setLineColor("None", "banda_jos")

# --- Imagini ---
scribus.setActiveLayer("Imagini")
scribus.createImage(MARG, 110, W - 2 * MARG, 190, "imagine_principala")
scribus.setLineColor("Albastru", "imagine_principala")
scribus.setLineWidth(0.5, "imagine_principala")
scribus.createImage(W - MARG - 35, H - 50, 35, 35, "cod_QR")
scribus.setFillColor("White", "cod_QR"); scribus.setLineColor("None", "cod_QR")

# --- Text ---
scribus.setActiveLayer("Text")
text(MARG, MARG, W - 2 * MARG, 55, "titlu", "TITLUL AFIȘULUI",
     FB, 72, "Negru bogat", scribus.ALIGN_CENTERED)
text(MARG, 72, W - 2 * MARG, 30, "subtitlu", "Subtitlu / slogan (max. 2 rânduri)",
     FR, 28, "Portocaliu", scribus.ALIGN_CENTERED)
text(MARG, 305, W - 2 * MARG, 45, "text_principal",
     "Data · Ora · Locul evenimentului\nText explicativ scurt: ce, unde, pentru cine.",
     FR, 20, "Negru bogat", scribus.ALIGN_CENTERED)
text(MARG, H - 50, W - 2 * MARG - 45, 35, "contact",
     "Organizator · telefon · site · e-mail", FR, 14, "White")

# --- Ghidaje (strat netiparit, blocat) ---
scribus.setActiveLayer("Ghidaje")
text(MARG, 350, W - 2 * MARG, 40, "instructiuni",
     "VERIFICARE ÎNAINTE DE EXPORT (stratul acesta nu se tipărește):\n"
     "1) Imagini ≥ 300 dpi la dimensiunea finală   2) Numai culori CMYK; negru bogat pe suprafețe, K100 pe text\n"
     "3) Textul în zona sigură (ghidaje la 10 mm)   4) Fundalul iese în bleed 3 mm\n"
     "5) Export: PDF/X-1a, Coated FOGRA39, bleed document + crop marks   6) Preflight Verifier fără erori",
     FR, 9, "Portocaliu")
scribus.setLayerPrintable("Ghidaje", False)
scribus.setLayerLocked("Ghidaje", True)

scribus.setActiveLayer("Text")
scribus.messageBox("Șablon gata",
                   "Salvează cu File → Save as Template…\nNume: Afiș A3 tipar / Categorie: Producție media",
                   scribus.ICON_INFORMATION)
