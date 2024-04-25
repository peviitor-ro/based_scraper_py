from scraper.Scraper import Scraper
from utils import (translate_city, show_jobs, publish_or_update, publish_logo)
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://kbr.wd5.myworkdayjobs.com/wday/cxs/kbr/KBR_Careers/jobs"

company = {"company": "KBR"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets":{},"limit":20,"offset":0,"searchText":"Romania"}

scraper.set_headers(headers)

response = scraper.post(apiUrl, data=json.dumps(data)).json()
iteration = ceil(response.get("total") / 20)
jobs = response.get("jobPostings")

for num in range(iteration):

    for job in jobs:
        job_title = job.get("title")
        job_link = "https://kbr.wd5.myworkdayjobs.com/en-US/KBR_Careers" + job.get("externalPath")
        city = translate_city(job.get("locationsText").split(",")[0])
        county = None

        if "Romania" in city:
            city = "All"
            county = "All"
        else:
            county = _counties.get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        })
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings")

publish_or_update(finalJobs)
logoUrl = "https://kbr.wd5.myworkdayjobs.com/KBR_Careers/assets/logo"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)