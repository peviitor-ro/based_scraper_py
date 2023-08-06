import requests
from bs4 import BeautifulSoup
from utils import *

url = 'https://www.ejobs.ro/company/cartofisserie/286239' 
company = 'CARTOFISSERIE'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

job_elements = soup.find_all('h2', class_='JCContentMiddle__Title')
location_elements = soup.find_all('span', class_='JCContentMiddle__Info')

job_titles = [job.text.strip() for job in job_elements]
job_urls = ['https://www.ejobs.ro' + job.find('a')['href'] for job in job_elements]
locations = []

for location_element in location_elements:
    location = location_element.text.strip()
    location = location.replace('\u0219', 's')
    location = location.split('si alte')[0]
    locations.append(', '.join(location.split(',')[:3]).strip())

seen_jobs = set()
final_jobs = []

for title, url, loc in zip(job_titles, job_urls, locations):
    job_id = (title, url, loc)
    if job_id not in seen_jobs:
        final_jobs.append(
            create_job(
                job_title=title,
                company=company,
                country='Romania',
                city=loc,
                job_link=url
            )
        )
        seen_jobs.add(job_id)

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/2/286239.png')

print(json.dumps(final_jobs, indent=4))
