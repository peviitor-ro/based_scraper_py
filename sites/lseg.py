import requests
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty


_counties = GetCounty()
apiUrl = "https://lseg.wd3.myworkdayjobs.com/wday/cxs/lseg/Careers/jobs"
session = requests.Session()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {
    "appliedFacets": {"locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]},
    "limit": 20,
    "offset": 0,
    "searchText": "",
}


def normalize_location(location_text):
    location_text = (location_text or "").strip()

    if not location_text:
        return None, []

    if "," in location_text:
        city = translate_city(location_text.split(",")[0].strip())
    else:
        city = translate_city(location_text.split("-")[0].strip())

    county = _counties.get_county(city) or []
    return city, county


def get_locations(job_path):
    detail_url = "https://lseg.wd3.myworkdayjobs.com/wday/cxs/lseg/Careers" + job_path

    try:
        response = session.get(detail_url, headers={"Accept": "application/json"}, timeout=40)
        job_info = response.json().get("jobPostingInfo") or {}
    except Exception:
        return []

    locations = []
    primary_location = job_info.get("location")
    additional_locations = job_info.get("additionalLocations") or []

    for raw_location in [primary_location] + additional_locations:
        city, county = normalize_location(raw_location)
        if city and county and city not in [item["city"] for item in locations]:
            locations.append({"city": city, "county": county})

    return locations


def get_basic_location(job):
    basic_city, basic_county = normalize_location(job.get("locationsText") or "")

    if basic_city and basic_county:
        return [{"city": basic_city, "county": basic_county}]

    return []


company = "LSEG"
finalJobs = []
seen_links = set()

response = session.post(apiUrl, json=data, headers=headers, timeout=40).json()
total_jobs = response.get("total") or 0

while data["offset"] < total_jobs:
    jobs = response.get("jobPostings") or []

    if not jobs:
        break

    for job in jobs:
        job_title = job.get("title")
        if not job_title:
            continue

        external_path = job.get("externalPath") or ""
        job_link = "https://lseg.wd3.myworkdayjobs.com/en-US/Careers" + external_path

        if job_link in seen_links:
            continue

        seen_links.add(job_link)
        locations = get_basic_location(job)

        if not locations:
            locations = get_locations(external_path)

        if not locations:
            locations = [{"city": "Bucuresti", "county": ["Bucuresti"]}]

        cities = [item["city"] for item in locations]
        counties = []
        for item in locations:
            for county in item["county"]:
                if county not in counties:
                    counties.append(county)

        finalJobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                city=cities,
                county=counties,
                company=company,
                remote=[],
            )
        )

    data["offset"] += data["limit"]

    if data["offset"] >= total_jobs:
        break

    response = session.post(apiUrl, json=data, headers=headers, timeout=40).json()


publish_or_update(finalJobs)
publish_logo(
    company,
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-Tp_lBl4hy9WFitdNzAtRw2tgxLYnxf1lyNrnXx8h&s",
)
show_jobs(finalJobs)
