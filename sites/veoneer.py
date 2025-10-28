from scraper.Scraper import Scraper
from utils import (
    translate_city,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
url = "https://veoneerro.teamtailor.com/jobs"

company = {"company": "Veoneer"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find("ul", {"id": "jobs_list_container"}).find_all(
    "li"
)

for job in jobs:
    job_title = job.find("a").text.strip()
    job_link = job.find("a").get("href")

    cities = [
        translate_city(remove_diacritics(city.strip()))
        for city in job.find("div", {"class": "mt-1 text-md"})
        .find_all("span")[2]
        .text.split(",")
    ]
    counties = []

    for city in cities:
        county = _counties.get_county(city) or []
        counties.extend(county)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "city": cities,
            "county": counties,
            "company": company.get("company"),
        }
    )

publish_or_update(finalJobs)

logoUrl = "https://seekvectorlogo.com/wp-content/uploads/2020/02/veoneer-inc-vector-logo-small.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
