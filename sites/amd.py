from scraper.Scraper import Scraper
from utils import (create_job, publish, publish_logo, show_jobs)

url = "https://careers.amd.com/api/jobs?stretchUnits=MILES&stretch=10&location=Romania&limit=100&page=1&sortBy=relevance&descending=false&internal=false"

company = "AMD"
jobs = []

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

for job in scraper.markup.get("jobs"):
    job = job.get("data")
    jobs.append(create_job(
        company = company,
        job_title = job.get("title"),
        job_link = "https://careers.amd.com/careers-home/jobs/" + str(job.get("slug")),
        country = "Romania",
        city =  job.get("city"),
    ))

for version in [1, 4]:
    publish(version, company, jobs, "APIKEY")

publish_logo(company, "https://1000logos.net/wp-content/uploads/2020/05/AMD-Logo.png")
show_jobs(jobs)