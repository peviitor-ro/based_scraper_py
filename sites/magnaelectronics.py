from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'MagnaElectronics'
url = 'https://magnaelectronicsromania.teamtailor.com/jobs?page='

scraper = Scraper()

jobs = []
page = 1

while True:
    scraper.get_from_url(url + str(page), "HTML")

    jobsElements = scraper.find_all("li", class_ = "transition-opacity duration-150 border rounded block-grid-item border-block-base-text border-opacity-15")

    if len(jobsElements) == 0:
        break

    for job in jobsElements:
        job_title = job.find("span", class_ = "text-block-base-link company-link-style").text.strip()
        job_link = job.find("a").get("href")
        try:
            city = job.find("div", class_ = "mt-1 text-md").find_all("span")[2].text.split(",")[0].strip()
        except:
            city = "Romania"

        jobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            city=city,
            country='Romania',
            company=company,
        ))

    page += 1
    
for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/6901fc63-3786-4d8b-8230-aa1bcd971324/original.png')
show_jobs(jobs)
