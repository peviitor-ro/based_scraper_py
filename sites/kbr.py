from scraper.Scraper import Scraper
from utils import translate_city, show_jobs, publish_or_update, publish_logo, create_job
from getCounty import GetCounty
import json

_counties = GetCounty()
apiUrl = "https://kbr.wd5.myworkdayjobs.com/wday/cxs/kbr/KBR_Careers/jobs"
company = "KBR"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Romania"}

scraper = Scraper()
scraper.set_headers(headers)

finalJobs = list()
seen_links = set()

response = scraper.post(apiUrl, json.dumps(data)).json()
total_jobs = response.get("total") or 0

if not total_jobs:
    data["searchText"] = ""
    response = scraper.post(apiUrl, json.dumps(data)).json()
    total_jobs = response.get("total") or 0

while data["offset"] < total_jobs:
    jobs = response.get("jobPostings") or []

    if not jobs:
        break

    for job in jobs:
        external_path = job.get("externalPath") or ""
        job_link = "https://kbr.wd5.myworkdayjobs.com/en-US/KBR_Careers" + external_path

        if job_link in seen_links:
            continue
        seen_links.add(job_link)

        locations_text = (job.get("locationsText") or "").strip()
        city_text = locations_text.split(",")[0].strip() if locations_text else ""

        if "Romania" in city_text or "Romania" in locations_text:
            city = "All"
            county = "All"
        else:
            city = translate_city(city_text) if city_text else "All"
            county = _counties.get_county(city)
            if not county:
                county = "All"

        finalJobs.append(
            create_job(
                job_title=job.get("title"),
                job_link=job_link,
                company=company,
                country="Romania",
                city=city,
                county=county,
            )
        )

    data["offset"] += data["limit"]
    if data["offset"] >= total_jobs:
        break
    response = scraper.post(apiUrl, json.dumps(data)).json()

try:
    publish_or_update(finalJobs)
except Exception as e:
    print(f"Warning: {e}")

publish_logo(
    company,
    "https://kbr.wd5.myworkdayjobs.com/KBR_Careers/assets/logo",
)

show_jobs(finalJobs)