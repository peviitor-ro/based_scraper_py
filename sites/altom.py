from bs4 import BeautifulSoup
import requests
import json
import uuid
import os
from getCounty import *

session = requests.session()
def get_data():
    # URL for the data
    url = 'https://www.altom.com/jobs/'

    # Get the data
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('article', class_='job')
    

    final_jobs = []

    # Create a list for the data
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find('h2', class_='job-title').text.strip()
        job_link = job.find('h2', class_='job-title').find('a').get('href')
        job_city = job.find('p', class_='job-feed-meta').text.strip()
        county = get_county(job_city)
        final_jobs.append({'id': str(id),
                            'job_title': job_title, 
                            'job_link': job_link,
                            'city': job_city,
                            'county': county,
                            'country': 'Romania',
                            'company': 'altom'})
    return final_jobs
data = get_data()

api_key = os.environ.get('Grasum_Key')

clean_data = requests.post('https://api.peviitor.ro/v4/clean/', headers={'Content_Type': 'application/x-www-form-urlencoded', 'apikey': api_key}, data={'company': 'altom'})

update_data = requests.post('https://api.peviitor.ro/v4/update/', headers={'Content_Type': 'application/json', 'apikey': api_key}, data=json.dumps(data))

requests.post('https://api.peviitor.ro/v1/logo/add/', headers={'Content_Type': 'application/json'}, data=json.dumps({'id': 'altom', 'logo': 'https://altom.com/app/themes/altom-sage-theme/dist/images/logo-altom_60516779.png'}))

print(json.dumps(data, indent=4))
