
from scraper.Scraper import Scraper
import json
from utils import (publish, publish_logo, create_job,
                   show_jobs, translate_city, acurate_city_and_county)
from getCounty import get_county
from math import ceil

apiUrl = "https://refinitiv.wd3.myworkdayjobs.com/wday/cxs/refinitiv/Careers/jobs"


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

        county = get_county(location)
        if not county:

            location_city = scraper.markup.get(
                "jobPostingInfo").get("location")

            if "," in location_city:
                location = translate_city(location_city.split(",")[0])
            else:
                location = translate_city(location_city.split(" ")[0])

        county = get_county(location)

        if county:
            cities.append(location)
            counties.append(county)

    return cities, counties


company = "LSEG"
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {"locationCountry": [
    "f2e609fe92974a55a05fc1cdc2852122"]}, "limit": 20, "offset": 0, "searchText": ""}

scraper.set_headers(headers)
response = scraper.post(apiUrl, json.
                        dumps(data)).json()

totalJobs = response.get("total")

pages = ceil(totalJobs / 20)

jobs = response.get("jobPostings")

for page in range(pages):

    for job in jobs:
        job_title = job.get("title")
        job_link = "https://refinitiv.wd3.myworkdayjobs.com/en-US/Careers" + \
            job.get("externalPath")
        cities, counties = None, None

        if "," in job.get("locationsText"):
            cities = translate_city(job.get("locationsText").split(",")[0])
        else:
            cities = translate_city(job.get("locationsText").split(" ")[0])

        counties = get_county(cities)

        if not counties:
            aditional_url = "https://refinitiv.wd3.myworkdayjobs.com/wday/cxs/refinitiv/Careers" + \
                job.get("externalPath")

            try:
                cities, counties = get_aditional_city(aditional_url)
            except:
                cities = "Bucuresti"
                counties = "Bucuresti"

            if not counties:
                cities = "Bucuresti"
                counties = "Bucuresti"

        finalJobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            country="Romania",
            city=cities,
            county=counties,
            company=company
        ))

    data["offset"] = data.get("offset") + 20
    response = scraper.post(apiUrl, json.
                            dumps(data)).json()
    jobs = response.get("jobPostings")

for version in [1, 4]:
    publish(version, company, finalJobs, 'APIKEY')
publish_logo(
    company, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-Tp_lBl4hy9WFitdNzAtRw2tgxLYnxf1lyNrnXx8h&s")
show_jobs(finalJobs)
