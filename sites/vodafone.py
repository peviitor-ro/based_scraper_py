import requests
import re
from utils import *

# List of sitemap URLs
sitemap_urls = [
    "https://jobs.vodafone.com/careers/sitemap_cat.txt?domain=vodafone.com",  
    "https://jobs.vodafone.com/careers/sitemap.txt?domain=vodafone.com",
]

company = 'Vodafone'

final_jobs = []

for sitemap_url in sitemap_urls:
    response = requests.get(sitemap_url)

    # split the response text by newline to get a list of URLs
    urls = response.text.split('\n')

    # filter and print URLs containing '-rou?'
    for url in urls:
        if '-rou?' in url:
            job_part = url.split('/')[-1]
            job_title_parts = job_part.split('-')[1:-3]
            job_title = ' '.join([word.capitalize() for word in job_title_parts])

            final_jobs.append(create_job(
                job_title = job_title,
                company = company,
                country = 'Romania',
                city = 'Bucharest',
                job_link = url
            ))

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://static.vscdn.net/images/careers/demo/eightfolddemo-vodafone2/8d898eb4-685e-441a-9b64-9.png')

print(json.dumps(final_jobs, indent=4))
