from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
import urllib.parse

company = 'AHK'
url = 'https://www.ahkrumaenien.ro/ro/cariere/vino-in-echipa-noastra'

scraper = Scraper()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
}
scraper.set_headers(headers)
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='b-page-content b-page-content--main').find_all("section")

for job in jobs_elements:
    job_elem = job.find('header')
    if job_elem:
        link_element = job.find('a', class_='rte_button--colored')
        if link_element:
            parsed = urllib.parse.urlparse(link_element['href'])
            if bool(parsed.netloc):  # The URL is absolute
                job_link = link_element['href']
            else:  # The URL is relative
                job_link = 'https://www.ahkrumaenien.ro' + link_element['href']
        else:
            job_link = None

        jobs.append(create_job(
            job_title=job.find('h3').text,
            job_link=job_link,
            city='Romania',
            country='Romania',
            company=company,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://images.admiralcloud.com/customer_609/cd351ef9-39bc-4e90-8ad6-89a887c05abc?response-content-disposition=inline%3B%20filename%3DAHK-Ro_NEU.svg&Expires=1690980719&Key-Pair-Id=K3XAA2YI8CUDC&Signature=PVTskdmMypVkDOEi3WbNcSGOzyaWbaSimVIXonQjx8clmcajJiq1JN7a8stBGPZ6-MD4uf8GyxHqANtWAwmzWvCEavnKglj6ilw9YygknnkmrBz6iNsUS-O0Jwhxt834PT9D3yvK3QiYDFAJ0p7r6Gk~zKavgyDcrmN2nkvDEnKwwGOYcVwXqT1e2KoVLE5hgg5sIjHEprkDFOpjatmIDc366aoAmhpxk5Ovs5z0hFfJcsWNDilOhAQb1kZfj-ksu0WosO0grpE1Zp3LhRxvLccbHQ2M5deQ73K9imCE7gqLCAXndrs7IxZJCjGcs8-j-4ETt~Lg1o7YVvbA9lz90w__')
show_jobs(jobs)

