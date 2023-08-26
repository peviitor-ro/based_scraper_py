from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

url = "https://careers.smartrecruiters.com/PublicisGroupe?search=Romania"

company = "PublicisGroupe"
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)

jobs_containers = scraper.find_all("section", class_="openings-section")

for job_container in jobs_containers:
    jobs = job_container.find("ul", class_="opening-jobs grid--gutter padding--none js-group-list").find_all("li")
    for job in jobs:
        finalJobs.append(create_job(
            job_title=job.find("h4").text,
            job_link=job.find("a")['href'],
            country="Romania",
            city="Romania",
            company=company,
        ))

for version in [1,4]:
    publish(version, company, finalJobs, 'APIKEY')

publish_logo(company, "https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc1/58822766e4b0680b1154ae69/huge?r=s3&_1533642429153")
show_jobs(finalJobs)