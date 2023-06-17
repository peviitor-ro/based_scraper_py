from scraper_peviitor import Scraper, Rules,loadingData
import uuid
import json

url = "https://jobs.jobvite.com/pragmaticplay"

company = {"company": "PragmaticPlay"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

jobs = rules.getTags("tr")

for job in jobs:
    try:
        country = job.find("td", {"class": "jv-job-list-location"}).text.split(",")[1].strip()
    except:
        country = None

    if country == "Romania":
        id = uuid.uuid4()
        job_title = job.find("td", {"class": "jv-job-list-name"}).text.strip()
        job_link = "https://jobs.jobvite.com" + job.find("a").get("href")
        city = job.find("td", {"class": "jv-job-list-location"}).text.split(",")[0].strip()

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

logoUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpPW3wkzEqzustHI4sHkexU14oanfsBQrtjMVDMXdT&s"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))