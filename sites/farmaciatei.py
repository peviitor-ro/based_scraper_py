from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'FarmaciaTei'
url = ' https://comenzi.farmaciatei.ro/cariere'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='cariere').find_all('div', class_='card')

i = 0
for job in jobs_elements:
    city_element = job.find('h4').text.split(',')
    try:
        job_element = job.find('div', class_='card-body').find_all('ul')[3].find_all('strong')
    except:
        try:
            job_element = job.find('div', class_='card-body text-success mb-3').find_all('strong')
        except:
            job_element = []

    no_jobs = ["❌"]
    for element in job_element:
        if len(element.text) > 1 and element.text[0] not in no_jobs:
            city = "Romania"
            if len(city_element) > 2:
                city = city_element[-2]

            jobs.append(create_job(
                job_title=element.text,
                job_link=url,
                city=city,
                country="Romania",
                company=company,
            ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://comenzi.farmaciatei.ro/themes/bootstrap5/images/logo.png')
show_jobs(jobs)