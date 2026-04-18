from scraper.Scraper import Scraper
from utils import publish_logo, publish_or_update, show_jobs, create_job
import json

company = "MotorolaSolutions"
apiUrl = "https://motorolasolutions.wd5.myworkdayjobs.com/wday/cxs/motorolasolutions/Careers/jobs"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper = Scraper()
scraper.set_headers(headers)
jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings") or []

finalJobs = []

for job in jobs:
    finalJobs.append(
        create_job(
            job_title=job.get("title"),
            job_link="https://motorolasolutions.wd5.myworkdayjobs.com/en-US/Careers" + (job.get("externalPath") or ""),
            company=company,
            country="Romania",
            remote=["remote"],
        )
    )

publish_or_update(finalJobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Motorola_Solutions_logo.svg/512px-Motorola_Solutions_logo.svg.png",
)
show_jobs(finalJobs)
