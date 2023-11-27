from scraper.Scraper import Scraper
from utils import (create_job, publish_logo, publish, show_jobs)

company = "AllianzTiriac"

url = "https://www.allianztiriac.ro/ro_RO/cariere/cariere-posturi-disponibile.html#TabVerticalNegative11694447096"

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_titles = scraper.find("div", class_="c-tabs__content").find_all("h1", class_="c-heading--subsection-large")
jobs_links = scraper.find("div", class_="c-tabs__content").find_all("a", class_="c-link")
jobs_elements = tuple(zip(jobs_titles,jobs_links))

for job in jobs_elements:
    jobs.append(
        create_job(
            job_title=job[0].text.strip(),
            job_link="https://www.allianztiriac.ro" + job[1]["href"],
            country="Romania",
            city="Bucuresti",
            county="Bucuresti",
            company=company
        )
    )

for version in [1,4]:
    publish(version,company, jobs, "APIKEY")

publish_logo(company, "https://www.allianztiriac.ro/content/dam/onemarketing/cee/azro/media/logo_azt/allianz_tiriac_logo.png")
show_jobs(jobs)
