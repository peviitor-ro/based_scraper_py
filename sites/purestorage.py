from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "PureStorage"
url = "https://boards-api.greenhouse.io/v1/boards/purestorage/jobs"

jobs = []

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

for job in scraper.markup.get("jobs", []):
    location = ((job.get("location") or {}).get("name") or "")
    locations = [item.strip() for item in location.split(";") if item.strip()]

    romania_locations = [item for item in locations if "Romania" in item]
    if not romania_locations:
        continue

    remote = []
    city = None
    county = None

    if any("Remote" in item for item in romania_locations):
        remote.append("remote")
    else:
        city = romania_locations[0].split(",")[0].strip()
        county = []

    jobs.append(
        create_job(
            job_title=job.get("title"),
            job_link=job.get("absolute_url"),
            company=company,
            country="Romania",
            city=city,
            county=county,
            remote=remote,
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Pure_Storage_logo.svg/512px-Pure_Storage_logo.svg.png",
)
show_jobs(jobs)
