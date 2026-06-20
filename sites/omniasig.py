import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import create_job, publish_or_update, publish_logo, show_jobs


API_URL = "https://omniasig.mingle.ro/api/boards/careers-page/jobs"
BASE_URL = "https://omniasig.mingle.ro/ro/apply"
LOGO_URL = "https://omniasig.ro/sites/default/files/2020-11/OMNIASIG.svg"
COMPANY = "OMNIASIG"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

_counties = GetCounty()

jobs = []
page = 0

while True:
    params = {
        "company": "omniasig",
        "page": page,
        "pageSize": 100,
    }

    resp = requests.get(API_URL, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("data", {}).get("results", [])
    pagination = data.get("data", {}).get("pagination", {})

    if not results:
        break

    for item in results:
        job_title = item.get("title")
        job_uid = item.get("uid")
        if not job_title or not job_uid:
            continue

        job_link = f"{BASE_URL}/{job_uid}"

        locations = item.get("locations", [])
        city = locations[0]["label"] if locations else None
        if not city:
            continue

        county = _counties.get_county(city) or []

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=COMPANY,
                country="Romania",
                city=[city],
                county=county,
            )
        )

    if not pagination.get("hasNext"):
        break

    page += 1

print(f"Total jobs: {len(jobs)}", flush=True)

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
