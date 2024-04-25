from scraper.Scraper import Scraper
from getCounty import remove_diacritics, GetCounty
from utils import publish_or_update, publish_logo, show_jobs, translate_city


def get_aditional_city(url):
    scraper = Scraper()
    scraper.get_from_url(url)

    locations = scraper.find(
        "span", {"class": "job-description__location-pin"}
    ).text.split("|")

    cities = []
    counties = []

    for location in locations:
        city = remove_diacritics(translate_city(location.split(",")[0].strip()))
        county = _counties.get_county(city)

        if county:
            cities.append(city)
            counties.extend(county)

    return cities, counties

_counties = GetCounty()
url = "https://jobs.intel.com/en/search-jobs/Romania/599/2/798549/46/25/50/2"

company = "Intel"
finalJobs = list()

scraper = Scraper()
scraper.set_headers(
    {
        "Accept-Language": "en-GB,en;q=0.9",
    }
)

scraper.get_from_url(url)

jobs = scraper.find("section", {"id": "search-results-list"}).findAll("li")

for job in jobs:
    job_title = job.find("h2").text.strip()
    job_link = "https://jobs.intel.com" + job.find("a").get("href")

    cities = job.find("span", {"class": "job-location"}).text.strip()
    if "Multiple Locations" in cities:
        cities, counties = get_aditional_city(job_link)
    else:
        locations = cities.split(",")
        cities = remove_diacritics(locations[0].strip())
        counties = remove_diacritics(locations[1].strip())

    finalJobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": "Romania",
            "city": cities,
            "county": counties,
        }
    )


publish_or_update(finalJobs)

logoUrl = (
    "https://tbcdn.talentbrew.com/company/599/gst-v1_0/img/logo/logo-intel-blue.svg"
)
publish_logo(company, logoUrl)
show_jobs(finalJobs)
