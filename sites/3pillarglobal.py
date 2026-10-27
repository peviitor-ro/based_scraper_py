import requests
from utils import publish_or_update, publish_logo, show_jobs

url = "https://3pillar.darwinbox.com/ms/candidateapi/job/alljobs"
company = {"company": "3PillarGlobal"}
logo = "https://i.imgur.com/SM5d3eE.png"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
})

try:
    session.get("https://3pillar.darwinbox.com/ms/candidatev2/main/careers/allJobs", timeout=30)
except Exception:
    pass

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": session.headers.get("User-Agent"),
    "Origin": "https://3pillar.darwinbox.com",
    "Referer": "https://3pillar.darwinbox.com/ms/candidatev2/main/careers/allJobs",
    "X-Requested-With": "XMLHttpRequest",
}

payload = {
    "companyId": "main",
    "page": 1,
    "sort_option": "new",
    "limit": 99,
    "department": [],
    "location": [],
    "work_mode": [],
    "capabilities": [],
    "job_tags": [],
    "functional_area": [],
    "country": ["Romania"],
    "legal_entities": [],
    "count": 1,
}

final_jobs = []

try:
    response = session.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"Failed to fetch jobs from Darwinbox API: {e}")
    data = {}

jobs = data.get("jobs") or data.get("data") or data.get("allJobs") or []
if isinstance(jobs, dict):
    jobs = jobs.get("jobs") or jobs.get("data") or []

for job in jobs:
    if not isinstance(job, dict):
        continue
    job_title = job.get("job_title") or job.get("jobTitle") or job.get("title") or ""
    job_link = job.get("job_link") or job.get("jobLink") or job.get("apply_url") or job.get("url") or ""
    if not job_link:
        job_id = job.get("job_id") or job.get("jobId") or job.get("internal_job_code")
        if job_id:
            job_link = f"https://3pillar.darwinbox.com/ms/candidatev2/main/careers/jobDetails/{job_id}"
    location = job.get("location") or job.get("city") or "Cluj-Napoca"
    country = "Romania"
    city = "Cluj-Napoca"
    county = "Cluj"

    final_jobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": country,
        "city": city,
        "county": county,
        "remote": "Remote" if "remote" in str(location).lower() else "",
    })

publish_or_update(final_jobs)
publish_logo(company.get("company"), logo)
show_jobs(final_jobs)
