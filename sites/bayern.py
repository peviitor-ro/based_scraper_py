import requests

from getCounty import GetCounty
from utils import publish_or_update, publish_logo, create_job, show_jobs
from utils import translate_city, acurate_city_and_county

company = "Bayern"
logo_url = "https://static.vscdn.net/images/careers/demo/bayer/1677751915::logo-bayer.svg"
api_url = "https://jobs.bayer.com/api/get-jobs"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://jobs.bayer.com",
    "Referer": "https://jobs.bayer.com/jobs",
}

_counties = GetCounty()
acurate_city = acurate_city_and_county(
    Sinesti={"city": "Sinesti", "county": "Ialomita"}
)

session = requests.Session()
session.get("https://jobs.bayer.com/", headers=headers, timeout=30)

jobs = []
seen_links = set()
page = 1
step = 10

while True:
    response = session.post(
        api_url,
        params={"page_number": page, "page_size": step},
        json={
            "disable_switch_search_mode": False,
            "site_available_languages": ["en"],
        },
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    positions = data.get("jobs") or []
    if not positions:
        break

    for job in positions:
        locations = [
            location
            for location in job.get("locations") or []
            if (location.get("country") or "").strip() == "Romania"
        ]
        if not locations:
            continue

        original_url = job.get("originalURL")
        job_link = (
            f"https://jobs.bayer.com/{original_url}"
            if original_url
            else job.get("applyURL")
        )
        if not job_link or job_link in seen_links:
            continue

        cities = []
        counties = []
        for location in locations:
            name = (location.get("city") or "").strip()
            accurate = acurate_city.get(name)
            if accurate:
                cities.append(accurate["city"])
                counties.append(accurate["county"])
            else:
                cities.append(translate_city(name))
                counties.append(_counties.get_county(name))

        jobs.append(
            create_job(
                job_title=job.get("title") or "",
                job_link=job_link,
                city=cities,
                county=counties,
                country="Romania",
                company=company,
            )
        )
        seen_links.add(job_link)

    if len(seen_links) >= data.get("totalJob", 0):
        break

    page += 1

publish_or_update(jobs)
publish_logo(company, logo_url)
show_jobs(jobs)
