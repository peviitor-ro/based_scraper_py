from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
import re

_counties = GetCounty()
company = "Notino"

BASE_URL = "https://career.notino.ro/free-positions"
scraper = Scraper()

page = 1
jobs = []

while True:
    url = f"{BASE_URL}?page={page}"
    scraper.get_from_url(url, verify=False, timeout=30)

    cards = scraper.select("div.uk-card.uk-card--job")
    if not cards:
        break

    for card in cards:
        job_title = card.get("data-job-title")
        job_link = card.get("href") or ""
        if job_link and not job_link.startswith("http"):
            job_link = "https://career.notino.ro" + job_link

        location = ""
        places = card.select_one("ul.uk-list.uk-list--places")
        if places:
            li = places.find("li")
            if li:
                location = li.get_text(strip=True)

        # Only keep jobs located in Romania
        if "RO" not in location and "Romania" not in location and "România" not in location:
            continue

        city = ""
        county = ""
        if location:
            city_match = re.search(r"<strong>([^<]+)</strong>", location)
            if city_match:
                city = translate_city(city_match.group(1))
            else:
                city = translate_city(location.split(",")[0].strip())
            county = _counties.get_county(city)

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city=city,
                county=county,
            )
        )

    # Check pagination to see if there is a next page
    pagination = scraper.select_one("nav[aria-label='Pagination']")
    next_page_exists = False
    if pagination:
        lis = pagination.select("ul.uk-pagination > li")
        active_index = -1
        for i, li in enumerate(lis):
            classes = li.get("class") or []
            if "uk-active" in classes:
                active_index = i
                break
        if active_index != -1 and active_index < len(lis) - 1:
            next_page_exists = True
        elif active_index == -1 and len(lis) > 0:
            next_page_exists = True

    if not next_page_exists:
        break

    page += 1

publish_or_update(jobs)
publish_logo(
    company,
    "https://career.notino.ro/assets/img/favicons/favicon-32x32.png",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")