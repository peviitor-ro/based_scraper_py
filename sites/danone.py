from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = "https://careers.danone.com/bin/jobs.json?countries=Romania&locale=en&limit=100"

company = {"company": "Danone"}


scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("results")

finalJobs = [
    {
        "job_title": job.get("title"),
        "job_link": "https://careers.danone.com/en-global/jobs/" + job.get("url"),
        "company": company.get("company"),
        "country": "Romania",
        "city": translate_city(job.get("city").title()),
        "county": _counties.get_county(translate_city(job.get("city").title())),
        "remote": job.get("workFromHome").replace("Field", "")
    }
    for job in jobs
]

publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/1/13/DANONE_LOGO_VERTICAL.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
