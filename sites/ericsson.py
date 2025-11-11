from scraper.Scraper import Scraper
from utils import create_job, publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://jobs.ericsson.com/api/pcsx/search?domain=ericsson.com&query=&location=Romania&start=0&sort_by=distance&filter_include_remote=1"

company = "Ericsson"
jobs = list()

scraper = Scraper()
scraper.get_from_url(url, "JSON")

tota_jobs = scraper.markup["data"]["count"]
step = 10

pages = ceil(tota_jobs / step)

for page in range(pages):
    url = f"https://jobs.ericsson.com/api/pcsx/search?domain=ericsson.com&query=&location=Romania&start={page * step}&sort_by=distance&filter_include_remote=1"
    scraper.get_from_url(url, "JSON")

    for job in scraper.markup["data"]["positions"]:
        cities = [
            translate_city(location.split(",")[0])
            for location in job["locations"]
        ]
        counties = []

        for city in cities:
            county = _counties.get_county(city) or []
            counties.extend(county)

        jobs.append(
            create_job(
                job_title=job["name"],
                job_link="https://jobs.ericsson.com" + job["positionUrl"],
                company=company,
                country="Romania",
                city=cities,
                county=counties,
            )
        )


publish_or_update(jobs)

publish_logo(
    company,
    "https://logos-world.net/wp-content/uploads/2020/12/Ericsson-Logo-700x394.png",
)
show_jobs(jobs)
