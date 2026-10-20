# PARTEA 1 - IMPORTURI

# Ex 1

import requests
print(requests.__version__)

import urllib.request


# Ex 2

import requests

response = requests.get("https://cybercor.org", timeout=10)
print(response.status_code)

from requests import get

response = get("https://cybercor.org", timeout=10)
print(response.status_code)


#  3

import requests as rq

response = rq.get("https://cybercor.org", timeout=10)
print(response.status_code)


# Ex 4

import urllib.request

response = urllib.request.urlopen("https://cybercor.org")
print(response.status)

continut = response.read().decode("utf-8")
print(continut[:200])


# Ex 5

import requests

print(dir(requests))

# Exemple:
# get - functie
# Session - clasa
# models - modul


# Ex 6

import requests

help(requests.get)

response = requests.get("https://cybercor.org", timeout=10)
print(response.status_code)


# Ex 7

import requests
import time

start = time.perf_counter()

response = requests.get("https://cybercor.org", timeout=10)

stop = time.perf_counter()

timp = stop - start

print("Timp perf_counter:", timp)
print("Timp response.elapsed:", response.elapsed)


# Ex 8

try:
    import bs4
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")



# PARTEA 2 - METODE SI ATRIBUTE


import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Ex 9

response = requests.get(BASE_URL, timeout=TIMEOUT)

print(response.status_code)   # atribut
print(response.ok)            # atribut
print(response.url)           # atribut
print(response.encoding)      # atribut


# Ex 10

response = requests.get(BASE_URL, timeout=TIMEOUT)

try:
    response.raise_for_status()
    print("Pagina exista.")
except requests.HTTPError:
    print("A aparut o eroare HTTP.")

try:
    response = requests.get(
        BASE_URL + "/this-page-does-not-exist",
        timeout=TIMEOUT
    )
    response.raise_for_status()
except requests.HTTPError:
    print("Pagina nu exista.")


# Ex 11

response = requests.get(BASE_URL, timeout=TIMEOUT)

for nume, valoare in response.headers.items():
    print(nume + ": " + valoare)


# Ex 12

response = requests.get(BASE_URL, timeout=TIMEOUT)

print(response.headers.get("Server", "lipsește"))
print(response.headers.get("Content-Type", "lipsește"))
print(response.headers.get("content-type", "lipsește"))


# Ex 13

response = requests.get(BASE_URL, timeout=TIMEOUT)

numar = response.text.lower().count("cyber")

print(numar)


# Ex 14

response = requests.get(BASE_URL, timeout=TIMEOUT)

html = response.text

start = html.find("<title>") + len("<title>")
end = html.find("</title>")

titlu = html[start:end].strip()

print(titlu)


# Ex 15

response = requests.get(BASE_URL, timeout=TIMEOUT)

lines = response.text.splitlines()

print("Numar linii:", len(lines))
print("Cea mai lunga linie:", len(max(lines, key=len)))


# Ex 16

response = requests.get(BASE_URL, timeout=TIMEOUT)

if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")


# Ex 17

response = requests.get(
    "http://cybercor.org",
    timeout=TIMEOUT
)

for redirectionare in response.history:
    print(redirectionare.status_code, redirectionare.url)

print("URL final:", response.url)


# Ex 18

response_head = requests.head(
    BASE_URL,
    timeout=TIMEOUT
)

response_get = requests.get(
    BASE_URL,
    timeout=TIMEOUT
)

print("HEAD:", len(response_head.content))
print("GET:", len(response_get.content))


# Ex 19

response = requests.get(BASE_URL, timeout=TIMEOUT)

if response.cookies:
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)
else:
    print("Niciun cookie setat.")


# Ex 20

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Tetelea"
})

response = session.get(
    ECHO_URL + "/headers",
    timeout=TIMEOUT
)

print(response.json())



# PARTEA 3 - PROPRIILE FUNCTII


import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Ex 21

