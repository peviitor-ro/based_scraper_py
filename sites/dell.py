from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

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
    id = uuid.uuid4()
    job_title = job.find("h2").text.strip()
    job_link = "https://jobs.dell.com" + job.find("a").get("href")
    city = job.find("span", {"class": "job-location-search"}).text.split(",")[0].strip()
    
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print(json.dumps(finaljobs, indent=4))

loadingData(finaljobs, company.get("company"))

logoUrl = "https://tbcdn.talentbrew.com/company/375/v4_0/img/logos/delltech_logo_prm_blue_rgb.jpg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))




