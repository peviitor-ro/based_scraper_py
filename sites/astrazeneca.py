from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://careers.astrazeneca.com/location/romania-jobs/7684/798549/2"

company = {"company": "AstraZeneca"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Accept-Language": "en-GB,en;q=0.9",
})

scraper.url = url
rules = Rules(scraper)

jobs = rules.getTag("section", {"id": "search-results-list"}).findAll("li")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2").text.strip()
    job_link = "https://careers.astrazeneca.com" + job.find("a").get("href")
    city = job.find("span", {"class": "job-location"}).text.split(",")[-1].strip()

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

logoUrl = "https://tbcdn.talentbrew.com/company/7684/img/logo/logo-14641-17887.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))