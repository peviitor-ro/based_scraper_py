import requests
from bs4 import BeautifulSoup
from utils import *

company = 'bancatransilvania'
urls = [
    'https://www.ejobs.ro/company/banca-transilvania/8092',
    'https://www.ejobs.ro/company/banca-transilvania/8092/2',
    'https://www.ejobs.ro/company/banca-transilvania/8092/3',
]

final_jobs = []

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    job_elements = soup.find_all('h2', class_='JCContentMiddle__Title')
    location_elements = soup.find_all('span', class_='JCContentMiddle__Info')

    for job_element, location_element in zip(job_elements, location_elements):
        job_title = job_element.text.strip()
        job_url = 'https://www.ejobs.ro' + job_element.find('a')['href']
        location = location_element.text.strip() 
        location = location.replace('\u0219', 's') # replacing ș with s
        locations = ', '.join(location.split(',')[:3]).strip() # get the first three cities


        final_jobs.append(
                create_job(
                    job_title = job_title,
                    company = company,
                    country = 'Romania',
                    city = locations,
                    job_url = job_url
                )
            )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.bancatransilvania.ro/themes/bancatransilvania/assets/images/logos/bt-cariere.svg')


print(json.dumps(final_jobs, indent=4))
