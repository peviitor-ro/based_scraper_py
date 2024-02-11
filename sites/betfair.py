from scraper_peviitor import Scraper, Rules
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county

url = "https://www.betfairromania.ro/find-a-job/?search=&country=Romania&pagesize=1000#results"

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("div", {"class": "card-job"})

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
        if get_county(city.split(",")[0].strip())
    ]

    county = [get_county(city) for city in cities if get_county(city)]

    if not cities or not county:
        job_element["remote"] = "Remote"
    else:
        job_element["city"] = cities
        job_element["county"] = county

    finalJobs.append(job_element)

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://www.betfairromania.ro/images/logo.svg?v1.1"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
