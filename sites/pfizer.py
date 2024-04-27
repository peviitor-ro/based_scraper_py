from scraper.Scraper import Scraper
from utils import translate_city, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://pfizer.wd1.myworkdayjobs.com/wday/cxs/pfizer/PfizerCareers/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets":{},"limit":20,"offset":0,"searchText":"Romania"}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")

iteration = ceil(numberOfJobs/20)

company = {"company": "Pfizer"}
finaljobs = list()

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings")

    for job in jobs:

        job_title = job.get("title")
        job_link = "https://pfizer.wd1.myworkdayjobs.com/en-US/PfizerCareers" + job.get("externalPath")
        city = translate_city(job.get("locationsText").split("-")[-1].strip())
        county = _counties.get_county(city)

        finaljobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county
        })

publish_or_update(finaljobs)

logo_url = (
    "https://helix-core-components.digitalpfizer.com/static/logo/pfizer-logo-color.svg"
)
publish_logo(company.get("company"), logo_url)
show_jobs(finaljobs)
