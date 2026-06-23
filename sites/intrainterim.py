import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty, remove_diacritics
from utils import create_job, publish_logo, publish_or_update, show_jobs, translate_city


URL = "https://www.intrainterim.ro/oferte-de-munca/romania"
BASE_URL = "https://www.intrainterim.ro"
COMPANY = "Intra Interim"
LOGO_URL = "https://www.intrainterim.ro/assets/imgs/logo-dark.png"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
}

_counties = GetCounty()
jobs = []


def normalize_city(raw_city):
    city = remove_diacritics((raw_city or "").strip())
    city = translate_city(city)
    return city.strip()


def get_county(city):
    if not city:
        return None

    counties = _counties.get_county(city)
    if not counties:
        return None
    if len(counties) == 1:
        return counties
    return None


response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

for heading in soup.select('h2 a[href^="/oferte-de-munca/romania/"]'):
    job_title = heading.get_text(" ", strip=True)
    job_link = BASE_URL + heading.get("href")

    city = None
    title_parts = job_title.split("-")
    if len(title_parts) > 1:
        city = normalize_city(title_parts[-1])

    county = get_county(city)

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


publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
