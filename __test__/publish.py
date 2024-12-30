import os
import requests
from dotenv import load_dotenv
from utils import get_token
import time
import threading

load_dotenv()


DOMAIN = os.environ.get("DOMAIN")
EMAIL = os.environ.get("EMAIL")
TOKEN = get_token()

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

get_companies_url = DOMAIN + "companies/"
get_jobs_url = DOMAIN + "jobs/get/"
publish_jobs_url = DOMAIN + "jobs/publish/"

companies = requests.get(
    DOMAIN + "companies/?page_size=50&order=access_name_asc", headers=HEADERS).json()

all_companies = []


while companies:
    for company in companies.get("results"):
        all_companies.append(company)

    if companies.get("next"):
        companies = requests.get(companies.get("next"), headers=HEADERS).json()
    else:
        companies = None

def publish_jobs(company):
    print(f"Publishing jobs from company {company.get('company')}")
    try:
        jobs = requests.get(
            get_jobs_url + f"?company={company.get('company')}", headers=HEADERS).json()
    except Exception as e:
        print(e)
        return

    jobs_to_publish = []
    while jobs:
        for job in jobs.get("results"):
            try:
                if not job.get("published"):
                    if requests.head(job.get("job_link"), timeout=5).status_code == 200:
                        if "remote" in job.get("remote") or (job.get("city") and job.get("county")):
                            job["published"] = True
                            jobs_to_publish.append(job)
                        else:
                            print(
                                f"Job {job.get('job_title')} from {job.get('company')} has no location")

                    else:
                        print(
                            f"Job {job.get('job_title')} from {job.get('company')} is not available")

                    time.sleep(3)
            except Exception as e:
                print(e)

        if jobs.get("next"):
            jobs = requests.get(jobs.get("next"), headers=HEADERS).json()
        else:
            jobs = None

    if len(jobs_to_publish):
        requests.post(
            url=publish_jobs_url, headers=HEADERS, json=jobs_to_publish
        )

    print(f"{len(jobs_to_publish)} jobs have been published from company {company.get('company')}")



for company in all_companies:
    threading.Thread(target=publish_jobs, args=(company,)).start()
    time.sleep(2)
    
   