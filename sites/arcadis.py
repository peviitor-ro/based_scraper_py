from scraper.Scraper import Scraper
import asyncio
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil
import json
import re

url = 'https://careers.arcadis.com/search-results'
company = 'Arcadis'

scraper = Scraper()
scraper.get_from_url(url)

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

total_jobs = json.loads("{" + re.search(pattern, scraper.prettify()).group(1) + "}").get("eagerLoadRefineSearch").get("totalHits")

async def get_jobs():
    jobs = list()
    for i in range(0, ceil(total_jobs / 10)):
        scraper.get_from_url(url + f'?from={i * 10}&s=1')
        pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)
        data = re.search(pattern, scraper.prettify()).group(1)
        jobs += json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("data").get("jobs")
    return jobs
    
async def main():
    objs = await get_jobs()
    jobs = list()
    for job in objs:
        jobs.append(create_job(
            job_title=job.get("title"),
            job_link=job.get("applyUrl"),
            company=company,
            country=job.get("country"),
            city=job.get("city")
        ))
    for version in [1,4]:
        publish(version, company, jobs, 'APIKEY')
    publish_logo(company, "https://cdn.phenompeople.com/CareerConnectResources/ARCAGLOBAL/images/MicrosoftTeams-image32-1620211091518.png")
    show_jobs(jobs)
asyncio.run(main())