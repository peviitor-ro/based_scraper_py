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
    print(len(jobs))
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("a").text.strip()
        job_link = "https://www.novartis.com" + job.find("a").get("href")
        country = "Romania"
        city = job.find("td", {"class": "views-field-field-job-work-location"}).text.strip()
        company = "Novartis"

        print(job_title + " -> " + city)
        
        finaljobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })

    page += 1
    scraper.url = "https://www.novartis.com/ro-ro/cariere/cauta-un-job?search_api_fulltext=&country%5B0%5D=LOC_RO&early_talent=All&page=" + str(page)
    try:
        jobs = rules.getTag("table", {"class": "views-view-table"}).find("tbody").find_all("tr")
    except:
        jobs = list()

print("Total jobs: " + str(len(finaljobs)))

loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Novartis")

logoUrl = "https://www.novartis.com/ro-ro/themes/custom/nvs_arctic/logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":"Novartis",
        "logo":logoUrl
    }
]))