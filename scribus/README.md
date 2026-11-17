# Scripturi Python pentru Scribus – demonstrații pentru elevi

Testate pe Scribus 1.5.8 / 1.6.x (Python 3 integrat).

## Cum se rulează
1. Deschide Scribus.
2. Meniul **Script → Execute Script...**
3. Alege fișierul `.py`. Scriptul cere 1–2 valori într-o fereastră, apoi desenează.
4. Ca să vadă elevii codul în timp ce rulează: **Script → Show Console**.

| Script | Ce face | Ce învață elevii |
|---|---|---|
| 01_mandala.py | mandala din petale colorate, pe inele | trigonometrie → poligoane, cerc cromatic HSV, transparență |
| 02_poster_tipografic.py | afiș cu cuvinte scalate să umple lățimea | corp de literă calculat din lățime, pt ↔ mm |
| 03_calendar.py | calendar de perete, 12 pagini A4 landscape | modulul `calendar`, grilă, pagini multiple |
| 04_carti_vizita_csv.py | 10 cărți de vizită/pagină din CSV | mail-merge, date → machetă, colțuri rotunjite |
| 05_spirograf.py | curbe hipotrohoide suprapuse | polilinii din formule, parametri → formă |

## Idei de exerciții
- Schimbă paleta `PALETA` (02) sau seturile `(R, r, d)` din 05.
- Adaugă o coloană `firma` în CSV și afișeaz-o pe cartea de vizită (04).
- Marchează sărbătorile legale în calendar (03) cu altă culoare.
- Exportă rezultatul: **File → Export → Save as PDF**.

## Efecte speciale (partea a II-a)

| Script | Ce face | Ce învață elevii |
|---|---|---|
| 06_album_foto.py | album foto din folder, copertă + grilă de poze cu ramă și umbră | cadre imagine, scalare proporțională, `os.listdir` |
| 07_text_3d.py | titlu extrudat 3D (25 straturi) + reflexie estompată | straturi suprapuse, luminozitate HSV, transparență |
| 08_arbore_fractal.py | copac fractal cu cer în gradient și frunze colorate | recursivitate, hazard controlat, grosime de linie |
| 09_galaxie.py | galaxie spiralată din ~1500 stele, nucleu strălucitor | spirala logaritmică, distribuție gaussiană |
| 10_val_puncte.py | grilă de puncte cu diametru/culoare după o funcție (relief 3D) | principiul rasterului tipografic, funcții 2D |
| 11_text_spirala.py | literele unei fraze pe spirală, rotite după tangentă | spirala arhimedică, rotire obiecte, cerc cromatic |

Atenție: 09 și 10 creează 1500–3000 obiecte – durează 10–30 s; nu închide Scribus în timpul barei de progres.

## Desene tehnice complexe / 3D (partea a III-a)

| Script | Ce face | Ce învață elevii |
|---|---|---|
| 12_noaptea_umbrelor.py | compoziție Halloween A3: lună, copaci fractali, cimitir, fantome, om tras în vârtej | compunerea unei scene din funcții, straturi, transparență |
| 13_surub_fara_sfarsit.py | angrenaj melc – roată melcată randat 3D umbrit (filet ca suprafață reală) | suprafețe parametrice, normale, algoritmul pictorului |
| 14_tren_roti_dintate.py | tren de roți dințate care angrenează corect (modul, distanța dintre axe, raport) | geometria roților dințate, fazarea dinților |
| 15_atelier_3d.py | arc elicoidal, tor, arbore strunjit, sferă, șurub M12 – randate 3D | corpuri de revoluție, prisme, elice |

Scripturile 13 și 15 conțin același „motor 3D” (≈60 de linii): rotire → proiecție ortogonală → sortare după adâncime → umbrire după normală. Elevii pot adăuga propriile obiecte scriind doar funcția (i, j) → (x, y, z).

## Machete de publicații (partea a IV-a)

| Script | Ce face | Ce învață elevii |
|---|---|---|
| 16_revista.py | revistă A4, 4 pagini: copertă cu cover lines și cod de bare, sumar, articol pe 3 coloane cu literă inițială și citat scos, galerie pe grilă modulară | grila de coloane, ierarhia titlurilor, folio, text în jurul obiectelor |
| 17_ziar.py | prima pagină de ziar A3 pe 5 coloane: frontispiciu, articol principal cu foto, secundare cu text înlănțuit, casetă „pe scurt”, vreme | cadre de text înlănțuite, ghidaje de coloană, ierarhie tipografică |
| 18_pliant_trei.py | pliant în trei (trifold) A4 landscape, față + verso, cu ordinea corectă a panourilor, pictograme, QR simulat | impoziția pliantului, panouri de 99 mm, linii de pliere |

Cadrele gri „FOTO” sunt cadre de imagine goale: clic dreapta → **Get Image** (Ctrl+I) și pui poza reală. Textul din coloane este text de umplutură – se înlocuiește cu articolul.

## Șabloane pentru tipar (din lecția „Fișierele PDF”)

| Script | Ce face |
|---|---|
| sablon_afis_A3.py | șablon de afiș A3 pentru tipar: bleed 3 mm, culori CMYK, straturi, ghidaje |
| sablon_pliant_trifold.py | șablon de pliant A4 în trei, pliere în C |
| sablon_pliant_Z.py | șablon de pliant A4 în trei, pliere în Z (3 panouri de 99 mm) |
