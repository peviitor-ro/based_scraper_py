from scraper_peviitor import Scraper, loadingData
import uuid
import json

url = "https://www.thoughtworks.com/rest/careers/jobs"

company = {"company": "ThoughtWorks"}
finalJobs = list()

scraper = Scraper(url)

jobs = scraper.getJson().get("jobs")

for job in jobs:
    country = job.get("country")

    if country == "Romania":
        id = uuid.uuid4()
        job_title = job.get("name")
        job_link = "https://www.thoughtworks.com/careers/jobs/" + str(job.get("sourceSystemId"))
        city = job.get("location")

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

loadingData(finalJobs, company.get("company"))

logoUrl = "https://www.thoughtworks.com/etc.clientlibs/thoughtworks/clientlibs/clientlib-site/resources/images/thoughtworks-logo.svg"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))