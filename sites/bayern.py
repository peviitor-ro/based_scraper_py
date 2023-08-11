from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil
import json

url = "https://bayer.eightfold.ai/api/apply/v2/jobs?domain=bayer.com&start=10&num=1000&exclude_pid=562949957688629&pid=562949957688629&domain=bayer.com&sort_by=relevance"


company = 'Bayern'
jobs = []

scraper = Scraper(url)
scraper.get_from_url(url, "JSON")

total_jobs = scraper.markup["count"]
step = 10
pages = ceil(total_jobs / step)

for page in range(0, pages):
    url = f"https://bayer.eightfold.ai/api/apply/v2/jobs?domain=bayer.com&start={page * step}&num={step}&exclude_pid=562949957688629&pid=562949957688629&domain=bayer.com&sort_by=relevance"
    scraper.get_from_url(url, "JSON")
    for job in scraper.markup["positions"]:
        locations = job["location"].split(",")
        country = locations[-1].strip()
        city = locations[0].strip()

        jobs.append(create_job(
            job_title=job["name"],
            job_link=job["canonicalPositionUrl"],
            city=city,
            country=country,
            company=company,
        ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://static.vscdn.net/images/careers/demo/bayer/1677751915::logo-bayer.svg')

show_jobs(jobs)


