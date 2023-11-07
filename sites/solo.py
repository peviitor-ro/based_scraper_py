import requests
from utils import publish, publish_logo

apiurl = "https://cariere.solo.ro/api/jobs/"
company = "SOLO"
logo = "https://cariere.solo.ro/assets/img/logo-black.svg"

raw_jobs = requests.get(apiurl + "list/").json()
jobs = []

for job in jobs:
    title = job["Title"]
    city = "Bucuresti"
    country = "Romania"
    job_link = f"https://cariere.solo.ro/job/{job['Slug']}"

    jobs.append({
        "job_title": title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

for v in [1, 4]:
    publish(v, company, jobs, "MSCDAVID")

publish_logo(company, logo)