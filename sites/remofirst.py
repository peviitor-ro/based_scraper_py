import requests

from ats_common import HEADERS, build_job, finalize_jobs

COMPANY = "RemoFirst"
LOGO_URL = "https://logo.clearbit.com/remofirst.com"
API_URL = "https://apply.workable.com/api/v3/accounts/remofirst/jobs"
JOB_URL = "https://apply.workable.com/remofirst/j/{shortcode}/"

jobs = []
seen_links = set()
token = None

while True:
    payload = {"query": ""}
    if token:
        payload["token"] = token

    response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()

    for job in data.get("results", []):
        shortcode = job.get("shortcode")
        if not shortcode:
            continue

        job_link = JOB_URL.format(shortcode=shortcode)
        if job_link in seen_links:
            continue

        location_signals = []
        for location in job.get("locations") or []:
            location_signals.extend(
                [location.get("city"), location.get("country"), location.get("region")]
            )

        job_data = build_job(
            COMPANY,
            job.get("title") or "",
            job_link,
            location_signals,
            [job.get("workplace") or ""],
        )
        if not job_data:
            continue

        seen_links.add(job_link)
        jobs.append(job_data)

    token = data.get("nextPage")
    if not token:
        break

finalize_jobs(COMPANY, LOGO_URL, jobs)
