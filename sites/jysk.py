from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
from bs4 import BeautifulSoup
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_counties = GetCounty()
company = "Jysk"

AJAX_URL = "https://cariere.jysk.ro/views/ajax"
BASE_URL = "https://cariere.jysk.ro"

HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_page(page):
    params = {
        "_wrapper_format": "drupal_ajax",
        "view_name": "job_search",
        "view_display_id": "block_1",
        "view_args": "",
        "view_path": "/open-position",
        "view_base_path": "",
        "view_dom_id": "06d41222004d85f9a52cf44a50b00773aff12010f1a828e3322a936b772e0d17",
        "pager_element": 0,
        "page": page,
        "_drupal_ajax": 1,
        "ajax_page_state[theme]": "jobs_jysk_bootstrap",
        "ajax_page_state[theme_token]": "",
        "ajax_page_state[libraries]": "eJx1UFtuAyEMvBCNj4QMOBtvDEbgTZfbl03VbVQ1P9Y8PmbGQdW6NawQfpCvjTwXNndKULXqg9qLYqpiXF28U2LT5jFGbYm1wIku16bFqCQXVbQF3aEKcjnpjBEuBH_49BtBaltFuSRG0eWCK-7uxtSwxRtHFG-4a9E8fKaywXvLrRr8Ovod8pE9WX9S_zvmOmv2f51FNKB8dBuz2OIEh27mE_d4_GOAFprlXacj22Nlj5tp1FyFjOCN7vroRhkCdnIPps8Oz_u98lXImjahL5DcqHg",
    }

    response = requests.get(AJAX_URL, params=params, headers=HEADERS, timeout=30, verify=False)
    data = response.json()

    for command in data:
        if isinstance(command, dict) and command.get("command") == "insert":
            return command.get("data", "")

    return ""


jobs = []
page = 0

while True:
    html = fetch_page(page)
    if not html:
        break

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tbody tr")

    if not rows:
        break

    for row in rows:
        title_cell = row.select_one("td.views-field-title")
        if not title_cell:
            continue

        link = title_cell.select_one("a")
        job_title = link.get_text(strip=True) if link else ""
        job_link = link.get("href", "") if link else ""
        if job_link and not job_link.startswith("http"):
            job_link = BASE_URL + job_link

        city_cell = row.select_one("td.views-field-field-city")
        city = city_cell.get_text(strip=True) if city_cell else ""
        city = translate_city(city)

        category_cell = row.select_one("td.views-field-field-category")
        department = category_cell.get_text(strip=True) if category_cell else ""

        contract_cell = row.select_one("td.views-field-field-contract-type")
        employment_type = contract_cell.get_text(strip=True) if contract_cell else ""

        county = _counties.get_county(city) if city else ""

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city=city,
                county=county,
                department=department,
                employment_type=employment_type,
            )
        )

    page += 1

publish_or_update(jobs)
publish_logo(
    company,
    "https://cariere.jysk.ro/themes/custom/jobs_jysk_bootstrap/favicon.ico",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")