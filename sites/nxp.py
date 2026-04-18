from scraper.Scraper import Scraper
from utils import translate_city, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://nxp.wd3.myworkdayjobs.com/wday/cxs/nxp/careers/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")
iteration = ceil(numberOfJobs / 20)

company = {"company": "NXP"}
finaljobs = []

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings") or []

    for job in jobs:
        locations_text = job.get("locationsText") or ""
        external_path = job.get("externalPath") or ""

        if not locations_text and "/job/" not in external_path:
            continue

        city = "Bucuresti"
        if "Sibiu" in locations_text or "/job/Sibiu/" in external_path:
            city = "Sibiu"

        county = _counties.get_county(city)

        finaljobs.append(
            {
                "job_title": job.get("title"),
                "job_link": "https://nxp.wd3.myworkdayjobs.com/en-US/careers" + external_path,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

publish_or_update(finaljobs)
publish_logo(
    company.get("company"),
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/NXP_logo.svg/512px-NXP_logo.svg.png",
)
show_jobs(finaljobs)
