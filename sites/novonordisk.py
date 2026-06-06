import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import create_job, publish_or_update, publish_logo, show_jobs, translate_city


API_URL = "https://www.novonordisk.ro/bin/nncorp/careersearch?keyword=&country=Romania&category=&locale=ro"
LOGO_URL = "https://www.novonordisk.ro/content/dam/nncorp/global/en/ogp/nn-logo.png"
COMPANY = "Novo Nordisk"
JOB_AD_BASE = "https://www.novonordisk.ro/ro/careers/find-a-job/job-ad"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.novonordisk.ro/ro/careers/find-a-job/career-search-results.html",
}

_counties = GetCounty()

response = requests.get(API_URL, headers=HEADERS, timeout=30)
response.raise_for_status()
data = response.json()

jobs = []
for job in data.get("data", {}).get("jobs", []):
    job_title = job.get("jobTitle", "").strip()
    job_id = job.get("jobId", "").strip()
    if not job_title or not job_id:
        continue

    job_link = f"{JOB_AD_BASE}.{job_id}.html"
    city = translate_city(job.get("jobCity", {}).get("label", ""))
    counties = _counties.get_county(city) if city else []

    jobs.append(create_job(
        job_title=job_title,
        job_link=job_link,
        company=COMPANY,
        country="Romania",
        city=[city] if city else [],
        county=counties,
    ))

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
