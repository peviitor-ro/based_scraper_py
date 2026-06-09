from scraper.Scraper import Scraper
from utils import (
    create_job,
    publish_or_update,
    publish_logo,
    show_jobs,
    translate_city,
)
from getCounty import GetCounty

_counties = GetCounty()

url = "https://careers.amd.com/api/jobs?stretchUnit=MILES&stretch=10&location=Romania&woe=12&regionCode=RO&limit=100&page=1&sortBy=relevance&descending=false&internal=false"

company = "AMD"

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

jobs_elements = scraper.markup.get("jobs")

jobs = []
for job in jobs_elements:
    data = job.get("data", {})
    location_name = data.get("location_name", "")
    city_raw = data.get("city")

    if not city_raw and location_name:
        parts = location_name.split(",")
        if len(parts) > 1:
            city_raw = parts[1].strip()

    if city_raw and "Home Office" not in city_raw:
        city = translate_city(city_raw.title())
        county = _counties.get_county(city)
        job_element = create_job(
            company=company,
            job_title=data.get("title"),
            job_link="https://careers.amd.com/careers-home/jobs/"
            + str(data.get("slug")),
            country="Romania",
            city=city,
            county=county,
        )
    else:
        job_element = create_job(
            company=company,
            job_title=data.get("title"),
            job_link="https://careers.amd.com/careers-home/jobs/"
            + str(data.get("slug")),
            country="Romania",
            remote="remote",
        )

    jobs.append(job_element)

publish_or_update(jobs)

publish_logo(company, "https://1000logos.net/wp-content/uploads/2020/05/AMD-Logo.png")
show_jobs(jobs)
