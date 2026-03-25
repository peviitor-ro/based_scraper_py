from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
import requests


_counties = GetCounty()

session = requests.Session()
seed_url = "https://careers.fedex.com/jobs?location_name=Romania&location_type=4&filter%5Bcountry%5D%5B0%5D=Romania"
session.get(seed_url, timeout=20)

url = (
    "https://careers.fedex.com/api/get-jobs?location_name=Romania&location_type=4"
    "&filter%5Bcountry%5D%5B0%5D=Romania&_pathname_=%2Fjobs&job_source=paradox"
    "&search_mode=2&enable_kilometers=false&include_remote_jobs=true"
)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://careers.fedex.com/jobs?location_name=Romania",
}
payload = {
    "site_available_languages": ["en"],
    "jobs_filter_options": [],
    "page_attributes": {"jobs_target_language": "en"},
    "oeid": 25,
}

company = {"company": "FedEx"}
finaljobs = []
page = 1


def normalize_city(city):
    city = translate_city(city or "")

    if city == "Judetul Cluj":
        return "Cluj-Napoca", ["Cluj"]

    if city == "Bucharest":
        return "Bucuresti", ["Bucuresti"]

    county = _counties.get_county(city) or []
    return city, county


while True:
    response = session.post(
        url + f"&page_number={page}",
        json=payload,
        headers=headers,
        timeout=20,
    ).json()
    jobs = response.get("jobs") or []

    if not jobs:
        break

    for job in jobs:
        locations = job.get("locations") or []
        romania_locations = [
            location for location in locations if location.get("country") == "Romania"
        ]

        remote = []
        city = ""
        county = []

        if romania_locations:
            city, county = normalize_city(romania_locations[0].get("city"))
        else:
            remote = ["Remote"]

        finaljobs.append(
            {
                "job_title": job.get("title"),
                "job_link": f"https://careers.fedex.com/{job.get('originalURL')}",
                "company": company.get("company"),
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": remote,
            }
        )

    page += 1


publish_or_update(finaljobs)

logoUrl = "https://1000logos.net/wp-content/uploads/2021/04/Fedex-logo-500x281.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
