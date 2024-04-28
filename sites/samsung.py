from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty
from math import ceil
import json

_counties = GetCounty()
apiUrl = "https://sec.wd3.myworkdayjobs.com/wday/cxs/sec/Samsung_Careers/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")

iteration = ceil(numberOfJobs / 20)

company = {"company": "Samsung"}
finaljobs = list()

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings")
    for job in jobs:
        try:
            job_title = job.get("title")
            job_link = "https://sec.wd3.myworkdayjobs.com/en-US/Samsung_Careers" + \
                job.get("externalPath")
            city = translate_city(
                job.get("locationsText").split(",")[1].split(" ")[1]
            )

            county = _counties.get_county(city)
            remote = job.get("remoteType")

            if county:
                finaljobs.append({
                    "job_title": job_title,
                    "job_link": job_link,
                    "company": company.get("company"),
                    "country": "Romania",
                    "city": city,
                    "county": county,
                    "remote": remote
                })
        except:
            pass

publish_or_update(finaljobs)

logo_url = "https://sec.wd3.myworkdayjobs.com/Samsung_Careers/assets/logo"
publish_logo(company.get("company"), logo_url)
show_jobs(finaljobs)
