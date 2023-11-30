from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

url = "https://www.fgaromania.ro/category/cariere/"

company = "fga"
jobs = []

scraper = Scraper()
scraper.get_from_url(url)

jobs_elements = scraper.find_all("article", class_="single-hentry")

for job in jobs_elements:
    jobs.append(create_job(
        job_title=job.find("h2", class_="entry-title").text.strip(),
        job_link=job.find("h2", class_="entry-title").a["href"],
        company=company,
        country="Romania",
        city="Bucuresti",
        county="Bucuresti",
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.fgaromania.ro/wp-content/uploads/2020/06/logo-FGA.png')
show_jobs(jobs)
