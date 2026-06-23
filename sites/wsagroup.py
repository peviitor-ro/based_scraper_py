import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty, remove_diacritics
from utils import create_job, publish_logo, publish_or_update, show_jobs, translate_city


BASE_URL = "https://wsagroup.ro/locuri-de-munca/tara-romania/"
LOGO_URL = "https://wsagroup.ro/wp-content/uploads/2024/02/wsa-logo-nou.png"
COMPANY = "WSA Group"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

_counties = GetCounty()
jobs = []
seen_links = set()


def normalize_city(raw_city):
    city = remove_diacritics((raw_city or "").strip())
    city = city.replace("jud.", "").replace("jud", "")
    city = " ".join(city.split()).strip(",")
    city = translate_city(city)
    return city.strip()


def parse_location(card):
    location_text = " ".join(
        " ".join(node.get_text(" ", strip=True).split())
        for node in card.select(".elementor-widget-text-editor")
    )
    location_parts = [part.strip() for part in location_text.split(",") if part.strip()]

    city = None
    county = None

    for part in location_parts:
        if "Romania" in part:
            continue

        normalized_part = remove_diacritics(part)
        if normalized_part.lower() == "romania":
            continue

        if normalized_part.lower().startswith("jud"):
            county_name = normalized_part.replace(".", " ").split()[-1]
            county = [translate_city(county_name)]
            continue

        if not city:
            city = normalize_city(normalized_part)
            continue

        if not county:
            county = [translate_city(normalized_part)]

    if city and not county:
        county = _counties.get_county(city)

    return city, county


page = 1
while True:
    page_url = BASE_URL if page == 1 else f"{BASE_URL}?e-page-35ffb19={page}"
    response = requests.get(page_url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    page_jobs = 0

    for heading in soup.select("h1.elementor-heading-title a"):
        job_title = heading.get_text(" ", strip=True)
        job_link = heading.get("href")

        if not job_link or job_link in seen_links:
            continue

        if "/locuri-de-munca/" not in job_link and "wsagroup.ro/" not in job_link:
            continue

        card = heading
        for _ in range(4):
            card = card.parent
            if card is None:
                break

        city, county = parse_location(card) if card else (None, None)

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=COMPANY,
                country="Romania",
                city=city,
                county=county,
            )
        )
        seen_links.add(job_link)
        page_jobs += 1

    if page_jobs == 0:
        break

    page += 1


publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
