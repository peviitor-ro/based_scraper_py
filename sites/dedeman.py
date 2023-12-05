import requests
import json
from utils import *
from getCounty import *

url = 'https://recrutare.dedeman.ro/api/sinapsi/jobs'
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

acurate_city = acurate_city_and_county(
    Ramnicu_Valcea={
        "city": "Ramnicu Valcea",
        "county": "Valcea"
    }
)

for job in job_announces:
    city = job['City']
    if acurate_city.get(city.replace('-', '_')):
        county = acurate_city.get(city.replace('-', '_')).get('county')
        city = acurate_city.get(city.replace('-', '_')).get('city')
    else:
        county = get_county(city)

    input_job_id = job['Id']
    format_job_title = '+'.join(job["Function"].lower().split())
    output_job_link = f'https://recrutare.dedeman.ro/detalii-post?job={format_job_title}&id={input_job_id}'
    final_jobs.append(
            create_job(
                job_title = job['Function'],
                company = company,
                city = city,
                county = county,
                country = 'Romania',
                job_link = output_job_link,
            )
        )

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://i.dedeman.ro/dedereact/design/images/logo.svg')

print(json.dumps(final_jobs, indent=4, sort_keys=True)) 
