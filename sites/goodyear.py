from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil

company = 'GoodYear'
url = 'https://jobs.goodyear.com/search/?createNewAlert=false&q=&locationsearch=Romania'

scraper = Scraper()
scraper.get_from_url(url)

totalJobs = int(scraper.find("span", class_ = "paginationLabel").find_all("b")[-1].text.strip())

pages = ceil(totalJobs / 25)

jobs = []

for page in range(1, pages + 1):
    
    jobs_elements = scraper.find('table', id='searchresults').find('tbody').find_all('tr')

    for job in jobs_elements:
        job_link = 'https://jobs.goodyear.com' + job.find('a')['href']
        job_title = job.find('a').text.strip()
        job_location = job.find('span', class_='jobLocation').text.split(',')[0].strip()

        jobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            city=job_location,
            country='Romania',
            company=company,
        ))

    scraper.get_from_url(url + f'&startrow={page * 25}')

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://rmkcdn.successfactors.com/38b5d3dd/ef930ba2-97c9-4abc-a14a-e.png')
show_jobs(jobs)
