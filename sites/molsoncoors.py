from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty
from math import ceil

_counties = GetCounty()
url = "https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow=1"

company = {"company": "MolsonCoors"}
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url, verify=False)

totalJobs = int(
    scraper.find("span", {"class": "paginationLabel"}
                 ).find_all("b")[-1].text.strip()
)

paginate = ceil(totalJobs / 25)

acurate_city = acurate_city_and_county(
    Alba={"city": "Alba Iulia", "county": "Alba"})
jobs = scraper.find("table", {"id": "searchresults"}).find(
    "tbody").find_all("tr")

for page in range(0, paginate):
    for job in jobs:
        job_title = job.find("a").text.strip()
        job_link = "https://jobs.molsoncoors.com" + job.find("a").get("href")

        city = translate_city(
            job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip())
        counties = []

        if acurate_city.get(city):
            city = acurate_city.get(city).get("city")
            counties.append(acurate_city.get(city).get("county"))
        else:
            counties.extend(_counties.get_county(city) or [])

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "country": "Romania",
                "city": city,
                "county": counties,
                "company": company.get("company"),
            }
        )
    url = f"https://jobs.molsoncoors.com/MolsonCoors_GBSRomania/search/?q=Romania&startrow={page + 1 * 25}"
    scraper.get_from_url(url, verify=False)
    jobs = scraper.find("table", {"id": "searchresults"}).find(
        "tbody").find_all("tr")

publish_or_update(finalJobs)

logoUrl = "https://rmkcdn.successfactors.com/e2403c2e/b8073680-5e29-45a9-8c61-4.png"
publish_logo(company.get("company"), logoUrl)
show_jobs(finalJobs)
