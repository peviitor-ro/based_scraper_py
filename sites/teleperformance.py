from scraper_peviitor import Scraper, loadingData
import uuid
import json

apiUrl = "https://www.teleperformance.com/Umbraco/Api/Careers/GetCareersBase?node=13761&country=Romania&pageSize=100"

company = {"company": "Teleperformance"}
finalJobs = list()

scraper = Scraper(apiUrl)

jobs = scraper.getJson().get("resultado")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = job.get("url")
    city = job.get("location")

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://www.teleperformance.com/media/yn5lcxbl/tp-main-logo-svg.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
