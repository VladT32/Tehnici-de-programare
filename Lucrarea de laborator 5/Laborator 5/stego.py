"""Ascunde si dezvaluie un mesaj folosind LSB pe canalele RGB."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
PROBE = ROOT / "probe"


def ascunde(intrare, iesire, mesaj=b"FLAG{ascuns_in_pixeli}"):
    img = Image.open(intrare).convert("RGB")
    pixeli = list(img.getdata())
    # Octetul nul marcheaza sfarsitul mesajului.
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")
    capacitate = len(pixeli) * 3
    if len(biti) > capacitate:
        raise ValueError("Imaginea nu are suficienta capacitate pentru mesaj.")
    rezultat = []
    index = 0
    for r, g, b in pixeli:
        canale = [r, g, b]
        for j in range(3):
            if index < len(biti):
                canale[j] = (canale[j] & ~1) | int(biti[index])
                index += 1
        rezultat.append(tuple(canale))
    img.putdata(rezultat)
    img.save(iesire, format="PNG")


def dezvaluie(cale):
    pixeli = Image.open(cale).convert("RGB").getdata()
    biti = []
    octeti = []
    for pixel in pixeli:
        for canal in pixel:
            biti.append(str(canal & 1))
            if len(biti) == 8:
                octet = int("".join(biti), 2)
                if octet == 0:
                    return bytes(octeti).decode("utf-8", errors="replace")
                octeti.append(octet)
                biti = []
    return bytes(octeti).decode("utf-8", errors="replace")


def main():
    intrare = PROBE / "foto.jpg"
    iesire = ROOT / "stego.png"
    if not intrare.exists():
        raise FileNotFoundError(f"Lipseste {intrare}. Ruleaza mai intai probe/pregateste.py.")
    ascunde(intrare, iesire)
    print("Mesaj ascuns in:", iesire.name)
    print("Mesaj dezvaluit:", dezvaluie(iesire))


if __name__ == "__main__":
    main()
