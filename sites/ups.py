from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs
from math import ceil
import json

url = "https://hcmportal.wd5.myworkdayjobs.com/wday/cxs/hcmportal/Search/jobs"

company = "UPS"
jobs = []

scraper = Scraper()
scraper.set_headers(
    {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
)
body = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

total_jobs = scraper.post(url, json.dumps(body)).json()
step = 20
pages = ceil(total_jobs["total"] / step)


for page in range(pages):
    body["offset"] = page * step
    response = scraper.post(url, json.dumps(body)).json()

    for job in response["jobPostings"]:
        jobs.append(
            create_job(
                job_title=job["title"],
                job_link="https://hcmportal.wd5.myworkdayjobs.com/en-US/Search"
                + job["externalPath"],
                city="Bucuresti",
                county="Bucuresti",
                country="Romania",
                company=company,
            )
        )

publish_or_update(jobs)

publish_logo(company, "/Search/assets/logo")
show_jobs(jobs)
