from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
from math import ceil
import re
import requests

_counties = GetCounty()
company = "SiemensHealthineers"
url = "https://careers.siemens-healthineers.com/widgets"

payload = {
    "lang": "en_global",
    "deviceType": "desktop",
    "country": "us",
    "pageName": "search-results",
    "ddoKey": "refineSearch",
    "sortBy": "",
    "subsearch": "",
    "from": 0,
    "irs": False,
    "jobs": True,
    "counts": True,
    "all_fields": ["remote", "country", "state", "city", "category", "employmentType"],
    "size": 10,
    "clearAll": False,
    "jdsource": "facets",
    "isSliderEnable": False,
    "pageId": "page22-ds",
    "siteType": "external",
    "keywords": "",
    "global": True,
    "selected_fields": {"country": ["Romania"]},
    "locationData": {},
}

headers = {"Content-Type": "application/json"}

jobs = []


def get_jobs(offset):
    request_payload = payload.copy()
    request_payload["from"] = offset
    response = requests.post(
        url, json=request_payload, headers=headers, timeout=10, verify=False
    )
    response = response.json().get("refineSearch", {})
    return response.get("totalHits", 0), response.get("data", {}).get("jobs", [])


total_jobs, jobs_elements = get_jobs(0)

pages = ceil(total_jobs / payload["size"])

for page in range(pages):
    if page:
        _, jobs_elements = get_jobs(page * payload["size"])

    for job in jobs_elements:
        city = translate_city(job.get("city") or "")
        counties = []

        if city:
            county = _counties.get_county(city) or []
            counties.extend(county)

        slug = re.sub(r"[^a-z0-9]+", "-", (job.get("title") or "").lower()).strip("-")
        job_link = (
            "https://careers.siemens-healthineers.com/global/en/job/"
            + (job.get("jobSeqNo") or "")
            + "/"
            + slug
        )

        jobs.append(
            create_job(
                job_title=job.get("title"),
                job_link=job_link,
                city=city,
                county=counties,
                country="Romania",
                company=company
            )
        )


publish_or_update(jobs)

publish_logo(
    company,
    "https://static.vscdn.net/images/careers/demo/siemens/1677769995::Healthineers+Logo+2023",
)
show_jobs(jobs)
