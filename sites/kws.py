from scraper.Scraper import Scraper
from utils import (publish_or_update, publish_logo, create_job,
                   show_jobs, translate_city)
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
company = 'KWS'
url = 'https://jobs.kws.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_city=&optionsFacetsDD_department=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield4='

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find(
    'table', id='searchresults').find('tbody').find_all('tr')

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
