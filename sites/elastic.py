from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "Elastic"
url = "https://boards-api.greenhouse.io/v1/boards/elastic/jobs"

jobs = []

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

for job in scraper.markup.get("jobs", []):
    location = ((job.get("location") or {}).get("name") or "")
    metadata = job.get("metadata") or []
    metadata_text = " ".join(str(item) for item in metadata)

    if "Romania" not in location and "Romania" not in metadata_text:
        continue

    jobs.append(
        create_job(
            job_title=job.get("title"),
            job_link=job.get("absolute_url"),
            company=company,
            country="Romania",
            remote=["remote"],
        )
    )

publish_or_update(jobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Elastic_logo.svg/512px-Elastic_logo.svg.png",
)
show_jobs(jobs)
