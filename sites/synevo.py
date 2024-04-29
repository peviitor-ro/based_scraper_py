from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs

url = "https://www.synevo.ro/cariere/"
scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("a", {"class": "jobContainer"})

company = {"company": "Synevo"}
finaljobs = list()

for job in jobs:
    job_title = job.text.strip()
    job_link = job["href"]

    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania"
        }
    )

publish_or_update(finaljobs)

logourl = "https://www.synevo.ro/wp-content/themes/synevo-sage/dist/images/synevo-logo_6edc429f.svg"
publish_logo(company.get("company"), logourl)

show_jobs(finaljobs)
