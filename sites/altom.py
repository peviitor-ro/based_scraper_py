from scraper.Scraper import Scraper
from utils import show_jobs, translate_city, publish, publish_logo
from getCounty import get_county


def get_data():
    # URL for the data
    url = 'https://www.altom.com/jobs/'

    # Get the data
    scraper = Scraper()
    scraper.get_from_url(url)
    jobs = scraper.find_all('article', class_='job')

    final_jobs = []

    # Create a list for the data
    for job in jobs:
        job_title = job.find('h2', class_='job-title').text.strip()
        job_link = job.find('h2', class_='job-title').find('a').get('href')
        job_city = translate_city(job.find('p', class_='job-feed-meta').text.strip())
        county = get_county(job_city)
        final_jobs.append({
            'job_title': job_title,
            'job_link': job_link,
            'city': job_city,
            'county': county,
            'country': 'Romania',
            'company': 'altom'})
    return final_jobs

data = get_data()

for version in range(1, 4):
    publish(version, 'altom', data, 'Grasum_Key')

publish_logo('altom', 'https://altom.com/app/themes/altom-sage-theme/dist/images/logo-altom_60516779.png')
show_jobs(data)
