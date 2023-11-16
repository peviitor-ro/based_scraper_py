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

    location_info = job.find('span', class_='JCContentMiddle__Info')
    city_parts = location_info.get_text(separator=',').split(',')

    cities = []
    for part in city_parts:
        part = part.strip().replace('\u0218', 'S').replace('\u0219', 's')
        if part and not any(word in part for word in ['orase', 'si alte']) and not part.isdigit():
            cities.append(part)

    additional_cities_span = location_info.find('span', class_='PartialList__Rest')
    if additional_cities_span and additional_cities_span.has_attr('title'):
        additional_cities = additional_cities_span['title'].split(',')
        for city in additional_cities:
            city = city.strip().replace('\u0218', 'S').replace('\u0219', 's')
            if city and not any(word in city for word in ['orase', 'si alte']) and not city.isdigit():
                cities.append(city)

    counties = [get_county(city) for city in cities if city]

    country = 'Romania'
    final_jobs.append(
        {
            'job_title': job_title,
            'job_url': job_url,
            'city': ", ".join(cities),
            'county': ", ".join([county for county in counties if county is not None]),
            'country': country,
            'company': company
        }
    )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/2/286239.png')

print(json.dumps(final_jobs, indent=4))
