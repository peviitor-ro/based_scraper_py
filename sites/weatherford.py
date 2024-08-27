from scraper.Scraper import Scraper
from utils import create_job, publish_or_update, publish_logo, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()

url = "https://fa-exmi-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000000465601,sortBy=POSTING_DATES_DESC"

company = "Weatherford"
jobs = []

scraper = Scraper()
headers = {
  "Content-Type": "application/json",
}
scraper.set_headers(headers)
scraper.get_from_url(url, "JSON")

elements = scraper.markup.get("items")[0].get("requisitionList")

jobs = [
    {
        "job_title": job.get("Title"),
        "job_link": "https://careers.weatherford.com/#en/sites/CX_1/job/" + job.get("Id"),
        "country": "Romania",
        "company": company,
    }
    for job in elements
]

publish_or_update(jobs)
publish_logo(
    company, "https://www.weatherford.com/Content/Images/logo-weatherford-text.png"
)
show_jobs(jobs)
