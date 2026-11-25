from scraper.Scraper import Scraper
from utils import (
    translate_city,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty
import time

_counties = GetCounty()
url = "https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow=1"

company = {"company": "MolsonCoors"}
finalJobs = list()

scraper = Scraper()


def fetch_with_retry(scraper, url, max_retries=2, delay=3):
    for attempt in range(max_retries):
        try:
            scraper.get_from_url(url, timeout=30, verify=False)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {url}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
    print(f"Warning: Could not fetch from {url} after {max_retries} attempts")
    return False


if fetch_with_retry(scraper, url):
    pagination_label = scraper.find("span", {"class": "paginationLabel"})
    total_jobs = 0
    page_size = 10
    if pagination_label:
        page_bolds = pagination_label.find_all("b")
        if page_bolds:
            total_jobs = int(page_bolds[-1].get_text(strip=True).split()[-1])
            bounds = page_bolds[0].get_text(strip=True).split("–")
            if len(bounds) == 2:
                page_size = int(bounds[1].strip()) - int(bounds[0].strip()) + 1

    startrow = 1
    seen_links = set()
    while True:
        if startrow > 1 and not fetch_with_retry(scraper, url + f"&startrow={startrow}"):
            break

        table = scraper.find("table", {"id": "searchresults"})
        rows = table.select("tbody tr.data-row") if table else []
        if not rows:
            break

        for row in rows:
            link = row.select_one("a.jobTitle-link")
            location_tag = row.select_one("td.colLocation span.jobLocation")
            if not link or not location_tag:
                continue

            location = location_tag.get_text(" ", strip=True)
            location_parts = [part.strip().upper() for part in location.split(",")]
            if "RO" not in location_parts and "ROMANIA" not in location_parts:
                continue

            job_link = "https://jobs.molsoncoors.com" + link.get("href")
            if job_link in seen_links:
                continue
            seen_links.add(job_link)

            city = translate_city(location.split(",")[0].strip())
            finalJobs.append(
                {
                    "job_title": link.get_text(" ", strip=True),
                    "job_link": job_link,
                    "country": "Romania",
                    "city": city,
                    "county": _counties.get_county(city) or [],
                    "company": company.get("company"),
                }
            )

        if total_jobs and startrow + len(rows) - 1 >= total_jobs:
            break
        if len(rows) < page_size:
            break
        startrow += page_size
else:
    print("Warning: Could not connect to Molson Coors jobs site, exiting with empty results")

print("Jobs found:", len(finalJobs))

publish_or_update(finalJobs)

logoUrl = "https://rmkcdn.successfactors.com/e2403c2e/b8073680-5e29-45a9-8c61-4.png"
publish_logo(company.get("company"), logoUrl)
show_jobs(finalJobs)
