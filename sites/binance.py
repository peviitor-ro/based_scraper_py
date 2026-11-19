import requests

from ats_common import (
    HEADERS,
    build_job,
    finalize_jobs,
    has_romania_signal,
    html_to_text,
    infer_city,
    normalize_text,
)
from getCounty import GetCounty
from utils import create_job

COMPANY = "Binance"
LOGO_URL = "https://logo.clearbit.com/binance.com"
URL = "https://boards-api.greenhouse.io/v1/boards/binance/jobs?content=true"

_counties = GetCounty()

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

jobs = []
seen_links = set()

for job in response.json().get("jobs", []):
    job_link = job.get("absolute_url")
    if not job_link or job_link in seen_links:
        continue

    title = job.get("title") or ""
    location_text = (job.get("location") or {}).get("name") or ""
    office_text = " ; ".join(
        office.get("name") or "" for office in job.get("offices") or []
    )
    locations = " ; ".join(part for part in (location_text, office_text) if part)
    description_text = html_to_text(job.get("content") or "")
    signals = [title, locations, description_text]

    if has_romania_signal(*signals):
        job_data = build_job(COMPANY, title, job_link, signals, signals)
    elif (
        "europe" in normalize_text(locations)
        or "europe" in normalize_text(title)
    ) and "remote" in normalize_text(title):
        city = infer_city(*signals)
        county = _counties.get_county(city) or [] if city else []
        job_data = create_job(
            job_title=title.strip(),
            job_link=job_link,
            company=COMPANY,
            country="Romania",
            city=city if city else [],
            county=county,
            remote=["remote"],
        )
    else:
        continue

    if not job_data:
        continue

    seen_links.add(job_link)
    jobs.append(job_data)

finalize_jobs(COMPANY, LOGO_URL, jobs)
