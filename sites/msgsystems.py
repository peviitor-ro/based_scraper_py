import requests
import json
from bs4 import BeautifulSoup
from utils import *

url = 'https://www.msg-systems.ro/roluri-disponibile'
company = 'MSGSYSTEMS'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

final_jobs = []

for job_item in soup.find_all('div', class_='job-item'):

    job_title = job_item.find('h3', class_='job-title').text.strip()
    job_city = job_item.find('div', class_='job-city').text.strip().replace('(sediu central)', '').replace('\u0219', 's').strip()
    relative_link = job_item.find('a')['href']
    job_link = f'https://www.msg-systems.ro{relative_link}'
    
    final_jobs.append({
        'job_title': job_title,
        'job_link': job_link,
        'job_location': job_city,
        'country': 'Romania',
        'company': company
    })

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.msg-systems.ro/images/20200219_Logo_msg.svg')

print(json.dumps(final_jobs, indent=4))
print(len(final_jobs))
