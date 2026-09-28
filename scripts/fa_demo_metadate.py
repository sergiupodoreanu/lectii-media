# -*- coding: utf-8 -*-
# scripts/fa_demo_metadate.py — mostra de FORENSICA pentru laborator.
# Fisier INERT: fara retea, fara JavaScript, fara actiuni.
# Demonstreaza: (1) metadate care dezvaluie autorul si calea de pe disc;
#               (2) "redactare gresita" — text sensibil acoperit cu o bara neagra,
#                   dar ramas in fisier, deci extractibil cu pdftotext / copy-paste.
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import sys

out = sys.argv[1] if len(sys.argv) > 1 else "demo-metadate.pdf"
c = canvas.Canvas(out, pagesize=A4)
c.setAuthor("Ion Popescu")
c.setTitle("C:/Users/ion.popescu/Desktop/salarii_2026_CONFIDENTIAL.docx")
c.setCreator("Microsoft Word pentru Microsoft 365")
c.setSubject("Draft salarii - NU se distribuie")
c.setKeywords("confidential, salarii, draft, ciorna")
W, H = A4
c.setFont("Helvetica-Bold", 18); c.drawString(25*mm, H-30*mm, "Adeverinta")
c.setFont("Helvetica", 11)
c.drawString(25*mm, H-45*mm, "Se adevereste ca elevul are media 9,50 la purtare.")
c.drawString(25*mm, H-53*mm, "Document de test pentru lectia de forensica PDF.")
y = H-70*mm
c.drawString(25*mm, y, "CNP elev: 5091128104427   (acesta ar trebui ascuns)")
c.setFillColorRGB(0, 0, 0)
c.rect(24*mm, y-2, 120*mm, 14, fill=1, stroke=0)   # bara neagra PESTE text (redactare gresita)
c.setFillColorRGB(0, 0, 0)
c.setFont("Helvetica-Oblique", 9)
c.drawString(25*mm, 25*mm, "Fisier de laborator, inert. Foloseste exiftool / pdfinfo si selecteaza sub bara neagra.")
c.showPage(); c.save()
print("scris", out)
