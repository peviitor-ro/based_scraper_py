from scraper.Scraper import Scraper
import json
from getCounty import GetCounty
from utils import translate_city, publish_logo, publish_or_update, show_jobs
from math import ceil

_counties = GetCounty()
url = "https://www.inetum.com/en/jobs?f%5B0%5D=region%3A1068"

company = {"company": "Inetum"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)

totalJobs = int(scraper.find("li", {"id": "1068"}).find("span", {"class":"facet-item__count"}).text.replace("(", "").replace(")", "").strip())

paginations = ceil(totalJobs / 9)

for page in range(paginations):
    scraper.get_from_url("https://www.inetum.com/en/jobs?f%5B0%5D=region%3A1068&page=" + str(page))

    jobs = scraper.find_all("div", {"class": "node node-job node-teaser"})

    for job in jobs:
        job_title = job.find("h3", {"class":"card-title"}).text.strip()
        job_link = "https://www.inetum.com" + job.find("a").get("href")
        city = translate_city(job.find("p", {"class": "card-text"}).text.split("-")[-1].split("/")[0].strip())
        county = _counties.get_county(city)
        remote = []

        jobs_types = ["Remote", "Hybrid"]


        for types in jobs_types:
            if types in job.find("p", {"class": "card-text"}).text.split("-")[-1].strip():
                remote.append(types) 

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": remote,
        })


publish_or_update(finalJobs)

logoUrl = "https://vtlogo.com/wp-content/uploads/2021/05/inetum-vector-logo-small.png"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)