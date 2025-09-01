from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from math import ceil
import json

apiUrl = "https://zentiva.wd3.myworkdayjobs.com/wday/cxs/zentiva/Zentiva/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {
    "appliedFacets": {"locations": ["ca7924da36fa0149be9376945a35dd27"]},
    "limit": 20,
    "offset": 0,
    "searchText": "",
}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")

iteration = ceil(numberOfJobs / 20)

company = {"company": "Zentiva"}
finaljobs = list()

for num in range(iteration):
    data["offset"] = num
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings")
    for job in jobs:
        job_title = job.get("title")
        job_link = "https://zentiva.wd3.myworkdayjobs.com/en-US/Zentiva" + job.get(
            "externalPath"
        )

        finaljobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": "Bucuresti",
                "county": "Bucuresti",
            }
        )

publish_or_update(finaljobs)
logoUrl = "https://zentiva.wd3.myworkdayjobs.com/Zentiva/assets/logo"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
