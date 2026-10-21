from utils import (
    translate_city,
    acurate_city_and_county,
    create_job,
    show_jobs,
    publish_logo,
    publish_or_update,
)
from getCounty import GetCounty
from requests.exceptions import ConnectTimeout, ConnectionError, RequestException
import requests
import sys
import time

company = "MegaImage"

url = "https://cariere.mega-image.ro/api/vacancy/?options%5Bsort_order%5D=desc&sort=created&sortDir=DESC&pageSize=1000"
_counties = GetCounty()

headers = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

MAX_ATTEMPTS = 3
RETRY_DELAY = 5


def fetch_jobs():
    last_error = None

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                raise RequestException(
                    f"Unexpected status code: {response.status_code}"
                )

            data = response.json()
            return data.get("vacancies") or []
        except (RequestException, ValueError) as error:
            last_error = error
            if attempt < MAX_ATTEMPTS - 1:
                print(
                    f"Attempt {attempt + 1} failed ({error}). "
                    f"Retrying in {RETRY_DELAY}s..."
                )
                time.sleep(RETRY_DELAY)

    raise last_error


try:
    jobs = fetch_jobs()
except (ConnectTimeout, ConnectionError, RequestException, ValueError):
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

    city = translate_city((job.get("city") or "").title())

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
