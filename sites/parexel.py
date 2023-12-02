from scraper.Scraper import Scraper
import json
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county

url = "https://jobs.parexel.com/en/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=877&ResultsType=0"

company = {"company": "Parexel"}
finalJobs = list()

scraper = Scraper()
scraper.set_headers({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.get_from_url(url, "JSON")
scraper.__init__(scraper.markup.get("results"), "html.parser")

jobs = scraper.find_all("li")

for job in jobs:
    job_title = job.find("h2").text
    job_link = "https://jobs.parexel.com" + job.find("a").get("href")
    cities = []
    counties = []

    locations = job.find("span", {"class": "job-city"})

    if locations:
        city = translate_city(locations.text)
        county = get_county(city)
        if county:
            cities.append(city)
            counties.append(county)

    locations = job.find(
        "span", {"class": "additional-locations-values"})
    if locations:
        locations = locations.text.split(";")
        for location in locations:
            city = translate_city(location.split(",")[0].strip())
            county = get_county(city)
            if county and county not in counties:
                cities.append(city)
                counties.append(get_county(city))

    if not cities and not counties:
        cities.append("Bucuresti")
        counties.append("Bucuresti")

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": cities,
        "county": counties,
        "company": company.get("company")
    })

for version in [1, 4]:
    publish(version, company.get("company"), finalJobs, 'APIKEY')
    
logoUrl = "https://www.parexel.com/packages/parexel/themes/parexel/img/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
