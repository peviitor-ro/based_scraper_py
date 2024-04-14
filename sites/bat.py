from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
url = "https://careers.bat.com/search-jobs/results?ActiveFacetID=798549&CurrentPage=1&RecordsPerPage=1000&Distance=50&RadiusUnitType=0&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=56&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&ResultsType=0"

scraper = Scraper()
scraper.set_headers({"Accept": "application/json"})
scraper.get_from_url(url, "JSON")

html = scraper.markup.get("results")

scraper.__init__(html, "html.parser")

jobs = scraper.find("ul", {"class": "results-list"}).find_all("li")

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
    county = _counties.get_county(city)

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

publish_or_update(finalJobs)

logoUrl = "https://cdn.radancy.eu/company/1045/v2_0/img/temporary/shared/bat-logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)

print(len(finalJobs))   
