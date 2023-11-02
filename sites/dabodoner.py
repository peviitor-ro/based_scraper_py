from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs)
from getCounty import get_county, remove_diacritics

url = "https://dabodoner.ro/ro/ro/joburi"
company = "Dabodoner"
scraper = Scraper()

scraper.get_from_url(url)

jobsElements = scraper.find("section", {"class": "jobs"}).find(
    "div", {"class": "row"}).find_all("div", "col-lg-6")

jobs = []

for job in jobsElements:
    job_title = job.find("div", {"class": "title"}).text.strip()
    job_link = job.find("a")["href"]
    country = "Romania"

    city = job.find("div", {"class": "location"}).text.strip()

    county = None
    if city == "Cluj":
        city = "Cluj-Napoca"

    date = job.find("div", {"class": "date"}).text.split(".")[-1].strip()

    if date >= "2023" and city != "":

        county = get_county(city)

        jobObj = create_job(
            job_title=job_title,
            job_link=job_link,
            city=city,
            county=county,
            country=country,
            company=company
        )

        jobs.append(jobObj)

    elif date >= "2023" and city == "":
        city = "Sibiu"
        county = "Sibiu"

        jobObj = create_job(
            job_title=job_title,
            job_link=job_link,
            city=city,
            county=county,
            country=country,
            company=company
        )

        jobs.append(jobObj)

for version in [1, 4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://dabodoner.ro/assets/images/logo.svg')
show_jobs(jobs)
