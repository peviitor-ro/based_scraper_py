from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty
from urllib.parse import quote

_counties = GetCounty()
url = "https://careers.veeam.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=150&TotalContentResults=&Distance=50&RadiusUnitType=1&Keywords=&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Section+11+-+Search+Results+List&SearchFiltersModuleName=Section+11+-+Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=22681&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"

company = "Veeam"
jobs = []

scraper = Scraper()
scraper.get_from_url(url, "JSON")

scraper.__init__(scraper.markup.get("results"), "html.parser")

jobs_elements = scraper.find_all("li")

for job in jobs_elements:
    job_title = job.find("h2").text.strip()
    job_link = "https://careers.veeam.com" + job.find("a").get("href")
    location = job.find(
        "span", {"class": "job-list__location"}).text.split(",")[0].strip()
    city = translate_city(location)
    county = _counties.get_county(city)
    jobObj = create_job(
        job_title=job_title,
        job_link=job_link,
        company=company,
        country="Romania",
        city=city,
        county=county,
    )

    jobs.append(jobObj)

publish_or_update(jobs)

publish_logo(company, "https://img.veeam.com/careers/logo/veeam/veeam_logo_bg.svg")
show_jobs(jobs)
