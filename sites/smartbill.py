import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

URL = "https://www.smartbill.ro/cariere"
LOGO_URL = "https://www.smartbill.ro/img/sb-logo-19-ani.svg"
COMPANY = "SmartBill"

scraper = Scraper()
scraper.get_from_url(URL, "HTML")

finalJobs = []
idx = 0

for job_tag in scraper.select("#jobs a[href]"):
    job_link = job_tag.get("href", "")
    name_el = job_tag.select_one(".name")
    place_el = job_tag.select_one(".place")

    if not name_el or not job_link:
        continue

    job_title = name_el.get_text(strip=True)
    place = place_el.get_text(strip=True) if place_el else ""

    city = translate_city(place)
    counties = _counties.get_county(city) or []

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": COMPANY,
        "country": "Romania",
        "city": [city] if city else [],
        "county": counties,
    })
    idx += 1

publish_or_update(finalJobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(finalJobs)
