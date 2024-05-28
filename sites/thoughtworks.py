from scraper_peviitor import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    create_job,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty

_counties = GetCounty()
url = "https://www.thoughtworks.com/rest/careers/jobs"

company = {"company": "ThoughtWorks"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("jobs")

acurate_city = acurate_city_and_county(
    Cluj={"city": "Cluj-Napoca", "county": "Cluj"},
    Iasi={"city": "Iasi", "county": "Iasi"},
)

for job in jobs:
    country = job.get("country")

    if country == "Romania":
        job_title = job.get("name")
        job_link = "https://www.thoughtworks.com/careers/jobs/" + str(
            job.get("sourceSystemId")
        )
        city = translate_city(job.get("location").split("-")[0].strip())

        job = create_job(
            job_title=job_title,
            job_link=job_link,
            company=company.get("company"),
            country=country,
        )

        if city in acurate_city.keys():
            job["city"] = acurate_city.get(city).get("city")
            job["county"] = acurate_city.get(city).get("county")
        else:
            job["city"] = city
            job["county"] = _counties.get_county(city)

        finalJobs.append(job)

publish_or_update(finalJobs)

logoUrl = "https://www.thoughtworks.com/etc.clientlibs/thoughtworks/clientlibs/clientlib-site/resources/images/thoughtworks-logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)