from scraper.Scraper import Scraper
from utils import publish, publish_logo, show_jobs

company = "evozone"
url = "https://www.evozon.com/careers/"

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("div", class_="job-name")

final_jobs = [
    {
        "job_link": job.find("a")["href"],
        "job_title": job.find("a").get_text(strip=True),
        "city": "Cluj-Napoca",
        "county": "Cluj",
        "country": "Romania",
        "company": company,
    }
    for job in jobs
]
publish(4, company, final_jobs, "Grasum_Key")

publish_logo(company, "https://www.evozon.com/wp-content/uploads/2021/03/Group-813.svg")
show_jobs(final_jobs)
