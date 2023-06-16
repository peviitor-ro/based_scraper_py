from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://ro.cariera.primark.com/loc/romania-posturi-vacante/39017/798549/2"

company = {"company": "Primark"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.url = url
rules = Rules(scraper)

jobs = rules.getTag("div", {"id": "search-results-list"}).findAll("li")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2").text.strip()
    job_link = "https://ro.cariera.primark.com" + job.find("a").get("href")
    city = job.find("span", {"class": "job-location"}).text.split(",")[0].strip()

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "company": company.get("company"),
        "country": "Romania",
        "city": city
    })

print(finalJobs)

loadingData(finalJobs, company.get("company"))

logoUrl = "https://primedia.primark.com/i/primark/logo-primark?w=200"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))