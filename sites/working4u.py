import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty, remove_diacritics
from utils import create_job, publish_logo, publish_or_update, show_jobs, translate_city


BASE_URL = "https://www.working4u.ro"
LIST_URL = f"{BASE_URL}/locuri-de-munca/"
LOGO_URL = "https://www.working4u.ro/wp-content/uploads/2023/02/logowhite.svg"
COMPANY = "Working4U"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}
CITY_OVERRIDES = {
    "bucuresti": ("Bucuresti", ["Bucuresti"]),
    "cluj napoca": ("Cluj-Napoca", ["Cluj"]),
    "brasov": ("Brasov", ["Brasov"]),
    "pitesti": ("Pitesti", ["Arges"]),
    "dascalu": ("Dascalu", ["Ilfov"]),
    "snagov": ("Snagov", ["Ilfov"]),
    "pantelimon": ("Pantelimon", ["Ilfov"]),
    "popesti-leordeni": ("Popesti-Leordeni", ["Ilfov"]),
    "branesti": ("Branesti", ["Ilfov"]),
    "ciorogarla": ("Ciorogarla", ["Ilfov"]),
    "crevedia": ("Crevedia", ["Dambovita"]),
}

_counties = GetCounty()
session = requests.Session()
session.headers.update(HEADERS)
jobs = []
seen_links = set()


def normalize_location_token(token):
    value = remove_diacritics((token or "").strip())
    value = value.replace(".", " ")
    value = " ".join(value.split())
    return value


def get_city_and_county(token):
    normalized = normalize_location_token(token)
    lowered = normalized.lower()

    if lowered in {"if", "ilfov", "db", "dambovita", "national", "remote", "relocare", "deplasare", "ue", "strainatate"}:
        return None, None

    if lowered in CITY_OVERRIDES:
        return CITY_OVERRIDES[lowered]

    city = translate_city(normalized)
    counties = _counties.get_county(city)
    if counties and len(counties) == 1:
        return city, counties

    return city, None


def extract_locations(job_link):
    response = session.get(job_link, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    location_terms = []
    for spec in soup.select(".awsm-job-specification-item"):
        label = spec.select_one(".awsm-job-specification-label")
        if not label:
            continue
        if "Job Locations" in label.get_text(" ", strip=True):
            location_terms = [
                term.get_text(" ", strip=True)
                for term in spec.select(".awsm-job-specification-term")
            ]
            break

    if not location_terms:
        return None, None

    cities = []
    counties = []

    for token in location_terms:
        city, county = get_city_and_county(token)
        if not city or city in cities:
            continue
        cities.append(city)
        if county:
            for item in county:
                if item not in counties:
                    counties.append(item)

    if not cities:
        return None, None
    if len(cities) == 1:
        return cities[0], counties or None

    return cities, counties or None


page = 1
while True:
    page_url = LIST_URL if page == 1 else f"{LIST_URL}?paged={page}"
    response = session.get(page_url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    page_jobs = 0
    for heading in soup.select('h2 a[href*="/jobs/"]'):
        job_title = heading.get_text(" ", strip=True)
        job_link = heading.get("href")

        if not job_link or job_link in seen_links:
            continue

        city, county = extract_locations(job_link)
        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=COMPANY,
                country="Romania",
                city=city,
                county=county,
            )
        )
        seen_links.add(job_link)
        page_jobs += 1

    if page_jobs == 0:
        break

    page += 1


publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
