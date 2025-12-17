from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs
import time

company = "SonnentoR"
jobs = []

url = "https://www.sonnentor.ro/despre-noi/cariere.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.sonnentor.ro/",
}

scraper = Scraper()
scraper.set_headers(headers)

# Delay anti-bot
time.sleep(2)

scraper.get_from_url(url)

jobs_elements = scraper.find_all(
    "section",
    class_="img-text-teaser__body img-text-teaser__body--papercut js-go-to-link img-text-teaser__body--papercut-right img-text-teaser__body--red"
)

print(f"Found {len(jobs_elements)} jobs")

for job in jobs_elements:
    a = job.find("a")
    if not a:
        continue

    jobs.append(
        create_job(
            company=company,
            job_title=a.text.strip(),
            job_link=a["href"],
            city="Reghin",
            county="Mures",
            country="Romania",
        )
    )

# publish_or_update(jobs)
# publish_logo(
#     company,
#     "https://www.sonnentor.ro/pub/static/version1690913752/frontend/sonnentor/ultimate/ro_RO/images/logo.png",
# )
# show_jobs(jobs)
