# -*- coding: utf-8 -*-
"""
15 – ATELIER 3D: arc elicoidal, tor, piesă strunjită, sferă, șurub cu cap hexagonal
Același „motor 3D” ca în scriptul 13 (suprafețe parametrice, algoritmul
pictorului, umbrire după normală). Alegi obiectul și unghiurile de vedere.

Rulare: Script > Execute Script... > 15_atelier_3d.py
"""
import math

try:
    import scribus
except ImportError:
    print("Rulează scriptul din Scribus (Script > Execute Script).")
    raise SystemExit

NUANTE = 14
LUMINA = (0.35, 0.55, 0.75)


def culoare(nume, r, g, b):
    try:
        scribus.defineColorRGB(nume, r, g, b)
    except Exception:
        c, m, y = 255 - r, 255 - g, 255 - b
        k = min(c, m, y)
        scribus.defineColor(nume, c - k, m - k, y - k, k)


def material(nume, baza):
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


def normalizat(v):
    l = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) or 1.0
    return (v[0] / l, v[1] / l, v[2] / l)


def rotit(p, beta, alfa):
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
        self.fete = []
        self.lum = normalizat(LUMINA)

    def fata(self, p3d, mat, ref):
        cxm = sum(p[0] for p in p3d) / len(p3d)
        cym = sum(p[1] for p in p3d) / len(p3d)
        czm = sum(p[2] for p in p3d) / len(p3d)
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
        if n[2] < 0:
            return
        il = max(0.0, n[0] * self.lum[0] + n[1] * self.lum[1] + n[2] * self.lum[2])
        k = int(il * (NUANTE - 1))
        adanc = sum(p[2] for p in r) / len(r)
        pts = []
        for x, y, z in r:
            pts += [self.cx + x * self.scara, self.cy - y * self.scara]
        self.fete.append((adanc, pts, "%s_%02d" % (mat, k)))

    def deseneaza(self):
        self.fete.sort(key=lambda f: f[0])
        scribus.progressTotal(len(self.fete))
        for i, (_, pts, cul) in enumerate(self.fete):
            p = scribus.createPolygon(pts)
            scribus.setFillColor(cul, p)
            scribus.setLineColor(cul, p)
            scribus.setLineWidth(0.15, p)
            if i % 50 == 0:
                scribus.progressSet(i)
        return len(self.fete)


def suprafata(scena, functie, nu, nv, mat, ref, inchis_u=False, inchis_v=True):
    mu = nu if inchis_u else nu - 1
    mv = nv if inchis_v else nv - 1
    for i in range(mu):
        for j in range(mv):
            i2, j2 = (i + 1) % nu, (j + 1) % nv
            scena.fata([functie(i, j), functie(i2, j), functie(i2, j2), functie(i, j2)], mat, ref)


# ---------- obiectele ----------
def arc_elicoidal(scena, mat):
    """arc de compresiune: tub (rază r_sarma) înfășurat pe o elice (rază R, pas p), axa y"""
    R, r, pas, spire = 22.0, 3.2, 12.0, 6
    nu, nv = 40 * spire, 14

    def p(i, j):
        t = 2 * math.pi * spire * i / (nu - 1)
        # capete plane: pasul scade la prima și ultima spiră
        f = min(1.0, min(t / (2 * math.pi), (2 * math.pi * spire - t) / (2 * math.pi)))
        y_axa = -pas * spire * 0.5 + pas * (t / (2 * math.pi)) * 1.0 - (1 - f) * 0
        ph = 2 * math.pi * j / nv
        # cadrul Frenet aproximat: direcția radială și axială
        rad = (math.cos(t), 0, math.sin(t))
        px = (R + r * math.cos(ph)) * rad[0]
        pz = (R + r * math.cos(ph)) * rad[2]
        py = y_axa + r * math.sin(ph)
        return (px, py, pz)

    def ref(q):
        t = math.atan2(q[2], q[0])
        return (R * math.cos(t), q[1], R * math.sin(t))
    suprafata(scena, p, nu, nv, mat, ref)


def tor(scena, mat):
    R, r = 30.0, 11.0
    nu, nv = 48, 24

    def p(i, j):
        u, v = 2 * math.pi * i / nu, 2 * math.pi * j / nv
        return ((R + r * math.cos(v)) * math.cos(u), r * math.sin(v), (R + r * math.cos(v)) * math.sin(u))

    def ref(q):
        t = math.atan2(q[2], q[0])
        return (R * math.cos(t), 0, R * math.sin(t))
    suprafata(scena, p, nu, nv, mat, ref, inchis_u=True)


def piesa_strunjita(scena, mat):
    """corp de revoluție dintr-un profil (y, r) – ca la strung"""
    profil = [(-45, 0), (-45, 8), (-40, 8), (-40, 14), (-28, 14), (-25, 20), (-10, 20), (-8, 26),
              (8, 26), (10, 20), (20, 20), (22, 12), (32, 12), (34, 9), (45, 9), (45, 0)]
    n = 36

    def p(i, j):
        y, r = profil[i]
        th = 2 * math.pi * j / n
        return (r * math.cos(th), y, r * math.sin(th))
    suprafata(scena, p, len(profil), n, mat, lambda q: (0, q[1], 0))
    # canal de pană pe treapta mare: reprezentat printr-un „decupaj” întunecat
    culoare("Canal_00", 30, 30, 34)
    for k in range(1, NUANTE):
        culoare("Canal_%02d" % k, 30, 30, 34)

    def canal(i, j):
        y = -8 + 16 * i
        x = -3 + 6 * j
        return (x, y, 26.05)
    suprafata(scena, canal, 2, 2, "Canal", lambda q: (0, q[1], 0), inchis_v=False)


