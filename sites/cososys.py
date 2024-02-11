import requests
from utils import publish, publish_logo, create_job, show_jobs


url = "https://apply.workable.com/api/v3/accounts/cososys/jobs"
company = "Cososys"

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

response = requests.post(url, json=data).json()["results"]

final_jobs = []


final_jobs = [
    create_job(
        job_title=job["title"],
        company=company,
        country=job["location"]["country"],
        city="Cluj-Napoca",
        county="Cluj",
        job_link="https://apply.workable.com/cososys/j/" + job["shortcode"],
    )
    for job in response
]

publish(4, company, final_jobs, "Grasum_Key")

publish_logo(
    company,
    "https://www.endpointprotector.com/images/img/site/endpoint-protector-by-cososys-logo.svg",
)
show_jobs(final_jobs)
