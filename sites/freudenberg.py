from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
company = "Freudenberg"
url = "https://jobs.freudenberg.com/Freudenberg/ro/?location=RO"

scraper = Scraper()
scraper.get_from_url(url)


jobs_elements = scraper.find("div", class_="jobs").find_all("div", class_="job")

jobs = [
    create_job(
        job_title=job.find("div", class_="jobtitle").text,
        job_link="https://jobs.freudenberg.com/freudenberg/job/ro/details/"
        + job.find("span")["id"],
        city=remove_diacritics(job.find("div", class_="location").text.split(",")[0]),
        country="Romania",
        company=company,
        county=_counties.get_county(job.find("div", class_="location").text.split(",")[0]),
    )
    for job in jobs_elements
]

publish_or_update(jobs)

publish_logo(company, "https://jobs.freudenberg.com/Freudenberg/static/img/logo.svg")
show_jobs(jobs)
