from scraper_peviitor import Scraper
from utils import (
    publish,
    publish_logo,
    show_jobs
)

url = "https://www.flanco.ro/cariere/posturi-vacante"

final_jobs = []
company = "flanco"

scraper = Scraper(url=url)

while True:
    scraper.getContent()
    content = scraper._soup
    jobs = content.select('div.vacant-position')
    for job in jobs:
        job_info = {
            'job_title': job.select_one("div.vp-title h2").get_text(),
            # 'department': job.select_one("div.vp-title div p:nth-child(1)").contents[-1].strip(),
            'job_city': job.select_one("div.vp-title div p:nth-child(2)").contents[-1].strip(),
            'job_link': job.select_one("div.description div.buttons a").get("href"),
        }
        final_jobs.append(job_info)
    next_page = content.select_one("li.item.pages-item-next a")

    if next_page is not None:
        url = next_page.get("href")
        scraper._url = url
    else:
        break

publish(4, company, final_jobs, "APIKEY")

logo_url = "https://upload.wikimedia.org/wikipedia/commons/7/78/Flanco_logo.svg"
publish_logo(company, logo_url)

show_jobs(final_jobs)