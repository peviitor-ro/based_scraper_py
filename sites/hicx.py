from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
import json

company = "hicx"
url = "https://apply.workable.com/api/v3/accounts/hicx-solutions/jobs"

data = {
    "query": "",
    "department": [],
    "location": [
        {
            "country": "Romania",
            "region": "Bucharest",
            "city": "Bucharest",
            "countryCode": "RO",
        }
    ],
    "remote": [],
    "workplace": [],
    "worktype": [],
}

scraper = Scraper()
scraper.set_headers({"Content-Type": "application/json"})
scraper.markup = scraper.post(url, json.dumps(data)).json().get("results")

jobs = [
    {
        "job_title": job["title"],
        "job_link": "https://apply.workable.com/hicx-solutions/j/" + job["shortcode"],
        "remote": job["workplace"].replace("_", "-"),
        "country": "Romania",
        "company": company,
        "city": translate_city(job["location"]["city"]),
        "county": translate_city(
            job["location"]["region"].replace("County", "").strip()
        ),
    }
    for job in scraper.markup
    if job["location"]["country"] == "Romania"
]

publish_or_update(jobs)

publish_logo(
    company,
    "https://workablehr.s3.amazonaws.com/uploads/account/logo/506721/logo",
)

show_jobs(jobs)
