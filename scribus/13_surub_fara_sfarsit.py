# -*- coding: utf-8 -*-
"""
13 – ȘURUB FĂRĂ SFÂRȘIT (angrenaj melc – roată melcată), randare 3D umbrită
Un mic „motor 3D” în Python pur: suprafețele sunt descrise parametric, împărțite
în patrulatere, rotite în spațiu, sortate după adâncime (algoritmul pictorului)
și umplute cu o nuanță calculată din unghiul dintre normală și lumină.
Filetul melcului este o suprafață reală r(x, θ) – nu un desen „pe deasupra”.

Rulare: Script > Execute Script... > 13_surub_fara_sfarsit.py
Cere: unghiurile de vedere (rotire orizontală / înclinare) și numărul de dinți.
"""
import math

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

NUANTE = 14                      # câte trepte de umbrire pe material
LUMINA = (0.35, 0.55, 0.75)      # direcția luminii (spre privitor, de sus-stânga)


# ---------- utilitare culoare / text ----------
def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def material(nume, baza):
    """definește NUANTE trepte de la întunecat la deschis pentru culoarea de bază"""
    for k in range(NUANTE):
        t = 0.18 + 0.82 * k / (NUANTE - 1)
        r, g, b = [min(255, int(c * t + 40 * (t ** 4))) for c in baza]
        culoare("%s_%02d" % (nume, k), r, g, b)


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


def text(x, y, w, h, s, f, corp, cul):
    t = scribus.createText(x, y, w, h)
    scribus.setText(s, t)
    scribus.setFont(f, t)
    scribus.setFontSize(corp, t)
    scribus.setTextColor(cul, t)
    return t


# ---------- motorul 3D ----------
def normalizat(v):
    l = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) or 1.0
    return (v[0] / l, v[1] / l, v[2] / l)


def rotit(p, beta, alfa):
    """rotire în jurul axei verticale y (beta) apoi înclinare în jurul axei x (alfa)"""
    x, y, z = p
    cb, sb = math.cos(beta), math.sin(beta)
    x, z = x * cb + z * sb, -x * sb + z * cb
    ca, sa = math.cos(alfa), math.sin(alfa)
    y, z = y * ca - z * sa, y * sa + z * ca
    return (x, y, z)


class Scena:
    def __init__(self, beta_grade, alfa_grade, cx, cy, scara):
        self.beta, self.alfa = math.radians(beta_grade), math.radians(alfa_grade)
        self.cx, self.cy, self.scara = cx, cy, scara
        self.fete = []          # (adancime, puncte2d, culoare)
        self.lum = normalizat(LUMINA)

    def fata(self, p3d, mat, ref):
        """p3d = 4 puncte 3D; ref = punct interior (pe axa piesei) – normala se
        orientează dinspre ref spre exterior, ca să știm ce fețe sunt în spate"""
        cxm = sum(p[0] for p in p3d) / 4.0
        cym = sum(p[1] for p in p3d) / 4.0
        czm = sum(p[2] for p in p3d) / 4.0
        rp = ref((cxm, cym, czm))
        ax, ay, az = p3d[1][0] - p3d[0][0], p3d[1][1] - p3d[0][1], p3d[1][2] - p3d[0][2]
        bx, by, bz = p3d[2][0] - p3d[0][0], p3d[2][1] - p3d[0][1], p3d[2][2] - p3d[0][2]
        n = (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)
        if abs(n[0]) + abs(n[1]) + abs(n[2]) < 1e-9:      # două colțuri suprapuse (pol)
            ax, ay, az = p3d[2][0] - p3d[0][0], p3d[2][1] - p3d[0][1], p3d[2][2] - p3d[0][2]
            bx, by, bz = p3d[3][0] - p3d[0][0], p3d[3][1] - p3d[0][1], p3d[3][2] - p3d[0][2]
            n = (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)
        if n[0] * (cxm - rp[0]) + n[1] * (cym - rp[1]) + n[2] * (czm - rp[2]) < 0:
            n = (-n[0], -n[1], -n[2])
        n = normalizat(rotit(n, self.beta, self.alfa))
        r = [rotit(p, self.beta, self.alfa) for p in p3d]
        if n[2] < 0:            # fața privește în spate → o ignorăm (economie de obiecte)
            return
        iluminare = max(0.0, n[0] * self.lum[0] + n[1] * self.lum[1] + n[2] * self.lum[2])
        k = int(iluminare * (NUANTE - 1))
        adanc = sum(p[2] for p in r) / len(r)
        pts = []
        for x, y, z in r:
            pts += [self.cx + x * self.scara, self.cy - y * self.scara]
        self.fete.append((adanc, pts, "%s_%02d" % (mat, k)))

    def deseneaza(self):
        self.fete.sort(key=lambda f: f[0])      # întâi cele îndepărtate
        scribus.progressTotal(len(self.fete))
        for i, (_, pts, cul) in enumerate(self.fete):
            p = scribus.createPolygon(pts)
            scribus.setFillColor(cul, p)
            scribus.setLineColor(cul, p)
            scribus.setLineWidth(0.15, p)       # acoperă rosturile dintre fețe
            if i % 50 == 0:
                scribus.progressSet(i)
        return len(self.fete)


