from scraper.Scraper import Scraper
import asyncio
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil
import json
import re
import threading

url = 'https://careers.arcadis.com/search-results'
company = 'Arcadis'

scraper = Scraper()
scraper.get_from_url(url)

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

total_jobs = json.loads("{" + re.search(pattern, scraper.prettify()).group(1) + "}").get("eagerLoadRefineSearch").get("totalHits")
jobs = list()
def fetch (url, jobs):
    scraper.get_from_url(url)
    pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)
    data = re.search(pattern, scraper.prettify()).group(1)
    jobs += json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("data").get("jobs")
    print(len(jobs))

async def get_jobs():
    fire = []
    
    for i in range(0, ceil(total_jobs / 10)):
        thread = threading.Thread(target=fetch, args=(url + f'?from={i * 10}&s=1', jobs))
        fire.append(thread)
    
    for thread in fire:
        thread.start()
    
    for thread in fire:
        thread.join()
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