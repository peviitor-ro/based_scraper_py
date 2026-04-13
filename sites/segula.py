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
jobs = []

url = "https://careers.segulatechnologies.com/wp/wp-admin/admin-ajax.php"

payload = {
    "action": "sgl_jobs_ajax",
    "limit": 100,
    "location": "Romania",
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

def fetch_with_retry(url, max_retries=2, delay=3):
    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=15, verify=False)
            return response
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {url}, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
    if last_error:
        raise last_error

try:
    response = fetch_with_retry(url)
except (ConnectTimeout, ConnectionError):
    print("Could not connect to the website. Exiting successfully.")
    jobs = []
    publish_or_update(jobs)
    publish_logo(
        company,
        "https://careers.segulatechnologies.com/app/themes/segula/library/medias/images/logo-blue.png",
    )
    show_jobs(jobs)
    sys.exit(0)

for job in response.json()["data"]["jobs"]:
    city = translate_city(remove_diacritics(job["city"]))
    county = _counties.get_county(city)
    jobs.append(
        create_job(
            company=company,
            job_title=job["title"],
            job_link=job["link"],
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