def suprafata(scena, functie, nu, nv, mat, ref, inchis_u=False, inchis_v=True):
    """împarte o suprafață parametrică (u,v)->(x,y,z) în patrulatere;
    ref(p) = punctul de pe axa piesei cel mai apropiat de p (pentru orientarea normalei)"""
    mu = nu if inchis_u else nu - 1
    mv = nv if inchis_v else nv - 1
    for i in range(mu):
        for j in range(mv):
            i2, j2 = (i + 1) % nu, (j + 1) % nv
            scena.fata([functie(i, j), functie(i2, j), functie(i2, j2), functie(i, j2)], mat, ref)


# ---------- piesele ----------
def melc(scena, lung, r_fund, r_varf, pas, ncap, mat):
    """suprafață r(x,θ): filet triunghiular cu `ncap` începuturi"""
    nx, nt = 70, 30

    def profil(f):                       # f în [0,1): dinte triunghiular rotunjit
        f = f % 1.0
        return 0.5 - 0.5 * math.cos(2 * math.pi * f) if f < 1 else 0

    def p(i, j):
        x = -lung / 2 + lung * i / (nx - 1)
        th = 2 * math.pi * j / nt
        f = ncap * (x / pas - th / (2 * math.pi))
        r = r_fund + (r_varf - r_fund) * profil(f)
        return (x, r * math.cos(th), r * math.sin(th))
    suprafata(scena, p, nx, nt, mat, lambda q: (q[0], 0, 0))
    # capetele (discuri) și arborele
    for semn in (-1, 1):
        def disc(i, j, semn=semn):
            th = 2 * math.pi * j / nt
            r = r_fund * (1 - i / 3.0)
            return (semn * lung / 2, r * math.cos(th), r * math.sin(th))
        suprafata(scena, disc, 4, nt, mat, lambda q: (0, 0, 0))
    # arborele: două cioturi în afara melcului (o singură bucată lungă s-ar sorta greșit)
    cilindru(scena, (-lung / 2 - 40, 0, 0), (-lung / 2, 0, 0), r_fund * 0.45, mat)
    cilindru(scena, (lung / 2, 0, 0), (lung / 2 + 40, 0, 0), r_fund * 0.45, mat)


def cilindru(scena, a, b, r, mat, n=24):
    """cilindru între punctele a și b (axa x sau y)"""
    axa_x = abs(b[0] - a[0]) > abs(b[1] - a[1])

    def p(i, j):
        t = i / 1.0
        th = 2 * math.pi * j / n
        if axa_x:
            x = a[0] + (b[0] - a[0]) * t
            return (x, r * math.cos(th), r * math.sin(th))
        y = a[1] + (b[1] - a[1]) * t
        return (r * math.cos(th) + a[0], y, r * math.sin(th) + a[2])
    ref = (lambda q: (q[0], a[1], a[2])) if axa_x else (lambda q: (a[0], q[1], a[2]))
    suprafata(scena, p, 2, n, mat, ref)


