from scraper.Scraper import Scraper
from utils import (publish, publish_logo, show_jobs)

company = "evozone"
url = 'https://www.evozon.com/careers/'

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all('div', class_='job-name')

final_jobs = []

for job in jobs:
    a_tag = job.find('a')
    url = a_tag['href']
    job_title = a_tag.get_text(strip=True)

    final_jobs.append({
        'job_link': url,
        'job_title': job_title,
        'city': 'Cluj-Napoca',
        'county': 'Cluj',
        'country': 'Romania',
        'company': company
    })

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(
    company, 'https://www.evozon.com/wp-content/uploads/2021/03/Group-813.svg')
show_jobs(final_jobs)
