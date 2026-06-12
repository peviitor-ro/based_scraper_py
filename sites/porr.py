import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).resolve().parent.parent))

from getCounty import GetCounty
from utils import create_job, publish_or_update, publish_logo, show_jobs, translate_city


BASE_URL = "https://cariere.porr.ro/joburi-porr"
LOGO_URL = "https://cariere.porr.ro/_assets/63211acade69d2a9884f8e688d2ef293/Images/logo.svg"
COMPANY = "PORR"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

_counties = GetCounty()
jobs = []
seen_links = set()

page = 1
while True:
    params = {}
    if page > 1:
        params["tx_solr[page]"] = page

    response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.select("div.rounded-porr.bg-lightgray")
    if not cards:
        break

    for card in cards:
        title_el = card.select_one("h2.headline-3xl a")
        if not title_el:
            continue

        job_title = title_el.get_text(" ", strip=True)
        job_link = title_el.get("href")
        if not job_link or job_link in seen_links:
            continue

        location = ""
        for dt in card.select("dl dt"):
            use = dt.select_one("use")
            if use and "#pin" in use.get("xlink:href", ""):
                dd = dt.find_next_sibling("dd")
                if dd:
                    location = dd.get_text(strip=True)
                break

        city = translate_city(location)
        counties = _counties.get_county(city) if city else []

        jobs.append(create_job(
            job_title=job_title,
            job_link=job_link,
            company=COMPANY,
            country="Romania",
            city=[city] if city else [],
            county=counties,
        ))
        seen_links.add(job_link)

    page += 1


publish_or_update(jobs)
publish_logo(COMPANY, LOGO_URL)
show_jobs(jobs)
