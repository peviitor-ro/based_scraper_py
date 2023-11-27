from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city)
from getCounty import get_county, remove_diacritics

company = 'SGS'
url = ' https://api.smartrecruiters.com/v1/companies/sgs/postings?offset='

offset = 0
jobs = []

scraper = Scraper()
while True:
    scraper.get_from_url(url + str(offset), type='JSON')

    if len(scraper.markup['content']) == 0:
        break

    for job in scraper.markup['content']:
        country = ''
        for location in job['customField']:
            if location['fieldId'] == 'COUNTRY':
                country = location['valueLabel']
                break

        job_element = create_job(
            job_title=job['name'],
            job_link='https://jobs.smartrecruiters.com/SGS/'+job['id'],
            city=job['location']['city'],
            country=country,
            company=company,
        )

        if country == 'Romania':
            city = translate_city(
                remove_diacritics(
                   job['location']['city'].replace('Comuna ', '')
                )
            )
            county = get_county(city)

            job_element['city'] = city
            job_element['county'] = county

        jobs.append(job_element)

    offset += 100

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc5/5d946e0d08c63e194f3a018e/huge?r=s3-eu-central-1&_1570091188190')
show_jobs(jobs)
