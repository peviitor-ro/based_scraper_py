from scraper.Scraper import Scraper
from utils import show_jobs, publish_or_update, publish_logo, translate_city
from getCounty import GetCounty
from bs4 import BeautifulSoup

_counties = GetCounty()

company = "sanofi"

additionalHeaders = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
}

scraper = Scraper()
scraper.set_headers(additionalHeaders)

url = "https://jobs.sanofi.com/en/search-jobs/results?CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=2&ResultsType=0"
scraper.get_from_url(url, "JSON", verify=False)

soup = BeautifulSoup(scraper.markup.get("results"), "html.parser")

jobs = soup.find_all("li")
final_jobs = []

for job in jobs:
    location_span = job.find("span", {"class": "job-location"})
    if location_span is None:
        continue
    location = location_span.text.split(",")[0].strip().replace("Location: ", "")
    if "Romania" not in location and "romania" not in location:
        continue

    job_title = job.find("h2")
    job_link = job.find("a")
    if job_title is None or job_link is None:
        continue

    city = translate_city(location)
    county = _counties.get_county(city)

    final_jobs.append(
        {
            "job_title": job_title.text.strip(),
            "job_link": "https://jobs.sanofi.com" + job_link.get("href"),
            "country": "Romania",
            "company": company,
            "city": city,
            "county": county,
        }
    )

publish_or_update(final_jobs)

logoUrl = "https://en.jobs.sanofi.com/search-jobs/results?CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=2&ResultsType=0"
publish_logo(company, logoUrl)

show_jobs(final_jobs)
