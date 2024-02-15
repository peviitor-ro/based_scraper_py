from scraper.Scraper import Scraper
from utils import publish, publish_logo, create_job, show_jobs
from getCounty import get_county, remove_diacritics

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
        county=get_county(job.find("div", class_="location").text.split(",")[0]),
    )
    for job in jobs_elements
]

publish(4, company, jobs, "APIKEY")

publish_logo(company, "https://jobs.freudenberg.com/Freudenberg/static/img/logo.svg")
show_jobs(jobs)
