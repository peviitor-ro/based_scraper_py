from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)

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
        jobs.append(create_job(
            job_title=job.find('h3').text,
            job_link='https://www.ahkrumaenien.ro' + job.find('a', class_='rte_button--colored')['href'],
            city='Romania',
            country='Romania',
            company=company,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://images.admiralcloud.com/customer_609/cd351ef9-39bc-4e90-8ad6-89a887c05abc?response-content-disposition=inline%3B%20filename%3DAHK-Ro_NEU.svg%3B%20filename*%3DUTF-8%27%27AHK-Ro_NEU.svg&Expires=1690801319&Key-Pair-Id=K3XAA2YI8CUDC&Signature=ehlSUkjHphrbNCE-qIc1eNv6G7n9w8diW1rhikXhRH~xGM00XcmLE3GK754tee2Hu-n7F37r1qbP6hA2tdxft5loSASZlZBah0TDNmrGmV2mkB5tMRHlnoQ3K52mdm6GGkwZfDWfzgbAoyfCpeofh6SM~JYJHA~Yz2DZbGKvnWnRGcxdP-NDiFnscUQqNFVWdkNY-tsMUDVm8vCoa18nD~ynDE2bduR6tSCXIy9UMO-yiMvMEr33iDRMSerW5GneYtHOm3eIV254bW4-5~VG6fZKgp5hq~AM-f6MZUoyNdzY7z1qXuc5p6avw2V~RqEvsTYeANOel9FPliNpBquFwg__')
show_jobs(jobs)

