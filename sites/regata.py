from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
company = "Regata"

BASE_URL = "https://regata.mingle.ro"
API_URL = f"{BASE_URL}/api/boards/careers-page/jobs"

scraper = Scraper()

page = 0
jobs = []

while True:
    scraper.get_from_url(
        f"{API_URL}?company=regata&page={page}&pageSize=50",
        "JSON",
        verify=False,
    )

    data = scraper.markup or {}
    results = data.get("data", {}).get("results", [])
    pagination = data.get("data", {}).get("pagination", {})

    if not results:
        break

    for job in results:
        job_title = job.get("title", "")
        job_uid = job.get("uid", "")
        job_link = f"{BASE_URL}/ro/apply/{job_uid}"

        locations = job.get("locations") or []
        location_names = [loc.get("label", "") for loc in locations if loc.get("label")]

        city = translate_city(location_names[0]) if location_names else ""
        county = _counties.get_county(city) if city else ""

        jobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city=city,
                county=county,
            )
        )

    if not pagination.get("hasNext", False):
        break

    page += 1

publish_or_update(jobs)
publish_logo(
    company,
    "https://regata.b-cdn.net/media/favicon/stores/1/FAVICON_32.png",
)
show_jobs(jobs)
print(f"Total jobs: {len(jobs)}")