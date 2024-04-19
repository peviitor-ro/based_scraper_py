from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()

url = "https://www.betfairromania.ro/find-a-job/?search=&country=Romania&pagesize=1000#results"

scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("div", {"class": "card-job"})

company = {"company": "Betfair"}
finalJobs = list()

for job in jobs:
    job_title = job.find("h2", {"class": "card-title"}).text.strip()
    job_link = "https://www.betfairromania.ro" + job.find("a").get("href")
    cities_elements = job.find("li").text.split("/")

    job_element = {
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
    }

    cities = [
        translate_city(city.split(",")[0].strip())
        for city in cities_elements
        if _counties.get_county(city.split(",")[0].strip())
    ]

    counties = []

    for city in cities:
        counties.extend(_counties.get_county(city))

    if not cities or not counties:
        job_element["remote"] = "Remote"
    else:
        job_element["city"] = cities
        job_element["county"] = counties

    finalJobs.append(job_element)

publish_or_update(finalJobs)

logoUrl = "https://www.betfairromania.ro/images/logo.svg?v1.1"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
