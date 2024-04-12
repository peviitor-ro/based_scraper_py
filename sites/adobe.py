from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
import json
import re
from math import ceil

_counties = GetCounty()

url = "https://careers.adobe.com/us/en/search-results"

company = {"company": "Adobe"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url, "HTML")

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

data = re.search(pattern, scraper.prettify()).group(1)
totalJobs = json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("totalHits")

querys = ceil(totalJobs / 10)

for query in range(0, querys):
    url = (
        "https://careers.adobe.com/us/en/search-results?keywords=Romania&from="
        + str(query * 10)
        + "&s=1"
    )
    scraper.get_from_url(url, "HTML")
    data = re.search(pattern, scraper.prettify()).group(1)
    jobs = (
        json.loads("{" + data + "}")
        .get("eagerLoadRefineSearch")
        .get("data")
        .get("jobs")
    )

    for job in jobs:
        country = job.get("country")
        if country == "Romania":
            job_title = job.get("title")
            job_link = "https://careers.adobe.com/us/en/job/" + job.get("jobId")
            city = job.get("city")

            remote = []

            if not city:
                city = job.get("cityStateCountry").split(",")[0]

            if city == "Remote":
                city = ""
                remote.append("Remote")

            job_element = {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": country,
                "city": city,
                "remote": remote,
            }

            if city:
                city = translate_city(city)
                county = _counties.get_county(city)

                job_element.update({"city": city, "county": county})

            finalJobs.append(job_element)

publish_or_update(finalJobs)

logoUrl = "https://cdn.phenompeople.com/CareerConnectResources/ADOBUS/images/Header-1649064948136.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
