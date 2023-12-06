from scraper_peviitor import Scraper, Rules
from utils import show_jobs, publish, publish_logo

url = "https://www.3pillarglobal.com/career-opportunities/"
company = "3PillarGlobal"
logo = "https://i.imgur.com/SM5d3eE.png"
scraper = Scraper(url)
rules = Rules(scraper)
raw_jobs = rules.getTags("li", {"data-city": "Romania"})
jobs = []

for job in raw_jobs:
    jobs.append({
        "job_title": job.find("h3", {"class": "careers__jobs-title"}).text,
        "job_link": job.find("a", {"class": "careers__jobs-button"})['href'],
        "company": company,
        "country": "Romania",
        "remote": "Remote",
    })

for v in [1, 4]:
    publish(v, company, jobs, "MSCDAVID")

publish_logo(company, logo)
show_jobs(jobs)