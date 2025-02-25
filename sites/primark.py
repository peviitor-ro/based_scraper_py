from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = "https://ro.cariera.primark.com/loc/romania-posturi-vacante/39017/798549/2"

company = {"company": "Primark"}
finalJobs = list()

scraper = Scraper()
scraper.set_headers({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.get_from_url(url, verify=False)

jobs = scraper.find("section", {"id": "search-results-list"}).find_all("li")

for job in jobs:
    job_title = job.find("h3").text.strip()
    job_link = "https://ro.cariera.primark.com" + job.find("a").get("href")
    city = translate_city(job.find(
        "span", {"class": "job-list-info--location"}).text.split(",")[0].strip())
    county = _counties.get_county(city)

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city,
        "county": county,
    })

publish_or_update(finalJobs)

logoUrl = "https://primedia.primark.com/i/primark/logo-primark?w=200"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
