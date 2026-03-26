import requests
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty


_counties = GetCounty()
company = "MagnaElectronics"
api_url = "https://wd3.myworkdaysite.com/wday/cxs/magna/Magna/jobs"
detail_base_url = "https://wd3.myworkdaysite.com/wday/cxs/magna/Magna"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

payload = {
    "appliedFacets": {"Country": ["f2e609fe92974a55a05fc1cdc2852122"]},
    "limit": 20,
    "offset": 0,
    "searchText": "",
}

session = requests.Session()
jobs = []


def normalize_location(location_text):
    if not location_text:
        return None, []

    city = translate_city(location_text.split(",")[0].strip())
    if city == "Iasi":
        county = ["Iasi"]
    else:
        county = _counties.get_county(city) or []
    return city, county


def get_job_locations(external_path):
    response = session.get(
        detail_base_url + external_path,
        headers={"Accept": "application/json"},
        timeout=20,
    ).json()
    info = response.get("jobPostingInfo") or {}

    locations = []
    for raw_location in [info.get("location")] + (info.get("additionalLocations") or []):
        city, county = normalize_location(raw_location)
        if city and county and city not in [item["city"] for item in locations]:
            locations.append({"city": city, "county": county})

    return locations


response = session.post(api_url, json=payload, headers=headers, timeout=20).json()
total_jobs = response.get("total") or 0

while payload["offset"] < total_jobs:
    for job in response.get("jobPostings") or []:
        external_path = job.get("externalPath") or ""
        locations = get_job_locations(external_path)

        if not locations:
            locations = [{"city": "Timisoara", "county": ["Timis"]}]

        cities = [item["city"] for item in locations]
        counties = []
        for item in locations:
            for county in item["county"]:
                if county not in counties:
                    counties.append(county)

        jobs.append(
            create_job(
                job_title=job.get("title"),
                job_link="https://wd3.myworkdaysite.com/en-US/recruiting/magna/Magna" + external_path,
                city=cities,
                county=counties,
                country="Romania",
                company=company,
                remote=[],
            )
        )

    payload["offset"] += payload["limit"]
    if payload["offset"] >= total_jobs:
        break
    response = session.post(api_url, json=payload, headers=headers, timeout=20).json()


publish_or_update(jobs)

publish_logo(
    company,
    "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/6901fc63-3786-4d8b-8230-aa1bcd971324/original.png",
)
show_jobs(jobs)
