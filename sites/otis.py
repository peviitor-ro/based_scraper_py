from scraper.Scraper import Scraper
from utils import publish_logo, publish_or_update, show_jobs, create_job
import json

company = "Otis"
apiUrl = "https://otis.wd5.myworkdayjobs.com/wday/cxs/otis/REC_Ext_Gateway/jobs"

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
            job_link="https://otis.wd5.myworkdayjobs.com/en-US/REC_Ext_Gateway" + (job.get("externalPath") or ""),
            company=company,
            country="Romania",
            city="Bucuresti",
            county="Bucuresti",
        )
    )

publish_or_update(finalJobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Otis_Logo.svg/512px-Otis_Logo.svg.png",
)
show_jobs(finalJobs)
