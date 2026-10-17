# Raport — Laboratorul 5: Forensics și steganografie

## Lucrarea A — Decoder universal

- Mesajul cu straturi din `probe/mesaj.txt` dezvăluie: `FLAG{straturi_de_encoding}`.
- Cheia XOR găsită pentru `probe/xor.bin`: `0x80` (128).
- Textul XOR recuperat: `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`.
- Hash-urile MD5 verificate prin dicționar:
  - `password`
  - `dragon`
  - `qwerty`
  - `letmein`
  - `monkey`
- `decode.py` clasifică și decodează Base64, Hex și URL, repetă decodarea straturilor, încearcă cheile XOR pe un octet și verifică hash-urile din wordlist.
- `fisa.json` păstrează rezultatul ultimei operații de decodare.

## Lucrarea B — Forensics pe fișiere

- `foto.jpg`: tip real JPEG.
- Metadate EXIF: producător `Apple`, model `iPhone 13`, data `2026:09:14 10:30:00`.
- Coordonate GPS: latitudine `47.0166667`, longitudine `28.8575` (Chișinău).
- `ascuns.png`: tip real PNG; arhiva ZIP începe la octetul `781`.
- În arhiva ZIP se află `secret.txt`, cu mesajul `FLAG{ascuns_prin_carving}`.
- Mesajul ascuns și recuperat prin LSB din `stego.png`: `FLAG{ascuns_in_pixeli}`.

## Comenzi de rulare

```bash
python probe/pregateste.py
python -m pytest teste/test_decode.py -q
python arsenal/forensics/decode.py "$(python -c "print(open('probe/mesaj.txt').read().strip())")"
python arsenal/forensics/decode.py probe/xor.bin --fisier --xor
python arsenal/forensics/decode.py probe/hashuri.txt --hashuri
python forensics.py
python stego.py
```

Notă: rezultatele de mai sus sunt cele produse de scriptul `pregateste.py` furnizat pentru acest laborator.
