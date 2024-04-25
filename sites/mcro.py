from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty

_counties = GetCounty()
company = 'Mcro'
base_url = 'https://mcro.tech'
careers_url = base_url + '/careers/'

scraper = Scraper()
soup = scraper.get_from_url(careers_url)

jobs = scraper.find_all('a', class_='job')

final_jobs = []

for job in jobs:
    job_link = job['href']
    job_title = job.find('h4').get_text(strip=True)
    location_slpit = job.find('div', class_='job__description--location').find('h5').get_text(strip=True).split(',')
    location_city = location_slpit[0]
    location_country = location_slpit[1].split('|')[0].strip()

    city = translate_city(location_city)
    county = _counties.get_county(city)
    remote = location_slpit[1].split('|')[1].strip()

    full_job_link = base_url + "/" + job_link

    final_jobs.append({
        'job_link': full_job_link,
        'job_title': job_title,
        'city': location_city,
        'county': county,
        'remote': remote,
        'country': location_country,
        'company': company
    })

publish_or_update(final_jobs)

publish_logo(company, 'https://mcro.tech/static/mcro-unicorn-logo-24cdacabaf115019db9895d78b862afb.svg')
show_jobs(final_jobs)

