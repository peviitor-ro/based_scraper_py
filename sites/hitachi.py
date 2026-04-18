from scraper.Scraper import Scraper
from utils import translate_city, publish_logo, publish_or_update, show_jobs
from getCounty import GetCounty
import json
from math import ceil

_counties = GetCounty()
apiUrl = "https://hitachi.wd1.myworkdayjobs.com/wday/cxs/hitachi/hitachi/jobs"
scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper.set_headers(headers)

numberOfJobs = scraper.post(apiUrl, json.dumps(data)).json().get("total")
iteration = ceil(numberOfJobs / 20)

company = {"company": "Hitachi"}
finaljobs = []

for num in range(iteration):
    data["offset"] = num * 20
    jobs = scraper.post(apiUrl, json.dumps(data)).json().get("jobPostings") or []

    for job in jobs:
        locations_text = job.get("locationsText") or ""

        if "Romania" not in locations_text and "Cluj" not in locations_text:
            continue

        city = translate_city(locations_text.split(",")[0].replace("(DEAI GL) RO ", "").strip())
        county = _counties.get_county(city)

        finaljobs.append(
            {
                "job_title": job.get("title"),
                "job_link": "https://hitachi.wd1.myworkdayjobs.com/en-US/hitachi" + (job.get("externalPath") or ""),
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
            }
        )

publish_or_update(finaljobs)
publish_logo(
    company.get("company"),
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Hitachi.svg/512px-Hitachi.svg.png",
)
show_jobs(finaljobs)
