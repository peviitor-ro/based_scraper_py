from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

category = 1


url = f"https://cariere.penny.ro/api_jobs/getJobs?categorie={category}"

scraper = Scraper()
scraper.get_from_url(url, "JSON")

jobs = scraper.markup

company = {"company": "Penny"}
finalJobs = list()

idx = 0

links = {
    1:"https://cariere.penny.ro/joburi/aplica/vanzari",
    2:"https://cariere.penny.ro/joburi/aplica/sediul-central",
    3: "https://cariere.penny.ro/joburi/aplica/logistica"
}

while category <= 3:
    for job in jobs:
        
        job_title = job.get("title")
        job_link = links[category] + "#" + str(idx)
        locations = job.get("location").split(",")
        cities = [
            translate_city(location.strip()) for location in locations
        ]
        counties = []

        for city in cities:
            counties.extend(_counties.get_county(city) or [])

        finalJobs.append(
            {
                "job_title": job_title,
                "job_link": job_link,
                "company": company.get("company"),
                "country": "Romania",
                "city": cities,
                "county": counties,
            }
        )
        idx += 1

    category += 1
    url = f"https://cariere.penny.ro/api_jobs/getJobs?categorie={category}"
    scraper.get_from_url(url, "JSON")
    jobs = scraper.markup



publish_or_update(finalJobs)

logo_url = "https://cariere.penny.ro/wp-content/themes/penny_cariere/img/logo.jpg"
publish_logo(company.get("company"), logo_url)
show_jobs(finalJobs)
