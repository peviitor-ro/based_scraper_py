import requests

from ats_common import HEADERS, build_job, finalize_jobs, html_to_text

COMPANY = "Airalo"
LOGO_URL = "https://logo.clearbit.com/airalo.com"
URL = "https://api.lever.co/v0/postings/airalo?mode=json"

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

jobs = []
seen_links = set()

for job in response.json():
    job_link = job.get("hostedUrl")
    if not job_link or job_link in seen_links:
        continue

    categories = job.get("categories") or {}
    all_locations = " ; ".join(categories.get("allLocations") or [])
    location_text = categories.get("location") or ""
    description_text = html_to_text(job.get("description") or "")
    salary_text = job.get("salaryDescriptionPlain") or ""

    job_data = build_job(
        COMPANY,
        job.get("text") or "",
        job_link,
        [location_text, all_locations, salary_text, description_text],
        [job.get("workplaceType") or "", description_text],
    )
    if not job_data:
        continue

    seen_links.add(job_link)
    jobs.append(job_data)

finalize_jobs(COMPANY, LOGO_URL, jobs)
