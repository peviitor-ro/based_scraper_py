from scraper.Scraper import Scraper
from getCounty import remove_diacritics, GetCounty
from utils import publish_or_update, publish_logo, show_jobs, translate_city
import json


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find(
        "span", {"class": "job-description__location-pin"}
    ).text.split("|")

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(translate_city(
            location.split(",")[0].strip()))
        county = _counties.get_county(city)

        if county:
            cities.append(city)
            counties.extend(county)

    return cities, counties


_counties = GetCounty()
url = "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs"

company = "Intel"
finalJobs = list()

post_data = {"appliedFacets": {"locations": [
    "1e4a4eb3adf101fc3983e778bf8131d1"]}, "limit": 20, "offset": 0, "searchText": ""}
headers = {"Content-Type": "application/json"}

scraper = Scraper()
scraper.set_headers(headers)

scraper.post(url, json.dumps(post_data))

jobs = scraper.post(url, json.dumps(post_data)).json().get("jobPostings")

for job in jobs:
    job_title = job.get("title")
    job_link = "https://intel.wd1.myworkdayjobs.com/en-US/External" + \
        job.get("externalPath")

    if "," in job.get("locationsText"):
        cities = translate_city(job.get("locationsText").split(",")[1])
    else:
        cities = translate_city(job.get("locationsText").split(" ")[1])

    counties = _counties.get_county(cities)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
            "city": cities,
            "county": counties,
        }
    )


publish_or_update(finalJobs)

logoUrl = (
    "https://tbcdn.talentbrew.com/company/599/gst-v1_0/img/logo/logo-intel-blue.svg"
)
publish_logo(company, logoUrl)
show_jobs(finalJobs)
