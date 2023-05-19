from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://www.capgemini.com/wp-json/macs/v1/jobs?country=ro-en&size=200"

company = {"company": "Capgemini"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("data")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.get("title")
    job_link = "https://www.capgemini.com/ro-en/jobs/" + job.get("_id") + "/" + job.get("title").replace(" ", "-").lower()
    city = job.get("location")

    if city == None:
        city = "Romania"

    print(job_title + " -> " + city)
    print(job_link)
    
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

logoUrl = "https://prod.ucwe.capgemini.com/ro-en/wp-content/themes/capgemini2020/assets/images/logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))