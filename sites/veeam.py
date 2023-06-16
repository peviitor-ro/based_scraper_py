from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://careers.veeam.com/api/vacancy"

company = {"company": "Veeam"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson()

for job in jobs:
    country = job.get("location")[0].get("country")

    if country == "Romania":
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = job.get("applyUrl")
        city = job.get("location")[0].get("city")

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "country": country,
            "city": city,
            "company": company.get("company")
        })

print(finalJobs) 

loadingData(finalJobs, company.get("company"))

logoUrl = "https://img.veeam.com/careers/logo/veeam/veeam_logo_bg.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))