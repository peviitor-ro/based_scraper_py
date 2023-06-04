from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://veoneerromania.teamtailor.com/jobs"

company = {"company": "Veoneer"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("li", {"class": "transition-opacity duration-150 border rounded block-grid-item border-block-base-text border-opacity-15"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("span", {"class": "company-link-style"}).text.strip()
    job_link = job.find("a").get("href")
    city = "Romania"

    print(job_title + " -> " + city)

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://seekvectorlogo.com/wp-content/uploads/2020/02/veoneer-inc-vector-logo-small.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))

