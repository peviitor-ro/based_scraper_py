from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty, remove_diacritics
import re
import json

_counties = GetCounty()   
url = "https://www.randstad.ro/locuri-de-munca/lucreaza-la-randstad/"

company = {"company": "Randstad"}
finalJobs = list()

scraper = Scraper()
session = scraper.session()
response = session.get(url)

pattern = re.compile(r"const data = {(.*?)};", re.DOTALL)

data = re.search(pattern, response.text).group(1)
jobs = json.loads("{" + data + "}").get("ecommerce").get("impressions")

for job in jobs:
    job_title = job.get("job_title")
    job_link = "https://www.randstad.ro" + job.get("url")
    city = translate_city(remove_diacritics(job.get("city")))
    county = _counties.get_county(city) or []

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county
    })

publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/1/10/Randstad_Logo.svg"
publish_logo(company.get("company"), logoUrl)
show_jobs(finalJobs)
