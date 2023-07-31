from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'Cat'
url = 'https://www.bm-cat.com/ro-ro/articole/resurse-umane'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='three').find_all('li')

for job in jobs_elements:  
    jobs.append(create_job(
        job_title=job.find('a').text,
        job_link=job.find('a')['href'],
        city='Romania',
        country='Romania',
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.bm-cat.com/ro-ro/sites/all/themes/custom/theme_brg/logo.png')
show_jobs(jobs)