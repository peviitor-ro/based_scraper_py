from scraper_peviitor import Scraper
from utils import translate_city, acurate_city_and_county, publish, publish_logo, show_jobs
from getCounty import get_county

url = "https://www.capgemini.com/wp-json/macs/v1/jobs?country=ro-en&size=200"

company = {"company": "Capgemini"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("data")

allCities = [
    "Bucuresti",
    "Cluj-Napoca",
    "Iasi",
    "Suceava",
    "Brasov",
]
allCounties = [
    "Bucuresti",
    "Cluj",
    "Iasi",
    "Suceava",
    "Brasov",
]

acurate_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})

for job in jobs:
    job_title = job.get("title")
    job_link = (
        "https://www.capgemini.com/ro-en/jobs/"
        + job.get("_id")
        + "/"
        + job.get("title").replace(" ", "-").lower()
    )
    city = translate_city(job.get("location"))
    county = get_county(city)

    job_element = {
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
    }

    if not county:
        job_element["city"] = allCities
        job_element["county"] = allCounties
    elif acurate_city.get(city):
        job_element["city"] = acurate_city.get(city).get("city")
        job_element["county"] = acurate_city.get(city).get("county")
    else:
        job_element["city"] = city
        job_element["county"] = county

    finalJobs.append(job_element)

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://prod.ucwe.capgemini.com/ro-en/wp-content/themes/capgemini2020/assets/images/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
