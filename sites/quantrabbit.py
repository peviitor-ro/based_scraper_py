import requests
import json
from bs4 import BeautifulSoup
from utils import *

url = 'https://quantrabbit.com/blog/'
company = 'QUANTRABBIT'

final_jobs = []

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

job_elements = soup.find_all('h2', class_='entry-title')

for job in job_elements:
    job_title = job.text.strip()
    job_url = job.a['href']

    final_jobs.append(
        {
            'job_title': job_title,
            'job_url' : job_url,
            'city' : 'Cluj-Napoca',
            'county' : 'Cluj',
            'country' : 'Romania',
            'company' : company
        }
    )

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://quantrabbit.com/wp-content/uploads/2017/09/cropped-Quant-Rabbit-Logo-Final-2.png')

print(json.dumps(final_jobs, indent=4))