from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'KWS'
url = 'https://jobs.kws.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_city=&optionsFacetsDD_department=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield4='

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('table', id='searchresults').find('tbody').find_all('tr')

for job in jobs_elements:
    jobs.append(create_job(
        job_title=job.find('a', class_='jobTitle-link').text,
        job_link='https://jobs.kws.com'+job.find('a', class_='jobTitle-link')['href'],
        city=job.find('span', class_='jobLocation').text.split(',')[0],
        country='Romania',
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://rmkcdn.successfactors.com/26823ea3/7e38ad11-136a-4629-bfec-6.svg')
show_jobs(jobs)