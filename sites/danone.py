from scraper_peviitor import Scraper
from utils import publish, publish_logo, show_jobs, translate_city
from getCounty import get_county

url = "https://careers.danone.com/bin/jobs.json?countries=Romania&locale=en&limit=100"

company = {"company": "Danone"}


scraper = Scraper(url)

jobs = scraper.getJson().get("results")

finalJobs = [
    {
        "job_title": job.get("title"),
        "job_link": "https://careers.danone.com/en-global/jobs/" + job.get("url"),
        "company": company.get("company"),
        "country": "Romania",
        "city": translate_city(job.get("city").title()),
        "county": get_county(translate_city(job.get("city").title())),
        "remote": job.get("workFromHome"),
    }
    for job in jobs
]

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/1/13/DANONE_LOGO_VERTICAL.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
