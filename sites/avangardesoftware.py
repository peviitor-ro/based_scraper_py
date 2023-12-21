import requests
from bs4 import BeautifulSoup
from getCounty import *
from utils import *

company = 'AvangardeSoftware'
url = 'https://avangarde-software.com/careers/'

# Use requests to fetch the HTML of the page
response = requests.get(url)

html_markup = response.text

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_markup, 'html.parser')

# Find all 'a' tags with the specified class
a_tags = soup.find_all('a', class_='stm_vacancies__single no_deco mbc_b')

final_jobs = []

for a_tag in a_tags:
    # Extract URL
    url = a_tag['href']

    # Extract job title
    job_title_div = a_tag.find('div', class_='stm_vacancies__title')
    job_title = job_title_div.get_text(strip=True)

    # Extract location
    location_div = a_tag.find('div', class_='stm_vacancies__location')
    location = location_div.get_text(strip=True).split(',')[0]
    county = get_county(location)

    final_jobs.append({
        'job_link': url,
        'job_title': job_title,
        'city': location,
        'county': county,
        'country': 'Romania',
        'company': company})

for version in [1, 4]:
    publish(version, company, final_jobs, 'Grasum_Key')

publish_logo(
    company, "https://avangarde-software.com/wp-content/uploads/2020/03/Avangarde-Software-Logo-1.png")
show_jobs(final_jobs)
