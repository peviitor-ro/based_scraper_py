from scraper.Scraper import Scraper
import json
import re
from utils import translate_city, publish_or_update, publish_logo, show_jobs, create_job
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://jobs.msd.com/gb/en/search-results?qcountry=Romania"

company = {"company": "MSD"}
finalJobs = list()

scraper = Scraper()
session = scraper.session()
response = session.get(url)

pattern = re.compile(r"phApp.ddo = {(.*?)};", re.DOTALL)

data = re.search(pattern, response.text).group(1)
totalJobs = json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("totalHits")

querys = ceil(totalJobs / 10)

jobs = json.loads("{" + data + "}").get("eagerLoadRefineSearch").get("data").get("jobs")

for query in range(querys):
    for job in jobs:
        job_title = job.get("title")
        job_link = "https://jobs.msd.com/gb/en/job/" + job.get("jobId")
        city = translate_city(job.get("city"))
        county = _counties.get_county(city)
        remote = []

        job_element = create_job(
            job_title=job_title,
            job_link=job_link,
            company=company.get("company"),
            country="Romania",
        )

        if not county:
            job_element["remote"] = "Remote"
        else:
            job_element["city"] = city
            job_element["county"] = county

        finalJobs.append(job_element)

    url = "https://jobs.msd.com/gb/en/search-results?qcountry=Romania&from=" + str(
        query + 1 * 10
    )
    response = session.get(url)
    data = re.search(pattern, response.text).group(1)
    jobs = (
        json.loads("{" + data + "}")
        .get("eagerLoadRefineSearch")
        .get("data")
        .get("jobs")
    )

publish_or_update(finalJobs)

logoUrl = "https://www.msdmanuals.com/Content/Images/msd_foot_logo.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
