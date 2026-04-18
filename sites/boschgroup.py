from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
company = "BoschGroup"
url = "https://api.smartrecruiters.com/v1/companies/BoschGroup/postings?offset="

offset = 0
jobs = []

scraper = Scraper()
while True:
    scraper.get_from_url(url + str(offset), type="JSON")
    content = scraper.markup.get("content", [])

    if not content:
        break

    for job in content:
        location = job.get("location") or {}
        country = (location.get("country") or "").lower()
        full_location = location.get("fullLocation") or ""

        if country != "ro" and "Romania" not in full_location:
            continue

        city = translate_city(remove_diacritics(location.get("city") or ""))
        county = _counties.get_county(city) if city else []

        jobs.append(
            create_job(
                job_title=job.get("name"),
                job_link="https://jobs.smartrecruiters.com/BoschGroup/" + job.get("id"),
                company=company,
                country="Romania",
                city=city,
                county=county,
            )
        )

    offset += 100

publish_or_update(jobs)
publish_logo(
    company,
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Bosch-logo.svg/512px-Bosch-logo.svg.png",
)
show_jobs(jobs)
