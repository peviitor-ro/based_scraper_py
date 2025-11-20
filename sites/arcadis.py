from scraper.Scraper import Scraper
from utils import (
    publish_or_update,
    publish_logo,
    create_job,
    show_jobs,
    get_jobtype
)
from getCounty import GetCounty
from math import ceil


start = 0
url = f"https://jobs.arcadis.com/api/pcsx/search?domain=arcadis.com&query=&location=Romania&start={start}&sort_by=distance&filter_include_remote=1"

company = "Arcadis"

scraper = Scraper()
scraper.get_from_url(url, type="JSON")
pages = ceil(scraper.markup.get("data").get("count") / 10)

jobs = list()

for page in range(1, pages + 1):
    jobs_objects = scraper.markup.get("data").get("positions")
    for job in jobs_objects:
        job_title = job.get("name")
        job_link = "https://jobs.arcadis.com" + job.get("positionUrl")
        country = "Romania"
        remote = get_jobtype(job.get("workLocationOption", ""))

        job = create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country=country,
            remote=remote,
        )

        jobs.append(job)
        
    start = page * 10
    scraper = Scraper()
    scraper.get_from_url(
        f"https://jobs.arcadis.com/api/pcsx/search?domain=arcadis.com&query=&location=Romania&start={start}&sort_by=distance&filter_include_remote=1",
        type="JSON",
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://cdn.phenompeople.com/CareerConnectResources/ARCAGLOBAL/images/header-1679586076111.svg",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")
