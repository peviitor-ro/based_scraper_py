from scraper.Scraper import Scraper
from utils import (
    publish_or_update,
    publish_logo,
    create_job,
    show_jobs,
    translate_city,
    acurate_city_and_county,
    get_jobtype
)
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()

url = "https://jobs.arcadis.com/api/apply/v2/jobs?domain=arcadis.com&location=Romania&domain=arcadis.com&sort_by=relevance" 
company = "Arcadis"

scraper = Scraper()
headers = {
    "Content-Type": "application/json",
}
scraper.set_headers(headers)

exclude_city = acurate_city_and_county(
    Iasi={"city": "Iasi", "county": "Iasi"}, Moldavia={"city": "Iasi", "county": "Iasi"}
)
scraper.get_from_url(url, type="JSON")
pages = ceil(scraper.markup.get("count") / 10)

jobs = list()

for page in range(1, pages + 1):
    jobs_objects = scraper.markup.get("positions")
    for job in jobs_objects:
        job_title = job.get("name")
        job_link = job.get("canonicalPositionUrl")
        country = "Romania"
        remote = get_jobtype(job.get("work_location_option"))

        cities = []
        cities.extend(
            [
                translate_city(location.split(",")[0].strip())
                for location in job.get("locations")
                if location.split(",")[-1].strip() == "Romania"
            ]
        )
        counties = []

        for city in cities:
            if exclude_city.get(city):
                counties.append(exclude_city.get(city).get("county"))
            else:
                counties.extend(_counties.get_county(city) if _counties.get_county(city) else [])
        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country=country,
                city=cities,
                county=counties,
                remote=remote,
            )
        )
    start = page * 10
    scrper = Scraper()
    scraper.get_from_url(url + f"&start={start}&num=10", type="JSON")

publish_or_update(jobs)
publish_logo(
    company,
    "https://cdn.phenompeople.com/CareerConnectResources/ARCAGLOBAL/images/header-1679586076111.svg",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")
