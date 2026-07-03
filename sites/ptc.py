from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, create_job
from math import ceil
import json

url = "https://ptc.wd1.myworkdayjobs.com/wday/cxs/ptc/PTC/jobs"

company = "PTC"
finalJobs = list()

post_data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

headers = {"Content-Type": "application/json"}
scraper = Scraper()
scraper.set_headers(headers)
obj = scraper.post(url, json.dumps(post_data))

step = 20
total_jobs = obj.json()["total"]
pages = ceil(total_jobs / step)

for page in range(pages):
    if page > 0:
        post_data["offset"] = page * step
        obj = scraper.post(url, json.dumps(post_data))

    for job in obj.json()["jobPostings"]:
        locations_text = job.get("locationsText", "")
        if "Bucharest" not in locations_text and "Bucuresti" not in locations_text and "ROM-" not in job.get("externalPath", ""):
            continue

        job_title = job.get("title")
        if not job_title:
            continue

        job_link = "https://ptc.wd1.myworkdayjobs.com/en-US/PTC" + job.get("externalPath", "")

        finalJobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                city="Bucuresti",
                county="Bucuresti",
                company=company,
            )
        )

publish_or_update(finalJobs)

logoUrl = "https://ptc.wd1.myworkdayjobs.com/PTC/assets/logo"
publish_logo(company, logoUrl)

show_jobs(finalJobs)
