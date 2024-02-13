from scraper_peviitor import Scraper, Rules
from utils import translate_city, publish, publish_logo, show_jobs
from getCounty import get_county

url = "https://jobs.dell.com/search-jobs/results?ActiveFacetID=0&RecordsPerPage=1000&Distance=50&RadiusUnitType=0&ShowRadius=False&IsPagination=False&FacetTerm=798549&FacetType=2&FacetFilters%5B0%5D.ID=798549&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=25&FacetFilters%5B0%5D.Display=Romania&FacetFilters%5B0%5D.IsApplied=true&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=3&OrganizationIds=375&ResultsType=0"

company = {"company": "Dell"}
finaljobs = list()

scraper = Scraper()
scraper.session.headers.update({"Accept": "application/json"})
scraper.url = url

html = scraper.getJson().get("results")

scraper.soup = html
rules = Rules(scraper)

jobs = rules.getTags("li")

for job in jobs:
    job_title = job.find("h2").text.strip()
    job_link = "https://jobs.dell.com" + job.find("a").get("href")
    city = translate_city(
        job.find("span", {"class": "job-location-search"}).text.split(",")[0].strip()
    )

    job_element = {
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "company": company.get("company"),
    }

    if "Remote" in city:
        job_element["remote"] = "Remote"
    else:
        job_element["city"] = city
        job_element["county"] = get_county(city)

    finaljobs.append(job_element)

publish(4, company.get("company"), finaljobs, "Grasum_Key")

logoUrl = "https://tbcdn.talentbrew.com/company/375/v4_0/img/logos/delltech_logo_prm_blue_rgb.jpg"
publish_logo(company.get("company"), logoUrl)

show_jobs(finaljobs)
