from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "Romaero"
url = "https://romaero.com/cariere/locuri-de-munca-romaero/"

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find("table", {"id": "myTable"}).find("tbody").find_all("tr")

for job in range(1, len(jobs_elements)):
    jobs.append(
        create_job(
            job_title=jobs_elements[job].find_all("td")[0].text.strip(),
            job_link=jobs_elements[job].find_all("td")[-1].find("a")["href"],
            city="Bucuresti",
            county="Bucuresti",
            country="Romania",
            company=company,
        )
    )

publish_or_update(jobs)

logo_url = "https://romaero.com/wp-content/uploads/2020/05/LOGO-100-FINAL.png"
publish_logo(company, logo_url)
show_jobs(jobs)
