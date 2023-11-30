from scraper.Scraper import Scraper
import json
from utils import show_jobs, translate_city, publish
from getCounty import get_county

url = "https://tbibank.ro/cariere/"

scraper = Scraper()
scraper.get_from_url(url)

container = scraper.find("div")
data = json.loads(container["data-props"])
jobs = data["appConfig"]["offers"]

company = "TBIBank"
finalJobs = list()

for job in jobs:
    job_title = job["translations"]["en"]["title"]
    job_link = "https://tbibankro.recruitee.com/o/" + job["slug"]
    cities = job["city"].split("/")

    translated_cities = [translate_city(city.strip()) for city in cities]
    counties = [get_county(city) for city in translated_cities]

    remote = job["tags"]

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": translated_cities,
        "county": counties,
        "remote": remote
    })

show_jobs(finalJobs)

for version in [1, 4]:
    publish(version, company, finalJobs, 'APIKEY')
