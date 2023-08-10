from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'Romaero'
url = 'https://romaero.com/cariere/locuri-de-munca-romaero/'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []



jobs_elements = scraper.find("table", {"id": "myTable"}).find("tbody").find_all("tr")

for job in range(1, len(jobs_elements)):
    jobs.append(create_job(
        job_title=jobs_elements[job].find_all("td")[0].text.strip(),
        job_link=jobs_elements[job].find_all("td")[-1].find("a")["href"],
        city='Bucuresti',
        country='Romania',
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

show_jobs(jobs)

