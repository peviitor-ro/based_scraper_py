from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'Selgros'
url = 'https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22selgros%22&page=0&pageSize=1000&sort=modifiedDate~DESC'

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = []

for job in scraper.markup['data']['results']:
    try:
        city = job['locations'][0]['name']
    except:
        city = 'Romania'

    jobs.append(create_job(
        job_title=job['jobTitle'],
        job_link='https://selgros.mingle.ro/ro/embed/apply/' + job['publicUid'],
        city=city,
        country='Romania',
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.selgros.ro/themes/contrib/garnet/dist/assets/branding/logo-selgros.svg')
show_jobs(jobs)