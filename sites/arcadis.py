from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, get_jobtype, translate_city
from getCounty import GetCounty, remove_diacritics
from math import ceil
import json
import re
import requests


_counties = GetCounty()
company = "Arcadis"
jobs = []

FALLBACK_CITY = ["Iasi", "Bucuresti"]
FALLBACK_COUNTY = ["Iasi", "Bucuresti"]


def get_arcadis_locations(job_link):
    matches = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        requests.get(job_link, timeout=10).text,
        re.DOTALL,
    )

    romanian_locations = []

    for match in matches:
        try:
            schema = json.loads(match)
        except json.JSONDecodeError:
            continue

        if not isinstance(schema, dict) or schema.get("@type") != "JobPosting":
            continue

        job_locations = schema.get("jobLocation") or []
        if isinstance(job_locations, dict):
            job_locations = [job_locations]

        for location in job_locations:
            address = (location or {}).get("address") or {}
            country = address.get("addressCountry")

            if isinstance(country, dict):
                country = country.get("name")

            if country != "RO":
                continue

            city = remove_diacritics(address.get("addressLocality") or "").strip()
            if city:
                city = translate_city(city)

            county = []
            if city == "Iasi":
                county = ["Iasi"]
            elif city == "Bucuresti":
                county = ["Bucuresti"]
            elif city:
                county = _counties.get_county(city) or []

            romanian_locations.append((city, county))

        break

    unique_locations = []

    for city, county in romanian_locations:
        if not city:
            continue

        if any(existing_city == city for existing_city, _ in unique_locations):
            continue

        unique_locations.append((city, county))

    if unique_locations:
        cities = [city for city, _ in unique_locations]
        counties = []

        for _, county in unique_locations:
            for item in county:
                if item not in counties:
                    counties.append(item)

        return cities, counties

    return FALLBACK_CITY, FALLBACK_COUNTY


start = 0
url = (
    "https://jobs.arcadis.com/api/pcsx/search?domain=arcadis.com&query=&location=Romania"
    f"&start={start}&sort_by=distance&filter_include_remote=1"
)

scraper = Scraper()
scraper.get_from_url(url, type="JSON")
response_data = scraper.markup if isinstance(scraper.markup, dict) else {}
pages = ceil((response_data.get("data") or {}).get("count", 0) / 10)

for page in range(1, pages + 1):
    jobs_objects = (response_data.get("data") or {}).get("positions") or []

    for job in jobs_objects:
        job_title = job.get("name")
        job_link = "https://jobs.arcadis.com" + job.get("positionUrl")
        remote = get_jobtype(job.get("workLocationOption", ""))
        city, county = get_arcadis_locations(job_link)

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city=city,
                county=county,
                remote=remote,
            )
        )

    start = page * 10
    scraper = Scraper()
    scraper.get_from_url(
        "https://jobs.arcadis.com/api/pcsx/search?domain=arcadis.com&query=&location=Romania"
        f"&start={start}&sort_by=distance&filter_include_remote=1",
        type="JSON",
    )
    response_data = scraper.markup if isinstance(scraper.markup, dict) else {}

publish_or_update(jobs)
publish_logo(
    company,
    "https://cdn.phenompeople.com/CareerConnectResources/ARCAGLOBAL/images/header-1679586076111.svg",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")
