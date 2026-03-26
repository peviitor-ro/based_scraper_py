import requests
from utils import show_jobs, publish_or_update, publish_logo, create_job


company = "sapfioneer"
url = "https://apply.workable.com/api/v3/accounts/fioneer/jobs"

payload = {
    "query": "",
    "department": [],
    "location": [{"country": "Romania", "countryCode": "RO"}],
    "workplace": [],
    "worktype": [],
}

response = requests.post(url, json=payload, timeout=20).json()
jobs = response.get("results") or []
final_jobs = []

for job in jobs:
    remote = []
    workplace = (job.get("workplace") or "").replace("_", "-").lower()

    if workplace:
        remote.append(workplace)

    final_jobs.append(
        create_job(
            job_title=job.get("title"),
            job_link="https://apply.workable.com/fioneer/j/" + job.get("shortcode"),
            remote=remote,
            country="Romania",
            company=company,
            city=[],
            county=[],
        )
    )


publish_or_update(final_jobs)

logourl = "https://workablehr.s3.amazonaws.com/uploads/account/logo/562664/logo"
publish_logo(company, logourl)

show_jobs(final_jobs)
