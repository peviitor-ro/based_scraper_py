from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://www.1and1.ro/jobs.json"

company = {"company": "1&1"}  
finalJobs = list()

scraper = Scraper() 

scraper.url = url

jobs = scraper.getJson().get("jobs")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("JobTitle")
    job_link = "https://www.1and1.ro/careers/" + job.get("RefURL")
    country = "Romania"
    city = job.get("Location")

    print(job_title + " -> " + city)
    
    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": country,
        "city": city,
        "company": company.get("company")
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://cdn.website-editor.net/b236a61347464e4b904f5e6b661c2af9/dms3rep/multi/1and1-logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))