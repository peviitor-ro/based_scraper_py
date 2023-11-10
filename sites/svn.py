from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city, acurate_city_and_county)
from getCounty import get_county

company = 'SVN'
url = 'https://jobs.svn.ro/posturi-vacante.html'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='jobs').find_all('div', class_='job')

for job in jobs_elements:
    job_title=job.find('h3').text
    job_link='https://jobs.svn.ro' + job.find('a')['href']
    city=translate_city(job.find('ul').find_all('li')[-1].text).replace("È", "s")
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

publish_logo(company, 'https://www.svn.ro/assets/images/logo/3.png')
show_jobs(jobs)