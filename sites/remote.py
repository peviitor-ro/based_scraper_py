from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "Remote"
url = "https://boards-api.greenhouse.io/v1/boards/remotecom/jobs"

jobs = []

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

for job in scraper.markup.get("jobs", []):
    metadata = job.get("metadata") or []
    metadata_text = " ".join(str(item) for item in metadata)
    location = ((job.get("location") or {}).get("name") or "")

    if "Romania" not in metadata_text and "Romania" not in location:
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
    "https://images.ctfassets.net/sg0x4vq2yn9t/4xw7O6q3i0DGvU0rNjn4L1/d9cdb9a8ba3dbf1f367cbf8c450271f4/remote-logo-color.png",
)
show_jobs(jobs)
