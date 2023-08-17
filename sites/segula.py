from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

company = 'Segula'
jobs = []

url = 'https://careers.segulatechnologies.com/wp/wp-admin/admin-ajax.php'

payload = {
    'action':'sgl_jobs_ajax',''
    'limit':10000
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

scraper = Scraper()
scraper.set_headers(headers)
response = scraper.post(url, data=payload)

for job in response.json()['data']['jobs']:
    jobs.append(create_job(
        company = company,
        job_title = job['title'],
        job_link = job['link'],
        city = job['city'],
        country = job['country'],
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://careers.segulatechnologies.com/app/themes/segula/library/medias/images/logo-blue.png')
show_jobs(jobs)
