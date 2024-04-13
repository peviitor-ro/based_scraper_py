from scraper.Scraper import Scraper
from utils import (
    create_job,
    publish_or_update,
    publish_logo,
    show_jobs,
    translate_city,
    acurate_city_and_county,
)
from getCounty import GetCounty

_counties = GetCounty()

url = "https://careers.amd.com/api/jobs?stretchUnits=MILES&stretch=10&location=Romania&limit=100&page=1&sortBy=relevance&descending=false&internal=false"

company = "AMD"

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

jobs_elements = scraper.markup.get("jobs")

acurate_location = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})

jobs = [
    create_job(
        company=company,
        job_title=job.get("data").get("title"),
        job_link="https://careers.amd.com/careers-home/jobs/"
        + str(job.get("data").get("slug")),
        country="Romania",
        city=translate_city(job.get("data").get("city").title()),
        county=(
            acurate_location.get(
                translate_city(job.get("data").get("city").title())
            ).get("county")
            if acurate_location.get(translate_city(job.get("data").get("city").title()))
            else _counties.get_county(translate_city(job.get("data").get("city").title()))
        ),
    )
    for job in jobs_elements
]

publish_or_update(jobs)

publish_logo(company, "https://1000logos.net/wp-content/uploads/2020/05/AMD-Logo.png")
show_jobs(jobs)
