from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
import json
url = "https://careers.veeam.com/api/vacancy"

company = "Veeam"
jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs_elements = scraper.markup

for job in jobs_elements:
    city = job["location"][0]["city"]
    if city == None:
        city = job["location"][0]["country"]
    jobs.append(create_job(
        job_title=job["title"],
        job_link=job["applyUrl"],
        city=city,
        country=job["location"][0]["country"],
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://img.veeam.com/careers/logo/veeam/veeam_logo_bg.svg')
show_jobs(jobs)  
