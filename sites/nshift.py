import requests
import re
import json
from bs4 import BeautifulSoup
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics


_counties = GetCounty()
company = "nShift"
url = "https://careers.nshift.com/jobs"


def normalize_city(city):
    city = translate_city(remove_diacritics((city or "").strip()))

    if city == "Bucuresti":
        return city, ["Bucuresti"]
    if city == "Brasov":
        return city, ["Brasov"]
    if city == "Cluj-Napoca":
        return city, ["Cluj"]

    return city, _counties.get_county(city) or []


html = requests.get(url, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

jobs = []
seen_links = set()

for job_element in soup.select('a[href*="/jobs/"]'):
    job_link = job_element.get("href")
    listing_text = job_element.get_text(" ", strip=True)

    if not job_link or "/locations/" in job_link or job_link in seen_links:
        continue

    seen_links.add(job_link)

    title_elem = job_element.find("span", class_="text-block-base-link")
    if not title_elem:
        continue

    detail_html = requests.get(job_link, timeout=20).text
    schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', detail_html, re.DOTALL)
    if not schema_match:
        continue

    schema = json.loads(schema_match.group(1))
    locations = schema.get("jobLocation") or []
    if isinstance(locations, dict):
        locations = [locations]

    cities = []
    counties = []

    for location in locations:
        address = (location or {}).get("address") or {}
        if address.get("addressCountry") != "RO":
            continue

        city, county = normalize_city(address.get("addressLocality"))
        if city and city not in cities:
            cities.append(city)
        for item in county:
            if item not in counties:
                counties.append(item)

    if not cities:
        continue

    remote = []
    detail_lower = detail_html.lower()
    listing_lower = listing_text.lower()
    if "fully remote" in listing_lower or schema.get("jobLocationType") == "TELECOMMUTE":
        remote.append("remote")
    elif "hybrid" in listing_lower or "#li-hybrid" in detail_lower:
        remote.append("hybrid")

    jobs.append(
        create_job(
            job_title=title_elem.text.strip(),
            job_link=job_link,
            city=cities,
            county=counties,
            remote=remote,
            country="Romania",
            company=company,
        )
    )


publish_or_update(jobs)

publish_logo(
    company,
    "https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v1/image_uploads/6b643d11-63d9-466b-bdc1-dfbab828db19/original.png",
)
show_jobs(jobs)
