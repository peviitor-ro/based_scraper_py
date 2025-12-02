from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from math import ceil
import json
from getCounty import GetCounty

_counties = GetCounty()

company = "Continental"
url = "https://jobs.continental.com/en/api/result-list/pagetype-jobs/"

post_data = {
    "tx_conjobs_api[filter][location]":
    '{"title":"Romania","type":"country","countryCode":"ro"}',
    "tx_conjobs_api[itemsPerPage]": 200,
    "tx_conjobs_api[currentPage]": 1,
}

headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "User-Agent": "Mozilla/5.0"}
jobs = []

scraper = Scraper()
scraper.set_headers(headers)

response = scraper.post(url, data=post_data).json()["result"]["list"]

for job in response:
    job_title = job["title"]
    job_link = "https://jobs.continental.com/en/detail-page/job-detail/" + job["url"]
    city = translate_city(job["cityLabel"])
    country = job["countryLabel"]

    county = _counties.get_county(city)

    job_data = create_job(
        job_title=job_title,
        job_link=job_link,
        country=country,
        city=city,
        county=county,
        company=company,
    )
    jobs.append(job_data)


publish_or_update(jobs)
publish_logo(
    company,
    "https://cdn.continental.com/fileadmin/_processed_/3/b/csm_continental_20logo-1920x1080_247d99d89e.png",
)
show_jobs(jobs)



