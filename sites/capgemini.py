from scraper.Scraper import Scraper
from utils import translate_city, acurate_city_and_county, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
url = "https://www.capgemini.com/wp-json/macs/v1/jobs?country=ro-en&size=200"

company = {"company": "Capgemini"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup.get("data")

acurate_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})

for job in jobs:
    job_title = job.get("title")
    job_link = (
        "https://www.capgemini.com/ro-en/jobs/"
        + job.get("_id")
        + "/"
        + job.get("title").replace(" ", "-").lower()
    )

    locations = job.get("location", "").split(",")
    cities = []
    counties = []

    for location in locations:
        city = translate_city(location.strip())
        if not city:
            continue

        if acurate_city.get(city):
            cities.append(acurate_city.get(city).get("city"))
            counties.append(acurate_city.get(city).get("county"))
        else:
            county = _counties.get_county(city)
            if county:
                cities.append(city)
                counties.extend(county if isinstance(county, list) else [county])

    if not cities:
        cities = [
            "Bucuresti",
            "Cluj-Napoca",
            "Iasi",
            "Suceava",
            "Brasov",
        ]
        counties = [
            "Bucuresti",
            "Cluj",
            "Iasi",
            "Suceava",
            "Brasov",
        ]

    job_element = {
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": cities,
        "county": counties,
    }

    finalJobs.append(job_element)

try:
    publish_or_update(finalJobs)
except Exception as e:
    pass

logoUrl = "https://prod.ucwe.capgemini.com/ro-en/wp-content/themes/capgemini2020/assets/images/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
