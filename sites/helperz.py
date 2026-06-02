import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import create_job, publish_or_update, publish_logo, show_jobs, translate_city


BASE_URL = "https://helperz.ro/locuri-de-munca/bona"
LOGO_URL = "https://helperz.ro/favicon.ico"
COMPANY = "Helperz"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

_counties = GetCounty()


def parse_salary(text):
    if not text:
        return None, None, None
    text = text.strip()
    match = re.search(r"de la\s*([\d\s.]+)\s*RON", text)
    if not match:
        return None, None, None
    salary_min = int(match.group(1).replace(" ", "").replace(".", ""))
    return salary_min, None, "RON"


def extract_location(card):
    for p in card.select("p.text-s"):
        prev = p.find_previous("p")
        if prev and prev.get_text(strip=True) == "Locație":
            value = p.get_text(strip=True)
            city = value.split(",")[0].strip()
            return city
    return ""


jobs = []
page = 1

while True:
    url = BASE_URL if page == 1 else f"{BASE_URL}?page={page}"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.select('div[class*="rounded-lg"][class*="shadow-custom"]')
    if not cards:
        break

    for card in cards:
        title_el = card.select_one("h3")
        if not title_el:
            continue

        job_title = title_el.get_text(" ", strip=True)
        link_el = card.select_one('a[href*="/locuri-de-munca/anunt/"]')
        if not link_el:
            continue

        job_link = f"https://helperz.ro{link_el['href']}"

        city_name = extract_location(card)
        city = translate_city(city_name) if city_name else ""
        counties = _counties.get_county(city) if city else []

        salary_text = ""
        for p in card.select("p.text-s"):
            prev = p.find_previous("p")
            if prev and prev.get_text(strip=True) == "Buget":
                salary_text = p.get_text(strip=True)
                break

        salary_min, salary_max, salary_currency = parse_salary(salary_text)

        jobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            company=COMPANY,
            country="Romania",
            city=[city] if city else [],
            county=counties,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_currency=salary_currency,
        ))

    page += 1

publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
