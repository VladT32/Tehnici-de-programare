import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Tetelea"
}

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