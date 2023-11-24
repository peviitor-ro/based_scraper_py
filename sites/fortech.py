from scraper.Scraper import Scraper
from utils import (publish, publish_logo, show_jobs)

page = 1
url = f'https://www.fortech.ro/job-openings/page/{page}/'
company = 'FORTECH'

final_jobs = []


scraper = Scraper()
scraper.get_from_url(url)

job_elements = scraper.find('div', class_='cards').find_all(
    'div', class_='card-wrapper')

while job_elements:
    for job in job_elements:
        job_link = job.find('a')
        if job_link:
            job_title = job_link['title']
            job_url = job_link['href']
            final_jobs.append(
                {
                    'job_title': job_title,
                    'job_link': job_url,
                    'remote': ['Hybrid', 'Remote', 'On-site'],
                    'country': 'Romania',
                    'company': company
                }
            )

    page += 1
    url = f'https://www.fortech.ro/job-openings/page/{page}/'
    scraper.get_from_url(url)
    job_elements = scraper.find('div', class_='cards fortech-cards')

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(
    company, 'https://www.fortech.ro/wp-content/themes/fresh-fortech/dist/images/logo-blue.png?v=1')

show_jobs(final_jobs)
