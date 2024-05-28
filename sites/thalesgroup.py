from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://thales.wd3.myworkdayjobs.com/wday/cxs/thales/Careers/jobs"

company = {"company": "ThalesGroup"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {
    "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
    "limit": 20,
    "offset": 0,
    "searchText": "",
}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")

iteration = ceil(numberOfJobs / 20)

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings")
    for job in jobs:
        job_title = job.get("title")
        job_link = "https://thales.wd3.myworkdayjobs.com/en-US/Careers" + job.get(
            "externalPath"
        )
        city = translate_city(job.get("locationsText").split(",")[0])
        county = _counties.get_county(city)

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Thales_Logo.svg/484px-Thales_Logo.svg.png?20210518101610"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
