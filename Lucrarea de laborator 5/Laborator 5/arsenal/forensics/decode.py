"""Decoder universal pentru laboratorul 5: encoding, XOR si verificare hash."""
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT / "probe"
FISA = ROOT / "arsenal" / "forensics" / "fisa.json"


def ghici_strat(s: str) -> str:
    """Clasifica un strat de codare: URL, hex sau Base64."""
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if s and len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if s and len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", s):
        try:
            base64.b64decode(s, validate=True)
            return "base64"
        except (ValueError, base64.binascii.Error):
            pass
    return "necunoscut"


def desfa(s: str):
    """Intoarce (numele_stratului, rezultat_bytes)."""
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s, validate=True)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode("utf-8")
    return strat, s.encode("utf-8")


def citibil(b: bytes) -> bool:
    return all(32 <= c < 127 for c in b)


def decode_straturi(s: str, max_straturi: int = 8):
    pasi = []
    curent = s
    for _ in range(max_straturi):
        strat, rezultat = desfa(curent)
        text_rezultat = rezultat.decode("utf-8", errors="replace")
        pasi.append({"strat": strat, "rezultat": text_rezultat})
        if strat == "necunoscut":
            return rezultat, pasi
        try:
            urmator = rezultat.decode("utf-8")
        except UnicodeDecodeError:
            return rezultat, pasi
        # Un strat poate produce text imprimabil care este inca o codare.
        if ghici_strat(urmator) == "necunoscut":
            return rezultat, pasi
        if urmator == curent:
            return rezultat, pasi
        curent = urmator
    return rezultat, pasi


def sparge_xor(cale: Path):
    date = cale.read_bytes()
    rezultate = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        try:
            text = clar.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scor = sum(ch.isprintable() or ch in "\r\n\t" for ch in text)
        if text and scor / len(text) > 0.9:
            rezultate.append({"cheie": k, "text": text, "scor": scor / len(text)})
    rezultate.sort(key=lambda x: x["scor"], reverse=True)
    return rezultate


def sparge_hash(cale_hashuri: Path, wordlist: Path):
    rezultate = []
    if not cale_hashuri.exists() or not wordlist.exists():
        return rezultate
    tinte = [linie.strip().lower() for linie in cale_hashuri.read_text(errors="ignore").splitlines() if linie.strip()]
    algoritmi = {32: "md5", 40: "sha1", 64: "sha256"}
    cuvinte = [linie.strip() for linie in wordlist.read_text(encoding="latin1").splitlines()]
    for tinta in tinte:
        alg = algoritmi.get(len(tinta))
        if not alg:
            rezultate.append({"hash": tinta, "algoritm": "necunoscut", "parola": None})
            continue
        gasit = None
        for cuv in cuvinte:
            if hashlib.new(alg, cuv.encode()).hexdigest() == tinta:
                gasit = cuv
                break
        rezultate.append({"hash": tinta, "algoritm": alg, "parola": gasit})
    return rezultate


def main():
    parser = argparse.ArgumentParser(description="Decoder universal pentru Laboratorul 5")
    parser.add_argument("intrare", help="sir de decodat sau cale catre fisier")
    parser.add_argument("--fisier", action="store_true", help="citeste intrarea ca fisier")
    parser.add_argument("--xor", action="store_true", help="incearca toate cheile XOR pe un octet")
    parser.add_argument("--hashuri", action="store_true", help="verifica hashurile din probe/hashuri.txt")
    args = parser.parse_args()

    if args.xor:
        rezultate = sparge_xor(Path(args.intrare))
        print(json.dumps(rezultate, ensure_ascii=False, indent=2))
        rezultat_fisa = {"operatie": "xor", "rezultate": rezultate}
    elif args.hashuri:
        rezultate = sparge_hash(PROBE / "hashuri.txt", PROBE / "wordlist.txt")
        print(json.dumps(rezultate, ensure_ascii=False, indent=2))
        rezultat_fisa = {"operatie": "hashuri", "rezultate": rezultate}
    else:
        if args.fisier:
            raw = Path(args.intrare).read_bytes()
            intrare = raw.decode("utf-8", errors="replace")
        else:
            intrare = args.intrare
        rezultat, pasi = decode_straturi(intrare)
        try:
            text_final = rezultat.decode("utf-8")
        except UnicodeDecodeError:
            text_final = rezultat.hex()
        rezultat_fisa = {"intrare": args.intrare, "strat_final": pasi[-1]["strat"] if pasi else "necunoscut",
                         "pasi": pasi, "rezultat": text_final}
        print(json.dumps(rezultat_fisa, ensure_ascii=False, indent=2))

    FISA.parent.mkdir(parents=True, exist_ok=True)
    FISA.write_text(json.dumps(rezultat_fisa, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
