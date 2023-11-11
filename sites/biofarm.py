from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city)
from getCounty import get_county

company = 'Biofarm'
url = 'https://mingle.ro/api/boards/mingle/jobs?q=companyUid~eq~%22biofarm%22&page=0&pageSize=1000&sort=modifiedDate~DESC'

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = []

for job in scraper.markup['data']['results']:
    if job['locations']:
        job_title=job['jobTitle']
        job_link='https://biofarm.mingle.ro/ro/embed/apply/' + job['publicUid']
        city = translate_city(job['locations'][0]['name'])
        county = get_county(city)

        jobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            company=company,
            country="Romania",
            city=city,
            county=county,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.biofarm.ro/wp-content/uploads/2019/10/logo.png')
show_jobs(jobs)