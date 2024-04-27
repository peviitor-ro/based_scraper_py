from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo


url = 'https://quantrabbit.com/blog/'
company = 'QUANTRABBIT'

final_jobs = []

scraper = Scraper()
scraper.get_from_url(url)

job_elements = scraper.find_all('h2', class_='entry-title')

for job in job_elements:
    job_title = job.text.strip()
    job_url = job.a['href']

    final_jobs.append(
        {
            'job_title': job_title,
            'job_link' : job_url,
            'city' : 'Cluj-Napoca',
            'county' : 'Cluj',
            'country' : 'Romania',
            'company' : company
        }
    )

publish_or_update(final_jobs)

publish_logo(company, 'https://quantrabbit.com/wp-content/uploads/2017/09/cropped-Quant-Rabbit-Logo-Final-2.png')
show_jobs(final_jobs)
