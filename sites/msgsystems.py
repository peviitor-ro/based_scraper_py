import requests
from bs4 import BeautifulSoup
from utils import publish_logo, publish_or_update, translate_city, show_jobs
from getCounty import GetCounty, remove_diacritics


_counties = GetCounty()
url = 'https://www.msg-systems.ro/en/careers/job-offerings'
company = 'MSGSYSTEMS'


def normalize_city(city):
    city = remove_diacritics(city.replace('(headquarters)', '').replace('(headquarter)', '').strip())
    city = city.replace('Tg. ', 'Targu-').replace('Targu Mures', 'Targu-Mures')
    city = translate_city(city)
    city = ' '.join(city.split())

    if city == 'Iasi':
        county = ['Iasi']
    else:
        county = _counties.get_county(city) or []

    return city, county


html = requests.get(url, timeout=20).text
soup = BeautifulSoup(html, 'html.parser')

final_jobs = []

for section in soup.select('section .text-section'):
    title_element = section.select_one('h4')
    link_element = section.select_one('a[href*="/en/careers/job-offerings/"]')
    paragraphs = section.find_all('p')

    if not title_element or not link_element or not paragraphs:
        continue

    location_text = ''
    for paragraph in paragraphs:
        text = paragraph.get_text(' ', strip=True)
        if '📍' in text:
            location_text = text.split('📍', 1)[1].strip()
            break

    if not location_text:
        continue

    cities = []
    counties = []

    for raw_city in location_text.split(','):
        city, county = normalize_city(raw_city)
        if city and city not in cities:
            cities.append(city)
        for item in county:
            if item not in counties:
                counties.append(item)

    final_jobs.append({
        'job_title': title_element.get_text(' ', strip=True),
        'job_link': f'https://www.msg-systems.ro{link_element.get("href")}',
        'city': cities,
        'county': counties,
        'country': 'Romania',
        'company': company
    })


publish_or_update(final_jobs)

publish_logo(company, 'https://www.msg-systems.ro/images/20200219_Logo_msg.svg')
show_jobs(final_jobs)
