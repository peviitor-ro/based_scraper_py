# TODO: De verificat cand sunt joburi noi

from scraper.Scraper import Scraper
from utils import (
    translate_city,
    acurate_city_and_county,
    publish_or_update,
    publish_logo,
    show_jobs,
)
from getCounty import GetCounty

_counties = GetCounty()
url = "https://cariere.romstal.ro/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_location=&optionsFacetsDD_department="
scraper = Scraper()
scraper.get_from_url(url)

jobs = scraper.find_all("li", {"class": "job-tile"})

company = {"company": "Romstal"}
finalJobs = list()

acurate_city = acurate_city_and_county(Iasi={"city": "Iasi", "county": "Iasi"})

for job in jobs:
    job_title = job.find("a", {"class": "jobTitle-link"}).text.strip()
    job_link = (
        "https://cariere.romstal.ro" + job.find("a", {"class": "jobTitle-link"})["href"]
    )
    city = job.find("div", {"class": "location"}).find("div").text.split(",")[0].strip()

    if "SECTOR" in city:
        city = "Bucuresti"

    city = translate_city(city.title().replace(" - ", "-"))

    if acurate_city.get(city):
        county = acurate_city.get(city).get("county")
    else:
        county = _counties.get_county(city)

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
        }
    )

publish_or_update(finalJobs)

logo_url = "https://rmkcdn.successfactors.com/129e1186/1bb86fb4-a088-4fcc-b390-5.png"
publish_logo(company.get("company"), logo_url)

show_jobs(finalJobs)
