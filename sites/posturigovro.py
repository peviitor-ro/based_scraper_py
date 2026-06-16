import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty, remove_diacritics
from utils import create_job, publish_or_update, publish_logo, show_jobs


LQ = "\u201e"
RQ = "\u201d"

BASE_URL = "https://posturi.gov.ro"
LOGO_URL = "https://posturi.gov.ro/wp-content/uploads/2022/01/Logo2-1-412x83.png"
COMPANY = "posturi.gov.ro"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

_counties = GetCounty()

# Normalized county → county seat lookup (lookup via _norm)
COUNTY_SEATS_RAW = {
    "Alba": "Alba Iulia",
    "Arad": "Arad",
    "Arges": "Pitești",
    "Argeș": "Pitești",
    "Bacău": "Bacău",
    "Bihor": "Oradea",
    "Bistrița-Năsăud": "Bistrița",
    "Bistrita-Nasaud": "Bistrița",
    "Botoșani": "Botoșani",
    "Botosani": "Botoșani",
    "Brăila": "Brăila",
    "Braila": "Brăila",
    "Brașov": "Brașov",
    "Brasov": "Brașov",
    "București": "București",
    "Bucuresti": "București",
    "Buzău": "Buzău",
    "Buzau": "Buzău",
    "Călărași": "Călărași",
    "Calarasi": "Călărași",
    "Caraș-Severin": "Reșița",
    "Caras-Severin": "Reșița",
    "Cluj": "Cluj-Napoca",
    "Constanța": "Constanța",
    "Constanta": "Constanța",
    "Covasna": "Sfântu Gheorghe",
    "Dâmbovița": "Târgoviște",
    "Dambovita": "Târgoviște",
    "Dolj": "Craiova",
    "Galați": "Galați",
    "Galati": "Galați",
    "Giurgiu": "Giurgiu",
    "Gorj": "Târgu Jiu",
    "Harghita": "Miercurea Ciuc",
    "Hunedoara": "Deva",
    "Ialomița": "Slobozia",
    "Ialomita": "Slobozia",
    "Iași": "Iași",
    "Iasi": "Iași",
    "Ilfov": "Buftea",
    "Maramureș": "Baia Mare",
    "Maramures": "Baia Mare",
    "Mehedinți": "Drobeta-Turnu Severin",
    "Mehedinti": "Drobeta-Turnu Severin",
    "Mureș": "Târgu Mureș",
    "Mureş": "Târgu Mureș",
    "Mures": "Târgu Mureș",
    "Neamț": "Piatra Neamț",
    "Neamt": "Piatra Neamț",
    "Olt": "Slatina",
    "Prahova": "Ploiești",
    "Sălaj": "Zalău",
    "Salaj": "Zalău",
    "Satu Mare": "Satu Mare",
    "Sibiu": "Sibiu",
    "Suceava": "Suceava",
    "Teleorman": "Alexandria",
    "Timiș": "Timișoara",
    "Timis": "Timișoara",
    "Tulcea": "Tulcea",
    "Vâlcea": "Râmnicu Vâlcea",
    "Valcea": "Râmnicu Vâlcea",
    "Vaslui": "Vaslui",
    "Vrancea": "Focșani",
}

def _norm(text):
    return remove_diacritics(text.lower())


COUNTY_NAMES_NORM = {_norm(k): v for k, v in COUNTY_SEATS_RAW.items()}


def _county_seat(county):
    return COUNTY_NAMES_NORM.get(_norm(county.strip()), county.strip())


def get_city(employer, county):
    if not county:
        return None

    county_norm = _norm(county.strip())
    if county_norm == "bucuresti":
        return "București"

    city = None
    if employer:
        text = employer.replace(LQ, "").replace(RQ, "").replace('"', "")

        parts = text.split(",")
        for part in reversed(parts):
            candidate = part.strip()
            if re.match(r"jude[țt]ul", candidate, re.IGNORECASE):
                continue
            words = [w for w in candidate.split() if w not in ("IS", "SA", "SRL")]
            if words:
                last = words[-1].strip(".,;:()")
                if len(last) > 2:
                    city = last
                    break

    if city:
        if _norm(city) == county_norm and county_norm in COUNTY_NAMES_NORM:
            city = None

    if city:
        resolved = _counties.get_county(city)
        if not resolved or not any(_norm(c) == county_norm for c in resolved):
            city = None

    if not city:
        city = _county_seat(county)

    return city


jobs = []
page = 1

while True:
    url = BASE_URL if page == 1 else f"{BASE_URL}/page/{page}/"
    print(f"Page {page}: {url}", flush=True)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error on page {page}: {e}", flush=True)
        break

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("article.box")

    if not articles:
        print(f"No articles on page {page}, stopping.", flush=True)
        break

    for article in articles:
        link_el = article.select_one("li.title div.title a.permalink")
        ang_el = article.select_one("div.angajator")
        county_el = article.select_one("li.locatie div.locatie a")

        if not link_el or not county_el:
            continue

        job_title = link_el.get_text(strip=True)
        job_link = link_el["href"]
        if job_link.startswith("/"):
            job_link = BASE_URL + job_link

        employer = ang_el.get_text(strip=True) if ang_el else None
        county = county_el.get_text(strip=True)

        city = get_city(employer, county)
        resolved = _counties.get_county(city) or [county]

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=COMPANY,
                country="Romania",
                city=[city],
                county=resolved,
            )
        )

    next_link = soup.select_one(".ast-pagination a.next.page-numbers")
    if not next_link:
        break

    page += 1

print(f"Total jobs: {len(jobs)}", flush=True)

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
