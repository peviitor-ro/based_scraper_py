import requests
import json
from utils import *

url = 'https://recrutare.dedeman.ro/sinapsi-jobannounceswithfilter/'
company = 'DEDEMAN'

data = {
    'request': {
        'JobAnnounces': [
            {
                'Id': '',
                'Function': '',
                'City': '',
            }
        ]
    }
}

response_data = requests.post(url, json=data).json()
job_announces = response_data['d']['JobAnnounces']

final_jobs = []

for job in job_announces:
    final_jobs.append(
            create_job(
                job_title = job['Function'],
                company = company,
                city = job['City'],
                country = 'Romania',
                job_link = 'https://recrutare.dedeman.ro/detalii-post.php?id=' + job['Id']
            )
        )

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://i.dedeman.ro/dedereact/design/images/logo.svg')

print(json.dumps(final_jobs, indent=4, sort_keys=True)) 
