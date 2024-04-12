from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from math import ceil
import json
from getCounty import GetCounty

_counties = GetCounty()


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url, "JSON")

    location = scraper.markup.get("jobPostingInfo").get("location")
    isremote = scraper.markup.get("jobPostingInfo").get("additionalLocations")
    remote = []

    if isremote:
        for city in isremote:
            if "Remote" in city:
                remote.append("Remote")
                break

    city = translate_city(location.split("-")[-1].replace("Office", "").strip())
    county = _counties.get_county(city)

    if not county:
        city = ""
        county = ""
        remote = ["Remote"]

    return city, county, remote


company = "8x8"
url = " https://8x8inc.wd5.myworkdayjobs.com/wday/cxs/8x8inc/8x8_External_Careers/jobs"

post_data = {
    "appliedFacets": {
        "locations": [
            "a0520e7938c001056f9e2c42f9005506",
            "fb8ec7a2f8b00187652b898b17476715",
        ]
    },
    "limit": 20,
    "offset": 0,
    "searchText": "",
}

headers = {"Content-Type": "application/json"}

jobs = []

scraper = Scraper()
scraper.set_headers(headers)
obj = scraper.post(url, json.dumps(post_data))
step = 20
total_jobs = obj.json()["total"]
pages = ceil(total_jobs / step)

for pages in range(0, pages):
    if pages > 1:
        post_data["offset"] = pages * step
        obj = scraper.post(url, json.dumps(post_data))

    for job in obj.json()["jobPostings"]:
        job_title = job["title"]
        job_link = (
            "https://8x8inc.wd5.myworkdayjobs.com/en-US/8x8_External_Careers"
            + job["externalPath"]
        )
        country = "Romania"
        remote = []

        city = translate_city(
            job["locationsText"].split("-")[-1].replace("Office", "").strip()
        )
        county = _counties.get_county(city)

        if not county:
            aditional_url = (
                "https://8x8inc.wd5.myworkdayjobs.com/wday/cxs/8x8inc/8x8_External_Careers"
                + job.get("externalPath")
            )
            city, county, remote = get_aditional_city(aditional_url)

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                city=city,
                county=county,
                company=company,
                remote=remote,
            )
        )

publish_or_update(jobs)

publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/8x8_square_logo.svg/220px-8x8_square_logo.svg.png",
)
show_jobs(jobs)
