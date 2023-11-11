import requests
import json
from utils import *

url = 'https://recrutare.dedeman.ro/api/sinapsi/jobs'
company = 'DEDEMAN'

data = {
    'request': {
        'JobAnnounces': [
            {
                'Id': 'specific_id_value',
                'Function': 'specific_function_value',
                'City': 'specific_city_value',
                'WorkingPoint': 'specific_point_value'
            }
        ]
    }
}

response_data = requests.post(url, json=data).json()

if 'd' in response_data and 'JobAnnounces' in response_data['d']:
    job_announces = response_data['d']['JobAnnounces']

    final_jobs = []

    for job in job_announces:
        final_jobs.append(
            create_job(
                job_title=job['Function'],
                company=company,
                city=job['City'],
                country='Romania',
                job_link='https://recrutare.dedeman.ro/detalii-post?id=' + job['Id']
            )
        )

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://i.dedeman.ro/dedereact/design/images/logo.svg')