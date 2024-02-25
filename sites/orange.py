from requests import get
from json import dumps
from getCounty import get_county

url = "https://www.orange.ro/ux-admin/api/jobs/getJobs?&limit=10000"

final_jobs = []
company = "orange"

response = get(url)

jobs = response.json()

for job in jobs:
    job_info = {
        "title": job["title"],
        "link": job["url"],
        "country": "Romania",
        "city": job["location"][0]["name"],
        "county": get_county(job["location"][0]["name"]),
        "company": company,
    }
    final_jobs.append(job_info)

print(dumps(final_jobs, indent=2))