from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

url = " https://careers.smartrecruiters.com/PublicisGroupe/api/more?search=Romania&type=location%2C%20RO&"

company = "PublicisGroupe"
finalJobs = list()
page = 0
scraper = Scraper()
scraper.get_from_url(url + f"page={page}")

jobs = scraper.find_all("li")


while jobs:
    for job in jobs:
        finalJobs.append(
            create_job(
                job_title=job.find("h4").text,
                job_link=job.find("a")["href"],
                country="Romania",
                city="Bucuresti",
                county="Bucuresti",
                company=company,
            )
        )

    page += 1
    scraper.get_from_url(url + f"page={page}")
    jobs = scraper.find_all("li")


publish_or_update(finalJobs)

publish_logo(
    company,
    "https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc1/58822766e4b0680b1154ae69/huge?r=s3&_1533642429153",
)
show_jobs(finalJobs)
