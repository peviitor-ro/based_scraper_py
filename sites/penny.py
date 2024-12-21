from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs

url = "https://cariere.penny.ro"
scraper = Scraper()
scraper.get_from_url(url)

pageNum = 1

jobs = scraper.find_all("li", {"class": "list-group-item"})

company = {"company": "Penny"}
finalJobs = list()

idx = 0

for job in jobs:
    job_title = job.text.strip()
    job_link = url + "#" + str(idx)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
        }
    )
    idx += 1


publish_or_update(finalJobs)

logo_url = "https://cariere.penny.ro/wp-content/themes/penny_cariere/img/logo.jpg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
