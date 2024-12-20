from scraper.Scraper import Scraper
import re
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
scraper = Scraper()
url = "https://jobs.ea.com/en_US/careers/Home/?8171=%5B10605%5D&8171_format=5683&listFilterMode=1&jobRecordsPerPage=20&jobOffset=0"

scraper.get_from_url(url)

totalJobs = int(scraper.find(
    "div", {"class": "list-controls__text__legend"}).get("aria-label").split(" ")[0])

pages = ceil(totalJobs / 20)

company = {"company": "ElectronicArts"}
finalJobs = list()

for page in range(pages):
    url = f"https://jobs.ea.com/en_US/careers/Home/?8171=%5B10605%5D&8171_format=5683&listFilterMode=1&jobRecordsPerPage=20&jobOffset={page * 20}"
    scraper.get_from_url(url)

    jobs = scraper.find("div", {"class": "results"}).find_all(
        "article", {"class": "article"})

    for job in jobs:
        job_title = job.find("h3").text.strip()
        job_link = job.find("h3").find("a").get("href")
        city = translate_city(
            job.find("span", {"class": "list-item-location"}).text.split(",")[0].strip())
        county = _counties.get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county
        })


publish_or_update(finalJobs)

logoUrl = "https://upload.wikimedia.org/wikipedia/commons/0/0d/Electronic-Arts-Logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
