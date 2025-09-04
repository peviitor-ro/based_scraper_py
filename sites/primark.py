from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty

_counties = GetCounty()
url = "https://careers.primark.com/ro/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=10&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=798549&FacetType=2&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=3&FacetFilters%5B0%5D.Display=Rom%C3%A2nia&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Results+Filters&SortCriteria=0&SortDirection=0&SearchType=3&OrganizationIds=8171&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"

company = {"company": "Primark"}
finalJobs = list()

scraper = Scraper()
scraper.set_headers({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.get_from_url(url,"JSON" ,verify=False)

scraper.__init__(scraper.markup.get("results"), "html.parser")

jobs = scraper.find("section", {"id": "search-results-list"}).find_all("li")

for job in jobs:
    job_title = job.find("h3").text.strip()
    job_link = "https://careers.primark.com" + job.find("a").get("href")
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
