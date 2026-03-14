from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
import requests

_counties = GetCounty()

url = "https://careers.adobe.com/widgets"

payload = {
    "lang": "en_us",
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
    "all_fields": [
        "remote",
        "country",
        "state",
        "city",
        "experienceLevel",
        "category",
        "profession",
        "employmentType",
        "jobLevel",
    ],
    "size": 10,
    "clearAll": False,
    "jdsource": "facets",
    "isSliderEnable": False,
    "pageId": "page15-ds",
    "siteType": "external",
    "keywords": "",
    "global": True,
    "selected_fields": {"country": ["Romania"]},
    "locationData": {},
}

headers = {"Content-Type": "application/json"}

company = {"company": "Adobe"}
finalJobs = list()

def get_jobs(offset):
    request_payload = payload.copy()
    request_payload["from"] = offset
    response = requests.post(url, json=request_payload, headers=headers, timeout=10)
    response = response.json().get("refineSearch", {})
    return response.get("totalHits", 0), response.get("data", {}).get("jobs", [])

totalJobs, jobs = get_jobs(0)

for offset in range(0, totalJobs, payload["size"]):
    if offset != 0:
        _, jobs = get_jobs(offset)

    for job in jobs:
        country = job.get("country")
        if country != "Romania":
            continue

        city = job.get("city") or (job.get("cityStateCountry") or "").split(",")[0]
        remote = []

        if city == "Remote":
            city = ""
            remote.append("Remote")

        job_element = {
            "job_title": job.get("title"),
            "job_link": "https://careers.adobe.com/us/en/job/" + job.get("jobId"),
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