def fetch(url):
    """Returneaza obiectul raspuns."""
    response = requests.get(url, timeout=TIMEOUT)
    return response


response = fetch(BASE_URL)
print(response.status_code)


# Ex 22

def get_status(url):
    """Returneaza codul de stare HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


print(get_status(BASE_URL))
time.sleep(1)

print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)

print(get_status(BASE_URL + "/sitemap.xml"))


# Ex 23

def fetch(url, timeout=10):
    """Descarca pagina si returneaza raspunsul."""
    response = requests.get(url, timeout=timeout)
    return response


response1 = fetch(BASE_URL)
response2 = fetch(BASE_URL, timeout=3)

print(response1.status_code)
print(response2.status_code)


# Ex 24

def get_title(html):
    """Returneaza titlul paginii HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")

    return html[start:end].strip()


response = requests.get(BASE_URL, timeout=TIMEOUT)
print(get_title(response.text))


# Ex 25

def get_title(html):
    """Returneaza titlul paginii HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")

    return html[start:end].strip()


help(get_title)


# Ex 26

def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


print(get_status(123))


# Ex 27

def page_exists(url):
    """Verifica daca pagina exista."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


print(page_exists(BASE_URL))
print(page_exists(
    "https://this-domain-does-not-exist.invalid"
))


# Ex 28

def check_paths(base, paths):
    """Returneaza codurile de stare pentru mai multe cai."""
    rezultate = {}

    for path in paths:
        response = requests.get(base + path, timeout=TIMEOUT)
        rezultate[path] = response.status_code
        time.sleep(1)

    return rezultate


paths = ["/", "/robots.txt", "/sitemap.xml"]

print(check_paths(BASE_URL, paths))


# Ex 29

def get_header(url, name, default="lipsește"):
    """Returneaza valoarea unui antet."""
    response = requests.get(url, timeout=TIMEOUT)

    return response.headers.get(name, default)


print(get_header(BASE_URL, name="Server"))


# Ex 30

def security_headers(url):
    """Verifica antetele de securitate."""
    response = requests.get(url, timeout=TIMEOUT)

    antete = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    rezultate = {}

    for antet in antete:
        rezultate[antet] = antet in response.headers

    return rezultate

print(security_headers(BASE_URL))


# Ex 31

def score_headers(results):
    """Calculeaza scorul antetelor de securitate."""
    total = len(results)
    gasite = 0

    for rezultat in results.values():
        if rezultat:
            gasite += 1

    return str(gasite) + "/" + str(total)

print(score_headers(security_headers(BASE_URL)))


# Ex 32

def fetch_robots(base):
    """Returneaza continutul robots.txt."""
    response = requests.get(base + "/robots.txt", timeout=TIMEOUT)

    if response.status_code == 200:
        return response.text

    return None

def disallowed_paths(robots_text):
    """Returneaza toate valorile Disallow."""
    if robots_text is None:
        return []

    rezultate = []

    for linie in robots_text.splitlines():
        if linie.startswith("Disallow:"):
            cale = linie.split(":", 1)[1].strip()
            rezultate.append(cale)

    return rezultate

robots = fetch_robots(BASE_URL)
print(disallowed_paths(robots))


# Ex 33

def response_times(*urls):
    """Returneaza timpul de raspuns pentru fiecare URL."""
    rezultate = {}

    for url in urls:
        start = time.perf_counter()

        requests.get(url, timeout=TIMEOUT)

        stop = time.perf_counter()

        rezultate[url] = stop - start

    return rezultate


print(response_times(
    BASE_URL,
    BASE_URL + "/robots.txt"
))

# Ex 34

def log(message, **details):
    """Afiseaza mesajul si detaliile."""
    print(message, end="")

    for nume, valoare in details.items():
        print(" | " + nume + "=" + str(valoare), end="")

    print()

log(
    "verificat",
    url=BASE_URL,
    status=200
)



