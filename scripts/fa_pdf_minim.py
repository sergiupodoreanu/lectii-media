# Genereaza "exemplu-minim.pdf": un PDF de o pagina, scris de mana, necomprimat,
# ca elevii sa-l poata citi in Notepad++. Calculeaza corect tabelul xref.
import sys

out = sys.argv[1] if len(sys.argv) > 1 else "exemplu-minim.pdf"

content = b"""BT
/F1 28 Tf
72 700 Td
(Acesta este un PDF minim.) Tj
0 -40 Td
/F1 14 Tf
(Deschide fisierul in Notepad++ si cauta obiectele.) Tj
ET
0 0 1 RG 4 w
72 600 m 400 600 l S
"""

objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
    b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"endstream",
]

pdf = bytearray(b"%PDF-1.4\n")
offsets = []
for i, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"

xref_pos = len(pdf)
pdf += f"xref\n0 {len(objects) + 1}\n".encode()
pdf += b"0000000000 65535 f \n"
for off in offsets:
    pdf += f"{off:010d} 00000 n \n".encode()
pdf += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n").encode()

open(out, "wb").write(pdf)
print(out, len(pdf), "octeti")
