from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
import requests

_counties = GetCounty()

session = requests.Session()

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://careers.fedex.com/jobs?location_name=Romania",
}

response = session.get(
    "https://careers.fedex.com/jobs?location_name=Romania&location_type=4&filter%5Bcountry%5D%5B0%5D=Romania", headers=headers
)

cookies = session.cookies.get_dict()
header_cookies = response.headers.get("Set-Cookie")

page = 1
url = "https://careers.fedex.com/api/get-jobs?location_name=Romania&location_type=4&filter%5Bcountry%5D%5B0%5D=Romania&_pathname_=%2Fjobs&job_source=paradox&search_mode=2&enable_kilometers=false&include_remote_jobs=true"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://careers.fedex.com/jobs?location_name=Romania",
    "Origin": "https://careers.fedex.com",
    "X-Requested-With": "XMLHttpRequest",
}

payload = {
    "site_available_languages": ["en"],
    "jobs_filter_options": [],
    "page_attributes": {
        "jobs_target_language": "en",
    },
    "oeid": 25,
    "site_available_languages": ["en"],
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://careers.fedex.com/jobs?location_name=Romania",
}

jobs = list()
while True:

    response = session.post(
        url + f"&page_number={page}", json=payload, headers=headers).json()

    if not response.get("jobs"):
        break

    jobs.extend(response.get("jobs"))
    page += 1


company = {"company": "FedEx"}
finaljobs = list()

for job in jobs:
    job_title = job.get("title")
    job_link = f"https://careers.fedex.com/{job.get('originalURL')}"
    locations = job.get("locations")
    country = [
        location.get("country")
        for location in locations
        if location.get("country") == "Romania"
    ]

    cities = [
        translate_city(location.get("city"))
        for location in locations
        if location.get("city")
    ]

    counties = []
    job_city = cities[0] if cities else None

    for city in cities:

        if city == "Judetul Cluj":
            city = "Cluj-Napoca"

        county = _counties.get_county(city)
        if county:
            counties.extend(county)

    if "Romania" in country:
        finaljobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": job_city,
                "county": counties,
            }
        )

publish_or_update(finaljobs)

logoUrl = "https://1000logos.net/wp-content/uploads/2021/04/Fedex-logo-500x281.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
