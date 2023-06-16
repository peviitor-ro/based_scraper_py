from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_45001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=200,locationId=300000000149199,sortBy=POSTING_DATES_DESC"

company = {"company": "Oracle"}
finaljobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = scraper.getJson().get("items")[0].get("requisitionList")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("Title")
    job_link = "https://careers.oracle.com/jobs/#en/sites/jobsearch/job/" + job.get("Id")

    try:
        city = job.get("PrimaryLocation").split(",")[0]
    except:
        city = "Romania"
    
    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print(finaljobs)

loadingData(finaljobs, company.get("company"))

logoUrl = "https://www.oracle.com/a/ocom/img/oracle-rgb-c74634.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))