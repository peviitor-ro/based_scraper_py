from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city, acurate_city_and_county)
from getCounty import get_county


def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """

    ta = 'È'.encode()
    a = 'Ä'.encode()
    aa = 'Ã¢'.encode()

    string = string.encode()
    string = string.replace(ta, b'ta')
    string = string.replace(a, b'a')
    string = string.replace(aa, b'a')
    
    string = string.decode('utf-8')
    return string

company = 'SVN'
url = 'https://jobs.svn.ro/posturi-vacante.html'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

jobs_elements = scraper.find('div', class_='jobs').find_all('div', class_='job')

for job in jobs_elements:
    job_title=remove_umlaut(job.find('h3').text)
    job_link='https://jobs.svn.ro' + job.find('a')['href']
    city=translate_city(job.find('ul').find_all('li')[-1].text).replace("È", "s")
    county = get_county(city)
    
    jobs.append(create_job(
        job_title=job_title,
        job_link=job_link,
        company=company,
        country="Romania",
        city=city,
        county=county,
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.svn.ro/assets/images/logo/3.png')
show_jobs(jobs)