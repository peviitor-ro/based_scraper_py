from scraper.Scraper import Scraper 
from utils import (create_job, publish, publish_logo, show_jobs, translate_city, acurate_city_and_county)
from getCounty import get_county, remove_diacritics
from math import ceil

company = "Auchan"
url = "https://cariere.auchan.ro/jobs?per_page=1000"
scraper = Scraper()
scraper.get_from_url(url)

total_jobs = scraper.find("div", class_="sumarry").text.split(" ")[-3]

jobs = list()

pages = ceil(int(total_jobs) / 1000)

acurate_city = acurate_city_and_county(
    Iasi = {
        "city": "Iasi",
        "county": "Iasi"
    },
    Galati = {
        "city": "Galati",
        "county": "Galati"
    },
    )

for page in range(pages):
    url = f"https://cariere.auchan.ro/jobs?page={page + 1}&per_page={pages * 1000}"
    scraper.get_from_url(url)

    jobs_elements = scraper.find_all("a", class_="job")
    for job in jobs_elements:
        city = translate_city(remove_diacritics(job.find("div", class_="js-job-oras").text.strip()))
        county = ""

        if city in acurate_city.keys():
            city = acurate_city[city]["city"]
            county = acurate_city[city]["county"]
        else:
            county = get_county(city)

        jobs.append(create_job(
            job_title=job.find("div", class_="job-title").text,
            job_link=job["href"],
            company=company,
            country="Romania",
            city=city,
            county=county,
        ))

for version in [1, 4]:
    publish(version, company, jobs, "APIKEY")

publish_logo(company, "https://res.cloudinary.com/smartdreamers/image/upload/v1685443347/company_logos/82780f0401d4b4b2097c8f79d13fa468.svg")
show_jobs(jobs)