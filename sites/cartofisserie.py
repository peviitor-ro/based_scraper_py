import requests
from bs4 import BeautifulSoup
from utils import *
from getCounty import *

url = 'https://www.ejobs.ro/company/cartofisserie/286239'
company = 'CARTOFISSERIE'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

job_elements = soup.find('main', class_='CDInner__Main').find_all('div', class_='JobCard')

final_jobs = []

for job in job_elements:
    job_title = job.find('h2', class_='JCContentMiddle__Title').text.strip()
    job_url = job.find('h2', class_='JCContentMiddle__Title').find('a')['href']
    job_url = 'https://www.ejobs.ro' + job_url
    job_location = job.find('span', class_='JCContentMiddle__Info').text.replace('\u0219', 's').split('si alte')[0].split(',')
    cities = [city.strip() for city in job_location]

    counties = [get_county(city) for city in cities if city]  # List of counties for each city

    country = 'Romania'
    final_jobs.append(
        {
            'job_title': job_title,
            'job_url': job_url,
            'city': cities,
            'county': counties,
            'country': country,
            'company': company
        }
    )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/2/286239.png')

print(json.dumps(final_jobs, indent=4))
