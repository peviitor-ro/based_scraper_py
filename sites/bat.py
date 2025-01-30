from scraper.Scraper import Scraper
from utils import translate_city, publish_or_update, publish_logo, show_jobs
from getCounty import GetCounty, remove_diacritics

_counties = GetCounty()
page = 1
url = f"https://careers.bat.com/search-jobs/results?ActiveFacetID=32003584&CurrentPage={page}&RecordsPerPage=10&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=50&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"

scraper = Scraper()
scraper.set_headers({"Accept": "application/json"})
scraper.get_from_url(url, "JSON")

html = scraper.markup.get("results")

scraper.__init__(html, "html.parser")

jobs = scraper.find("ul", {"class": "search-results-job-list"}).find_all("li")

company = {"company": "BAT"}
finalJobs = list()
while jobs:
    for job in jobs:
        
        job_title = job.find("h3").text
        job_link = "https://careers.bat.com" + job.find("a").get("href")
        location = job.find("span", {"class": "search-results-job-location"}).text.split(",")
        city = translate_city(
            remove_diacritics(
                job.find(
                    "span", {"class": "search-results-job-location"}).text.split(",")[0].strip().replace("Location: ", "")
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
    
    page += 1
    url = f"https://careers.bat.com/search-jobs/results?ActiveFacetID=32003584&CurrentPage={page}&RecordsPerPage=10&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=50&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"
    scraper.get_from_url(url, "JSON")
    html = scraper.markup.get("results")
    scraper.__init__(html, "html.parser")
    jobs = scraper.find("ul", {"class": "search-results-job-list"}).find_all("li")

publish_or_update(finalJobs)

logoUrl = "https://cdn.radancy.eu/company/1045/v2_0/img/temporary/shared/bat-logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
