from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from math import ceil
from getCounty import GetCounty

_counties = GetCounty()

url = "https://jobs.vodafone.com/api/apply/v2/jobs?domain=vodafone.com&start=10&num=10&exclude_pid=563018680721259&location=Romania&pid=563018680721259&domain=vodafone.com&sort_by=relevance"

company = "Vodafone"
jobs = []

scraper = Scraper(url)
scraper.get_from_url(url, "JSON")

total_jobs = scraper.markup["count"]
step = 10
pages = ceil(total_jobs / step)

for page in range(0, pages):

    for job in scraper.markup["positions"]:
        locations = job["location"].split(",")
        country = locations[-1].strip()
        consol = locations[0].strip()

        city = translate_city(locations[0].strip())
        if "Drobeta Turnu-Severin" in city:
            city = "Drobeta-Turnu Severin"
        county = _counties.get_county(city)

        jobs.append(
            create_job(
                job_title=job["name"],
                job_link=job["canonicalPositionUrl"],
                city=city,
                country="Romania",
                company=company,
                county=county,
            )
        )

    url = f"https://jobs.vodafone.com/api/apply/v2/jobs?domain=vodafone.com&start={page * step}&num={step}&exclude_pid=563018680721259&location=Romania&pid=563018680721259&domain=vodafone.com&sort_by=relevance"
    scraper.get_from_url(url, "JSON")

publish_or_update(jobs)

publish_logo(
    company,
    "https://static.vscdn.net/images/careers/demo/eightfolddemo-vodafone2/8d898eb4-685e-441a-9b64-9.png",
)

show_jobs(jobs)
