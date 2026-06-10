import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

BASE_URL = "https://cariere.kaufland.ro"
API_URL = f"{BASE_URL}/api/v1/search"
LOGO_URL = f"{BASE_URL}/content/download/13399/icon/kaufland-logo.svg"
COMPANY = "Kaufland"

scraper = Scraper()

finalJobs = []
page = 1

while True:
    params = {
        "general": f'{{"page":{page},"results_per_page":100,"sort_field":"","sort_order":"asc"}}',
    }

    scraper.get_from_url(API_URL, "JSON", params=params)
    data = scraper.markup

    jobs = data.get("jobs", [])
    if not jobs:
        break

    for job in jobs:
        job_title = job.get("title")
        job_link = BASE_URL + job.get("jobDetailUrl", "")

        location = job.get("location", {})
        city = translate_city(location.get("city", ""))
        country = location.get("country", "Romania")

        counties = _counties.get_county(city) or []

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": COMPANY,
            "country": "Romania",
            "city": [city],
            "county": counties,
        })

    meta = data.get("meta", {})
    total_count = meta.get("totalCount", 0)
    results_per_page = meta.get("resultsPerPage", 100)
    page_count = (total_count + results_per_page - 1) // results_per_page
    page += 1
    if page > page_count:
        break

publish_or_update(finalJobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(finalJobs)
