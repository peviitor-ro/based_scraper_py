import requests
from utils import (
    publish_or_update,
    publish_logo,
    create_job,
    show_jobs,
    translate_city,
)
from getCounty import remove_diacritics

url = "https://careers.publicisgroupe.com/api/jobs"

company = "PublicisGroupe"
finalJobs = list()

counties = {
    "Bucuresti": "Bucuresti",
    "Brasov": "Brasov",
    "Cluj-Napoca": "Cluj",
    "Iasi": "Iasi",
    "Timisoara": "Timis",
}

offset = 0
limit = 100

while True:
    response = requests.get(
        url,
        params={"country": "Romania", "limit": limit, "offset": offset},
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    jobs = data.get("jobs") or []
    if not jobs:
        break

    for item in jobs:
        job = item.get("data") or item
        job_title = (job.get("title") or "").strip()
        job_link = (job.get("meta_data") or {}).get("canonical_url") or job.get("apply_url")

        if not job_title or not job_link:
            continue

        city = translate_city(remove_diacritics((job.get("city") or "Bucuresti").strip()))

        finalJobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                country="Romania",
                city=city,
                county=counties.get(city, city),
                company=company,
            )
        )

    offset += len(jobs)
    if offset >= (data.get("totalCount") or data.get("count") or 0):
        break


publish_or_update(finalJobs)

publish_logo(
    company,
    "https://c.smartrecruiters.com/sr-company-logo-prod-aws-dc1/58822766e4b0680b1154ae69/huge?r=s3&_1533642429153",
)
show_jobs(finalJobs)
