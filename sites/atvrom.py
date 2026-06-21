import sys
from pathlib import Path

import cloudscraper
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import (
    create_job,
    publish_or_update,
    publish_logo,
    show_jobs,
    translate_city,
)

BASE_URL = "https://www.atvrom.ro/cariere"
LOGO_URL = "https://www.atvrom.ro/template/img/logo.svg"
COMPANY = "ATVRom"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

_counties = GetCounty()

scraper = cloudscraper.create_scraper()
response = scraper.get(BASE_URL, headers=HEADERS, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

careers_list = soup.find("div", class_="careers-list")
if not careers_list:
    publish_or_update([])
    publish_logo(COMPANY, LOGO_URL)
    show_jobs([])
    sys.exit(0)

job_rows = careers_list.find_all(
    "div",
    class_=lambda c: c and any(x in c for x in ["mt-4", "mt-5"]),
    recursive=False,
)

jobs = []
idx = 0

for row in job_rows:
    status_el = row.find("p", class_="text-danger")
    status = status_el.get_text(strip=True) if status_el else ""

    if "disponibil" not in status.lower():
        continue

    title = ""
    for h2 in row.find_all("h2"):
        t = h2.get_text(strip=True)
        if t and t.lower() != "vezi detalii":
            title = t
            break

    if not title:
        continue

    locations = []
    for td in row.find_all("td"):
        label_p = td.find("p")
        if label_p and "locatii" in label_p.get_text(strip=True).lower():
            next_td = td.find_next_sibling("td")
            if next_td:
                loc_text = next_td.get_text(strip=True)
                locations = [loc.strip() for loc in loc_text.split(",")]
            break

    for location in locations:
        city = translate_city(location)
        county = _counties.get_county(city) or []

        jobs.append(create_job(
            job_title=title,
            job_link=f"{BASE_URL}#{idx}",
            company=COMPANY,
            country="Romania",
            city=[city] if city else [],
            county=county,
        ))

    idx += 1

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
