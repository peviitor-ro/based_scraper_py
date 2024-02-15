from scraper.Scraper import Scraper
import json
from utils import show_jobs, translate_city, publish, publish_logo
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
    country = job["translations"]["en"]["country"]
    cities = job["city"].split("/")
    remote = job["tags"]

    job_obj = {
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "remote": remote,
    }

    if country == "Romania":
        translated_cities = [translate_city(city.strip()) for city in cities]
        counties = [get_county(city) for city in translated_cities]

        job_obj["city"] = translated_cities
        job_obj["county"] = counties
    else:
        job_obj["city"] = cities

    finalJobs.append(job_obj)


publish(4, company, finalJobs, "APIKEY")

logoUrl = "https://tbibank.ro/wp-content/themes/Avada-child-bg/assets/images/tbi-layout/logo/new-logo.svg"
publish_logo(company, logoUrl)

show_jobs(finalJobs)
