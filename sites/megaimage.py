from utils import (
    translate_city,
    acurate_city_and_county,
    create_job,
    show_jobs,
    publish_logo,
    publish_or_update,
)
from getCounty import GetCounty
from requests.exceptions import ConnectTimeout, ConnectionError
import requests
import sys

company = "MegaImage"

url = "https://cariere.mega-image.ro/api/vacancy/?options%5Bsort_order%5D=desc&sort=created&sortDir=DESC&pageSize=1000"
_counties = GetCounty()

headers = {"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}

try:
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    jobs = data.get("vacancies")
except (ConnectTimeout, ConnectionError):
    print("Could not connect to the website. Exiting successfully.")
    finalJobs = []
    publish_or_update(finalJobs)
    logo_url = "https://cariere.mega-image.ro/uploads/MEGA%20IMAGE%20LOGO.png"
    publish_logo(company, logo_url)
    show_jobs(finalJobs)
    sys.exit(0)

finalJobs = list()

acurate_city = acurate_city_and_county(
    iasi={"city": "Iasi", "county": "Iasi"},
    municipiul_bucuresti={"city": "Bucuresti", "county": "Bucuresti"},
    stefanestii_de_jos={"city": "Stefanestii de Jos", "county": "Ilfov"},
    cluj_napoca={"city": "Cluj-Napoca", "county": "Cluj"},
)


for job in jobs:
    job_title = job.get("title")
    if not job_title:
        continue

    job_link = (
        "https://cariere.mega-image.ro/post-vacant/"
        + str(job.get("id"))
        + "/"
        + job.get("slug")
    )

    job_element = create_job(
        job_title=job_title,
        job_link=job_link,
        company=company,
        country="Romania",
    )

    city = translate_city(job.get("city").title())

    if acurate_city.get(city.replace(" ", "_").replace("-", "_").lower()):
        job_element["city"] = acurate_city.get(
            city.replace(" ", "_").replace("-", "_").lower()
        ).get("city")
        job_element["county"] = acurate_city.get(
            city.replace(" ", "_").replace("-", "_").lower()
        ).get("county")
    else:
        job_element["city"] = city
        job_element["county"] = _counties.get_county(city)

    finalJobs.append(job_element)

publish_or_update(finalJobs)

logo_url = "https://cariere.mega-image.ro/uploads/MEGA%20IMAGE%20LOGO.png"
publish_logo(company, logo_url)
show_jobs(finalJobs)
