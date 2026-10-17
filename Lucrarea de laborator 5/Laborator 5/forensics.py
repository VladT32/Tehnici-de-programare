"""Analiza semnaturilor, sirurilor, EXIF/GPS si extragerea arhivelor."""
import re
import zipfile
from pathlib import Path
from PIL import Image, ExifTags

ROOT = Path(__file__).resolve().parent
PROBE = ROOT / "probe"


def tip_real(cale):
    cap = Path(cale).read_bytes()[:8]
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if cap.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return "necunoscut: " + cap.hex()


def extrage_strings(cale, lungime_minima=4):
    date = Path(cale).read_bytes()
    return [m.decode("ascii", errors="replace")
            for m in re.findall(rb"[ -~]{" + str(lungime_minima).encode() + rb",}", date)]


def coordonate_gps(gps):
    def rational(v):
        return float(v[0]) / float(v[1]) if hasattr(v, "__len__") and len(v) == 2 else float(v)

    def decimal_triplet(v):
        grade, minute, secunde = [rational(x) for x in v]
        return grade + minute / 60 + secunde / 3600

    lat = decimal_triplet(gps[2])
    lon = decimal_triplet(gps[4])
    if gps[1] in ("S", b"S"):
        lat = -lat
    if gps[3] in ("W", b"W"):
        lon = -lon
    return lat, lon


def exif_gps(cale):
    img = Image.open(cale)
    exif = img.getexif()
    rezultat = {}
    for tag_id, val in exif.items():
        rezultat[ExifTags.TAGS.get(tag_id, tag_id)] = str(val)
    gps_id = next((k for k, v in ExifTags.TAGS.items() if v == "GPSInfo"), 34853)
    gps = exif.get_ifd(gps_id) if gps_id in exif else {}
    if gps:
        rezultat["GPSInfo"] = {ExifTags.GPSTAGS.get(k, k): str(v) for k, v in gps.items()}
        try:
            rezultat["coordonate_zecimale"] = coordonate_gps(gps)
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            rezultat["coordonate_zecimale"] = "GPS prezent, dar nu a putut fi convertit"
    return rezultat


def extrage_zip(cale, iesire="gasit.zip"):
    date = Path(cale).read_bytes()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None
    Path(iesire).write_bytes(date[i:])
    return i


def main():
    foto = PROBE / "foto.jpg"
    ascuns = PROBE / "ascuns.png"
    for cale in (foto, ascuns):
        if cale.exists():
            print(f"{cale.name}: tip real = {tip_real(cale)}")
    if ascuns.exists():
        print("\nSiruri citibile din ascuns.png:")
        for s in extrage_strings(ascuns):
            print(s)
        pozitie = extrage_zip(ascuns, ROOT / "gasit.zip")
        print("\nPozitia arhivei ZIP:", pozitie if pozitie is not None else "nu a fost gasita")
        if pozitie is not None:
            try:
                with zipfile.ZipFile(ROOT / "gasit.zip") as z:
                    print("Continut arhiva:", z.namelist())
                    z.extractall(ROOT / "arhiva_extrasa")
            except zipfile.BadZipFile:
                print("Arhiva extrasa, dar ZIP-ul pare incomplet sau invalid.")
    if foto.exists():
        print("\nMetadate EXIF/GPS:")
        for k, v in exif_gps(foto).items():
            print(f"{k} = {v}")


if __name__ == "__main__":
    main()
