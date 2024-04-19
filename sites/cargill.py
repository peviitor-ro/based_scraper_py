from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find("span", {"class": "job-location"}).text.split("|")

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(translate_city(location.split(",")[0].strip()))
        county = _counties.get_county(city)

        if county:
            cities.append(city)
            counties.extend(county)

    return cities, counties


url = "https://careers.cargill.com/en/search-jobs/Romania/23251/2/798549/46/25/50/2"

company = {"company": "Cargill"}
finalJobs = list()

scraper = Scraper()
scraper.set_headers(
    {
        "Accept-Language": "en-GB,en;q=0.9",
    }
)
scraper.get_from_url(url)

jobs = scraper.find("section", {"id": "search-results-list"}).find_all("li")

for job in jobs:
    job_title = job.find("h3").text.strip()
    job_link = "https://careers.cargill.com" + job.find("a").get("href")
    city = [
        translate_city(
            remove_diacritics(
                job.find("span", {"class": "job-location"}).text.split(",")[0].strip()
            )
        )
    ]
    county = []

    for c in city:
        county.extend(_counties.get_county(c) or [])

    if not county:
        city, county = get_aditional_city(job_link)

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

logoUrl = "https://tbcdn.talentbrew.com/company/23251/18994/content/logo-full.png"

publish_logo(company.get("company"), logoUrl)
show_jobs(finalJobs)
