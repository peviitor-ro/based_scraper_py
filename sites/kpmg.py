from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
import requests
import urllib3

_counties = GetCounty()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apiUrl = "https://careers.kpmg.ro/api/Talentlyft/jobs/filter"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"Departments":[],"Locations":[],"CareerLevel":None,"WorkplaceType":None,"Tags":[],"CurrentPage":1,"PageSize":10}

company = {"company": "KPMG"}
finalJobs = list()

jobs = requests.post(apiUrl, json=data, headers=headers, timeout=10, verify=False).json().get("Data") or []

while jobs:
    for job in jobs:
        job_title = job.get("Title")
        job_link = job.get("AbsoluteUrl")
        city = translate_city(job.get("City"))
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
    jobs = requests.post(apiUrl, json=data, headers=headers, timeout=10, verify=False).json().get("Data") or []

publish_or_update(finalJobs)

logo_url = "https://careers.kpmg.ro/assets/images/logo-kpmg.jpg"
publish_logo(company.get("company"), logo_url)

show_jobs(finalJobs)
