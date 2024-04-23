from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

scraper = Scraper()
url = "https://mingle.ro/api/boards/careers-page/jobs?company=ppc&page=0&pageSize=1000"

scraper.get_from_url(url, "JSON")

company = {"company": "PPCEnergy"}
finaljobs = list()

jobs = scraper.markup.get("data").get("results")

for job in jobs:
    job_title = job.get("title")
    job_link = f"https://enel.mingle.ro/en/apply/{job.get('uid')}"
    locations = job.get("locations") or []

    cities = []
    counties = []

    for city in locations:
        county = _counties.get_county(translate_city(city.get("label"))) or []

        if len(county):
            cities.append(translate_city(city.get("label")))
            counties.extend(county)


    finaljobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": list(set(cities)),
            "county": list(set(counties)),
        }
    )

publish_or_update(finaljobs)

logoUrl = "https://www.ppcenergy.ro/wp-content/uploads/logo.svg?w=1024"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
