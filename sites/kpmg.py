from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
import json
from getCounty import GetCounty

_counties = GetCounty()
apiUrl = " https://careers.kpmg.ro/api/Talentlyft/jobs/filter"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"Departments":[],"Locations":[],"CareerLevel":None,"WorkplaceType":None,"Tags":[],"CurrentPage":1,"PageSize":10}

scraper = Scraper()
scraper.set_headers(headers)

jobs = scraper.post(apiUrl, json.dumps(data), verify=False).json().get("Results") or []

company = {"company": "KPMG"}
finalJobs = list()

while jobs:
    for job in jobs:
        job_title = job.get("Title")
        job_link = job.get("AbsoluteUrl")
        city = translate_city(job.get("Location").get("City"))
        county = _counties.get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        })

    data["CurrentPage"] += 1
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("Results")

publish_or_update(finalJobs)

logo_url = "https://careers.kpmg.ro/assets/images/logo-kpmg.jpg"
publish_logo(company.get("company"), logo_url)

show_jobs(finalJobs)
