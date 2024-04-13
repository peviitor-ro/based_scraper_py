from scraper.Scraper import Scraper
from utils import create_job, publish_logo, publish_or_update, show_jobs

company = "AllianzTiriac"

url = "https://www.allianztiriac.ro/ro_RO/cariere/cariere-posturi-disponibile.html#TabVerticalNegative11694447096"

scraper = Scraper()
scraper.get_from_url(url)

jobs_titles = scraper.find("div", class_="c-tabs__content").find_all(
    "h1", class_="c-heading--subsection-large"
)
jobs_links = scraper.find("div", class_="c-tabs__content").find_all(
    "a", class_="c-link"
)
jobs_elements = tuple(zip(jobs_titles, jobs_links))

jobs = [
    create_job(
        job_title=job[0].text.strip(),
        job_link="https://www.allianztiriac.ro" + job[1]["href"],
        country="Romania",
        city="Bucuresti",
        county="Bucuresti",
        company=company,
    )
    for job in jobs_elements
]


publish_or_update(jobs)

publish_logo(
    company,
    "https://www.allianztiriac.ro/content/dam/onemarketing/cee/azro/media/logo_azt/allianz_tiriac_logo.png",
)
show_jobs(jobs)
