from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://jobs.webasto.com/search/?createNewAlert=false&q=&optionsFacetsDD_country=RO&optionsFacetsDD_location=&optionsFacetsDD_dept=&optionsFacetsDD_shifttype="

company = {"company": "Webasto"}
finaljobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTag("table", {"id": "searchresults"}).find("tbody").find_all("tr")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("a").text.strip()
    job_link = "https://jobs.webasto.com" + job.find("a").get("href")
    country = "Romania"
    city = job.find("span", {"class": "jobLocation"}).text.split(",")[0].strip()
    company = "Webasto"

    print(job_title + " -> " + city)

    finaljobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city
    })

print("Total jobs: " + str(len(finaljobs)))

loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Webasto")

logoUrl = "https://www.webasto-career.com/build/images/webasto.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":"Webasto",
        "logo":logoUrl
    }
]))
