import requests
import json
import uuid
import os
from bs4 import BeautifulSoup

company = "evozone"
url = 'https://www.evozon.com/careers/'

response = requests.get(url)
html_markup = response.text

soup = BeautifulSoup(html_markup, 'html.parser')

jobs = soup.find_all('div', class_='job-name')

final_jobs = []

for job in jobs:
    a_tag = job.find('a')
    url = a_tag['href']
    job_title = a_tag.get_text(strip=True)
    
    final_jobs.append({
        'id': str(uuid.uuid4()),
        'job_link': url,
        'job_title': job_title,
        'city': 'Cluj-Napoca',
        'country': 'Romania',
        'company': company
    })

api_key = os.environ.get('Grasum_Key')

clean_data = requests.post('https://api.peviitor.ro/v4/clean/', headers={'Content_Type': 'application/x-www-form-urlencoded', 'apikey': api_key}, data={'company': company})

update_data = requests.post('https://api.peviitor.ro/v4/update/', headers={'Content_Type': 'application/json', 'apikey': api_key}, data=json.dumps(final_jobs))

requests.post('https://api.peviitor.ro/v1/logo/add/', headers={'Content_Type': 'application/json'}, data=json.dumps([{'id': company, 'logo': 'https://www.evozon.com/wp-content/uploads/2021/03/Group-813.svg'}]))

print(json.dumps(final_jobs, indent=4))
