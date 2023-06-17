from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://www.novartis.com/ro-ro/cariere/cauta-un-job?search_api_fulltext=&country%5B0%5D=LOC_RO&early_talent=All&page=0"

company = {"company": "Novartis"}
finaljobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("table", {"class": "views-view-table"}).find("tbody").find_all("tr")
page = 0

while len(jobs) > 0:
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text.strip()
        job_link = "https://www.novartis.com" + job.find("a").get("href")
        city = job.find("td", {"class": "views-field-field-job-work-location"}).text.strip()
        
        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

    page += 1
    scraper.url = "https://www.novartis.com/ro-ro/cariere/cauta-un-job?search_api_fulltext=&country%5B0%5D=LOC_RO&early_talent=All&page=" + str(page)
    try:
        jobs = rules.getTag("table", {"class": "views-view-table"}).find("tbody").find_all("tr")
    except:
        jobs = list()

print(json.dumps(finaljobs, indent=4))

loadingData(finaljobs, company.get("company"))

logoUrl = "https://www.novartis.com/ro-ro/themes/custom/nvs_arctic/logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))