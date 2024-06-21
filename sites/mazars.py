from scraper.Scraper import Scraper
import json
from utils import (
    translate_city,
    publish_or_update,
    publish_logo,
    show_jobs,
    translate_city,
)
from getCounty import GetCounty

_counties = GetCounty()
url = " https://www.mazarscareers.com/ro/wp-admin/admin-ajax.php?action=get_job_listing_html&searchTerm=&form=contract%3D%26location%3D%26service%3D&amount=-1&location="

company = {"company": "Mazars"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url, "JSON")

html = scraper.markup.get("html")
scraper.__init__(html, "html.parser")

jobs = scraper.find_all("article", {"class": "JobResult"})

for job in jobs:
    job_title = job.find("h3").text.strip()
    job_link = job.find("h3").find("a").get("href")
    city = [
        translate_city(
            job.find("p", {"class": "job-listing__location"})
            .text.split(":")[-1]
            .strip()
        )
    ]

    if not city[0]:
        city = ["Bucuresti", "Cluj-Napoca"]

    counties = []

    for c in city:
        county = _counties.get_county(c) or []
        counties.extend(county)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "country": "Romania",
            "city": city,
            "county": counties,
            "company": company.get("company"),
        }
    )

publish_or_update(finalJobs)

logoUrl = "https://www.mazarscareers.com/ro/wp-content/themes/mazars-2020/assets/images/mazars-logo.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
