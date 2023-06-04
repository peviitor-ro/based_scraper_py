from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://careers.cargill.com/en/search-jobs/Romania/23251/2/798549/46/25/50/2"

company = {"company": "Cargill"}
finalJobs = list()

scraper = Scraper()
scraper.session.headers.update({
    "Accept-Language": "en-GB,en;q=0.9",
})
scraper.url = url
rules = Rules(scraper)

jobs = rules.getTag("section", {"id": "search-results-list"}).find_all("li")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h3").text.strip()
    job_link = "https://careers.cargill.com" + job.find("a").get("href")
    city = job.find("span", {"class": "job-location"}).text.split(",")[0].strip()

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

loadingData(finalJobs, company.get("company"))

logoUrl = "https://tbcdn.talentbrew.com/company/23251/18994/content/logo-full.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))