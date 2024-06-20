from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, acurate_city_and_county
from getCounty import GetCounty, remove_diacritics

_coubties = GetCounty()

url = "https://api.ejobs.ro/companies/286239"
company = "CARTOFISSERIE"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("jobs")
acurate_city = acurate_city_and_county()

final_jobs = []

for job in jobs:
    job_title = job.get("title")
    slug = job.get("slug")
    job_id = job.get("id")
    job_url = f"https://www.ejobs.ro/user/locuri-de-munca/{slug}/{job_id}"
    locations = job.get("locations")
    cities = [
        remove_diacritics(location.get("address").split(",")[0].strip())
        for location in locations
        if location.get("address")
    ]
    counties = []

    for city in cities:
        counties.extend(_coubties.get_county(city))
        

    country = "Romania"
    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_url,
            "city": cities,
            "county": counties,
            "country": country,
            "company": company,
        }
    )

publish_or_update(final_jobs)
publish_logo(company, "https://content.ejobs.ro/img/logos/2/286239.png")

show_jobs(final_jobs)
