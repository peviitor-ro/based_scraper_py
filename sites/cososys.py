import json
import requests
from utils import *


url = 'https://apply.workable.com/api/v3/accounts/cososys/jobs'
company = 'Cososys'

data = {
        "query":"",
        "location":[{
            "country": "Romania",
            "countryCode":"RO",
            }],
        "department":[],"worktype":[],"remote":[]
        }

response = requests.post(url, json=data).json()['results']

final_jobs = []

for job in response:
    final_jobs.append(
        create_job(
            job_title = job['title'], 
            company = company,
            country = job['location']['country'],
            city = "Cluj-Napoca",
            job_link = 'https://apply.workable.com/cososys/j/' + job['shortcode']
            )
        )
for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://www.endpointprotector.com/images/img/site/endpoint-protector-by-cososys-logo.svg')
show_jobs(final_jobs)
