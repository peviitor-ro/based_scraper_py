import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import create_job, publish_or_update, publish_logo, show_jobs

BASE_URL = "https://hellojets.com/ro/cariere/"
LOGO_URL = "https://hellojets.com/wp-content/uploads/2024/11/art.png"
COMPANY = "HelloJets"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

_counties = GetCounty()

# All HelloJets positions are based in Bucharest
CITY = "București"
COUNTY = _counties.get_county(CITY)

response = requests.get(BASE_URL, headers=HEADERS, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

jobs = []

for link in soup.select("a"):
    if link.get_text(strip=True) != "Detalii job":
        continue

    job_link = link.get("href")
    if not job_link:
        continue

    wrapper = link.parent.parent
    title_el = wrapper.select_one("h3")
    if not title_el:
        continue

    job_title = title_el.get_text(" ", strip=True)

    jobs.append(create_job(
        job_title=job_title,
        job_link=job_link,
        company=COMPANY,
        country="Romania",
        city=[CITY],
        county=COUNTY,
    ))

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
