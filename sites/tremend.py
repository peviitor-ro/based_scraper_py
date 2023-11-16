import requests
from bs4 import BeautifulSoup
from utils import *
from getCounty import *

url = 'https://tremend.com/careers/'
company = 'tremend'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

final_jobs = []
job_elements = soup.find('div', id='jobs').find_all('div', class_='career-wrapper')

for job in job_elements:
    job_title = job.find('h3').text.strip()
    job_link = 'https://tremend.com/careers/' + job.find('a')['href'].strip('/')
    location_text = job.find('p', id='location-word').text.strip().replace('Location', '').strip()

    is_remote = 'Remote' in location_text
    city = None
    county = None

    if is_remote:
        remote = "Remote"
    else:
        remote = ""
        city = location_text
        if 'Bucharest' in city:
            city = city.replace('Bucharest', 'Bucuresti')
        county = get_county(city) if city else None

    final_jobs.append(
        {
            'job_title': job_title,
            'job_link': job_link,
            'country': 'Romania',
            'company': company,
            'remote': remote
        }
    )
    if city:
        final_jobs[-1]['city'] = city
        final_jobs[-1]['county'] = county

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.drupal.org/files/styles/grid-4-2x/public/logo%20Tremend%20480%20x480.png')

print(json.dumps(final_jobs, indent=4))