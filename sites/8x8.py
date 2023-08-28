import requests
import json
from bs4 import BeautifulSoup
from utils import *

#url = 'https://www.8x8.com/careers?city=cluj-napoca&country=romania'
url = 'https://jobs.lever.co/8x8?location=Cluj-Napoca%2C%20Romania'
company = '8x8'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

job_titles_elements = soup.find_all('h5', attrs={'data-qa': 'posting-name'})
job_titles = [element.text for element in job_titles_elements]

job_links_elements = soup.find_all('a', class_='posting-title')
job_links = [element['href'] for element in job_links_elements]

job_locations = soup.find_all('span', class_='location')
job_locations = [element.text.split(', ') for element in job_locations]

final_jobs = []

for job_title, job_link, job_location in zip(job_titles, job_links, job_locations):
    final_jobs.append(create_job(
            job_title = job_title,
            company = company,
            country = job_location[1],
            city = job_location[0],
            job_link = job_link
        )
    )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/8x8_square_logo.svg/220px-8x8_square_logo.svg.png')

print(json.dumps(final_jobs, indent=4))
