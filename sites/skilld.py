from utils import *
from getCounty import get_county, remove_diacritics
from scraper.Scraper import Scraper

acurete_city = acurate_city_and_county(
    Ilfov= {
        'city': 'Otopeni',
    }
)


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find(
        'meta', {'data-hid': 'cXenseParse:b19-ejobs_city'})['content'].split(',')

    cities = []
    counties = set()

    for location in locations:
        city = translate_city(
            remove_diacritics(
                location.strip()
            ))
        
        if acurete_city.get(city):
            city = acurete_city.get(city)['city']

        county = get_county(city)

        if not county:
            city = location.replace(' ', '-')
            county = get_county(city)

        cities.append(city)
        counties.add(county)

    return cities, counties

url = 'https://www.ejobs.ro/company/skilld-by-ejobs/317733'
company = 'SKILLD'

scraper = Scraper()
scraper.get_from_url(url)

job_elements = scraper.find('main', class_='CDInner__Main').find_all('div', class_='JobCard')

final_jobs = []

for job in job_elements:
    job_title = job.find('h2', class_='JCContentMiddle__Title').text.strip()
    job_url = job.find('h2', class_='JCContentMiddle__Title').find('a')['href']
    job_url = 'https://www.ejobs.ro' + job_url

    locations = job.find(
        'span', class_='JCContentMiddle__Info').text.strip().split(',')

    if 'și alte' in locations[-1]:
        cities, counties = get_aditional_city(job_url)
    else:
        cities = []
        counties = set()

        for location in locations:
            city = translate_city(
                remove_diacritics(
                    location.strip()
                ))
            
            if acurete_city.get(city):
                city = acurete_city.get(city)['city']

            county = get_county(city)

            if not county:
                city = city.replace(' ', '-')
                county = get_county(city)

            cities.append(city)
            counties.add(county)

    final_jobs.append(
            {
                'job_title' : job_title,
                'job_link' : job_url,
                'city' : cities,
                'country' : list(counties),
                'company' : company
            }
    )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/3/317733.png')

print(json.dumps(final_jobs, indent=4))
