from scraper.Scraper import Scraper
from utils import create_job, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty

_counties = GetCounty()

company = "Acrom"

url = "https://mingle.ro/api/boards/careers-page/jobs?company=acrom&page=0&pageSize=200&sort=id~ASC"

scraper = Scraper()
scraper.set_headers({
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://acrom.mingle.ro/en/careers",
})
scraper.get_from_url(url, type="JSON", verify=False)

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
