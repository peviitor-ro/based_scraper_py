import requests
from utils import publish, publish_logo, show_jobs

url = "https://join-us.tickbird.com/recruit/v2/public/Job_Openings?pagename=Careers&source=CareerSite&extra_fields=%5B%22State%22,%22Salary%22,%22Industry%22%5D"
company = "TICKBIRD"

final_jobs = []
response = requests.get(url)
data = response.json()

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

publish(4, company, final_jobs, "Grasum_Key")

publish_logo(company, "https://tickbird.com/assets/images/logo/tickbird-logo.svg")

show_jobs(final_jobs)
