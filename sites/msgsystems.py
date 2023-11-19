import requests
import json
from bs4 import BeautifulSoup
from utils import *
from utils import (translate_city)
from getCounty import (get_county)

url = 'https://www.msg-systems.ro/roluri-disponibile'
company = 'MSGSYSTEMS'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

final_jobs = []

for job_item in soup.find_all('div', class_='job-item'):

    job_title = job_item.find('h3', class_='job-title').text.strip()
    cities = [
        translate_city(city.replace('Tg. ', 'Targu-').strip()) for city in
        job_item.find('div', class_='job-city').text.strip().replace(
            '(sediu central)', '').replace('\u0219', 's').strip().split(',')
    ]
    counties = [get_county(city) for city in cities]

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

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.msg-systems.ro/images/20200219_Logo_msg.svg')

print(json.dumps(final_jobs, indent=4))
