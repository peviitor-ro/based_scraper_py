from scraper.Scraper import Scraper
from utils import create_job, publish_logo, publish, show_jobs
from getCounty import get_county

company = "Acrom"

url = "https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22acrom%22&page=0&pageSize=30&sort=modifiedDate~DESC"

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

jobs_elements = scraper.markup.get("data").get("results")

jobs = [
    create_job(
        job_title=job.get("jobTitle"),
        job_link="https://acrom.mingle.ro/en/apply/" + job.get("publicUid"),
        country="Romania",
        city=job.get("locations")[0].get("name"),
        county=get_county(job.get("locations")[0].get("name")),
        company=company,
    )
    for job in jobs_elements
    if job.get("locations")
]

publish(4, company, jobs, "Grasum_Key")

publish_logo(
    company, "https://www.acrom.ro/wp-content/uploads/2022/05/1-Acrom-logo-main.png"
)
show_jobs(jobs)
