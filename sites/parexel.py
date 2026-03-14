from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, show_jobs, translate_city
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
results_html = scraper.markup.get("results") if isinstance(scraper.markup, dict) else None
scraper.__init__(results_html or "", "html.parser")

jobs_container = scraper.find("ul", {"id": "search-results-jobs"})
jobs = jobs_container.find_all("li", recursive=False) if jobs_container else []


def extract_romanian_locations(job):
    location_nodes = [
        job.find("span", {"class": "job-location primary-locations"}),
        job.find("span", {"class": "job-location additional-locations"}),
    ]
    romanian_locations = []

    for node in location_nodes:
        if not node:
            continue

        raw_locations = node.get_text(" ", strip=True).split(";")
        for location in raw_locations:
            parts = [part.strip() for part in location.split(",") if part.strip()]
            if parts and parts[0] == "Romania":
                romanian_locations.append(parts[1] if len(parts) > 1 else "")

    return romanian_locations

for job in jobs:
    title_node = job.find("h2")
    link_node = job.find("a", href=True)

    if not title_node or not link_node:
        continue

    href = link_node.attrs.get("href")
    if not isinstance(href, str):
        continue

    job_title = title_node.get_text(strip=True)
    job_link = "https://jobs.parexel.com" + href
    locations = extract_romanian_locations(job)
    cities = []
    counties = []
    remote = []

    for location in locations:
        if location.lower() == "remote":
            remote.append("remote")
            continue

        city = translate_city(location)
        if city not in cities:
            cities.append(city)

        county = _counties.get_county(city) or []
        for county_name in county:
            if county_name not in counties:
                counties.append(county_name)

    job_data = {
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "company": company.get("company"),
        "remote": remote,
    }

    if cities:
        job_data["city"] = cities
        job_data["county"] = counties

    finalJobs.append(job_data)

publish_or_update(finalJobs)
    
logoUrl = "https://www.parexel.com/packages/parexel/themes/parexel/img/logo.svg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finalJobs)
