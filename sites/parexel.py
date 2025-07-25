from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty

_counties = GetCounty()
url = "https://jobs.parexel.com/en/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=877&ResultsType=0"

company = {"company": "Parexel"}
finalJobs = []

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

    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": "Bucuresti",
        "county": "Bucuresti",
        "company": company.get("company")
    })

publish_or_update(finalJobs)
    
logoUrl = "https://www.parexel.com/packages/parexel/themes/parexel/img/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
