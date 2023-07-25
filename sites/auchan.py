from scraper.Scraper import Scraper 
from utils import (create_job, clean, update, publish, publish_logo, show_jobs)
from math import ceil

company = "Auchan"
url = "https://cariere.auchan.ro/jobs?per_page=1000"
scraper = Scraper()
scraper.get_from_url(url)

total_jobs = scraper.find("div", class_="sumarry").text.split(" ")[-3]

jobs = list()

pages = ceil(int(total_jobs) / 1000)

for page in range(pages):
    url = f"https://cariere.auchan.ro/jobs?page={page + 1}&per_page={pages * 1000}"
    scraper.get_from_url(url)

    jobs_elements = scraper.find_all("a", class_="job")
    for job in jobs_elements:
        jobs.append(create_job(
            job_title=job.find("div", class_="job-title").text,
            job_link=job["href"],
            company=company,
            country="Romania",
            city=job.find("div", class_="js-job-oras").text,
        ))

for version in [1, 4]:
    publish(version, company, jobs, "APIKEY")

show_jobs(jobs)