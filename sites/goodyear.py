from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from math import ceil
import json

company = "GoodYear"
url = "https://goodyear.wd1.myworkdayjobs.com/wday/cxs/goodyear/GoodyearCareers/jobs"

post_data = {"appliedFacets": {"locations": ["8e6033e1c034100168b80fcc8d420000",
                                             "013bdadd1adf100168e66388c7390000"]}, "limit": 20, "offset": 0, "searchText": ""}

headers = {"Content-Type": "application/json"}
scraper = Scraper()
scraper.set_headers(headers)
obj = scraper.post(url, json.dumps(post_data))

step = 20
total_jobs = obj.json()["total"]
pages = ceil(total_jobs / step)

jobs = []

for pages in range(0, pages):
    if pages > 1:
        post_data["offset"] = pages * step
        obj = scraper.post(url, json.dumps(post_data))

    for job in obj.json()["jobPostings"]:
        job_title = job["title"]
        job_link = "https://goodyear.wd1.myworkdayjobs.com/en-US/GoodyearCareers" + \
            job["externalPath"]
        country = "Romania"
        remote = [job.get("remoteType")] if job.get("remoteType") else []

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                company=company,
                remote=remote,
            )
        )


publish_or_update(jobs)

publish_logo(
    company, "https://rmkcdn.successfactors.com/38b5d3dd/ef930ba2-97c9-4abc-a14a-e.png"
)
show_jobs(jobs)
