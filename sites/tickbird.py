import sys
import requests
from utils import publish_or_update, publish_logo, show_jobs
import time

url = "https://join-us.tickbird.com/recruit/v2/public/Job_Openings?pagename=Careers&source=CareerSite&extra_fields=%5B%22State%22,%22Salary%22,%22Industry%22%5D"
company = "TICKBIRD"
logo_url = "https://tickbird.com/assets/images/logo/tickbird-logo.svg"


def fetch_with_retry(url, max_retries=3, delay=5):
    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
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
except Exception:
    print("Could not connect to the website. Exiting successfully.")
    publish_or_update([])
    publish_logo(company, logo_url)
    show_jobs([])
    sys.exit(0)

data = response.json()
final_jobs = []

for job in data["data"]:
    job_title = job["Posting_Title"]
    job_url = job["$url"]
    city = job["City"]
    state = job["State"]
    country = job["Country"]

    remote = job.get("Remote_Job", "No")

    if remote == "Yes":
        remote = "remote"
        country = "Romania"
    else:
        remote = "on-site"

    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_url,
            "city": city,
            "county": state,
            "country": country,
            "remote": remote,
            "company": company,
        }
    )

publish_or_update(final_jobs)

publish_logo(company, "https://tickbird.com/assets/images/logo/tickbird-logo.svg")

show_jobs(final_jobs)
