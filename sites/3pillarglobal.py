from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, get_jobtype

url = "https://jobs.lever.co/3pillarglobal?location=Romania"
company = "3PillarGlobal"
logo = "https://i.imgur.com/SM5d3eE.png"
scraper = Scraper()
scraper.get_from_url(url)

raw_jobs = scraper.find_all("div", {"class": "posting"})

jobs = [
    {
        "job_title": job.find("h5").text,
        "job_link": job.find("div", {"class": "posting-apply"}).find("a")["href"],
        "company": company,
        "country": "Romania",
        "remote": get_jobtype(job.find("div", {"class": "posting-categories"}).text),
    }
    for job in raw_jobs
]

publish_or_update(jobs)
publish_logo(company, logo)
show_jobs(jobs)