def sfera(scena, mat):
    R, nu, nv = 36.0, 36, 24

    def p(i, j):
        u, v = 2 * math.pi * i / nu, math.pi * j / (nv - 1)
        return (R * math.sin(v) * math.cos(u), R * math.cos(v), R * math.sin(v) * math.sin(u))
    suprafata(scena, p, nu, nv, mat, lambda q: (0, 0, 0), inchis_u=True, inchis_v=False)


def surub_hexagonal(scena, mat):
    """cap hexagonal + tijă filetată (filet metric, suprafață r(y,θ))"""
    s, hcap, r_ext, r_int, pas, lung = 17.0, 8.0, 6.0, 4.9, 1.75, 45.0
    rc = s / math.sqrt(3)               # raza cercului circumscris hexagonului
    # capul: prismă hexagonală (6 fețe laterale + 2 capace)
    for k in range(6):
        a1, a2 = math.pi / 3 * k, math.pi / 3 * (k + 1)
        p1 = (rc * math.cos(a1), lung / 2, rc * math.sin(a1))
        p2 = (rc * math.cos(a2), lung / 2, rc * math.sin(a2))
        scena.fata([p1, p2, (p2[0], p2[1] + hcap, p2[2]), (p1[0], p1[1] + hcap, p1[2])], mat, lambda q: (0, q[1], 0))
    for yy in (lung / 2, lung / 2 + hcap):
        for k in range(6):
            a1, a2 = math.pi / 3 * k, math.pi / 3 * (k + 1)
            scena.fata([(0, yy, 0), (rc * math.cos(a1), yy, rc * math.sin(a1)),
                        (rc * math.cos(a2), yy, rc * math.sin(a2)), (0.001, yy, 0.001)], mat, lambda q: (0, lung / 2 + hcap / 2, 0))
    ny, nt = 90, 24

    def filet(i, j):
        y = -lung / 2 + lung * i / (ny - 1)
        th = 2 * math.pi * j / nt
        f = (y / pas - th / (2 * math.pi)) % 1.0
        r = r_int + (r_ext - r_int) * (0.5 - 0.5 * math.cos(2 * math.pi * f))
        if y > lung / 2 - 6:                 # porțiune nefiletată sub cap
            r = r_ext
        return (r * math.cos(th), y, r * math.sin(th))
    suprafata(scena, filet, ny, nt, mat, lambda q: (0, q[1], 0))

    def varf(i, j):                          # teșitura de la capăt
        th = 2 * math.pi * j / nt
        r = r_int * (1 - i)
        return (r * math.cos(th), -lung / 2 - 1.5 * i, r * math.sin(th))
    suprafata(scena, varf, 2, nt, mat, lambda q: (0, -lung / 2, 0))


OBIECTE = [("Arc elicoidal de compresiune", arc_elicoidal, (190, 60, 60), 2.0),
           ("Tor", tor, (70, 140, 210), 2.0),
           ("Piesă strunjită (arbore în trepte)", piesa_strunjita, (150, 175, 205), 2.2),
           ("Sferă", sfera, (230, 170, 60), 2.2),
           ("Șurub cu cap hexagonal M12", surub_hexagonal, (140, 150, 165), 3.4)]


def main():
    meniu = "\n".join("%d – %s" % (i + 1, o[0]) for i, o in enumerate(OBIECTE))
    alege = int(scribus.valueDialog("Atelier 3D", "Alege obiectul:\n" + meniu, "1") or 1)
    alege = max(1, min(len(OBIECTE), alege)) - 1
    beta = float(scribus.valueDialog("Atelier 3D", "Rotire orizontală (grade):", "-30") or -30)
    alfa = float(scribus.valueDialog("Atelier 3D", "Înclinare (grade):", "20") or 20)

    scribus.newDocument((210.0, 297.0), (10, 10, 10, 10), scribus.PORTRAIT,
                        1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    scribus.setUnit(scribus.UNIT_MILLIMETERS)
    W, H = scribus.getPageSize()
    culoare("A3D_Fundal", 28, 30, 36)
    culoare("A3D_Text", 230, 230, 230)
    nume, functie, baza, scara = OBIECTE[alege]
    material("Mat", baza)
    fnd = scribus.createRect(0, 0, W, H)
    scribus.setFillColor("A3D_Fundal", fnd)
    scribus.setLineColor("None", fnd)

    scribus.setRedraw(False)
    scena = Scena(beta, alfa, W / 2, H / 2, scara)
    functie(scena, "Mat")
    nf = scena.deseneaza()

    fb = font(["DejaVu Sans Bold", "Liberation Sans Bold", "Arial Bold"])
    t = scribus.createText(12, 10, W - 24, 12)
    scribus.setText(nume.upper() + "   (%d fețe, vedere %.0f°/%.0f°)" % (nf, beta, alfa), t)
    scribus.setFont(fb, t)
    scribus.setFontSize(14, t)
    scribus.setTextColor("A3D_Text", t)
    scribus.setRedraw(True)
    scribus.redrawAll()
    scribus.progressReset()
    scribus.messageBox("Atelier 3D", "%s: %d fețe." % (nume, nf), scribus.ICON_INFORMATION)


if __name__ == "__main__":
    main()