# PARTEA 4 - ALTE MODULE DIN BIBLIOTECA STANDARD

# Ex 35

from urllib.parse import urlparse

url = "https://cybercor.org/path?x=1#top"

rezultat = urlparse(url)

print("scheme:", rezultat.scheme)
print("netloc:", rezultat.netloc)
print("path:", rezultat.path)
print("query:", rezultat.query)
print("fragment:", rezultat.fragment)


# Ex 36

from urllib.parse import urljoin

BASE_URL = "https://cybercor.org"

print(urljoin(BASE_URL, "/about"))
print(urljoin(BASE_URL, "contact.html"))
print(urljoin(BASE_URL, "../index.html"))


# Ex 37

import re

def extract_links(html):
    """Returneaza legaturile fara duplicate."""
    links = re.findall(r'href="([^"]+)"', html)

    rezultate = []

    for link in links:
        if link not in rezultate:
            rezultate.append(link)

    return rezultate


response = requests.get(BASE_URL, timeout=TIMEOUT)

print(extract_links(response.text))


# Ex 38

from urllib.parse import urljoin, urlparse

def split_links(links, domain):
    """Imparte linkurile in interne si externe."""
    interne = []
    externe = []

    for link in links:
        link_complet = urljoin(domain, link)
        domeniu = urlparse(link_complet).netloc

        if domeniu == urlparse(domain).netloc:
            interne.append(link_complet)
        else:
            externe.append(link_complet)

    return interne, externe


response = requests.get(BASE_URL, timeout=TIMEOUT)

links = extract_links(response.text)

interne, externe = split_links(links, BASE_URL)

print("Interne:", interne)
print("Externe:", externe)


# Ex 39

from html.parser import HTMLParser

class ImageFinder(HTMLParser):

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src is not None:
                self.images.append(src)


test_html = """
<html><body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fără src">
<img src="https://cdn.example.com/banner.webp" />
<a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)

print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
]

print("Testul a trecut!")

response = requests.get(BASE_URL, timeout=TIMEOUT)

finder = ImageFinder()
finder.feed(response.text)

print(len(finder.images), "imagini gasite")

for src in finder.images:
    print(src)


# Ex 40

import hashlib

def page_fingerprint(url):
    """Returneaza amprenta SHA-256 a paginii."""
    response = requests.get(url, timeout=TIMEOUT)

    return hashlib.sha256(response.content).hexdigest()

print(page_fingerprint(BASE_URL))
print(page_fingerprint(BASE_URL))


# Ex 41

import json

response = requests.get(BASE_URL, timeout=TIMEOUT)

with open("headers.json", "w", encoding="utf-8") as file:
    json.dump(
        dict(response.headers),
        file,
        indent=2
    )

with open("headers.json", "r", encoding="utf-8") as file:
    headers = json.load(file)


print(headers.get("Server"))


# Ex 42

import socket

def resolve(hostname):
    """Returneaza adresa IP a domeniului."""
    return socket.gethostbyname(hostname)


print(resolve("cybercor.org"))


# Ex 43

import ssl
import socket
from datetime import datetime


def cert_days_left(hostname):
    """Returneaza numarul de zile pana la expirarea certificatului."""

    context = ssl.create_default_context()

    sock = socket.create_connection(
        (hostname, 443)
    )

    secure_sock = context.wrap_socket(
        sock,
        server_hostname=hostname
    )

    certificat = secure_sock.getpeercert()

    secure_sock.close()

    data_expirare = certificat["notAfter"]

    timestamp = ssl.cert_time_to_seconds(data_expirare)

    data_expirare = datetime.fromtimestamp(timestamp)
    data_curenta = datetime.now()

    diferenta = data_expirare - data_curenta

    return diferenta.days


print(cert_days_left("cybercor.org"))



# PARTEA 5 - PROPRIUL MODUL

# Ex 44

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


def fetch(url):
    """Descarca pagina si returneaza raspunsul."""
    response = requests.get(url, timeout=TIMEOUT)
    return response


def get_status(url):
    """Returneaza codul de stare HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


