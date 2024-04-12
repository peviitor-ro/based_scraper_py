from scraper.Scraper import Scraper
from utils import create_job, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty

_counties = GetCounty()

company = "Acrom"

url = "https://mingle.ro/api/boards/careers-page/jobs?company=acrom&page=0&pageSize=200&sort=id~ASC"

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

jobs_elements = scraper.markup.get("data").get("results")

jobs = [
    create_job(
        job_title=job.get("title"),
        job_link="https://acrom.mingle.ro/en/apply/" + job.get("uid"),
        country="Romania",
        city=(
            job.get("locations")[0].get("label") if job.get("locations") != None else []
        ),
        county=(
            _counties.get_county(job.get("locations")[0].get("label"))
            if job.get("locations") != None
            else []
        ),
        company=company,
    )
    for job in jobs_elements
]

publish_or_update(jobs)
publish_logo(
    company, "https://www.acrom.ro/wp-content/uploads/2022/05/1-Acrom-logo-main.png"
)
show_jobs(jobs)
