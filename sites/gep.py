from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'GEP'
url = 'https://jobseurope-gep.icims.com/jobs/search?ss=1&searchRelation=keyword_all&searchLocation=13526--Cluj&in_iframe=1'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []
jobs_elements = scraper.find('div', class_='iCIMS_JobsTable').find_all('div', class_='row')

for job in jobs_elements:
    jobs.append(create_job(
        job_title=job.find('div', class_='title').text.strip().replace('Title\n\n', ''),
        job_link=job.find('a', class_='iCIMS_Anchor')['href'],
        city='Cluj-Napoca',
        country='Romania',
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://gep.icims.com/icims2/servlet/icims2?module=AppInert&action=download&id=96578&hashed=855987836')
show_jobs(jobs)
