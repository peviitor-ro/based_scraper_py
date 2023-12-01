from scraper_peviitor import Scraper, loadingData
import json
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county
import re

url = "https://www.1and1.ro/jobs.json"

company = {"company": "1and1"}  
finalJobs = list()

scraper = Scraper() 
scraper.url = url

jobs = scraper.getJson().get("jobs")

remote_pattern = re.compile(r"\(.+\)")


for job in jobs:
    job_title = job.get("JobTitle")
    job_link = "https://www.1and1.ro/careers/" + job.get("RefURL")
    city = translate_city(job.get("Location"))
    county = get_county(city)
    remote_element = remote_pattern.search(job_title).group(0) if remote_pattern.search(job_title) else None

    remote = []

    if "remote" in job_title.lower():
        remote.append("Remote")
    if "hybrid" in job_title.lower():
        remote.append("Hybrid")

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "county": county,
        "remote": remote,
        "company": company.get("company")
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://cdn.website-editor.net/b236a61347464e4b904f5e6b661c2af9/dms3rep/multi/1and1-logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
