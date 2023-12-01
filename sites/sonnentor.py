from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'SonnentoR'
jobs = []

url = 'https://www.sonnentor.ro/despre-noi/cariere.html'

scraper = Scraper()
scraper.get_from_url(url)

jobs_elements = scraper.find('section', class_='js-go-to-link').find_all('div', class_='row')

for job in jobs_elements:
    jobs.append(create_job(
        company=company,
        job_title=job.find('a').text.strip(),
        job_link=job.find('a')['href'],
        city='Reghin',
        county='Mures',
        country='Romania'
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.sonnentor.ro/pub/static/version1690913752/frontend/sonnentor/ultimate/ro_RO/images/logo.png')
show_jobs(jobs)
