from scraper_peviitor import Scraper, Rules
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county, remove_diacritics

url = "https://careers.bat.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=1000&Distance=100&RadiusUnitType=0&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=1045&ResultsType=0"

scraper = Scraper()
scraper.session.headers.update({"Accept": "application/json"})

scraper.url = url

response = scraper.getJson().get("results")

scraper.soup = response

rules = Rules(scraper)

jobs = rules.getTags("li")

company = {"company": "BAT"}
finalJobs = list()

for job in jobs:
    job_title = job.find("h3").text
    job_link = "https://careers.bat.com" + job.find("a").get("href")
    city = translate_city(
        remove_diacritics(
            job.find("span", {"class": "job-location"}).text.split(",")[0].strip()
        )
    )
    county = get_county(city)

    if county:
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

publish(4, company.get("company"), finalJobs, "APIKEY")

logoUrl = "https://cdn.radancy.eu/company/1045/v2_0/img/temporary/shared/bat-logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
