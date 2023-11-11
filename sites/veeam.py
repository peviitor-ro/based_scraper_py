from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city)
from getCounty import get_county

url = "https://careers.veeam.com/api/vacancy"

company = "Veeam"
jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs_elements = scraper.markup

for job in jobs_elements:
    for location in job["location"]:
        country = location["country"]
        city = location["city"]

        jobObj = create_job(
            job_title=job["title"],
            job_link="https://jobs.smartrecruiters.com/Veeam2/" + job["remoteId"],
            city=city,
            country=country,
            company=company
        )

        if country == "Romania":
            jobObj["job_link"] = job["applyUrl"]
            county = get_county(translate_city(city))
            jobObj["county"] = county

        jobs.append(jobObj)

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://img.veeam.com/careers/logo/veeam/veeam_logo_bg.svg')
show_jobs(jobs)  