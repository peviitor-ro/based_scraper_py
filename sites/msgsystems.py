from scraper.Scraper import Scraper
from utils import publish_logo, publish_or_update, translate_city, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
url = 'https://www.msg-systems.ro/roluri-disponibile'
company = 'MSGSYSTEMS'

scraper = Scraper()
scraper.get_from_url(url)

final_jobs = []

for job_item in scraper.find_all('div', class_='job-item'):

    job_title = job_item.find('h3', class_='job-title').text.strip()
    cities = [
        translate_city(city.replace('Tg. ', 'Targu-').strip()) for city in
        job_item.find('div', class_='job-city').text.strip().replace(
            '(sediu central)', '').replace('\u0219', 's').strip().split(',')
    ]
    counties = []

    for city in cities:
        counties.extend(_counties.get_county(city) or [])

    relative_link = job_item.find('a')['href']
    job_link = f'https://www.msg-systems.ro{relative_link}'

    final_jobs.append({
        'job_title': job_title,
        'job_link': job_link,
        'city': cities,
        'county': counties,
        'country': 'Romania',
        'company': company
    })

publish_or_update(final_jobs)

publish_logo(company, 'https://www.msg-systems.ro/images/20200219_Logo_msg.svg')
show_jobs(final_jobs)
