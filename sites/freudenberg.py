from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'Freudenberg'
url = 'https://jobs.freudenberg.com/Freudenberg/ro/?company=FPM&location=RO'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='jobs').find_all('div', class_='job')

for job in jobs_elements:
    jobs.append(create_job(
        job_title=job.find('div', class_='jobtitle').text,
        job_link='https://jobs.freudenberg.com/freudenberg/job/ro/details/'+ job.find('span')['id'],
        city=job.find('div', class_='location').text.split(',')[0],
        country="Romania",
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://jobs.freudenberg.com/Freudenberg/static/img/logo.svg')
show_jobs(jobs)