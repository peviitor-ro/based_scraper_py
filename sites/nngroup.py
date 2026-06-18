import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import create_job, publish_or_update, publish_logo, show_jobs


API_URL = "https://nngroup.wd3.myworkdayjobs.com/wday/cxs/nngroup/WDExternal/jobs"
BASE_URL = "https://nngroup.wd3.myworkdayjobs.com/WDExternal"
LOGO_URL = f"{BASE_URL}/assets/logo"
COMPANY = "NN Group"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

_counties = GetCounty()

ROMANIA_COUNTRY_ID = "f2e609fe92974a55a05fc1cdc2852122"

jobs = []
offset = 0

while True:
    payload = {
        "limit": 20,
        "offset": offset,
        "searchText": "",
        "appliedFacets": {"locationCountry": [ROMANIA_COUNTRY_ID]},
    }

    resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("jobPostings", [])
    if not results:
        break

    for item in results:
        job_title = item.get("title")
        external_path = item.get("externalPath")
        if not job_title or not external_path:
            continue

        job_link = f"{BASE_URL}{external_path}"

        city = item.get("locationsText")
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

    offset += len(results)
    if offset >= (data.get("total") or 0):
        break

print(f"Total jobs: {len(jobs)}", flush=True)

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
