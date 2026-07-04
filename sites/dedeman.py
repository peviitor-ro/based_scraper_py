import requests
from utils import (
    create_job,
    publish_or_update,
    publish_logo,
    acurate_city_and_county,
    show_jobs,
    translate_city,
)
from getCounty import GetCounty

_counties = GetCounty()

url = "https://recrutare.dedeman.ro/api/sinapsi/jobs"
company = "DEDEMAN"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://recrutare.dedeman.ro/",
    "Origin": "https://recrutare.dedeman.ro",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

data = {"request": {"FilterByCity": ""}}

response = requests.post(url, json=data, headers=headers).json()
jobs = response["d"]["JobAnnounces"]

final_jobs = []

acurate_city = acurate_city_and_county()

for job in jobs:
    city = translate_city(job["City"])
    if acurate_city.get(city.replace("-", "_")):
        county = acurate_city.get(city.replace("-", "_")).get("county")
        city = acurate_city.get(city.replace("-", "_")).get("city")
    else:
        county = _counties.get_county(city)

    input_job_id = job["Id"]
    format_job_title = "+".join(job["Function"].lower().split())
    output_job_link = f"https://recrutare.dedeman.ro/detalii-post?job={format_job_title}&id={input_job_id}"
    final_jobs.append(
        create_job(
            job_title=job["Function"],
            company=company,
            city=city,
            county=county,
            country="Romania",
            job_link=output_job_link,
        )
    )


try:
    publish_or_update(final_jobs)
except Exception as e:
    print(f"Failed to publish jobs: {e}")

publish_logo(company, "https://i.dedeman.ro/dedereact/design/images/logo.svg")

show_jobs(final_jobs)
