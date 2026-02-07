from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
import json
from math import ceil

company = "atkinsrealis"
url = "https://slihrms.wd3.myworkdayjobs.com/wday/cxs/slihrms/Careers/jobs"
post_data = {"appliedFacets": {"locations": [
    "a19c13ab2cba10a5238f4fb548d3bdf5"]}, "limit": 20, "offset": 0, "searchText": ""}

scraper = Scraper()
scraper.set_headers(
    {   
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 91.0.4472.124 Safari/537.36",
    }
)

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
        job_link = "https://slihrms.wd3.myworkdayjobs.com/en-US/Careers" + \
            job["externalPath"]
        country = "Romania"
        remote = [job.get("remoteType")] if job.get("remoteType") else []

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                city="Bucuresti",
                county="Bucuresti",
                company=company,
                remote=remote,
            )
        )


publish_or_update(jobs)

publish_logo(
    company,
    "https://attraxcdnprod1-freshed3dgayb7c3.z01.azurefd.net/1481103/1e2dbbdd-b55c-47cb-941b-4ecd47e8f5ef/2023.17000.541/Blob/img/snc-logo.png",
)
show_jobs(jobs)
