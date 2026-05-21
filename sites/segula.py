from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics
from requests.exceptions import ConnectTimeout, ConnectionError
import requests
import urllib3
import time
import sys

_counties = GetCounty()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
company = "Segula"

API_BASE = "https://api.digitalrecruiters.com/public/v1"
HEADERS = {
    "Origin": "https://careers.segulatechnologies.com",
    "Referer": "https://careers.segulatechnologies.com/ro/annonces",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
DOMAIN = "careers.segulatechnologies.com"


def fetch_with_retry(url, max_retries=2, delay=3, method="POST", **kwargs):
    last_error = None
    for attempt in range(max_retries):
        try:
            if method == "POST":
                response = requests.post(url, headers=HEADERS, timeout=15, verify=False, **kwargs)
            else:
                response = requests.get(url, headers=HEADERS, timeout=15, verify=False, **kwargs)
            return response
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {url}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
    if last_error:
        raise last_error


def fetch_all_jobs():
    all_jobs = []
    page = 1
    while True:
        url = f"{API_BASE}/careers-site/job-ads?domainName={DOMAIN}&limit=100&page={page}"
        payload = {"filters": {}, "searchParameters": {"keywords": [], "place": None}}
        response = fetch_with_retry(url, json=payload)
        if response.status_code != 200:
            break
        data = response.json()
        items = data.get("items", [])
        if not items:
            break
        all_jobs.extend(items)
        if len(items) < 100:
            break
        page += 1
    return all_jobs


def fetch_job_detail(job_ad_id):
    url = f"{API_BASE}/careers-site/job-ads/{job_ad_id}?domainName={DOMAIN}"
    response = fetch_with_retry(url, method="GET")
    if response.status_code == 200:
        return response.json()
    return None


try:
    jobs_data = fetch_all_jobs()
except (ConnectTimeout, ConnectionError, Exception) as e:
    print(f"Could not connect to the website: {e}. Exiting successfully.")
    jobs = []
    publish_or_update(jobs)
    publish_logo(
        company,
        "https://careers.segulatechnologies.com/app/themes/segula/library/medias/images/logo-blue.png",
    )
    show_jobs(jobs)
    sys.exit(0)

jobs = []
for job in jobs_data:
    detail = fetch_job_detail(job["job_ad_id"])
    if detail is None:
        continue
    country = detail.get("address", {}).get("country", "")
    if country.lower() != "romania":
        continue
    city = translate_city(remove_diacritics(detail["address"]["city"]))
    county = _counties.get_county(city)
    jobs.append(
        create_job(
            company=company,
            job_title=detail.get("title", job.get("title", "")),
            job_link=f"https://careers.segulatechnologies.com/ro/annonce/{job['url']}",
            city=city,
            county=county,
            country="Romania",
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://careers.segulatechnologies.com/app/themes/segula/library/medias/images/logo-blue.png",
)
show_jobs(jobs)
