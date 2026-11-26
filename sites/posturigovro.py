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
ALL_JOBS_URL = f"{BASE_URL}/toate-posturile/"
LOGO_URL = "https://posturi.gov.ro/wp-content/uploads/2022/01/Logo2-1-412x83.png"
COMPANY = "posturi.gov.ro"
PUBLISH_BATCH_SIZE = 250
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


def get_city(employer, county, explicit_city=None):
    if not county:
        return None

    county_norm = _norm(county.strip())
    if county_norm == "bucuresti":
        return "București"

    city = explicit_city
    if not city and employer:
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
    url = f"{ALL_JOBS_URL}?pg_page={page}"
    print(f"Page {page}: {url}", flush=True)

    try:
        resp = requests.get(ALL_JOBS_URL, params={"pg_page": page}, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error on page {page}: {e}", flush=True)
        break

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("a.pg-card.pg-card--link")

    if not cards:
        print(f"No job cards on page {page}, stopping.", flush=True)
        break

    for card in cards:
        title_el = card.select_one(".pg-card-h")
        ang_el = card.select_one(".pg-card-inst")
        location_el = card.select_one(".pg-card-city span")

        if not title_el or not location_el:
            continue

        job_title = title_el.get("title") or title_el.get_text(strip=True)
        job_link = card["href"]
        if job_link.startswith("/"):
            job_link = BASE_URL + job_link

        employer = ang_el.get_text(strip=True) if ang_el else None
        location = location_el.get_text(" ", strip=True)
        parts = [part.strip() for part in location.split(",")]
        county = parts[-1]
        if _norm(county) not in COUNTY_NAMES_NORM and len(parts) > 1:
            county = parts[0]
        explicit_city = parts[0] if len(parts) > 1 and _norm(parts[0]) != _norm(county) else None

        city = get_city(employer, county, explicit_city)
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

    next_link = soup.select_one(".pg-arc-pagi a.next.page-numbers")
    if not next_link:
        break

    page += 1

print(f"Total jobs: {len(jobs)}", flush=True)

for start in range(0, len(jobs), PUBLISH_BATCH_SIZE):
    publish_or_update(jobs[start : start + PUBLISH_BATCH_SIZE])

publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
