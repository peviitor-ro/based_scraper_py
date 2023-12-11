from scraper.Scraper import Scraper
from utils import translate_city, publish, publish_logo, show_jobs, acurate_city_and_county
from getCounty import get_county, remove_diacritics

acurate_city = acurate_city_and_county(
    Iasi={
        'city': 'Iasi',
        'county': 'Iasi'
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
        
        if acurate_city.get(city):
            city = acurate_city.get(city)['city']
            county = acurate_city.get(city)['county']
        else:
            county = get_county(city)

        cities.append(city)
        counties.add(county)

    return cities, counties

url = 'https://www.ejobs.ro/company/veo/161798'
page = 1

company = 'VEO'
final_jobs = []

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find(
    'main', class_='CDInner__Main').find_all('div', class_='JobCard')

while jobs:   
    for job in jobs:
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
                
                if acurate_city.get(city):
                    city = acurate_city.get(city)['city']
                    county = acurate_city.get(city)['county']
                else:
                    county = get_county(city)

                if not county:
                    city = city.replace(' ', '-')
                    county = get_county(city)

                cities.append(city)
                counties.add(county)
        
        final_jobs.append(
            {
                'job_title': job_title,
                'job_link': job_url,
                'city': cities,
                'county': list(counties),
                'company': company,
                'country': 'Romania'
            }
        )

    page += 1
    scraper.get_from_url(url + '/' + str(page))
    jobs = scraper.find(
        'main', class_='CDInner__Main').find_all('div', class_='JobCard')

# Publish the final_jobs list after processing all URLs
for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://content.ejobs.ro/img/logos/1/161798.png')

show_jobs(final_jobs)
