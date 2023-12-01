from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city)
from getCounty import get_county
from math import ceil

company = 'SiemensHealthineers'
url = 'https://jobs.siemens-healthineers.com/api/apply/v2/jobs?domain=siemens.com&profile=&query=Romania&location=Romania&pid=563156116352285&domain=siemens.com&sort_by=relevance&triggerGoButton=true'

scraper = Scraper()
scraper.get_from_url(url, type='JSON')

jobs = []

step = 10
total_jobs = scraper.markup['count']

pages = ceil(int(total_jobs) / step)

for page in range(pages ):
    for job in scraper.markup['positions']:
        cities = [
            translate_city(city.split(',')[0].replace('?', 's').replace(' ', '-')) for city in job['locations']
            ]
        counties = [
            get_county(city) for city in cities
        ]
        jobs.append(create_job(
            job_title=job['name'],
            job_link=job['canonicalPositionUrl'],
            city=cities,
            county=counties,
            country="Romania",
            company=company,
            remote=job['work_location_option'].title()
        ))
    url = f'{url}&start={page * step}&num={page * step + step}'
    scraper.get_from_url(url, type='JSON')

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://static.vscdn.net/images/careers/demo/siemens/1677769995::Healthineers+Logo+2023')
show_jobs(jobs)