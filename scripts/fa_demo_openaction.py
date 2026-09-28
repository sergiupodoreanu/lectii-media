# -*- coding: utf-8 -*-
# scripts/fa_demo_openaction.py — mostra pentru DETECTIE, la laborator.
# Fisierul are un /OpenAction (actiune executata automat la deschidere), dar actiunea
# este COMPLET benigna: sare la pagina 2. FARA retea, FARA JavaScript, FARA URI/Launch.
# Rolul lui: sa "aprinda becul" /OpenAction in pdfid, ca elevii sa vada cum arata
# indicatorul — pericolul real e cand /OpenAction e insotit de /JS, /URI sau /SubmitForm.
import sys

out = sys.argv[1] if len(sys.argv) > 1 else "demo-openaction.pdf"

def stream(text):
    body = ("BT /F1 16 Tf 72 750 Td (" + text + ") Tj ET").encode()
    return b"<< /Length " + str(len(body)).encode() + b" >>\nstream\n" + body + b"\nendstream"

objs = [
    b"<< /Type /Catalog /Pages 2 0 R /OpenAction [4 0 R /Fit] >>",   # deschide direct la pag. 2
    b"<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 6 0 R >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 7 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    stream("Pagina 1 - dar fisierul se deschide direct la pagina 2"),
    stream("Pagina 2 - aici a sarit /OpenAction la deschidere"),
]
pdf = bytearray(b"%PDF-1.4\n"); offs = []
for i, o in enumerate(objs, 1):
    offs.append(len(pdf)); pdf += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
x = len(pdf); pdf += f"xref\n0 {len(objs)+1}\n".encode() + b"0000000000 65535 f \n"
for o in offs: pdf += f"{o:010d} 00000 n \n".encode()
pdf += (f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n").encode()
open(out, "wb").write(pdf)
print("scris", out, len(pdf), "octeti")
