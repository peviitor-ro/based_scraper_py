from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from math import ceil
from getCounty import get_county
from utils import translate_city, acurate_city_and_county

url = "https://bayer.eightfold.ai/api/apply/v2/jobs?domain=bayer.com&start=10&num=1000&exclude_pid=562949957688629&pid=562949957688629&domain=bayer.com&sort_by=relevance"


company = 'Bayern'
jobs = []

scraper = Scraper(url)
scraper.get_from_url(url, "JSON")

total_jobs = scraper.markup["count"]
step = 10
pages = ceil(total_jobs / step)

acurate_city = acurate_city_and_county(
    Sinesti={
        "city": "Sinesti",
        "county": "Ialomita"
    }
)

for page in range(0, pages):
    url = f"https://bayer.eightfold.ai/api/apply/v2/jobs?domain=bayer.com&start={page * step}&num={step}&exclude_pid=562949957688629&pid=562949957688629&domain=bayer.com&sort_by=relevance"
    scraper.get_from_url(url, "JSON")
    for job in scraper.markup["positions"]:
        locations = job["location"].split(",")
        country = locations[-1].strip()
        city = locations[0].strip()

        job_element = create_job(
            job_title=job["name"],
            job_link=job["canonicalPositionUrl"],
            city=[city],
            country=country,
            company=company,
        )

        if country == "Romania" and job.get("locations"):
            counties = []
            cities = []

            for city in job["locations"]:
                if acurate_city.get(city.split(",")[0]):
                    counties.append(acurate_city.get(
                        city.split(",")[0])["county"])
                    cities.append(acurate_city.get(city.split(",")[0])["city"])
                else:
                    counties.append(get_county(city.split(",")[0]))
                    cities.append(translate_city(city.split(",")[0]))

            job_element["county"] = counties
            job_element["city"] = cities

        elif country == "Romania" and job.get("location"):
            city = job["location"].split(",")[0].strip()
            county = get_county(city)
            job_element["county"] = county

        jobs.append(job_element)

for version in [1, 4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(
    company, 'https://static.vscdn.net/images/careers/demo/bayer/1677751915::logo-bayer.svg')

show_jobs(jobs)
