import requests
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city


url = "https://apply.workable.com/api/v3/accounts/nuvei/jobs"
company = "Nuvei"

data = {
    "query": "",
    "location": [
        {
            "country": "Romania",
            "countryCode": "RO",
        }
    ],
    "department": [],
    "worktype": [],
    "remote": [],
}

response = requests.post(url, json=data).json().get("results") or []

final_jobs = [
    create_job(
        job_title=job["title"],
        company=company,
        country=job["location"]["country"],
        city=translate_city(job["location"]["city"]),
        county=translate_city(job["location"]["region"].replace("County", "").strip()),
        job_link="https://apply.workable.com/nuvei/j/" + job["shortcode"],
        remote=job["workplace"].replace("_", "-"),
    )
    for job in response
    if job["location"]["country"] == "Romania"
]

publish_or_update(final_jobs)

publish_logo(
    company,
    "https://www.nuvei.com/wp-content/uploads/2021/07/nuvei-logo.svg",
)
show_jobs(final_jobs)