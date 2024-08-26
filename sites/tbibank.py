from scraper.Scraper import Scraper
import json
from utils import show_jobs, translate_city, publish_or_update, publish_logo
from getCounty import GetCounty

_counties = GetCounty()
url = "https://tbibankro.recruitee.com/"

scraper = Scraper()
scraper.get_from_url(url)

container = scraper.find("div", {"data-component": "PublicApp"})

data = json.loads(container["data-props"])
jobs = data["appConfig"]["offers"]

company = "TBIBank"
finalJobs = list()

for job in jobs:

        job_title = job["translations"].get("ro") or job["translations"].get("en")
        job_link = "https://tbibankro.recruitee.com/o/" + job["slug"]
        country = job["translations"].get("ro") or job["translations"].get("en")
        cities = job["city"].split("/")
        remote = job["tags"]

        job_obj = {
            "job_title": job_title.get("title"),
            "job_link": job_link,
            "company": company,
            "country": country.get("country"),
            "remote": [type.lower().replace("onsite", "on-site") for type in remote],
        }

        if country == "Romania":
            translated_cities = [translate_city(city.strip()) for city in cities]
            counties = []

            for city in translated_cities:
                county = _counties.get_county(city) or []
                counties.extend(county)

            job_obj["city"] = translated_cities
            job_obj["county"] = counties
        else:
            job_obj["city"] = cities

        finalJobs.append(job_obj)


publish_or_update(finalJobs)

logoUrl = "https://tbibank.ro/wp-content/themes/Avada-child-bg/assets/images/tbi-layout/logo/new-logo.svg"
publish_logo(company, logoUrl)

show_jobs(finalJobs)