def roata_melcata(scena, centru, z, modul, latime, unghi_elice, mat, faza=0.0):
    """roată dințată cu dinți înclinați (elicoidali) – axa pe y"""
    rp = modul * z / 2.0
    ra, rf = rp + modul, rp - 1.25 * modul
    n = z * 6
    ny = 6
    tg = math.tan(math.radians(unghi_elice))

    def raza(f):                       # profil dinte (trapez rotunjit) pe un pas
        f = f % 1.0
        s = 0.5 - 0.5 * math.cos(2 * math.pi * f)
        return rf + (ra - rf) * min(1.0, s * 1.6)

    def coroana(i, j):
        y = -latime / 2 + latime * i / (ny - 1)
        # dinții „alunecă” cu y → elice; concavitate ușoară pe lățime (roată melcată)
        phi = 2 * math.pi * j / n + faza + y * tg / rp
        r = raza(z * phi / (2 * math.pi)) - 0.35 * modul * (1 - (2 * y / latime) ** 2)
        return (centru[0] + r * math.cos(phi), centru[1] + y, centru[2] + r * math.sin(phi))
    suprafata(scena, coroana, ny, n, mat, lambda q: centru, inchis_u=False)
    # flancurile laterale (inele) + butuc
    for semn in (-1, 1):
        def inel(i, j, semn=semn):
            y = semn * latime / 2
            phi = 2 * math.pi * j / n + faza + y * tg / rp
            r_ext = raza(z * phi / (2 * math.pi)) - 0.35 * modul * (1 - (2 * y / latime) ** 2)
            r = r_ext - (r_ext - rp * 0.3) * i
            return (centru[0] + r * math.cos(phi), centru[1] + y, centru[2] + r * math.sin(phi))
        suprafata(scena, inel, 2, n, mat, lambda q: centru)
    for a, b in ((-latime * 1.6, -latime / 2), (latime / 2, latime * 1.6)):
        cilindru(scena, (centru[0], centru[1] + a, centru[2]),
                 (centru[0], centru[1] + b, centru[2]), rp * 0.3, mat)


# ---------- program ----------
def main():
    beta = float(scribus.valueDialog("Melc–roată melcată", "Rotire orizontală (grade):", "-35") or -35)
    alfa = float(scribus.valueDialog("Melc–roată melcată", "Înclinare (grade):", "25") or 25)
    z = int(scribus.valueDialog("Melc–roată melcată", "Dinți pe roata melcată:", "30") or 30)

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.LANDSCAPE,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()

    culoare("M3D_Fundal", 28, 30, 36)
    culoare("M3D_Text", 230, 230, 230)
    culoare("M3D_Accent", 255, 190, 60)
    material("Otel", (150, 175, 205))        # melcul – oțel albăstrui
    material("Bronz", (205, 140, 70))        # roata – bronz
    fnd = scribus.createRect(0, 0, W, H)
    scribus.setFillColor("M3D_Fundal", fnd)
    scribus.setLineColor("None", fnd)

    modul = 3.0
    ncap = 1                                   # melc cu un început
    r_fund, r_varf = 10.0, 10.0 + 2.25 * modul
    pas = math.pi * modul
    rp_melc = (r_fund + r_varf) / 2 - 0.1
    rp_roata = modul * z / 2.0
    d = rp_melc + rp_roata                     # distanța dintre axe
    unghi_elice = math.degrees(math.atan(ncap * modul / (2 * rp_melc)))

    scribus.setRedraw(False)
    scena = Scena(beta, alfa, W * 0.5, H * 0.46, 1.1)
    melc(scena, 110, r_fund, r_varf, pas, ncap, "Otel")
    roata_melcata(scena, (0, 0, -d), z, modul, 22, unghi_elice, "Bronz", faza=math.pi / z)
    nf = scena.deseneaza()

    f = font(["DejaVu Sans", "Liberation Sans", "Arial"])
    fb = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    text(12, 10, 200, 12, "ANGRENAJ MELC – ROATĂ MELCATĂ", fb, 18, "M3D_Accent")
    info = ("modul m = %.1f mm   |   melc: %d început, pas p = %.2f mm, unghi elice %.1f°\n"
            "roată melcată: z = %d dinți, diametru de divizare %.0f mm   |   raport de transmitere i = %d:1\n"
            "distanța dintre axe a = %.1f mm   |   %d fețe randate"
            % (modul, ncap, pas, unghi_elice, z, 2 * rp_roata, z // ncap, d, nf))
    text(12, H - 30, W - 24, 24, info, f, 9, "M3D_Text")

    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Melc–roată melcată", "%d fețe. Schimbă unghiurile de vedere și rulează din nou." % nf,
                       scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
