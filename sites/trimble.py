from scraper.Scraper import Scraper
from utils import publish_logo, publish_or_update, show_jobs, create_job
import json

company = "Trimble"
apiUrl = "https://trimble.wd1.myworkdayjobs.com/wday/cxs/trimble/TrimbleCareers/jobs"

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
    locations_text = job.get("locationsText") or ""
    if "Brasov" in locations_text:
        city = "Brasov"
        county = "Brasov"
        remote = []
    else:
        city = None
        county = None
        remote = ["remote"]

    finalJobs.append(
        create_job(
            job_title=job.get("title"),
            job_link="https://trimble.wd1.myworkdayjobs.com/en-US/TrimbleCareers" + (job.get("externalPath") or ""),
            company=company,
            country="Romania",
            city=city,
            county=county,
            remote=remote,
        )
    )

publish_or_update(finalJobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Trimble_logo.svg/512px-Trimble_logo.svg.png",
)
show_jobs(finalJobs)
