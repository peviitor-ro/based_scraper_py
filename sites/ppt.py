import requests
from bs4 import BeautifulSoup
from utils import *

url = 'https://www.ejobs.ro/company/preturi-pentru-tine/194591'
company = 'ppt'

final_jobs = []

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

job_elements = soup.find_all('h2', class_='JCContentMiddle__Title')
location_elements = soup.find_all('span', class_='JCContentMiddle__Info')

for job_element, location_element in zip(job_elements, location_elements):
    job_title = job_element.text.strip()
    location = location_element.text.strip()
    location = location.replace('\u0219', 's')
    location = location.split('si alte')[0]
    location = ', '.join(location.split(',')[:3]).strip()
    job_url = 'https://www.ejobs.ro' + job_element.find('a')['href']

    final_jobs.append(
            create_job(
                job_title = job_title,
                company = company,
                country = 'Romania',
                city = location,
                job_link = job_url
            )
        )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/1/194591.png')

print(json.dumps(final_jobs, indent=4))
