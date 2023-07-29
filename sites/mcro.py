import requests
import json
import uuid
import os
from bs4 import BeautifulSoup

company = 'Mcro'
base_url = 'https://mcro.tech'
careers_url = base_url + '/careers/'

response = requests.get(careers_url)
html_markup = response.text

soup = BeautifulSoup(html_markup, 'html.parser')

jobs = soup.find_all('a', class_='job')

final_jobs = []

for job in jobs:
    job_link = job['href']
    job_title = job.find('h4').get_text(strip=True)
    location = job.find('div', class_='job__description--location').find('h5').get_text(strip=True)
    

    # Concatenate base_url with job_link
    full_job_link = base_url + "/" + job_link

    final_jobs.append({
        'id': str(uuid.uuid4()),
        'job_link': full_job_link,
        'job_title': job_title,
        'location': location,
        'company': company
    })

api_key = os.environ.get('Grasum_Key')

clean_data = requests.post('https://api.peviitor.ro/v4/clean/', headers={'Content_Type': 'application/x-www-form-urlencoded', 'apikey': api_key}, data={'company': company})

update_data = requests.post('https://api.peviitor.ro/v4/update/', headers={'Content_Type': 'application/json', 'apikey': api_key}, data=json.dumps(final_jobs))

requests.post('https://api.peviitor.ro/v1/logo/add/', headers={'Content_Type': 'application/json'}, data=json.dumps([{'id': company, 'logo': 'https://www.evozon.com/wp-content/uploads/2021/03/Group-813.svg'}]))

print(json.dumps(final_jobs, indent=4))
