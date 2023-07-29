from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'SNCLavalin'
url = 'https://careers.snclavalin.com/jobs?options=6477&page=1'

scraper = Scraper()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
scraper.set_headers(headers)
scraper.get_from_url(url)

jobs = []
jobs_elements = scraper.find_all('div', class_='attrax-vacancy-tile')

for job in jobs_elements:
    jobs.append(create_job(
        job_title=job.find('a', class_='attrax-vacancy-tile__title').text.strip(),
        job_link='https://careers.snclavalin.com'+job.find('a', class_='attrax-vacancy-tile__title')['href'],
        city=job.find('div', class_='attrax-vacancy-tile__option-location-valueset').text.strip(),
        country='Romania',
        company=company,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://attraxcdnprod1-freshed3dgayb7c3.z01.azurefd.net/1481103/1e2dbbdd-b55c-47cb-941b-4ecd47e8f5ef/2023.17000.541/Blob/img/snc-logo.png')
show_jobs(jobs)