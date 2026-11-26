from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs

company = "Remote"
url = "https://apply.remote.com/api/public/jobs"

jobs = []

scraper = Scraper()
scraper.get_from_url(url, type="JSON")

for job in scraper.markup.get("jobs", []):
    if job.get("status") != "open" or not job.get("accepting_applications"):
        continue

    if "EMEA" not in (job.get("location") or ""):
        continue

    jobs.append(
        create_job(
            job_title=job.get("title"),
            job_link=f"https://apply.remote.com/jobs/{job.get('public_id')}",
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
