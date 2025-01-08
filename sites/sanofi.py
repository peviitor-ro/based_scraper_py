from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty

_counties = GetCounty()

company = "sanofi"
url = "https://en.jobs.sanofi.com/search-jobs/results?ActiveFacetID=798549&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&ShowRadius=False&IsPagination=False&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=13&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&ResultsType=0"

additionalHeaders = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
}

scraper = Scraper()

scraper.set_headers(additionalHeaders)

scraper.get_from_url(url, "JSON", verify=False)
scraper.__init__(scraper.markup.get("results"), "html.parser")

jobs = scraper.find_all("ul")[1].find_all("li")
final_jobs = []

for job in jobs:
    job_title = job.find("h2").text.strip()
    job_link = "https://jobs.sanofi.com" + job.find("a")["href"]
    location = job.find("span", {"class": "job-location"}).text.split(",")[
        0].strip().replace("Location: ", "")
    city = translate_city(location)
    county = _counties.get_county(city)

    final_jobs.append(
        {
            "job_title": job_title,
            "job_link": job_link,
            "remote": "no",
            "country": "Romania",
            "company": company,
            "city": city,
            "county": county,
        }
    )

publish_or_update(final_jobs)

logoUrl = "hhttps://en.jobs.sanofi.com/search-jobs/results?ActiveFacetID=798549&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&ShowRadius=False&IsPagination=False&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=13&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&ResultsType=0"
publish_logo(company, logoUrl)

show_jobs(final_jobs)
