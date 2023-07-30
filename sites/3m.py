from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil
import json

company = '3M'
url = 'https://3m.wd1.myworkdayjobs.com/wday/cxs/3m/Search/jobs'

post_data = {
    "appliedFacets":{
        "Location_Country":["f2e609fe92974a55a05fc1cdc2852122"]
        },
        "limit":20,
        "offset":0,
        "searchText":""
    }

headers = {
    'Content-Type': 'application/json'
}

jobs = []

scraper = Scraper()
scraper.set_headers(headers)
obj = scraper.post(url, json.dumps(post_data))
step = 20
total_jobs = obj.json()['total']
pages = ceil(total_jobs / step)

for pages in range(0, pages):
    if pages > 1:
        post_data['offset'] = pages * step
        obj = scraper.post(url, json.dumps(post_data))

    for job in obj.json()['jobPostings']:
        jobs.append(create_job(
            job_title=job['title'],
            job_link='https://3m.wd1.myworkdayjobs.com/en-US/Search'+job['externalPath'],
            city='Romania',
            country='Romania',
            company=company,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.3m.com.ro/3m_theme_assets/themes/3MTheme/assets/images/unicorn/Logo.svg')
show_jobs(jobs)