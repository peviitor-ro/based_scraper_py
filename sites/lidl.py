import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

import json as _json

BASE_URL = "https://cariere.lidl.ro"
API_URL = f"{BASE_URL}/api/v1/search"
LOGO_URL = f"{BASE_URL}/assets-lica/logo.svg"
COMPANY = "Lidl"

scraper = Scraper()

finalJobs = []
page = 1
page_size = 20

while True:
    general = _json.dumps({"page": page, "resultsPerPage": page_size})
    params = {"general": general}

    scraper.get_from_url(API_URL, "JSON", params=params)
    data = scraper.markup

    jobs = data.get("jobs", [])
    if not jobs:
        break

    meta = data.get("meta", {})
    total_count = meta.get("totalCount", 0)

    for job in jobs:
        job_title = job.get("title")
        job_link = job.get("jobDetailUrl") or (BASE_URL + job.get("url", ""))

        location = job.get("location", {})
        city = translate_city(location.get("city", ""))

        counties = _counties.get_county(city) or []

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": COMPANY,
            "country": "Romania",
            "city": [city],
            "county": counties,
        })

    page += 1
    if (page - 1) * page_size >= total_count:
        break

try:
    publish_or_update(finalJobs)
except Exception as e:
    print(f"Failed to publish jobs: {e}")

publish_logo(COMPANY, LOGO_URL)
show_jobs(finalJobs)
