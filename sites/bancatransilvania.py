import requests
from bs4 import BeautifulSoup
from utils import *

company = 'BANCATRANSILVANIA'
urls = [
    'https://www.ejobs.ro/company/banca-transilvania/8092',
    'https://www.ejobs.ro/company/banca-transilvania/8092/2',
    'https://www.ejobs.ro/company/banca-transilvania/8092/3',
]

final_jobs = []

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    job_elements = soup.find('main', class_='CDInner__Main').find_all('div', class_='JobCard')

    final_jobs.extend([
        {
            'job_title': job.find('h2', class_='JCContentMiddle__Title').text.strip(),
            'job_link': 'https://www.ejobs.ro' + job.find('h2', class_='JCContentMiddle__Title').find('a')['href'],
            'job_location': job.find('span', class_='JCContentMiddle__Info').text.replace('\u0219', 's').split('si alte')[0].split(','),
            'country': 'Romania',
            'company': company
        }
        for job in job_elements
    ])


for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.bancatransilvania.ro/themes/bancatransilvania/assets/images/logos/bt-cariere.svg')


print(json.dumps(final_jobs, indent=4))
