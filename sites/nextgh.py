import requests
from bs4 import BeautifulSoup
from utils import *

url = 'https://careers.smartrecruiters.com/NEXT2'
company = 'nextgh'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

final_jobs = []

for job_element in soup.find_all('li', class_='opening-job job column wide-1of2 medium-1of2'):
    job_title = job_element.find('h4', class_='details-title job-title link--block-target').text.strip()
    job_url = job_element.find('a')['href']
    final_jobs.append(create_job(
        job_title = job_title,
        company = company,
        country = 'Romania',
        city = 'Cluj-Napoca',
        job_link = job_url,
        )
    )

for version in [1,4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(company, 'https://scontent.ftsr1-1.fna.fbcdn.net/v/t39.30808-6/271447577_226020786360522_657598264093586690_n.png?_nc_cat=100&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=4fnN6TYDzOAAX8Nblr3&_nc_ht=scontent.ftsr1-1.fna&oh=00_AfAeX3bzkMKDkq8y9yOj0N_D6-ZD_7rqgz5IDEx0W4qnkA&oe=64D1AA45')

print(json.dumps(final_jobs, indent=4))
