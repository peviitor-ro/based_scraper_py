from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil

company = 'SiemensHealthineers'
url = 'https://jobs.siemens-healthineers.com/api/apply/v2/jobs?domain=siemens.com&start=1&num=10&exclude_pid=563156116052044&location=Romania&pid=563156116052044&domain=siemens.com&sort_by=relevance'

scraper = Scraper()
scraper.get_from_url(url, type='JSON')

jobs = []

step = 10
total_jobs = scraper.markup['count']

pages = ceil(int(total_jobs) / step)

for page in range(pages):
    url = f'https://jobs.siemens-healthineers.com/api/apply/v2/jobs?domain=siemens.com&start={page * step}&num={page * step + step}&exclude_pid=563156116052044&location=Romania&pid=563156116052044&domain=siemens.com&sort_by=relevance'
    scraper.get_from_url(url, type='JSON')

    for job in scraper.markup['positions']:
        jobs.append(create_job(
            job_title=job['name'],
            job_link=job['canonicalPositionUrl'],
            city=job['location'].split(',')[0],
            country="Romania",
            company=company,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://static.vscdn.net/images/careers/demo/siemens/1677769995::Healthineers+Logo+2023')
show_jobs(jobs)