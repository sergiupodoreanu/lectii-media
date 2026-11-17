# -*- coding: utf-8 -*-
"""
03 – CALENDAR ANUAL AUTOMAT (12 pagini A4 landscape)
Generează un calendar de perete: o pagină pe lună, grilă de zile,
weekend-urile colorate, ziua curentă evidențiată.
Arată elevilor cum date (modulul `calendar`) devin machetă.

Rulare: Script > Execute Script... > 03_calendar.py
"""
import calendar
import datetime

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

LUNI = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie",
        "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
ZILE = ["Lu", "Ma", "Mi", "Jo", "Vi", "Sâ", "Du"]


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


def text(x, y, w, h, s, f, corp, cul, align=None):
    t = scribus.createText(x, y, w, h)
    scribus.setText(s, t)
    scribus.setFont(f, t)
    scribus.setFontSize(corp, t)
    scribus.setTextColor(cul, t)
    if align is not None:
        scribus.setTextAlignment(align, t)
    return t


def main():
    an = scribus.valueDialog("Calendar", "Anul:", str(datetime.date.today().year))
    an = int(an or datetime.date.today().year)
    azi = datetime.date.today()

    scribus.newDocument((210.0, 297.0), (12, 12, 12, 12), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    w, h = scribus.getPageSize()
    m = 12
    lat = w - 2 * m

    culoare("Cal_Titlu", 30, 60, 120)
    culoare("Cal_Cap", 30, 60, 120)
    culoare("Cal_Celula", 245, 245, 248)
    culoare("Cal_Weekend", 255, 228, 225)
    culoare("Cal_Azi", 255, 205, 60)
    culoare("Cal_Linie", 200, 200, 210)
    culoare("Cal_Text", 40, 40, 40)

    f_bold = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    f_reg = font(["DejaVu Sans", "Liberation Sans", "Arial"])

    calendar.setfirstweekday(calendar.MONDAY)
    scribus.setRedraw(False)
    scribus.progressTotal(12)

    for luna in range(1, 13):
        if luna > 1:
            scribus.newPage(-1)
            scribus.gotoPage(luna)

        # titlul lunii
        text(m, m, lat, 22, "%s %d" % (LUNI[luna - 1], an), f_bold, 40, "Cal_Titlu",
             scribus.ALIGN_LEFT)
        linie = scribus.createLine(m, m + 24, w - m, m + 24)
        scribus.setLineColor("Cal_Titlu", linie)
        scribus.setLineWidth(1.2, linie)

        # capul de tabel (zilele săptămânii)
        y0 = m + 28
        cw = lat / 7.0
        for c, z in enumerate(ZILE):
            r = scribus.createRect(m + c * cw, y0, cw, 9)
            scribus.setFillColor("Cal_Cap", r)
            scribus.setLineColor("None", r)
            text(m + c * cw, y0 + 1.5, cw, 7, z, f_bold, 12, "White", scribus.ALIGN_CENTERED)

        # grila zilelor
        saptamani = calendar.monthcalendar(an, luna)
        ch = (h - m - (y0 + 10)) / 6.0
        for rnd in range(6):
            for c in range(7):
                x = m + c * cw
                y = y0 + 10 + rnd * ch
                r = scribus.createRect(x, y, cw, ch)
                scribus.setLineColor("Cal_Linie", r)
                scribus.setLineWidth(0.4, r)
                zi = saptamani[rnd][c] if rnd < len(saptamani) else 0
                if zi and an == azi.year and luna == azi.month and zi == azi.day:
                    scribus.setFillColor("Cal_Azi", r)
                elif c >= 5:
                    scribus.setFillColor("Cal_Weekend", r)
                else:
                    scribus.setFillColor("Cal_Celula", r)
                if zi:
                    text(x + 2, y + 1.5, cw - 4, 10, str(zi), f_bold, 16,
                         "Cal_Text", scribus.ALIGN_RIGHT)
        scribus.progressSet(luna)

    scribus.gotoPage(1)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Calendar", "Calendar %d generat: 12 pagini." % an,
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
