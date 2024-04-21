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

data = {
    "request": {
        "JobAnnounces": [
            {
                "Id": "",
                "Function": "",
                "City": "",
            }
        ]
    }
}

response = requests.post(url, json=data).json()
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


publish_or_update(final_jobs)

publish_logo(company, "https://i.dedeman.ro/dedereact/design/images/logo.svg")

show_jobs(final_jobs)
