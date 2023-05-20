from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://careers.danone.com/bin/jobs.json?countries=Romania&locale=en&limit=100"

company = {"company": "Danone"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("results")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = "https://careers.danone.com/en-global/jobs/" + job.get("url")
    city = job.get("city")

    print(job_title + " -> " + city)

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://careers.danone.com/content/dam/danone-corp/hr/global/homepage/logo.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))

