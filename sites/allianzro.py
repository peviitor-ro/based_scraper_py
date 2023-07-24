from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import json
import uuid
import os

def parse_sitemap(url):
    response = requests.get(url)

    # check the response status code, 200 means OK
    if response.status_code == 200:
        # parse the sitemap XML
        sitemap = BeautifulSoup(response.content, 'xml')
        urls = [element.text for element in sitemap.find_all('loc') if 'cariere-posturi-disponibile/' in element.text]
        return urls

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_title = soup.select_one('h1.c-heading')
    job_title = job_title.text.strip() if job_title else None
    job_location = soup.select_one('h5.c-heading')
    job_location = job_location.text.strip() if job_location else None
    job_url = soup.find_all("a", class_="c-link c-link--block c-link--icon-right")

    if job_url:
        relative_url = job_url.get('href')
        job_link = urljoin(url, relative_url)

    else:
        job_url = None

    return job_title, job_location, job_url

sitemap_url = 'https://www.allianztiriac.ro/sitemap.xml'
urls = parse_sitemap(sitemap_url)

final_jobs = []
for url in urls:
    title, location, link = scrape_data(url)
    id = uuid.uuid4()
    final_jobs.append({
        'id': str(id),
        'job_title': title,
        'job_link': link,
        'job_location': location,
        'job_city': 'Bucuresti',
         })
    return final_jobs

api_key = os.environ.get('Grasum_Key')

clean_data = requests.post('https://api.peviitor.ro/v4/clean/', headers={'Content_Type': 'application/x-www-form-urlencoded', 'apikey': api_key}, data={'company': 'allianztiriac'})

update_data = requests.post('https://api.peviitor.ro/v4/update/', headers={'Content_Type': 'application/json', 'apikey': api_key}, data=json.dumps(data))

requests.post('https://api.peviitor.ro/v1/logo/add/', headers={'Content_Type': 'application/json'}, data=json.dumps({'id': 'allianztiriac', 'logo': 'https://www.allianztiriac.ro/content/dam/onemarketing/cee/azro/media/logo_azt/allianz_tiriac_logo.png'}))

print(json.dumps(data, indent=4))

