import requests
import json
from bs4 import BeautifulSoup
from utils import *

url = 'https://tremend.com/careers/'
company = 'tremend'

final_jobs = []

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

job_elements = soup.find('div', id='jobs')

for job in job_elements.find_all('div', class_='career-wrapper'):
    job_title = job.find('h3').text
    job_link = url + job.find('a')['href']
    city = job.find('p', id='location-word').text.strip().replace('Location', '').strip()
    remote = False
    if city == 'Remote':
        remote = True
    else :
        try:
            city = city.split(',')[1]
            remote = True
        except:
            city = city
    if remote :
        final_jobs.append(
            create_job(
                job_title = job_title,
                job_link = job_link,
                country = 'Romania',
                remote = 'Remote'
            )
        )
    else:
        final_jobs.append(
            create_job(
                job_title = job_title,
                job_link = job_link,
                city = city,
                country = 'Romania'
            )
        )
for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.drupal.org/files/styles/grid-4-2x/public/logo%20Tremend%20480%20x480.png')

print(json.dumps(final_jobs, indent=4))