from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from math import ceil
import json
from getCounty import GetCounty

_counties = GetCounty()


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url, "JSON")

    job = scraper.markup.get("jobPostingInfo").get("additionalLocations")

    cities = []
    counties = []

    for city in job:
        location = None
        if "," in city:
            location = translate_city(city.split(",")[0])
        else:
            location = translate_city(city.split(" ")[0])

        county = _counties.get_county(location)
        if not county:
            location_city = scraper.markup.get("jobPostingInfo").get("location")

            if "," in location_city:
                location = translate_city(location_city.split(",")[0])
            else:
                location = translate_city(location_city.split(" ")[0])

        county = _counties.get_county(location)

        if county:
            cities.append(location)
            counties.append(county)

    return cities, counties


company = "3M"
url = "https://3m.wd1.myworkdayjobs.com/wday/cxs/3m/Search/jobs"

post_data = {
    "appliedFacets": {"Location_Country": ["f2e609fe92974a55a05fc1cdc2852122"]},
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
        job_link = "https://3m.wd1.myworkdayjobs.com/en-US/Search" + job["externalPath"]
        country = "Romania"
        remote = [job.get("remoteType") if job.get("remoteType") else []]

        cities, counties = None, None

        if "," in job.get("locationsText"):
            cities = translate_city(job.get("locationsText").split(",")[0])
        else:
            cities = translate_city(job.get("locationsText").split(" ")[0])

        counties = _counties.get_county(cities)

        if not counties:
            aditional_url = (
                "https://3m.wd1.myworkdayjobs.com/wday/cxs/3m/Search"
                + job.get("externalPath")
            )
            cities, counties = get_aditional_city(aditional_url)

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                city=cities,
                county=counties,
                company=company,
                remote=remote,
            )
        )

publish_or_update(jobs)

publish_logo(
    company,
    "https://www.3m.com.ro/3m_theme_assets/themes/3MTheme/assets/images/unicorn/Logo.svg",
)
show_jobs(jobs)
