from scraper.Scraper import Scraper
from utils import (publish_or_update, publish_logo, create_job,
                   show_jobs, translate_city)
from getCounty import GetCounty, remove_diacritics
from requests.exceptions import ConnectTimeout, ConnectionError
import sys
import time

_counties = GetCounty()
company = 'KWS'
url = 'https://jobs.kws.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_city=&optionsFacetsDD_department=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield4='

scraper = Scraper()

def fetch_with_retry(scraper, url, max_retries=2, delay=3):
    last_error = None
    for attempt in range(max_retries):
        try:
            scraper.get_from_url(url, timeout=5, verify=False)
            return True
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {url}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
    if last_error:
        raise last_error

try:
    fetch_with_retry(scraper, url)
except (ConnectTimeout, ConnectionError):
    print("Could not connect to the website. Exiting successfully.")
    jobs = []
    publish_or_update(jobs)
    publish_logo(company, 'https://rmkcdn.successfactors.com/26823ea3/7e38ad11-136a-4629-bfec-6.svg')
    show_jobs(jobs)
    sys.exit(0)

jobs = []

searchresults_table = scraper.find('table', id='searchresults')

if searchresults_table:
    jobs_elements = searchresults_table.find('tbody').find_all('tr')

    for job in jobs_elements:
        job_title = job.find('a', class_='jobTitle-link').text
        job_link = 'https://jobs.kws.com' + \
            job.find('a', class_='jobTitle-link')['href']
        city = translate_city(remove_diacritics(
            job.find('span', class_='jobLocation').text.split(',')[0].strip()))
        county = _counties.get_county(city)

        jobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            city=city,
            county=county,
            country='Romania',
            company=company,
        ))

publish_or_update(jobs)

publish_logo(company, 'https://rmkcdn.successfactors.com/26823ea3/7e38ad11-136a-4629-bfec-6.svg')
show_jobs(jobs)
