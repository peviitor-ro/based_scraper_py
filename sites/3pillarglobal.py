from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo

url = "https://www.3pillarglobal.com/career-opportunities/"
company = "3PillarGlobal"
logo = "https://i.imgur.com/SM5d3eE.png"
scraper = Scraper()
scraper.get_from_url(url)

raw_jobs = scraper.find_all("li", {"data-city": "Romania"})

jobs = [
    {
        "job_title": job.find("h3", {"class": "careers__jobs-title"}).text,
        "job_link": job.find("a", {"class": "careers__jobs-button"})["href"],
        "company": company,
        "country": "Romania",
        "remote": "Remote",
    }
    for job in raw_jobs
]

publish_or_update(jobs)
publish_logo(company, logo)
show_jobs(jobs)
