from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
from math import ceil
import json

_counties = GetCounty()

apiUrl = (
    "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs"
)

company = {"company": "ADI"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper.set_headers(headers)

response = scraper.post(apiUrl, json.dumps(data)).json()

pages = ceil(response.get("total") / 20)
jobs = response.get("jobPostings")

for page in range(pages):
    for job in jobs:
        job_title = job.get("title")
        job_link = (
            "https://analogdevices.wd1.myworkdayjobs.com/en-US/External"
            + job.get("externalPath")
        )
        location = job.get("locationsText").split(",")
        city = translate_city(location[-1].strip())

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": _counties.get_county(city),
            }
        )
    data["offset"] = page * 20
    jobs = scraper.post(apiUrl, data).json().get("jobPostings")

publish_or_update(finalJobs)

logoUrl = "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/072011/analog-logo.ai_.png?itok=RM5-oQ34"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
