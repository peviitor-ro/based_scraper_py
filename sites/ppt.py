import requests
from bs4 import BeautifulSoup
from utils import *
from getCounty import *

url = 'https://www.ejobs.ro/company/preturi-pentru-tine/194591'
company = 'PPT'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

job_elements = soup.find('main', class_='CDInner__Main').find_all('div', class_='JobCard')

final_jobs = []
counties = []

for job in job_elements:
    job_title = job.find('h2', class_='JCContentMiddle__Title').text.strip()
    job_url = job.find('h2', class_='JCContentMiddle__Title').find('a')['href']
    job_url = 'https://www.ejobs.ro' + job_url
    job_location = job.find('span', class_='JCContentMiddle__Info').text.replace('\u0219', 's').split('si alte')[0].split(',')
    clean_job_location = [city.strip() for city in job_location]

    counties = []
    for city in clean_job_location:
        if city:
            county = get_county(city)
            counties.append(county)
        else:
            counties.append(None)

    country = 'Romania'
    company = company
    final_jobs.append(
        {
            'job_title': job_title,
            'job_link': job_url,
            'city': clean_job_location,
            'country': country,
            'county': counties,
            'company': company
        }
    )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/1/194591.png')

print(json.dumps(final_jobs, indent=4))
