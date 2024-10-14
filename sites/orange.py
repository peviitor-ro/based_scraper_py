from requests import get
from json import dumps
from getCounty import get_county
from utils import (
    publish,
    publish_logo,
    show_jobs
)


url = "https://www.orange.ro/ux-admin/api/jobs/getJobs?&limit=10000"

final_jobs = []
company = "orange"

response = get(url)

jobs = response.json()

for job in jobs:
    job_info = {
        "job_title": job["title"],
        "job_link": job["url"],
        "country": "Romania",
        "city": job["location"][0]["name"],
        "county": get_county(job["location"][0]["name"]),
        "company": company,
    }
    final_jobs.append(job_info)

publish(4, company, final_jobs, 'APIKEY')

publish_logo(
    company,
    'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Orange_logo.svg/426px-Orange_logo.svg.png?20220928152222'
)

show_jobs(final_jobs)