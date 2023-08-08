import requests
from bs4 import BeautifulSoup
from utils import *

urls = [
    'https://www.ejobs.ro/company/veo/161798',
    'https://www.ejobs.ro/company/veo/161798/2'  # Corrected the missing comma here
]
company = 'VEO'
final_jobs = []

# Loop over each URL in the urls list
for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    job_elements = soup.find('main', class_='CDInner__Main').find_all('div', class_='JobCard')
    
    for job in job_elements:
        job_title = job.find('h2', class_='JCContentMiddle__Title').text.strip()
        job_url = job.find('h2', class_='JCContentMiddle__Title').find('a')['href']
        job_url = 'https://www.ejobs.ro' + job_url
        job_location = job.find('span', class_='JCContentMiddle__Info').text.replace('\u0219', 's').split('si alte')[0].split(',')
        country = 'Romania'
        
        final_jobs.append(
            {
                'job_title': job_title,
                'job_link': job_url,
                'city': job_location,
                'country': country,
                'company': company
            }
        )

# Publish the final_jobs list after processing all URLs
for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/1/161798.png')

print(json.dumps(final_jobs, indent=4))
