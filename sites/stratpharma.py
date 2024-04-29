from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs

company = "stratpharma"
url = "https://jobs.workable.com/api/v1/companies/kRMJQQdcEfWFqoT2heypL5"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = [
    {
        "job_title": job["title"],
        "job_link": job["url"],
        "remote": job["workplace"].replace("_", "-"),
        "country": "Romania",
        "company": company,
        "city": job["location"]["city"],
        "county": job["location"]["subregion"].replace("County", "").strip(),
    }
    for job in scraper.markup.get("jobs")
    if job["location"]["countryName"] == "Romania"
]

publish_or_update(jobs)

publish_logo(
    company,
    "https://workablehr.s3.amazonaws.com/uploads/account/logo/24841/logo",
)

show_jobs(jobs)
