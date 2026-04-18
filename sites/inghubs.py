from scraper.Scraper import Scraper
from utils import translate_city, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://ing.wd3.myworkdayjobs.com/wday/cxs/ing/ICSGBLCOR/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")
iteration = ceil(numberOfJobs / 20)

company = {"company": "INGHubs"}
finaljobs = []

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings") or []

    for job in jobs:
        external_path = job.get("externalPath") or ""
        locations_text = job.get("locationsText") or ""

        if "Romania" not in job.get("title", "") and "Bucharest" not in external_path and "Cluj" not in locations_text and "Ploiesti" not in locations_text and "Targu" not in locations_text:
            continue

        city = "Bucuresti"
        if "Cluj" in locations_text:
            city = "Cluj-Napoca"
        elif "Ploiesti" in locations_text:
            city = "Ploiesti"
        elif "Targu" in locations_text:
            city = "Targu-Mures"

        county = _counties.get_county(city)

        finaljobs.append(
            {
                "job_title": job.get("title"),
                "job_link": "https://ing.wd3.myworkdayjobs.com/en-US/ICSGBLCOR" + external_path,
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

publish_or_update(finaljobs)
publish_logo(
    company.get("company"),
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/ING_logo.svg/512px-ING_logo.svg.png",
)
show_jobs(finaljobs)
