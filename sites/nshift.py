from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
import re
import requests

company ='nShift'
url = 'https://cdn.jobylon.com/jobs/companies/890/embed/v1/?target=jobylon-jobs-widget&page_size=100'
pattern = re.compile(r"var html_embed = '(.*?)';")

response = requests.get(url)
html = re.findall(pattern, response.text)[0]
scraper = Scraper(html, 'html.parser')

jobs = []

jobs_elements = scraper.find_all('div', class_='jobylon-job')

for job_element in jobs_elements:

    locations = ['Romania','Buchares']

    location = job_element.find('li', class_='jobylon-location').text.split(':')[1].split(' ')[1].strip()

    if location in locations:
        if location == 'Romania':
            city = 'Bucharest'
        else:
            city = location
            location = 'Romania'
        jobs.append(create_job(
            job_title=job_element.find('div', class_='jobylon-job-title').text.strip(),
            job_link=job_element.find('a', class_='jobylon-apply-btn')['href'],
            city=city,
            country=location,
            company=company,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://media-eu.jobylon.com/CACHE/companies/company-logo/nshift/nshift-gart-lp-logo.1a151e03/2ace39d080af84b6618cdc6fd1b86896.jpg')
show_jobs(jobs)
