from scraper.Scraper import Scraper
from getCounty import GetCounty, remove_diacritics
from utils import publish_or_update, publish_logo, show_jobs

_counties = GetCounty()
url = "https://www.autonom.ro/cariere"

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("a", {"class": "box-listing-job"})

company = {"company": "Autonom"}
finalJobs = list()

acurate_city = {"Iasi": {"city": "Iasi", "county": "Iasi"}}

for job in jobs:
    job_title = job.find("p", {"class": "nume-listing-job"}).text
    job_link = job["href"].strip()

    locations = job.find_all("span", {"class": "locatie-job"})
    cities = [remove_diacritics(city.text) for city in locations]
    counties = []

    for city in cities:
        if city in acurate_city.keys():
            counties = acurate_city[city]["county"]
        else:
            counties.extend(_counties.get_county(city) or [])

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": cities,
            "county": counties,
        }
    )

publish_or_update(finalJobs)

logoUrl = "https://www.autonom.ro/assets/uploads/autonom_logo-high-res.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
