import requests
import json
from bs4 import BeautifulSoup
from utils import *

urls = [
    'https://www.fortech.ro/job-openings/',
    'https://www.fortech.ro/job-openings/page/2/',
]
company = 'FORTECH'

final_jobs = []

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    job_elements = soup.find('div', class_='cards fortech-cards')

    for job in job_elements:
        job_link = job.find('a')
        if job_link and 'title' in job_link.attrs:
            job_title = job_link['title']
            job_url = job_link['href']        

            final_jobs.append(
                {
                    'job_title' : job_title,
                    'job_url' : job_url,
                    'remote' : 'remote',
                    'city' : 'Cluj-Napoca',
                    'county': 'Cluj',
                    'country' : 'Romania',
                    'company' : company
                }
            )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.fortech.ro/wp-content/themes/fresh-fortech/dist/images/logo-blue.png?v=1')

print(json.dumps(final_jobs, indent=4))