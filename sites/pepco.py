from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
import re

_counties = GetCounty()
company = "Pepco"

BASE_URL = "https://careers.pepco.eu"
SEARCH_URL = f"{BASE_URL}/PepcoRomania/search/?createNewAlert=false&q=&locationsearch=Romania&optionsFacetsDD_customfield1="

scraper = Scraper()

jobs = []

page = 0

while True:
    scraper.get_from_url(f"{SEARCH_URL}&page={page}", verify=False, timeout=30)

    rows = scraper.select("tr.data-row")
    if not rows:
        break

    for row in rows:
        link = row.select_one("a.jobTitle-link")
        if not link:
            continue

        job_title = link.get_text(strip=True)
        job_link = link.get("href", "")
        if job_link and not job_link.startswith("http"):
            job_link = BASE_URL + job_link

        location_el = row.select_one(".jobLocation")
        location_text = location_el.get_text(strip=True) if location_el else ""

        # Location format: "București, RO, 014052"
        parts = [p.strip() for p in location_text.split(",")]
        city = ""
        if parts:
            city = translate_city(parts[0])
        county = _counties.get_county(city) if city else ""
        if not county and city and " " in city:
            county = _counties.get_county(city.replace(" ", "-"))

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city=city,
                county=county,
            )
        )

    # Check pagination: look for "Page X of Y"
    pagination = scraper.select_one(".pagination")
    next_page_exists = False
    if pagination:
        text = pagination.get_text(" ", strip=True)
        match = re.search(r"Page\s+(\d+)\s+of\s+(\d+)", text)
        if match:
            current_page = int(match.group(1))
            total_pages = int(match.group(2))
            if current_page < total_pages:
                next_page_exists = True

    if not next_page_exists:
        break

    page += 1

publish_or_update(jobs)
publish_logo(
    company,
    "https://careers.pepco.eu/favicon.ico",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")