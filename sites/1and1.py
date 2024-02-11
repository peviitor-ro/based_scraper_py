from scraper_peviitor import Scraper
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county
import re

url = "https://www.1and1.ro/jobs.json"

company = {"company": "1and1"}

scraper = Scraper()
scraper.url = url

jobs = scraper.getJson().get("jobs")

remote_pattern = re.compile(r"\(.+\)")

finalJobs = [
    {
        "job_title": job.get("JobTitle"),
        "job_link": "https://www.1and1.ro/careers/" + job.get("RefURL"),
        "country": "Romania",
        "city": translate_city(job.get("Location")),
        "county": get_county(translate_city(job.get("Location"))),
        "remote": (
            remote_pattern.search(job.get("JobTitle"))
            .group(0)
            .replace("(", "")
            .replace(")", "")
            .replace("full", "")
            .replace(" ", "")
            .split("/")
            if remote_pattern.search(job.get("JobTitle"))
            else []
        ),
        "company": company.get("company"),
    }
    for job in jobs
]

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://cdn.website-editor.net/b236a61347464e4b904f5e6b661c2af9/dms3rep/multi/1and1-logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