def get_title(html):
    """Returneaza titlul paginii."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")

    return html[start:end].strip()


def security_headers(url):
    """Verifica antetele de securitate."""
    response = requests.get(url, timeout=TIMEOUT)

    antete = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    rezultate = {}

    for antet in antete:
        rezultate[antet] = antet in response.headers

    return rezultate


# main.py

import webtools

print(
    webtools.get_title(
        webtools.fetch(webtools.BASE_URL).text
    )
)



# Ex 45


import webtools
from webtools import get_title, security_headers

print(get_title(webtools.fetch(BASE_URL).text))
print(security_headers(BASE_URL))

# Daca main.py ar avea propria functie get_title,
# aceasta ar putea ascunde functia importata.



# Ex 46


if __name__ == "__main__":
    print(
        "Autotest:",
        get_status("https://cybercor.org")
    )



# Ex 47

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Tetelea"
}


def fetch(url):
    """Descarca pagina folosind User-Agent personalizat."""
    response = requests.get(
        url,
        headers=DEFAULT_HEADERS,
        timeout=TIMEOUT
    )

    return response




from webtools import DEFAULT_HEADERS

print(DEFAULT_HEADERS)



# Ex 48


import argparse
import webtools

parser = argparse.ArgumentParser()

parser.add_argument("url")

args = parser.parse_args()

url = args.url

response = webtools.fetch(url)

print(webtools.get_status(url))
print(webtools.get_title(response.text))



# Ex 49

import csv
from datetime import datetime

def save_report(paths_result):
    """Salveaza rezultatele intr-un fisier CSV."""

    with open(
        "report.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "path",
            "status",
            "checked_at"
        ])

        for path, status in paths_result.items():
            writer.writerow([
                path,
                status,
                datetime.now().isoformat()
            ])


results = webtools.check_paths(
    BASE_URL,
    ["/", "/robots.txt", "/sitemap.xml"]
)

save_report(results)



# Ex 50

import json
import requests
from urllib.parse import urlparse
from datetime import datetime


def site_report(url):
    """Genereaza raportul complet al unui site."""

    response = requests.get(
        url,
        timeout=TIMEOUT
    )

    status = response.status_code
    final_url = response.url

    title = get_title(response.text)

    hostname = urlparse(final_url).hostname
    ip = resolve(hostname)

    http_url = "http://" + hostname

    redirect_response = requests.get(
        http_url,
        timeout=TIMEOUT
    )

    redirectari = []

    for redirectionare in redirect_response.history:
        redirectari.append(
            str(redirectionare.status_code)
            + " -> "
            + redirectionare.headers.get(
                "Location",
                ""
            )
        )

    security = security_headers(url)
    security_score = score_headers(security)

    certificat = cert_days_left(hostname)

    links = extract_links(response.text)

    interne, externe = split_links(
        links,
        url
    )

    robots = fetch_robots(url)
    disallowed = disallowed_paths(robots)

    raport = {
        "status": status,
        "url_final": final_url,
        "titlu": title,
        "ip": ip,
        "redirectionari": redirectari,
        "scor_securitate": security_score,
        "certificat_zile": certificat,
        "legaturi_interne": len(interne),
        "legaturi_externe": len(externe),
        "cai_interzise": disallowed
    }

    print("=== Raport site:", url, "===")
    print("Cod de stare:", status)
    print("Titlu:", title)
    print("Adresa IP:", ip)
    print("Redirectionari:", redirectari)
    print("Scor securitate:", security_score)
    print("Certificat:", certificat, "zile ramase")
    print(
        "Legaturi:",
        len(interne),
        "interne,",
        len(externe),
        "externe"
    )
    print("Cai interzise:", disallowed)

    with open(
        "report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            raport,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("Salvat in report.json")

    return raport